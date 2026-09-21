import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_066.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

def test_scan066_requires_two_independent_buyer_signals_and_pre_category_status():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_066"
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert len(scan["examined_formations"]) == 6
    assert "AT_LEAST_TWO_INDEPENDENT_BUYER_SIGNALS" in scan["search_mode"]
    assert "NOT_ALREADY_A_NAMED_MATURE_APP_SAAS_OR_MANAGED_SERVICE_CATEGORY" in scan["search_mode"]
    assert all(len(x["independent_buyer_signals"]) >= 2 for x in scan["examined_formations"])

def test_scan066_distinguishes_problem_signals_from_confirmed_external_money_motion():
    scan = load(SCAN)
    verdicts = {x["formation_id"]: x["verdict"] for x in scan["examined_formations"]}
    assert "CATEGORY_IS_ALREADY_MATURE" in verdicts["ATTRACTION_SCAN_066-F1"]
    assert "EXTERNAL_RECURRING_MONEY_MOTION_NOT_PROVEN" in verdicts["ATTRACTION_SCAN_066-F2"]
    assert "DENSE_MATURE_CATEGORY" in verdicts["ATTRACTION_SCAN_066-F3"]
    assert "EXTERNAL_PAID_UNIT_NOT_PROVEN" in verdicts["ATTRACTION_SCAN_066-F4"]
    assert "CATEGORY_IS_MATURE" in verdicts["ATTRACTION_SCAN_066-F5"]
    assert "RECURRING_SAME_UNIT_NOT_PROVEN" in verdicts["ATTRACTION_SCAN_066-F6"]

def test_scan067_raises_floor_to_two_confirmed_external_money_motions():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_067"
    boundary = scan["next_search_boundary"]
    assert "TWO_INDEPENDENT_CONFIRMED_EXTERNAL_MONEY_MOTIONS" in boundary
    assert "RECURRING_OR_REPEATED_PAYMENT_EVIDENCE" in boundary
    assert "DATA_RIGHTS_PREFLIGHT" in boundary
    assert "FAIL_CLOSED_PROMOTION" in boundary

def test_state_advances_after_scan066():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_066"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_067"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert {x["formation_id"] for x in state["retained_research_formations"]} == {"ATTRACTION_SCAN_015-F1"}
