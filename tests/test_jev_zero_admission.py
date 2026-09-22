from src.jev_research_advisory import (
    JevResearchConfig,
    build_continuation_directive,
    evaluate_research_advisory,
)


def test_authoritative_zero_admission_advances_without_provider_call():
    payload = evaluate_research_advisory(
        states=[],
        config=JevResearchConfig(enabled=True, shadow_mode=True),
        authoritative_zero_admission=True,
    )

    assert payload["execution_status"] == "SUCCESS"
    assert payload["entity_count"] == 0
    assert payload["authoritative_zero_admission"] is True
    assert payload["summary"]["evaluated"] == 0

    directive = build_continuation_directive(payload)
    assert directive["next_action"] == "ADVANCE_TO_NEXT_SCAN"
    assert directive["autonomous_continuation_allowed"] is True
    assert directive["human_intervention_required"] is False
    assert directive["dispatch_items"] == []


def test_unmarked_empty_input_remains_fail_closed():
    payload = evaluate_research_advisory(
        states=[],
        config=JevResearchConfig(enabled=True, shadow_mode=True),
    )

    assert payload["execution_status"] == "FAILED"
    assert payload["entity_count"] == 0
    assert payload["authoritative_zero_admission"] is False

    directive = build_continuation_directive(payload)
    assert directive["next_action"] == "STOP_FOR_HUMAN_REVIEW"
    assert directive["autonomous_continuation_allowed"] is False
    assert directive["human_intervention_required"] is True
