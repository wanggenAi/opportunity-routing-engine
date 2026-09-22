import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_078.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan078_requires_executed_non_incumbent_residual_payment_without_mechanism_inheritance():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_078"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_mechanism_as_requirement"] is False
    assert len(scan["examined_formations"]) == 5
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    for formation in scan["examined_formations"]:
        assert formation["evidence_summary"]
        assert formation["buyer_authored_post_live_failure_evidence"]
        assert formation["actual_non_incumbent_recurring_payment_evidence"]
        assert formation["same_outcome_causal_chain"]
        assert formation["non_incumbent_residual_provider_preflight"]
        assert formation["exact_incumbent_preflight"]
        assert formation["founder_independence_check"]
        assert formation["data_action_rights_check"]
        assert formation["normalized_margin_check"]
        assert formation["machine_delegatability_check"]
        assert formation["generic_agent_substitutability_check"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan078_proves_non_incumbent_payment_is_not_white_space():
    scan = load(SCAN)
    learnings = " ".join(scan["scan_learnings"])
    assert "NON_INCUMBENT_PAYMENT_DOES_NOT_ESTABLISH_WHITE_SPACE" in learnings
    assert "DURHAM_MOVEWORKS_SHOWS_DISTINCT_RESIDUAL_PROVIDERS_CAN_BE_ABSORBED_DIRECTLY" in learnings
    assert "SCAN078_ZERO_RETENTION" in learnings


def test_scan078_escalates_to_post_residual_purchase_same_outcome_failure_without_router_ontology():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_079"
    boundary = scan["next_search_boundary"]
    assert "BUYER_AUTHORED_POST_RESIDUAL_PURCHASE_EVIDENCE" in boundary
    assert "SAME_OUTCOME_REMAINS_UNRESOLVED_DESPITE_THAT_PAID_RESIDUAL_LAYER" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert "MULTI_PROVIDER" not in boundary
    assert "ROUTER" not in boundary


def test_scan078_updates_reset_state_without_promoting_commercial_candidate():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_078"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_079"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_079"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
