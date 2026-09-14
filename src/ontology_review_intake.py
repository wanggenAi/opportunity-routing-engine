"""Auditable intake for explicit ontology review decisions.

This layer binds a human/operator decision to the exact review item content that was
examined. It is intentionally separate from ontology version creation and activation:
recording a decision here never mutates ``SQLiteOntologyRegistry`` and never creates
business truth.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Mapping

from src.ontology_governance import (
    BUSINESS_PROMOTION,
    REVIEW_DECISIONS,
    REVIEW_ITEM_STATE,
    TAXONOMY_PROMOTION,
    OntologyReviewDecision,
)

SCHEMA_VERSION = "ontology-review-decision-intake.v1"
REGISTRY_EFFECT = "NONE_DECISION_INTAKE_DOES_NOT_CREATE_OR_ACTIVATE_ONTOLOGY_VERSION"

_REVISION_DECISIONS = frozenset(
    {
        "REQUIRE_MERGE_REVIEW",
        "REQUIRE_SPLIT_REVIEW",
        "REQUIRE_RENAME_REVIEW",
    }
)
_TERMINAL_DECISIONS = frozenset({"APPROVE_NEW_CONCEPT_VERSION", "REJECT"}) | _REVISION_DECISIONS
_ALLOWED_FIELDS = frozenset(
    {
        "decision_id",
        "review_item_id",
        "decision",
        "review_outcome",
        "reviewer_id",
        "reviewed_at",
        "rationale",
        "review_provenance_ref",
        "supporting_evidence_refs",
        "reviewed_boundary",
        "reviewed_counterexamples",
        "proposed_concept_id",
        "proposed_label",
        "revision_instruction",
    }
)
_FORBIDDEN_TRUTH_FIELDS = frozenset(
    {
        "payer",
        "payer_confirmed",
        "paid_need",
        "route_testable",
        "transaction_ready",
        "business_promoted",
        "taxonomy_promoted",
        "active_version",
        "activated_at",
    }
)


def _require_text(name: str, value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} is required")
    return value.strip()


def _optional_text(name: str, value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string when provided")
    return value.strip()


def _unique_texts(name: str, values: object, *, nonempty: bool = True) -> tuple[str, ...]:
    if not isinstance(values, (list, tuple)):
        raise ValueError(f"{name} must be an array of strings")
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise ValueError(f"{name} must contain only non-empty strings")
    result = tuple(value.strip() for value in values)
    if nonempty and not result:
        raise ValueError(f"{name} is required")
    if len(result) != len(set(result)):
        raise ValueError(f"{name} must be unique")
    return result


def _review_time(value: object) -> str:
    text = _require_text("reviewed_at", value)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("reviewed_at must be ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("reviewed_at must be timezone-aware")
    return text


def _utc_iso(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("reviewed_at must be timezone-aware")
    return parsed.astimezone(timezone.utc).isoformat()


def review_outcome_for_decision(decision: str) -> str:
    if decision == "APPROVE_NEW_CONCEPT_VERSION":
        return "ACCEPT"
    if decision == "REJECT":
        return "REJECT"
    if decision == "DEFER":
        return "DEFER"
    if decision in _REVISION_DECISIONS:
        return "REVISE"
    raise ValueError(f"unsupported ontology review decision: {decision}")


@dataclass(frozen=True)
class OntologyReviewDecisionEvent:
    decision_id: str
    review_item_id: str
    decision: str
    review_outcome: str
    reviewer_id: str
    reviewed_at: str
    rationale: str
    review_provenance_ref: str
    supporting_evidence_refs: tuple[str, ...]
    reviewed_boundary: str
    reviewed_counterexamples: tuple[str, ...]
    proposed_concept_id: str | None = None
    proposed_label: str | None = None
    revision_instruction: str | None = None

    def __post_init__(self) -> None:
        _require_text("decision_id", self.decision_id)
        _require_text("review_item_id", self.review_item_id)
        if self.decision not in REVIEW_DECISIONS:
            raise ValueError(f"unsupported ontology review decision: {self.decision}")
        expected_outcome = review_outcome_for_decision(self.decision)
        if self.review_outcome != expected_outcome:
            raise ValueError(
                f"review_outcome must be {expected_outcome} for decision {self.decision}"
            )
        _require_text("reviewer_id", self.reviewer_id)
        _review_time(self.reviewed_at)
        _require_text("rationale", self.rationale)
        _require_text("review_provenance_ref", self.review_provenance_ref)
        _unique_texts("supporting_evidence_refs", self.supporting_evidence_refs)
        _require_text("reviewed_boundary", self.reviewed_boundary)
        _unique_texts("reviewed_counterexamples", self.reviewed_counterexamples)

        if self.decision == "APPROVE_NEW_CONCEPT_VERSION":
            _require_text("proposed_concept_id", self.proposed_concept_id)
            _require_text("proposed_label", self.proposed_label)
        elif self.proposed_concept_id is not None or self.proposed_label is not None:
            raise ValueError(
                "proposed concept identity is only allowed for APPROVE_NEW_CONCEPT_VERSION"
            )

        if self.decision in _REVISION_DECISIONS:
            _require_text("revision_instruction", self.revision_instruction)
        elif self.revision_instruction is not None:
            raise ValueError("revision_instruction is only allowed for revision decisions")

    def as_governance_decision(self) -> OntologyReviewDecision:
        """Project the audited event into the version-governance decision type.

        Projection does not register a version and does not activate anything.
        """
        return OntologyReviewDecision(
            review_item_id=self.review_item_id,
            decision=self.decision,
            reviewer_id=self.reviewer_id,
            reviewed_at=self.reviewed_at,
            rationale=self.rationale,
            proposed_concept_id=self.proposed_concept_id,
            proposed_label=self.proposed_label,
        )

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def review_decision_event_from_record(record: Mapping[str, object]) -> OntologyReviewDecisionEvent:
    keys = set(record)
    forbidden = sorted(keys & _FORBIDDEN_TRUTH_FIELDS)
    if forbidden:
        raise ValueError(
            "commercial/activation truth fields are not accepted: " + ",".join(forbidden)
        )
    unknown = sorted(keys - _ALLOWED_FIELDS)
    if unknown:
        raise ValueError("unknown ontology review intake fields: " + ",".join(unknown))

    decision = _require_text("decision", record.get("decision"))
    expected_outcome = review_outcome_for_decision(decision)
    outcome = _require_text("review_outcome", record.get("review_outcome"))
    if outcome != expected_outcome:
        raise ValueError(f"review_outcome must be {expected_outcome} for decision {decision}")

    return OntologyReviewDecisionEvent(
        decision_id=_require_text("decision_id", record.get("decision_id")),
        review_item_id=_require_text("review_item_id", record.get("review_item_id")),
        decision=decision,
        review_outcome=outcome,
        reviewer_id=_require_text("reviewer_id", record.get("reviewer_id")),
        reviewed_at=_review_time(record.get("reviewed_at")),
        rationale=_require_text("rationale", record.get("rationale")),
        review_provenance_ref=_require_text(
            "review_provenance_ref", record.get("review_provenance_ref")
        ),
        supporting_evidence_refs=_unique_texts(
            "supporting_evidence_refs", record.get("supporting_evidence_refs")
        ),
        reviewed_boundary=_require_text("reviewed_boundary", record.get("reviewed_boundary")),
        reviewed_counterexamples=_unique_texts(
            "reviewed_counterexamples", record.get("reviewed_counterexamples")
        ),
        proposed_concept_id=_optional_text(
            "proposed_concept_id", record.get("proposed_concept_id")
        ),
        proposed_label=_optional_text("proposed_label", record.get("proposed_label")),
        revision_instruction=_optional_text(
            "revision_instruction", record.get("revision_instruction")
        ),
    )


def records_from_path(path: str | Path, *, format: str = "auto") -> Iterator[Mapping[str, object]]:
    input_path = Path(path)
    text = input_path.read_text(encoding="utf-8")
    selected = format
    if selected == "auto":
        selected = "jsonl" if input_path.suffix.lower() in {".jsonl", ".ndjson"} else "json"

    if selected == "jsonl":
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid jsonl line {line_number}") from exc
            if not isinstance(item, Mapping):
                raise ValueError(f"jsonl line {line_number} must be an object")
            yield item
        return

    if selected == "json":
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("invalid json input") from exc
        if isinstance(payload, Mapping):
            yield payload
            return
        if isinstance(payload, list):
            for index, item in enumerate(payload):
                if not isinstance(item, Mapping):
                    raise ValueError(f"json item {index} must be an object")
                yield item
            return
        raise ValueError("json input must be an object or array of objects")

    raise ValueError("format must be auto, json or jsonl")


def _queue_texts(item: Mapping[str, object], key: str, *, nonempty: bool = True) -> tuple[str, ...]:
    return _unique_texts(key, item.get(key, []), nonempty=nonempty)


def review_item_fingerprint(review_item: Mapping[str, object]) -> str:
    """Hash the full JSON review item so any stale-input drift remains visible."""
    _require_text("review_item_id", review_item.get("review_item_id"))
    try:
        canonical = json.dumps(
            dict(review_item),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("review item must be JSON-serializable") from exc
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_review_event_against_item(
    event: OntologyReviewDecisionEvent,
    review_item: Mapping[str, object],
) -> OntologyReviewDecision:
    """Fail closed unless the event explicitly re-attests the queue item's evidence boundary."""
    if _require_text("review_state", review_item.get("review_state")) != REVIEW_ITEM_STATE:
        raise ValueError("review item is not awaiting explicit review")
    if review_item.get("taxonomy_promotion") != TAXONOMY_PROMOTION:
        raise ValueError("review item already claims taxonomy promotion")
    if review_item.get("business_promotion") != BUSINESS_PROMOTION:
        raise ValueError("review item already claims business promotion")

    item_id = _require_text("review_item_id", review_item.get("review_item_id"))
    if event.review_item_id != item_id:
        raise ValueError("review_item_id does not match reviewed queue item")

    allowed_decisions = set(_queue_texts(review_item, "allowed_decisions"))
    if event.decision not in allowed_decisions:
        raise ValueError("decision is not allowed by this review item")

    boundary = _require_text("boundary", review_item.get("boundary"))
    if event.reviewed_boundary != boundary:
        raise ValueError("reviewed_boundary does not match review item boundary")

    counterexamples = _queue_texts(review_item, "counterexamples")
    if event.reviewed_counterexamples != counterexamples:
        raise ValueError("reviewed_counterexamples do not match review item counterexamples")

    claim_refs = _queue_texts(review_item, "supporting_claim_refs")
    observation_refs = _queue_texts(review_item, "supporting_observation_refs")
    evidence_universe = set(claim_refs) | set(observation_refs)
    unknown_refs = sorted(set(event.supporting_evidence_refs) - evidence_universe)
    if unknown_refs:
        raise ValueError(
            "supporting_evidence_refs are not present in the review item: "
            + ",".join(unknown_refs)
        )

    if event.decision == "APPROVE_NEW_CONCEPT_VERSION":
        missing_claims = sorted(set(claim_refs) - set(event.supporting_evidence_refs))
        if missing_claims:
            raise ValueError(
                "approval must explicitly reference every supporting claim: "
                + ",".join(missing_claims)
            )

    return event.as_governance_decision()


