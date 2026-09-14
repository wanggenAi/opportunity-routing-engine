from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from src.semantic_kernel import SemanticObservation


@dataclass(frozen=True)
class TaxonomyAssessment:
    concept: str
    state: str
    observation_count: int
    source_count: int
    actor_count: int
    period_count: int
    supporting_observation_ids: tuple[str, ...]
    reasons: tuple[str, ...]


def _period_key(value: str) -> str:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return value.strip()


def assess_emergent_concept(
    concept: str,
    observations: Iterable[SemanticObservation],
    *,
    min_observations: int = 4,
    min_sources: int = 2,
    min_actors: int = 2,
    min_periods: int = 2,
) -> TaxonomyAssessment:
    """Assess whether an open-ended concept is ready for ontology review.

    This function never promotes a concept into canonical truth. It only moves
    repeated unexplained observations from RESIDUAL to CANDIDATE and finally to
    PROMOTION_REVIEW_READY when diversity/persistence gates are met.

    INFERRED semantic claims are deliberately excluded from promotion evidence so
    downstream interpretation cannot bootstrap itself into a taxonomy fact.
    """

    if not concept.strip():
        raise ValueError("concept is required")
    for name, value in {
        "min_observations": min_observations,
        "min_sources": min_sources,
        "min_actors": min_actors,
        "min_periods": min_periods,
    }.items():
        if value < 1:
            raise ValueError(f"{name} must be >= 1")

    matched = tuple(
        item
        for item in observations
        if item.concept == concept and item.epistemic_status != "INFERRED"
    )
    sources = {item.source_id for item in matched}
    actors = {item.actor_id for item in matched if item.actor_id}
    periods = {_period_key(item.observed_at) for item in matched}

    reasons: list[str] = []
    if len(matched) < min_observations:
        reasons.append("INSUFFICIENT_OBSERVATION_COUNT")
    if len(sources) < min_sources:
        reasons.append("INSUFFICIENT_SOURCE_DIVERSITY")
    if len(actors) < min_actors:
        reasons.append("INSUFFICIENT_ACTOR_DIVERSITY")
    if len(periods) < min_periods:
        reasons.append("INSUFFICIENT_TIME_PERSISTENCE")

    if not matched:
        state = "RESIDUAL"
    elif reasons:
        state = "CANDIDATE"
    else:
        state = "PROMOTION_REVIEW_READY"

    return TaxonomyAssessment(
        concept=concept,
        state=state,
        observation_count=len(matched),
        source_count=len(sources),
        actor_count=len(actors),
        period_count=len(periods),
        supporting_observation_ids=tuple(item.observation_id for item in matched),
        reasons=tuple(reasons),
    )
