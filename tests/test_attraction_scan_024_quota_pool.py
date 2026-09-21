import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_024.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan024_searches_micro_edges_not_whole_marketplaces():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_024"
    assert scan["search_mode"] == "HIGH_ENERGY_EXISTING_FLOWS_FIND_UNOWNED_MICRO_EDGES_NO_WHOLE_MARKETPLACE_OR_POLICY_PRIOR"
    assert scan["whole_marketplace_allowed"] is False
    assert scan["inherited_active_formation_as_seed"] is False
    assert scan["active_commercial_candidate_promotions"] == []


def test_scan024_retains_only_prepaid_quota_micro_edge_as_research():
    scan = load(SCAN)
    assert scan["retained_research_formations"] == ["ATTRACTION_SCAN_024-F1"]
    f1 = scan["high_attraction_beacons"][0]
    assert f1["formation_id"] == "ATTRACTION_SCAN_024-F1"
    assert f1["mechanism_class"] == "PREPAID_CAPACITY_UTILIZATION_CONTROL"
    assert f1["commercial_candidate"] is False
    assert "EXACT_WILLINGNESS_TO_PAY_FOR_PREPAID_QUOTA_UTILIZATION_CONTROL" in f1["decisive_unknowns"]
    assert "DISTINCT_OPERATOR_ASSET_BEYOND_AN_OPEN_SOURCE_ROUTER_FEATURE" in f1["decisive_unknowns"]


def test_scan024_does_not_relabel_generic_gateway_cost_routing_as_white_space():
    scan = load(SCAN)
    verdicts = {item["title"]: item["verdict"] for item in scan["examined_formations"]}
    assert verdicts["GENERIC_LLM_COST_ROUTER"] == "DEMOTED_MATURE_GATEWAY_CONTROL_SURFACE"
    assert verdicts["CROSS_ORDER_TRAVEL_DISRUPTION_REFUND_ORCHESTRATOR"] == "DEMOTED_PLATFORM_INTERNALIZATION_AND_FRAGMENTED_ACTION_RIGHTS"
    assert verdicts["RENTAL_HOUSING_DEPOSIT_EVIDENCE_ASSISTANT"] == "DEMOTED_REGULATORY_AND_PLATFORM_ABSORPTION"


def test_state_advances_to_scan025_without_commercial_promotion():
    state = load(STATE)
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    assert retained == {
        "ATTRACTION_SCAN_015-F1",
        "ATTRACTION_SCAN_016-F1",
        "ATTRACTION_SCAN_024-F1",
    }
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_024"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_025"
