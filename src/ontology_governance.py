"""Versioned governance for the emergent ontology.

`PROMOTION_REVIEW_READY` is an input to governance, never an activation event.
The lifecycle is deliberately two-stage:

    reviewed alignment
    -> ontology review queue
    -> explicit review decision
    -> immutable ontology version
    -> explicit activation

The registry is domain-neutral and keeps historical versions plus lineage. It does
not create opportunity, payer, route, resource-availability or business truth.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from src.semantic_kernel import SEMANTIC_PRIMITIVES


REVIEW_QUEUE_KIND = "ONTOLOGY_PROMOTION_REVIEW"
REVIEW_ITEM_STATE = "AWAITING_EXPLICIT_REVIEW"
TAXONOMY_PROMOTION = "NOT_PROMOTED"
BUSINESS_PROMOTION = "NOT_PROMOTED"

REVIEW_DECISIONS = frozenset(
    {
        "APPROVE_NEW_CONCEPT_VERSION",
        "DEFER",
        "REJECT",
        "REQUIRE_MERGE_REVIEW",
        "REQUIRE_SPLIT_REVIEW",
        "REQUIRE_RENAME_REVIEW",
    }
)
CHANGE_KINDS = frozenset({"CREATE", "REVISE", "RENAME", "MERGE", "SPLIT", "DEPRECATE"})
VERSION_STATES = frozenset({"ELIGIBLE", "DEPRECATED"})
LINEAGE_RELATIONS = frozenset(
    {"REVISED_FROM", "RENAMED_FROM", "MERGED_FROM", "SPLIT_FROM", "DEPRECATED_BY"}
)
INITIAL_VERSION_CHANGE_KINDS = frozenset({"CREATE", "MERGE", "SPLIT"})
LINEAGE_RELATION_BY_CHANGE_KIND = {
    "REVISE": "REVISED_FROM",
    "RENAME": "RENAMED_FROM",
    "MERGE": "MERGED_FROM",
    "SPLIT": "SPLIT_FROM",
    "DEPRECATE": "DEPRECATED_BY",
}


def _require_text(name: str, value: object) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{name} is required")
    return text


def _require_unique_texts(name: str, values: Sequence[object], *, nonempty: bool = True) -> tuple[str, ...]:
    result = tuple(str(value).strip() for value in values if str(value).strip())
    if nonempty and not result:
        raise ValueError(f"{name} is required")
    if len(result) != len(set(result)):
        raise ValueError(f"{name} must be unique")
    return result


def _iso_datetime(name: str, value: object) -> str:
    text = _require_text(name, value)
    parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return text


@dataclass(frozen=True)
class OntologyConceptVersion:
    concept_id: str
    version: int
    primitive: str
    preferred_label: str
    aliases: tuple[str, ...]
    definition: str
    boundary: str
    counterexamples: tuple[str, ...]
    source_alignment_refs: tuple[str, ...]
    supporting_claim_refs: tuple[str, ...]
    created_from_review_item_id: str
    change_kind: str
    version_state: str
    rationale: str

    def __post_init__(self) -> None:
        _require_text("concept_id", self.concept_id)
        if not isinstance(self.version, int) or isinstance(self.version, bool) or self.version < 1:
            raise ValueError("version must be an integer >= 1")
        if self.primitive not in SEMANTIC_PRIMITIVES:
            raise ValueError(f"unknown semantic primitive: {self.primitive}")
        _require_text("preferred_label", self.preferred_label)
        _require_text("definition", self.definition)
        _require_text("boundary", self.boundary)
        _require_unique_texts("counterexamples", self.counterexamples)
        _require_unique_texts("source_alignment_refs", self.source_alignment_refs)
        _require_unique_texts("supporting_claim_refs", self.supporting_claim_refs)
        _require_text("created_from_review_item_id", self.created_from_review_item_id)
        if self.change_kind not in CHANGE_KINDS:
            raise ValueError(f"unsupported change_kind: {self.change_kind}")
        if self.version_state not in VERSION_STATES:
            raise ValueError(f"unsupported version_state: {self.version_state}")
        if self.change_kind == "CREATE" and self.version != 1:
            raise ValueError("CREATE must use version 1")
        if self.version == 1 and self.change_kind not in INITIAL_VERSION_CHANGE_KINDS:
            raise ValueError("version 1 is only valid for CREATE, MERGE or SPLIT")
        if self.change_kind == "DEPRECATE" and self.version_state != "DEPRECATED":
            raise ValueError("DEPRECATE version must use DEPRECATED state")
        if self.change_kind != "DEPRECATE" and self.version_state != "ELIGIBLE":
            raise ValueError("non-DEPRECATE version must use ELIGIBLE state")
        _require_text("rationale", self.rationale)
        if self.preferred_label in self.aliases:
            raise ValueError("preferred_label must not be repeated as an alias")
        if len(self.aliases) != len(set(self.aliases)):
            raise ValueError("aliases must be unique")

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OntologyReviewDecision:
    review_item_id: str
    decision: str
    reviewer_id: str
    reviewed_at: str
    rationale: str
    proposed_concept_id: str | None = None
    proposed_label: str | None = None

    def __post_init__(self) -> None:
        _require_text("review_item_id", self.review_item_id)
        if self.decision not in REVIEW_DECISIONS:
            raise ValueError(f"unsupported ontology review decision: {self.decision}")
        _require_text("reviewer_id", self.reviewer_id)
        _iso_datetime("reviewed_at", self.reviewed_at)
        _require_text("rationale", self.rationale)
        if self.decision == "APPROVE_NEW_CONCEPT_VERSION":
            _require_text("proposed_concept_id", self.proposed_concept_id)
            _require_text("proposed_label", self.proposed_label)
        elif self.proposed_concept_id is not None or self.proposed_label is not None:
            raise ValueError("proposed concept identity is only allowed for APPROVE_NEW_CONCEPT_VERSION")


def build_ontology_review_queue(observation_review: Mapping[str, Any]) -> dict[str, Any]:
    """Materialize governance work from a conservative observation-review artifact.

    Only PROMOTION_REVIEW_READY assessments enter the queue. The returned queue is
    planning/governance state: it cannot activate or create an ontology node.
    """

    if observation_review.get("schema_version") != "broad-discovery-observation-review.v1":
        raise ValueError("unexpected observation review schema")
    if observation_review.get("taxonomy_promotion") != TAXONOMY_PROMOTION:
        raise ValueError("ontology review must start from non-promoted taxonomy state")
    if observation_review.get("business_promotion") != BUSINESS_PROMOTION:
        raise ValueError("ontology review cannot start from promoted business truth")

    run_id = _require_text("run_id", observation_review.get("run_id"))
    raw_assessments = observation_review.get("assessments")
    if not isinstance(raw_assessments, list):
        raise ValueError("observation review requires assessments[]")

    items: list[dict[str, Any]] = []
    candidate_count = 0
    residual_count = 0
    for raw in raw_assessments:
        if not isinstance(raw, Mapping):
            raise ValueError("assessment must be an object")
        state = _require_text("assessment.state", raw.get("state"))
        if state == "CANDIDATE":
            candidate_count += 1
            continue
        if state == "RESIDUAL":
            residual_count += 1
            continue
        if state != "PROMOTION_REVIEW_READY":
            raise ValueError(f"unsupported assessment state: {state}")
        if raw.get("taxonomy_promotion") != TAXONOMY_PROMOTION:
            raise ValueError("review-ready assessment cannot self-promote taxonomy")
        if raw.get("business_promotion") != BUSINESS_PROMOTION:
            raise ValueError("review-ready assessment cannot self-promote business truth")

        alignment_id = _require_text("alignment_id", raw.get("alignment_id"))
        primitive = _require_text("primitive", raw.get("primitive"))
        if primitive not in SEMANTIC_PRIMITIVES:
            raise ValueError(f"unknown semantic primitive: {primitive}")
        concept = _require_text("candidate_concept", raw.get("candidate_concept"))
        item_id = f"ONTOLOGY_REVIEW::{run_id}::{alignment_id}"
        items.append(
            {
                "review_item_id": item_id,
                "source_review_run_id": run_id,
                "source_alignment_id": alignment_id,
                "candidate_concept": concept,
                "primitive": primitive,
                "definition": _require_text("definition", raw.get("definition")),
                "boundary": _require_text("boundary", raw.get("boundary")),
                "counterexamples": list(_require_unique_texts("counterexamples", raw.get("counterexamples", []))),
                "supporting_claim_refs": list(
                    _require_unique_texts("supporting_claim_refs", raw.get("supporting_claim_refs", []))
                ),
                "supporting_observation_refs": list(
                    _require_unique_texts("supporting_observation_refs", raw.get("supporting_observation_refs", []))
                ),
                "supporting_source_ids": list(
                    _require_unique_texts("supporting_source_ids", raw.get("supporting_source_ids", []))
                ),
                "supporting_actor_ids": list(
                    _require_unique_texts("supporting_actor_ids", raw.get("supporting_actor_ids", []))
                ),
                "supporting_periods": list(
                    _require_unique_texts("supporting_periods", raw.get("supporting_periods", []))
                ),
                "observation_count": int(raw.get("observation_count", 0)),
                "source_count": int(raw.get("source_count", 0)),
                "actor_count": int(raw.get("actor_count", 0)),
                "period_count": int(raw.get("period_count", 0)),
                "epistemic_counts": dict(raw.get("epistemic_counts", {})),
                "review_state": REVIEW_ITEM_STATE,
                "allowed_decisions": sorted(REVIEW_DECISIONS),
                "registry_effect": "NONE_UNTIL_EXPLICIT_REVIEW_DECISION_AND_SEPARATE_ACTIVATION",
                "taxonomy_promotion": TAXONOMY_PROMOTION,
                "business_promotion": BUSINESS_PROMOTION,
            }
        )

    return {
        "queue_kind": REVIEW_QUEUE_KIND,
        "source_review_run_id": run_id,
        "review_ready_count": len(items),
        "candidate_not_queued_count": candidate_count,
        "residual_not_queued_count": residual_count,
        "items": items,
        "active_ontology_changes": 0,
        "taxonomy_promotion": TAXONOMY_PROMOTION,
        "business_promotion": BUSINESS_PROMOTION,
        "truth_boundaries": [
            "PROMOTION_REVIEW_READY_NE_TAXONOMY_PROMOTED",
            "REVIEW_QUEUE_NE_ONTOLOGY_VERSION",
            "ONTOLOGY_VERSION_NE_ACTIVE_TAXONOMY_UNTIL_EXPLICIT_ACTIVATION",
            "MODEL_SUGGESTION_NE_REVIEW_DECISION",
            "ONTOLOGY_CONCEPT_NE_BUSINESS_OPPORTUNITY",
            "UNKNOWN_NE_PASS",
        ],
    }


def review_decision_from_dict(raw: Mapping[str, Any]) -> OntologyReviewDecision:
    allowed = {
        "review_item_id",
        "decision",
        "reviewer_id",
        "reviewed_at",
        "rationale",
        "proposed_concept_id",
        "proposed_label",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise ValueError(f"unknown ontology review decision fields: {sorted(unknown)}")
    return OntologyReviewDecision(
        review_item_id=str(raw.get("review_item_id") or "").strip(),
        decision=str(raw.get("decision") or "").strip(),
        reviewer_id=str(raw.get("reviewer_id") or "").strip(),
        reviewed_at=str(raw.get("reviewed_at") or "").strip(),
        rationale=str(raw.get("rationale") or "").strip(),
        proposed_concept_id=(
            str(raw["proposed_concept_id"]).strip()
            if raw.get("proposed_concept_id") is not None
            else None
        ),
        proposed_label=(
            str(raw["proposed_label"]).strip()
            if raw.get("proposed_label") is not None
            else None
        ),
    )


_SCHEMA = """
CREATE TABLE IF NOT EXISTS ontology_concept_version (
    concept_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    primitive TEXT NOT NULL,
    preferred_label TEXT NOT NULL,
    aliases_json TEXT NOT NULL,
    definition TEXT NOT NULL,
    boundary TEXT NOT NULL,
    counterexamples_json TEXT NOT NULL,
    source_alignment_refs_json TEXT NOT NULL,
    supporting_claim_refs_json TEXT NOT NULL,
    created_from_review_item_id TEXT NOT NULL,
    change_kind TEXT NOT NULL,
    version_state TEXT NOT NULL,
    rationale TEXT NOT NULL,
    PRIMARY KEY (concept_id, version)
);
CREATE TABLE IF NOT EXISTS ontology_activation (
    concept_id TEXT PRIMARY KEY,
    active_version INTEGER NOT NULL,
    activated_by TEXT NOT NULL,
    activated_at TEXT NOT NULL,
    rationale TEXT NOT NULL,
    FOREIGN KEY (concept_id, active_version)
        REFERENCES ontology_concept_version(concept_id, version)
);
CREATE TABLE IF NOT EXISTS ontology_lineage_edge (
    from_concept_id TEXT NOT NULL,
    from_version INTEGER NOT NULL,
    relation TEXT NOT NULL,
    to_concept_id TEXT NOT NULL,
    to_version INTEGER NOT NULL,
    rationale TEXT NOT NULL,
    PRIMARY KEY (from_concept_id, from_version, relation, to_concept_id, to_version),
    FOREIGN KEY (from_concept_id, from_version)
        REFERENCES ontology_concept_version(concept_id, version),
    FOREIGN KEY (to_concept_id, to_version)
        REFERENCES ontology_concept_version(concept_id, version)
);
"""


def _json_tuple(values: Sequence[str]) -> str:
    return json.dumps(list(values), ensure_ascii=False, sort_keys=False, separators=(",", ":"))


def _tuple_from_json(raw: str) -> tuple[str, ...]:
    value = json.loads(raw)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError("stored ontology tuple must be a string list")
    return tuple(value)


class SQLiteOntologyRegistry:
    """Append-versioned ontology registry with explicit activation and lineage."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        if str(path) != ":memory:":
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(path))
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.executescript(_SCHEMA)
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "SQLiteOntologyRegistry":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def register_version(self, spec: OntologyConceptVersion) -> None:
        existing = self.get(spec.concept_id, spec.version)
        if existing is not None:
            if existing != spec:
                raise ValueError("ontology concept version already exists with different content")
            return

        prior_versions = self.versions(spec.concept_id)
        if prior_versions and prior_versions[-1].version_state == "DEPRECATED":
            raise ValueError(
                "deprecated ontology concept history is terminal; create a new concept identity with lineage"
            )
        if spec.version == 1:
            if prior_versions:
                raise ValueError("version 1 cannot be added after concept history exists")
        else:
            if not prior_versions:
                raise ValueError("non-initial version requires existing concept history")
            expected = prior_versions[-1].version + 1
            if spec.version != expected:
                raise ValueError(f"ontology version must be contiguous; expected {expected}")

        if spec.change_kind == "DEPRECATE" and self.active_version(spec.concept_id) is not None:
            raise ValueError(
                "active ontology concept must be explicitly deactivated before deprecation"
            )

        with self.connection:
            self.connection.execute(
                """
                INSERT INTO ontology_concept_version (
                    concept_id, version, primitive, preferred_label, aliases_json,
                    definition, boundary, counterexamples_json, source_alignment_refs_json,
                    supporting_claim_refs_json, created_from_review_item_id, change_kind,
                    version_state, rationale
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    spec.concept_id.strip(),
                    spec.version,
                    spec.primitive,
                    spec.preferred_label.strip(),
                    _json_tuple(spec.aliases),
                    spec.definition.strip(),
                    spec.boundary.strip(),
                    _json_tuple(spec.counterexamples),
                    _json_tuple(spec.source_alignment_refs),
                    _json_tuple(spec.supporting_claim_refs),
                    spec.created_from_review_item_id.strip(),
                    spec.change_kind,
                    spec.version_state,
                    spec.rationale.strip(),
                ),
            )

    def get(self, concept_id: str, version: int) -> OntologyConceptVersion | None:
        row = self.connection.execute(
            "SELECT * FROM ontology_concept_version WHERE concept_id = ? AND version = ?",
            (concept_id, version),
        ).fetchone()
        if row is None:
            return None
        return OntologyConceptVersion(
            concept_id=row["concept_id"],
            version=row["version"],
            primitive=row["primitive"],
            preferred_label=row["preferred_label"],
            aliases=_tuple_from_json(row["aliases_json"]),
            definition=row["definition"],
            boundary=row["boundary"],
            counterexamples=_tuple_from_json(row["counterexamples_json"]),
            source_alignment_refs=_tuple_from_json(row["source_alignment_refs_json"]),
            supporting_claim_refs=_tuple_from_json(row["supporting_claim_refs_json"]),
            created_from_review_item_id=row["created_from_review_item_id"],
            change_kind=row["change_kind"],
            version_state=row["version_state"],
            rationale=row["rationale"],
        )

    def versions(self, concept_id: str) -> tuple[OntologyConceptVersion, ...]:
        rows = self.connection.execute(
            "SELECT version FROM ontology_concept_version WHERE concept_id = ? ORDER BY version",
            (concept_id,),
        ).fetchall()
        return tuple(self.get(concept_id, int(row["version"])) for row in rows)

    def _lineage_rows_for_version(self, spec: OntologyConceptVersion) -> tuple[sqlite3.Row, ...]:
        relation = LINEAGE_RELATION_BY_CHANGE_KIND.get(spec.change_kind)
        if relation is None:
            return ()
        if spec.change_kind == "DEPRECATE":
            rows = self.connection.execute(
                """
                SELECT * FROM ontology_lineage_edge
                WHERE relation = ? AND to_concept_id = ? AND to_version = ?
                ORDER BY from_concept_id, from_version
                """,
                (relation, spec.concept_id, spec.version),
            ).fetchall()
        else:
            rows = self.connection.execute(
                """
                SELECT * FROM ontology_lineage_edge
                WHERE relation = ? AND from_concept_id = ? AND from_version = ?
                ORDER BY to_concept_id, to_version
                """,
                (relation, spec.concept_id, spec.version),
            ).fetchall()
        return tuple(rows)

    def _validate_version_lineage(self, spec: OntologyConceptVersion) -> None:
        if spec.change_kind == "CREATE":
            return

        relation = LINEAGE_RELATION_BY_CHANGE_KIND[spec.change_kind]
        rows = self._lineage_rows_for_version(spec)
        if not rows:
            raise ValueError(f"{spec.change_kind} requires explicit {relation} lineage")

        if spec.change_kind in {"REVISE", "RENAME"}:
            if not any(
                row["to_concept_id"] == spec.concept_id
                and int(row["to_version"]) == spec.version - 1
                for row in rows
            ):
                raise ValueError(
                    f"{spec.change_kind} must point to the immediately previous version of the same concept"
                )
            return

        if spec.change_kind == "DEPRECATE":
            if not any(
                row["from_concept_id"] == spec.concept_id
                and int(row["from_version"]) == spec.version - 1
                for row in rows
            ):
                raise ValueError(
                    "DEPRECATE must be linked from the immediately previous version by DEPRECATED_BY"
                )
            return

        if spec.change_kind == "MERGE":
            parent_concepts = {str(row["to_concept_id"]) for row in rows}
            if len(parent_concepts) < 2:
                raise ValueError("MERGE requires MERGED_FROM lineage to at least two parent concepts")
            return

        if spec.change_kind == "SPLIT":
            for row in rows:
                sibling_rows = self.connection.execute(
                    """
                    SELECT DISTINCT from_concept_id, from_version
                    FROM ontology_lineage_edge
                    WHERE relation = 'SPLIT_FROM' AND to_concept_id = ? AND to_version = ?
                    """,
                    (row["to_concept_id"], int(row["to_version"])),
                ).fetchall()
                if len({str(sibling["from_concept_id"]) for sibling in sibling_rows}) >= 2:
                    return
            raise ValueError(
                "SPLIT requires at least two child concept identities linked to a shared source version"
            )

    def validate_lifecycle(self) -> None:
        rows = self.connection.execute(
            "SELECT concept_id, version FROM ontology_concept_version ORDER BY concept_id, version"
        ).fetchall()
        for row in rows:
            spec = self.get(str(row["concept_id"]), int(row["version"]))
            if spec is None:
                raise ValueError("ontology registry lost a referenced concept version")
            self._validate_version_lineage(spec)

    def activate(
        self,
        concept_id: str,
        version: int,
        *,
        activated_by: str,
        activated_at: str,
        rationale: str,
    ) -> None:
        spec = self.get(concept_id, version)
        if spec is None:
            raise KeyError((concept_id, version))
        if spec.version_state != "ELIGIBLE":
            raise ValueError("deprecated ontology version cannot be activated")
        history = self.versions(concept_id)
        if history and history[-1].version_state == "DEPRECATED":
            raise ValueError("deprecated ontology concept cannot reactivate an older eligible version")
        self._validate_version_lineage(spec)
        actor = _require_text("activated_by", activated_by)
        at = _iso_datetime("activated_at", activated_at)
        why = _require_text("rationale", rationale)
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO ontology_activation (concept_id, active_version, activated_by, activated_at, rationale)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(concept_id) DO UPDATE SET
                    active_version=excluded.active_version,
                    activated_by=excluded.activated_by,
                    activated_at=excluded.activated_at,
                    rationale=excluded.rationale
                """,
                (concept_id, version, actor, at, why),
            )

    def deactivate(self, concept_id: str) -> None:
        with self.connection:
            self.connection.execute("DELETE FROM ontology_activation WHERE concept_id = ?", (concept_id,))

    def active_version(self, concept_id: str) -> OntologyConceptVersion | None:
        row = self.connection.execute(
            "SELECT active_version FROM ontology_activation WHERE concept_id = ?",
            (concept_id,),
        ).fetchone()
        if row is None:
            return None
        return self.get(concept_id, int(row["active_version"]))

    def add_lineage(
        self,
        *,
        from_concept_id: str,
        from_version: int,
        relation: str,
        to_concept_id: str,
        to_version: int,
        rationale: str,
    ) -> None:
        if relation not in LINEAGE_RELATIONS:
            raise ValueError(f"unsupported ontology lineage relation: {relation}")
        from_spec = self.get(from_concept_id, from_version)
        if from_spec is None:
            raise KeyError((from_concept_id, from_version))
        to_spec = self.get(to_concept_id, to_version)
        if to_spec is None:
            raise KeyError((to_concept_id, to_version))
        if (from_concept_id, from_version) == (to_concept_id, to_version):
            raise ValueError("ontology lineage cannot self-reference the same concept version")

        if relation == "REVISED_FROM":
            if from_spec.change_kind != "REVISE":
                raise ValueError("REVISED_FROM must originate from a REVISE version")
            if from_concept_id != to_concept_id or from_version != to_version + 1:
                raise ValueError("REVISED_FROM must point to the immediately previous version of the same concept")
        elif relation == "RENAMED_FROM":
            if from_spec.change_kind != "RENAME":
                raise ValueError("RENAMED_FROM must originate from a RENAME version")
            if from_concept_id != to_concept_id or from_version != to_version + 1:
                raise ValueError("RENAMED_FROM must point to the immediately previous version of the same concept")
        elif relation == "MERGED_FROM":
            if from_spec.change_kind != "MERGE":
                raise ValueError("MERGED_FROM must originate from a MERGE version")
        elif relation == "SPLIT_FROM":
            if from_spec.change_kind != "SPLIT":
                raise ValueError("SPLIT_FROM must originate from a SPLIT version")
        elif relation == "DEPRECATED_BY":
            if to_spec.change_kind != "DEPRECATE":
                raise ValueError("DEPRECATED_BY must point to a DEPRECATE version")
            if from_concept_id != to_concept_id or to_version != from_version + 1:
                raise ValueError("DEPRECATED_BY must connect adjacent versions of the same concept")

        why = _require_text("lineage rationale", rationale)
        with self.connection:
            self.connection.execute(
                """
                INSERT OR IGNORE INTO ontology_lineage_edge (
                    from_concept_id, from_version, relation, to_concept_id, to_version, rationale
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (from_concept_id, from_version, relation, to_concept_id, to_version, why),
            )

    def lineage(self) -> tuple[dict[str, Any], ...]:
        rows = self.connection.execute(
            """
            SELECT from_concept_id, from_version, relation, to_concept_id, to_version, rationale
            FROM ontology_lineage_edge
            ORDER BY from_concept_id, from_version, relation, to_concept_id, to_version
            """
        ).fetchall()
        return tuple(dict(row) for row in rows)

    def snapshot(self) -> dict[str, Any]:
        self.validate_lifecycle()
        version_rows = self.connection.execute(
            "SELECT concept_id, version FROM ontology_concept_version ORDER BY concept_id, version"
        ).fetchall()
        activation_rows = self.connection.execute(
            "SELECT concept_id, active_version, activated_by, activated_at, rationale FROM ontology_activation ORDER BY concept_id"
        ).fetchall()
        return {
            "schema_version": "ontology-registry-snapshot.v1",
            "version_count": len(version_rows),
            "active_concept_count": len(activation_rows),
            "versions": [self.get(row["concept_id"], int(row["version"])).as_dict() for row in version_rows],
            "activations": [dict(row) for row in activation_rows],
            "lineage": list(self.lineage()),
            "lineage_integrity": "VALIDATED",
            "business_promotion": BUSINESS_PROMOTION,
        }


def approved_new_concept_version(
    review_item: Mapping[str, Any],
    decision: OntologyReviewDecision,
) -> OntologyConceptVersion:
    """Convert an explicit approval into an immutable *inactive* version-1 node."""

    if review_item.get("review_state") != REVIEW_ITEM_STATE:
        raise ValueError("review item must be awaiting explicit review")
    if review_item.get("taxonomy_promotion") != TAXONOMY_PROMOTION:
        raise ValueError("review item cannot already be taxonomy-promoted")
    if review_item.get("business_promotion") != BUSINESS_PROMOTION:
        raise ValueError("review item cannot carry business promotion")
    item_id = _require_text("review_item_id", review_item.get("review_item_id"))
    if decision.review_item_id != item_id:
        raise ValueError("review decision does not match review item")
    if decision.decision != "APPROVE_NEW_CONCEPT_VERSION":
        raise ValueError("only APPROVE_NEW_CONCEPT_VERSION creates a new concept version")
    primitive = _require_text("primitive", review_item.get("primitive"))
    if primitive not in SEMANTIC_PRIMITIVES:
        raise ValueError(f"unknown semantic primitive: {primitive}")

    return OntologyConceptVersion(
        concept_id=_require_text("proposed_concept_id", decision.proposed_concept_id),
        version=1,
        primitive=primitive,
        preferred_label=_require_text("proposed_label", decision.proposed_label),
        aliases=(),
        definition=_require_text("definition", review_item.get("definition")),
        boundary=_require_text("boundary", review_item.get("boundary")),
        counterexamples=_require_unique_texts("counterexamples", review_item.get("counterexamples", [])),
        source_alignment_refs=(_require_text("source_alignment_id", review_item.get("source_alignment_id")),),
        supporting_claim_refs=_require_unique_texts(
            "supporting_claim_refs", review_item.get("supporting_claim_refs", [])
        ),
        created_from_review_item_id=item_id,
        change_kind="CREATE",
        version_state="ELIGIBLE",
        rationale=decision.rationale,
    )


GOVERNING_INVARIANTS = (
    "PROMOTION_REVIEW_READY_NE_TAXONOMY_PROMOTED",
    "REVIEW_QUEUE_NE_ONTOLOGY_VERSION",
    "EXPLICIT_REVIEW_DECISION_NE_ACTIVE_TAXONOMY",
    "ONTOLOGY_VERSION_REQUIRES_EXPLICIT_ACTIVATION",
    "ONTOLOGY_VERSION_IS_APPEND_ONLY",
    "MERGE_AND_SPLIT_MAY_CREATE_NEW_STABLE_CONCEPT_ID_AT_VERSION_1",
    "REVISE_RENAME_MERGE_SPLIT_DEPRECATE_REQUIRE_EXPLICIT_LINEAGE",
    "ORPHAN_LIFECYCLE_VERSION_CANNOT_BE_ACTIVATED_OR_SNAPSHOTTED",
    "MERGE_REQUIRES_AT_LEAST_TWO_PARENT_CONCEPTS",
    "SPLIT_REQUIRES_AT_LEAST_TWO_CHILD_CONCEPT_IDENTITIES",
    "DEPRECATION_REQUIRES_EXPLICIT_DEACTIVATION",
    "DEPRECATED_CONCEPT_HISTORY_IS_TERMINAL",
    "DEPRECATED_CONCEPT_CANNOT_REACTIVATE_OLDER_ELIGIBLE_VERSION",
    "MODEL_SUGGESTION_NE_REVIEW_DECISION",
    "ONTOLOGY_CONCEPT_NE_BUSINESS_OPPORTUNITY",
    "UNKNOWN_NE_PASS",
)
