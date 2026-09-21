import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_047.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan047_tests_six_paid_flows_and_promotes_none():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_047"
    assert len(scan["examined_formations"]) == 6
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"

def test_scan047_all_formations_close_at_hard_floors():
    scan = load(SCAN)
    assert all(row["verdict"].startswith("DEMOTED_") for row in scan["examined_formations"])
    verdicts = " ".join(row["verdict"] for row in scan["examined_formations"])
    assert "CONTROL_SURFACE" in verdicts
    assert "ACTION_RIGHTS" in verdicts
    assert "EXPERT" in verdicts

def test_scan047_advances_without_inheriting_examined_verticals():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_048"
    boundary = scan["next_search_boundary"]
    for token in ["VIBE_CODE_SECURITY","VOICE_AI_QA","PLATFORM_APPEAL","EUDR","PRODUCT_COMPLIANCE","LLM_EVAL"]:
        assert token in boundary

def test_state_advances_to_scan048_with_only_prior_validation_beacon():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_047"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_048"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1"}
