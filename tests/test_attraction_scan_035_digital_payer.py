import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_035.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan035_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_035"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_paid_digital_categories_still_fail_exact_incumbent_floors():
    scan=load(SCAN)
    verdicts={x["title"]:x["verdict"] for x in scan["examined_formations"]}
    assert verdicts["GEO_AI_SEARCH_BRAND_VISIBILITY_CONTROL"]=="DEMOTED_DENSE_EXACT_SAAS_AND_SERVICE_INCUMBENTS"
    assert verdicts["APP_SDK_PRIVACY_COMPLIANCE_AUTOMATION"]=="DEMOTED_EXACT_PAID_SECURITY_PLATFORM"
    assert verdicts["AI_JOB_APPLICATION_AND_RESUME_AUTOMATION"]=="DEMOTED_JOB_PLATFORM_NATIVE_AND_MULTIPLE_PAID_INCUMBENTS"
    assert verdicts["SOFTWARE_LOCALIZATION_TRANSLATION_AUTOMATION"]=="DEMOTED_HYPERSCALER_ENTERPRISE_TRANSLATION_AND_LOCALIZATION_MARKET"

def test_platform_native_rights_and_label_controls_are_not_reinvented():
    scan=load(SCAN)
    verdicts={x["title"]:x["verdict"] for x in scan["examined_formations"]}
    assert verdicts["AIGC_COMMERCIAL_RIGHTS_PROOF_LAYER"]=="DEMOTED_GENERATION_PLATFORM_NATIVE_LICENSE_AND_RIGHTS_BOUNDARY"
    assert verdicts["SHORT_VIDEO_CONTENT_LABELING_AUTOMATION"]=="DEMOTED_PLATFORM_NATIVE_PUBLISHING_REQUIREMENT_AND_RISK_TOOLING"

def test_state_keeps_only_scan015_and_advances():
    state=load(STATE)
    retained={x["formation_id"] for x in state["retained_research_formations"]}
    assert retained=={"ATTRACTION_SCAN_015-F1"}
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_035"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_036"

def test_scan036_changes_research_order_not_business_shape():
    scan=load(SCAN)
    assert scan["next_search_boundary"]=="BROAD_CURRENT_REALITY_DIRECT_PAYER_OR_REPEATED_WORKAROUND_DIGITAL_OR_DELEGATABLE_DELIVERY_EXACT_INCUMBENT_PREFLIGHT_BEFORE_DEEP_RESEARCH_NO_PRIOR_VERTICAL_OR_REQUIRED_MECHANISM"
