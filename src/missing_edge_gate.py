"""Fail-closed market-gap gate for latent-value formation hypotheses.

A formation hypothesis is not worth field promotion merely because resources are
underused and complementary.  Before a route is selected for field validation the
system must search for already-existing exchange structures and prove that a
material edge is still missing.

Core boundary:

    COMPLEMENTARITY
    + COUNTERFACTUAL EXCHANGE
    != MISSING EDGE

Promotion requires evidence for all three questions:

1. What exchange structures already exist for the same actor/outcome/geography?
2. What material failure remains despite those structures?
3. Why has the market not already closed that failure cheaply enough?

If an observed existing route already solves the target outcome adequately, the
candidate is closed rather than "improved" into a new opportunity narrative.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence


class MissingEdgeState(str, Enum):
    EXISTING_EXCHANGE_SEARCH_REQUIRED = "EXISTING_EXCHANGE_SEARCH_REQUIRED"
    MARKET_ALREADY_CLOSED = "MARKET_ALREADY_CLOSED"
    STRUCTURAL_FAILURE_EVIDENCE_REQUIRED = "STRUCTURAL_FAILURE_EVIDENCE_REQUIRED"
    MISSING_EDGE_HYPOTHESIS = "MISSING_EDGE_HYPOTHESIS"
    VALIDATION_READY = "VALIDATION_READY"


@dataclass(frozen=True)
class MissingEdgeEvidence:
    source_id: str
    claim: str

    def is_usable(self) -> bool:
        return bool(self.source_id.strip() and self.claim.strip())


@dataclass(frozen=True)
class ExistingExchangeRoute:
    route_id: str
    observed_exchange: str
    target_actor_outcome_fit: str
    evidence_refs: tuple[str, ...]
    observed_limitation: str = ""
    adequately_solves_target: bool = False

    def is_usable(self) -> bool:
        return bool(
            self.route_id.strip()
            and self.observed_exchange.strip()
            and self.target_actor_outcome_fit.strip()
            and self.evidence_refs
            and all(isinstance(ref, str) and ref.strip() for ref in self.evidence_refs)
        )


@dataclass(frozen=True)
class MissingEdgeCounterevidence:
    source_id: str
    claim: str
    material: bool = True
    resolved: bool = False

    def is_usable(self) -> bool:
        return bool(self.source_id.strip() and self.claim.strip())


@dataclass(frozen=True)
class MissingEdgeAssessment:
    candidate_id: str
    actor_segment: str
    geography: str
    target_outcome: str
    existing_exchange_search_scope: str
    existing_exchange_search_evidence: Sequence[MissingEdgeEvidence]
    existing_routes: Sequence[ExistingExchangeRoute]
    structural_failure_evidence: Sequence[MissingEdgeEvidence]
    missing_edge_hypothesis: str
    why_market_has_not_already_solved_it: str
    orchestrator_unique_contribution: str
    cheapest_decisive_validation: str
    kill_conditions: str
    counterevidence: Sequence[MissingEdgeCounterevidence] = field(default_factory=tuple)


_REQUIRED_TEXT_FIELDS = (
    "candidate_id",
    "actor_segment",
    "geography",
    "target_outcome",
    "existing_exchange_search_scope",
    "missing_edge_hypothesis",
    "why_market_has_not_already_solved_it",
    "orchestrator_unique_contribution",
    "cheapest_decisive_validation",
    "kill_conditions",
)


def _usable_search_evidence(
    assessment: MissingEdgeAssessment,
) -> list[MissingEdgeEvidence]:
    return [item for item in assessment.existing_exchange_search_evidence if item.is_usable()]


def _usable_failure_evidence(
    assessment: MissingEdgeAssessment,
) -> list[MissingEdgeEvidence]:
    return [item for item in assessment.structural_failure_evidence if item.is_usable()]


def _material_unresolved_counterevidence(
    assessment: MissingEdgeAssessment,
) -> list[MissingEdgeCounterevidence]:
    return [
        item
        for item in assessment.counterevidence
        if item.is_usable() and item.material and not item.resolved
    ]


def _distinct_source_count(evidence: Sequence[MissingEdgeEvidence]) -> int:
    return len({item.source_id.strip() for item in evidence if item.is_usable()})


def validate_missing_edge(assessment: MissingEdgeAssessment) -> list[str]:
    """Return fail-closed errors before missing-edge field validation.

    ``VALIDATION_READY`` means only that a narrow missing-edge hypothesis has
    survived an existing-exchange search and has enough observed structural failure
    to justify a cheap reality test.  It does not establish payer truth, permission,
    transactionability, profit, or repeatability.
    """

    errors: list[str] = []

    for name in _REQUIRED_TEXT_FIELDS:
        value = getattr(assessment, name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing:{name}")

    search_evidence = _usable_search_evidence(assessment)
    if not search_evidence:
        errors.append("missing:existing_exchange_search_evidence")
    elif _distinct_source_count(search_evidence) < 2:
        errors.append("insufficient:existing_exchange_search_independence")

    if not assessment.existing_routes:
        errors.append("missing:existing_routes_or_explicit_no-route-result")
    else:
        for route in assessment.existing_routes:
            if not route.is_usable():
                errors.append(f"invalid:existing_route:{route.route_id or 'UNKNOWN'}")

    if any(
        route.is_usable() and route.adequately_solves_target
        for route in assessment.existing_routes
    ):
        errors.append("market_already_closed")

    failure_evidence = _usable_failure_evidence(assessment)
    if not failure_evidence:
        errors.append("missing:structural_failure_evidence")

    if _material_unresolved_counterevidence(assessment):
        errors.append("unresolved_material_counterevidence")

    return errors


def missing_edge_state(assessment: MissingEdgeAssessment) -> MissingEdgeState:
    search_evidence = _usable_search_evidence(assessment)
    usable_routes = [route for route in assessment.existing_routes if route.is_usable()]

    if _distinct_source_count(search_evidence) < 2 or not usable_routes:
        return MissingEdgeState.EXISTING_EXCHANGE_SEARCH_REQUIRED

    if any(route.adequately_solves_target for route in usable_routes):
        return MissingEdgeState.MARKET_ALREADY_CLOSED

    if not _usable_failure_evidence(assessment):
        return MissingEdgeState.STRUCTURAL_FAILURE_EVIDENCE_REQUIRED

    if _material_unresolved_counterevidence(assessment):
        return MissingEdgeState.MISSING_EDGE_HYPOTHESIS

    if validate_missing_edge(assessment):
        return MissingEdgeState.MISSING_EDGE_HYPOTHESIS

    return MissingEdgeState.VALIDATION_READY


def field_validation_allowed(assessment: MissingEdgeAssessment) -> bool:
    """Whether the missing edge itself is ready for a cheap bounded field test."""

    return missing_edge_state(assessment) is MissingEdgeState.VALIDATION_READY


GOVERNING_INVARIANTS = (
    "COMPLEMENTARITY_NE_MISSING_EDGE",
    "MARKET_SIZE_NE_STRUCTURAL_FAILURE",
    "COMPETITION_NE_OPPORTUNITY",
    "EXISTING_EXCHANGE_SEARCH_REQUIRED_BEFORE_FIELD_PROMOTION",
    "MISSING_EDGE_REQUIRES_OBSERVED_FAILURE_EVIDENCE",
    "ADEQUATE_EXISTING_ROUTE_CLOSES_CANDIDATE",
    "WHY_NOT_ALREADY_SOLVED_REQUIRES_EVIDENCE_NOT_STORY",
    "UNKNOWN_NE_PASS",
)
