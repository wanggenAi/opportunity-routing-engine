"""Convert reviewed JSON records into neutral SignalObservation objects."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Mapping, Sequence

from src.live_resource_signals import (
    AvailabilityState,
    ExplicitCapability,
    ObservedFact,
    PermissionState,
    SignalObservation,
)


def _text(record: Mapping[str, object], key: str, *, required: bool = True) -> str:
    value = record.get(key, "")
    if value is None and not required:
        return ""
    if not isinstance(value, str) or (required and not value.strip()):
        raise ValueError(f"{key} must be a string")
    return value.strip()


def _time(record: Mapping[str, object]) -> datetime:
    raw = _text(record, "observed_at")
    try:
        value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("observed_at must be ISO-8601") from exc
    if value.tzinfo is None:
        raise ValueError("observed_at must be timezone-aware")
    return value


def _facts(record: Mapping[str, object]) -> tuple[ObservedFact, ...]:
    raw = record.get("facts", [])
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError("facts must be an array")
    result: list[ObservedFact] = []
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError("fact must be an object")
        key = item.get("key")
        evidence = item.get("evidence_text")
        if not isinstance(key, str) or not key.strip():
            raise ValueError("fact key is required")
        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError("fact evidence_text is required")
        result.append(ObservedFact(key.strip(), item.get("value"), evidence.strip()))
    return tuple(result)


def _capabilities(record: Mapping[str, object]) -> tuple[ExplicitCapability, ...]:
    raw = record.get("explicit_capabilities", [])
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError("explicit_capabilities must be an array")
    result: list[ExplicitCapability] = []
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError("explicit capability must be an object")
        key = item.get("capability_key")
        evidence = item.get("evidence_text")
        if not isinstance(key, str) or not key.strip():
            raise ValueError("capability_key is required")
        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError("capability evidence_text is required")
        result.append(ExplicitCapability(key.strip(), evidence.strip()))
    return tuple(result)


def signal_from_record(record: Mapping[str, object]) -> SignalObservation:
    availability = AvailabilityState(str(record.get("availability", "UNKNOWN")))
    if availability not in {AvailabilityState.UNKNOWN, AvailabilityState.ADVERTISED}:
        raise ValueError("structured import cannot create confirmed availability")

    permission = PermissionState(str(record.get("permission", "UNKNOWN")))
    if permission is not PermissionState.UNKNOWN:
        raise ValueError("structured import cannot create permission state")

    signal = SignalObservation(
        signal_id=_text(record, "signal_id"),
        source_id=_text(record, "source_id"),
        observed_at=_time(record),
        actor_ref=_text(record, "actor_ref"),
        geography=_text(record, "geography", required=False),
        raw_text=_text(record, "raw_text", required=False),
        source_url=_text(record, "source_url", required=False),
        facts=_facts(record),
        explicit_capabilities=_capabilities(record),
        availability=availability,
        permission=permission,
    )
    errors = signal.validate()
    if errors:
        raise ValueError("invalid signal: " + ",".join(errors))
    return signal


def load_records(path: str | Path) -> tuple[Mapping[str, object], ...]:
    source = Path(path)
    text = source.read_text(encoding="utf-8")
    if source.suffix.lower() == ".jsonl":
        result: list[Mapping[str, object]] = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL line {line_number}") from exc
            if not isinstance(item, Mapping):
                raise ValueError(f"JSONL line {line_number} must be an object")
            result.append(item)
        return tuple(result)

    payload = json.loads(text)
    if not isinstance(payload, list) or any(not isinstance(item, Mapping) for item in payload):
        raise ValueError("JSON input must be an array of objects")
    return tuple(payload)


GOVERNING_INVARIANTS = (
    "STRUCTURED_IMPORT_NE_CONFIRMATION",
    "STRUCTURED_IMPORT_NE_COMMITMENT",
    "EXPLICIT_CLAIM_REQUIRES_EVIDENCE_TEXT",
    "UNKNOWN_NE_PASS",
)
