import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_050.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan050_tests_six_recurring_outcome_flows_and_promotes_none():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_050"
    assert len(scan["examined_formations"]) == 6
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"

def test_scan050_requires_measurable_outcome_not_tool_build_budget():
    scan = load(SCAN)
    assert "DIRECT_RECURRING_OUTCOME_SPEND" in scan["search_mode"]
    assert "NO_AI_AGENT_BUILD_CONFIGURATION" in scan["search_mode"]
    assert "POST_EXECUTION_MEASURABLE_OUTCOME" in scan["search_mode"]

def test_scan050_all_formations_close_at_control_or_execution_floors():
    scan = load(SCAN)
    assert all(row["verdict"].startswith("DEMOTED_") for row in scan["examined_formations"])
    verdicts = " ".join(row["verdict"] for row in scan["examined_formations"])
    for token in ["DELIVERABILITY", "AMAZON_PPC", "SEO", "CRM", "INVENTORY", "ACQUISITION"]:
        assert token in verdicts

def test_scan051_moves_to_machine_verifiable_replaceable_outcome_units():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_051"
    boundary = scan["next_search_boundary"]
    assert "MACHINE_VERIFIABLE_ACCEPTANCE" in boundary
    assert "REPLACEABLE_EXECUTION" in boundary
    assert "NO_EXTERNAL_ALGORITHM_AS_PRIMARY_SUCCESS_CONTROLLER" in boundary
    assert "NO_SCAN050_VERTICAL_INHERITANCE" in boundary

def test_state_advances_to_scan051_without_new_retention():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_050"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_051"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1"}
