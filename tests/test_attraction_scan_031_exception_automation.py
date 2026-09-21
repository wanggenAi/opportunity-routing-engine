import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_031.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan031_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_031"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_exception_surfaces_are_not_reinvented():
    scan=load(SCAN)
    verdicts={x["title"]:x["verdict"] for x in scan["examined_formations"]}
    assert verdicts["APP_STORE_REJECTION_DIAGNOSIS_AND_REMEDIATION"]=="DEMOTED_EXACT_SPECIALIZED_INCUMBENTS"
    assert verdicts["PAYMENT_HOLD_AND_REJECTION_DECISIONING"]=="DEMOTED_BANK_AND_ERP_NATIVE_DECISION_APIS"
    assert verdicts["IDENTITY_ACCESS_EXCEPTION_REMEDIATION"]=="DEMOTED_CLOUD_IAM_NATIVE_POLICY_TROUBLESHOOTING_AND_AUTOMATION"
    assert verdicts["PRODUCTION_INCIDENT_AUTOREMEDIATION"]=="DEMOTED_AI_SRE_CONTROL_SURFACE"
    assert verdicts["PROCUREMENT_ACKNOWLEDGMENT_EXCEPTION"]=="DEMOTED_COPILOT_SAP_REFERENCE_AUTOMATION"

def test_state_advances_to_broad_reset():
    state=load(STATE)
    retained={x["formation_id"] for x in state["retained_research_formations"]}
    assert retained=={"ATTRACTION_SCAN_015-F1","ATTRACTION_SCAN_016-F1"}
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_031"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_032"

def test_scan032_does_not_inherit_failure_derived_shape():
    scan=load(SCAN)
    assert scan["next_search_boundary"]=="BROAD_CURRENT_REALITY_RESET_SAMPLE_UNRELATED_DOMAINS_NO_FAILURE_DERIVED_SHAPE_NO_ACTIVE_VERTICAL_OR_MECHANISM_INHERITANCE_KEEP_COMMERCIAL_HARD_FLOORS"
