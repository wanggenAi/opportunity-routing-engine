from src.attraction_leverage import (
    AttractionLeverageAssessment,
    assess_attraction_leverage,
)


def test_closeout_process_quality_is_rejected_before_external_validation():
    result = assess_attraction_leverage(
        AttractionLeverageAssessment(
            intervention_stage="CLOSEOUT",
            decision_mobility="LOCKED",
            economic_proximity="PROCESS_QUALITY_ONLY",
            participant_pull="INFERRED_FROM_BEHAVIOR",
            absence_consequence="MATERIAL_DELAY_OR_REWORK",
            evidence_refs=("current-agent-acceptance-flow",),
        )
    )

    assert result["leverage_state"] == "WEAK_DOWNSTREAM"
    assert result["validation_eligible"] is False
    assert "VALUE_ALLOCATION_ALREADY_LOCKED" in result["reasons"]


def test_precommitment_budget_control_can_consume_validation_capital():
    result = assess_attraction_leverage(
        AttractionLeverageAssessment(
            intervention_stage="PRE_COMMITMENT",
            decision_mobility="OPEN",
            economic_proximity="DIRECT_BUDGET_OR_REVENUE",
            participant_pull="OBSERVED_ONE_SIDE",
            absence_consequence="MATERIAL_VALUE_LOSS",
            evidence_refs=("buyer-behavior", "provider-behavior"),
        )
    )

    assert result["leverage_state"] == "VALIDATION_WORTHY"
    assert result["validation_eligible"] is True


def test_late_stage_can_survive_only_if_it_still_controls_value_release():
    result = assess_attraction_leverage(
        AttractionLeverageAssessment(
            intervention_stage="CLOSEOUT",
            decision_mobility="LOCKED",
            economic_proximity="TRANSACTION_ENABLEMENT",
            participant_pull="OBSERVED_BILATERAL",
            absence_consequence="TRANSACTION_BLOCKED",
            evidence_refs=("payment-release-boundary",),
        )
    )

    assert result["leverage_state"] == "VALIDATION_WORTHY"
    assert result["validation_eligible"] is True


def test_no_pull_signal_fails_closed():
    result = assess_attraction_leverage(
        AttractionLeverageAssessment(
            intervention_stage="PRE_COMMITMENT",
            decision_mobility="OPEN",
            economic_proximity="DIRECT_BUDGET_OR_REVENUE",
            participant_pull="NONE",
            absence_consequence="TRANSACTION_BLOCKED",
            evidence_refs=("market-context-only",),
        )
    )

    assert result["leverage_state"] == "INSUFFICIENT_EVIDENCE"
    assert result["validation_eligible"] is False
