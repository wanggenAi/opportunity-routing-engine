from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Iterable, Mapping

from src.observation_fabric import ObservationEnvelope
from src.semantic_kernel import SEMANTIC_PRIMITIVES, SemanticObservation


TAXONOMY_PROMOTION = "NOT_PROMOTED"
ALIGNMENT_BASIS = "REVIEWED_SEMANTIC_ALIGNMENT"


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


@dataclass(frozen=True)
class ReviewedConceptAlignment:
    """A reviewed grouping hypothesis over source-native concepts.

    The alignment does not rewrite source claims and does not create a canonical
    ontology node. It merely asks whether several differently worded observations
    appear coherent enough to justify ontology promotion *review*.
    """

    alignment_id: str
    candidate_concept: str
    primitive: str
    definition: str
    boundary: str
    counterexamples: tuple[str, ...]
    supporting_claim_refs: tuple[str, ...]
    alignment_rationale: str
    mapping_basis: str = ALIGNMENT_BASIS
    taxonomy_promotion: str = TAXONOMY_PROMOTION

    def __post_init__(self) -> None:
        for name in (
            "alignment_id",
            "candidate_concept",
            "definition",
            "boundary",
            "alignment_rationale",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} is required")
        if self.primitive not in SEMANTIC_PRIMITIVES:
            raise ValueError(f"unknown semantic primitive: {self.primitive}")
        if not self.counterexamples:
            raise ValueError("reviewed concept alignment requires counterexamples")
        if not self.supporting_claim_refs:
            raise ValueError("reviewed concept alignment requires supporting claim refs")
        if len(self.supporting_claim_refs) != len(set(self.supporting_claim_refs)):
            raise ValueError("supporting claim refs must be unique")
        if self.mapping_basis != ALIGNMENT_BASIS:
            raise ValueError("unsupported concept alignment basis")
        if self.taxonomy_promotion != TAXONOMY_PROMOTION:
            raise ValueError("reviewed alignment cannot self-promote taxonomy")


@dataclass(frozen=True)
class AlignedTaxonomyAssessment:
    alignment_id: str
    candidate_concept: str
    primitive: str
    state: str
    observation_count: int
    source_count: int
    actor_count: int
    period_count: int
    epistemic_counts: Mapping[str, int]
    source_concepts: tuple[str, ...]
    supporting_observation_refs: tuple[str, ...]
    supporting_claim_refs: tuple[str, ...]
    supporting_actor_ids: tuple[str, ...]
    supporting_source_ids: tuple[str, ...]
    supporting_periods: tuple[str, ...]
    reasons: tuple[str, ...]
    definition: str
    boundary: str
    counterexamples: tuple[str, ...]
    alignment_rationale: str
    mapping_basis: str = ALIGNMENT_BASIS
    taxonomy_promotion: str = TAXONOMY_PROMOTION
    business_promotion: str = "NOT_PROMOTED"

    def __post_init__(self) -> None:
        if self.state not in {"RESIDUAL", "CANDIDATE", "PROMOTION_REVIEW_READY"}:
            raise ValueError(f"unsupported aligned taxonomy state: {self.state}")
        if self.taxonomy_promotion != TAXONOMY_PROMOTION:
            raise ValueError("aligned taxonomy assessment cannot promote taxonomy")
        if self.business_promotion != "NOT_PROMOTED":
            raise ValueError("aligned taxonomy assessment cannot promote business truth")

    def as_dict(self) -> dict:
        return asdict(self)


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


def _claim_index(envelopes: Iterable[ObservationEnvelope]) -> dict[str, tuple[ObservationEnvelope, object]]:
    result: dict[str, tuple[ObservationEnvelope, object]] = {}
    for envelope in envelopes:
        for claim in envelope.claims:
            ref = f"{envelope.source_id}::{envelope.observation_id}::{claim.claim_id}"
            if ref in result:
                raise ValueError(f"duplicate claim identity: {ref}")
            result[ref] = (envelope, claim)
    return result


