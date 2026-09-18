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
    LOW_REACHABILITY_DEFER = "LOW_REACHABILITY_DEFER"
    HIGH_FRICTION_DEFER = "HIGH_FRICTION_DEFER"


class ReachabilityGrade(str, Enum):
    """Current-stage reality-contact quality, not market attractiveness."""

    UNASSESSED = "UNASSESSED"
    A = "A"
    B = "B"
    C = "C"
    D = "D"


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

    # REACHABILITY GATE — required before P0 promotion. These fields answer:
    # "If we validate tomorrow, where do we go, who do we contact, and can one
    # bounded reality probe happen without burning founder time/capital?"
    named_actor: str = ""
    location: str = ""
    public_contact_route: str = ""
    physical_access_route: str = ""
    decision_maker_distance: str = ""
    permission_level: str = ""
    capital_required_before_contact: float | int | None = None
    can_contact_within_24h: bool = False
    can_physically_verify_within_72h: bool = False
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
    "named_actor",
    "location",
    "public_contact_route",
    "physical_access_route",
    "decision_maker_distance",
    "permission_level",
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

    if not isinstance(profile.can_contact_within_24h, bool):
        errors.append("invalid:can_contact_within_24h")
    if not isinstance(profile.can_physically_verify_within_72h, bool):
        errors.append("invalid:can_physically_verify_within_72h")

    capital = profile.capital_required_before_contact
    if not isinstance(capital, (int, float)) or isinstance(capital, bool) or capital < 0:
        errors.append("invalid:capital_required_before_contact")

    distance = profile.decision_maker_distance.strip().upper()
    if distance not in {"DIRECT", "ONE_HOP", "MULTI_HOP", "UNKNOWN"}:
        errors.append("invalid:decision_maker_distance")

    permission = profile.permission_level.strip().upper()
    if permission not in {"LOW", "MEDIUM", "HIGH"}:
        errors.append("invalid:permission_level")

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


def _is_xuzhou(location: str) -> bool:
    text = location.strip().upper()
    return "徐州" in location or "XUZHOU" in text or "CN-JS-XZ" in text


def _is_jiangsu(location: str) -> bool:
    text = location.strip().upper()
    return _is_xuzhou(location) or "江苏" in location or "JIANGSU" in text or "CN-JS" in text


def reachability_grade(profile: FieldAccessProfile) -> ReachabilityGrade:
    """Derive A-D reachability from concrete actor/contact/permission facts.

    This is deliberately a current-stage routing gate. It does not rank the market
    and it does not mutate the underlying missing-edge truth.
    """

    if validate_field_access(profile):
        return ReachabilityGrade.UNASSESSED

    hard_access_requirements = (
        profile.requires_enterprise_procurement,
        profile.requires_proprietary_data,
        profile.requires_large_capital,
        profile.requires_sensitive_personal_data,
        profile.requires_preexisting_contract,
    )
    permission = profile.permission_level.strip().upper()
    distance = profile.decision_maker_distance.strip().upper()

    if (
        any(hard_access_requirements)
        or permission == "HIGH"
        or not profile.reachable_actor_class
        or not profile.observable_without_proprietary_access
    ):
        return ReachabilityGrade.D

    if (
        _is_xuzhou(profile.location)
        and profile.can_contact_within_24h
        and profile.can_physically_verify_within_72h
        and permission == "LOW"
        and distance in {"DIRECT", "ONE_HOP"}
        and profile.capital_required_before_contact == 0
        and not profile.intermediary_required
    ):
        return ReachabilityGrade.A

    if (
        _is_jiangsu(profile.location)
        and profile.can_contact_within_24h
        and permission in {"LOW", "MEDIUM"}
        and distance in {"DIRECT", "ONE_HOP"}
    ):
        return ReachabilityGrade.B

    return ReachabilityGrade.C


def field_access_state(profile: FieldAccessProfile) -> FieldAccessState:
    """Classify first-probe friction without ranking long-term market value."""

    if validate_field_access(profile):
        return FieldAccessState.ACCESS_EVIDENCE_REQUIRED

    grade = reachability_grade(profile)
    if grade is ReachabilityGrade.D:
        return FieldAccessState.HIGH_FRICTION_DEFER
    if grade is ReachabilityGrade.C:
        return FieldAccessState.LOW_REACHABILITY_DEFER

    if profile.intermediary_required:
        return FieldAccessState.MEDIATED_TESTABLE

    return FieldAccessState.DIRECTLY_TESTABLE


def field_validation_allowed(assessment: MissingEdgeAssessment) -> bool:
    """Whether the missing edge itself is ready for a cheap bounded field test."""

    return missing_edge_state(assessment) is MissingEdgeState.VALIDATION_READY


def p0_access_priority_allowed(profile: FieldAccessProfile) -> bool:
    """Whether a candidate is practical for the current first-truth P0.

    Current-stage promotion requires both a testable access state and Reachability
    Grade A/B. Grade C is preserved as a lower-priority observation candidate; Grade
    D is deferred/closed from P0 execution unless new access evidence changes it.
    """

    return (
        reachability_grade(profile) in {ReachabilityGrade.A, ReachabilityGrade.B}
        and field_access_state(profile)
        in {
            FieldAccessState.DIRECTLY_TESTABLE,
            FieldAccessState.MEDIATED_TESTABLE,
        }
    )


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
    "REACHABILITY_IS_PART_OF_CURRENT_STAGE_OPPORTUNITY_QUALITY",
    "P0_REQUIRES_NAMED_ACTOR_AND_CONCRETE_CONTACT_ROUTE",
    "P0_REQUIRES_REACHABILITY_GRADE_A_OR_B",
    "FIELD_ACCESS_CLAIM_REQUIRES_EVIDENCE",
    "UNKNOWN_NE_PASS",
)
