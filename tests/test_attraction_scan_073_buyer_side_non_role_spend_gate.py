import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_073.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan073_uses_buyer_side_non_role_spend_and_closes_all_six():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_073"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_mechanism_as_requirement"] is False
    assert len(scan["examined_formations"]) == 6
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["payer_evidence_policy"] == (
        "BUYER_SIDE_NON_ROLE_REPEAT_PURCHASE_PROCUREMENT_AWARD_INVOICE_OR_RENEWAL_EVIDENCE_NOT_DISCOVERY_ONTOLOGY"
    )
    for formation in scan["examined_formations"]:
        assert formation["verdict"].startswith("DEMOTED_")
        assert formation["buyer_non_role_spend_evidence"]
        assert formation["exact_incumbent_preflight"]
        assert formation["founder_independence_check"]
        assert formation["data_action_rights_check"]
        assert formation["normalized_margin_check"]


def test_scan073_keeps_second_pass_broad_instead_of_deriving_mechanism():
    scan = load(SCAN)
    boundary = scan["next_search_boundary"]
    learnings = " ".join(scan["scan_learnings"])
    assert "ONE_BUYER_SIDE_NON_ROLE_SPEND_PASS_IS_NOT_ENOUGH" in learnings
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_074"
    assert "SECOND_FORMATION_DIVERSE_PASS" in boundary
    assert "NO_JOB_POSTING_AS_SOLE_PAYER_EVIDENCE" in boundary
    assert "NO_SELLER_DEFINED_PRODUCTIZED_SERVICE_AS_PRIMARY_SIGNAL" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary


def test_scan073_updates_reset_state_without_promoting_commercial_candidate():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_073"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_074"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_074"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
