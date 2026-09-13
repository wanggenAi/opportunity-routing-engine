"""Reviewed JSON/JSONL intake for real composition outcome evidence.

Inputs may record one atomic observed outcome event. They cannot self-declare evidence
maturity, profitability, repeatability, strategic gates, or a regenerative loop.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterator, Mapping

from src.composition_outcome_store import CompositionOutcomeEvent, OutcomeEventType


_ALLOWED_FIELDS = {
    "outcome_id",
    "composition_run_id",
    "hypothesis_index",
    "transaction_ref",
    "event_type",
    "observed_at",
    "validation_as_of",
    "validation_snapshot_fingerprint",
    "evidence_ref",
    "evidence_note",
    "subject_ref",
    "amount",
    "currency",
    "details",
}

_FORBIDDEN_DERIVED_FIELDS = {
    "evidence_maturity",
    "transaction_success",
    "transaction_ready",
    "profitable",
    "repeatable",
    "scale_ready",
    "regenerative_loop",
    "G0",
    "G1",
    "G2",
    "G3",
    "G4",
    "G5",
    "G6",
    "L3",
    "L4",
    "L5",
    "L6",
    "L7",
}


def _required_text(record: Mapping[str, object], key: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"missing:{key}")
    return value.strip()


def _optional_text(record: Mapping[str, object], key: str) -> str:
    value = record.get(key, "")
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError(f"invalid:{key}")
    return value.strip()


def _optional_scalar_text(record: Mapping[str, object], key: str) -> str | None:
    value = record.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError(f"invalid:{key}")
    text = str(value).strip()
    return text or None


def _required_int(record: Mapping[str, object], key: str) -> int:
    value = record.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"invalid:{key}")
    return value


def _time(record: Mapping[str, object], key: str) -> datetime:
    raw = _required_text(record, key)
    try:
        value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"invalid:{key}") from exc
    if value.tzinfo is None:
        raise ValueError(f"{key}_must_be_timezone_aware")
    return value


def _details(record: Mapping[str, object]) -> Mapping[str, object]:
    value = record.get("details", {})
    if not isinstance(value, Mapping):
        raise ValueError("details must be an object")
    return dict(value)


def outcome_event_from_record(record: Mapping[str, object]) -> CompositionOutcomeEvent:
    keys = set(record)
    forbidden = sorted(keys & _FORBIDDEN_DERIVED_FIELDS)
    if forbidden:
        raise ValueError("derived outcome fields are not accepted: " + ",".join(forbidden))
    unknown = sorted(keys - _ALLOWED_FIELDS)
    if unknown:
        raise ValueError("unknown outcome fields: " + ",".join(unknown))

    try:
        event_type = OutcomeEventType(_required_text(record, "event_type"))
    except ValueError as exc:
        raise ValueError("invalid:event_type") from exc

    event = CompositionOutcomeEvent(
        outcome_id=_required_text(record, "outcome_id"),
        composition_run_id=_required_int(record, "composition_run_id"),
        hypothesis_index=_required_int(record, "hypothesis_index"),
        transaction_ref=_required_text(record, "transaction_ref"),
        event_type=event_type,
        observed_at=_time(record, "observed_at"),
        validation_as_of=_time(record, "validation_as_of"),
        validation_snapshot_fingerprint=_required_text(
            record, "validation_snapshot_fingerprint"
        ),
        evidence_ref=_required_text(record, "evidence_ref"),
        evidence_note=_required_text(record, "evidence_note"),
        subject_ref=_optional_text(record, "subject_ref"),
        amount=_optional_scalar_text(record, "amount"),
        currency=_optional_text(record, "currency") or None,
        details=_details(record),
    )
    errors = event.validate()
    if errors:
        raise ValueError("invalid composition outcome: " + ",".join(errors))
    return event


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


def outcome_events_from_path(
    path: str | Path, *, format: str = "auto"
) -> Iterator[CompositionOutcomeEvent]:
    for record in records_from_path(path, format=format):
        yield outcome_event_from_record(record)


GOVERNING_INVARIANTS = (
    "OUTCOME_INTAKE_ACCEPTS_ATOMIC_OBSERVATIONS_ONLY",
    "OUTCOME_INTAKE_REQUIRES_EXACT_VALIDATION_SNAPSHOT_LINEAGE",
    "DERIVED_MATURITY_AND_GATE_FIELDS_ARE_REJECTED",
    "ONE_OUTCOME_EVENT_NE_TRANSACTION_SUCCESS",
    "SETTLEMENT_NE_PROFITABILITY",
    "ONE_SUCCESS_NE_REPEATABILITY",
    "L7_IS_NOT_INPUT_TRUTH",
)
