"""Persistent verification ledger for capability truth beyond public observation.

Ordinary sensors and reviewed public/manual intake may create OBSERVED or INFERRED
capability claims only. This module is the separate evidence boundary for explicit
confirmation or falsification. Verification never rewrites the underlying raw signal
or capability-graph materialization; it produces a time-scoped projection.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Sequence

from src.live_resource_signals import (
    AvailabilityState,
    CapabilityClaim,
    EvidenceStatus,
    PermissionState,
)


class VerificationVerdict(str, Enum):
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class CapabilityVerificationEvent:
    verification_id: str
    actor_ref: str
    capability_key: str
    verdict: VerificationVerdict
    verified_at: datetime
    evidence_ref: str
    evidence_note: str
    geography: str = ""
    availability: AvailabilityState = AvailabilityState.UNKNOWN
    permission: PermissionState = PermissionState.UNKNOWN
    related_signal_refs: Sequence[str] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.verification_id.strip():
            errors.append("missing:verification_id")
        if not self.actor_ref.strip():
            errors.append("missing:actor_ref")
        if not self.capability_key.strip():
            errors.append("missing:capability_key")
        if self.verified_at.tzinfo is None:
            errors.append("verified_at_must_be_timezone_aware")
        if not self.evidence_ref.strip():
            errors.append("missing:evidence_ref")
        if not self.evidence_note.strip():
            errors.append("missing:evidence_note")
        if any(not isinstance(ref, str) or not ref.strip() for ref in self.related_signal_refs):
            errors.append("invalid:related_signal_refs")

        if self.verdict is VerificationVerdict.CONFIRMED:
            if self.availability is AvailabilityState.ADVERTISED:
                errors.append("invalid:confirmed_availability_advertised")
        elif self.verdict is VerificationVerdict.REJECTED:
            if self.availability is not AvailabilityState.UNKNOWN:
                errors.append("rejected_capability_must_not_set_availability")
            if self.permission is not PermissionState.UNKNOWN:
                errors.append("rejected_capability_must_not_set_permission")
        return errors


_SCHEMA = """
CREATE TABLE IF NOT EXISTS capability_verification_event (
    sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    verification_id TEXT NOT NULL UNIQUE,
    actor_ref TEXT NOT NULL,
    capability_key TEXT NOT NULL,
    verdict TEXT NOT NULL,
    verified_at TEXT NOT NULL,
    evidence_ref TEXT NOT NULL,
    evidence_note TEXT NOT NULL,
    geography TEXT NOT NULL,
    availability TEXT NOT NULL,
    permission TEXT NOT NULL,
    related_signal_refs_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_capability_verification_identity
ON capability_verification_event(actor_ref, capability_key, verified_at, sequence_id);
"""


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    return value.astimezone(timezone.utc)


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _event_payload(event: CapabilityVerificationEvent) -> dict[str, object]:
    return {
        "verification_id": event.verification_id.strip(),
        "actor_ref": event.actor_ref.strip(),
        "capability_key": event.capability_key.strip(),
        "verdict": event.verdict.value,
        "verified_at": _utc(event.verified_at).isoformat(),
        "evidence_ref": event.evidence_ref.strip(),
        "evidence_note": event.evidence_note.strip(),
        "geography": event.geography.strip(),
        "availability": event.availability.value,
        "permission": event.permission.value,
        "related_signal_refs": [ref.strip() for ref in event.related_signal_refs],
    }


def _event_identity(event: CapabilityVerificationEvent) -> tuple[object, ...]:
    payload = _event_payload(event)
    return (
        payload["verification_id"],
        payload["actor_ref"],
        payload["capability_key"],
        payload["verdict"],
        payload["verified_at"],
        payload["evidence_ref"],
        payload["evidence_note"],
        payload["geography"],
        payload["availability"],
        payload["permission"],
        tuple(payload["related_signal_refs"]),
    )


def _verification_claim(event: CapabilityVerificationEvent) -> CapabilityClaim:
    refs = (f"verification::{event.verification_id.strip()}",) + tuple(
        ref.strip() for ref in event.related_signal_refs
    )
    return CapabilityClaim(
        actor_ref=event.actor_ref.strip(),
        capability_key=event.capability_key.strip(),
        evidence_status=EvidenceStatus.CONFIRMED,
        source_signal_ids=refs,
        rationale=event.evidence_note.strip(),
        last_observed_at=_utc(event.verified_at),
        geography=event.geography.strip(),
        availability=event.availability,
        permission=event.permission,
        inference_rule_id="",
    )


class SQLiteCapabilityVerificationStore:
    """Append-only verification/falsification evidence and time-scoped projection."""

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

    def __enter__(self) -> "SQLiteCapabilityVerificationStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @staticmethod
    def _event_from_row(row: sqlite3.Row) -> CapabilityVerificationEvent:
        refs = json.loads(row["related_signal_refs_json"])
        if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
            raise ValueError("stored related signal refs are invalid")
        verified_at = datetime.fromisoformat(row["verified_at"])
        if verified_at.tzinfo is None:
            raise ValueError("stored verification time must be timezone-aware")
        return CapabilityVerificationEvent(
            verification_id=row["verification_id"],
            actor_ref=row["actor_ref"],
            capability_key=row["capability_key"],
            verdict=VerificationVerdict(row["verdict"]),
            verified_at=verified_at,
            evidence_ref=row["evidence_ref"],
            evidence_note=row["evidence_note"],
            geography=row["geography"],
            availability=AvailabilityState(row["availability"]),
            permission=PermissionState(row["permission"]),
            related_signal_refs=tuple(refs),
        )

    def get(self, verification_id: str) -> CapabilityVerificationEvent | None:
        row = self.connection.execute(
            "SELECT * FROM capability_verification_event WHERE verification_id = ?",
            (verification_id,),
        ).fetchone()
        return None if row is None else self._event_from_row(row)

    def append(self, event: CapabilityVerificationEvent) -> None:
        errors = event.validate()
        if errors:
            raise ValueError("invalid capability verification: " + ",".join(errors))

        existing = self.get(event.verification_id.strip())
        if existing is not None:
            if _event_identity(existing) != _event_identity(event):
                raise ValueError("verification_id already exists with different content")
            return

        payload = _event_payload(event)
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO capability_verification_event (
                    verification_id, actor_ref, capability_key, verdict, verified_at,
                    evidence_ref, evidence_note, geography, availability, permission,
                    related_signal_refs_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["verification_id"],
                    payload["actor_ref"],
                    payload["capability_key"],
                    payload["verdict"],
                    payload["verified_at"],
                    payload["evidence_ref"],
                    payload["evidence_note"],
                    payload["geography"],
                    payload["availability"],
                    payload["permission"],
                    _json(payload["related_signal_refs"]),
                ),
            )

    def events(self, *, as_of: datetime | None = None) -> tuple[CapabilityVerificationEvent, ...]:
        if as_of is None:
            rows = self.connection.execute(
                "SELECT * FROM capability_verification_event ORDER BY verified_at, sequence_id"
            ).fetchall()
        else:
            boundary = _utc(as_of).isoformat()
            rows = self.connection.execute(
                """
                SELECT * FROM capability_verification_event
                WHERE verified_at <= ? ORDER BY verified_at, sequence_id
                """,
                (boundary,),
            ).fetchall()
        return tuple(self._event_from_row(row) for row in rows)

    def latest_events(
        self, *, as_of: datetime | None = None
    ) -> tuple[CapabilityVerificationEvent, ...]:
        latest: dict[tuple[str, str], CapabilityVerificationEvent] = {}
        for event in self.events(as_of=as_of):
            latest[(event.actor_ref, event.capability_key)] = event
        return tuple(latest[key] for key in sorted(latest))

    def snapshot_fingerprint(self, *, as_of: datetime) -> str:
        if as_of.tzinfo is None:
            raise ValueError("as_of must be timezone-aware")
        payload = [_event_payload(event) for event in self.latest_events(as_of=as_of)]
        return hashlib.sha256(_json(payload).encode("utf-8")).hexdigest()

    def project_claims(
        self,
        base_claims: Sequence[CapabilityClaim],
        *,
        as_of: datetime,
    ) -> tuple[CapabilityClaim, ...]:
        """Overlay explicit verification without rewriting base graph lineage.

        A latest REJECTED event suppresses base claims for the same actor/capability only
        when the rejection is at least as new as that base evidence. A newer observation
        may therefore re-open the capability as OBSERVED/INFERRED until it is verified
        again. A latest CONFIRMED event contributes a separate CONFIRMED claim.
        """

        if as_of.tzinfo is None:
            raise ValueError("as_of must be timezone-aware")
        latest = {
            (event.actor_ref, event.capability_key): event
            for event in self.latest_events(as_of=as_of)
        }

        projected: list[CapabilityClaim] = []
        for claim in base_claims:
            event = latest.get((claim.actor_ref, claim.capability_key))
            if (
                event is not None
                and event.verdict is VerificationVerdict.REJECTED
                and _utc(event.verified_at) >= _utc(claim.last_observed_at)
            ):
                continue
            projected.append(claim)

        for event in latest.values():
            if event.verdict is VerificationVerdict.CONFIRMED:
                projected.append(_verification_claim(event))

        return tuple(
            sorted(
                projected,
                key=lambda claim: (
                    claim.actor_ref,
                    claim.capability_key,
                    claim.evidence_status.value,
                    tuple(claim.source_signal_ids),
                    claim.last_observed_at.isoformat(),
                ),
            )
        )


GOVERNING_INVARIANTS = (
    "PUBLIC_OBSERVATION_NE_VERIFICATION",
    "VERIFICATION_EVENT_REQUIRES_EXPLICIT_EVIDENCE_REF",
    "VERIFICATION_HISTORY_IS_APPEND_ONLY",
    "CONFIRMATION_NE_AVAILABILITY",
    "CONFIRMATION_NE_PERMISSION",
    "REJECTION_DOES_NOT_REWRITE_RAW_EVIDENCE",
    "NEWER_OBSERVATION_MAY_REOPEN_REJECTED_CAPABILITY_AS_UNVERIFIED",
    "CONFIRMED_CLAIM_NE_CALLABLE_UNLESS_AVAILABILITY_PERMISSION_FRESHNESS_PASS",
    "CALLABLE_NE_TRANSACTIONABLE",
    "UNKNOWN_NE_PASS",
)