def assess_reviewed_alignment(
    alignment: ReviewedConceptAlignment,
    envelopes: Iterable[ObservationEnvelope],
    *,
    min_observations: int = 4,
    min_sources: int = 2,
    min_actors: int = 2,
    min_periods: int = 2,
) -> AlignedTaxonomyAssessment:
    """Assess a reviewed semantic alignment without rewriting source-native claims.

    The caller must explicitly enumerate exact claim refs. Source concepts remain
    immutable. Non-INFERRED claims may support ontology-review readiness, matching
    the existing emergent-taxonomy policy; REPORTED support remains disclosed in
    ``epistemic_counts`` and does not become an OBSERVED recurring pattern.
    """

    for name, value in {
        "min_observations": min_observations,
        "min_sources": min_sources,
        "min_actors": min_actors,
        "min_periods": min_periods,
    }.items():
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be an integer >= 1")

    index = _claim_index(tuple(envelopes))
    missing = [ref for ref in alignment.supporting_claim_refs if ref not in index]
    if missing:
        raise ValueError(f"alignment references unknown claims: {missing}")

    usable: list[tuple[ObservationEnvelope, object, str]] = []
    epistemic_counts: Counter[str] = Counter()
    for ref in alignment.supporting_claim_refs:
        envelope, claim = index[ref]
        if claim.primitive != alignment.primitive:
            raise ValueError(
                f"alignment primitive mismatch for {ref}: {claim.primitive} != {alignment.primitive}"
            )
        epistemic_counts[claim.epistemic_status] += 1
        if claim.epistemic_status == "INFERRED":
            continue
        usable.append((envelope, claim, ref))

    observation_refs = {
        f"{envelope.source_id}::{envelope.observation_id}"
        for envelope, _, _ in usable
    }
    source_ids = {envelope.source_id for envelope, _, _ in usable}
    actors: set[str] = set()
    periods: set[str] = set()
    source_concepts: set[str] = set()
    usable_claim_refs: set[str] = set()
    for envelope, claim, ref in usable:
        source_concepts.add(claim.concept)
        usable_claim_refs.add(ref)
        periods.add(_period_key(envelope.observed_at))
        if claim.actor_id:
            actors.add(claim.actor_id)
        elif len(envelope.actor_ids) == 1:
            actors.add(envelope.actor_ids[0])

    reasons: list[str] = []
    if len(observation_refs) < min_observations:
        reasons.append("INSUFFICIENT_OBSERVATION_COUNT")
    if len(source_ids) < min_sources:
        reasons.append("INSUFFICIENT_SOURCE_DIVERSITY")
    if len(actors) < min_actors:
        reasons.append("INSUFFICIENT_ACTOR_DIVERSITY")
    if len(periods) < min_periods:
        reasons.append("INSUFFICIENT_TIME_PERSISTENCE")

    if not usable:
        state = "RESIDUAL"
    elif reasons:
        state = "CANDIDATE"
    else:
        state = "PROMOTION_REVIEW_READY"

    return AlignedTaxonomyAssessment(
        alignment_id=alignment.alignment_id,
        candidate_concept=alignment.candidate_concept,
        primitive=alignment.primitive,
        state=state,
        observation_count=len(observation_refs),
        source_count=len(source_ids),
        actor_count=len(actors),
        period_count=len(periods),
        epistemic_counts=dict(sorted(epistemic_counts.items())),
        source_concepts=tuple(sorted(source_concepts)),
        supporting_observation_refs=tuple(sorted(observation_refs)),
        supporting_claim_refs=tuple(sorted(usable_claim_refs)),
        supporting_actor_ids=tuple(sorted(actors)),
        supporting_source_ids=tuple(sorted(source_ids)),
        supporting_periods=tuple(sorted(periods)),
        reasons=tuple(reasons),
        definition=alignment.definition,
        boundary=alignment.boundary,
        counterexamples=alignment.counterexamples,
        alignment_rationale=alignment.alignment_rationale,
    )
