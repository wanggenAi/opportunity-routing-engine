import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_036.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan036_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_036"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_scan036_runs_exact_incumbent_preflight_before_deep_research():
    scan=load(SCAN)
    assert "EXACT_INCUMBENT_PREFLIGHT_BEFORE_DEEP_RESEARCH" in scan["search_mode"]
    assert all(x["incumbent_preflight"].startswith("EXACT") or "EXACT" in x["incumbent_preflight"] or x["incumbent_preflight"]=="DENSE_EXACT_PAID_PRODUCTS_FOUND" for x in scan["examined_formations"])

def test_scan036_demotes_same_control_loop_incumbents():
    scan=load(SCAN)
    verdicts={x["title"]:x["verdict"] for x in scan["examined_formations"]}
    assert verdicts["AI_USAGE_BASED_SOFTWARE_SPEND_CONTROL"]=="DEMOTED_VENDOR_NATIVE_AND_PROCUREMENT_FINOPS_CONTROL_SURFACES"
    assert verdicts["EU_AI_ACT_CONTINUOUS_EVIDENCE_AUTOMATION"]=="DEMOTED_DENSE_EXACT_AI_GOVERNANCE_AND_COMPLIANCE_SAAS"
    assert verdicts["EV_FLEET_HOME_CHARGING_REIMBURSEMENT"]=="DEMOTED_EXACT_FLEET_HOME_CHARGING_REIMBURSEMENT_PRODUCTS"
    assert verdicts["API_DEPRECATION_SUNSET_MONITORING"]=="DEMOTED_EXACT_LOW_COST_API_CHANGE_MONITORING_PRODUCT"

def test_state_keeps_only_scan015_and_advances_to_scan037():
    state=load(STATE)
    retained={x["formation_id"] for x in state["retained_research_formations"]}
    assert retained=={"ATTRACTION_SCAN_015-F1"}
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_036"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_037"

def test_scan037_requires_residual_leakage_after_incumbent_preflight():
    scan=load(SCAN)
    assert "OBSERVED_RESIDUAL_LEAKAGE_OR_UNOWNED_ACTION_EDGE" in scan["next_search_boundary"]
