import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_076.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan076_requires_same_unresolved_outcome_not_merely_post_live_support():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_076"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_mechanism_as_requirement"] is False
    assert len(scan["examined_formations"]) == 6
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    for formation in scan["examined_formations"]:
        assert formation["verdict"].startswith("DEMOTED_")
        assert formation["residual_spend_evidence"]
        assert formation["same_unresolved_outcome_causal_chain"]
        assert formation["exact_incumbent_preflight"]
        assert formation["founder_independence_check"]
        assert formation["data_action_rights_check"]
        assert formation["normalized_margin_check"]
        assert formation["generic_agent_substitutability_check"]


def test_scan076_escalates_to_explicit_buyer_authored_post_replacement_causality():
    scan = load(SCAN)
    boundary = scan["next_search_boundary"]
    learnings = " ".join(scan["scan_learnings"])
    assert "SEPARATE_RECURRING_SPEND_AFTER_PLATFORM_ADOPTION_IS_NOT_ENOUGH" in learnings
    assert "THE_NEXT_EVIDENCE_ESCALATION_SHOULD_REQUIRE_EXPLICIT_BUYER_AUTHORED_PROOF" in learnings
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_077"
    assert "BUYER_AUTHORED_POST_REPLACEMENT_OR_POST_GO_LIVE_UNRESOLVED_OUTCOME_CAUSAL_CHAIN" in boundary
    assert "SEPARATE_RECURRING_PAID_RESIDUAL_CONTRACT" in boundary
    assert "EXCLUDE_STANDARD_OEM_PARTNER_AMS_MAINTENANCE_MONITORING_ENHANCEMENT_TRAINING_TRANSITION" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary


def test_scan076_updates_reset_state_without_promoting_commercial_candidate():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_076"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_077"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_077"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