def review_items_by_id(queue: Mapping[str, object]) -> dict[str, Mapping[str, object]]:
    if queue.get("queue_kind") != "ONTOLOGY_PROMOTION_REVIEW":
        raise ValueError("unexpected ontology review queue kind")
    if queue.get("taxonomy_promotion") != TAXONOMY_PROMOTION:
        raise ValueError("review queue must remain non-promoted taxonomy state")
    if queue.get("business_promotion") != BUSINESS_PROMOTION:
        raise ValueError("review queue must remain non-promoted business state")
    if queue.get("active_ontology_changes") != 0:
        raise ValueError("review queue must not contain active ontology changes")
    items = queue.get("items")
    if not isinstance(items, list):
        raise ValueError("review queue requires items[]")
    result: dict[str, Mapping[str, object]] = {}
    for item in items:
        if not isinstance(item, Mapping):
            raise ValueError("review queue item must be an object")
        item_id = _require_text("review_item_id", item.get("review_item_id"))
        if item.get("registry_effect") != (
            "NONE_UNTIL_EXPLICIT_REVIEW_DECISION_AND_SEPARATE_ACTIVATION"
        ):
            raise ValueError("review queue item has an unexpected registry effect")
        if item_id in result:
            raise ValueError(f"duplicate review_item_id: {item_id}")
        result[item_id] = item
    return result


