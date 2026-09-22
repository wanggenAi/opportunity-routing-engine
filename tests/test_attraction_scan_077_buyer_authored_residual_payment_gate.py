import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_077.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan077_requires_buyer_authored_post_live_failure_and_actual_residual_payment():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_077"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_mechanism_as_requirement"] is False
    assert len(scan["examined_formations"]) == 6
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    for formation in scan["examined_formations"]:
        assert formation["verdict"].startswith("DEMOTED_")
        assert formation["buyer_authored_post_live_failure_evidence"]
        assert formation["separate_recurring_paid_residual_evidence"]
        assert formation["same_outcome_causal_chain"]
        assert formation["exact_incumbent_preflight"]
        assert formation["founder_independence_check"]
        assert formation["data_action_rights_check"]
        assert formation["normalized_margin_check"]
        assert formation["generic_agent_substitutability_check"]


def test_scan077_distinguishes_real_causal_chain_from_unowned_white_space():
    scan = load(SCAN)
    learnings = " ".join(scan["scan_learnings"])
    assert "BALTIMORE_COUNTY_IS_THE_STRONGEST_SCAN077_EXAMPLE" in learnings
    assert "EVEN_THE_STRONGEST_CHAIN_CAN_STILL_FAIL_WHITE_SPACE" in learnings
    assert "BUDGET_REQUESTS_AND_TOOL_EVALUATION_ARE_NOT_EXTERNAL_VALUE_FLOW" in learnings
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_078"


def test_scan077_escalates_to_actual_non_incumbent_recurring_residual_payment():
    scan = load(SCAN)
    boundary = scan["next_search_boundary"]
    assert "ACTUAL_RECURRING_PAYMENT_TO_A_NON_INCUMBENT_RESIDUAL_PROVIDER_OR_ASSET" in boundary
    assert "REQUIRE_EXECUTED_PAYMENT_NOT_BUDGET_INTENT" in boundary
    assert "EXCLUDE_STANDARD_AMS_OEM_PARTNER_SUPPORT_INTEGRATORS_CONSULTANTS_BPO" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert "MACHINE_DELEGATABILITY" in boundary


def test_scan077_updates_reset_state_without_promoting_commercial_candidate():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_077"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_078"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_078"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
