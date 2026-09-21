import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "research_runs" / "attraction_scan_024_f1_falsification.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan024_f1_is_demoted_not_promoted():
    result = load(RESULT)
    assert result["formation_id"] == "ATTRACTION_SCAN_024-F1"
    assert result["verdict"] == "DEMOTED_ACTIVE_OPEN_SOURCE_CONTROL_SURFACE_AND_NONCOMPOUNDING_GATEWAY_FEATURE"
    assert result["commercial_candidate"] is False
    assert result["retain_for_active_validation"] is False
    assert result["first_external_value_flow"] == "NOT_PROVEN"


def test_exact_incumbent_and_operator_asset_are_hard_kills():
    result = load(RESULT)
    kills = {item["kill"]: item["status"] for item in result["decisive_kills"]}
    assert kills["EXACT_ACTIVE_INCUMBENT"] == "FAIL"
    assert kills["FEATURE_ABSORPTION"] == "FAIL"
    assert kills["DISTINCT_OPERATOR_ASSET"] == "FAIL"
    assert kills["EXACT_PAYER_WILLINGNESS"] != "PASS"


def test_state_removes_scan024_f1_from_active_validation():
    state = load(STATE)
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    resolved = {item["formation_id"]: item["verdict"] for item in state["resolved_research_formations"]}
    active_validation = {item["formation_id"] for item in state["parallel_workstreams"]["validation"]}
    assert "ATTRACTION_SCAN_024-F1" not in retained
    assert "ATTRACTION_SCAN_024-F1" not in active_validation
    assert resolved["ATTRACTION_SCAN_024-F1"] == "DEMOTED_ACTIVE_OPEN_SOURCE_CONTROL_SURFACE_AND_NONCOMPOUNDING_GATEWAY_FEATURE"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_025"