_SCHEMA = """
CREATE TABLE IF NOT EXISTS ontology_review_decision_event (
    sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    decision_id TEXT NOT NULL UNIQUE,
    review_item_id TEXT NOT NULL,
    review_item_fingerprint TEXT NOT NULL,
    decision TEXT NOT NULL,
    review_outcome TEXT NOT NULL,
    reviewer_id TEXT NOT NULL,
    reviewed_at TEXT NOT NULL,
    rationale TEXT NOT NULL,
    review_provenance_ref TEXT NOT NULL,
    supporting_evidence_refs_json TEXT NOT NULL,
    reviewed_boundary TEXT NOT NULL,
    reviewed_counterexamples_json TEXT NOT NULL,
    proposed_concept_id TEXT,
    proposed_label TEXT,
    revision_instruction TEXT
);

CREATE INDEX IF NOT EXISTS idx_ontology_review_decision_item
ON ontology_review_decision_event(review_item_id, reviewed_at, sequence_id);
"""


def _event_payload(event: OntologyReviewDecisionEvent) -> dict[str, object]:
    payload = event.as_dict()
    payload["reviewed_at"] = _utc_iso(event.reviewed_at)
    payload["supporting_evidence_refs"] = list(event.supporting_evidence_refs)
    payload["reviewed_counterexamples"] = list(event.reviewed_counterexamples)
    return payload


