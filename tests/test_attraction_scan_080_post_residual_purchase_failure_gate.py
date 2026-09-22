import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_080.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan080_is_second_independent_same_floor_pass_without_mechanism_inheritance():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_080"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_mechanism_as_requirement"] is False
    assert "SECOND_INDEPENDENT" in scan["search_mode"]
    assert len(scan["examined_formations"]) == 3
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan080_has_strong_post_payment_failure_but_rejects_replacement_control_surface():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    f1 = formations["ATTRACTION_SCAN_080-F1"]
    assert f1["post_residual_same_outcome_causal_chain"].startswith("PASS_STRONG_")
    assert f1["non_incumbent_residual_provider_preflight"].startswith("FAIL_")
    assert "$268,750" in f1["evidence_summary"]


def test_scan080_distinguishes_live_failure_from_distinct_residual_payment_and_negative_control():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    f2 = formations["ATTRACTION_SCAN_080-F2"]
    f3 = formations["ATTRACTION_SCAN_080-F3"]
    assert f2["post_residual_same_outcome_causal_chain"].startswith("PASS_STRONG_")
    assert any("FAIL_EXECUTED_RECURRING_PAYMENT_TO_DISTINCT_RESIDUAL_PROVIDER_NOT_PROVEN" in x for x in f2["actual_non_incumbent_recurring_payment_evidence"])
    assert f3["post_residual_same_outcome_causal_chain"].startswith("FAIL_")
    assert any("FAIL_NO_BUYER_AUTHORED_POST_PURCHASE_SAME_OUTCOME_FAILURE" in x for x in f3["buyer_authored_post_residual_purchase_failure_evidence"])


def test_scan080_resets_discovery_source_after_two_independent_passes_instead_of_deriving_router_ontology():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_081"
    boundary = scan["next_search_boundary"]
    assert "BROAD_CURRENT_REALITY_SOURCE_RESET" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert "NO_JOB_GIG_RFQ_OR_PROCUREMENT_FEED_AS_DISCOVERY_ONTOLOGY" in boundary
    assert "PROVIDER_SWITCH" not in boundary
    assert "MULTI_PROVIDER" not in boundary
    assert "ROUTER" not in boundary


def test_scan080_updates_reset_state_without_promoting_commercial_candidate():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_080"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_080-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_081"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_081"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
