"""Evidence-bound mobilization gate for current-stage opportunity routing.

Reality validity still comes first. This module does not manufacture demand from an
attractive story. It asks a narrower downstream question once a latent connection is
already evidence-bound:

    IF THE MISSING EDGE OPENS, WILL BOTH SIDES MOVE WITH LITTLE FOUNDER PUSH?

The preferred commercial shape is:

    STRONG DEMAND PULL
    + HUNGRY / IDLE SUPPLY
    + ABUNDANT CALLABLE RESOURCE
    + EXISTING PARTIAL FLOW
    + NARROW MISSING EDGE
    + HIGH REACHABILITY
    + LOW ACTIVATION COST
    + CLEAR MONEY FLOW
    + REPEATABILITY
    + ROUTER CAN EXIT THE RECURRING DELIVERY LOOP

Mobilization is not market validation. A high score only means the observed actors
already show enough bilateral pull and self-propulsion to deserve priority after
truth and reachability gates pass.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import prod
from typing import Sequence

from src.missing_edge_gate import ReachabilityGrade


class MobilizationGrade(str, Enum):
    UNASSESSED = "UNASSESSED"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True)
class MobilizationEvidence:
    source_id: str
    claim: str

    def is_usable(self) -> bool:
        return bool(self.source_id.strip() and self.claim.strip())


@dataclass(frozen=True)
class OpportunityMobilizationProfile:
    candidate_id: str
    demand_actor: str
    supply_actor: str
    payer: str
    operator_role: str
    task_unit: str
    money_flow: str
    missing_edge: str

    demand_urgency: int
    supply_hunger: int
    resource_abundance: int
    activation_ease: int
    value_capture: int
    repeatability: int
    self_propulsion: int
    operator_exit: int

    demand_pull_evidence: Sequence[MobilizationEvidence] = field(default_factory=tuple)
    supply_hunger_evidence: Sequence[MobilizationEvidence] = field(default_factory=tuple)
    resource_abundance_evidence: Sequence[MobilizationEvidence] = field(default_factory=tuple)
    activation_evidence: Sequence[MobilizationEvidence] = field(default_factory=tuple)
    value_capture_evidence: Sequence[MobilizationEvidence] = field(default_factory=tuple)
    repeatability_evidence: Sequence[MobilizationEvidence] = field(default_factory=tuple)
    self_propulsion_evidence: Sequence[MobilizationEvidence] = field(default_factory=tuple)
    operator_exit_evidence: Sequence[MobilizationEvidence] = field(default_factory=tuple)

    founder_delivery_required: bool = False
    founder_sales_required_per_transaction: bool = False
    notes: str = ""


_SCORE_EVIDENCE_FIELDS = {
    "demand_urgency": "demand_pull_evidence",
    "supply_hunger": "supply_hunger_evidence",
    "resource_abundance": "resource_abundance_evidence",
    "activation_ease": "activation_evidence",
    "value_capture": "value_capture_evidence",
    "repeatability": "repeatability_evidence",
    "self_propulsion": "self_propulsion_evidence",
    "operator_exit": "operator_exit_evidence",
}

_REQUIRED_TEXT_FIELDS = (
    "candidate_id",
    "demand_actor",
    "supply_actor",
    "payer",
    "operator_role",
    "task_unit",
    "money_flow",
    "missing_edge",
)


def _usable(evidence: Sequence[MobilizationEvidence]) -> list[MobilizationEvidence]:
    return [item for item in evidence if item.is_usable()]


def validate_mobilization(profile: OpportunityMobilizationProfile) -> list[str]:
    """Fail closed when a mobilization score is unsupported by observed evidence."""

    errors: list[str] = []

    for name in _REQUIRED_TEXT_FIELDS:
        value = getattr(profile, name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing:{name}")

    for score_name, evidence_name in _SCORE_EVIDENCE_FIELDS.items():
        score = getattr(profile, score_name)
        if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 3:
            errors.append(f"invalid:{score_name}")
            continue
        if score > 0 and not _usable(getattr(profile, evidence_name)):
            errors.append(f"missing_evidence:{score_name}")

    return errors


def bilateral_pull(profile: OpportunityMobilizationProfile) -> bool:
    """Both sides are already taking observable action toward exchange."""

    return (
        not validate_mobilization(profile)
        and profile.demand_urgency >= 2
        and profile.supply_hunger >= 2
    )


def mobilization_index(profile: OpportunityMobilizationProfile) -> float:
    """Return a 0-100 evidence-backed geometric mobilization index.

    Every core dimension matters. Any zero dimension drives the index to zero rather
    than allowing a large market story to compensate for absent willingness, money
    flow, repeatability or operator exit.
    """

    if validate_mobilization(profile):
        return 0.0

    dimensions = (
        profile.demand_urgency,
        profile.supply_hunger,
        profile.resource_abundance,
        profile.activation_ease,
        profile.value_capture,
        profile.repeatability,
        profile.self_propulsion,
        profile.operator_exit,
    )
    normalized = [value / 3 for value in dimensions]
    return round((prod(normalized) ** (1 / len(normalized))) * 100, 2)


def mobilization_grade(profile: OpportunityMobilizationProfile) -> MobilizationGrade:
    if validate_mobilization(profile):
        return MobilizationGrade.UNASSESSED

    if (
        not bilateral_pull(profile)
        or profile.self_propulsion <= 1
        or profile.value_capture <= 1
        or profile.repeatability <= 1
        or profile.operator_exit <= 1
        or profile.founder_delivery_required
        or profile.founder_sales_required_per_transaction
    ):
        return MobilizationGrade.LOW

    high_floor = (
        profile.demand_urgency,
        profile.supply_hunger,
        profile.resource_abundance,
        profile.activation_ease,
        profile.value_capture,
        profile.repeatability,
        profile.self_propulsion,
        profile.operator_exit,
    )
    if all(value >= 2 for value in high_floor):
        return MobilizationGrade.HIGH

    return MobilizationGrade.MEDIUM


def current_stage_mobilization_priority_allowed(
    profile: OpportunityMobilizationProfile,
    reachability: ReachabilityGrade,
) -> bool:
    """Current-stage priority requires truth-adjacent mobilization and A/B access."""

    return (
        reachability in {ReachabilityGrade.A, ReachabilityGrade.B}
        and mobilization_grade(profile) is MobilizationGrade.HIGH
    )


GOVERNING_INVARIANTS = (
    "REALITY_VALIDITY_PRECEDES_MOBILIZATION",
    "MOBILIZATION_NE_MARKET_VALIDATION",
    "DEMAND_PULL_AND_SUPPLY_HUNGER_BOTH_REQUIRED",
    "OBSERVED_ACTION_NE_THEORETICAL_INTEREST",
    "SELF_PROPULSION_NE_FOUNDER_HUSTLE",
    "FOUNDER_CANNOT_BE_RECURRING_DELIVERY_UNIT",
    "FOUNDER_CANNOT_BE_REQUIRED_SALES_UNIT_PER_TRANSACTION",
    "HIGH_MOBILIZATION_REQUIRES_CLEAR_VALUE_CAPTURE",
    "HIGH_MOBILIZATION_REQUIRES_REPEATABLE_FLOW",
    "HIGH_MOBILIZATION_REQUIRES_OPERATOR_EXIT",
    "CURRENT_STAGE_HIGH_MOBILIZATION_STILL_REQUIRES_REACHABILITY_A_OR_B",
    "UNKNOWN_NE_PASS",
)
