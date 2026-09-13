"""Durable SQLite store for live signal evidence and semantic state.

SQLite is an implementation detail below the canonical time/state semantics in
``src.live_signal_ledger``. The store keeps three distinct layers:

1. append-only reviewed/raw ``SignalObservation`` evidence for future replay;
2. append-only semantic transitions;
3. current semantic state.

This separation allows inference rules to change later without rewriting what the
system originally observed.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Iterator, Mapping

from src.live_resource_signals import (
    AvailabilityState,
    ExplicitCapability,
    ObservedFact,
    PermissionState,
    SignalObservation,
)
from src.live_signal_ledger import (
    SignalLedgerEntry,
    SignalTransition,
    TransitionKind,
    observe_signal,
)


_SCHEMA = """
CREATE TABLE IF NOT EXISTS signal_observation (
    sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    signal_id TEXT NOT NULL,
    actor_ref TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    observation_hash TEXT NOT NULL,
    observation_json TEXT NOT NULL,
    UNIQUE(source_id, signal_id, observed_at, observation_hash)
);

CREATE INDEX IF NOT EXISTS idx_signal_observation_identity
ON signal_observation(source_id, signal_id, sequence_id);

CREATE TABLE IF NOT EXISTS signal_current (
    source_id TEXT NOT NULL,
    signal_id TEXT NOT NULL,
    actor_ref TEXT NOT NULL,
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    seen_count INTEGER NOT NULL,
    revision_count INTEGER NOT NULL,
    current_fingerprint TEXT NOT NULL,
    current_payload_json TEXT NOT NULL,
    previous_fingerprints_json TEXT NOT NULL,
    PRIMARY KEY (source_id, signal_id)
);

