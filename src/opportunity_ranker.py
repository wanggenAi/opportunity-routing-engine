"""Evidence-gated opportunity scoring for the Opportunity Routing Engine.

This module automates ranking discipline only. It does not manufacture commercial
truth. UNKNOWN never becomes PASS, founder willingness never substitutes for
Delegatability, and a high score cannot bypass transaction or sustainability gates.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping


SCORE_MAXIMA: Dict[str, int] = {
    "pain_severity": 10,
    "frequency_density": 10,
    "payment_evidence": 15,
    "current_solution_weakness": 10,
    "supply_availability": 5,
    "acquisition_route_feasibility": 8,
    "delivery_controllability": 8,
    "delegatability_orchestration_leverage": 10,
    "time_to_first_cash": 8,
    "unit_economics_potential": 5,
    "defensibility_learning": 5,
    "capital_efficiency": 6,
}

TOTAL_MAX = sum(SCORE_MAXIMA.values())
assert TOTAL_MAX == 100

VALID_GATES = {"PASS", "UNKNOWN", "FAIL", "CONDITIONAL"}
REQUIRED_GATES = {"G0", "G1", "G2", "G3", "G4", "G5", "G6"}


@dataclass(frozen=True)
class Evaluation:
    raw_score: int
    penalty_points: int
    final_score: int
    transaction_ready: bool
    scale_ready: bool
    hard_blocked: bool
    strategic_blocked: bool
    band: str
    decision: str
    reason: str


def _validate_scores(scores: Mapping[str, int]) -> None:
    missing = set(SCORE_MAXIMA) - set(scores)
    extra = set(scores) - set(SCORE_MAXIMA)
    if missing or extra:
        raise ValueError(
            f"score keys mismatch; missing={sorted(missing)}, extra={sorted(extra)}"
        )
    for key, max_value in SCORE_MAXIMA.items():
        value = scores[key]
        if not isinstance(value, int):
            raise TypeError(f"{key} must be int")
        if value < 0 or value > max_value:
            raise ValueError(f"{key} must be between 0 and {max_value}")


def _validate_gates(gates: Mapping[str, str]) -> None:
    missing = REQUIRED_GATES - set(gates)
    extra = set(gates) - REQUIRED_GATES
    if missing or extra:
        raise ValueError(
            f"gate keys mismatch; missing={sorted(missing)}, extra={sorted(extra)}"
        )
    for key in REQUIRED_GATES:
        value = gates[key]
        if value not in VALID_GATES:
            raise ValueError(f"invalid {key} gate value: {value}")
    # Only legal/trust/safety supports CONDITIONAL.
    for key in ("G0", "G1", "G2", "G4", "G5", "G6"):
        if gates[key] == "CONDITIONAL":
            raise ValueError(f"{key} cannot be CONDITIONAL")


def evaluate(
    scores: Mapping[str, int],
    gates: Mapping[str, str],
    penalty_points: int = 0,
) -> Evaluation:
    """Evaluate an opportunity without allowing scores to bypass truth gates.

    G0-G3 determine whether a bounded transaction test is ready.
    G4-G6 determine whether it can become a durable orchestration-system wedge.
    G4-G6 may be UNKNOWN during explicit validation but all must PASS before scale.
    """
    _validate_scores(scores)
    _validate_gates(gates)
    if not isinstance(penalty_points, int) or penalty_points < 0:
        raise ValueError("penalty_points must be a non-negative integer")

    raw_score = sum(scores.values())
    final_score = max(0, raw_score - penalty_points)

    hard_blocked = any(gates[g] == "FAIL" for g in ("G0", "G1", "G2", "G3"))
    strategic_blocked = any(gates[g] == "FAIL" for g in ("G4", "G5", "G6"))

    transaction_ready = (
        gates["G0"] == "PASS"
        and gates["G1"] == "PASS"
        and gates["G2"] == "PASS"
        and gates["G3"] in {"PASS", "CONDITIONAL"}
    )
    scale_ready = (
        transaction_ready
        and gates["G4"] == "PASS"
        and gates["G5"] == "PASS"
        and gates["G6"] == "PASS"
    )

    if final_score >= 80:
        band = "A"
    elif final_score >= 65:
        band = "B"
    elif final_score >= 50:
        band = "C"
    else:
        band = "D"

    if hard_blocked:
        decision = "REJECT_OR_REDESIGN"
        reason = "G0-G3 contains FAIL; score cannot override transaction/safety gates."
    elif not transaction_ready:
        decision = "INVESTIGATE"
        reason = "At least one of G0-G3 remains UNKNOWN; UNKNOWN != PASS."
    elif strategic_blocked:
        decision = "REDESIGN_STRATEGIC_FIT"
        reason = "A transaction may work, but G4-G6 contains FAIL; it cannot be the core sustainable orchestration wedge in this form."
    elif band == "A":
        decision = "TEST_NOW"
        if scale_ready:
            reason = "All gates pass and adjusted score is at least 80."
        else:
            reason = "Transaction gates pass and score is at least 80; use the test to resolve remaining G4-G6 orchestration/circulation unknowns."
    elif band == "B":
        decision = "INVESTIGATE"
        reason = "Commercially promising but below TEST_NOW threshold."
    elif band == "C":
        decision = "WATCH_OR_REDESIGN"
        reason = "Relative evidence/economics/orchestration fit are currently weak."
    else:
        decision = "REJECT_OR_DORMANT"
        reason = "Adjusted score is below 50."

    return Evaluation(
        raw_score=raw_score,
        penalty_points=penalty_points,
        final_score=final_score,
        transaction_ready=transaction_ready,
        scale_ready=scale_ready,
        hard_blocked=hard_blocked,
        strategic_blocked=strategic_blocked,
        band=band,
        decision=decision,
        reason=reason,
    )
