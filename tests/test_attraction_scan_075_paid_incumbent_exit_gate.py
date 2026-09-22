import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_075.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan075_uses_paid_incumbent_exit_or_replacement_failure_signals():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_075"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_mechanism_as_requirement"] is False
    assert len(scan["examined_formations"]) == 6
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert "PAID_INCUMBENT_EXIT_OR_REPLACEMENT" in scan["payer_evidence_policy"]
    for formation in scan["examined_formations"]:
        assert formation["verdict"].startswith("DEMOTED_")
        assert formation["buyer_exit_evidence"]
        assert formation["exact_replacement_incumbent_preflight"]
        assert formation["founder_independence_check"]
        assert formation["data_action_rights_check"]
        assert formation["normalized_margin_check"]


def test_scan075_escalates_to_post_replacement_separate_residual_spend_not_mechanism():
    scan = load(SCAN)
    boundary = scan["next_search_boundary"]
    learnings = " ".join(scan["scan_learnings"])
    assert "ACTUAL_PAID_INCUMBENT_EXIT_OR_REPLACEMENT_IS_A_MATERIALLY_STRONGER_WHITE_SPACE_SENSOR" in learnings
    assert "THE_NEXT_EVIDENCE_ESCALATION_SHOULD_LOOK_FOR_SEPARATE_RECURRING_PAID_RESIDUAL_SPEND_AFTER_A_REPLACEMENT" in learnings
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_076"
    assert "POST_REPLACEMENT_SEPARATE_RECURRING_PAID_RESIDUAL_SPEND" in boundary
    assert "EXCLUDE_ROUTINE_IMPLEMENTATION_MIGRATION_TRAINING_TRANSITION_SUPPORT" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert "GENERIC_AGENT_SUBSTITUTABILITY_PREFLIGHT" in boundary


def test_scan075_updates_reset_state_without_promoting_commercial_candidate():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_075"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_076"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_076"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
