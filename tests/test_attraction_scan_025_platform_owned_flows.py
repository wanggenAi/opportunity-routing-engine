import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_025.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan025_closes_with_zero_retention():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_025"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["high_attraction_beacons"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_scan025_kills_platform_owned_and_human_delivery_edges():
    scan = load(SCAN)
    verdicts = {item["title"]: item["verdict"] for item in scan["examined_formations"]}
    assert verdicts["INSTANT_RETAIL_STOCKOUT_AND_AFTERSALES_MICRO_ORCHESTRATOR"] == "DEMOTED_PLATFORM_OWNS_ORDER_STOCK_AND_REFUND_ACTION_RAIL"
    assert verdicts["HOME_REPAIR_PRICE_AND_DIAGNOSIS_GUARD"] == "DEMOTED_PLATFORM_GUARANTEE_AND_RECURRING_HUMAN_DIAGNOSIS"
    assert verdicts["PET_CLINIC_PRICE_AND_TRUST_MICRO_EDGE"] == "DEMOTED_EXACT_PROPRIETARY_DATA_INCUMBENT_AND_HUMAN_MEDICAL_DELIVERY"
    assert verdicts["COLLECTIBLES_PRESALE_AUTHENTICITY_AND_FULFILLMENT_GUARD"] == "DEMOTED_TRANSACTION_PLATFORM_WAREHOUSE_AUTHENTICATION_AND_PRICE_DATA_INTERNALIZATION"
    assert verdicts["SHARED_BIKE_OVERCHARGE_REFUND_EDGE"] == "DEMOTED_PLATFORM_BILLING_RIGHTS_AND_GENERIC_COMPLAINT_ASSISTANCE"


def test_state_advances_without_manufacturing_a_candidate():
    state = load(STATE)
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1", "ATTRACTION_SCAN_016-F1"}
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_025"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_026"


def test_scan026_boundary_moves_outside_dominant_consumer_platform_action_loops():
    scan = load(SCAN)
    assert scan["next_search_boundary"] == "HIGH_ENERGY_EXISTING_BUSINESS_FLOWS_OUTSIDE_DOMINANT_TRANSACTION_PLATFORMS_FIND_UNOWNED_MACHINE_STATE"
