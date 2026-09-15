"""Reconcile operational source registry and dynamic sensor candidates.

The repository historically contains two different truths:

- ``data/source_registry.csv`` records sources already known to operations, including
  live automated collectors, manual surfaces, case-only sources and disabled paths;
- ``data/sensor_candidates.json`` records newly discovered candidates under a
  separate governance lifecycle.

This module produces one read-only portfolio view without changing either registry.
Most importantly, discovery/readiness/manual availability never counts as live
production coverage.
"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

from src.sensor_registry import SensorCandidate, assess_sensor_candidate


@dataclass(frozen=True)
class OperationalSource:
    source_id: str
    name: str
    source_tier: str
    owner: str
    base_url: str
    geography: str
    indicator_scope: str
    access_mode: str
    refresh_cadence: str
    automation_allowed: str
    status: str

    def __post_init__(self) -> None:
        for name in (
            "source_id",
            "name",
            "source_tier",
            "owner",
            "base_url",
            "geography",
            "indicator_scope",
            "access_mode",
            "refresh_cadence",
            "automation_allowed",
            "status",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"operational source {name} is required")
        parsed = urlparse(self.base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("operational source base_url must be an http(s) URL")

    @property
    def is_production_live(self) -> bool:
        """Only explicit ACTIVE_LIVE* registry states are production-live truth."""

        return self.status.strip().upper().startswith("ACTIVE_LIVE")

    @property
    def is_manual_surface(self) -> bool:
        access = self.access_mode.upper()
        status = self.status.upper()
        return "MANUAL" in access or "MANUAL" in status

    @property
    def is_disabled_or_retired(self) -> bool:
        status = self.status.upper()
        return "DISABLED" in status or "RETIRED" in status

    @property
    def operational_class(self) -> str:
        if self.is_production_live:
            return "PRODUCTION_LIVE"
        if self.is_disabled_or_retired:
            return "INACTIVE"
        if self.is_manual_surface:
            return "REGISTERED_MANUAL"
        return "REGISTERED_NONLIVE"

    def as_dict(self) -> dict:
        payload = asdict(self)
        payload.update(
            {
                "operational_class": self.operational_class,
                "production_coverage": self.is_production_live,
            }
        )
        return payload


def load_operational_sources(path: str | Path) -> tuple[OperationalSource, ...]:
    expected = {
        "source_id",
        "name",
        "source_tier",
        "owner",
        "base_url",
        "geography",
        "indicator_scope",
        "access_mode",
        "refresh_cadence",
        "automation_allowed",
        "status",
    }
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("source registry is missing a header")
        if set(reader.fieldnames) != expected:
            raise ValueError(
                f"unexpected source registry columns: {sorted(set(reader.fieldnames))}"
            )
        result: list[OperationalSource] = []
        seen: set[str] = set()
        for row in reader:
            source = OperationalSource(
                **{key: str(row.get(key) or "").strip() for key in expected}
            )
            if source.source_id in seen:
                raise ValueError(f"duplicate operational source_id: {source.source_id}")
            seen.add(source.source_id)
            result.append(source)
    return tuple(result)


def _candidate_record(candidate: SensorCandidate) -> dict:
    assessment = assess_sensor_candidate(candidate)
    explicitly_active = candidate.lifecycle_state == "ACTIVE"
    production_coverage = explicitly_active and bool(assessment["automation_ready"])
    return {
        "source_id": candidate.source_id,
        "name": candidate.name,
        "lifecycle_state": candidate.lifecycle_state,
        "effective_state": assessment["effective_state"],
        "china_relevant": assessment["china_relevant"],
        "qualified": assessment["qualified"],
        "automation_ready": assessment["automation_ready"],
        "production_coverage": production_coverage,
        "qualification_blockers": assessment["qualification_blockers"],
        "activation_blockers": assessment["activation_blockers"],
        "observable_dimensions": list(candidate.observable_dimensions),
    }


def reconcile_sensor_portfolio(
    operational_sources: Iterable[OperationalSource],
    candidates: Iterable[SensorCandidate],
) -> dict:
    operational = tuple(operational_sources)
    candidate_items = tuple(candidates)
    operational_ids = {item.source_id for item in operational}
    candidate_ids = {item.source_id for item in candidate_items}
    if len(operational_ids) != len(operational):
        raise ValueError("duplicate source ids in operational registry")
    if len(candidate_ids) != len(candidate_items):
        raise ValueError("duplicate source ids in candidate registry")

    operational_records = [item.as_dict() for item in operational]
    candidate_records = [_candidate_record(item) for item in candidate_items]

    operational_live = sorted(
        item.source_id for item in operational if item.is_production_live
    )
    candidate_live = sorted(
        item["source_id"] for item in candidate_records if item["production_coverage"]
    )
    production_ids = sorted(set(operational_live) | set(candidate_live))

    overlap = sorted(operational_ids & candidate_ids)
    candidate_only = sorted(candidate_ids - operational_ids)
    operational_only = sorted(operational_ids - candidate_ids)

    mismatches: list[dict] = []
    operational_by_id = {item.source_id: item for item in operational}
    candidate_by_id = {item["source_id"]: item for item in candidate_records}
    for source_id in overlap:
        op_live = operational_by_id[source_id].is_production_live
        cand_live = bool(candidate_by_id[source_id]["production_coverage"])
        if op_live != cand_live:
            mismatches.append(
                {
                    "source_id": source_id,
                    "operational_registry_production_live": op_live,
                    "candidate_registry_production_live": cand_live,
                    "state": "REGISTRY_STATE_MISMATCH",
                }
            )

    manual_sources = sorted(
        item.source_id for item in operational if item.is_manual_surface
    )
    registered_nonlive = sorted(
        item.source_id for item in operational if not item.is_production_live
    )
    candidate_not_production = sorted(
        item["source_id"] for item in candidate_records if not item["production_coverage"]
    )

    return {
        "schema_version": "sensor-portfolio-reconciliation.v1",
        "operational_registry_count": len(operational),
        "candidate_registry_count": len(candidate_items),
        "operational_production_live_count": len(operational_live),
        "candidate_production_live_count": len(candidate_live),
        "production_coverage_count": len(production_ids),
        "registered_nonlive_count": len(registered_nonlive),
        "registered_manual_count": len(manual_sources),
        "candidate_not_production_count": len(candidate_not_production),
        "overlap_count": len(overlap),
        "registry_mismatch_count": len(mismatches),
        "operational_production_live_source_ids": operational_live,
        "candidate_production_live_source_ids": candidate_live,
        "production_coverage_source_ids": production_ids,
        "registered_manual_source_ids": manual_sources,
        "candidate_not_production_source_ids": candidate_not_production,
        "candidate_only_source_ids": candidate_only,
        "operational_only_source_ids": operational_only,
        "overlap_source_ids": overlap,
        "registry_mismatches": mismatches,
        "operational_sources": operational_records,
        "candidate_sources": candidate_records,
        "truth_boundaries": [
            "DISCOVERED_SOURCE_NE_PRODUCTION_COVERAGE",
            "QUALIFIED_SOURCE_NE_PRODUCTION_COVERAGE",
            "ACTIVE_READY_NE_ACTIVE_COLLECTION",
            "MANUAL_SURFACE_NE_AUTOMATED_LIVE_SENSOR",
            "REGISTERED_SOURCE_NE_LIVE_OBSERVATION",
            "GLOBAL_CANDIDATE_NE_CHINA_PRIMARY_EVIDENCE",
            "PLATFORM_NE_ONTOLOGY",
            "PRODUCTION_COVERAGE_REQUIRES_EXPLICIT_LIVE_STATE",
            "REGISTRY_MISMATCH_NE_PASS",
            "UNKNOWN_NE_PASS",
        ],
    }


GOVERNING_INVARIANTS = (
    "OPERATIONAL_AND_CANDIDATE_REGISTRIES_MUST_BE_RECONCILED",
    "DISCOVERY_READINESS_NE_ACTIVATION",
    "MANUAL_ACCESS_NE_AUTOMATED_COLLECTION",
    "PRODUCTION_COVERAGE_COUNTS_ONLY_EXPLICIT_LIVE_STATE",
    "REGISTRY_MISMATCH_MUST_REMAIN_VISIBLE",
    "UNKNOWN_NE_PASS",
)
