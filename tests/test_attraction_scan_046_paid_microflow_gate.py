import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_046.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan046_has_six_money_first_formations_and_zero_commercial_promotions():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_046"
    assert len(scan["examined_formations"]) == 6
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"

def test_scan046_retains_only_mcp_migration_for_cheap_falsification():
    scan = load(SCAN)
    assert scan["retained_research_formations"] == ["ATTRACTION_SCAN_046-F1"]
    retained = [row for row in scan["examined_formations"] if row["verdict"] == "RETAINED_FOR_CHEAP_FALSIFICATION"]
    assert len(retained) == 1
    assert retained[0]["formation_id"] == "ATTRACTION_SCAN_046-F1"
    assert "MCP_2026_07_28" in retained[0]["title"]

def test_scan046_closes_paid_but_crowded_or_expert_platformized_flows():
    scan = load(SCAN)
    closed = [row for row in scan["examined_formations"] if row["verdict"].startswith("DEMOTED_")]
    assert len(closed) == 5
    verdicts = " ".join(row["verdict"] for row in closed)
    assert "DENSE" in verdicts or "CROWDED" in verdicts
    assert "EXPERT" in verdicts
    assert "CONTROL_SURFACE" in verdicts

def test_scan046_retained_beacon_is_fail_closed_and_research_only():
    beacon = load(SCAN)["high_attraction_beacons"][0]
    assert beacon["formation_id"] == "ATTRACTION_SCAN_046-F1"
    assert beacon["commercial_candidate"] is False
    assert len(beacon["decisive_unknowns"]) >= 5
    assert "CHEAP_FALSIFY" in beacon["next_action"]

def test_state_advances_to_scan047_and_keeps_zero_active_candidates():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_046"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_047"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    ids = [row["formation_id"] for row in state["retained_research_formations"]]
    assert "ATTRACTION_SCAN_046-F1" in ids

def test_scan047_does_not_inherit_mcp_migration_as_required_search_prior():
    boundary = load(SCAN)["next_search_boundary"]
    assert "NO_MCP_SPEC_MIGRATION" in boundary
    assert "ACTIVE_VERTICAL_INHERITANCE" in boundary
