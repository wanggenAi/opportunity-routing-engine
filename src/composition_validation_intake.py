"""Reviewed JSON/JSONL intake for composition validation evidence.

Validation evidence is bound to an exact composition run and hypothesis. Generic
events may update only one explicit validation dimension. Operator access is special:
it must carry a canonical AccessFeasibility record and is classified by access_state();
the intake never accepts a hand-written access PASS.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterator, Mapping

from src.access_feasibility import (
    AccessEvidence,
    AccessFeasibility,
    AccessRouteKind,
)
from src.composition_validation_store import (
    CompositionValidationEvent,
    ValidationDimension,
    ValidationGateState,
    access_validation_event,
)


_ALLOWED_FIELDS = {
    "validation_id",
    "composition_run_id",
    "hypothesis_index",
    "dimension",
    "value",
    "observed_at",
    "evidence_ref",
    "evidence_note",
    "subject_ref",
    "details",
    "access_record",
}

_FORBIDDEN_DERIVED_FIELDS = {
    "transaction_ready",
    "bounded_transaction_ready",
    "scale_ready",
    "gate_overrides",
    "G0",
    "G1",
    "G2",
    "G3",
    "G4",
    "G5",
    "G6",
}

_ACCESS_RECORD_FIELDS = {
    "candidate_id",
    "target_actor",
    "route_kind",
    "legitimate_entry_path",
    "backing_leverage",
    "counterparty_reason_to_engage",
    "counterparty_visible_surplus",
    "surplus_realization_mechanism",
    "institutional_cover_or_referral",
    "status_trust_friction",
    "operator_credibility_assets",
    "missing_credibility",
    "operator_commitment",
    "counterparty_commitment_requested",
    "founder_identity_dependency",
    "first_value_packet",
    "counterparty_downside",
    "cultural_context_notes",
    "evidence",
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


def _required_int(record: Mapping[str, object], key: str) -> int:
    value = record.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"invalid:{key}")
    return value


def _time(record: Mapping[str, object]) -> datetime:
    raw = _required_text(record, "observed_at")
    try:
        value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid:observed_at") from exc
    if value.tzinfo is None:
        raise ValueError("observed_at_must_be_timezone_aware")
    return value


def _details(record: Mapping[str, object]) -> Mapping[str, object]:
    value = record.get("details", {})
    if not isinstance(value, Mapping):
        raise ValueError("details must be an object")
    return dict(value)


def _access_record(raw: object) -> AccessFeasibility:
    if not isinstance(raw, Mapping):
        raise ValueError("access_record must be an object")
    unknown = sorted(set(raw) - _ACCESS_RECORD_FIELDS)
    if unknown:
        raise ValueError("unknown access_record fields: " + ",".join(unknown))
    try:
        route_kind = AccessRouteKind(_required_text(raw, "route_kind"))
    except ValueError as exc:
        raise ValueError("invalid:access_record.route_kind") from exc

    evidence_raw = raw.get("evidence")
    if not isinstance(evidence_raw, list):
        raise ValueError("access_record.evidence must be an array")
    evidence: list[AccessEvidence] = []
    for index, item in enumerate(evidence_raw):
        if not isinstance(item, Mapping):
            raise ValueError(f"access_record.evidence[{index}] must be an object")
        if set(item) != {"source_id", "claim"}:
            raise ValueError(f"invalid:access_record.evidence[{index}]")
        evidence.append(
            AccessEvidence(
                _required_text(item, "source_id"),
                _required_text(item, "claim"),
            )
        )

    return AccessFeasibility(
        candidate_id=_required_text(raw, "candidate_id"),
        target_actor=_required_text(raw, "target_actor"),
        route_kind=route_kind,
        legitimate_entry_path=_required_text(raw, "legitimate_entry_path"),
        backing_leverage=_required_text(raw, "backing_leverage"),
        counterparty_reason_to_engage=_required_text(raw, "counterparty_reason_to_engage"),
        counterparty_visible_surplus=_required_text(raw, "counterparty_visible_surplus"),
        surplus_realization_mechanism=_required_text(raw, "surplus_realization_mechanism"),
        institutional_cover_or_referral=_optional_text(raw, "institutional_cover_or_referral"),
        status_trust_friction=_required_text(raw, "status_trust_friction"),
        operator_credibility_assets=_optional_text(raw, "operator_credibility_assets"),
        missing_credibility=_optional_text(raw, "missing_credibility"),
        operator_commitment=_required_text(raw, "operator_commitment"),
        counterparty_commitment_requested=_required_text(raw, "counterparty_commitment_requested"),
        founder_identity_dependency=_required_text(raw, "founder_identity_dependency"),
        first_value_packet=_optional_text(raw, "first_value_packet"),
        counterparty_downside=_optional_text(raw, "counterparty_downside"),
        cultural_context_notes=_optional_text(raw, "cultural_context_notes"),
        evidence=tuple(evidence),
    )


def validation_event_from_record(record: Mapping[str, object]) -> CompositionValidationEvent:
    keys = set(record)
    forbidden = sorted(keys & _FORBIDDEN_DERIVED_FIELDS)
    if forbidden:
        raise ValueError("derived gate fields are not accepted: " + ",".join(forbidden))
    unknown = sorted(keys - _ALLOWED_FIELDS)
    if unknown:
        raise ValueError("unknown validation fields: " + ",".join(unknown))

    try:
        dimension = ValidationDimension(_required_text(record, "dimension"))
    except ValueError as exc:
        raise ValueError("invalid:dimension") from exc

    common = {
        "validation_id": _required_text(record, "validation_id"),
        "composition_run_id": _required_int(record, "composition_run_id"),
        "hypothesis_index": _required_int(record, "hypothesis_index"),
        "observed_at": _time(record),
        "evidence_ref": _required_text(record, "evidence_ref"),
        "evidence_note": _required_text(record, "evidence_note"),
    }

    if dimension is ValidationDimension.OPERATOR_ACCESS:
        if "value" in record:
            raise ValueError("operator access value cannot be supplied directly")
        if "details" in record or "subject_ref" in record:
            raise ValueError("operator access details/subject are derived from access_record")
        event = access_validation_event(
            record=_access_record(record.get("access_record")),
            **common,
        )
    else:
        if "access_record" in record:
            raise ValueError("access_record is only valid for OPERATOR_ACCESS")
        try:
            value = ValidationGateState(_required_text(record, "value"))
        except ValueError as exc:
            raise ValueError("invalid:value") from exc
        event = CompositionValidationEvent(
            dimension=dimension,
            value=value.value,
            subject_ref=_optional_text(record, "subject_ref"),
            details=_details(record),
            **common,
        )

    errors = event.validate()
    if errors:
        raise ValueError("invalid composition validation: " + ",".join(errors))
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


def validation_events_from_path(
    path: str | Path, *, format: str = "auto"
) -> Iterator[CompositionValidationEvent]:
    for record in records_from_path(path, format=format):
        yield validation_event_from_record(record)


GOVERNING_INVARIANTS = (
    "VALIDATION_INTAKE_BINDS_EXACT_COMPOSITION_HYPOTHESIS",
    "OPERATOR_ACCESS_MUST_USE_CANONICAL_ACCESS_MODEL",
    "DERIVED_GATE_FIELDS_ARE_REJECTED",
    "ONE_RECORD_UPDATES_ONE_VALIDATION_DIMENSION",
    "PAYER_CLARITY_NE_PAYER_COMMITMENT",
    "UNKNOWN_NE_PASS",
)
