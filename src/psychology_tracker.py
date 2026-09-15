"""Consumer psychology signal aggregation for the discovery engine.

This module does not scrape websites and does not claim population prevalence from
social content. It aggregates already-normalized, provenance-retaining signals into
bounded directional indexes used only for opportunity discovery.

Commercial rule: psychology is a sensor; behavior and money are corroboration.
Ontology rule: PERCEPTION / MOTIVE / BEHAVIOR are stable primitives; named
psychology concepts are an open namespace. The seed concepts below are advisory
2026 vocabulary, never a validation boundary.
Evidence rule: every signal and every non-zero corroboration value must retain
explicit evidence lineage. A naked confidence scalar is not evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from math import exp, log
from typing import Iterable, Optional, Sequence


SOURCE_WEIGHTS = {
    "A_HARD_MONEY_BEHAVIOR": 1.00,
    "B_REPRESENTATIVE_RESEARCH": 0.85,
    "C_SEARCH_PLATFORM_TREND": 0.55,
    "D_SOCIAL_MEDIA_LANGUAGE": 0.35,
}

PSYCHOLOGY_PRIMITIVES = frozenset({"PERCEPTION", "MOTIVE", "BEHAVIOR"})

# Advisory seed taxonomy only. New concepts MUST NOT require a core-code change.
PSYCHOLOGY_SEED_CONCEPTS = frozenset(
    {
        "SPENDING_CAUTION",
        "VALUE_FOR_MONEY",
        "SMALL_TRIAL_PREFERENCE",
        "EXPERIENCE_ORIENTATION",
        "EMOTIONAL_VALUE_SELF_REWARD",
        "CONVENIENCE_TIME_VALUE",
        "TRUST_RISK_AVERSION",
        "QUALITY_UPGRADE_SELECTIVITY",
        "HEALTH_LONGEVITY",
        "SOCIAL_CONNECTION_BELONGING",
        "REPAIR_REUSE_RENT",
        "OUTCOME_CERTAINTY",
    }
)

# Backward-compatible import alias. This is intentionally NOT consulted by
# validation or aggregation; callers must treat it as seed vocabulary only.
PSYCHOLOGY_DIMENSIONS = PSYCHOLOGY_SEED_CONCEPTS


def _require_open_concept(value: str) -> str:
    concept = str(value or "").strip()
    if not concept:
        raise ValueError("psychology concept is required")
    return concept


def _require_psychology_primitive(value: str) -> str:
    primitive = str(value or "").strip()
    if primitive not in PSYCHOLOGY_PRIMITIVES:
        raise ValueError(
            "semantic_primitive must be one of PERCEPTION, MOTIVE, or BEHAVIOR"
        )
    return primitive


def _validated_evidence_refs(
    name: str,
    values: Sequence[str],
    *,
    required: bool = False,
) -> tuple[str, ...]:
    if not isinstance(values, (tuple, list)):
        raise ValueError(f"{name} must be a tuple/list of strings")
    refs = tuple(values)
    if any(not isinstance(ref, str) or not ref.strip() for ref in refs):
        raise ValueError(f"{name} must contain non-empty strings")
    if len(refs) != len(set(refs)):
        raise ValueError(f"{name} must be unique")
    if required and not refs:
        raise ValueError(f"{name} is required")
    return refs


@dataclass(frozen=True)
class PsychologySignal:
    signal_id: str
    observed_at: date
    source_date: date
    source_type: str
    source_name: str
    geography: str
    actor_segment: str
    psychology_dimension: str
    direction: float
    intensity: float
    behavior_corroboration: float = 0.0
    money_corroboration: float = 0.0
    representative_sample: bool = False
    representative_share: Optional[float] = None
    sample_size: Optional[int] = None
    provenance_quality: str = "MEDIUM"
    semantic_primitive: str = "PERCEPTION"
    key_evidence_refs: tuple[str, ...] = ()
    behavior_evidence_refs: tuple[str, ...] = ()
    money_evidence_refs: tuple[str, ...] = ()
    representative_evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.source_type not in SOURCE_WEIGHTS:
            raise ValueError(f"unknown source_type: {self.source_type}")
        _require_open_concept(self.psychology_dimension)
        _require_psychology_primitive(self.semantic_primitive)
        key_refs = _validated_evidence_refs(
            "key_evidence_refs", self.key_evidence_refs, required=True
        )
        behavior_refs = _validated_evidence_refs(
            "behavior_evidence_refs", self.behavior_evidence_refs
        )
        money_refs = _validated_evidence_refs(
            "money_evidence_refs", self.money_evidence_refs
        )
        representative_refs = _validated_evidence_refs(
            "representative_evidence_refs", self.representative_evidence_refs
        )
        key_set = set(key_refs)
        for name, refs in (
            ("behavior_evidence_refs", behavior_refs),
            ("money_evidence_refs", money_refs),
            ("representative_evidence_refs", representative_refs),
        ):
            if not set(refs).issubset(key_set):
                raise ValueError(f"{name} must be included in key_evidence_refs")

        if not -1.0 <= self.direction <= 1.0:
            raise ValueError("direction must be between -1.0 and 1.0")
        for name, value in (
            ("intensity", self.intensity),
            ("behavior_corroboration", self.behavior_corroboration),
            ("money_corroboration", self.money_corroboration),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0.0 and 1.0")

        if self.behavior_corroboration > 0 and not behavior_refs:
            raise ValueError(
                "non-zero behavior_corroboration requires behavior_evidence_refs"
            )
        if self.money_corroboration > 0 and not money_refs:
            raise ValueError(
                "non-zero money_corroboration requires money_evidence_refs"
            )

        if self.representative_sample and not representative_refs:
            raise ValueError(
                "representative_sample=True requires representative_evidence_refs"
            )
        if self.representative_share is not None:
            if not self.representative_sample:
                raise ValueError(
                    "representative_share requires representative_sample=True"
                )
            if not 0.0 <= self.representative_share <= 1.0:
                raise ValueError("representative_share must be between 0.0 and 1.0")
            if self.sample_size is None:
                raise ValueError(
                    "representative_share requires an explicit positive sample_size"
                )
        if self.sample_size is not None:
            if self.sample_size <= 0:
                raise ValueError("sample_size must be positive")
            if not self.representative_sample:
                raise ValueError("sample_size requires representative_sample=True")
        if self.provenance_quality not in {"LOW", "MEDIUM", "HIGH"}:
            raise ValueError("provenance_quality must be LOW, MEDIUM, or HIGH")

    @property
    def concept(self) -> str:
        """Open concept namespace alias matching the canonical tracker schema."""

        return self.psychology_dimension


@dataclass(frozen=True)
class PsychologySnapshot:
    geography: str
    actor_segment: str
    psychology_dimension: str
    window_days: int
    signal_count: int
    source_class_count: int
    salience_index: float
    momentum: str
    confidence: str
    behavior_corroboration: float
    money_corroboration: float
    representative_share: Optional[float]
    representative_sample_size: Optional[int]
    semantic_primitive: str = "PERCEPTION"
    supporting_evidence_refs: tuple[str, ...] = ()
    behavior_evidence_refs: tuple[str, ...] = ()
    money_evidence_refs: tuple[str, ...] = ()
    representative_evidence_refs: tuple[str, ...] = ()

    @property
    def concept(self) -> str:
        return self.psychology_dimension


def _as_date(value: date | datetime) -> date:
    return value.date() if isinstance(value, datetime) else value


def _recency_weight(age_days: int, half_life_days: float) -> float:
    if age_days < 0:
        age_days = 0
    return exp(-log(2.0) * age_days / half_life_days)


def _quality_weight(quality: str) -> float:
    return {"LOW": 0.70, "MEDIUM": 0.85, "HIGH": 1.00}[quality]


def _signal_weight(signal: PsychologySignal, as_of: date, half_life_days: float) -> float:
    age = (as_of - signal.source_date).days
    source = SOURCE_WEIGHTS[signal.source_type]
    recency = _recency_weight(age, half_life_days)
    quality = _quality_weight(signal.provenance_quality)

    # Corroboration can increase economic relevance only because non-zero values
    # have already been forced to carry explicit evidence refs by PsychologySignal.
    corroboration = 0.50 + 0.25 * signal.behavior_corroboration + 0.25 * signal.money_corroboration
    return source * recency * quality * corroboration


def _weighted_direction(
    signals: Sequence[PsychologySignal], as_of: date, half_life_days: float
) -> float:
    if not signals:
        return 0.0
    weighted_sum = 0.0
    denominator = 0.0
    for signal in signals:
        weight = _signal_weight(signal, as_of, half_life_days)
        weighted_sum += signal.direction * signal.intensity * weight
        denominator += weight
    if denominator == 0:
        return 0.0
    return max(-1.0, min(1.0, weighted_sum / denominator))


def _weighted_corroboration(
    signals: Sequence[PsychologySignal], field: str, as_of: date, half_life_days: float
) -> float:
    if not signals:
        return 0.0
    weighted_sum = 0.0
    denominator = 0.0
    for signal in signals:
        weight = _signal_weight(signal, as_of, half_life_days)
        weighted_sum += getattr(signal, field) * weight
        denominator += weight
    return 0.0 if denominator == 0 else weighted_sum / denominator


def _unique_refs(signals: Sequence[PsychologySignal], field: str) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                ref
                for signal in signals
                for ref in getattr(signal, field)
            }
        )
    )


def _momentum(
    signals: Sequence[PsychologySignal], as_of: date, window_days: int
) -> str:
    if len(signals) < 2:
        return "INSUFFICIENT_DATA"

    midpoint = max(1, window_days // 2)
    recent = [s for s in signals if 0 <= (as_of - s.source_date).days <= midpoint]
    earlier = [
        s
        for s in signals
        if midpoint < (as_of - s.source_date).days <= window_days
    ]
    if not recent or not earlier:
        return "INSUFFICIENT_DATA"

    half_life = max(7.0, window_days / 2.0)
    recent_value = _weighted_direction(recent, as_of, half_life)
    earlier_value = _weighted_direction(earlier, as_of, half_life)
    delta = recent_value - earlier_value

    if delta >= 0.25:
        return "ACCELERATING"
    if delta >= 0.08:
        return "RISING"
    if delta <= -0.25:
        return "FALLING_FAST"
    if delta <= -0.08:
        return "FALLING"
    return "STABLE"


def _representative_share(
    signals: Sequence[PsychologySignal], as_of: date
) -> tuple[Optional[float], Optional[int]]:
    valid = [
        s
        for s in signals
        if s.representative_sample and s.representative_share is not None
    ]
    if not valid:
        return None, None

    # Do not average incomparable surveys. Expose the most recent defensible estimate.
    latest = max(valid, key=lambda s: (s.source_date, s.observed_at))
    return latest.representative_share, latest.sample_size


def _confidence(
    signals: Sequence[PsychologySignal], behavior: float, money: float
) -> str:
    source_classes = {s.source_type for s in signals}
    has_hard = any(s.source_type == "A_HARD_MONEY_BEHAVIOR" for s in signals)
    has_structured = any(
        s.source_type == "B_REPRESENTATIVE_RESEARCH" for s in signals
    )

    # Social/search-only evidence can never become HIGH confidence.
    if len(source_classes) >= 3 and len(signals) >= 5 and (has_hard or has_structured):
        if behavior >= 0.35 and money >= 0.25:
            return "HIGH"

    if len(source_classes) >= 2 and len(signals) >= 3 and (behavior >= 0.20 or money >= 0.20):
        return "MEDIUM"

    return "LOW"


def aggregate_snapshot(
    signals: Iterable[PsychologySignal],
    *,
    as_of: date | datetime,
    geography: str,
    actor_segment: str,
    psychology_dimension: str,
    window_days: int = 30,
    semantic_primitive: str = "PERCEPTION",
) -> PsychologySnapshot:
    """Aggregate normalized signals into a directional discovery snapshot.

    The named concept is deliberately open-ended. The result is not a population
    estimate unless a representative source explicitly supplies one. Primitive
    filtering prevents a same-named PERCEPTION, MOTIVE and BEHAVIOR concept from
    being silently averaged together. All returned corroboration retains refs to
    the evidence that justified it.
    """

    concept = _require_open_concept(psychology_dimension)
    primitive = _require_psychology_primitive(semantic_primitive)
    if window_days <= 0:
        raise ValueError("window_days must be positive")

    as_of_date = _as_date(as_of)
    selected = [
        s
        for s in signals
        if s.geography == geography
        and s.actor_segment == actor_segment
        and s.psychology_dimension == concept
        and s.semantic_primitive == primitive
        and 0 <= (as_of_date - s.source_date).days <= window_days
    ]

    half_life = max(7.0, window_days / 2.0)
    directional = _weighted_direction(selected, as_of_date, half_life)
    salience = round(directional * 100.0, 2)
    behavior = round(
        _weighted_corroboration(
            selected, "behavior_corroboration", as_of_date, half_life
        ),
        3,
    )
    money = round(
        _weighted_corroboration(
            selected, "money_corroboration", as_of_date, half_life
        ),
        3,
    )
    rep_share, rep_sample_size = _representative_share(selected, as_of_date)

    return PsychologySnapshot(
        geography=geography,
        actor_segment=actor_segment,
        psychology_dimension=concept,
        window_days=window_days,
        signal_count=len(selected),
        source_class_count=len({s.source_type for s in selected}),
        salience_index=salience,
        momentum=_momentum(selected, as_of_date, window_days),
        confidence=_confidence(selected, behavior, money),
        behavior_corroboration=behavior,
        money_corroboration=money,
        representative_share=rep_share,
        representative_sample_size=rep_sample_size,
        semantic_primitive=primitive,
        supporting_evidence_refs=_unique_refs(selected, "key_evidence_refs"),
        behavior_evidence_refs=_unique_refs(selected, "behavior_evidence_refs"),
        money_evidence_refs=_unique_refs(selected, "money_evidence_refs"),
        representative_evidence_refs=_unique_refs(
            selected, "representative_evidence_refs"
        ),
    )
