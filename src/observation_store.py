"""Append-oriented durable store for source-neutral ObservationEnvelope history."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from src.observation_fabric import EvidenceRef, ObservationEnvelope, SemanticClaim


_SCHEMA = """
CREATE TABLE IF NOT EXISTS observation_history (
    sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    observation_id TEXT NOT NULL,
    source_record_id TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    retrieved_at TEXT NOT NULL,
    envelope_hash TEXT NOT NULL,
    envelope_json TEXT NOT NULL,
    supersedes_observation_id TEXT,
    UNIQUE(source_id, observation_id, envelope_hash)
);
CREATE INDEX IF NOT EXISTS idx_observation_history_identity
ON observation_history(source_id, observation_id, sequence_id);
CREATE INDEX IF NOT EXISTS idx_observation_history_time
ON observation_history(observed_at, retrieved_at);

CREATE TABLE IF NOT EXISTS observation_current (
    source_id TEXT NOT NULL,
    observation_id TEXT NOT NULL,
    sequence_id INTEGER NOT NULL,
    retrieved_at TEXT NOT NULL,
    envelope_hash TEXT NOT NULL,
    PRIMARY KEY(source_id, observation_id)
);

CREATE TABLE IF NOT EXISTS observation_claim_index (
    sequence_id INTEGER NOT NULL,
    source_id TEXT NOT NULL,
    observation_id TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    primitive TEXT NOT NULL,
    concept TEXT NOT NULL,
    actor_id TEXT,
    geography TEXT,
    epistemic_status TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_observation_claim_primitive
ON observation_claim_index(primitive, concept, sequence_id);
CREATE INDEX IF NOT EXISTS idx_observation_claim_actor
ON observation_claim_index(actor_id, sequence_id);

CREATE TABLE IF NOT EXISTS observation_actor_index (
    sequence_id INTEGER NOT NULL,
    actor_id TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_observation_actor
ON observation_actor_index(actor_id, sequence_id);

CREATE TABLE IF NOT EXISTS observation_geography_index (
    sequence_id INTEGER NOT NULL,
    geography TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_observation_geography
ON observation_geography_index(geography, sequence_id);

CREATE TABLE IF NOT EXISTS observation_transition (
    sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    observation_id TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    retrieved_at TEXT NOT NULL,
    transition_kind TEXT NOT NULL,
    envelope_hash TEXT NOT NULL,
    history_sequence_id INTEGER NOT NULL
);
"""


@dataclass(frozen=True)
class ObservationTransition:
    source_id: str
    observation_id: str
    kind: str
    history_sequence_id: int
    envelope_hash: str


def _parse_time(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("stored observation time must be timezone-aware")
    return result


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _envelope_hash(envelope: ObservationEnvelope) -> tuple[str, str]:
    rendered = _canonical_json(envelope.as_dict())
    return rendered, hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def _tuple_strings(value: object, name: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"stored {name} must be an array of strings")
    return tuple(value)


def envelope_from_stored_dict(payload: dict) -> ObservationEnvelope:
    evidence_raw = payload.get("evidence")
    claims_raw = payload.get("claims")
    if not isinstance(evidence_raw, list) or not isinstance(claims_raw, list):
        raise ValueError("stored evidence/claims are invalid")

    evidence = tuple(
        EvidenceRef(
            ref_id=str(item["ref_id"]),
            locator=str(item["locator"]),
            excerpt=str(item.get("excerpt", "")),
            content_hash=str(item.get("content_hash", "")),
        )
        for item in evidence_raw
        if isinstance(item, dict)
    )
    claims = tuple(
        SemanticClaim(
            claim_id=str(item["claim_id"]),
            primitive=str(item["primitive"]),
            concept=str(item["concept"]),
            epistemic_status=str(item["epistemic_status"]),
            evidence_refs=_tuple_strings(item.get("evidence_refs", []), "claim evidence_refs"),
            value=item.get("value"),
            actor_id=(None if item.get("actor_id") is None else str(item["actor_id"])),
            geography=(None if item.get("geography") is None else str(item["geography"])),
            inference_depth=int(item.get("inference_depth", 0)),
            contradiction_refs=_tuple_strings(
                item.get("contradiction_refs", []), "claim contradiction_refs"
            ),
        )
        for item in claims_raw
        if isinstance(item, dict)
    )
    if len(evidence) != len(evidence_raw) or len(claims) != len(claims_raw):
        raise ValueError("stored evidence/claim item is invalid")

    return ObservationEnvelope(
        observation_id=str(payload["observation_id"]),
        source_id=str(payload["source_id"]),
        source_record_id=str(payload["source_record_id"]),
        source_locator=str(payload["source_locator"]),
        source_origin_geography=str(payload["source_origin_geography"]),
        relevance_geographies=_tuple_strings(
            payload.get("relevance_geographies", []), "relevance_geographies"
        ),
        source_tier=str(payload["source_tier"]),
        observed_at=str(payload["observed_at"]),
        retrieved_at=str(payload["retrieved_at"]),
        parser_version=str(payload["parser_version"]),
        raw_payload_hash=str(payload["raw_payload_hash"]),
        sampling_boundary=str(payload["sampling_boundary"]),
        evidence=evidence,
        claims=claims,
        published_at=(
            None if payload.get("published_at") is None else str(payload["published_at"])
        ),
        actor_ids=_tuple_strings(payload.get("actor_ids", []), "actor_ids"),
        unknown_fields=_tuple_strings(payload.get("unknown_fields", []), "unknown_fields"),
        contradiction_refs=_tuple_strings(
            payload.get("contradiction_refs", []), "contradiction_refs"
        ),
        supersedes_observation_id=(
            None
            if payload.get("supersedes_observation_id") is None
            else str(payload["supersedes_observation_id"])
        ),
        schema_version=str(payload["schema_version"]),
    )


class SQLiteObservationStore:
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

    def __enter__(self) -> "SQLiteObservationStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _current_row(self, source_id: str, observation_id: str):
        return self.connection.execute(
            "SELECT * FROM observation_current WHERE source_id=? AND observation_id=?",
            (source_id, observation_id),
        ).fetchone()

    def ingest(self, envelope: ObservationEnvelope) -> ObservationTransition:
        rendered, fingerprint = _envelope_hash(envelope)
        duplicate = self.connection.execute(
            """
            SELECT sequence_id FROM observation_history
            WHERE source_id=? AND observation_id=? AND envelope_hash=?
            """,
            (envelope.source_id, envelope.observation_id, fingerprint),
        ).fetchone()
        if duplicate is not None:
            return ObservationTransition(
                envelope.source_id,
                envelope.observation_id,
                "DUPLICATE",
                int(duplicate["sequence_id"]),
                fingerprint,
            )

        current = self._current_row(envelope.source_id, envelope.observation_id)
        kind = "FIRST_SEEN"
        update_current = True
        if current is not None:
            if _parse_time(envelope.retrieved_at) < _parse_time(current["retrieved_at"]):
                kind = "OUT_OF_ORDER"
                update_current = False
            else:
                kind = "REVISION"

        with self.connection:
            cursor = self.connection.execute(
                """
                INSERT INTO observation_history (
                    source_id, observation_id, source_record_id, observed_at,
                    retrieved_at, envelope_hash, envelope_json,
                    supersedes_observation_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    envelope.source_id,
                    envelope.observation_id,
                    envelope.source_record_id,
                    envelope.observed_at,
                    envelope.retrieved_at,
                    fingerprint,
                    rendered,
                    envelope.supersedes_observation_id,
                ),
            )
            history_sequence_id = int(cursor.lastrowid)

            for claim in envelope.claims:
                self.connection.execute(
                    """
                    INSERT INTO observation_claim_index (
                        sequence_id, source_id, observation_id, claim_id, primitive,
                        concept, actor_id, geography, epistemic_status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        history_sequence_id,
                        envelope.source_id,
                        envelope.observation_id,
                        claim.claim_id,
                        claim.primitive,
                        claim.concept,
                        claim.actor_id,
                        claim.geography,
                        claim.epistemic_status,
                    ),
                )
            for actor_id in sorted(set(envelope.actor_ids)):
                self.connection.execute(
                    "INSERT INTO observation_actor_index(sequence_id,actor_id) VALUES (?,?)",
                    (history_sequence_id, actor_id),
                )
            geographies = set(envelope.relevance_geographies)
            geographies.update(
                claim.geography for claim in envelope.claims if claim.geography
            )
            for geography in sorted(geographies):
                self.connection.execute(
                    "INSERT INTO observation_geography_index(sequence_id,geography) VALUES (?,?)",
                    (history_sequence_id, geography),
                )

            if update_current:
                self.connection.execute(
                    """
                    INSERT INTO observation_current (
                        source_id, observation_id, sequence_id, retrieved_at, envelope_hash
                    ) VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(source_id,observation_id) DO UPDATE SET
                        sequence_id=excluded.sequence_id,
                        retrieved_at=excluded.retrieved_at,
                        envelope_hash=excluded.envelope_hash
                    """,
                    (
                        envelope.source_id,
                        envelope.observation_id,
                        history_sequence_id,
                        envelope.retrieved_at,
                        fingerprint,
                    ),
                )

            self.connection.execute(
                """
                INSERT INTO observation_transition (
                    source_id, observation_id, observed_at, retrieved_at,
                    transition_kind, envelope_hash, history_sequence_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    envelope.source_id,
                    envelope.observation_id,
                    envelope.observed_at,
                    envelope.retrieved_at,
                    kind,
                    fingerprint,
                    history_sequence_id,
                ),
            )

        return ObservationTransition(
            envelope.source_id,
            envelope.observation_id,
            kind,
            history_sequence_id,
            fingerprint,
        )

    def _envelope_for_sequence(self, sequence_id: int) -> ObservationEnvelope:
        row = self.connection.execute(
            "SELECT envelope_json FROM observation_history WHERE sequence_id=?",
            (sequence_id,),
        ).fetchone()
        if row is None:
            raise KeyError(sequence_id)
        payload = json.loads(row["envelope_json"])
        if not isinstance(payload, dict):
            raise ValueError("stored envelope JSON is invalid")
        return envelope_from_stored_dict(payload)

    def current(self, source_id: str, observation_id: str) -> ObservationEnvelope | None:
        row = self._current_row(source_id, observation_id)
        if row is None:
            return None
        return self._envelope_for_sequence(int(row["sequence_id"]))

    def history(
        self, source_id: str, observation_id: str
    ) -> tuple[ObservationEnvelope, ...]:
        rows = self.connection.execute(
            """
            SELECT sequence_id FROM observation_history
            WHERE source_id=? AND observation_id=? ORDER BY sequence_id
            """,
            (source_id, observation_id),
        ).fetchall()
        return tuple(self._envelope_for_sequence(int(row["sequence_id"])) for row in rows)

    def transitions(
        self, source_id: str, observation_id: str
    ) -> tuple[ObservationTransition, ...]:
        rows = self.connection.execute(
            """
            SELECT * FROM observation_transition
            WHERE source_id=? AND observation_id=? ORDER BY sequence_id
            """,
            (source_id, observation_id),
        ).fetchall()
        return tuple(
            ObservationTransition(
                source_id=row["source_id"],
                observation_id=row["observation_id"],
                kind=row["transition_kind"],
                history_sequence_id=int(row["history_sequence_id"]),
                envelope_hash=row["envelope_hash"],
            )
            for row in rows
        )

    def query(
        self,
        *,
        source_id: str | None = None,
        actor_id: str | None = None,
        primitive: str | None = None,
        concept: str | None = None,
        geography: str | None = None,
        observed_from: str | None = None,
        observed_to: str | None = None,
        include_history: bool = False,
    ) -> tuple[ObservationEnvelope, ...]:
        if primitive is not None and not primitive.strip():
            raise ValueError("primitive must not be blank")
        for name, value in (("observed_from", observed_from), ("observed_to", observed_to)):
            if value is not None:
                _parse_time(value)

        base = (
            "SELECT h.sequence_id FROM observation_history h"
            if include_history
            else """
            SELECT h.sequence_id FROM observation_history h
            JOIN observation_current c ON c.sequence_id=h.sequence_id
            """
        )
        clauses: list[str] = []
        params: list[str] = []
        if source_id is not None:
            clauses.append("h.source_id=?")
            params.append(source_id)
        if observed_from is not None:
            clauses.append("h.observed_at>=?")
            params.append(observed_from)
        if observed_to is not None:
            clauses.append("h.observed_at<=?")
            params.append(observed_to)
        if actor_id is not None:
            clauses.append(
                "EXISTS(SELECT 1 FROM observation_actor_index a WHERE a.sequence_id=h.sequence_id AND a.actor_id=?)"
            )
            params.append(actor_id)
        if geography is not None:
            clauses.append(
                "EXISTS(SELECT 1 FROM observation_geography_index g WHERE g.sequence_id=h.sequence_id AND g.geography=?)"
            )
            params.append(geography)
        if primitive is not None or concept is not None:
            sub = ["ci.sequence_id=h.sequence_id"]
            if primitive is not None:
                sub.append("ci.primitive=?")
                params.append(primitive)
            if concept is not None:
                sub.append("ci.concept=?")
                params.append(concept)
            clauses.append(
                "EXISTS(SELECT 1 FROM observation_claim_index ci WHERE "
                + " AND ".join(sub)
                + ")"
            )

        sql = base
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY h.sequence_id"
        rows = self.connection.execute(sql, tuple(params)).fetchall()
        return tuple(self._envelope_for_sequence(int(row["sequence_id"])) for row in rows)

    def iter_current(self) -> Iterable[ObservationEnvelope]:
        return self.query()


GOVERNING_INVARIANTS = (
    "SQLITE_IS_STORAGE_NOT_ONTOLOGY",
    "OBSERVATION_HISTORY_IS_APPEND_ONLY",
    "REVISION_NE_SILENT_OVERWRITE",
    "OUT_OF_ORDER_NE_CURRENT_ROLLBACK",
    "DUPLICATE_INGESTION_IS_IDEMPOTENT",
    "MISSING_NE_ZERO",
    "UNKNOWN_NE_FALSE",
)
