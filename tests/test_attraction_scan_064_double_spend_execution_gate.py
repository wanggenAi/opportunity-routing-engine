import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_064.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

def test_scan064_uses_parallel_double_spend_as_primary_sensor():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_064"
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert len(scan["examined_formations"]) == 6
    assert "SEPARATE_RECURRING_EXTERNAL_WORKAROUND_SPEND" in scan["search_mode"]

def test_scan064_decomposes_second_spend_not_just_presence_of_money():
    scan = load(SCAN)
    verdicts = {x["formation_id"]: x["verdict"] for x in scan["examined_formations"]}
    assert "STRATEGY_CREATIVE_ATTRIBUTION_ACCOUNTABILITY" in verdicts["ATTRACTION_SCAN_064-F1"]
    assert "24X7_ACCOUNTABILITY" in verdicts["ATTRACTION_SCAN_064-F2"]
    assert "HUMAN_INCIDENT_RESPONSIBILITY" in verdicts["ATTRACTION_SCAN_064-F3"]
    assert "RECURRING_EXPERT_PROCESS_DISCOVERY" in verdicts["ATTRACTION_SCAN_064-F4"]
    assert "BUSINESS_PROCESS_CONTEXT_GOVERNANCE" in verdicts["ATTRACTION_SCAN_064-F5"]
    assert "RECURRING_EXTERNAL_SPEND_GATE_NOT_PROVEN" in verdicts["ATTRACTION_SCAN_064-F6"]

def test_scan065_keeps_economic_signal_and_raises_execution_floor():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_065"
    boundary = scan["next_search_boundary"]
    assert "SEPARATE_RECURRING_EXTERNAL_SPEND_PRIMARILY_FOR_DETERMINISTIC_REPEATABLE_EXECUTION" in boundary
    assert "OBJECTIVE_MACHINE_VERIFIABLE_OUTPUT" in boundary
    assert "BOUNDED_HUMAN_JUDGMENT_AND_LIABILITY" in boundary
    assert "NO_SCAN064_VERTICAL_INHERITANCE" in boundary
    assert "NO_REQUIRED_PRODUCT_SHAPE" in boundary
    assert "FAIL_CLOSED_PROMOTION" in boundary

def test_state_advances_after_scan064():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_064"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_065"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert {x["formation_id"] for x in state["retained_research_formations"]} == {"ATTRACTION_SCAN_015-F1"}
