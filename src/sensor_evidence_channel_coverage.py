"""Fail-closed evidence-channel coverage across the sensor portfolio.

This layer answers a different question from source coverage and execution-capability
coverage: which kinds of evidence can the world-observation system actually sense
through governed production observations right now?

Evidence channels are data-governed records, not code enums. Source/platform names
remain concrete collection surfaces. A channel can have registered/manual/candidate
sources without being observed in the production Observation Fabric.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from src.semantic_kernel import SEMANTIC_PRIMITIVES
from src.sensor_portfolio import OperationalSource
from src.sensor_registry import SensorCandidate, assess_sensor_candidate


REGISTRY_SCHEMA_VERSION = "sensor-evidence-channel-registry.v1"
COVERAGE_SCHEMA_VERSION = "sensor-evidence-channel-coverage.v1"
_CHANNEL_ID_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


@dataclass(frozen=True)
class EvidenceChannelDefinition:
    channel_id: str
    description: str
    semantic_dimensions: tuple[str, ...]
    operational_source_ids: tuple[str, ...]
    candidate_source_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not _CHANNEL_ID_RE.fullmatch(self.channel_id):
            raise ValueError(f"invalid evidence channel_id: {self.channel_id!r}")
        if not self.description.strip():
            raise ValueError(f"evidence channel {self.channel_id} description is required")
        if not self.semantic_dimensions:
            raise ValueError(f"evidence channel {self.channel_id} semantic_dimensions are required")
        unknown = set(self.semantic_dimensions) - SEMANTIC_PRIMITIVES
        if unknown:
            raise ValueError(
                f"evidence channel {self.channel_id} has unknown semantic dimensions: {sorted(unknown)}"
            )
        if len(self.semantic_dimensions) != len(set(self.semantic_dimensions)):
            raise ValueError(f"evidence channel {self.channel_id} has duplicate semantic dimensions")
        for field_name, values in (
            ("operational_source_ids", self.operational_source_ids),
            ("candidate_source_ids", self.candidate_source_ids),
        ):
            if any(not isinstance(value, str) or not value.strip() for value in values):
                raise ValueError(f"evidence channel {self.channel_id} has invalid {field_name}")
            if len(values) != len(set(values)):
                raise ValueError(f"evidence channel {self.channel_id} has duplicate {field_name}")
        if not self.operational_source_ids and not self.candidate_source_ids:
            raise ValueError(f"evidence channel {self.channel_id} must bind at least one source")


def _string_tuple(value: object, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{field} must be an array of strings")
    return tuple(item.strip() for item in value)


def load_evidence_channel_registry(path: str | Path) -> tuple[EvidenceChannelDefinition, ...]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("evidence channel registry must contain an object")
    if set(payload) != {"schema_version", "channels"}:
        raise ValueError("unexpected evidence channel registry fields")
    if payload.get("schema_version") != REGISTRY_SCHEMA_VERSION:
        raise ValueError("unsupported evidence channel registry schema")
    rows = payload.get("channels")
    if not isinstance(rows, list) or not rows:
        raise ValueError("evidence channel registry requires channels")

    expected = {
        "channel_id",
        "description",
        "semantic_dimensions",
        "operational_source_ids",
        "candidate_source_ids",
    }
    result: list[EvidenceChannelDefinition] = []
    seen: set[str] = set()
    for index, raw in enumerate(rows):
        if not isinstance(raw, dict) or set(raw) != expected:
            raise ValueError(f"invalid evidence channel record at index {index}")
        channel = EvidenceChannelDefinition(
            channel_id=str(raw["channel_id"]).strip(),
            description=str(raw["description"]).strip(),
            semantic_dimensions=_string_tuple(
                raw["semantic_dimensions"], f"channels[{index}].semantic_dimensions"
            ),
            operational_source_ids=_string_tuple(
                raw["operational_source_ids"], f"channels[{index}].operational_source_ids"
            ),
            candidate_source_ids=_string_tuple(
                raw["candidate_source_ids"], f"channels[{index}].candidate_source_ids"
            ),
        )
        if channel.channel_id in seen:
            raise ValueError(f"duplicate evidence channel_id: {channel.channel_id}")
        seen.add(channel.channel_id)
        result.append(channel)
    return tuple(result)


def _string_set(value: object, field: str) -> set[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{field} must be an array of non-empty strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{field} contains duplicates")
    return set(value)


def _validate_live_observation_coverage(payload: Mapping[str, Any]) -> tuple[set[str], set[str], set[str]]:
    if payload.get("schema_version") != "live-observation-coverage.v1":
        raise ValueError("unsupported live observation coverage schema")

    production = _string_set(
        payload.get("production_live_source_ids"), "production_live_source_ids"
    )
    supported = _string_set(
        payload.get("adapter_supported_production_source_ids"),
        "adapter_supported_production_source_ids",
    )
    observed = _string_set(
        payload.get("observed_production_source_ids"), "observed_production_source_ids"
    )
    if not observed <= supported <= production:
        raise ValueError("live observation coverage source sets are inconsistent")

    count_fields = {
        "production_live_registry_count": len(production),
        "adapter_supported_production_count": len(supported),
        "observed_production_count": len(observed),
    }
    for field, expected in count_fields.items():
        value = payload.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value != expected:
            raise ValueError(f"live observation coverage {field} diverges from source ids")

    supported_not_observed = _string_set(
        payload.get("adapter_supported_not_observed_source_ids"),
        "adapter_supported_not_observed_source_ids",
    )
    no_adapter = _string_set(
        payload.get("no_unified_adapter_source_ids"), "no_unified_adapter_source_ids"
    )
    if supported_not_observed != supported - observed:
        raise ValueError("supported-not-observed source set diverges")
    if no_adapter != production - supported:
        raise ValueError("no-adapter source set diverges")
    return production, supported, observed


def reconcile_sensor_evidence_channel_coverage(
    operational_sources: Iterable[OperationalSource],
    candidates: Iterable[SensorCandidate],
    live_observation_coverage: Mapping[str, Any],
    channels: Iterable[EvidenceChannelDefinition],
) -> dict[str, Any]:
    """Reconcile registered source surfaces with actual observed evidence channels."""

    operational = tuple(operational_sources)
    candidate_rows = tuple(candidates)
    channel_rows = tuple(channels)
    if not channel_rows:
        raise ValueError("at least one evidence channel is required")

    operational_by_id = {item.source_id: item for item in operational}
    candidate_by_id = {item.source_id: item for item in candidate_rows}
    if len(operational_by_id) != len(operational):
        raise ValueError("duplicate operational source ids")
    if len(candidate_by_id) != len(candidate_rows):
        raise ValueError("duplicate candidate source ids")

    production_ids, supported_ids, observed_ids = _validate_live_observation_coverage(
        live_observation_coverage
    )
    registry_production_ids = {
        item.source_id for item in operational if item.is_production_live
    }
    if production_ids != registry_production_ids:
        raise ValueError(
            "live observation coverage production source set diverges from operational registry"
        )

    mapped_operational: set[str] = set()
    mapped_candidates: set[str] = set()
    channel_payloads: list[dict[str, Any]] = []

    for channel in sorted(channel_rows, key=lambda item: item.channel_id):
        unknown_operational = set(channel.operational_source_ids) - set(operational_by_id)
        unknown_candidates = set(channel.candidate_source_ids) - set(candidate_by_id)
        if unknown_operational or unknown_candidates:
            raise ValueError(
                f"evidence channel {channel.channel_id} references unknown sources: "
                f"operational={sorted(unknown_operational)} candidates={sorted(unknown_candidates)}"
            )

        mapped_operational.update(channel.operational_source_ids)
        mapped_candidates.update(channel.candidate_source_ids)

        bound_operational = set(channel.operational_source_ids)
        channel_production = sorted(bound_operational & production_ids)
        channel_supported = sorted(bound_operational & supported_ids)
        channel_observed = sorted(bound_operational & observed_ids)
        channel_manual = sorted(
            source_id
            for source_id in bound_operational
            if operational_by_id[source_id].is_manual_surface
        )
        channel_nonlive = sorted(bound_operational - production_ids)
        channel_candidates = sorted(channel.candidate_source_ids)
        candidate_ready = sorted(
            source_id
            for source_id in channel_candidates
            if assess_sensor_candidate(candidate_by_id[source_id])["automation_ready"]
        )

        if channel_observed:
            state = "OBSERVED_PRODUCTION"
        elif channel_production:
            state = "PRODUCTION_LIVE_NOT_OBSERVED"
        elif bound_operational:
            state = "REGISTERED_NONLIVE_ONLY"
        else:
            state = "CANDIDATE_ONLY"

        channel_payloads.append(
            {
                "channel_id": channel.channel_id,
                "description": channel.description,
                "semantic_dimensions": list(channel.semantic_dimensions),
                "coverage_state": state,
                "blind_spot": not bool(channel_observed),
                "registered_operational_source_ids": sorted(bound_operational),
                "production_live_source_ids": channel_production,
                "adapter_supported_source_ids": channel_supported,
                "observed_production_source_ids": channel_observed,
                "production_live_not_observed_source_ids": sorted(
                    set(channel_production) - set(channel_observed)
                ),
                "registered_nonlive_source_ids": channel_nonlive,
                "manual_surface_source_ids": channel_manual,
                "candidate_source_ids": channel_candidates,
                "candidate_automation_ready_source_ids": candidate_ready,
            }
        )

    observed_channels = sorted(
        row["channel_id"] for row in channel_payloads if row["observed_production_source_ids"]
    )
    blind_spots = sorted(
        row["channel_id"] for row in channel_payloads if row["blind_spot"]
    )
    production_channel_ids = sorted(
        row["channel_id"] for row in channel_payloads if row["production_live_source_ids"]
    )
    mapped_observed = sorted(
        {
            source_id
            for row in channel_payloads
            for source_id in row["observed_production_source_ids"]
        }
    )

    return {
        "schema_version": COVERAGE_SCHEMA_VERSION,
        "channel_count": len(channel_payloads),
        "production_live_channel_count": len(production_channel_ids),
        "observed_channel_count": len(observed_channels),
        "blind_spot_channel_count": len(blind_spots),
        "production_live_channel_ids": production_channel_ids,
        "observed_channel_ids": observed_channels,
        "blind_spot_channel_ids": blind_spots,
        "latest_live_observation_coverage": {
            "production_live_source_count": len(production_ids),
            "adapter_supported_source_count": len(supported_ids),
            "observed_production_source_count": len(observed_ids),
            "production_live_source_ids": sorted(production_ids),
            "adapter_supported_source_ids": sorted(supported_ids),
            "observed_production_source_ids": sorted(observed_ids),
        },
        "mapped_observed_production_source_ids": mapped_observed,
        "unmapped_operational_source_ids": sorted(set(operational_by_id) - mapped_operational),
        "unmapped_candidate_source_ids": sorted(set(candidate_by_id) - mapped_candidates),
        "channels": channel_payloads,
        "truth_boundaries": [
            "SOURCE_COVERAGE_NE_EVIDENCE_CHANNEL_COVERAGE",
            "ONE_OBSERVED_SOURCE_NE_CHANNEL_COMPLETENESS",
            "OBSERVED_CHANNEL_NE_REPRESENTATIVE_POPULATION_COVERAGE",
            "REGISTERED_SURFACE_NE_PRODUCTION_OBSERVATION",
            "MANUAL_SURFACE_NE_LIVE_SENSOR",
            "CANDIDATE_SOURCE_NE_ACTIVE_SENSOR",
            "GLOBAL_AUXILIARY_NE_CHINA_PRIMARY_EVIDENCE",
            "PLATFORM_NE_ONTOLOGY",
            "SEARCH_SALIENCE_NE_PAID_DEMAND",
            "SOCIAL_DISCOURSE_NE_MARKET_DEMAND",
            "RESEARCH_REPORT_NE_CURRENT_LOCAL_REALITY",
            "HARD_BEHAVIOR_NE_PAYMENT_OR_OPPORTUNITY",
            "UNKNOWN_NE_PASS"
        ],
    }


GOVERNING_INVARIANTS = (
    "EVIDENCE_CHANNEL_REGISTRY_IS_DATA_GOVERNED_NOT_CODE_ENUM",
    "CHANNEL_COVERAGE_REQUIRES_ACTUAL_LATEST_FABRIC_OBSERVATION",
    "REGISTERED_MANUAL_AND_CANDIDATE_SOURCES_REMAIN_VISIBLE_WITHOUT_PROMOTION",
    "ALL_OPERATIONAL_AND_CANDIDATE_SOURCES_MUST_REMAIN_CLASSIFIABLE_OR_EXPLICITLY_UNMAPPED",
    "PLATFORM_NE_ONTOLOGY",
    "UNKNOWN_NE_PASS",
)
