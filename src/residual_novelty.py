"""Fail-closed residual and novelty bridge over source-native observations.

Exact source concepts that do not satisfy ObservedPattern recurrence remain useful
unknowns. This module preserves them as residual atoms and allows two strictly
separate downstream operations:

1. untrusted model cluster suggestions may be evidence-gated, but can only reach
   AWAITING_EXPLICIT_SEMANTIC_REVIEW;
2. explicitly reviewed semantic alignments may be bound back to exact residual
   lineage and assessed by the existing emergent-taxonomy evidence gate.

Neither path promotes taxonomy, creates an ontology version, activates taxonomy,
or creates commercial truth.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Iterable, Mapping, Sequence

from src.emergent_taxonomy import ReviewedConceptAlignment, assess_reviewed_alignment
from src.observation_fabric import ObservationEnvelope
from src.observed_patterns import PatternGate, build_observed_patterns
from src.semantic_kernel import SEMANTIC_PRIMITIVES


RESIDUAL_SCHEMA_VERSION = "residual-novelty.v1"
TAXONOMY_PROMOTION = "NOT_PROMOTED"
BUSINESS_PROMOTION = "NOT_PROMOTED"
MODEL_SUGGESTION_ORIGIN = "MODEL_SUGGESTION"
MODEL_STATES = frozenset({"INSUFFICIENT_EVIDENCE", "AWAITING_EXPLICIT_SEMANTIC_REVIEW"})
REVIEWED_STATES = frozenset({"RESIDUAL", "CANDIDATE", "PROMOTION_REVIEW_READY"})


@dataclass(frozen=True)
class ResidualGate:
    min_observations: int = 4
    min_sources: int = 2
    min_actors: int = 2
    min_periods: int = 2
    min_source_concepts: int = 2

    def __post_init__(self) -> None:
        for name, value in asdict(self).items():
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise ValueError(f"{name} must be an integer >= 1")


@dataclass(frozen=True)
class ResidualAtom:
    residual_id: str
    exact_pattern_id: str
    primitive: str
    concept: str
    geography: str
    exact_pattern_state: str
    claim_count: int
    usable_non_inferred_claim_count: int
    epistemic_counts: Mapping[str, int]
    supporting_claim_refs: tuple[str, ...]
    usable_claim_refs: tuple[str, ...]
    supporting_observation_refs: tuple[str, ...]
    supporting_actor_ids: tuple[str, ...]
    supporting_source_ids: tuple[str, ...]
    supporting_periods: tuple[str, ...]
    missing_pattern_evidence: tuple[str, ...]
    evidence_cautions: tuple[str, ...]
    taxonomy_promotion: str = TAXONOMY_PROMOTION
    business_promotion: str = BUSINESS_PROMOTION

    def __post_init__(self) -> None:
        if self.exact_pattern_state != "UNBOUND":
            raise ValueError("ResidualAtom requires an exact UNBOUND pattern")
        if self.taxonomy_promotion != TAXONOMY_PROMOTION:
            raise ValueError("ResidualAtom cannot promote taxonomy")
        if self.business_promotion != BUSINESS_PROMOTION:
            raise ValueError("ResidualAtom cannot promote business truth")
        if not all((self.residual_id, self.exact_pattern_id, self.primitive, self.concept, self.geography)):
            raise ValueError("residual identity fields are required")

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ModelClusterSuggestion:
    suggestion_id: str
    proposed_concept: str
    primitive: str
    supporting_claim_refs: tuple[str, ...]
    rationale: str
    origin: str = MODEL_SUGGESTION_ORIGIN
    taxonomy_promotion: str = TAXONOMY_PROMOTION
    business_promotion: str = BUSINESS_PROMOTION

    def __post_init__(self) -> None:
        for name in ("suggestion_id", "proposed_concept", "rationale"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} is required")
        if self.primitive not in SEMANTIC_PRIMITIVES:
            raise ValueError(f"unknown semantic primitive: {self.primitive}")
        if not self.supporting_claim_refs:
            raise ValueError("model cluster suggestion requires supporting claim refs")
        if len(self.supporting_claim_refs) != len(set(self.supporting_claim_refs)):
            raise ValueError("supporting claim refs must be unique")
        if self.origin != MODEL_SUGGESTION_ORIGIN:
            raise ValueError("model cluster suggestion origin must remain MODEL_SUGGESTION")
        if self.taxonomy_promotion != TAXONOMY_PROMOTION or self.business_promotion != BUSINESS_PROMOTION:
            raise ValueError("model cluster suggestion cannot promote truth")


@dataclass(frozen=True)
class ModelClusterAssessment:
    suggestion_id: str
    proposed_concept: str
    primitive: str
    state: str
    observation_count: int
    source_count: int
    actor_count: int
    period_count: int
    source_concept_count: int
    epistemic_counts: Mapping[str, int]
    source_concepts: tuple[str, ...]
    source_residual_ids: tuple[str, ...]
    supporting_claim_refs: tuple[str, ...]
    reasons: tuple[str, ...]
    semantic_coherence_state: str = "UNREVIEWED"
    automatic_alignment_creation: bool = False
    taxonomy_promotion: str = TAXONOMY_PROMOTION
    business_promotion: str = BUSINESS_PROMOTION

    def __post_init__(self) -> None:
        if self.state not in MODEL_STATES:
            raise ValueError(f"unsupported model cluster state: {self.state}")
        if self.semantic_coherence_state != "UNREVIEWED":
            raise ValueError("model suggestions cannot self-review semantic coherence")
        if self.automatic_alignment_creation:
            raise ValueError("model suggestion cannot auto-create reviewed alignment")
        if self.taxonomy_promotion != TAXONOMY_PROMOTION or self.business_promotion != BUSINESS_PROMOTION:
            raise ValueError("model cluster assessment cannot promote truth")

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ReviewedResidualCluster:
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
    source_residual_ids: tuple[str, ...]
    supporting_claim_refs: tuple[str, ...]
    definition: str
    boundary: str
    counterexamples: tuple[str, ...]
    alignment_rationale: str
    semantic_coherence_state: str = "EXPLICITLY_REVIEWED"
    taxonomy_promotion: str = TAXONOMY_PROMOTION
    business_promotion: str = BUSINESS_PROMOTION

    def __post_init__(self) -> None:
        if self.state not in REVIEWED_STATES:
            raise ValueError(f"unsupported reviewed cluster state: {self.state}")
        if self.semantic_coherence_state != "EXPLICITLY_REVIEWED":
            raise ValueError("reviewed residual cluster requires explicit semantic review")
        if self.taxonomy_promotion != TAXONOMY_PROMOTION or self.business_promotion != BUSINESS_PROMOTION:
            raise ValueError("reviewed residual cluster cannot promote truth")

    def as_dict(self) -> dict:
        return asdict(self)


def model_cluster_suggestion_from_dict(raw: Mapping[str, object]) -> ModelClusterSuggestion:
    allowed = {"suggestion_id", "proposed_concept", "primitive", "supporting_claim_refs", "rationale"}
    unknown = set(raw) - allowed
    if unknown:
        raise ValueError(f"unknown model cluster suggestion fields: {sorted(unknown)}")
    refs = raw.get("supporting_claim_refs", [])
    if not isinstance(refs, list):
        raise ValueError("supporting_claim_refs must be an array")
    return ModelClusterSuggestion(
        suggestion_id=str(raw.get("suggestion_id") or "").strip(),
        proposed_concept=str(raw.get("proposed_concept") or "").strip(),
        primitive=str(raw.get("primitive") or "").strip(),
        supporting_claim_refs=tuple(str(item).strip() for item in refs if str(item).strip()),
        rationale=str(raw.get("rationale") or "").strip(),
    )


def _claim_geography(envelope: ObservationEnvelope, claim) -> str:
    if claim.geography:
        return claim.geography
    if len(envelope.relevance_geographies) == 1:
        return envelope.relevance_geographies[0]
    return "UNSPECIFIED"


def _claim_actor(envelope: ObservationEnvelope, claim) -> str | None:
    if claim.actor_id:
        return claim.actor_id
    if len(envelope.actor_ids) == 1:
        return envelope.actor_ids[0]
    return None


def _period(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("observation time must be timezone-aware")
    return parsed.date().isoformat()


def _claim_ref(envelope: ObservationEnvelope, claim) -> str:
    return f"{envelope.source_id}::{envelope.observation_id}::{claim.claim_id}"


def _observation_ref(envelope: ObservationEnvelope) -> str:
    return f"{envelope.source_id}::{envelope.observation_id}"


def build_residual_pool(
    envelopes: Iterable[ObservationEnvelope],
    *,
    exact_pattern_gate: PatternGate | None = None,
) -> tuple[ResidualAtom, ...]:
    """Preserve every exact UNBOUND source-native identity with complete claim lineage."""

    current = tuple(envelopes)
    patterns = build_observed_patterns(current, gate=exact_pattern_gate)
    unbound = {
        (item.primitive, item.concept, item.geography): item
        for item in patterns
        if item.state == "UNBOUND"
    }
    groups: dict[tuple[str, str, str], dict[str, object]] = defaultdict(
        lambda: {
            "epistemic_counts": Counter(),
            "all_claim_refs": set(),
            "usable_claim_refs": set(),
            "observation_refs": set(),
            "actors": set(),
            "sources": set(),
            "periods": set(),
        }
    )
    seen_claim_refs: set[str] = set()
    for envelope in current:
        for claim in envelope.claims:
            geography = _claim_geography(envelope, claim)
            key = (claim.primitive, claim.concept, geography)
            if key not in unbound:
                continue
            ref = _claim_ref(envelope, claim)
            if ref in seen_claim_refs:
                continue
            seen_claim_refs.add(ref)
            group = groups[key]
            group["epistemic_counts"][claim.epistemic_status] += 1
            group["all_claim_refs"].add(ref)
            if claim.epistemic_status == "INFERRED":
                continue
            group["usable_claim_refs"].add(ref)
            group["observation_refs"].add(_observation_ref(envelope))
            group["sources"].add(envelope.source_id)
            group["periods"].add(_period(envelope.observed_at))
            actor = _claim_actor(envelope, claim)
            if actor:
                group["actors"].add(actor)

    atoms: list[ResidualAtom] = []
    for key, pattern in unbound.items():
        group = groups[key]
        all_refs = tuple(sorted(group["all_claim_refs"]))
        usable_refs = tuple(sorted(group["usable_claim_refs"]))
        atoms.append(
            ResidualAtom(
                residual_id=f"residual::{pattern.pattern_id}",
                exact_pattern_id=pattern.pattern_id,
                primitive=pattern.primitive,
                concept=pattern.concept,
                geography=pattern.geography,
                exact_pattern_state=pattern.state,
                claim_count=len(all_refs),
                usable_non_inferred_claim_count=len(usable_refs),
                epistemic_counts=dict(sorted(group["epistemic_counts"].items())),
                supporting_claim_refs=all_refs,
                usable_claim_refs=usable_refs,
                supporting_observation_refs=tuple(sorted(group["observation_refs"])),
                supporting_actor_ids=tuple(sorted(group["actors"])),
                supporting_source_ids=tuple(sorted(group["sources"])),
                supporting_periods=tuple(sorted(group["periods"])),
                missing_pattern_evidence=pattern.missing_pattern_evidence,
                evidence_cautions=pattern.evidence_cautions,
            )
        )
    atoms.sort(key=lambda item: (item.primitive, item.concept, item.geography, item.residual_id))
    return tuple(atoms)


def _claim_index(envelopes: Sequence[ObservationEnvelope]) -> dict[str, tuple[ObservationEnvelope, object]]:
    result: dict[str, tuple[ObservationEnvelope, object]] = {}
    for envelope in envelopes:
        for claim in envelope.claims:
            ref = _claim_ref(envelope, claim)
            if ref in result:
                raise ValueError(f"duplicate claim identity: {ref}")
            result[ref] = (envelope, claim)
    return result


def _residual_ref_index(pool: Sequence[ResidualAtom]) -> dict[str, ResidualAtom]:
    result: dict[str, ResidualAtom] = {}
    for atom in pool:
        for ref in atom.supporting_claim_refs:
            if ref in result and result[ref].residual_id != atom.residual_id:
                raise ValueError(f"claim belongs to multiple residual atoms: {ref}")
            result[ref] = atom
    return result


def assess_model_cluster_suggestion(
    suggestion: ModelClusterSuggestion,
    envelopes: Iterable[ObservationEnvelope],
    residual_pool: Sequence[ResidualAtom],
    *,
    gate: ResidualGate | None = None,
) -> ModelClusterAssessment:
    """Evidence-gate an untrusted model grouping without creating reviewed semantics."""

    current = tuple(envelopes)
    active_gate = gate or ResidualGate()
    claims = _claim_index(current)
    residual_refs = _residual_ref_index(residual_pool)
    missing = [ref for ref in suggestion.supporting_claim_refs if ref not in residual_refs]
    if missing:
        raise ValueError(f"model cluster suggestion references non-residual claims: {missing}")

    epistemic_counts: Counter[str] = Counter()
    observation_refs: set[str] = set()
    source_ids: set[str] = set()
    actor_ids: set[str] = set()
    periods: set[str] = set()
    source_concepts: set[str] = set()
    residual_ids: set[str] = set()
    usable_refs: set[str] = set()

    for ref in suggestion.supporting_claim_refs:
        envelope, claim = claims[ref]
        atom = residual_refs[ref]
        if claim.primitive != suggestion.primitive or atom.primitive != suggestion.primitive:
            raise ValueError(f"model cluster primitive mismatch for {ref}")
        epistemic_counts[claim.epistemic_status] += 1
        source_concepts.add(claim.concept)
        residual_ids.add(atom.residual_id)
        if claim.epistemic_status == "INFERRED":
            continue
        usable_refs.add(ref)
        observation_refs.add(_observation_ref(envelope))
        source_ids.add(envelope.source_id)
        periods.add(_period(envelope.observed_at))
        actor = _claim_actor(envelope, claim)
        if actor:
            actor_ids.add(actor)

    reasons: list[str] = []
    if len(observation_refs) < active_gate.min_observations:
        reasons.append("INSUFFICIENT_OBSERVATION_COUNT")
    if len(source_ids) < active_gate.min_sources:
        reasons.append("INSUFFICIENT_SOURCE_DIVERSITY")
    if len(actor_ids) < active_gate.min_actors:
        reasons.append("INSUFFICIENT_ACTOR_DIVERSITY")
    if len(periods) < active_gate.min_periods:
        reasons.append("INSUFFICIENT_TIME_PERSISTENCE")
    if len(source_concepts) < active_gate.min_source_concepts:
        reasons.append("INSUFFICIENT_SOURCE_CONCEPT_DIVERSITY")

    state = "INSUFFICIENT_EVIDENCE" if reasons or not usable_refs else "AWAITING_EXPLICIT_SEMANTIC_REVIEW"
    return ModelClusterAssessment(
        suggestion_id=suggestion.suggestion_id,
        proposed_concept=suggestion.proposed_concept,
        primitive=suggestion.primitive,
        state=state,
        observation_count=len(observation_refs),
        source_count=len(source_ids),
        actor_count=len(actor_ids),
        period_count=len(periods),
        source_concept_count=len(source_concepts),
        epistemic_counts=dict(sorted(epistemic_counts.items())),
        source_concepts=tuple(sorted(source_concepts)),
        source_residual_ids=tuple(sorted(residual_ids)),
        supporting_claim_refs=tuple(sorted(usable_refs)),
        reasons=tuple(reasons),
    )


def bind_reviewed_alignment_to_residual_pool(
    alignment: ReviewedConceptAlignment,
    envelopes: Iterable[ObservationEnvelope],
    residual_pool: Sequence[ResidualAtom],
) -> ReviewedResidualCluster:
    """Bind an explicitly reviewed alignment to exact residual lineage."""

    current = tuple(envelopes)
    residual_refs = _residual_ref_index(residual_pool)
    missing = [ref for ref in alignment.supporting_claim_refs if ref not in residual_refs]
    if missing:
        raise ValueError(f"reviewed alignment references non-residual claims: {missing}")
    assessment = assess_reviewed_alignment(alignment, current)
    residual_ids = {residual_refs[ref].residual_id for ref in alignment.supporting_claim_refs}
    return ReviewedResidualCluster(
        alignment_id=assessment.alignment_id,
        candidate_concept=assessment.candidate_concept,
        primitive=assessment.primitive,
        state=assessment.state,
        observation_count=assessment.observation_count,
        source_count=assessment.source_count,
        actor_count=assessment.actor_count,
        period_count=assessment.period_count,
        epistemic_counts=assessment.epistemic_counts,
        source_concepts=assessment.source_concepts,
        source_residual_ids=tuple(sorted(residual_ids)),
        supporting_claim_refs=assessment.supporting_claim_refs,
        definition=assessment.definition,
        boundary=assessment.boundary,
        counterexamples=assessment.counterexamples,
        alignment_rationale=assessment.alignment_rationale,
    )


def summarize_residual_novelty(
    envelopes: Iterable[ObservationEnvelope],
    *,
    reviewed_alignments: Iterable[ReviewedConceptAlignment] = (),
    model_suggestions: Iterable[ModelClusterSuggestion] = (),
    exact_pattern_gate: PatternGate | None = None,
    suggestion_gate: ResidualGate | None = None,
) -> dict:
    current = tuple(envelopes)
    patterns = build_observed_patterns(current, gate=exact_pattern_gate)
    pool = build_residual_pool(current, exact_pattern_gate=exact_pattern_gate)
    reviewed = tuple(
        bind_reviewed_alignment_to_residual_pool(item, current, pool)
        for item in reviewed_alignments
    )
    suggestions = tuple(
        assess_model_cluster_suggestion(item, current, pool, gate=suggestion_gate)
        for item in model_suggestions
    )

    reviewed_state_counts = Counter(item.state for item in reviewed)
    suggestion_state_counts = Counter(item.state for item in suggestions)
    reviewed_covered_ids = {
        residual_id
        for item in reviewed
        for residual_id in item.source_residual_ids
    }
    suggestion_covered_ids = {
        residual_id
        for item in suggestions
        for residual_id in item.source_residual_ids
    }
    unclustered = tuple(item for item in pool if item.residual_id not in reviewed_covered_ids)
    pattern_state_counts = Counter(item.state for item in patterns)

    return {
        "schema_version": RESIDUAL_SCHEMA_VERSION,
        "source_current_observation_count": len(current),
        "exact_pattern_count": len(patterns),
        "exact_observed_pattern_count": pattern_state_counts.get("OBSERVED_PATTERN", 0),
        "exact_unbound_pattern_count": pattern_state_counts.get("UNBOUND", 0),
        "residual_atom_count": len(pool),
        "reviewed_alignment_count": len(reviewed),
        "reviewed_alignment_state_counts": dict(sorted(reviewed_state_counts.items())),
        "reviewed_clustered_residual_atom_count": len(reviewed_covered_ids),
        "unclustered_residual_atom_count": len(unclustered),
        "model_suggestion_count": len(suggestions),
        "model_suggestion_state_counts": dict(sorted(suggestion_state_counts.items())),
        "model_suggestion_covered_residual_atom_count": len(suggestion_covered_ids),
        "automatic_alignment_creation_count": 0,
        "automatic_taxonomy_promotion_count": 0,
        "active_ontology_changes": 0,
        "taxonomy_promotion": TAXONOMY_PROMOTION,
        "business_promotion": BUSINESS_PROMOTION,
        "residual_atoms": [item.as_dict() for item in pool],
        "reviewed_clusters": [item.as_dict() for item in reviewed],
        "model_cluster_assessments": [item.as_dict() for item in suggestions],
        "unclustered_residuals": [item.as_dict() for item in unclustered],
        "truth_boundaries": [
            "EXACT_UNBOUND_PATTERN_NE_FAILURE",
            "RESIDUAL_ATOM_PRESERVES_SOURCE_NATIVE_CONCEPT",
            "MODEL_CLUSTER_SUGGESTION_NE_REVIEWED_ALIGNMENT",
            "EVIDENCE_GATED_CLUSTER_NE_SEMANTIC_COHERENCE",
            "REVIEWED_ALIGNMENT_NE_TAXONOMY_PROMOTION",
            "TAXONOMY_PROMOTION_REQUIRES_SEPARATE_ONTOLOGY_GOVERNANCE",
            "UNCLUSTERED_RESIDUAL_MUST_REMAIN_VISIBLE",
            "REPORTED_NE_OBSERVED",
            "INFERRED_CLAIM_NE_PROMOTION_EVIDENCE",
            "RESIDUAL_CLUSTER_NE_OPPORTUNITY",
            "UNKNOWN_NE_PASS",
        ],
    }


GOVERNING_INVARIANTS = (
    "SOURCE_NATIVE_CONCEPTS_ARE_IMMUTABLE_INPUTS",
    "EXACT_UNBOUND_PATTERN_NE_FAILURE",
    "MODEL_CLUSTER_SUGGESTION_NE_REVIEWED_ALIGNMENT",
    "MODEL_CLUSTER_SUGGESTION_NE_TAXONOMY",
    "EVIDENCE_GATE_NE_SEMANTIC_COHERENCE",
    "REVIEWED_ALIGNMENT_NE_TAXONOMY_PROMOTION",
    "UNCLUSTERED_RESIDUAL_REMAINS_VISIBLE",
    "INFERRED_CLAIMS_CANNOT_BOOTSTRAP_CLUSTER_READINESS",
    "RESIDUAL_CLUSTER_NE_BUSINESS_OPPORTUNITY",
    "UNKNOWN_NE_PASS",
)
