"""Evidence gate between ontology-review-ready structure and business archetype review.

This module does not score attractiveness and cannot promote a business.  It asks
whether a recurrent latent-value structure has direct evidence for the mechanisms
that would make it commercially repeatable.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping


SCHEMA_VERSION = "structural-commercialization.v1"
DIMENSIONS = (
    "STANDARDIZABILITY",
    "COMPLEMENTARY_ACTOR_STRUCTURE",
    "REGENERATING_EVENT_FLOW",
    "REPEAT_MONETIZATION",
    "COMPOUNDING",
)
DIMENSION_STATES = frozenset({"EVIDENCED", "UNKNOWN", "CONTRADICTED"})
BUSINESS_PROMOTION = "NOT_PROMOTED"


@dataclass(frozen=True)
class CommercialEvidence:
    evidence_id: str
    dimension: str
    source_id: str
    source_url: str
    claim: str
    geography: str
    observed_at: str
    actor_roles: tuple[str, ...] = ()
    event_types: tuple[str, ...] = ()
    payment_basis: str = ""
    economic_exchange_observed: bool = False
    direct_process_specification: bool = False
    outcome_linked_improvement: bool = False
    contradiction: bool = False

    def __post_init__(self) -> None:
        for name in ("evidence_id", "dimension", "source_id", "source_url", "claim", "geography", "observed_at"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} is required")
        if self.dimension not in DIMENSIONS:
            raise ValueError(f"unsupported commercialization dimension: {self.dimension}")
        if self.economic_exchange_observed and not self.payment_basis.strip():
            raise ValueError("observed economic exchange requires payment_basis")

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CommercialDimension:
    state: str
    evidence_refs: tuple[str, ...]
    source_count: int
    rationale: str

    def __post_init__(self) -> None:
        if self.state not in DIMENSION_STATES:
            raise ValueError(f"unsupported dimension state: {self.state}")
        if self.state == "EVIDENCED" and not self.evidence_refs:
            raise ValueError("EVIDENCED dimension requires evidence refs")


@dataclass(frozen=True)
class StructuralCommercializationAssessment:
    candidate_id: str
    candidate_concept: str
    source_taxonomy_state: str
    dimensions: Mapping[str, CommercialDimension]
    commercial_structure_state: str
    missing_dimensions: tuple[str, ...]
    validation_tasks: tuple[dict[str, str], ...]
    business_promotion: str = BUSINESS_PROMOTION
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.source_taxonomy_state != "PROMOTION_REVIEW_READY":
            raise ValueError("commercialization probe requires PROMOTION_REVIEW_READY concept")
        if set(self.dimensions) != set(DIMENSIONS):
            raise ValueError("commercialization dimensions are incomplete")
        if self.business_promotion != BUSINESS_PROMOTION:
            raise ValueError("commercialization probe cannot promote a business")

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def evidence_from_dict(raw: Mapping[str, Any]) -> CommercialEvidence:
    allowed = {
        "evidence_id", "dimension", "source_id", "source_url", "claim", "geography", "observed_at",
        "actor_roles", "event_types", "payment_basis", "economic_exchange_observed",
        "direct_process_specification", "outcome_linked_improvement", "contradiction",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise ValueError(f"unknown commercialization evidence fields: {sorted(unknown)}")
    return CommercialEvidence(
        evidence_id=str(raw.get("evidence_id") or ""),
        dimension=str(raw.get("dimension") or ""),
        source_id=str(raw.get("source_id") or ""),
        source_url=str(raw.get("source_url") or ""),
        claim=str(raw.get("claim") or ""),
        geography=str(raw.get("geography") or ""),
        observed_at=str(raw.get("observed_at") or ""),
        actor_roles=tuple(str(v) for v in raw.get("actor_roles", []) if str(v)),
        event_types=tuple(str(v) for v in raw.get("event_types", []) if str(v)),
        payment_basis=str(raw.get("payment_basis") or ""),
        economic_exchange_observed=bool(raw.get("economic_exchange_observed", False)),
        direct_process_specification=bool(raw.get("direct_process_specification", False)),
        outcome_linked_improvement=bool(raw.get("outcome_linked_improvement", False)),
        contradiction=bool(raw.get("contradiction", False)),
    )


def _dimension_state(dimension: str, items: tuple[CommercialEvidence, ...]) -> CommercialDimension:
    positive = tuple(item for item in items if not item.contradiction)
    negative = tuple(item for item in items if item.contradiction)
    sources = {item.source_id for item in positive}
    refs = tuple(item.evidence_id for item in positive)

    evidenced = False
    rationale = "Evidence is insufficient for this dimension."
    if dimension == "STANDARDIZABILITY":
        evidenced = len(sources) >= 2 and any(item.direct_process_specification for item in positive)
        rationale = "Requires multiple independent cases plus at least one direct reusable process/interface specification."
    elif dimension == "COMPLEMENTARY_ACTOR_STRUCTURE":
        roles = {role for item in positive for role in item.actor_roles}
        evidenced = len(sources) >= 2 and len(roles) >= 3
        rationale = "Requires multiple sources and at least three observed complementary actor roles."
    elif dimension == "REGENERATING_EVENT_FLOW":
        event_types = {event for item in positive for event in item.event_types}
        evidenced = len(sources) >= 2 and len(event_types) >= 2
        rationale = "Requires recurring lifecycle/workflow events from multiple independent sources."
    elif dimension == "REPEAT_MONETIZATION":
        paid = tuple(item for item in positive if item.economic_exchange_observed and item.payment_basis.strip())
        evidenced = len({item.source_id for item in paid}) >= 2
        rationale = "Requires at least two independent sources showing accepted/contracted economic payment bases for the underlying service class."
    elif dimension == "COMPOUNDING":
        improving = tuple(item for item in positive if item.outcome_linked_improvement)
        evidenced = len({item.source_id for item in improving}) >= 2
        rationale = "Requires outcome-linked evidence that accumulated data/templates/trust/rules measurably improve later execution."

    state = "EVIDENCED" if evidenced else ("CONTRADICTED" if negative and not positive else "UNKNOWN")
    return CommercialDimension(state=state, evidence_refs=refs if evidenced else (), source_count=len(sources), rationale=rationale)


def assess_structural_commercialization(
    *,
    candidate_id: str,
    candidate_concept: str,
    source_taxonomy_state: str,
    evidence: Iterable[CommercialEvidence],
) -> StructuralCommercializationAssessment:
    records = tuple(evidence)
    ids = [item.evidence_id for item in records]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate commercialization evidence_id")

    dimensions = {
        dimension: _dimension_state(dimension, tuple(item for item in records if item.dimension == dimension))
        for dimension in DIMENSIONS
    }
    missing = tuple(name for name in DIMENSIONS if dimensions[name].state != "EVIDENCED")

    if not missing:
        structure_state = "ARCHETYPE_REVIEW_READY"
    elif all(dimensions[name].state == "EVIDENCED" for name in DIMENSIONS if name != "COMPOUNDING"):
        structure_state = "STRUCTURE_VALIDATION_READY"
    else:
        structure_state = "STRUCTURE_HYPOTHESIS"

    task_map = {
        "STANDARDIZABILITY": "Find repeated bounded transformation steps and stable acceptance criteria across independent actors.",
        "COMPLEMENTARY_ACTOR_STRUCTURE": "Verify resource owner, transformation/operator and beneficiary/economic counterparty roles in real cases.",
        "REGENERATING_EVENT_FLOW": "Verify a natural lifecycle, workflow or actor behavior that repeatedly emits new events without unrelated founder-led hunting.",
        "REPEAT_MONETIZATION": "Verify repeated accepted service or transaction payment bases rather than budgets, asking prices or unaccepted quotes.",
        "COMPOUNDING": "Measure whether accumulated data, templates, trust, routing, rules or prior outcomes reduce later search, coordination, QA or failure cost, or improve later acceptance.",
    }
    tasks = tuple(
        {"dimension": name, "task": task_map[name]}
        for name in missing
    )
    return StructuralCommercializationAssessment(
        candidate_id=candidate_id,
        candidate_concept=candidate_concept,
        source_taxonomy_state=source_taxonomy_state,
        dimensions=dimensions,
        commercial_structure_state=structure_state,
        missing_dimensions=missing,
        validation_tasks=tasks,
    )


def summarize_assessment(assessment: StructuralCommercializationAssessment, records: Iterable[CommercialEvidence]) -> dict[str, Any]:
    records = tuple(records)
    return {
        **assessment.as_dict(),
        "evidence_count": len(records),
        "source_count": len({item.source_id for item in records}),
        "dimension_counts": dict(sorted(Counter(item.dimension for item in records).items())),
        "governing_invariants": [
            "ONTOLOGY_REVIEW_READINESS_NE_BUSINESS",
            "PROCESS_REPEATABILITY_NE_MARKET_SIZE",
            "CONTRACT_OR_FEE_EVIDENCE_NE_ORCHESTRATOR_FIT",
            "DIGITAL_PLATFORM_NE_COMPOUNDING_PROOF",
            "STRUCTURE_VALIDATION_READY_NE_ROUTE_TESTABLE",
            "UNKNOWN_NE_PASS",
        ],
    }
