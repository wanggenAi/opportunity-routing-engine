"""Bind web/browser/API research captures to an exact governed mission task.

Executors should not hand-copy opaque query IDs. They return a stable mission lane,
seed identity and provenance-bearing source metadata; this module resolves the one
exact query task from the already-built plan. Zero or multiple matches fail closed.

A capture is research evidence only. Commercial/canonical truth fields are rejected.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping
from urllib.parse import urlparse

from src.research_control_plane import RESEARCH_LANES


CAPTURE_SCHEMA_VERSION = "research-executor-capture.v1"
_FORBIDDEN_FIELDS = frozenset(
    {
        "opportunity_score",
        "commercial_score",
        "payer",
        "paid_need",
        "route_testable",
        "core_business_candidate",
        "business_promotion",
        "availability_confirmed",
        "permission_confirmed",
        "taxonomy_promotion",
    }
)
_ALLOWED_FIELDS = frozenset(
    {
        "evidence_id",
        "mission_id",
        "lane",
        "seed_id",
        "source_url",
        "source_family",
        "origin_geography",
        "relevance_geography",
        "provenance_ref",
        "collected_via",
        "domestic_corroboration_ref",
        "contradiction",
    }
)


@dataclass(frozen=True)
class ResearchExecutorCapture:
    evidence_id: str
    mission_id: str
    lane: str
    seed_id: str
    source_url: str
    source_family: str
    origin_geography: str
    relevance_geography: str
    provenance_ref: str
    collected_via: str
    domestic_corroboration_ref: str | None = None
    contradiction: bool = False

    def __post_init__(self) -> None:
        for name in (
            "evidence_id",
            "mission_id",
            "lane",
            "seed_id",
            "source_url",
            "source_family",
            "origin_geography",
            "relevance_geography",
            "provenance_ref",
            "collected_via",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} is required")
        if self.lane not in RESEARCH_LANES:
            raise ValueError(f"unsupported research lane: {self.lane}")
        parsed = urlparse(self.source_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("source_url must be an absolute http(s) URL")

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def capture_from_dict(raw: Mapping[str, Any]) -> ResearchExecutorCapture:
    forbidden = sorted(set(raw) & _FORBIDDEN_FIELDS)
    if forbidden:
        raise ValueError(f"executor capture cannot carry commercial/canonical truth fields: {forbidden}")
    unknown = sorted(set(raw) - _ALLOWED_FIELDS)
    if unknown:
        raise ValueError(f"unknown research executor capture fields: {unknown}")
    return ResearchExecutorCapture(
        evidence_id=str(raw.get("evidence_id") or "").strip(),
        mission_id=str(raw.get("mission_id") or "").strip(),
        lane=str(raw.get("lane") or "").strip(),
        seed_id=str(raw.get("seed_id") or "").strip(),
        source_url=str(raw.get("source_url") or "").strip(),
        source_family=str(raw.get("source_family") or "").strip(),
        origin_geography=str(raw.get("origin_geography") or "").strip(),
        relevance_geography=str(raw.get("relevance_geography") or "").strip(),
        provenance_ref=str(raw.get("provenance_ref") or "").strip(),
        collected_via=str(raw.get("collected_via") or "").strip(),
        domestic_corroboration_ref=(
            None
            if raw.get("domestic_corroboration_ref") is None
            else str(raw.get("domestic_corroboration_ref") or "").strip() or None
        ),
        contradiction=bool(raw.get("contradiction", False)),
    )


def _plan_mission_id(plan: Mapping[str, Any]) -> str:
    mission = plan.get("mission")
    if not isinstance(mission, Mapping):
        raise ValueError("research plan mission is missing")
    mission_id = str(mission.get("mission_id") or "").strip()
    if not mission_id:
        raise ValueError("research plan mission_id is missing")
    return mission_id


def bind_capture_to_plan(
    plan: Mapping[str, Any],
    capture: ResearchExecutorCapture,
) -> dict[str, Any]:
    """Return canonical ResearchEvidence-shaped data with exact query lineage."""

    mission_id = _plan_mission_id(plan)
    if capture.mission_id != mission_id:
        raise ValueError("capture mission_id does not match research plan")

    queries = plan.get("queries")
    if not isinstance(queries, list):
        raise ValueError("research plan queries must be an array")
    matches = [
        item
        for item in queries
        if isinstance(item, Mapping)
        and str(item.get("lane") or "") == capture.lane
        and str(item.get("seed_id") or "") == capture.seed_id
    ]
    if len(matches) != 1:
        raise ValueError(
            "capture must resolve to exactly one research query task; "
            f"resolved={len(matches)} lane={capture.lane} seed_id={capture.seed_id}"
        )
    task = matches[0]
    query_id = str(task.get("query_id") or "").strip()
    if not query_id:
        raise ValueError("resolved query task has no query_id")

    target_geography = str(task.get("target_geography") or "").strip()
    if target_geography and not capture.relevance_geography.startswith("CN"):
        raise ValueError("China-primary mission evidence must declare China relevance")

    return {
        "evidence_id": capture.evidence_id,
        "query_id": query_id,
        "source_url": capture.source_url,
        "source_family": capture.source_family,
        "origin_geography": capture.origin_geography,
        "relevance_geography": capture.relevance_geography,
        "provenance_ref": capture.provenance_ref,
        "collected_via": capture.collected_via,
        "domestic_corroboration_ref": capture.domestic_corroboration_ref,
        "contradiction": capture.contradiction,
    }


def bind_captures_to_plan(
    plan: Mapping[str, Any],
    captures: Iterable[ResearchExecutorCapture],
) -> dict[str, Any]:
    records = tuple(captures)
    evidence_ids = [item.evidence_id for item in records]
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError("duplicate research executor evidence_id")
    evidence = [bind_capture_to_plan(plan, item) for item in records]
    return {
        "schema_version": "research-evidence-batch.v1",
        "mission_id": _plan_mission_id(plan),
        "capture_schema_version": CAPTURE_SCHEMA_VERSION,
        "evidence_count": len(evidence),
        "evidence": evidence,
        "truth_boundaries": [
            "EXECUTOR_CAPTURE_NE_OBSERVATION",
            "QUERY_BINDING_NE_EVIDENCE_VALIDATION",
            "SEARCH_RESULT_NE_WORLD_FACT",
            "GLOBAL_AUXILIARY_NE_CHINA_FACT",
            "RESEARCH_EVIDENCE_NE_COMMERCIAL_TRUTH",
        ],
    }
