"""Append-only real-world outcome evidence for exact composition hypotheses.

Outcome evidence begins only after a composition has an explicit transaction-validation
snapshot. It records what actually happened without rewriting discovery, capability,
composition, or validation history.

Evidence maturity is conservative:
- L3 requires a deposit, authorized commitment, or signed task;
- L4 requires delivery acceptance AND observed positive settlement for the same transaction;
- L5 requires a second accepted+settled transaction or a referral after L4;
- L6 requires L5 plus delegated repeat, successful provider replacement, or successful
  alternate route on an accepted+settled transaction;
- L7 is never inferred here.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from enum import Enum
from pathlib import Path
from typing import Mapping

from src.composition_run_store import SQLiteCompositionRunStore
from src.composition_validation_store import SQLiteCompositionValidationStore


class OutcomeEventType(str, Enum):
    ROUTE_TEST_STARTED = "ROUTE_TEST_STARTED"
    DEPOSIT_OBSERVED = "DEPOSIT_OBSERVED"
    AUTHORIZED_COMMITMENT_OBSERVED = "AUTHORIZED_COMMITMENT_OBSERVED"
    SIGNED_TASK_OBSERVED = "SIGNED_TASK_OBSERVED"
    DELIVERY_ACCEPTED = "DELIVERY_ACCEPTED"
    DELIVERY_REJECTED = "DELIVERY_REJECTED"
    SETTLEMENT_OBSERVED = "SETTLEMENT_OBSERVED"
    SETTLEMENT_FAILED = "SETTLEMENT_FAILED"
    REFERRAL_OBSERVED = "REFERRAL_OBSERVED"
    DELEGATED_REPEAT_OBSERVED = "DELEGATED_REPEAT_OBSERVED"
    PROVIDER_REPLACEMENT_SUCCEEDED = "PROVIDER_REPLACEMENT_SUCCEEDED"
    ALTERNATE_ROUTE_SUCCEEDED = "ALTERNATE_ROUTE_SUCCEEDED"
    ROUTE_FAILED = "ROUTE_FAILED"


_COMMITMENT_EVENTS = {
    OutcomeEventType.DEPOSIT_OBSERVED,
    OutcomeEventType.AUTHORIZED_COMMITMENT_OBSERVED,
    OutcomeEventType.SIGNED_TASK_OBSERVED,
}

_L6_EVENTS = {
    OutcomeEventType.DELEGATED_REPEAT_OBSERVED,
    OutcomeEventType.PROVIDER_REPLACEMENT_SUCCEEDED,
    OutcomeEventType.ALTERNATE_ROUTE_SUCCEEDED,
}


@dataclass(frozen=True)
class CompositionOutcomeEvent:
    outcome_id: str
    composition_run_id: int
    hypothesis_index: int
    transaction_ref: str
    event_type: OutcomeEventType
    observed_at: datetime
    validation_as_of: datetime
    validation_snapshot_fingerprint: str
    evidence_ref: str
    evidence_note: str
    subject_ref: str = ""
    amount: str | None = None
    currency: str | None = None
    details: Mapping[str, object] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.outcome_id.strip():
            errors.append("missing:outcome_id")
        if self.composition_run_id < 1:
            errors.append("invalid:composition_run_id")
        if self.hypothesis_index < 0:
            errors.append("invalid:hypothesis_index")
        if not self.transaction_ref.strip():
            errors.append("missing:transaction_ref")
        if self.observed_at.tzinfo is None:
            errors.append("observed_at_must_be_timezone_aware")
        if self.validation_as_of.tzinfo is None:
            errors.append("validation_as_of_must_be_timezone_aware")
        if (
            self.observed_at.tzinfo is not None
            and self.validation_as_of.tzinfo is not None
            and _utc(self.observed_at) < _utc(self.validation_as_of)
        ):
            errors.append("outcome_cannot_precede_validation_snapshot")
        if not self.validation_snapshot_fingerprint.strip():
            errors.append("missing:validation_snapshot_fingerprint")
        if not self.evidence_ref.strip():
            errors.append("missing:evidence_ref")
        if not self.evidence_note.strip():
            errors.append("missing:evidence_note")

        if self.event_type is OutcomeEventType.SETTLEMENT_OBSERVED:
            if self.amount is None or not str(self.amount).strip():
                errors.append("settlement_requires_amount")
            else:
                try:
                    parsed = Decimal(str(self.amount).replace(",", ""))
                except InvalidOperation:
                    errors.append("invalid:settlement_amount")
                else:
                    if parsed <= 0:
                        errors.append("settlement_amount_must_be_positive")
            if self.currency is None or not str(self.currency).strip():
                errors.append("settlement_requires_currency")
        elif self.amount is not None or self.currency is not None:
            errors.append("amount_currency_only_allowed_for_settlement")

        try:
            json.dumps(self.details, ensure_ascii=False, sort_keys=True)
        except (TypeError, ValueError):
            errors.append("details_must_be_json_serializable")
        return errors


@dataclass(frozen=True)
class CompositionOutcomeProjection:
    composition_run_id: int
    hypothesis_index: int
    as_of: datetime
    evidence_maturity: str
    event_count: int
    transaction_count: int
    accepted_settled_transaction_count: int
    failed_transaction_count: int
    commitment_observed: bool
    referral_observed: bool
    l6_mechanism_observed: bool
    settlement_totals: Mapping[str, str]
    latest_event_type: OutcomeEventType | None
    evidence_snapshot_fingerprint: str


_SCHEMA = """
CREATE TABLE IF NOT EXISTS composition_outcome_event (
    sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    outcome_id TEXT NOT NULL UNIQUE,
    composition_run_id INTEGER NOT NULL,
    hypothesis_index INTEGER NOT NULL,
    transaction_ref TEXT NOT NULL,
    event_type TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    validation_as_of TEXT NOT NULL,
    validation_snapshot_fingerprint TEXT NOT NULL,
    evidence_ref TEXT NOT NULL,
    evidence_note TEXT NOT NULL,
    subject_ref TEXT NOT NULL,
    amount TEXT,
    currency TEXT,
    details_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_composition_outcome_target
ON composition_outcome_event(
    composition_run_id, hypothesis_index, observed_at, sequence_id
);

CREATE INDEX IF NOT EXISTS idx_composition_outcome_transaction
ON composition_outcome_event(
    composition_run_id, hypothesis_index, transaction_ref, observed_at, sequence_id
);
"""


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    return value.astimezone(timezone.utc)


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _event_payload(event: CompositionOutcomeEvent) -> dict[str, object]:
    return {
        "outcome_id": event.outcome_id.strip(),
        "composition_run_id": event.composition_run_id,
        "hypothesis_index": event.hypothesis_index,
        "transaction_ref": event.transaction_ref.strip(),
        "event_type": event.event_type.value,
        "observed_at": _utc(event.observed_at).isoformat(),
        "validation_as_of": _utc(event.validation_as_of).isoformat(),
        "validation_snapshot_fingerprint": event.validation_snapshot_fingerprint.strip(),
        "evidence_ref": event.evidence_ref.strip(),
        "evidence_note": event.evidence_note.strip(),
        "subject_ref": event.subject_ref.strip(),
        "amount": None if event.amount is None else str(event.amount).replace(",", "").strip(),
        "currency": None if event.currency is None else str(event.currency).strip().upper(),
        "details": dict(event.details),
    }


class SQLiteCompositionOutcomeStore:
    """Persist immutable outcome observations and derive conservative maturity views."""

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

    def __enter__(self) -> "SQLiteCompositionOutcomeStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @staticmethod
    def _event_from_row(row: sqlite3.Row) -> CompositionOutcomeEvent:
        observed_at = datetime.fromisoformat(row["observed_at"])
        validation_as_of = datetime.fromisoformat(row["validation_as_of"])
        if observed_at.tzinfo is None or validation_as_of.tzinfo is None:
            raise ValueError("stored outcome datetimes must be timezone-aware")
        details = json.loads(row["details_json"])
        if not isinstance(details, dict):
            raise ValueError("stored outcome details must be an object")
        return CompositionOutcomeEvent(
            outcome_id=row["outcome_id"],
            composition_run_id=int(row["composition_run_id"]),
            hypothesis_index=int(row["hypothesis_index"]),
            transaction_ref=row["transaction_ref"],
            event_type=OutcomeEventType(row["event_type"]),
            observed_at=observed_at,
            validation_as_of=validation_as_of,
            validation_snapshot_fingerprint=row["validation_snapshot_fingerprint"],
            evidence_ref=row["evidence_ref"],
            evidence_note=row["evidence_note"],
            subject_ref=row["subject_ref"],
            amount=row["amount"],
            currency=row["currency"],
            details=details,
        )

    def get(self, outcome_id: str) -> CompositionOutcomeEvent | None:
        row = self.connection.execute(
            "SELECT * FROM composition_outcome_event WHERE outcome_id = ?",
            (outcome_id,),
        ).fetchone()
        return None if row is None else self._event_from_row(row)

    @staticmethod
    def _assert_target_and_validation_snapshot(
        event: CompositionOutcomeEvent,
        *,
        composition_runs: SQLiteCompositionRunStore,
        validations: SQLiteCompositionValidationStore,
    ) -> None:
        run = composition_runs.get_run(event.composition_run_id)
        if run is None:
            raise ValueError("unknown composition_run_id")
        hypotheses = composition_runs.hypotheses(event.composition_run_id)
        if event.hypothesis_index >= len(hypotheses):
            raise ValueError("unknown composition hypothesis index")

        projection = validations.projection(
            event.composition_run_id,
            event.hypothesis_index,
            composition_runs=composition_runs,
            as_of=event.validation_as_of,
        )
        if projection.evidence_snapshot_fingerprint != event.validation_snapshot_fingerprint:
            raise ValueError("validation_snapshot_fingerprint does not match exact validation_as_of")
        if not projection.bounded_transaction_ready:
            raise ValueError("outcome evidence requires bounded_transaction_ready validation snapshot")

    def append(
        self,
        event: CompositionOutcomeEvent,
        *,
        composition_runs: SQLiteCompositionRunStore,
        validations: SQLiteCompositionValidationStore,
    ) -> None:
        errors = event.validate()
        if errors:
            raise ValueError("invalid composition outcome: " + ",".join(errors))
        self._assert_target_and_validation_snapshot(
            event,
            composition_runs=composition_runs,
            validations=validations,
        )

        existing = self.get(event.outcome_id.strip())
        if existing is not None:
            if _event_payload(existing) != _event_payload(event):
                raise ValueError("outcome_id already exists with different content")
            return

        payload = _event_payload(event)
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO composition_outcome_event (
                    outcome_id, composition_run_id, hypothesis_index, transaction_ref,
                    event_type, observed_at, validation_as_of,
                    validation_snapshot_fingerprint, evidence_ref, evidence_note,
                    subject_ref, amount, currency, details_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["outcome_id"],
                    payload["composition_run_id"],
                    payload["hypothesis_index"],
                    payload["transaction_ref"],
                    payload["event_type"],
                    payload["observed_at"],
                    payload["validation_as_of"],
                    payload["validation_snapshot_fingerprint"],
                    payload["evidence_ref"],
                    payload["evidence_note"],
                    payload["subject_ref"],
                    payload["amount"],
                    payload["currency"],
                    _json(payload["details"]),
                ),
            )

    def events(
        self,
        composition_run_id: int,
        hypothesis_index: int,
        *,
        as_of: datetime | None = None,
    ) -> tuple[CompositionOutcomeEvent, ...]:
        params: list[object] = [composition_run_id, hypothesis_index]
        where = "composition_run_id = ? AND hypothesis_index = ?"
        if as_of is not None:
            where += " AND observed_at <= ?"
            params.append(_utc(as_of).isoformat())
        rows = self.connection.execute(
            f"""
            SELECT * FROM composition_outcome_event
            WHERE {where}
            ORDER BY observed_at, sequence_id
            """,
            tuple(params),
        ).fetchall()
        return tuple(self._event_from_row(row) for row in rows)

    def snapshot_fingerprint(
        self,
        composition_run_id: int,
        hypothesis_index: int,
        *,
        as_of: datetime,
    ) -> str:
        payload = [
            _event_payload(event)
            for event in self.events(composition_run_id, hypothesis_index, as_of=as_of)
        ]
        return hashlib.sha256(_json(payload).encode("utf-8")).hexdigest()

    def projection(
        self,
        composition_run_id: int,
        hypothesis_index: int,
        *,
        as_of: datetime,
    ) -> CompositionOutcomeProjection:
        if as_of.tzinfo is None:
            raise ValueError("as_of must be timezone-aware")
        events = self.events(composition_run_id, hypothesis_index, as_of=as_of)
        by_transaction: dict[str, list[CompositionOutcomeEvent]] = {}
        for event in events:
            by_transaction.setdefault(event.transaction_ref, []).append(event)

        successful_transactions: set[str] = set()
        failed_transactions: set[str] = set()
        commitment_observed = False
        referral_observed = False
        l6_transactions: set[str] = set()
        settlement_totals: dict[str, Decimal] = {}

        for transaction_ref, tx_events in by_transaction.items():
            event_types = {event.event_type for event in tx_events}
            if event_types & _COMMITMENT_EVENTS:
                commitment_observed = True
            if OutcomeEventType.REFERRAL_OBSERVED in event_types:
                referral_observed = True
            if event_types & {
                OutcomeEventType.ROUTE_FAILED,
                OutcomeEventType.DELIVERY_REJECTED,
                OutcomeEventType.SETTLEMENT_FAILED,
            }:
                failed_transactions.add(transaction_ref)
            has_acceptance = OutcomeEventType.DELIVERY_ACCEPTED in event_types
            settlements = [
                event
                for event in tx_events
                if event.event_type is OutcomeEventType.SETTLEMENT_OBSERVED
            ]
            if has_acceptance and settlements:
                successful_transactions.add(transaction_ref)
                for settlement in settlements:
                    currency = (settlement.currency or "").upper()
                    settlement_totals[currency] = settlement_totals.get(currency, Decimal("0")) + Decimal(
                        str(settlement.amount)
                    )
                if event_types & _L6_EVENTS:
                    l6_transactions.add(transaction_ref)

        maturity = "L0"
        if commitment_observed:
            maturity = "L3"
        if successful_transactions:
            maturity = "L4"
        if len(successful_transactions) >= 2 or (successful_transactions and referral_observed):
            maturity = "L5"
        if maturity == "L5" and l6_transactions:
            maturity = "L6"

        return CompositionOutcomeProjection(
            composition_run_id=composition_run_id,
            hypothesis_index=hypothesis_index,
            as_of=as_of,
            evidence_maturity=maturity,
            event_count=len(events),
            transaction_count=len(by_transaction),
            accepted_settled_transaction_count=len(successful_transactions),
            failed_transaction_count=len(failed_transactions),
            commitment_observed=commitment_observed,
            referral_observed=referral_observed,
            l6_mechanism_observed=bool(l6_transactions),
            settlement_totals={
                currency: format(amount, "f")
                for currency, amount in sorted(settlement_totals.items())
            },
            latest_event_type=None if not events else events[-1].event_type,
            evidence_snapshot_fingerprint=self.snapshot_fingerprint(
                composition_run_id, hypothesis_index, as_of=as_of
            ),
        )


GOVERNING_INVARIANTS = (
    "OUTCOME_BINDS_EXACT_COMPOSITION_AND_VALIDATION_SNAPSHOT",
    "ROUTE_TEST_STARTED_NE_COUNTERPARTY_COMMITMENT",
    "COMMITMENT_NE_DELIVERY_ACCEPTANCE",
    "DELIVERY_ACCEPTANCE_NE_SETTLEMENT",
    "SETTLEMENT_NE_PROFITABILITY",
    "ONE_ACCEPTED_SETTLED_TRANSACTION_NE_REPEATABILITY",
    "L4_REQUIRES_ACCEPTANCE_AND_SETTLEMENT_SAME_TRANSACTION",
    "L5_REQUIRES_REPEAT_OR_REFERRAL_AFTER_L4",
    "L6_REQUIRES_L5_AND_DELEGATED_OR_REPLACEMENT_OR_ALTERNATE_ROUTE_EVIDENCE",
    "OUTCOME_LEDGER_NE_G4_G6_GATE_TRUTH",
    "L7_IS_NOT_INFERRED_HERE",
    "FAILURE_EVENT_NE_FALSE_LATENT_VALUE_THESIS",
    "OUTCOME_HISTORY_IS_APPEND_ONLY",
    "UNKNOWN_NE_PASS",
)
