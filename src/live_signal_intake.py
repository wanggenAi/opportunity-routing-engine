"""Source-neutral JSON/JSONL intake for live resource observations.

This is deliberately not a platform scraper. It provides a stable ingestion boundary
so public/manual observations and future source adapters enter the same canonical
SignalObservation contract.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterable, Iterator, Mapping

from src.live_resource_signals import (
    AvailabilityState,
    ExplicitCapability,
    ObservedFact,
    PermissionState,
    SignalObservation,
)


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


def _observed_at(record: Mapping[str, object]) -> datetime:
    raw = _required_text(record, "observed_at")
    try:
        value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid:observed_at") from exc
    if value.tzinfo is None:
        raise ValueError("observed_at_must_be_timezone_aware")
    return value


def _facts(record: Mapping[str, object]) -> tuple[ObservedFact, ...]:
    raw = record.get("facts", [])
    if not isinstance(raw, list):
        raise ValueError("invalid:facts")
    result: list[ObservedFact] = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError(f"invalid:facts[{index}]")
        key = _required_text(item, "key")
        evidence_text = _required_text(item, "evidence_text")
        if "value" not in item:
            raise ValueError(f"missing:facts[{index}].value")
        result.append(ObservedFact(key, item["value"], evidence_text))
    return tuple(result)


def _capabilities(record: Mapping[str, object]) -> tuple[ExplicitCapability, ...]:
    raw = record.get("explicit_capabilities", [])
    if not isinstance(raw, list):
        raise ValueError("invalid:explicit_capabilities")
    result: list[ExplicitCapability] = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError(f"invalid:explicit_capabilities[{index}]")
        result.append(
            ExplicitCapability(
                _required_text(item, "capability_key"),
                _required_text(item, "evidence_text"),
            )
        )
    return tuple(result)


def signal_from_record(record: Mapping[str, object]) -> SignalObservation:
    """Parse one neutral observation record without semantic invention."""

    try:
        availability = AvailabilityState(str(record.get("availability", "UNKNOWN")))
    except ValueError as exc:
        raise ValueError("invalid:availability") from exc
    try:
        permission = PermissionState(str(record.get("permission", "UNKNOWN")))
    except ValueError as exc:
        raise ValueError("invalid:permission") from exc

    signal = SignalObservation(
        signal_id=_required_text(record, "signal_id"),
        source_id=_required_text(record, "source_id"),
        observed_at=_observed_at(record),
        actor_ref=_required_text(record, "actor_ref"),
        geography=_optional_text(record, "geography"),
        raw_text=_optional_text(record, "raw_text"),
        source_url=_optional_text(record, "source_url"),
        facts=_facts(record),
        explicit_capabilities=_capabilities(record),
        availability=availability,
        permission=permission,
    )
    errors = signal.validate()
    if errors:
        raise ValueError("invalid signal: " + ",".join(errors))
    return signal


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
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid jsonl line {line_number}") from exc
            if not isinstance(record, Mapping):
                raise ValueError(f"jsonl line {line_number} must be an object")
            yield record
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
            for index, record in enumerate(payload):
                if not isinstance(record, Mapping):
                    raise ValueError(f"json item {index} must be an object")
                yield record
            return
        raise ValueError("json input must be an object or array of objects")

    raise ValueError("format must be auto, json or jsonl")


def signals_from_path(path: str | Path, *, format: str = "auto") -> Iterator[SignalObservation]:
    for record in records_from_path(path, format=format):
        yield signal_from_record(record)


GOVERNING_INVARIANTS = (
    "NEUTRAL_INTAKE_NE_PLATFORM_STRATEGY",
    "INPUT_RECORD_NE_CONFIRMED_TRUTH",
    "NO_SEMANTIC_INVENTION_DURING_PARSE",
    "SOURCE_SUPPORTED_AVAILABILITY_PERMISSION_ONLY",
    "UNKNOWN_NE_PASS",
)
