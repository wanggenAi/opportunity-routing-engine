import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_055.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

def test_scan055_closes_six_non_recovery_state_transitions_without_promotion():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_055"
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"
    rows = scan["examined_formations"]
    assert len(rows) == 6
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_scan055_distinguishes_native_control_from_low_unit_economics():
    scan = load(SCAN)
    verdicts = {row["formation_id"]: row["verdict"] for row in scan["examined_formations"]}
    assert "SAAS_MANAGEMENT_CONTROL_SURFACE" in verdicts["ATTRACTION_SCAN_055-F1"]
    assert "KUBERNETES_OPTIMIZATION_CONTROL_SURFACE" in verdicts["ATTRACTION_SCAN_055-F2"]
    assert "REVENUE_MANAGEMENT_CONTROL_SURFACE" in verdicts["ATTRACTION_SCAN_055-F3"]
    assert "POS_TO_DELIVERY_MENU_CONTROL_SURFACE" in verdicts["ATTRACTION_SCAN_055-F4"]
    assert "LOW_UNIT_ECONOMICS" in verdicts["ATTRACTION_SCAN_055-F5"]
    assert "RATE_SHOP_AND_LABEL_CONTROL_SURFACE" in verdicts["ATTRACTION_SCAN_055-F6"]

def test_scan055_advances_to_external_trigger_boundary():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_056"
    boundary = scan["next_search_boundary"]
    assert "EXTERNAL_EVENT_TRIGGER" in boundary
    assert "BUYER_OWNED_FIXED_STATE_TRANSITION" in boundary
    assert "STANDARDIZED_TRIGGER_ACTION_MAPPING" in boundary
    assert "NO_SAME_VENDOR_NATIVE_OBSERVABILITY" in boundary

def test_state_advances_after_scan055():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_055"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_056"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    retained = {x["formation_id"] for x in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1"}
