"""Govern broad internet research without turning any source into the strategy.

The control plane decides *why* to search, *what* coverage is required, how far a
research agent may expand, and when the resulting evidence is broad enough to be
used as discovery context.  It does not fetch the web itself and it never promotes
commercial truth.

Concrete executors may be ChatGPT/Web, a browser agent, an official API, a direct
source adapter, an authorized export, or documented manual sampling.  Executors
must return provenance-bearing evidence into the Observation Fabric.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import urlparse

from src.semantic_kernel import SEMANTIC_PRIMITIVES


RESEARCH_SCOPE_STATES = frozenset(
    {"CALIBRATION_ONLY", "PARTIAL_DISCOVERY", "BROAD_DISCOVERY_READY"}
)
RESEARCH_LANES = (
    "CHINA_CORE",
    "JIANGSU_ZOOM",
    "XUZHOU_ZOOM",
    "GLOBAL_AUXILIARY",
    "CONTRADICTION_SEARCH",
    "SOURCE_DISCOVERY",
)
DEFAULT_EXECUTION_MODES = (
    "INTERACTIVE_AGENT_WEB",
    "DIRECT_PUBLIC_SOURCE",
    "AUTHORIZED_API",
    "AUTHORIZED_EXPORT",
    "PUBLIC_MANUAL",
)


@dataclass(frozen=True)
class ResearchSeed:
    seed_id: str
    text: str
    language: str
    target_primitives: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.seed_id.strip() or not self.text.strip() or not self.language.strip():
            raise ValueError("research seed identity/text/language are required")
        if not self.target_primitives:
            raise ValueError("target_primitives are required")
        unknown = set(self.target_primitives) - SEMANTIC_PRIMITIVES
        if unknown:
            raise ValueError(f"unknown semantic primitives: {sorted(unknown)}")


@dataclass(frozen=True)
class ResearchMission:
    mission_id: str
    as_of_date: str
    primary_geography: str
    zoom_geographies: tuple[str, ...]
    objective_primitives: tuple[str, ...]
    seeds: tuple[ResearchSeed, ...]
    lane_weights: Mapping[str, int]
    freshness_days: int = 30
    max_query_count: int = 80
    max_results_per_query: int = 20
    max_results_per_host: int = 25
    min_independent_hosts: int = 8
    min_source_families: int = 5
    max_single_host_share: float = 0.30
    max_global_auxiliary_share: float = 0.35
    require_domestic_corroboration_for_global: bool = True
    cross_border_mode: str = "EXCEPTION_ONLY"
    allowed_execution_modes: tuple[str, ...] = DEFAULT_EXECUTION_MODES

    def __post_init__(self) -> None:
        if not self.mission_id.strip():
            raise ValueError("mission_id is required")
        date.fromisoformat(self.as_of_date)
        if self.primary_geography != "CN":
            raise ValueError("primary research geography must remain CN")
        if not self.zoom_geographies:
            raise ValueError("zoom_geographies are required")
        if not self.objective_primitives:
            raise ValueError("objective_primitives are required")
        unknown = set(self.objective_primitives) - SEMANTIC_PRIMITIVES
        if unknown:
            raise ValueError(f"unknown objective primitives: {sorted(unknown)}")
        if not self.seeds:
            raise ValueError("at least one research seed is required")
        if set(self.lane_weights) != set(RESEARCH_LANES):
            raise ValueError("lane_weights must define every research lane exactly once")
        if any(not isinstance(v, int) or isinstance(v, bool) or v < 0 for v in self.lane_weights.values()):
            raise ValueError("lane weights must be non-negative integers")
        if sum(self.lane_weights.values()) <= 0:
            raise ValueError("lane weights must allocate at least one query")
        for name in (
            "freshness_days",
            "max_query_count",
            "max_results_per_query",
            "max_results_per_host",
            "min_independent_hosts",
            "min_source_families",
        ):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise ValueError(f"{name} must be an integer >= 1")
        for name in ("max_single_host_share", "max_global_auxiliary_share"):
            value = getattr(self, name)
            if not isinstance(value, (float, int)) or isinstance(value, bool) or not 0 < float(value) <= 1:
                raise ValueError(f"{name} must be in (0, 1]")
        if self.cross_border_mode not in {"DISABLED", "EXCEPTION_ONLY"}:
            raise ValueError("cross_border_mode must be DISABLED or EXCEPTION_ONLY")
        if not self.allowed_execution_modes:
            raise ValueError("allowed_execution_modes are required")


@dataclass(frozen=True)
class ResearchQueryTask:
    query_id: str
    seed_id: str
    lane: str
    query: str
    language: str
    target_geography: str
    target_primitives: tuple[str, ...]
    purpose: str
    execution_modes: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ResearchEvidenceRecord:
    evidence_id: str
    query_id: str
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
            "query_id",
            "source_url",
            "source_family",
            "origin_geography",
            "relevance_geography",
            "provenance_ref",
            "collected_via",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} is required")
        parsed = urlparse(self.source_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("source_url must be an absolute http(s) URL")

    @property
    def host(self) -> str:
        return (urlparse(self.source_url).hostname or "").lower()


@dataclass(frozen=True)
class ResearchCoverageAssessment:
    state: str
    mission_id: str
    evidence_count: int
    independent_host_count: int
    source_family_count: int
    lane_counts: Mapping[str, int]
    host_counts: Mapping[str, int]
    source_family_counts: Mapping[str, int]
    blockers: tuple[str, ...]
    cautions: tuple[str, ...]
    broad_discovery_use_authorized: bool

    def __post_init__(self) -> None:
        if self.state not in RESEARCH_SCOPE_STATES:
            raise ValueError(f"unsupported research scope state: {self.state}")
        if self.broad_discovery_use_authorized != (self.state == "BROAD_DISCOVERY_READY"):
            raise ValueError("broad discovery authorization must match scope state")

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _seed_from_dict(raw: Mapping[str, Any]) -> ResearchSeed:
    return ResearchSeed(
        seed_id=str(raw.get("seed_id") or "").strip(),
        text=str(raw.get("text") or "").strip(),
        language=str(raw.get("language") or "").strip(),
        target_primitives=tuple(str(v).strip() for v in raw.get("target_primitives", []) if str(v).strip()),
    )


def mission_from_dict(raw: Mapping[str, Any]) -> ResearchMission:
    allowed = {
        "mission_id",
        "as_of_date",
        "primary_geography",
        "zoom_geographies",
        "objective_primitives",
        "seeds",
        "lane_weights",
        "freshness_days",
        "max_query_count",
        "max_results_per_query",
        "max_results_per_host",
        "min_independent_hosts",
        "min_source_families",
        "max_single_host_share",
        "max_global_auxiliary_share",
        "require_domestic_corroboration_for_global",
        "cross_border_mode",
        "allowed_execution_modes",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise ValueError(f"unknown research mission fields: {sorted(unknown)}")
    seeds_raw = raw.get("seeds", [])
    if not isinstance(seeds_raw, list):
        raise ValueError("seeds must be a JSON array")
    lane_weights = raw.get("lane_weights", {})
    if not isinstance(lane_weights, Mapping):
        raise ValueError("lane_weights must be an object")
    return ResearchMission(
        mission_id=str(raw.get("mission_id") or "").strip(),
        as_of_date=str(raw.get("as_of_date") or "").strip(),
        primary_geography=str(raw.get("primary_geography") or "").strip(),
        zoom_geographies=tuple(str(v).strip() for v in raw.get("zoom_geographies", []) if str(v).strip()),
        objective_primitives=tuple(str(v).strip() for v in raw.get("objective_primitives", []) if str(v).strip()),
        seeds=tuple(_seed_from_dict(item) for item in seeds_raw),
        lane_weights={str(k): int(v) for k, v in lane_weights.items()},
        freshness_days=int(raw.get("freshness_days", 30)),
        max_query_count=int(raw.get("max_query_count", 80)),
        max_results_per_query=int(raw.get("max_results_per_query", 20)),
        max_results_per_host=int(raw.get("max_results_per_host", 25)),
        min_independent_hosts=int(raw.get("min_independent_hosts", 8)),
        min_source_families=int(raw.get("min_source_families", 5)),
        max_single_host_share=float(raw.get("max_single_host_share", 0.30)),
        max_global_auxiliary_share=float(raw.get("max_global_auxiliary_share", 0.35)),
        require_domestic_corroboration_for_global=bool(raw.get("require_domestic_corroboration_for_global", True)),
        cross_border_mode=str(raw.get("cross_border_mode", "EXCEPTION_ONLY")),
        allowed_execution_modes=tuple(
            str(v).strip() for v in raw.get("allowed_execution_modes", DEFAULT_EXECUTION_MODES) if str(v).strip()
        ),
    )


def _query_id(mission_id: str, seed_id: str, lane: str, query: str) -> str:
    payload = json.dumps([mission_id, seed_id, lane, query], ensure_ascii=False, separators=(",", ":"))
    return "rq-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:18]


def _qualify_query(seed: ResearchSeed, lane: str, as_of_year: str) -> tuple[str, str, str]:
    text = seed.text.strip()
    if lane == "CHINA_CORE":
        return f"{text} 中国 {as_of_year} 数据 行为 变化", "CN", "Establish China-primary reality from independent public/authorized evidence."
    if lane == "JIANGSU_ZOOM":
        return f"{text} 江苏 {as_of_year} 数据 行为 变化", "CN-JS", "Test whether the China signal diverges or concentrates in Jiangsu."
    if lane == "XUZHOU_ZOOM":
        return f"{text} 徐州 {as_of_year} 数据 行为 变化", "CN-JS-XUZHOU", "Seek locally verifiable Xuzhou actor/state evidence."
    if lane == "GLOBAL_AUXILIARY":
        return f"{text} China Chinese {as_of_year}", "CN", "Use global information only to explain, challenge, lead or reprice a China hypothesis."
    if lane == "CONTRADICTION_SEARCH":
        return f"{text} 中国 {as_of_year} 反证 争议 相反 数据", "CN", "Actively search for counterevidence and alternative explanations."
    if lane == "SOURCE_DISCOVERY":
        return f"{text} 中国 数据源 API 报告 评论 论坛 公开数据 {as_of_year}", "CN", "Discover new lawful/authorized observation surfaces without activating them automatically."
    raise ValueError(f"unsupported research lane: {lane}")


def _allocate_slots(weights: Mapping[str, int], total: int) -> dict[str, int]:
    positive = {lane: weight for lane, weight in weights.items() if weight > 0}
    if not positive:
        return {lane: 0 for lane in RESEARCH_LANES}
    total_weight = sum(positive.values())
    raw = {lane: total * weight / total_weight for lane, weight in positive.items()}
    allocated = {lane: int(value) for lane, value in raw.items()}
    remainder = total - sum(allocated.values())
    order = sorted(positive, key=lambda lane: (-(raw[lane] - allocated[lane]), RESEARCH_LANES.index(lane)))
    for lane in order[:remainder]:
        allocated[lane] += 1
    return {lane: allocated.get(lane, 0) for lane in RESEARCH_LANES}


def build_research_plan(
    mission: ResearchMission,
    *,
    dynamic_terms: Sequence[str] = (),
) -> dict[str, Any]:
    """Create a bounded query plan for any compliant research executor.

    ``dynamic_terms`` may come from residual concepts, observed changes, macro
    divergences, pattern gaps, or newly discovered vocabulary.  They expand the
    mission without modifying the ontology or source registry.
    """

    year = mission.as_of_date[:4]
    dynamic_seeds: list[ResearchSeed] = []
    for index, term in enumerate(dynamic_terms, start=1):
        term = str(term).strip()
        if not term:
            continue
        dynamic_seeds.append(
            ResearchSeed(
                seed_id=f"dynamic-{index:03d}",
                text=term,
                language="und",
                target_primitives=mission.objective_primitives,
            )
        )
    # Novel/residual vocabulary is intentionally researched first. Bootstrap
    # seeds remain coverage scaffolding, not a permanent taxonomy boundary.
    seeds = dynamic_seeds + list(mission.seeds)

    slots = _allocate_slots(mission.lane_weights, mission.max_query_count)
    tasks: list[ResearchQueryTask] = []
    if seeds:
        for lane in RESEARCH_LANES:
            lane_slots = slots[lane]
            for index in range(lane_slots):
                seed = seeds[index % len(seeds)]
                query, geography, purpose = _qualify_query(seed, lane, year)
                tasks.append(
                    ResearchQueryTask(
                        query_id=_query_id(mission.mission_id, seed.seed_id, lane, query),
                        seed_id=seed.seed_id,
                        lane=lane,
                        query=query,
                        language=seed.language,
                        target_geography=geography,
                        target_primitives=seed.target_primitives,
                        purpose=purpose,
                        execution_modes=mission.allowed_execution_modes,
                    )
                )

    query_ids = [task.query_id for task in tasks]
    query_texts = [task.query for task in tasks]
    if len(set(query_ids)) != len(tasks) or len(set(query_texts)) != len(tasks):
        raise ValueError(
            "research plan contains duplicate query slots; add distinct bootstrap seeds/dynamic terms or reduce the query budget"
        )

    return {
        "schema_version": "research-control-plane.v1",
        "mission": {
            "mission_id": mission.mission_id,
            "as_of_date": mission.as_of_date,
            "primary_geography": mission.primary_geography,
            "zoom_geographies": list(mission.zoom_geographies),
            "objective_primitives": list(mission.objective_primitives),
            "freshness_days": mission.freshness_days,
            "max_query_count": mission.max_query_count,
            "max_results_per_query": mission.max_results_per_query,
            "max_results_per_host": mission.max_results_per_host,
            "min_independent_hosts": mission.min_independent_hosts,
            "min_source_families": mission.min_source_families,
            "max_single_host_share": mission.max_single_host_share,
            "max_global_auxiliary_share": mission.max_global_auxiliary_share,
            "require_domestic_corroboration_for_global": mission.require_domestic_corroboration_for_global,
            "cross_border_mode": mission.cross_border_mode,
        },
        "dynamic_term_count": len(dynamic_seeds),
        "lane_query_budget": slots,
        "query_count": len(tasks),
        "queries": [task.as_dict() for task in tasks],
        "executor_contract": {
            "fetch_policy": "PUBLIC_OR_AUTHORIZED_ONLY",
            "private_messages_allowed": False,
            "login_or_access_control_bypass_allowed": False,
            "captcha_or_antibot_bypass_allowed": False,
            "source_discovery_implies_activation": False,
            "foreign_signal_implies_china_fact": False,
            "social_salience_implies_population_share": False,
            "result_to_observation_requirement": "PROVENANCE_BEARING_OBSERVATION_ENVELOPE",
            "stop_conditions": [
                "QUERY_BUDGET_EXHAUSTED",
                "COVERAGE_GATE_SATISFIED",
                "SOURCE_PERMISSION_BLOCKED",
                "MARGINAL_SOURCE_DIVERSITY_EXHAUSTED",
            ],
        },
        "truth_boundaries": [
            "RESEARCH_PLAN_NE_EVIDENCE",
            "SEARCH_RESULT_NE_OBSERVATION_UNTIL_PROVENANCE_CAPTURED",
            "GLOBAL_AUXILIARY_NE_DOMESTIC_FACT",
            "SOURCE_DISCOVERY_NE_SOURCE_ACTIVATION",
            "COVERAGE_NE_COMMERCIAL_TRUTH",
            "CROSS_BORDER_EXCEPTION_ONLY",
        ],
    }


def evidence_from_dict(raw: Mapping[str, Any]) -> ResearchEvidenceRecord:
    return ResearchEvidenceRecord(
        evidence_id=str(raw.get("evidence_id") or "").strip(),
        query_id=str(raw.get("query_id") or "").strip(),
        source_url=str(raw.get("source_url") or "").strip(),
        source_family=str(raw.get("source_family") or "").strip(),
        origin_geography=str(raw.get("origin_geography") or "").strip(),
        relevance_geography=str(raw.get("relevance_geography") or "").strip(),
        provenance_ref=str(raw.get("provenance_ref") or "").strip(),
        collected_via=str(raw.get("collected_via") or "").strip(),
        domestic_corroboration_ref=(str(raw.get("domestic_corroboration_ref")).strip() if raw.get("domestic_corroboration_ref") else None),
        contradiction=bool(raw.get("contradiction", False)),
    )


def assess_research_coverage(
    mission: ResearchMission,
    plan: Mapping[str, Any],
    evidence: Iterable[ResearchEvidenceRecord],
) -> ResearchCoverageAssessment:
    """Assess breadth only; this never judges whether an opportunity is true."""

    evidence_items = tuple(evidence)
    query_lane = {
        str(item.get("query_id")): str(item.get("lane"))
        for item in plan.get("queries", []) or []
        if item.get("query_id") and item.get("lane")
    }
    unknown_query_ids = sorted({item.query_id for item in evidence_items if item.query_id not in query_lane})
    if unknown_query_ids:
        raise ValueError(f"evidence references unknown query ids: {unknown_query_ids}")

    host_counts = Counter(item.host for item in evidence_items)
    family_counts = Counter(item.source_family for item in evidence_items)
    lane_counts = Counter(query_lane[item.query_id] for item in evidence_items)

    blockers: list[str] = []
    cautions: list[str] = []
    count = len(evidence_items)
    if count == 0:
        blockers.append("NO_RESEARCH_EVIDENCE_EXECUTED")
    if len(host_counts) < mission.min_independent_hosts:
        blockers.append("INSUFFICIENT_INDEPENDENT_HOSTS")
    if len(family_counts) < mission.min_source_families:
        blockers.append("INSUFFICIENT_SOURCE_FAMILY_DIVERSITY")

    required_lanes = {lane for lane, weight in mission.lane_weights.items() if weight > 0}
    missing_lanes = sorted(lane for lane in required_lanes if lane_counts.get(lane, 0) == 0)
    if missing_lanes:
        blockers.append("MISSING_RESEARCH_LANES:" + ",".join(missing_lanes))

    if count:
        largest_host_share = max(host_counts.values()) / count
        if largest_host_share > mission.max_single_host_share:
            blockers.append("SINGLE_HOST_OVERCONCENTRATION")
        global_aux_count = lane_counts.get("GLOBAL_AUXILIARY", 0)
        if global_aux_count / count > mission.max_global_auxiliary_share:
            blockers.append("GLOBAL_AUXILIARY_OVERWEIGHT")

    if mission.require_domestic_corroboration_for_global:
        uncorroborated = [
            item.evidence_id
            for item in evidence_items
            if query_lane[item.query_id] == "GLOBAL_AUXILIARY"
            and not item.domestic_corroboration_ref
        ]
        if uncorroborated:
            cautions.append("GLOBAL_AUXILIARY_WITHOUT_DOMESTIC_CORROBORATION")

    if lane_counts.get("CONTRADICTION_SEARCH", 0) == 0:
        cautions.append("NO_COUNTEREVIDENCE_CAPTURED")

    if not evidence_items:
        state = "CALIBRATION_ONLY"
    elif blockers:
        state = "PARTIAL_DISCOVERY"
    else:
        state = "BROAD_DISCOVERY_READY"

    return ResearchCoverageAssessment(
        state=state,
        mission_id=mission.mission_id,
        evidence_count=count,
        independent_host_count=len(host_counts),
        source_family_count=len(family_counts),
        lane_counts=dict(sorted(lane_counts.items())),
        host_counts=dict(sorted(host_counts.items())),
        source_family_counts=dict(sorted(family_counts.items())),
        blockers=tuple(blockers),
        cautions=tuple(cautions),
        broad_discovery_use_authorized=state == "BROAD_DISCOVERY_READY",
    )


def empty_coverage_assessment(mission: ResearchMission, plan: Mapping[str, Any]) -> dict[str, Any]:
    """Explicitly mark a generated-but-unexecuted mission as calibration-only."""

    assessment = assess_research_coverage(mission, plan, ())
    payload = assessment.as_dict()
    payload["truth_notes"] = [
        "The control plane has generated a research mission; no internet evidence is implied.",
        "CALIBRATION_ONLY means current ObservedPatterns may test framework behavior but must not be presented as broad market discovery.",
        "A future web/browser/API executor must return provenance-bearing evidence before coverage can advance.",
        "BROAD_DISCOVERY_READY is a coverage state only and never proves a business opportunity.",
    ]
    return payload
