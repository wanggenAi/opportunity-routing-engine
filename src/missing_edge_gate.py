"""Fail-closed market-gap and field-access gates for latent-value formation.

A formation hypothesis is not worth field promotion merely because resources are
underused and complementary. Before a route is selected for field validation the
system must search for already-existing exchange structures and prove that a
material edge is still missing.

For the current P0 (first external truth), a second distinction also matters:

    IMPORTANT / NOVEL HYPOTHESIS != GOOD FIRST FIELD ROUTE

A candidate can remain intellectually valid while being a poor first probe because
truth requires enterprise procurement, proprietary data, large capital, a prior
contract, or other heavy permission. P0 therefore prefers directly observable,
reachable actor classes whose first falsification can be run cheaply and lawfully.
This is a routing priority rule, not a claim that hard-access markets lack value.

Core boundaries:

    COMPLEMENTARITY + COUNTERFACTUAL EXCHANGE != MISSING EDGE
    MISSING EDGE != P0 FIELD ACCESS
    HIGH ACCESS FRICTION != BAD LONG-TERM OPPORTUNITY

Missing-edge promotion requires evidence for all three questions:

1. What exchange structures already exist for the same actor/outcome/geography?
2. What material failure remains despite those structures?
3. Why has the market not already closed that failure cheaply enough?

P0 field priority additionally asks:

4. Can the first decisive observation reach real actors without proprietary data,
   enterprise procurement, large capital, sensitive dossiers, or a pre-existing
   commercial contract?

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


class FieldAccessState(str, Enum):
    """Practical accessibility of the first decisive field probe."""

    ACCESS_EVIDENCE_REQUIRED = "ACCESS_EVIDENCE_REQUIRED"
    DIRECTLY_TESTABLE = "DIRECTLY_TESTABLE"
    MEDIATED_TESTABLE = "MEDIATED_TESTABLE"
    HIGH_FRICTION_DEFER = "HIGH_FRICTION_DEFER"


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


@dataclass(frozen=True)
class FieldAccessProfile:
    """Evidence-bound P0 accessibility profile.

    This profile does not score market quality. It answers only whether the current
    system can cheaply touch reality for the *first* decisive probe.

    `reachable_actor_class` means real members of the actor class can be reached
    through ordinary lawful channels; it does not mean any individual has consented.
    `observable_without_proprietary_access` means the first hypothesis-killing facts
    can be observed without requesting trade secrets, private datasets, credentials,
    or internal production systems.
    """

    candidate_id: str
    actor_segment: str
    first_probe_description: str
    access_evidence: Sequence[MissingEdgeEvidence]
    reachable_actor_class: bool
    observable_without_proprietary_access: bool
    requires_enterprise_procurement: bool = False
    requires_proprietary_data: bool = False
    requires_large_capital: bool = False
    requires_sensitive_personal_data: bool = False
    requires_preexisting_contract: bool = False
    intermediary_required: bool = False
    notes: str = ""


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


_FIELD_ACCESS_REQUIRED_TEXT_FIELDS = (
    "candidate_id",
    "actor_segment",
    "first_probe_description",
)


def _usable_search_evidence(
    assessment: MissingEdgeAssessment,
) -> list[MissingEdgeEvidence]:
    return [item for item in assessment.existing_exchange_search_evidence if item.is_usable()]


def _usable_failure_evidence(
    assessment: MissingEdgeAssessment,
) -> list[MissingEdgeEvidence]:
    return [item for item in assessment.structural_failure_evidence if item.is_usable()]


def _usable_access_evidence(profile: FieldAccessProfile) -> list[MissingEdgeEvidence]:
    return [item for item in profile.access_evidence if item.is_usable()]


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
    to justify a cheap reality test. It does not establish payer truth, permission,
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


def validate_field_access(profile: FieldAccessProfile) -> list[str]:
    """Validate that P0 access claims are evidence-bound rather than convenient story."""

    errors: list[str] = []
    for name in _FIELD_ACCESS_REQUIRED_TEXT_FIELDS:
        value = getattr(profile, name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing:{name}")

    if not _usable_access_evidence(profile):
        errors.append("missing:field_access_evidence")

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


def field_access_state(profile: FieldAccessProfile) -> FieldAccessState:
    """Classify first-probe friction without ranking long-term market value."""

    if validate_field_access(profile):
        return FieldAccessState.ACCESS_EVIDENCE_REQUIRED

    hard_access_requirements = (
        profile.requires_enterprise_procurement,
        profile.requires_proprietary_data,
        profile.requires_large_capital,
        profile.requires_sensitive_personal_data,
        profile.requires_preexisting_contract,
    )
    if any(hard_access_requirements):
        return FieldAccessState.HIGH_FRICTION_DEFER

    if not profile.reachable_actor_class:
        return FieldAccessState.HIGH_FRICTION_DEFER

    if not profile.observable_without_proprietary_access:
        return FieldAccessState.HIGH_FRICTION_DEFER

    if profile.intermediary_required:
        return FieldAccessState.MEDIATED_TESTABLE

    return FieldAccessState.DIRECTLY_TESTABLE


def field_validation_allowed(assessment: MissingEdgeAssessment) -> bool:
    """Whether the missing edge itself is ready for a cheap bounded field test."""

    return missing_edge_state(assessment) is MissingEdgeState.VALIDATION_READY


def p0_access_priority_allowed(profile: FieldAccessProfile) -> bool:
    """Whether a candidate is practical for the current first-truth P0."""

    return field_access_state(profile) in {
        FieldAccessState.DIRECTLY_TESTABLE,
        FieldAccessState.MEDIATED_TESTABLE,
    }


def p0_field_validation_allowed(
    assessment: MissingEdgeAssessment,
    profile: FieldAccessProfile,
) -> bool:
    """Combined truth + access gate for P0 field execution."""

    if assessment.candidate_id != profile.candidate_id:
        return False
    return field_validation_allowed(assessment) and p0_access_priority_allowed(profile)


GOVERNING_INVARIANTS = (
    "COMPLEMENTARITY_NE_MISSING_EDGE",
    "MARKET_SIZE_NE_STRUCTURAL_FAILURE",
    "COMPETITION_NE_OPPORTUNITY",
    "EXISTING_EXCHANGE_SEARCH_REQUIRED_BEFORE_FIELD_PROMOTION",
    "MISSING_EDGE_REQUIRES_OBSERVED_FAILURE_EVIDENCE",
    "ADEQUATE_EXISTING_ROUTE_CLOSES_CANDIDATE",
    "WHY_NOT_ALREADY_SOLVED_REQUIRES_EVIDENCE_NOT_STORY",
    "MISSING_EDGE_NE_P0_FIELD_ACCESS",
    "HIGH_ACCESS_FRICTION_NE_BAD_LONG_TERM_OPPORTUNITY",
    "P0_PREFERS_OBSERVABLE_REACHABLE_LOW_PERMISSION_VALIDATION",
    "FIELD_ACCESS_CLAIM_REQUIRES_EVIDENCE",
    "UNKNOWN_NE_PASS",
)
