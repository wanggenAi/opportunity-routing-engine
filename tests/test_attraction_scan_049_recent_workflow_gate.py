import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_049.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan049_tests_six_recent_paid_workflows_and_promotes_none():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_049"
    assert len(scan["examined_formations"]) == 6
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"

def test_scan049_separates_implementation_budget_from_operator_control():
    scan = load(SCAN)
    verdicts = " ".join(row["verdict"] for row in scan["examined_formations"])
    assert "BROWSER_AGENT" in verdicts
    assert "JOB_APPLICATION" in verdicts
    assert "WHATSAPP" in verdicts
    assert "AI_VIDEO" in verdicts
    assert "AGENTIC_COMMERCE" in verdicts
    assert "DOCUMENT" in verdicts
    assert all(row["verdict"].startswith("DEMOTED_") for row in scan["examined_formations"])

def test_scan049_uses_post_july_boundary_without_inheriting_scan048_verticals():
    scan = load(SCAN)
    assert "SINCE_2026_07_01" in scan["search_mode"]
    assert "NO_SCAN048_VERTICAL_INHERITANCE" in scan["search_mode"]
    assert scan["inherited_active_formation_as_seed"] is False

def test_scan050_moves_from_tool_build_spend_to_recurring_outcome_spend():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_050"
    boundary = scan["next_search_boundary"]
    assert "DIRECT_RECURRING_OUTCOME_SPEND" in boundary
    assert "NO_AI_AGENT_BUILD_CONFIGURATION" in boundary
    assert "INDEPENDENT_NONPLATFORM_ACTION_RIGHT" in boundary

def test_state_advances_to_scan050_without_new_retention():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_049"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_050"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1"}
