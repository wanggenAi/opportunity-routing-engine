import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_030.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan030_closes_with_zero_retention():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_030"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["high_attraction_beacons"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_scan030_does_not_relabel_generic_integration_as_business():
    scan = load(SCAN)
    verdicts = {item["title"]: item["verdict"] for item in scan["examined_formations"]}
    assert verdicts["LOGISTICS_MULTI_SYSTEM_AR_AP_RECONCILIATION"] == "DEMOTED_EXACT_ERP_BMS_TMS_AUTOMATION"
    assert verdicts["MANUFACTURING_BOM_REPORT_AND_ORDER_COPY_BRIDGE"] == "DEMOTED_GENERIC_RPA_IDP_LOW_CODE_AND_NATIVE_INTEGRATION"
    assert verdicts["CROSS_BORDER_DECLARATION_DATA_REENTRY_BRIDGE"] == "DEMOTED_EXISTING_API_EXCEL_IMPORT_AND_DECLARATION_SAAS"
    assert verdicts["CHAIN_STORE_OMNICHANNEL_SETTLEMENT_RECONCILIATION"] == "DEMOTED_EXACT_OMNICHANNEL_SETTLEMENT_PLATFORMS"


def test_state_advances_to_non_generic_exception_scan():
    state = load(STATE)
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1", "ATTRACTION_SCAN_016-F1"}
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_030"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_031"


def test_scan031_requires_non_generic_exception_state():
    scan = load(SCAN)
    assert scan["next_search_boundary"] == "FORMATION_DIVERSE_SINGLE_OWNER_HIGH_CONSEQUENCE_EXCEPTIONS_NON_GENERIC_STATE_NOT_DATA_MOVEMENT_INPUT_AND_ACTION_RIGHTS_OWNED_NO_RECURRING_EXPERT"
