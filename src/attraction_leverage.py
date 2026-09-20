"""Fail-closed value-chain leverage gate for scarce external validation.

A real friction can still be commercially weak when it appears after budget, scope,
vendor choice, or most value allocation is already locked. This module prevents the
engine from confusing "observable pain" with "strategically attractive position".

The gate is intentionally categorical rather than a vanity score.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


INTERVENTION_STAGES = frozenset({
    "DISCOVERY",
    "PRE_COMMITMENT",
    "COMMITMENT",
    "EXECUTION",
    "CLOSEOUT",
    "POST_TRANSACTION",
})

DECISION_MOBILITY = frozenset({"OPEN", "PARTIAL", "LOCKED"})

ECONOMIC_PROXIMITY = frozenset({
    "DIRECT_BUDGET_OR_REVENUE",
    "MATERIAL_COST_OR_RISK",
    "TRANSACTION_ENABLEMENT",
    "PROCESS_QUALITY_ONLY",
})

PARTICIPANT_PULL = frozenset({
    "OBSERVED_BILATERAL",
    "OBSERVED_ONE_SIDE",
    "INFERRED_FROM_BEHAVIOR",
    "NONE",
})

ABSENCE_CONSEQUENCE = frozenset({
    "TRANSACTION_BLOCKED",
    "MATERIAL_VALUE_LOSS",
    "MATERIAL_DELAY_OR_REWORK",
    "MINOR_FRICTION",
})

LEVERAGE_STATES = frozenset({
    "VALIDATION_WORTHY",
    "WEAK_DOWNSTREAM",
    "INSUFFICIENT_EVIDENCE",
})


@dataclass(frozen=True)
class AttractionLeverageAssessment:
    intervention_stage: str
    decision_mobility: str
    economic_proximity: str
    participant_pull: str
    absence_consequence: str
    evidence_refs: tuple[str, ...]
    rationale: str = ""

    def __post_init__(self) -> None:
        checks = (
            ("intervention_stage", self.intervention_stage, INTERVENTION_STAGES),
            ("decision_mobility", self.decision_mobility, DECISION_MOBILITY),
            ("economic_proximity", self.economic_proximity, ECONOMIC_PROXIMITY),
            ("participant_pull", self.participant_pull, PARTICIPANT_PULL),
            ("absence_consequence", self.absence_consequence, ABSENCE_CONSEQUENCE),
        )
        for name, value, allowed in checks:
            if value not in allowed:
                raise ValueError(f"unsupported {name}: {value}")
        if not self.evidence_refs or any(not str(ref).strip() for ref in self.evidence_refs):
            raise ValueError("evidence_refs must contain at least one non-empty ref")

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def assess_attraction_leverage(
    assessment: AttractionLeverageAssessment,
) -> dict[str, Any]:
    """Classify whether scarce external validation is worth spending.

    The gate does not prove a business. It only prevents late-stage, low-control
    frictions from consuming validation effort unless absence has a material
    transaction/economic consequence.
    """

    reasons: list[str] = []

    if assessment.participant_pull == "NONE":
        return {
            **assessment.as_dict(),
            "leverage_state": "INSUFFICIENT_EVIDENCE",
            "validation_eligible": False,
            "reasons": ["NO_PARTICIPANT_PULL_SIGNAL"],
        }

    late_stage = assessment.intervention_stage in {"CLOSEOUT", "POST_TRANSACTION"}
    locked = assessment.decision_mobility == "LOCKED"
    weak_economics = assessment.economic_proximity == "PROCESS_QUALITY_ONLY"
    weak_absence = assessment.absence_consequence in {
        "MATERIAL_DELAY_OR_REWORK",
        "MINOR_FRICTION",
    }

    if late_stage and locked:
        reasons.append("VALUE_ALLOCATION_ALREADY_LOCKED")
    if weak_economics:
        reasons.append("NO_DIRECT_ECONOMIC_CONTROL")
    if assessment.absence_consequence == "MINOR_FRICTION":
        reasons.append("ABSENCE_ONLY_CAUSES_MINOR_FRICTION")

    # A closeout/post-transaction position can survive only when it still controls
    # whether value is released or prevents a material economic loss.
    late_stage_override = assessment.absence_consequence in {
        "TRANSACTION_BLOCKED",
        "MATERIAL_VALUE_LOSS",
    } and assessment.economic_proximity in {
        "DIRECT_BUDGET_OR_REVENUE",
        "MATERIAL_COST_OR_RISK",
        "TRANSACTION_ENABLEMENT",
    }

    if (late_stage and locked and not late_stage_override) or (
        weak_economics and weak_absence
    ):
        return {
            **assessment.as_dict(),
            "leverage_state": "WEAK_DOWNSTREAM",
            "validation_eligible": False,
            "reasons": reasons or ["LOW_VALUE_CHAIN_LEVERAGE"],
        }

    if assessment.decision_mobility == "LOCKED" and not late_stage_override:
        return {
            **assessment.as_dict(),
            "leverage_state": "WEAK_DOWNSTREAM",
            "validation_eligible": False,
            "reasons": reasons + ["DECISION_MOBILITY_LOCKED"],
        }

    if assessment.absence_consequence == "MINOR_FRICTION":
        return {
            **assessment.as_dict(),
            "leverage_state": "WEAK_DOWNSTREAM",
            "validation_eligible": False,
            "reasons": reasons,
        }

    return {
        **assessment.as_dict(),
        "leverage_state": "VALIDATION_WORTHY",
        "validation_eligible": True,
        "reasons": [],
    }
