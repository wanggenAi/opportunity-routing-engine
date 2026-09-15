"""Reconcile live-source registry truth with unified Observation Fabric coverage.

A source may be marked production-live in the operational registry while still lacking
an adapter into the source-neutral Observation Fabric. Likewise, having adapter code
does not prove that the latest durable Fabric actually contains an observation from
that source. This module keeps those states separate and fail-closed.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Iterable

from src.sensor_portfolio import OperationalSource


# Governed source identities currently understood by the unified adapter layer.
# This is intentionally narrower than "anything the generic function can parse".
UNIFIED_ADAPTER_SUPPORT: dict[str, tuple[str, ...]] = {
    "JS_STATS": ("jiangsu_money_flow_observations",),
    "XZ_GGZY": (
        "xuzhou_procurement_observations",
        "xuzhou_resource_underuse_observations",
    ),
    "EJY365_XZ_LINKED": ("xuzhou_resource_underuse_observations",),
    "JS_GGZY_XZ_MIRROR": ("xuzhou_resource_underuse_observations",),
}


def _source_counts(assessment: Mapping[str, Any]) -> dict[str, int]:
    if assessment.get("schema_version") != "live-observation-fabric.v1":
        raise ValueError("unsupported Observation Fabric assessment schema")
    if assessment.get("fixture_only") is not False:
        raise ValueError("coverage assessment requires non-fixture Observation Fabric state")
    if assessment.get("live_source_artifacts") is not True:
        raise ValueError("coverage assessment requires live source artifacts")

    raw = assessment.get("source_counts")
    if not isinstance(raw, Mapping):
        raise ValueError("Observation Fabric source_counts must be an object")
    result: dict[str, int] = {}
    for source_id, count in raw.items():
        if not isinstance(source_id, str) or not source_id.strip():
            raise ValueError("Observation Fabric source id must be a non-empty string")
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ValueError(f"Observation Fabric source count for {source_id} must be a non-negative integer")
        if source_id in result:
            raise ValueError(f"duplicate Observation Fabric source id: {source_id}")
        result[source_id] = count

    current_count = assessment.get("current_observation_count")
    if isinstance(current_count, bool) or not isinstance(current_count, int) or current_count < 0:
        raise ValueError("current_observation_count must be a non-negative integer")
    if sum(result.values()) != current_count:
        raise ValueError("source_counts do not sum to current_observation_count")
    return result


def _validate_adapter_support(
    adapter_support: Mapping[str, Sequence[str]],
) -> dict[str, tuple[str, ...]]:
    result: dict[str, tuple[str, ...]] = {}
    for source_id, adapters in adapter_support.items():
        if not isinstance(source_id, str) or not source_id.strip():
            raise ValueError("adapter-supported source id must be non-empty")
        if isinstance(adapters, (str, bytes)) or not isinstance(adapters, Sequence) or not adapters:
            raise ValueError(f"adapter support for {source_id} must name at least one adapter")
        normalized: list[str] = []
        for adapter in adapters:
            if not isinstance(adapter, str) or not adapter.strip():
                raise ValueError(f"adapter support for {source_id} contains an invalid adapter name")
            normalized.append(adapter.strip())
        result[source_id.strip()] = tuple(normalized)
    return result


def reconcile_live_observation_coverage(
    operational_sources: Iterable[OperationalSource],
    fabric_assessment: Mapping[str, Any],
    *,
    adapter_support: Mapping[str, Sequence[str]] = UNIFIED_ADAPTER_SUPPORT,
) -> dict[str, Any]:
    """Return a fail-closed registry → adapter → latest-Fabric coverage matrix."""

    operational = tuple(operational_sources)
    production = tuple(item for item in operational if item.is_production_live)
    production_ids = {item.source_id for item in production}
    if len({item.source_id for item in operational}) != len(operational):
        raise ValueError("duplicate source ids in operational registry")

    source_counts = _source_counts(fabric_assessment)
    observed_ids = {source_id for source_id, count in source_counts.items() if count > 0}
    support = _validate_adapter_support(adapter_support)
    supported_ids = set(support)

    rows: list[dict[str, Any]] = []
    for source in sorted(production, key=lambda item: item.source_id):
        observed_count = source_counts.get(source.source_id, 0)
        adapter_supported = source.source_id in supported_ids
        observed = observed_count > 0
        integrity_alert = None
        if observed and adapter_supported:
            state = "OBSERVED_IN_LATEST_FABRIC"
        elif adapter_supported:
            state = "ADAPTER_SUPPORTED_NOT_OBSERVED"
        elif observed:
            state = "OBSERVED_WITHOUT_GOVERNED_ADAPTER_SUPPORT"
            integrity_alert = "OBSERVATION_WITHOUT_GOVERNED_ADAPTER_SUPPORT"
        else:
            state = "NO_UNIFIED_ADAPTER"
        rows.append(
            {
                "source_id": source.source_id,
                "registry_status": source.status,
                "registry_production_live": True,
                "adapter_supported": adapter_supported,
                "adapter_names": list(support.get(source.source_id, ())),
                "observed_in_latest_fabric": observed,
                "latest_current_observation_count": observed_count,
                "coverage_state": state,
                "integrity_alert": integrity_alert,
            }
        )

    observed_production = sorted(production_ids & observed_ids)
    supported_production = sorted(production_ids & supported_ids)
    supported_not_observed = sorted(
        source_id
        for source_id in production_ids & supported_ids
        if source_id not in observed_ids
    )
    no_unified_adapter = sorted(production_ids - supported_ids)
    observed_without_support = sorted((production_ids & observed_ids) - supported_ids)
    observed_nonproduction = sorted(observed_ids - production_ids)

    upstream_manifest = fabric_assessment.get("upstream_manifest")
    if upstream_manifest is not None and not isinstance(upstream_manifest, Mapping):
        raise ValueError("upstream_manifest must be an object or null")

    return {
        "schema_version": "live-observation-coverage.v1",
        "production_live_registry_count": len(production_ids),
        "adapter_supported_production_count": len(supported_production),
        "observed_production_count": len(observed_production),
        "adapter_supported_not_observed_count": len(supported_not_observed),
        "no_unified_adapter_count": len(no_unified_adapter),
        "observed_without_governed_support_count": len(observed_without_support),
        "observed_nonproduction_count": len(observed_nonproduction),
        "latest_fabric_current_observation_count": sum(source_counts.values()),
        "production_live_source_ids": sorted(production_ids),
        "adapter_supported_production_source_ids": supported_production,
        "observed_production_source_ids": observed_production,
        "adapter_supported_not_observed_source_ids": supported_not_observed,
        "no_unified_adapter_source_ids": no_unified_adapter,
        "observed_without_governed_support_source_ids": observed_without_support,
        "observed_nonproduction_source_ids": observed_nonproduction,
        "latest_fabric_source_counts": dict(sorted(source_counts.items())),
        "coverage_rows": rows,
        "fabric_upstream_manifest": dict(upstream_manifest) if upstream_manifest is not None else None,
        "truth_boundaries": [
            "ACTIVE_LIVE_REGISTRY_NE_OBSERVED_IN_FABRIC",
            "ADAPTER_SUPPORT_NE_CURRENT_OBSERVATION",
            "SEPARATE_WORKFLOW_NE_UNIFIED_FABRIC",
            "MISSING_FABRIC_SOURCE_NE_ZERO_WORLD_ACTIVITY",
            "OBSERVED_SOURCE_NE_COMPLETE_DOMAIN_COVERAGE",
            "NO_COMMERCIAL_PROMOTION",
            "NO_TAXONOMY_PROMOTION",
            "UNKNOWN_NE_PASS",
        ],
    }


GOVERNING_INVARIANTS = (
    "REGISTRY_LIVENESS_ADAPTER_SUPPORT_AND_CURRENT_OBSERVATION_ARE_DISTINCT",
    "LATEST_FABRIC_ARTIFACT_IS_REQUIRED_FOR_OBSERVED_COVERAGE",
    "ADAPTER_MANIFEST_IS_EXPLICIT_AND_SOURCE_ID_BOUND",
    "MISSING_UNIFIED_ADAPTER_MUST_REMAIN_VISIBLE",
    "OBSERVATION_WITHOUT_GOVERNED_SUPPORT_IS_AN_INTEGRITY_ALERT",
    "UNKNOWN_NE_PASS",
)
