import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_053.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

def test_scan053_closes_six_exception_queues_without_promotion():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_053"
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"
    rows = scan["examined_formations"]
    assert len(rows) == 6
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_scan053_distinguishes_control_surface_from_expert_tail():
    scan = load(SCAN)
    verdicts = {row["formation_id"]: row["verdict"] for row in scan["examined_formations"]}
    assert "EXACT_REVENUE_RECOVERY_CONTROL_SURFACE" in verdicts["ATTRACTION_SCAN_053-F1"]
    assert "CLIENT_SPECIFIC_INTEGRATION_ENGINEERING" in verdicts["ATTRACTION_SCAN_053-F2"]
    assert "EXTERNAL_CARRIER_ACTION_DEPENDENCE" in verdicts["ATTRACTION_SCAN_053-F3"]
    assert "EXACT_FREIGHT_AUDIT_AND_RESOLUTION_CONTROL_SURFACE" in verdicts["ATTRACTION_SCAN_053-F4"]
    assert "APPROVAL_SECURITY_JUDGMENT" in verdicts["ATTRACTION_SCAN_053-F5"]
    assert "RECURRING_GDS_EXPERT_JUDGMENT" in verdicts["ATTRACTION_SCAN_053-F6"]

def test_scan053_advances_to_single_exception_fixed_remediation():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_054"
    boundary = scan["next_search_boundary"]
    assert "SINGLE_EXCEPTION_CLASS" in boundary
    assert "FIXED_REMEDIATION" in boundary
    assert "OPEN_ACTION_API" in boundary
    assert "DIRECT_ECONOMIC_SETTLEMENT" in boundary

def test_state_advances_after_scan053():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_053"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_054"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    retained = {x["formation_id"] for x in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1"}