CREATE TABLE IF NOT EXISTS signal_transition (
    sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    signal_id TEXT NOT NULL,
    actor_ref TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    transition_kind TEXT NOT NULL,
    changed_dimensions_json TEXT NOT NULL,
    resulting_entry_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_signal_transition_identity
ON signal_transition(source_id, signal_id, sequence_id);
"""


def _dt(value: str) -> datetime:
    result = datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError("stored datetime must be timezone-aware")
    return result


def _entry_to_dict(entry: SignalLedgerEntry) -> dict[str, object]:
    return {
        "source_id": entry.source_id,
        "signal_id": entry.signal_id,
        "actor_ref": entry.actor_ref,
        "first_seen_at": entry.first_seen_at.isoformat(),
        "last_seen_at": entry.last_seen_at.isoformat(),
        "seen_count": entry.seen_count,
        "revision_count": entry.revision_count,
        "current_fingerprint": entry.current_fingerprint,
        "current_payload": dict(entry.current_payload),
        "previous_fingerprints": list(entry.previous_fingerprints),
    }


def _entry_from_dict(payload: Mapping[str, object]) -> SignalLedgerEntry:
    return SignalLedgerEntry(
        source_id=str(payload["source_id"]),
        signal_id=str(payload["signal_id"]),
        actor_ref=str(payload["actor_ref"]),
        first_seen_at=_dt(str(payload["first_seen_at"])),
        last_seen_at=_dt(str(payload["last_seen_at"])),
        seen_count=int(payload["seen_count"]),
        revision_count=int(payload["revision_count"]),
        current_fingerprint=str(payload["current_fingerprint"]),
        current_payload=dict(payload["current_payload"]),
        previous_fingerprints=tuple(str(x) for x in payload.get("previous_fingerprints", [])),
    )


def _json(value: object) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    except TypeError as exc:
        raise ValueError("durable signal evidence must be JSON-serializable") from exc


def _observation_to_dict(signal: SignalObservation) -> dict[str, object]:
    return {
        "signal_id": signal.signal_id,
        "source_id": signal.source_id,
        "observed_at": signal.observed_at.isoformat(),
        "actor_ref": signal.actor_ref,
        "geography": signal.geography,
        "raw_text": signal.raw_text,
        "source_url": signal.source_url,
        "facts": [
            {
                "key": fact.key,
                "value": fact.value,
                "evidence_text": fact.evidence_text,
            }
            for fact in signal.facts
        ],
        "explicit_capabilities": [
            {
                "capability_key": capability.capability_key,
                "evidence_text": capability.evidence_text,
            }
            for capability in signal.explicit_capabilities
        ],
        "availability": signal.availability.value,
        "permission": signal.permission.value,
    }


def _observation_from_dict(payload: Mapping[str, object]) -> SignalObservation:
    raw_facts = payload.get("facts", [])
    raw_capabilities = payload.get("explicit_capabilities", [])
    if not isinstance(raw_facts, list) or not isinstance(raw_capabilities, list):
        raise ValueError("stored observation collections are invalid")

    facts = tuple(
        ObservedFact(
            key=str(item["key"]),
            value=item.get("value"),
            evidence_text=str(item["evidence_text"]),
        )
        for item in raw_facts
        if isinstance(item, Mapping)
    )
    capabilities = tuple(
        ExplicitCapability(
            capability_key=str(item["capability_key"]),
            evidence_text=str(item["evidence_text"]),
        )
        for item in raw_capabilities
        if isinstance(item, Mapping)
    )
    if len(facts) != len(raw_facts) or len(capabilities) != len(raw_capabilities):
        raise ValueError("stored observation item is invalid")

    signal = SignalObservation(
        signal_id=str(payload["signal_id"]),
        source_id=str(payload["source_id"]),
        observed_at=_dt(str(payload["observed_at"])),
        actor_ref=str(payload["actor_ref"]),
        geography=str(payload.get("geography", "")),
        raw_text=str(payload.get("raw_text", "")),
        source_url=str(payload.get("source_url", "")),
        facts=facts,
        explicit_capabilities=capabilities,
        availability=AvailabilityState(str(payload.get("availability", "UNKNOWN"))),
        permission=PermissionState(str(payload.get("permission", "UNKNOWN"))),
    )
    errors = signal.validate()
    if errors:
        raise ValueError("stored observation is invalid: " + ",".join(errors))
    return signal


def _observation_json_and_hash(signal: SignalObservation) -> tuple[str, str]:
    rendered = _json(_observation_to_dict(signal))
    return rendered, hashlib.sha256(rendered.encode("utf-8")).hexdigest()


class SQLiteSignalLedgerStore:
    """Durable adapter preserving raw evidence plus ``observe_signal`` semantics."""

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

    def __enter__(self) -> "SQLiteSignalLedgerStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def get(self, source_id: str, signal_id: str) -> SignalLedgerEntry | None:
        row = self.connection.execute(
            "SELECT * FROM signal_current WHERE source_id = ? AND signal_id = ?",
            (source_id, signal_id),
        ).fetchone()
        if row is None:
            return None
        return SignalLedgerEntry(
            source_id=row["source_id"],
            signal_id=row["signal_id"],
            actor_ref=row["actor_ref"],
            first_seen_at=_dt(row["first_seen_at"]),
            last_seen_at=_dt(row["last_seen_at"]),
            seen_count=row["seen_count"],
            revision_count=row["revision_count"],
            current_fingerprint=row["current_fingerprint"],
            current_payload=json.loads(row["current_payload_json"]),
            previous_fingerprints=tuple(json.loads(row["previous_fingerprints_json"])),
        )

    def ingest(self, signal: SignalObservation) -> SignalTransition:
        observation_json, observation_hash = _observation_json_and_hash(signal)
        existing = self.get(signal.source_id, signal.signal_id)
        entry, transition = observe_signal(existing, signal)
        entry_dict = _entry_to_dict(entry)

        with self.connection:
            self.connection.execute(
                """
                INSERT OR IGNORE INTO signal_observation (
                    source_id, signal_id, actor_ref, observed_at,
                    observation_hash, observation_json
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    signal.source_id,
                    signal.signal_id,
                    signal.actor_ref,
                    signal.observed_at.isoformat(),
                    observation_hash,
                    observation_json,
                ),
            )

            if transition.kind is not TransitionKind.OUT_OF_ORDER:
                self.connection.execute(
                    """
                    INSERT INTO signal_current (
                        source_id, signal_id, actor_ref, first_seen_at, last_seen_at,
                        seen_count, revision_count, current_fingerprint,
                        current_payload_json, previous_fingerprints_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(source_id, signal_id) DO UPDATE SET
                        actor_ref = excluded.actor_ref,
                        first_seen_at = excluded.first_seen_at,
                        last_seen_at = excluded.last_seen_at,
                        seen_count = excluded.seen_count,
                        revision_count = excluded.revision_count,
                        current_fingerprint = excluded.current_fingerprint,
                        current_payload_json = excluded.current_payload_json,
                        previous_fingerprints_json = excluded.previous_fingerprints_json
                    """,
                    (
                        entry.source_id,
                        entry.signal_id,
                        entry.actor_ref,
                        entry.first_seen_at.isoformat(),
                        entry.last_seen_at.isoformat(),
                        entry.seen_count,
                        entry.revision_count,
                        entry.current_fingerprint,
                        _json(entry.current_payload),
                        _json(list(entry.previous_fingerprints)),
                    ),
                )

            self.connection.execute(
                """
                INSERT INTO signal_transition (
                    source_id, signal_id, actor_ref, observed_at, transition_kind,
                    changed_dimensions_json, resulting_entry_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    signal.source_id,
                    signal.signal_id,
                    signal.actor_ref,
                    signal.observed_at.isoformat(),
                    transition.kind.value,
                    _json(list(transition.changed_dimensions)),
                    _json(entry_dict),
                ),
            )
        return transition

    def observations(
        self,
        source_id: str | None = None,
        signal_id: str | None = None,
    ) -> tuple[SignalObservation, ...]:
        """Return archived original observations in ingestion order for replay/audit."""

        clauses: list[str] = []
        params: list[str] = []
        if source_id is not None:
            clauses.append("source_id = ?")
            params.append(source_id)
        if signal_id is not None:
            clauses.append("signal_id = ?")
            params.append(signal_id)

        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        rows = self.connection.execute(
            "SELECT observation_json FROM signal_observation"
            + where
            + " ORDER BY sequence_id",
            tuple(params),
        ).fetchall()
        return tuple(
            _observation_from_dict(json.loads(row["observation_json"])) for row in rows
        )

    def transitions(self, source_id: str, signal_id: str) -> tuple[SignalTransition, ...]:
        rows = self.connection.execute(
            """
            SELECT * FROM signal_transition
            WHERE source_id = ? AND signal_id = ?
            ORDER BY sequence_id
            """,
            (source_id, signal_id),
        ).fetchall()
        return tuple(
            SignalTransition(
                source_id=row["source_id"],
                signal_id=row["signal_id"],
                kind=TransitionKind(row["transition_kind"]),
                observed_at=_dt(row["observed_at"]),
                changed_dimensions=tuple(json.loads(row["changed_dimensions_json"])),
            )
            for row in rows
        )

    def rebuild_entry(self, source_id: str, signal_id: str) -> SignalLedgerEntry | None:
        """Rebuild the latest accepted ledger entry from append-only history."""

        row = self.connection.execute(
            """
            SELECT resulting_entry_json FROM signal_transition
            WHERE source_id = ? AND signal_id = ? AND transition_kind != ?
            ORDER BY sequence_id DESC LIMIT 1
            """,
            (source_id, signal_id, TransitionKind.OUT_OF_ORDER.value),
        ).fetchone()
        if row is None:
            return None
        return _entry_from_dict(json.loads(row["resulting_entry_json"]))

    def iter_current(self) -> Iterator[SignalLedgerEntry]:
        rows = self.connection.execute(
            "SELECT source_id, signal_id FROM signal_current ORDER BY source_id, signal_id"
        ).fetchall()
        for row in rows:
            entry = self.get(row["source_id"], row["signal_id"])
            if entry is not None:
                yield entry


GOVERNING_INVARIANTS = (
    "SQLITE_IS_STORAGE_NOT_ONTOLOGY",
    "RAW_OBSERVATION_NE_DERIVED_STATE",
    "RAW_OBSERVATION_HISTORY_IS_APPEND_ONLY",
    "CURRENT_STATE_MUST_BE_REBUILDABLE_FROM_HISTORY",
    "OUT_OF_ORDER_OBSERVATION_MUST_NOT_ROLL_BACK_CURRENT_STATE",
    "TRANSITION_HISTORY_IS_APPEND_ONLY",
    "RULE_CHANGE_MUST_NOT_REWRITE_OBSERVED_HISTORY",
    "UNKNOWN_NE_PASS",
)
