import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_026.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan026_closes_with_zero_retention():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_026"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["high_attraction_beacons"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_scan026_does_not_relabel_mature_enterprise_tools_as_micro_edges():
    scan = load(SCAN)
    verdicts = {item["title"]: item["verdict"] for item in scan["examined_formations"]}
    assert verdicts["MULTI_CLOUD_COMMITMENT_AND_IDLE_RESOURCE_RECOVERY"] == "DEMOTED_NATIVE_FINOPS_AND_MATURE_COST_MANAGEMENT"
    assert verdicts["SOFTWARE_LICENSE_SHELFWARE_AND_IDLE_LICENSE_RECOVERY"] == "DEMOTED_EXACT_SAM_INCUMBENTS_WITH_AUTOMATED_RECOVERY"
    assert verdicts["SUPPLIER_QUALITY_CLAIM_AND_8D_RECOVERY_EDGE"] == "DEMOTED_QMS_CONTROL_SURFACE_AND_EXPERT_ROOT_CAUSE"
    assert verdicts["FREIGHT_INVOICE_OVERCHARGE_RECOVERY"] == "DEMOTED_EXACT_FREIGHT_AUDIT_INCUMBENTS"


def test_state_advances_to_contractual_value_leakage_scan():
    state = load(STATE)
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1", "ATTRACTION_SCAN_016-F1"}
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_026"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_027"


def test_scan027_boundary_is_contractually_owed_value_not_generic_cost_optimization():
    scan = load(SCAN)
    assert scan["next_search_boundary"] == "CONTRACTUALLY_OWED_VALUE_LEAKAGE_MISSED_REBATES_CREDITS_SLA_COMPENSATION_PRICE_PROTECTION_WITHOUT_MATURE_RECOVERY_CONTROL_SURFACE"
