"""Persistent composition runs linking capability graph snapshots to requirement versions.

A composition run proves only structural capability coverage under explicit inputs. It
does not prove demand truth, payer commitment, counterpart consent, access, safety, or
transactionability.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.capability_graph_store import CapabilityMaterialization, SQLiteCapabilityGraphStore
from src.live_resource_signals import EvidenceStatus
from src.requirement_bundle_registry import RequirementBundleSpec
from src.resource_composition import (
    CapabilityContribution,
    CompositionState,
    ResourceCompositionHypothesis,
    generate_composition_hypotheses,
)


_SCHEMA = """
CREATE TABLE IF NOT EXISTS composition_run (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    input_fingerprint TEXT NOT NULL UNIQUE,
    materialization_id INTEGER NOT NULL,
    graph_ruleset_fingerprint TEXT NOT NULL,
    graph_observation_snapshot_fingerprint TEXT NOT NULL,
    bundle_id TEXT NOT NULL,
    bundle_version INTEGER NOT NULL,
    bundle_source_ref TEXT NOT NULL,
    bundle_rationale TEXT NOT NULL,
    bundle_fingerprint TEXT NOT NULL,
    as_of TEXT NOT NULL,
    max_age_seconds INTEGER NOT NULL,
    max_actors INTEGER NOT NULL,
    max_hypotheses INTEGER NOT NULL,
    hypothesis_count INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_composition_run_bundle
ON composition_run(bundle_id, bundle_version, run_id);

CREATE TABLE IF NOT EXISTS composition_hypothesis_snapshot (
    run_id INTEGER NOT NULL,
    hypothesis_index INTEGER NOT NULL,
    state TEXT NOT NULL,
    actor_refs_json TEXT NOT NULL,
    source_signal_ids_json TEXT NOT NULL,
    contributions_json TEXT NOT NULL,
    PRIMARY KEY (run_id, hypothesis_index),
    FOREIGN KEY (run_id) REFERENCES composition_run(run_id) ON DELETE RESTRICT
);
"""


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _hash(value: object) -> str:
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _dt(raw: str) -> datetime:
    value = datetime.fromisoformat(raw)
    if value.tzinfo is None:
        raise ValueError("stored datetime must be timezone-aware")
    return value


def _bundle_payload(spec: RequirementBundleSpec) -> dict[str, object]:
    return {
        "bundle_id": spec.bundle_id,
        "version": spec.version,
        "required_capabilities": [key.strip() for key in spec.required_capabilities],
        "geography": spec.geography.strip(),
        "source_ref": spec.source_ref.strip(),
        "rationale": spec.rationale.strip(),
    }


def _composition_payload(item: ResourceCompositionHypothesis) -> dict[str, object]:
    return {
        "state": item.state.value,
        "actor_refs": list(item.actor_refs),
        "source_signal_ids": list(item.source_signal_ids),
        "contributions": [
            {
                "capability_key": contribution.capability_key,
                "actor_refs": list(contribution.actor_refs),
                "strongest_evidence_status": contribution.strongest_evidence_status.value,
                "callable_actor_refs": list(contribution.callable_actor_refs),
                "source_signal_ids": list(contribution.source_signal_ids),
            }
            for contribution in item.contributions
        ],
    }


@dataclass(frozen=True)
class CompositionRun:
    run_id: int
    created_at: datetime
    input_fingerprint: str
    materialization_id: int
    graph_ruleset_fingerprint: str
    graph_observation_snapshot_fingerprint: str
    bundle_id: str
    bundle_version: int
    bundle_source_ref: str
    bundle_rationale: str
    bundle_fingerprint: str
    as_of: datetime
    max_age: timedelta
    max_actors: int
    max_hypotheses: int
    hypothesis_count: int


class SQLiteCompositionRunStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        if self.path != Path(":memory:"):
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.path))
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.executescript(_SCHEMA)
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "SQLiteCompositionRunStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _run_from_row(self, row: sqlite3.Row) -> CompositionRun:
        return CompositionRun(
            run_id=int(row["run_id"]),
            created_at=_dt(row["created_at"]),
            input_fingerprint=row["input_fingerprint"],
            materialization_id=int(row["materialization_id"]),
            graph_ruleset_fingerprint=row["graph_ruleset_fingerprint"],
            graph_observation_snapshot_fingerprint=row[
                "graph_observation_snapshot_fingerprint"
            ],
            bundle_id=row["bundle_id"],
            bundle_version=int(row["bundle_version"]),
            bundle_source_ref=row["bundle_source_ref"],
            bundle_rationale=row["bundle_rationale"],
            bundle_fingerprint=row["bundle_fingerprint"],
            as_of=_dt(row["as_of"]),
            max_age=timedelta(seconds=int(row["max_age_seconds"])),
            max_actors=int(row["max_actors"]),
            max_hypotheses=int(row["max_hypotheses"]),
            hypothesis_count=int(row["hypothesis_count"]),
        )

    def get_run(self, run_id: int) -> CompositionRun | None:
        row = self.connection.execute(
            "SELECT * FROM composition_run WHERE run_id = ?", (run_id,)
        ).fetchone()
        return None if row is None else self._run_from_row(row)

    def latest_run(self, bundle_id: str | None = None) -> CompositionRun | None:
        if bundle_id is None:
            row = self.connection.execute(
                "SELECT * FROM composition_run ORDER BY run_id DESC LIMIT 1"
            ).fetchone()
        else:
            row = self.connection.execute(
                """
                SELECT * FROM composition_run
                WHERE bundle_id = ? ORDER BY run_id DESC LIMIT 1
                """,
                (bundle_id,),
            ).fetchone()
        return None if row is None else self._run_from_row(row)

    def build_run(
        self,
        graph_store: SQLiteCapabilityGraphStore,
        bundle_spec: RequirementBundleSpec,
        *,
        materialization_id: int | None = None,
        as_of: datetime | None = None,
        max_age: timedelta = timedelta(days=30),
        max_actors: int = 4,
        max_hypotheses: int = 100,
        created_at: datetime | None = None,
    ) -> CompositionRun:
        errors = bundle_spec.validate()
        if errors:
            raise ValueError("invalid requirement bundle spec: " + ",".join(errors))
        if as_of is None:
            as_of = datetime.now(timezone.utc)
        if created_at is None:
            created_at = datetime.now(timezone.utc)
        if as_of.tzinfo is None or created_at.tzinfo is None:
            raise ValueError("as_of and created_at must be timezone-aware")
        if max_age < timedelta(0):
            raise ValueError("max_age must not be negative")

        materialization: CapabilityMaterialization | None
        if materialization_id is None:
            materialization = graph_store.latest_materialization()
        else:
            materialization = graph_store.get_materialization(materialization_id)
        if materialization is None:
            raise ValueError("capability graph materialization is required")

        bundle_payload = _bundle_payload(bundle_spec)
        bundle_fingerprint = _hash(bundle_payload)
        input_payload = {
            "materialization_id": materialization.materialization_id,
            "graph_ruleset_fingerprint": materialization.ruleset_fingerprint,
            "graph_observation_snapshot_fingerprint": materialization.observation_snapshot_fingerprint,
            "bundle": bundle_payload,
            "as_of": as_of.isoformat(),
            "max_age_seconds": int(max_age.total_seconds()),
            "max_actors": max_actors,
            "max_hypotheses": max_hypotheses,
        }
        input_fingerprint = _hash(input_payload)

        existing = self.connection.execute(
            "SELECT * FROM composition_run WHERE input_fingerprint = ?",
            (input_fingerprint,),
        ).fetchone()
        if existing is not None:
            return self._run_from_row(existing)

        claims = graph_store.capability_claims(materialization.materialization_id)
        hypotheses = generate_composition_hypotheses(
            claims,
            bundle_spec.as_bundle(),
            as_of=as_of,
            max_age=max_age,
            max_actors=max_actors,
            max_hypotheses=max_hypotheses,
        )

        with self.connection:
            cursor = self.connection.execute(
                """
                INSERT INTO composition_run (
                    created_at, input_fingerprint, materialization_id,
                    graph_ruleset_fingerprint, graph_observation_snapshot_fingerprint,
                    bundle_id, bundle_version, bundle_source_ref, bundle_rationale,
                    bundle_fingerprint, as_of, max_age_seconds, max_actors,
                    max_hypotheses, hypothesis_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    created_at.isoformat(),
                    input_fingerprint,
                    materialization.materialization_id,
                    materialization.ruleset_fingerprint,
                    materialization.observation_snapshot_fingerprint,
                    bundle_spec.bundle_id.strip(),
                    bundle_spec.version,
                    bundle_spec.source_ref.strip(),
                    bundle_spec.rationale.strip(),
                    bundle_fingerprint,
                    as_of.isoformat(),
                    int(max_age.total_seconds()),
                    max_actors,
                    max_hypotheses,
                    len(hypotheses),
                ),
            )
            run_id = int(cursor.lastrowid)
            for index, hypothesis in enumerate(hypotheses):
                payload = _composition_payload(hypothesis)
                self.connection.execute(
                    """
                    INSERT INTO composition_hypothesis_snapshot (
                        run_id, hypothesis_index, state, actor_refs_json,
                        source_signal_ids_json, contributions_json
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        run_id,
                        index,
                        hypothesis.state.value,
                        _json(payload["actor_refs"]),
                        _json(payload["source_signal_ids"]),
                        _json(payload["contributions"]),
                    ),
                )

        result = self.get_run(run_id)
        if result is None:
            raise RuntimeError("composition run disappeared after commit")
        return result

    def hypotheses(self, run_id: int) -> tuple[ResourceCompositionHypothesis, ...]:
        run = self.get_run(run_id)
        if run is None:
            raise KeyError(run_id)
        rows = self.connection.execute(
            """
            SELECT * FROM composition_hypothesis_snapshot
            WHERE run_id = ? ORDER BY hypothesis_index
            """,
            (run_id,),
        ).fetchall()
        result: list[ResourceCompositionHypothesis] = []
        for row in rows:
            raw_contributions = json.loads(row["contributions_json"])
            if not isinstance(raw_contributions, list):
                raise ValueError("stored composition contributions are invalid")
            contributions = tuple(
                CapabilityContribution(
                    capability_key=str(item["capability_key"]),
                    actor_refs=tuple(str(x) for x in item["actor_refs"]),
                    strongest_evidence_status=EvidenceStatus(
                        str(item["strongest_evidence_status"])
                    ),
                    callable_actor_refs=tuple(
                        str(x) for x in item["callable_actor_refs"]
                    ),
                    source_signal_ids=tuple(str(x) for x in item["source_signal_ids"]),
                )
                for item in raw_contributions
                if isinstance(item, dict)
            )
            if len(contributions) != len(raw_contributions):
                raise ValueError("stored composition contribution item is invalid")
            result.append(
                ResourceCompositionHypothesis(
                    bundle_id=run.bundle_id,
                    actor_refs=tuple(json.loads(row["actor_refs_json"])),
                    state=CompositionState(row["state"]),
                    contributions=contributions,
                    source_signal_ids=tuple(json.loads(row["source_signal_ids_json"])),
                )
            )
        return tuple(result)


GOVERNING_INVARIANTS = (
    "COMPOSITION_RUN_INPUTS_ARE_IMMUTABLE",
    "COMPOSITION_RUN_LINKS_EXACT_GRAPH_MATERIALIZATION",
    "COMPOSITION_RUN_LINKS_EXACT_REQUIREMENT_VERSION",
    "REQUIREMENT_BUNDLE_NE_DEMAND_TRUTH",
    "COMPOSITION_HYPOTHESIS_NE_PAYER_COMMITMENT",
    "CALLABLE_COMPOSED_NE_COUNTERPARTY_CONSENT",
    "CALLABLE_COMPOSED_NE_TRANSACTIONABILITY",
    "UNKNOWN_NE_PASS",
)
