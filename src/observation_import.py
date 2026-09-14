"""Strict reviewed JSON/JSONL import into the source-neutral Observation Fabric."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping, Sequence

from src.observation_fabric import EvidenceRef, ObservationEnvelope, SemanticClaim


_ENVELOPE_FIELDS = {
    "observation_id",
    "source_id",
    "source_record_id",
    "source_locator",
    "source_origin_geography",
    "relevance_geographies",
    "source_tier",
    "observed_at",
    "retrieved_at",
    "parser_version",
    "raw_payload_hash",
    "sampling_boundary",
    "evidence",
    "claims",
    "published_at",
    "actor_ids",
    "unknown_fields",
    "contradiction_refs",
    "supersedes_observation_id",
    "schema_version",
}


def _string(record: Mapping[str, object], key: str, *, required: bool = True) -> str:
    value = record.get(key)
    if value is None and not required:
        return ""
    if not isinstance(value, str) or (required and not value.strip()):
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()


def _strings(record: Mapping[str, object], key: str) -> tuple[str, ...]:
    raw = record.get(key, [])
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError(f"{key} must be an array of strings")
    if not all(isinstance(item, str) and item.strip() for item in raw):
        raise ValueError(f"{key} must contain non-empty strings")
    return tuple(str(item).strip() for item in raw)


def _evidence(record: Mapping[str, object]) -> tuple[EvidenceRef, ...]:
    raw = record.get("evidence")
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError("evidence must be an array")
    result: list[EvidenceRef] = []
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError("evidence item must be an object")
        allowed = {"ref_id", "locator", "excerpt", "content_hash"}
        unknown = set(item) - allowed
        if unknown:
            raise ValueError(f"unknown evidence fields: {sorted(unknown)}")
        result.append(
            EvidenceRef(
                ref_id=_string(item, "ref_id"),
                locator=_string(item, "locator"),
                excerpt=_string(item, "excerpt", required=False),
                content_hash=_string(item, "content_hash", required=False),
            )
        )
    return tuple(result)


def _claims(record: Mapping[str, object]) -> tuple[SemanticClaim, ...]:
    raw = record.get("claims")
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError("claims must be an array")
    result: list[SemanticClaim] = []
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError("claim item must be an object")
        allowed = {
            "claim_id",
            "primitive",
            "concept",
            "epistemic_status",
            "evidence_refs",
            "value",
            "actor_id",
            "geography",
            "inference_depth",
            "contradiction_refs",
        }
        unknown = set(item) - allowed
        if unknown:
            raise ValueError(f"unknown claim fields: {sorted(unknown)}")
        actor = item.get("actor_id")
        geography = item.get("geography")
        if actor is not None and not isinstance(actor, str):
            raise ValueError("actor_id must be a string or null")
        if geography is not None and not isinstance(geography, str):
            raise ValueError("geography must be a string or null")
        depth = item.get("inference_depth", 0)
        if not isinstance(depth, int) or isinstance(depth, bool):
            raise ValueError("inference_depth must be an integer")
        result.append(
            SemanticClaim(
                claim_id=_string(item, "claim_id"),
                primitive=_string(item, "primitive"),
                concept=_string(item, "concept"),
                epistemic_status=_string(item, "epistemic_status"),
                evidence_refs=_strings(item, "evidence_refs"),
                value=item.get("value"),
                actor_id=(actor.strip() if isinstance(actor, str) and actor.strip() else None),
                geography=(
                    geography.strip()
                    if isinstance(geography, str) and geography.strip()
                    else None
                ),
                inference_depth=depth,
                contradiction_refs=_strings(item, "contradiction_refs"),
            )
        )
    return tuple(result)


def envelope_from_record(record: Mapping[str, object]) -> ObservationEnvelope:
    unknown = set(record) - _ENVELOPE_FIELDS
    if unknown:
        raise ValueError(f"unknown observation fields: {sorted(unknown)}")

    required = {
        "observation_id",
        "source_id",
        "source_record_id",
        "source_locator",
        "source_origin_geography",
        "relevance_geographies",
        "source_tier",
        "observed_at",
        "retrieved_at",
        "parser_version",
        "raw_payload_hash",
        "sampling_boundary",
        "evidence",
        "claims",
    }
    missing = required - set(record)
    if missing:
        raise ValueError(f"missing observation fields: {sorted(missing)}")

    published = record.get("published_at")
    supersedes = record.get("supersedes_observation_id")
    if published is not None and not isinstance(published, str):
        raise ValueError("published_at must be a string or null")
    if supersedes is not None and not isinstance(supersedes, str):
        raise ValueError("supersedes_observation_id must be a string or null")

    return ObservationEnvelope(
        observation_id=_string(record, "observation_id"),
        source_id=_string(record, "source_id"),
        source_record_id=_string(record, "source_record_id"),
        source_locator=_string(record, "source_locator"),
        source_origin_geography=_string(record, "source_origin_geography"),
        relevance_geographies=_strings(record, "relevance_geographies"),
        source_tier=_string(record, "source_tier"),
        observed_at=_string(record, "observed_at"),
        retrieved_at=_string(record, "retrieved_at"),
        parser_version=_string(record, "parser_version"),
        raw_payload_hash=_string(record, "raw_payload_hash"),
        sampling_boundary=_string(record, "sampling_boundary"),
        evidence=_evidence(record),
        claims=_claims(record),
        published_at=(published.strip() if isinstance(published, str) and published.strip() else None),
        actor_ids=_strings(record, "actor_ids"),
        unknown_fields=_strings(record, "unknown_fields"),
        contradiction_refs=_strings(record, "contradiction_refs"),
        supersedes_observation_id=(
            supersedes.strip()
            if isinstance(supersedes, str) and supersedes.strip()
            else None
        ),
        schema_version=str(record.get("schema_version", "observation-envelope.v1")),
    )


def load_raw_records(path: str | Path) -> tuple[Mapping[str, object], ...]:
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


def load_observations(path: str | Path) -> tuple[ObservationEnvelope, ...]:
    return tuple(envelope_from_record(record) for record in load_raw_records(path))


GOVERNING_INVARIANTS = (
    "REVIEWED_IMPORT_NE_WORLD_TRUTH_PROMOTION",
    "UNKNOWN_CONCEPT_IS_ACCEPTED",
    "UNKNOWN_PRIMITIVE_IS_REJECTED",
    "STRUCTURED_IMPORT_NE_CONFIRMED_AVAILABILITY",
    "STRUCTURED_IMPORT_NE_PERMISSION",
    "UNKNOWN_NE_PASS",
)
