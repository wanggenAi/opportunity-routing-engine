"""Append-only validation evidence for exact resource-composition hypotheses.

This layer sits after structural resource composition. It preserves existing access
semantics and the canonical G0-G3 transaction gates without allowing one evidence
dimension to promote another.

Canonical transaction gates remain:
G0 Actor / role clarity
G1 Payer clarity
G2 Transactionability
G3 Legal / trust / safety
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Mapping

from src.access_feasibility import AccessFeasibility, AccessState, access_state
from src.composition_run_store import SQLiteCompositionRunStore
from src.resource_composition import CompositionState


class ValidationDimension(str, Enum):
    ACTOR_ROLE_CLARITY = "ACTOR_ROLE_CLARITY"
    PAYER_CLARITY = "PAYER_CLARITY"
    NEED_CONFIRMATION = "NEED_CONFIRMATION"
    OPERATOR_ACCESS = "OPERATOR_ACCESS"
    COUNTERPARTY_VISIBLE_SURPLUS = "COUNTERPARTY_VISIBLE_SURPLUS"
    COUNTERPARTY_CONSENT = "COUNTERPARTY_CONSENT"
    PAYER_COMMITMENT = "PAYER_COMMITMENT"
    ECONOMICS = "ECONOMICS"
    LEGAL_TRUST_SAFETY = "LEGAL_TRUST_SAFETY"


class ValidationGateState(str, Enum):
    UNKNOWN = "UNKNOWN"
    PASS = "PASS"
    FAIL = "FAIL"
    CONDITIONAL = "CONDITIONAL"


_STANDARD_DIMENSIONS = {
    ValidationDimension.ACTOR_ROLE_CLARITY,
    ValidationDimension.PAYER_CLARITY,
    ValidationDimension.NEED_CONFIRMATION,
    ValidationDimension.COUNTERPARTY_VISIBLE_SURPLUS,
    ValidationDimension.COUNTERPARTY_CONSENT,
    ValidationDimension.PAYER_COMMITMENT,
    ValidationDimension.ECONOMICS,
    ValidationDimension.LEGAL_TRUST_SAFETY,
}


@dataclass(frozen=True)
class CompositionValidationEvent:
    validation_id: str
    composition_run_id: int
    hypothesis_index: int
    dimension: ValidationDimension
    value: str
    observed_at: datetime
    evidence_ref: str
    evidence_note: str
    subject_ref: str = ""
    details: Mapping[str, object] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.validation_id.strip():
            errors.append("missing:validation_id")
        if self.composition_run_id < 1:
            errors.append("invalid:composition_run_id")
        if self.hypothesis_index < 0:
            errors.append("invalid:hypothesis_index")
        if self.observed_at.tzinfo is None:
            errors.append("observed_at_must_be_timezone_aware")
        if not self.evidence_ref.strip():
            errors.append("missing:evidence_ref")
        if not self.evidence_note.strip():
            errors.append("missing:evidence_note")

        if self.dimension is ValidationDimension.OPERATOR_ACCESS:
            try:
                state = AccessState(self.value)
            except ValueError:
                errors.append("invalid:operator_access_state")
            else:
                if state is AccessState.UNASSESSED:
                    errors.append("operator_access_event_must_be_assessed")
        elif self.dimension in _STANDARD_DIMENSIONS:
            try:
                state = ValidationGateState(self.value)
            except ValueError:
                errors.append("invalid:validation_gate_state")
            else:
                if state is ValidationGateState.UNKNOWN:
                    errors.append("validation_event_must_not_assert_unknown")
                if (
                    state is ValidationGateState.CONDITIONAL
                    and self.dimension is not ValidationDimension.LEGAL_TRUST_SAFETY
                ):
                    errors.append("conditional_only_allowed_for_legal_trust_safety")

        try:
            json.dumps(self.details, ensure_ascii=False, sort_keys=True)
        except (TypeError, ValueError):
            errors.append("details_must_be_json_serializable")
        return errors


@dataclass(frozen=True)
class CompositionValidationProjection:
    composition_run_id: int
    hypothesis_index: int
    composition_state: CompositionState
    access_state: AccessState
    actor_role_clarity: ValidationGateState
    payer_clarity: ValidationGateState
    need_confirmation: ValidationGateState
    counterparty_visible_surplus: ValidationGateState
    counterparty_consent: ValidationGateState
    payer_commitment: ValidationGateState
    economics: ValidationGateState
    legal_trust_safety: ValidationGateState
    evidence_snapshot_fingerprint: str

    @staticmethod
    def _combine(*states: ValidationGateState) -> ValidationGateState:
        if any(state is ValidationGateState.FAIL for state in states):
            return ValidationGateState.FAIL
        if all(state is ValidationGateState.PASS for state in states):
            return ValidationGateState.PASS
        return ValidationGateState.UNKNOWN

    def transaction_gates(self) -> dict[str, str]:
        """Project only canonical G0-G3; never invent strategic G4-G6 truth."""

        # Canonical definitions are fixed by FORMAL_TRUTH / OPPORTUNITY_SCORECARD.
        g0 = self.actor_role_clarity
        g1 = self.payer_clarity

        if self.access_state is AccessState.ACCESS_BLOCKED:
            access_gate = ValidationGateState.FAIL
        elif self.access_state is AccessState.VALIDATION_ACCESS_READY:
            access_gate = ValidationGateState.PASS
        else:
            access_gate = ValidationGateState.UNKNOWN

        callable_gate = (
            ValidationGateState.PASS
            if self.composition_state is CompositionState.CALLABLE_COMPOSED
            else ValidationGateState.UNKNOWN
        )
        g2 = self._combine(
            callable_gate,
            self.need_confirmation,
            access_gate,
            self.counterparty_visible_surplus,
            self.counterparty_consent,
            self.payer_commitment,
            self.economics,
        )
        g3 = self.legal_trust_safety
        return {"G0": g0.value, "G1": g1.value, "G2": g2.value, "G3": g3.value}

    @property
    def bounded_transaction_ready(self) -> bool:
        gates = self.transaction_gates()
        return (
            gates["G0"] == "PASS"
            and gates["G1"] == "PASS"
            and gates["G2"] == "PASS"
            and gates["G3"] in {"PASS", "CONDITIONAL"}
        )


_SCHEMA = """
CREATE TABLE IF NOT EXISTS composition_validation_event (
    sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    validation_id TEXT NOT NULL UNIQUE,
    composition_run_id INTEGER NOT NULL,
    hypothesis_index INTEGER NOT NULL,
    dimension TEXT NOT NULL,
    value TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    evidence_ref TEXT NOT NULL,
    evidence_note TEXT NOT NULL,
    subject_ref TEXT NOT NULL,
    details_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_composition_validation_target
ON composition_validation_event(
    composition_run_id, hypothesis_index, dimension, observed_at, sequence_id
);
"""


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    return value.astimezone(timezone.utc)


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _event_payload(event: CompositionValidationEvent) -> dict[str, object]:
    return {
        "validation_id": event.validation_id.strip(),
        "composition_run_id": event.composition_run_id,
        "hypothesis_index": event.hypothesis_index,
        "dimension": event.dimension.value,
        "value": event.value,
        "observed_at": _utc(event.observed_at).isoformat(),
        "evidence_ref": event.evidence_ref.strip(),
        "evidence_note": event.evidence_note.strip(),
        "subject_ref": event.subject_ref.strip(),
        "details": dict(event.details),
    }


def _access_details(record: AccessFeasibility) -> dict[str, object]:
    payload = asdict(record)
    payload["route_kind"] = record.route_kind.value
    payload["evidence"] = [
        {"source_id": item.source_id, "claim": item.claim} for item in record.evidence
    ]
    return payload


def access_validation_event(
    *,
    validation_id: str,
    composition_run_id: int,
    hypothesis_index: int,
    record: AccessFeasibility,
    observed_at: datetime,
    evidence_ref: str,
    evidence_note: str,
) -> CompositionValidationEvent:
    """Persist canonical access_state(record), never a parallel access classifier."""

    return CompositionValidationEvent(
        validation_id=validation_id,
        composition_run_id=composition_run_id,
        hypothesis_index=hypothesis_index,
        dimension=ValidationDimension.OPERATOR_ACCESS,
        value=access_state(record).value,
        observed_at=observed_at,
        evidence_ref=evidence_ref,
        evidence_note=evidence_note,
        subject_ref=record.target_actor,
        details=_access_details(record),
    )


class SQLiteCompositionValidationStore:
    """Append-only validation evidence bound to immutable composition hypotheses."""

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

    def __enter__(self) -> "SQLiteCompositionValidationStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @staticmethod
    def _event_from_row(row: sqlite3.Row) -> CompositionValidationEvent:
        observed_at = datetime.fromisoformat(row["observed_at"])
        if observed_at.tzinfo is None:
            raise ValueError("stored validation time must be timezone-aware")
        details = json.loads(row["details_json"])
        if not isinstance(details, dict):
            raise ValueError("stored validation details must be an object")
        return CompositionValidationEvent(
            validation_id=row["validation_id"],
            composition_run_id=int(row["composition_run_id"]),
            hypothesis_index=int(row["hypothesis_index"]),
            dimension=ValidationDimension(row["dimension"]),
            value=row["value"],
            observed_at=observed_at,
            evidence_ref=row["evidence_ref"],
            evidence_note=row["evidence_note"],
            subject_ref=row["subject_ref"],
            details=details,
        )

    def get(self, validation_id: str) -> CompositionValidationEvent | None:
        row = self.connection.execute(
            "SELECT * FROM composition_validation_event WHERE validation_id = ?",
            (validation_id,),
        ).fetchone()
        return None if row is None else self._event_from_row(row)

    @staticmethod
    def _assert_target_exists(
        event: CompositionValidationEvent,
        composition_runs: SQLiteCompositionRunStore,
    ) -> None:
        run = composition_runs.get_run(event.composition_run_id)
        if run is None:
            raise ValueError("unknown composition_run_id")
        hypotheses = composition_runs.hypotheses(event.composition_run_id)
        if event.hypothesis_index >= len(hypotheses):
            raise ValueError("unknown composition hypothesis index")

    def append(
        self,
        event: CompositionValidationEvent,
        *,
        composition_runs: SQLiteCompositionRunStore,
    ) -> None:
        errors = event.validate()
        if errors:
            raise ValueError("invalid composition validation: " + ",".join(errors))
        self._assert_target_exists(event, composition_runs)

        existing = self.get(event.validation_id.strip())
        if existing is not None:
            if _event_payload(existing) != _event_payload(event):
                raise ValueError("validation_id already exists with different content")
            return

        payload = _event_payload(event)
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO composition_validation_event (
                    validation_id, composition_run_id, hypothesis_index, dimension,
                    value, observed_at, evidence_ref, evidence_note, subject_ref,
                    details_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["validation_id"],
                    payload["composition_run_id"],
                    payload["hypothesis_index"],
                    payload["dimension"],
                    payload["value"],
                    payload["observed_at"],
                    payload["evidence_ref"],
                    payload["evidence_note"],
                    payload["subject_ref"],
                    _json(payload["details"]),
                ),
            )

    def events(
        self,
        composition_run_id: int,
        hypothesis_index: int,
        *,
        as_of: datetime | None = None,
    ) -> tuple[CompositionValidationEvent, ...]:
        params: list[object] = [composition_run_id, hypothesis_index]
        where = "composition_run_id = ? AND hypothesis_index = ?"
        if as_of is not None:
            where += " AND observed_at <= ?"
            params.append(_utc(as_of).isoformat())
        rows = self.connection.execute(
            f"""
            SELECT * FROM composition_validation_event
            WHERE {where}
            ORDER BY observed_at, sequence_id
            """,
            tuple(params),
        ).fetchall()
        return tuple(self._event_from_row(row) for row in rows)

    def latest_events(
        self,
        composition_run_id: int,
        hypothesis_index: int,
        *,
        as_of: datetime,
    ) -> dict[ValidationDimension, CompositionValidationEvent]:
        latest: dict[ValidationDimension, CompositionValidationEvent] = {}
        for event in self.events(
            composition_run_id, hypothesis_index, as_of=as_of
        ):
            latest[event.dimension] = event
        return latest

    def snapshot_fingerprint(
        self,
        composition_run_id: int,
        hypothesis_index: int,
        *,
        as_of: datetime,
    ) -> str:
        latest = self.latest_events(
            composition_run_id, hypothesis_index, as_of=as_of
        )
        payload = [
            _event_payload(latest[dimension])
            for dimension in sorted(latest, key=lambda item: item.value)
        ]
        return hashlib.sha256(_json(payload).encode("utf-8")).hexdigest()

    def projection(
        self,
        composition_run_id: int,
        hypothesis_index: int,
        *,
        composition_runs: SQLiteCompositionRunStore,
        as_of: datetime,
    ) -> CompositionValidationProjection:
        if as_of.tzinfo is None:
            raise ValueError("as_of must be timezone-aware")
        run = composition_runs.get_run(composition_run_id)
        if run is None:
            raise ValueError("unknown composition_run_id")
        hypotheses = composition_runs.hypotheses(composition_run_id)
        if hypothesis_index < 0 or hypothesis_index >= len(hypotheses):
            raise ValueError("unknown composition hypothesis index")
        hypothesis = hypotheses[hypothesis_index]

        latest = self.latest_events(
            composition_run_id, hypothesis_index, as_of=as_of
        )

        access = AccessState.UNASSESSED
        access_event = latest.get(ValidationDimension.OPERATOR_ACCESS)
        if access_event is not None:
            access = AccessState(access_event.value)

        def gate(dimension: ValidationDimension) -> ValidationGateState:
            event = latest.get(dimension)
            return (
                ValidationGateState.UNKNOWN
                if event is None
                else ValidationGateState(event.value)
            )

        return CompositionValidationProjection(
            composition_run_id=composition_run_id,
            hypothesis_index=hypothesis_index,
            composition_state=hypothesis.state,
            access_state=access,
            actor_role_clarity=gate(ValidationDimension.ACTOR_ROLE_CLARITY),
            payer_clarity=gate(ValidationDimension.PAYER_CLARITY),
            need_confirmation=gate(ValidationDimension.NEED_CONFIRMATION),
            counterparty_visible_surplus=gate(
                ValidationDimension.COUNTERPARTY_VISIBLE_SURPLUS
            ),
            counterparty_consent=gate(ValidationDimension.COUNTERPARTY_CONSENT),
            payer_commitment=gate(ValidationDimension.PAYER_COMMITMENT),
            economics=gate(ValidationDimension.ECONOMICS),
            legal_trust_safety=gate(ValidationDimension.LEGAL_TRUST_SAFETY),
            evidence_snapshot_fingerprint=self.snapshot_fingerprint(
                composition_run_id, hypothesis_index, as_of=as_of
            ),
        )


GOVERNING_INVARIANTS = (
    "COMPOSITION_VALIDATION_BINDS_EXACT_RUN_AND_HYPOTHESIS",
    "ACCESS_STATE_USES_CANONICAL_ACCESS_FEASIBILITY_MODEL",
    "G0_IS_ACTOR_ROLE_CLARITY",
    "G1_IS_PAYER_CLARITY",
    "G2_IS_TRANSACTIONABILITY",
    "G3_IS_LEGAL_TRUST_SAFETY",
    "OPERATOR_ACCESS_NE_COUNTERPARTY_CONSENT",
    "PAYER_CLARITY_NE_PAYER_COMMITMENT",
    "COUNTERPARTY_VISIBLE_SURPLUS_NE_PAYER_COMMITMENT",
    "PAYER_COMMITMENT_NE_ECONOMICS",
    "ONE_VALIDATION_DIMENSION_NE_ANOTHER",
    "VALIDATION_HISTORY_IS_APPEND_ONLY",
    "UNKNOWN_NE_PASS",
    "G0_G3_PROJECTION_NE_G4_G6_TRUTH",
)
