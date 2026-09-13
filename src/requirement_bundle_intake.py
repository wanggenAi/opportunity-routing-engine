"""Reviewed JSON/JSONL intake for versioned requirement-bundle decompositions.

This boundary accepts only decomposition metadata. It cannot manufacture demand truth,
payer commitment, counterparty consent, or transaction readiness.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator, Mapping

from src.requirement_bundle_registry import RequirementBundleSpec


_ALLOWED_FIELDS = {
    "bundle_id",
    "version",
    "required_capabilities",
    "geography",
    "source_ref",
    "rationale",
    "active",
}

_FORBIDDEN_TRUTH_FIELDS = {
    "demand_confirmed",
    "counterparty_confirmed",
    "payer_confirmed",
    "payer_committed",
    "transaction_ready",
    "transactionable",
    "consent_confirmed",
    "access_confirmed",
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


def requirement_spec_from_record(record: Mapping[str, object]) -> RequirementBundleSpec:
    """Parse one reviewed decomposition record without promoting external truth."""

    keys = set(record)
    forbidden = sorted(keys & _FORBIDDEN_TRUTH_FIELDS)
    if forbidden:
        raise ValueError("truth promotion fields are not accepted: " + ",".join(forbidden))
    unknown = sorted(keys - _ALLOWED_FIELDS)
    if unknown:
        raise ValueError("unknown requirement fields: " + ",".join(unknown))

    version = record.get("version")
    if isinstance(version, bool) or not isinstance(version, int):
        raise ValueError("version must be an integer")

    capabilities = record.get("required_capabilities")
    if not isinstance(capabilities, list):
        raise ValueError("required_capabilities must be an array")
    if any(not isinstance(key, str) for key in capabilities):
        raise ValueError("required_capabilities items must be strings")

    active = record.get("active", False)
    if not isinstance(active, bool):
        raise ValueError("active must be a boolean")

    spec = RequirementBundleSpec(
        bundle_id=_required_text(record, "bundle_id"),
        version=version,
        required_capabilities=tuple(key.strip() for key in capabilities),
        geography=_optional_text(record, "geography"),
        source_ref=_required_text(record, "source_ref"),
        rationale=_required_text(record, "rationale"),
        active=active,
    )
    errors = spec.validate()
    if errors:
        raise ValueError("invalid requirement bundle spec: " + ",".join(errors))
    return spec


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


def requirement_specs_from_path(
    path: str | Path, *, format: str = "auto"
) -> Iterator[RequirementBundleSpec]:
    for record in records_from_path(path, format=format):
        yield requirement_spec_from_record(record)


GOVERNING_INVARIANTS = (
    "REVIEWED_INTAKE_NE_DEMAND_CONFIRMATION",
    "REVIEWED_INTAKE_NE_PAYER_COMMITMENT",
    "REVIEWED_INTAKE_NE_TRANSACTION_READINESS",
    "INPUT_SCHEMA_IS_EXPLICIT_ALLOWLIST",
    "TRUTH_PROMOTION_FIELDS_ARE_REJECTED",
    "SOURCE_REF_AND_RATIONALE_ARE_REQUIRED",
    "UNKNOWN_NE_PASS",
)
