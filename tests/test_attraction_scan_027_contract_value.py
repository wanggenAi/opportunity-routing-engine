import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_027.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan027_closes_with_zero_retention():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_027"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["high_attraction_beacons"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_contract_value_recovery_categories_are_not_reinvented():
    scan = load(SCAN)
    verdicts = {item["title"]: item["verdict"] for item in scan["examined_formations"]}
    assert verdicts["SAAS_AND_CLOUD_SLA_CREDIT_RECOVERY"] == "DEMOTED_EXACT_AUTOMATED_RECOVERY_INCUMBENTS"
    assert verdicts["VENDOR_REBATE_AND_TIERED_DISCOUNT_RECOVERY"] == "DEMOTED_ERP_DMS_PRM_STANDARD_CAPABILITY"
    assert verdicts["CONTRACT_TO_INVOICE_PRICE_PROTECTION_AND_CREDIT_AUDIT"] == "DEMOTED_CONTRACT_PERFORMANCE_AND_INVOICE_AUDIT_INCUMBENTS"


def test_state_advances_to_behavior_first_scan_without_new_candidate():
    state = load(STATE)
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1", "ATTRACTION_SCAN_016-F1"}
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_027"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_028"


def test_scan028_resets_recovery_mechanism_bias():
    scan = load(SCAN)
    assert scan["next_search_boundary"] == "CURRENT_EMERGENT_BEHAVIOR_AND_NEW_WORKFLOW_FORMATIONS_NO_COST_REFUND_REBATE_RECOVERY_OR_PRIOR_MECHANISM_INHERITANCE"
