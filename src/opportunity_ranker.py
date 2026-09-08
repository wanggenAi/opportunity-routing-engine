"""Evidence-gated opportunity scoring for Opportunity Routing Engine.

This module intentionally automates only ranking discipline, not commercial truth.
UNKNOWN never becomes PASS, and a high numeric score cannot bypass hard gates.
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
    "acquisition_feasibility": 10,
    "delivery_controllability": 10,
    "time_to_first_cash": 10,
    "unit_economics_potential": 5,
    "defensibility_learning": 5,
    "operator_fit": 5,
    "capital_efficiency": 5,
}

TOTAL_MAX = sum(SCORE_MAXIMA.values())
assert TOTAL_MAX == 100

VALID_GATES = {"PASS", "UNKNOWN", "FAIL", "CONDITIONAL"}


@dataclass(frozen=True)
class Evaluation:
    raw_score: int
    penalty_points: int
    final_score: int
    gate_ready: bool
    hard_blocked: bool
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
    required = {"G0", "G1", "G2", "G3"}
    missing = required - set(gates)
    if missing:
        raise ValueError(f"missing hard gates: {sorted(missing)}")

    for key in required:
        value = gates[key]
        if value not in VALID_GATES:
            raise ValueError(f"invalid {key} gate value: {value}")

    # G0–G2 do not support CONDITIONAL in the canonical scorecard.
    for key in ("G0", "G1", "G2"):
        if gates[key] == "CONDITIONAL":
            raise ValueError(f"{key} cannot be CONDITIONAL")


def evaluate(
    scores: Mapping[str, int],
    gates: Mapping[str, str],
    penalty_points: int = 0,
) -> Evaluation:
    """Evaluate one opportunity without allowing scores to bypass hard gates.

    penalty_points is a non-negative integer representing the total penalties already
    justified by the canonical scorecard. The caller must preserve penalty provenance.
    """

    _validate_scores(scores)
    _validate_gates(gates)

    if not isinstance(penalty_points, int) or penalty_points < 0:
        raise ValueError("penalty_points must be a non-negative integer")

    raw_score = sum(scores.values())
    final_score = max(0, raw_score - penalty_points)

    hard_blocked = any(gates[g] == "FAIL" for g in ("G0", "G1", "G2", "G3"))
    gate_ready = (
        gates["G0"] == "PASS"
        and gates["G1"] == "PASS"
        and gates["G2"] == "PASS"
        and gates["G3"] in {"PASS", "CONDITIONAL"}
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
        reason = "At least one hard gate is FAIL; numeric score cannot override it."
    elif not gate_ready:
        decision = "INVESTIGATE"
        reason = "At least one hard gate remains UNKNOWN; UNKNOWN != PASS."
    elif band == "A":
        decision = "TEST_NOW"
        reason = "All hard gates are ready and adjusted score is at least 80."
    elif band == "B":
        decision = "INVESTIGATE"
        reason = "Commercially promising but below TEST_NOW threshold."
    elif band == "C":
        decision = "WATCH"
        reason = "Relative evidence/economics are currently weak."
    else:
        decision = "REJECT_OR_DORMANT"
        reason = "Adjusted score is below 50."

    return Evaluation(
        raw_score=raw_score,
        penalty_points=penalty_points,
        final_score=final_score,
        gate_ready=gate_ready,
        hard_blocked=hard_blocked,
        band=band,
        decision=decision,
        reason=reason,
    )
