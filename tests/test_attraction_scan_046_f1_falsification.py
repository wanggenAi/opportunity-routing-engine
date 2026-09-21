import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "research_runs" / "attraction_scan_046_f1_falsification.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan046_f1_is_demoted_not_promoted():
    result = load(RESULT)
    assert result["formation_id"] == "ATTRACTION_SCAN_046-F1"
    assert result["verdict"].startswith("DEMOTED_")
    assert result["commercial_candidate"] is False
    assert result["retain_for_active_validation"] is False
    assert result["first_external_value_flow"] == "NOT_PROVEN"

def test_paid_signal_does_not_override_structural_kills():
    result = load(RESULT)
    kills = {item["kill"]: item["status"] for item in result["decisive_kills"]}
    assert kills["CURRENT_PAYER_EVIDENCE"] == "PARTIAL_PASS"
    assert kills["SPARSE_SPECIALIZED_SUPPLY"] == "FAIL"
    assert kills["MACHINE_FIRST_FOUNDER_INDEPENDENT_DELIVERY"] == "FAIL"
    assert kills["FAST_PLATFORM_AND_TOOL_ABSORPTION"] == "FAIL"
    assert kills["DISTINCT_COMPOUNDING_OPERATOR_ASSET"] == "FAIL"

def test_state_removes_scan046_f1_from_active_research():
    state = load(STATE)
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    resolved = {item["formation_id"]: item["verdict"] for item in state["resolved_research_formations"]}
    assert "ATTRACTION_SCAN_046-F1" not in retained
    assert resolved["ATTRACTION_SCAN_046-F1"].startswith("DEMOTED_")
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_046-F1"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_047"
