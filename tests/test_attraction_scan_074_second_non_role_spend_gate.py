import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_074.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan074_is_second_independent_non_role_spend_pass_and_closes_all_six():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_074"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_mechanism_as_requirement"] is False
    assert len(scan["examined_formations"]) == 6
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["payer_evidence_policy"].startswith("SECOND_INDEPENDENT_BUYER_SIDE_NON_ROLE")
    for formation in scan["examined_formations"]:
        assert formation["verdict"].startswith("DEMOTED_")
        assert formation["buyer_non_role_spend_evidence"]
        assert formation["exact_incumbent_preflight"]
        assert formation["founder_independence_check"]
        assert formation["data_action_rights_check"]
        assert formation["normalized_margin_check"]


def test_scan074_changes_evidence_source_after_two_passes_not_mechanism():
    scan = load(SCAN)
    boundary = scan["next_search_boundary"]
    learnings = " ".join(scan["scan_learnings"])
    assert "TWO_INDEPENDENT_NON_ROLE_SPEND_PASSES_NOW_JUSTIFY_CHANGING_THE_EVIDENCE_SOURCE_AGAIN" in learnings
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_075"
    assert "PAID_INCUMBENT_EXIT_REPLACEMENT_NON_RENEWAL_OR_RECOMPETE" in boundary
    assert "EXPLICIT_UNRESOLVED_OPERATIONAL_FAILURE" in boundary
    assert "EXCLUDE_SIMPLE_PRICE_ONLY_DEPRECATION_ONLY_OR_POLICY_ONLY_SWITCHES" in boundary
    assert "NO_PERSISTENT_WORKAROUND_AS_PRIMARY_SIGNAL" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary


def test_scan074_updates_reset_state_without_promoting_commercial_candidate():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_074"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_075"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_075"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
