import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / "data" / "research_runs" / "attraction_scan_022_f1_falsification.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan022_f1_is_demoted_not_promoted():
    result = load(VALIDATION)
    assert result["formation_id"] == "ATTRACTION_SCAN_022-F1"
    assert result["verdict"] == "DEMOTED_ERP_ABSORPTION_AND_NONCOMPOUNDING_COMPLIANCE_LAYER"
    assert result["commercial_candidate"] is False
    assert result["retain_for_active_validation"] is False
    assert result["first_external_value_flow"] == "NOT_PROVEN"


def test_scan022_f1_records_non_compensatory_kills():
    result = load(VALIDATION)
    kills = {item["kill"]: item["status"] for item in result["decisive_kills"]}
    assert kills["GENERIC_AGENT_OR_EXCEL_SUBSTITUTABILITY"] == "FAIL"
    assert kills["INCUMBENT_ERP_TAX_FEATURE_ABSORPTION"] == "FAIL"
    assert kills["VALUE_LAYER_SQUEEZE"] == "FAIL"
    assert kills["COMPOUNDING_OPERATOR_ASSET"] == "FAIL"
    assert kills["EXACT_PAYER_WILLINGNESS"] != "PASS"
    assert kills["FOUNDER_INDEPENDENT_DATA_IMPORT"] != "PASS"


def test_state_removes_scan022_f1_from_active_validation():
    state = load(STATE)
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    resolved = {item["formation_id"]: item["verdict"] for item in state["resolved_research_formations"]}
    validation = {item["formation_id"] for item in state["parallel_workstreams"]["validation"]}
    assert "ATTRACTION_SCAN_022-F1" not in retained
    assert "ATTRACTION_SCAN_022-F1" not in validation
    assert resolved["ATTRACTION_SCAN_022-F1"] == "DEMOTED_ERP_ABSORPTION_AND_NONCOMPOUNDING_COMPLIANCE_LAYER"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_022"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_023"
