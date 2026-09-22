import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_072.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan072_is_second_broad_pass_and_closes_all_six():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_072"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_mechanism_as_requirement"] is False
    assert len(scan["examined_formations"]) == 6
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["budget_source_policy"] == "DOWNSTREAM_ROLE_OR_CONTRACT_BUDGET_EVIDENCE_NOT_DISCOVERY_ONTOLOGY"
    for formation in scan["examined_formations"]:
        assert formation["verdict"].startswith("DEMOTED_")
        assert formation["buyer_budget_evidence"]
        assert formation["exact_incumbent_preflight"]
        assert formation["founder_independence_check"]
        assert formation["data_action_rights_check"]
        assert formation["normalized_margin_check"]


def test_scan072_changes_evidence_source_not_mechanism():
    scan = load(SCAN)
    boundary = scan["next_search_boundary"]
    learnings = " ".join(scan["scan_learnings"])
    assert "TWO_POST_RESET_BROAD_ROLE_BUDGET_PASSES_NOW_JUSTIFY_CHANGING_EVIDENCE_SOURCE" in learnings
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_073"
    assert "BUYER_SIDE_NON_ROLE" in boundary
    assert "NO_JOB_POSTING_AS_SOLE_PAYER_EVIDENCE" in boundary
    assert "NO_SELLER_DEFINED_PRODUCTIZED_SERVICE_AS_PRIMARY_SIGNAL" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary


def test_scan072_updates_reset_state_without_promoting_commercial_candidate():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_072"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_073"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_073"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
