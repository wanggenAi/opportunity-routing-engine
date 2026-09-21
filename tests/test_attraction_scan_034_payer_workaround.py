import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_034.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan034_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_034"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_direct_payment_does_not_override_delivery_or_incumbent_floors():
    scan=load(SCAN)
    verdicts={x["title"]:x["verdict"] for x in scan["examined_formations"]}
    assert verdicts["GENERAL_LIFESTYLE_PROXY_SERVICE_MARKETPLACE"]=="DEMOTED_RECURRING_HUMAN_DELIVERY_AND_MARKETPLACE_OPERATIONS"
    assert verdicts["HOME_ORGANIZATION_AUTOMATION_LAYER"]=="DEMOTED_DIRECT_HUMAN_SERVICE_AND_EXISTING_VERTICAL_PLATFORM"
    assert verdicts["AI_BID_DOCUMENT_PRODUCTION_LAYER"]=="DEMOTED_MULTIPLE_EXACT_SPECIALIZED_INCUMBENTS"
    assert verdicts["ENTERPRISE_CONTENT_MODERATION_SERVICE_LAYER"]=="DEMOTED_HYPERSCALER_PAID_API_CONTROL_SURFACE"

def test_repeated_workaround_does_not_override_native_control_surface():
    scan=load(SCAN)
    verdicts={x["title"]:x["verdict"] for x in scan["examined_formations"]}
    assert verdicts["AI_TO_HUMAN_CUSTOMER_SERVICE_CONTEXT_CONTINUITY"]=="DEMOTED_NATIVE_CONTACT_CENTER_HANDOFF_AND_CONTEXT_CONTINUITY"
    assert verdicts["WECHAT_EXCEL_TO_CRM_SALES_MEMORY_BRIDGE"]=="DEMOTED_CRM_LOW_CODE_AND_GENERIC_INTEGRATION"

def test_state_keeps_only_scan015_and_advances():
    state=load(STATE)
    retained={x["formation_id"] for x in state["retained_research_formations"]}
    assert retained=={"ATTRACTION_SCAN_015-F1"}
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_034"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_035"

def test_scan035_adds_delivery_prefilter_without_mechanism_lock():
    scan=load(SCAN)
    assert scan["next_search_boundary"]=="BROAD_CURRENT_REALITY_DIRECT_PAYER_OR_REPEATED_WORKAROUND_PLUS_DIGITAL_OR_DELEGATABLE_DELIVERY_NO_PRIOR_VERTICAL_OR_REQUIRED_MECHANISM_KEEP_COMMERCIAL_HARD_FLOORS"