def _event_identity(event: OntologyReviewDecisionEvent) -> str:
    canonical = json.dumps(
        _event_payload(event), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class SQLiteOntologyReviewDecisionStore:
    """Append-only review ledger. It deliberately has no ontology-registry handle."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        if self.path != Path(":memory:"):
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.path))
        self.connection.row_factory = sqlite3.Row
        self.connection.executescript(_SCHEMA)
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "SQLiteOntologyReviewDecisionStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @staticmethod
    def _event_from_row(row: sqlite3.Row) -> OntologyReviewDecisionEvent:
        evidence = json.loads(row["supporting_evidence_refs_json"])
        counterexamples = json.loads(row["reviewed_counterexamples_json"])
        return OntologyReviewDecisionEvent(
            decision_id=row["decision_id"],
            review_item_id=row["review_item_id"],
            decision=row["decision"],
            review_outcome=row["review_outcome"],
            reviewer_id=row["reviewer_id"],
            reviewed_at=row["reviewed_at"],
            rationale=row["rationale"],
            review_provenance_ref=row["review_provenance_ref"],
            supporting_evidence_refs=_unique_texts("supporting_evidence_refs", evidence),
            reviewed_boundary=row["reviewed_boundary"],
            reviewed_counterexamples=_unique_texts(
                "reviewed_counterexamples", counterexamples
            ),
            proposed_concept_id=row["proposed_concept_id"],
            proposed_label=row["proposed_label"],
            revision_instruction=row["revision_instruction"],
        )

    def _row_for_decision(self, decision_id: str) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM ontology_review_decision_event WHERE decision_id = ?",
            (decision_id,),
        ).fetchone()

    def get(self, decision_id: str) -> OntologyReviewDecisionEvent | None:
        row = self._row_for_decision(decision_id)
        return None if row is None else self._event_from_row(row)

    def events(
        self, review_item_id: str | None = None
    ) -> tuple[OntologyReviewDecisionEvent, ...]:
        if review_item_id is None:
            rows = self.connection.execute(
                "SELECT * FROM ontology_review_decision_event ORDER BY reviewed_at, sequence_id"
            ).fetchall()
        else:
            rows = self.connection.execute(
                """
                SELECT * FROM ontology_review_decision_event
                WHERE review_item_id = ? ORDER BY reviewed_at, sequence_id
                """,
                (review_item_id,),
            ).fetchall()
        return tuple(self._event_from_row(row) for row in rows)

    def append(
        self,
        event: OntologyReviewDecisionEvent,
        review_item: Mapping[str, object],
    ) -> None:
        validate_review_event_against_item(event, review_item)
        fingerprint = review_item_fingerprint(review_item)

        existing_row = self._row_for_decision(event.decision_id)
        if existing_row is not None:
            existing = self._event_from_row(existing_row)
            if _event_identity(existing) != _event_identity(event):
                raise ValueError("decision_id already exists with different content")
            if existing_row["review_item_fingerprint"] != fingerprint:
                raise ValueError("review item changed since the decision was recorded")
            return

        history = self.events(event.review_item_id)
        if history:
            latest_time = max(_utc_iso(record.reviewed_at) for record in history)
            if _utc_iso(event.reviewed_at) < latest_time:
                raise ValueError("reviewed_at cannot move backwards for a review item")
            if any(record.decision in _TERMINAL_DECISIONS for record in history):
                raise ValueError("review item already has a terminal decision")

        payload = _event_payload(event)
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO ontology_review_decision_event (
                    decision_id, review_item_id, review_item_fingerprint, decision,
                    review_outcome, reviewer_id, reviewed_at, rationale,
                    review_provenance_ref, supporting_evidence_refs_json,
                    reviewed_boundary, reviewed_counterexamples_json,
                    proposed_concept_id, proposed_label, revision_instruction
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["decision_id"],
                    payload["review_item_id"],
                    fingerprint,
                    payload["decision"],
                    payload["review_outcome"],
                    payload["reviewer_id"],
                    payload["reviewed_at"],
                    payload["rationale"],
                    payload["review_provenance_ref"],
                    json.dumps(
                        payload["supporting_evidence_refs"],
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    payload["reviewed_boundary"],
                    json.dumps(
                        payload["reviewed_counterexamples"],
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    payload["proposed_concept_id"],
                    payload["proposed_label"],
                    payload["revision_instruction"],
                ),
            )

    def snapshot(self) -> dict[str, object]:
        rows = self.connection.execute(
            "SELECT * FROM ontology_review_decision_event ORDER BY reviewed_at, sequence_id"
        ).fetchall()
        events: list[dict[str, object]] = []
        review_items: set[str] = set()
        terminal_count = 0
        for row in rows:
            event = self._event_from_row(row)
            payload = event.as_dict()
            payload["review_item_fingerprint"] = row["review_item_fingerprint"]
            events.append(payload)
            review_items.add(event.review_item_id)
            if event.decision in _TERMINAL_DECISIONS:
                terminal_count += 1
        return {
            "schema_version": SCHEMA_VERSION,
            "decision_event_count": len(events),
            "review_item_count": len(review_items),
            "terminal_decision_count": terminal_count,
            "events": events,
            "active_ontology_changes": 0,
            "registry_effect": REGISTRY_EFFECT,
            "taxonomy_promotion": TAXONOMY_PROMOTION,
            "business_promotion": BUSINESS_PROMOTION,
            "truth_boundaries": [
                "REVIEW_DECISION_EVENT_NE_ONTOLOGY_VERSION",
                "REVIEW_DECISION_EVENT_NE_ACTIVE_TAXONOMY",
                "DECISION_INTAKE_NE_BUSINESS_PROMOTION",
                "REVIEW_ITEM_CONTENT_MUST_BE_REATTESTED",
                "APPROVAL_MUST_REFERENCE_ALL_SUPPORTING_CLAIMS",
                "REVIEW_HISTORY_IS_APPEND_ONLY",
                "UNKNOWN_NE_PASS",
            ],
        }


GOVERNING_INVARIANTS = (
    "EXPLICIT_REVIEW_DECISION_REQUIRES_REVIEWER_AND_PROVENANCE",
    "EXPLICIT_REVIEW_DECISION_REQUIRES_TIMEZONE_AWARE_TIME",
    "EXPLICIT_REVIEW_DECISION_REATTESTS_BOUNDARY_AND_COUNTEREXAMPLES",
    "EXPLICIT_REVIEW_DECISION_REQUIRES_SUPPORTING_EVIDENCE_REFS",
    "APPROVAL_REQUIRES_ALL_SUPPORTING_CLAIM_REFS",
    "REVIEW_DECISION_HISTORY_IS_APPEND_ONLY",
    "REVIEW_DECISION_NE_ONTOLOGY_VERSION",
    "REVIEW_DECISION_NE_ONTOLOGY_ACTIVATION",
    "REVIEW_DECISION_NE_BUSINESS_PROMOTION",
    "UNKNOWN_NE_PASS",
)
