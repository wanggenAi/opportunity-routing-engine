"""Reviewed JSON/JSONL intake for explicit capability verification evidence.

This is intentionally separate from public/manual signal intake. Records may confirm or
reject a capability only when they carry explicit verification identity, time, evidence
reference and evidence note. Transaction/payer/consent truth remains out of scope.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterator, Mapping

from src.capability_verification_store import (
    CapabilityVerificationEvent,
    VerificationVerdict,
)
from src.live_resource_signals import AvailabilityState, PermissionState


_ALLOWED_FIELDS = {
    "verification_id",
    "actor_ref",
    "capability_key",
    "verdict",
    "verified_at",
    "evidence_ref",
    "evidence_note",
    "geography",
    "availability",
    "permission",
    "related_signal_refs",
}

_FORBIDDEN_TRUTH_FIELDS = {
    "counterparty_consented",
    "payer_confirmed",
    "payer_committed",
    "transaction_ready",
    "transactionable",
    "access_approved",
    "safety_approved",
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


def _time(record: Mapping[str, object]) -> datetime:
    raw = _required_text(record, "verified_at")
    try:
        value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid:verified_at") from exc
    if value.tzinfo is None:
        raise ValueError("verified_at_must_be_timezone_aware")
    return value


def verification_event_from_record(
    record: Mapping[str, object],
) -> CapabilityVerificationEvent:
    keys = set(record)
    forbidden = sorted(keys & _FORBIDDEN_TRUTH_FIELDS)
    if forbidden:
        raise ValueError("transaction truth fields are not accepted: " + ",".join(forbidden))
    unknown = sorted(keys - _ALLOWED_FIELDS)
    if unknown:
        raise ValueError("unknown verification fields: " + ",".join(unknown))

    try:
        verdict = VerificationVerdict(_required_text(record, "verdict"))
    except ValueError as exc:
        raise ValueError("invalid:verdict") from exc
    try:
        availability = AvailabilityState(str(record.get("availability", "UNKNOWN")))
    except ValueError as exc:
        raise ValueError("invalid:availability") from exc
    try:
        permission = PermissionState(str(record.get("permission", "UNKNOWN")))
    except ValueError as exc:
        raise ValueError("invalid:permission") from exc

    raw_refs = record.get("related_signal_refs", [])
    if not isinstance(raw_refs, list) or any(not isinstance(ref, str) for ref in raw_refs):
        raise ValueError("related_signal_refs must be an array of strings")

    event = CapabilityVerificationEvent(
        verification_id=_required_text(record, "verification_id"),
        actor_ref=_required_text(record, "actor_ref"),
        capability_key=_required_text(record, "capability_key"),
        verdict=verdict,
        verified_at=_time(record),
        evidence_ref=_required_text(record, "evidence_ref"),
        evidence_note=_required_text(record, "evidence_note"),
        geography=_optional_text(record, "geography"),
        availability=availability,
        permission=permission,
        related_signal_refs=tuple(ref.strip() for ref in raw_refs),
    )
    errors = event.validate()
    if errors:
        raise ValueError("invalid capability verification: " + ",".join(errors))
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


def verification_events_from_path(
    path: str | Path, *, format: str = "auto"
) -> Iterator[CapabilityVerificationEvent]:
    for record in records_from_path(path, format=format):
        yield verification_event_from_record(record)


GOVERNING_INVARIANTS = (
    "VERIFICATION_INTAKE_IS_SEPARATE_FROM_PUBLIC_SIGNAL_INTAKE",
    "VERIFICATION_REQUIRES_EVIDENCE_REF_AND_NOTE",
    "VERIFICATION_REQUIRES_TIMEZONE_AWARE_TIME",
    "VERIFICATION_NE_COUNTERPARTY_CONSENT",
    "VERIFICATION_NE_PAYER_COMMITMENT",
    "VERIFICATION_NE_TRANSACTION_READINESS",
    "TRANSACTION_TRUTH_FIELDS_ARE_REJECTED",
    "UNKNOWN_NE_PASS",
)
