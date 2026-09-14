from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from src.semantic_kernel import SEMANTIC_PRIMITIVES


LIFECYCLE_STATES = frozenset(
    {"DISCOVERED", "QUALIFIED", "ACTIVE", "DEGRADED", "RETIRED"}
)

COLLECTION_MODES = frozenset(
    {
        "UNKNOWN",
        "PUBLIC_MANUAL",
        "PUBLIC_ALLOWED_AUTOMATION",
        "AUTHORIZED_API",
        "AUTHORIZED_EXPORT",
    }
)


@dataclass(frozen=True)
class SensorCandidate:
    source_id: str
    name: str
    base_url: str
    origin_geography: str
    relevance_geographies: tuple[str, ...]
    observable_dimensions: tuple[str, ...]
    collection_mode: str
    provenance_refs: tuple[str, ...]
    china_relevance_evidence_refs: tuple[str, ...] = ()
    activation_evidence_refs: tuple[str, ...] = ()
    unique_signal_value: str = "UNKNOWN"
    lifecycle_state: str = "DISCOVERED"

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        parsed = urlparse(self.base_url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("base_url must be an https URL")
        if not self.origin_geography.strip():
            raise ValueError("origin_geography is required")
        if not self.relevance_geographies:
            raise ValueError("relevance_geographies are required")
        if not self.observable_dimensions:
            raise ValueError("observable_dimensions are required")
        unknown_dimensions = set(self.observable_dimensions) - SEMANTIC_PRIMITIVES
        if unknown_dimensions:
            raise ValueError(
                f"observable_dimensions must use semantic primitives: {sorted(unknown_dimensions)}"
            )
        if self.collection_mode not in COLLECTION_MODES:
            raise ValueError(f"unsupported collection_mode: {self.collection_mode}")
        if self.lifecycle_state not in LIFECYCLE_STATES:
            raise ValueError(f"unsupported lifecycle_state: {self.lifecycle_state}")
        if not self.provenance_refs:
            raise ValueError("provenance_refs are required")


def _tuple_field(record: dict, name: str) -> tuple[str, ...]:
    raw = record.get(name, [])
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise ValueError(f"{name} must be a list of strings")
    return tuple(item.strip() for item in raw if item.strip())


def sensor_candidate_from_dict(record: dict) -> SensorCandidate:
    allowed = {
        "source_id",
        "name",
        "base_url",
        "origin_geography",
        "relevance_geographies",
        "observable_dimensions",
        "collection_mode",
        "provenance_refs",
        "china_relevance_evidence_refs",
        "activation_evidence_refs",
        "unique_signal_value",
        "lifecycle_state",
    }
    unknown = set(record) - allowed
    if unknown:
        raise ValueError(f"unknown sensor candidate fields: {sorted(unknown)}")

    required = {
        "source_id",
        "name",
        "base_url",
        "origin_geography",
        "relevance_geographies",
        "observable_dimensions",
        "collection_mode",
        "provenance_refs",
    }
    missing = required - set(record)
    if missing:
        raise ValueError(f"missing sensor candidate fields: {sorted(missing)}")

    return SensorCandidate(
        source_id=str(record["source_id"]),
        name=str(record["name"]),
        base_url=str(record["base_url"]),
        origin_geography=str(record["origin_geography"]),
        relevance_geographies=_tuple_field(record, "relevance_geographies"),
        observable_dimensions=_tuple_field(record, "observable_dimensions"),
        collection_mode=str(record["collection_mode"]),
        provenance_refs=_tuple_field(record, "provenance_refs"),
        china_relevance_evidence_refs=_tuple_field(
            record, "china_relevance_evidence_refs"
        ),
        activation_evidence_refs=_tuple_field(record, "activation_evidence_refs"),
        unique_signal_value=str(record.get("unique_signal_value", "UNKNOWN")),
        lifecycle_state=str(record.get("lifecycle_state", "DISCOVERED")),
    )


def load_sensor_candidates(path: str | Path) -> tuple[SensorCandidate, ...]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("sensor candidate file must contain a JSON array")

    result: list[SensorCandidate] = []
    seen: set[str] = set()
    for raw in payload:
        if not isinstance(raw, dict):
            raise ValueError("each sensor candidate must be an object")
        candidate = sensor_candidate_from_dict(raw)
        if candidate.source_id in seen:
            raise ValueError(f"duplicate source_id: {candidate.source_id}")
        seen.add(candidate.source_id)
        result.append(candidate)
    return tuple(result)


def is_china_relevant(candidate: SensorCandidate) -> bool:
    domestic = any(
        geo == "CN" or geo.startswith("CN-")
        for geo in candidate.relevance_geographies
    )
    if candidate.origin_geography == "CN" or candidate.origin_geography.startswith("CN-"):
        return domestic
    return domestic and bool(candidate.china_relevance_evidence_refs)


def assess_sensor_candidate(candidate: SensorCandidate) -> dict:
    """Assess lifecycle readiness without silently activating data collection.

    The registry is intentionally source-agnostic. A source can be discovered and
    useful without being automatable. Foreign/global sources need explicit China
    relevance before they enter the China-primary research lane.
    """

    blockers: list[str] = []
    china_relevant = is_china_relevant(candidate)
    if not china_relevant:
        blockers.append("CHINA_RELEVANCE_NOT_EVIDENCED")
    if candidate.unique_signal_value.strip().upper() in {"", "UNKNOWN"}:
        blockers.append("UNIQUE_SIGNAL_VALUE_UNASSESSED")

    qualified = not blockers
    activation_blockers: list[str] = []
    if candidate.collection_mode == "UNKNOWN":
        activation_blockers.append("COLLECTION_MODE_UNRESOLVED")
    if candidate.collection_mode in {
        "PUBLIC_ALLOWED_AUTOMATION",
        "AUTHORIZED_API",
        "AUTHORIZED_EXPORT",
    } and not candidate.activation_evidence_refs:
        activation_blockers.append("ACTIVATION_PERMISSION_EVIDENCE_MISSING")
    if candidate.collection_mode == "PUBLIC_MANUAL":
        activation_blockers.append("MANUAL_ONLY_NOT_AUTOMATED")
    if not qualified:
        activation_blockers.append("SOURCE_NOT_QUALIFIED")

    automation_ready = qualified and not activation_blockers

    if candidate.lifecycle_state == "ACTIVE" and not automation_ready:
        effective_state = "DEGRADED"
    elif candidate.lifecycle_state == "RETIRED":
        effective_state = "RETIRED"
    elif automation_ready:
        effective_state = "ACTIVE_READY"
    elif qualified:
        effective_state = "QUALIFIED"
    else:
        effective_state = "DISCOVERED"

    return {
        "source_id": candidate.source_id,
        "china_relevant": china_relevant,
        "qualified": qualified,
        "automation_ready": automation_ready,
        "effective_state": effective_state,
        "qualification_blockers": blockers,
        "activation_blockers": activation_blockers,
        "observable_dimensions": list(candidate.observable_dimensions),
        "truth_boundaries": [
            "SOURCE_DISCOVERY_IS_NOT_SOURCE_ACTIVATION",
            "PLATFORM_IS_NOT_ONTOLOGY",
            "GLOBAL_SOURCE_IS_NOT_DOMESTIC_EVIDENCE",
            "ACCESSIBILITY_IS_NOT_PERMISSION_TO_AUTOMATE",
        ],
    }
