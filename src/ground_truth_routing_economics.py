"""Evidence-bound economics screening for Scan 126 ground-truth routing.

Raw buyer/executor price spread is not normalized margin.  This module is
intentionally fail-closed around scope comparability, authorization, access,
travel, QA and rework.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EconomicsDecision(str, Enum):
    REJECT_SPECIALIST_SCOPE = "REJECT_SPECIALIST_SCOPE"
    REJECT_SCOPE_NOT_COMPARABLE = "REJECT_SCOPE_NOT_COMPARABLE"
    REJECT_PRICE_BELOW_EXECUTOR_FLOOR = "REJECT_PRICE_BELOW_EXECUTOR_FLOOR"
    REJECT_NONPOSITIVE_WORST_CASE_HEADROOM = "REJECT_NONPOSITIVE_WORST_CASE_HEADROOM"
    BLOCKED_SUBCONTRACT_AUTHORIZATION = "BLOCKED_SUBCONTRACT_AUTHORIZATION"
    BLOCKED_ACCESS_OR_PRIVACY = "BLOCKED_ACCESS_OR_PRIVACY"
    POSITIVE_HEADROOM_NOT_NORMALIZED = "POSITIVE_HEADROOM_NOT_NORMALIZED"
    BOUNDED_BOOTSTRAP_ECONOMICS_READY = "BOUNDED_BOOTSTRAP_ECONOMICS_READY"


@dataclass(frozen=True)
class TaskEconomicsEvidence:
    buyer_budget_cny: float
    executor_payout_min_cny: float
    executor_payout_max_cny: float
    marketplace_fee_rate_max: float = 0.0

    same_scope_cost_binding: bool = False
    specialist_required: bool = False
    subcontract_path_authorized: bool = False
    access_and_privacy_resolved: bool = False

    travel_cost_max_cny: float | None = None
    qa_rework_cost_max_cny: float | None = None

    def buyer_net_after_marketplace_fee(self) -> float:
        fee = min(1.0, max(0.0, float(self.marketplace_fee_rate_max)))
        return float(self.buyer_budget_cny) * (1.0 - fee)

    def raw_headroom_range(self) -> tuple[float, float]:
        net = self.buyer_net_after_marketplace_fee()
        low = net - float(self.executor_payout_max_cny)
        high = net - float(self.executor_payout_min_cny)
        return (low, high)

    def normalized_worst_case_headroom(self) -> float | None:
        if self.travel_cost_max_cny is None or self.qa_rework_cost_max_cny is None:
            return None
        low, _ = self.raw_headroom_range()
        return low - float(self.travel_cost_max_cny) - float(self.qa_rework_cost_max_cny)


def evaluate_task_economics(evidence: TaskEconomicsEvidence) -> EconomicsDecision:
    """Return the strongest conclusion currently supported by bounded evidence."""

    if evidence.specialist_required:
        return EconomicsDecision.REJECT_SPECIALIST_SCOPE

    if not evidence.same_scope_cost_binding:
        return EconomicsDecision.REJECT_SCOPE_NOT_COMPARABLE

    net = evidence.buyer_net_after_marketplace_fee()
    if net < float(evidence.executor_payout_min_cny):
        return EconomicsDecision.REJECT_PRICE_BELOW_EXECUTOR_FLOOR

    low, _ = evidence.raw_headroom_range()
    if low <= 0:
        return EconomicsDecision.REJECT_NONPOSITIVE_WORST_CASE_HEADROOM

    if not evidence.subcontract_path_authorized:
        return EconomicsDecision.BLOCKED_SUBCONTRACT_AUTHORIZATION

    if not evidence.access_and_privacy_resolved:
        return EconomicsDecision.BLOCKED_ACCESS_OR_PRIVACY

    normalized = evidence.normalized_worst_case_headroom()
    if normalized is None:
        return EconomicsDecision.POSITIVE_HEADROOM_NOT_NORMALIZED

    if normalized <= 0:
        return EconomicsDecision.REJECT_NONPOSITIVE_WORST_CASE_HEADROOM

    return EconomicsDecision.BOUNDED_BOOTSTRAP_ECONOMICS_READY


def ground_truth_economics_boundaries() -> tuple[str, ...]:
    return (
        "RAW_SPREAD_NE_NORMALIZED_MARGIN",
        "SAME_SCOPE_COST_BINDING_REQUIRED",
        "SPECIALIST_SCOPE_REJECTED_FROM_GENERIC_BOOTSTRAP",
        "SUBCONTRACT_PATH_MUST_BE_AUTHORIZED",
        "ACCESS_AND_PRIVACY_MUST_BE_RESOLVED",
        "TRAVEL_QA_REWORK_MUST_BE_BOUNDED_FOR_READY_STATE",
        "PRICE_BELOW_EXECUTOR_FLOOR_REJECTED_EARLY",
        "POSITIVE_WORST_CASE_HEADROOM_REQUIRED",
    )
