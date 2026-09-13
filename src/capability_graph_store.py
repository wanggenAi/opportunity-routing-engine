"""Persistent, replayable Resource Capability Graph materializations.

The graph is a derived evidence layer, not a second source of truth. Raw observations
remain authoritative evidence; active versioned rules derive INFERRED claims; explicit
source capabilities derive OBSERVED claims. Each materialization is immutable so rule
changes can be replayed and diffed without rewriting earlier reasoning.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Sequence

from src.capability_rule_registry import SQLiteCapabilityRuleRegistry
from src.live_resource_signals import (
    AvailabilityState,
    CapabilityClaim,
    EvidenceStatus,
    PermissionState,
    SignalObservation,
    extract_capability_claims,
)
from src.live_signal_store import SQLiteSignalLedgerStore


_SCHEMA = """
CREATE TABLE IF NOT EXISTS capability_materialization (
    materialization_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    ruleset_fingerprint TEXT NOT NULL,
    observation_snapshot_fingerprint TEXT NOT NULL,
    active_rule_ids_json TEXT NOT NULL,
    observation_count INTEGER NOT NULL,
    claim_count INTEGER NOT NULL,
    UNIQUE(ruleset_fingerprint, observation_snapshot_fingerprint)
);

CREATE TABLE IF NOT EXISTS capability_claim_snapshot (
    materialization_id INTEGER NOT NULL,
    claim_index INTEGER NOT NULL,
    source_id TEXT NOT NULL,
    signal_id TEXT NOT NULL,
    actor_ref TEXT NOT NULL,
    capability_key TEXT NOT NULL,
    evidence_status TEXT NOT NULL,
    rationale TEXT NOT NULL,
    last_observed_at TEXT NOT NULL,
    geography TEXT NOT NULL,
    availability TEXT NOT NULL,
    permission TEXT NOT NULL,
    inference_rule_id TEXT NOT NULL,
    PRIMARY KEY (materialization_id, claim_index),
    FOREIGN KEY (materialization_id)
        REFERENCES capability_materialization(materialization_id)
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_capability_claim_actor
ON capability_claim_snapshot(materialization_id, actor_ref, capability_key);

CREATE INDEX IF NOT EXISTS idx_capability_claim_capability
ON capability_claim_snapshot(materialization_id, capability_key, actor_ref);
"""


def _dt(raw: str) -> datetime:
    value = datetime.fromisoformat(raw)
    if value.tzinfo is None:
        raise ValueError("stored datetime must be timezone-aware")
    return value


def _json(value: object) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    except TypeError as exc:
        raise ValueError("capability graph materialization must be JSON-serializable") from exc


def _hash(value: object) -> str:
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def signal_ref(source_id: str, signal_id: str) -> str:
    """Return a globally unambiguous signal lineage reference."""

    source = source_id.strip()
    signal = signal_id.strip()
    if not source or not signal:
        raise ValueError("source_id and signal_id are required")
    return f"{source}::{signal}"


def _signal_payload(signal: SignalObservation) -> dict[str, object]:
    return {
        "source_id": signal.source_id,
        "signal_id": signal.signal_id,
        "observed_at": signal.observed_at.isoformat(),
        "actor_ref": signal.actor_ref,
        "geography": signal.geography,
        "raw_text": signal.raw_text,
        "source_url": signal.source_url,
        "facts": [
            {"key": item.key, "value": item.value, "evidence_text": item.evidence_text}
            for item in signal.facts
        ],
        "explicit_capabilities": [
            {"capability_key": item.capability_key, "evidence_text": item.evidence_text}
            for item in signal.explicit_capabilities
        ],
        "availability": signal.availability.value,
        "permission": signal.permission.value,
    }


def _rule_payload(registry: SQLiteCapabilityRuleRegistry) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for spec in registry.active_specs():
        result.append(
            {
                "rule_id": spec.rule_id,
                "version": spec.version,
                "capability_key": spec.capability_key,
                "conditions": [
                    {"key": condition.key, "expected_value": condition.expected_value}
                    for condition in spec.conditions
                ],
                "rationale": spec.rationale,
            }
        )
    return result


@dataclass(frozen=True)
class CapabilityMaterialization:
    materialization_id: int
    created_at: datetime
    ruleset_fingerprint: str
    observation_snapshot_fingerprint: str
    active_rule_ids: tuple[str, ...]
    observation_count: int
    claim_count: int


@dataclass(frozen=True)
class CapabilityGraphClaim:
    materialization_id: int
    source_id: str
    signal_id: str
    actor_ref: str
    capability_key: str
    evidence_status: EvidenceStatus
    rationale: str
    last_observed_at: datetime
    geography: str
    availability: AvailabilityState
    permission: PermissionState
    inference_rule_id: str = ""

    @property
    def source_signal_ref(self) -> str:
        return signal_ref(self.source_id, self.signal_id)

    def as_capability_claim(self) -> CapabilityClaim:
        return CapabilityClaim(
            actor_ref=self.actor_ref,
            capability_key=self.capability_key,
            evidence_status=self.evidence_status,
            source_signal_ids=(self.source_signal_ref,),
            rationale=self.rationale,
            last_observed_at=self.last_observed_at,
            geography=self.geography,
            availability=self.availability,
            permission=self.permission,
            inference_rule_id=self.inference_rule_id,
        )


@dataclass(frozen=True)
class CapabilityGraphDiff:
    before_materialization_id: int
    after_materialization_id: int
    added: tuple[CapabilityGraphClaim, ...]
    removed: tuple[CapabilityGraphClaim, ...]


class SQLiteCapabilityGraphStore:
    """Immutable capability snapshots derived from raw observations and rule versions."""

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

    def __enter__(self) -> "SQLiteCapabilityGraphStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _materialization_from_row(self, row: sqlite3.Row) -> CapabilityMaterialization:
        return CapabilityMaterialization(
            materialization_id=int(row["materialization_id"]),
            created_at=_dt(row["created_at"]),
            ruleset_fingerprint=row["ruleset_fingerprint"],
            observation_snapshot_fingerprint=row["observation_snapshot_fingerprint"],
            active_rule_ids=tuple(json.loads(row["active_rule_ids_json"])),
            observation_count=int(row["observation_count"]),
            claim_count=int(row["claim_count"]),
        )

    def get_materialization(self, materialization_id: int) -> CapabilityMaterialization | None:
        row = self.connection.execute(
            "SELECT * FROM capability_materialization WHERE materialization_id = ?",
            (materialization_id,),
        ).fetchone()
        return None if row is None else self._materialization_from_row(row)

    def latest_materialization(self) -> CapabilityMaterialization | None:
        row = self.connection.execute(
            "SELECT * FROM capability_materialization ORDER BY materialization_id DESC LIMIT 1"
        ).fetchone()
        return None if row is None else self._materialization_from_row(row)

    def materialize_current(
        self,
        signal_store: SQLiteSignalLedgerStore,
        rule_registry: SQLiteCapabilityRuleRegistry,
        *,
        created_at: datetime | None = None,
    ) -> CapabilityMaterialization:
        """Materialize current accepted observations under the active rule versions.

        Re-running with the same observation snapshot and active rules is idempotent.
        Activating a new rule version creates a new immutable materialization instead of
        rewriting the previous graph.
        """

        if created_at is None:
            created_at = datetime.now(timezone.utc)
        if created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        observations = signal_store.current_observations()
        active_specs = rule_registry.active_specs()
        active_rules = rule_registry.active_rules()
        rule_ids = tuple(spec.as_inference_rule().rule_id for spec in active_specs)

        ruleset_fingerprint = _hash(_rule_payload(rule_registry))
        observation_snapshot_fingerprint = _hash(
            [_signal_payload(signal) for signal in observations]
        )

        existing = self.connection.execute(
            """
            SELECT * FROM capability_materialization
            WHERE ruleset_fingerprint = ? AND observation_snapshot_fingerprint = ?
            """,
            (ruleset_fingerprint, observation_snapshot_fingerprint),
        ).fetchone()
        if existing is not None:
            return self._materialization_from_row(existing)

        derived: list[tuple[SignalObservation, CapabilityClaim]] = []
        for signal in observations:
            for claim in extract_capability_claims(signal, active_rules):
                derived.append((signal, claim))

        with self.connection:
            cursor = self.connection.execute(
                """
                INSERT INTO capability_materialization (
                    created_at, ruleset_fingerprint, observation_snapshot_fingerprint,
                    active_rule_ids_json, observation_count, claim_count
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    created_at.isoformat(),
                    ruleset_fingerprint,
                    observation_snapshot_fingerprint,
                    _json(list(rule_ids)),
                    len(observations),
                    len(derived),
                ),
            )
            materialization_id = int(cursor.lastrowid)
            for index, (signal, claim) in enumerate(derived):
                self.connection.execute(
                    """
                    INSERT INTO capability_claim_snapshot (
                        materialization_id, claim_index, source_id, signal_id,
                        actor_ref, capability_key, evidence_status, rationale,
                        last_observed_at, geography, availability, permission,
                        inference_rule_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        materialization_id,
                        index,
                        signal.source_id,
                        signal.signal_id,
                        claim.actor_ref,
                        claim.capability_key,
                        claim.evidence_status.value,
                        claim.rationale,
                        claim.last_observed_at.isoformat(),
                        claim.geography,
                        claim.availability.value,
                        claim.permission.value,
                        claim.inference_rule_id,
                    ),
                )

        result = self.get_materialization(materialization_id)
        if result is None:
            raise RuntimeError("capability materialization disappeared after commit")
        return result

    def claims(
        self,
        materialization_id: int | None = None,
        *,
        actor_ref: str | None = None,
        capability_key: str | None = None,
    ) -> tuple[CapabilityGraphClaim, ...]:
        if materialization_id is None:
            latest = self.latest_materialization()
            if latest is None:
                return ()
            materialization_id = latest.materialization_id

        clauses = ["materialization_id = ?"]
        params: list[object] = [materialization_id]
        if actor_ref is not None:
            clauses.append("actor_ref = ?")
            params.append(actor_ref)
        if capability_key is not None:
            clauses.append("capability_key = ?")
            params.append(capability_key)

        rows = self.connection.execute(
            """
            SELECT * FROM capability_claim_snapshot
            WHERE """
            + " AND ".join(clauses)
            + " ORDER BY actor_ref, capability_key, source_id, signal_id, claim_index",
            tuple(params),
        ).fetchall()
        return tuple(
            CapabilityGraphClaim(
                materialization_id=int(row["materialization_id"]),
                source_id=row["source_id"],
                signal_id=row["signal_id"],
                actor_ref=row["actor_ref"],
                capability_key=row["capability_key"],
                evidence_status=EvidenceStatus(row["evidence_status"]),
                rationale=row["rationale"],
                last_observed_at=_dt(row["last_observed_at"]),
                geography=row["geography"],
                availability=AvailabilityState(row["availability"]),
                permission=PermissionState(row["permission"]),
                inference_rule_id=row["inference_rule_id"],
            )
            for row in rows
        )

    def capability_claims(
        self,
        materialization_id: int | None = None,
        *,
        actor_ref: str | None = None,
        capability_key: str | None = None,
    ) -> tuple[CapabilityClaim, ...]:
        return tuple(
            item.as_capability_claim()
            for item in self.claims(
                materialization_id,
                actor_ref=actor_ref,
                capability_key=capability_key,
            )
        )

    @staticmethod
    def _identity(claim: CapabilityGraphClaim) -> tuple[str, ...]:
        return (
            claim.actor_ref,
            claim.capability_key,
            claim.evidence_status.value,
            claim.source_id,
            claim.signal_id,
            claim.inference_rule_id,
        )

    def diff(
        self,
        before_materialization_id: int,
        after_materialization_id: int,
    ) -> CapabilityGraphDiff:
        before = self.claims(before_materialization_id)
        after = self.claims(after_materialization_id)
        before_map = {self._identity(item): item for item in before}
        after_map = {self._identity(item): item for item in after}
        added_keys = sorted(set(after_map) - set(before_map))
        removed_keys = sorted(set(before_map) - set(after_map))
        return CapabilityGraphDiff(
            before_materialization_id=before_materialization_id,
            after_materialization_id=after_materialization_id,
            added=tuple(after_map[key] for key in added_keys),
            removed=tuple(before_map[key] for key in removed_keys),
        )


GOVERNING_INVARIANTS = (
    "RAW_OBSERVATION_IS_EVIDENCE_AUTHORITY",
    "CAPABILITY_GRAPH_IS_DERIVED_NOT_SOURCE_TRUTH",
    "RULE_VERSION_CHANGE_CREATES_NEW_MATERIALIZATION",
    "MATERIALIZATION_HISTORY_IS_IMMUTABLE",
    "SOURCE_ID_PLUS_SIGNAL_ID_IS_LINEAGE_IDENTITY",
    "INFERRED_NE_OBSERVED",
    "OBSERVED_NE_CONFIRMED",
    "GRAPH_CLAIM_NE_CALLABILITY",
    "GRAPH_CLAIM_NE_TRANSACTIONABILITY",
    "UNKNOWN_NE_PASS",
)
