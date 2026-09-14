from __future__ import annotations

from dataclasses import dataclass
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
