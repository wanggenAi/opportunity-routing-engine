"""Bounded founder-manual bootstrap validation.

The project forbids recurring founder acquisition, search and delivery as the steady
state.  That does not imply that the first few transactions must already be fully
automated.  A founder may temporarily coordinate a tiny number of transactions when
the manual work is explicitly a measurement instrument for an already evidenced,
high-attraction formation.

This module prevents "move fast" from becoming an excuse for low-attraction MVPs.

    BOUNDED MANUAL BOOTSTRAP != RECURRING FOUNDER DEPENDENCE
    FIRST 1-3 MANUAL TRANSACTIONS != PERMISSION FOR PERMANENT MANUAL OPERATIONS
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from src.attraction_discovery import (
    AttractionBeaconState,
    AttractionDiscoveryProfile,
    attraction_beacon_state,
)


class BootstrapDecision(str, Enum):
    FORBIDDEN = "FORBIDDEN"
    BOUNDED_VALIDATION_ALLOWED = "BOUNDED_VALIDATION_ALLOWED"


@dataclass(frozen=True)
class BoundedBootstrapPlan:
    formation_id: str
    decisive_unknown: str

    external_demand_evidence_count: int
    external_payment_signal_count: int
    local_executor_supply_evidence_count: int

    buyer_prepayment_or_platform_escrow_available: bool
    standardized_task_brief: bool
    standardized_acceptance_evidence: bool
    executor_replaceability_path: bool

    founder_manual_transaction_cap: int
    founder_manual_day_cap: int
    founder_free_labor_excluded_from_unit_economics: bool

    founder_manufactured_demand: bool = False
    specialist_certification_required: bool = False
    target_state_founder_search_required_per_transaction: bool = False
    target_state_founder_delivery_required_per_transaction: bool = False


def bounded_manual_bootstrap_allowed(
    profile: AttractionDiscoveryProfile,
    plan: BoundedBootstrapPlan,
) -> BootstrapDecision:
    """Allow only a tightly bounded manual bootstrap for a high-attraction target state.

    Manual work in the bootstrap may collect transaction truth, but it cannot be used
    as evidence that founder-independence has already been proven.
    """

    if attraction_beacon_state(profile) is not AttractionBeaconState.HIGH_ATTRACTION_BEACON:
        return BootstrapDecision.FORBIDDEN

    if not plan.formation_id.strip() or not plan.decisive_unknown.strip():
        return BootstrapDecision.FORBIDDEN

    if plan.external_demand_evidence_count < 2:
        return BootstrapDecision.FORBIDDEN
    if plan.external_payment_signal_count < 1:
        return BootstrapDecision.FORBIDDEN
    if plan.local_executor_supply_evidence_count < 2:
        return BootstrapDecision.FORBIDDEN

    if not plan.buyer_prepayment_or_platform_escrow_available:
        return BootstrapDecision.FORBIDDEN
    if not plan.standardized_task_brief:
        return BootstrapDecision.FORBIDDEN
    if not plan.standardized_acceptance_evidence:
        return BootstrapDecision.FORBIDDEN
    if not plan.executor_replaceability_path:
        return BootstrapDecision.FORBIDDEN

    # Bootstrap means tiny and temporary.  Larger caps are operations, not a test.
    if not 1 <= plan.founder_manual_transaction_cap <= 3:
        return BootstrapDecision.FORBIDDEN
    if not 1 <= plan.founder_manual_day_cap <= 14:
        return BootstrapDecision.FORBIDDEN

    if not plan.founder_free_labor_excluded_from_unit_economics:
        return BootstrapDecision.FORBIDDEN
    if plan.founder_manufactured_demand:
        return BootstrapDecision.FORBIDDEN
    if plan.specialist_certification_required:
        return BootstrapDecision.FORBIDDEN

    # The intended steady state itself must remain founder-light.
    if plan.target_state_founder_search_required_per_transaction:
        return BootstrapDecision.FORBIDDEN
    if plan.target_state_founder_delivery_required_per_transaction:
        return BootstrapDecision.FORBIDDEN

    return BootstrapDecision.BOUNDED_VALIDATION_ALLOWED


def bootstrap_truth_boundaries() -> tuple[str, ...]:
    return (
        "BOOTSTRAP_MANUALITY_NE_RECURRING_FOUNDER_DEPENDENCE",
        "MANUAL_BOOTSTRAP_CANNOT_PROVE_FOUNDER_INDEPENDENCE",
        "EXTERNAL_DEMAND_MUST_EXIST_BEFORE_BOOTSTRAP",
        "EXTERNAL_PAYMENT_SIGNAL_REQUIRED",
        "PREPAYMENT_OR_PLATFORM_ESCROW_REQUIRED_BEFORE_LOCAL_EXECUTION",
        "STANDARDIZED_TASK_AND_ACCEPTANCE_EVIDENCE_REQUIRED",
        "EXECUTOR_REPLACEABILITY_PATH_REQUIRED",
        "FOUNDER_FREE_LABOR_MUST_BE_EXCLUDED_FROM_NORMALIZED_ECONOMICS",
        "MAX_THREE_MANUAL_TRANSACTIONS",
        "MAX_FOURTEEN_DAYS",
        "NO_FOUNDER_MANUFACTURED_DEMAND",
        "NO_SPECIALIST_CERTIFICATION_AS_GENERIC_BOOTSTRAP",
        "TARGET_STEADY_STATE_MUST_NOT_REQUIRE_FOUNDER_SEARCH_OR_DELIVERY",
    )
