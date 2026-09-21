import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_052.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

def test_scan052_has_six_formation_diverse_closures_and_no_promotion():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_052"
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"
    rows = scan["examined_formations"]
    assert len(rows) == 6
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_scan052_closes_native_platform_agent_and_human_attestation_traps():
    scan = load(SCAN)
    verdicts = {row["formation_id"]: row["verdict"] for row in scan["examined_formations"]}
    assert "NATIVE_OPEN_DENTAL_ERA_AUTOMATION" in verdicts["ATTRACTION_SCAN_052-F1"]
    assert "AWS_NATIVE_FUNDING_AGENT" in verdicts["ATTRACTION_SCAN_052-F2"]
    assert "EXTERNAL_PLATFORM_POLICY_GATE" in verdicts["ATTRACTION_SCAN_052-F3"]
    assert "RECURRING_RESEARCH" in verdicts["ATTRACTION_SCAN_052-F4"]
    assert "GENERIC_WEB_RESEARCH_AGENT" in verdicts["ATTRACTION_SCAN_052-F5"]
    assert "REGULATED_HUMAN_ATTESTATION" in verdicts["ATTRACTION_SCAN_052-F6"]

def test_scan052_advances_to_cross_system_exception_remediation():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_053"
    assert "CROSS_SYSTEM_ACTION" in scan["next_search_boundary"]
    assert "NOT_PLATFORM_APPROVAL" in scan["next_search_boundary"]
    assert "NOT_REGULATED_SIGNATURE" in scan["next_search_boundary"]

def test_state_advances_after_scan052():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_052"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_053"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    retained = {x["formation_id"] for x in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1"}
