import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_033.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan033_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_033"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_second_broad_sample_is_independent():
    scan=load(SCAN)
    assert scan["search_mode"]=="SECOND_INDEPENDENT_BROAD_CURRENT_REALITY_SAMPLE_UNRELATED_DOMAINS_NO_SCAN032_VERTICAL_INHERITANCE_NO_REQUIRED_MECHANISM_KEEP_COMMERCIAL_HARD_FLOORS"
    assert scan["inherited_active_formation_as_seed"] is False
    assert scan["inherited_mechanism_as_requirement"] is False
    assert len(scan["examined_formations"])>=6

def test_new_infrastructure_and_direct_payment_do_not_override_hard_floors():
    scan=load(SCAN)
    verdicts={x["title"]:x["verdict"] for x in scan["examined_formations"]}
    assert verdicts["DATA_PROPERTY_REGISTRATION_EVIDENCE_COMPILER"]=="DEMOTED_REGISTRATION_INSTITUTION_FULL_CHAIN_AND_PROFESSIONAL_REVIEW"
    assert verdicts["DRONE_SERVICE_CAPACITY_ORCHESTRATOR"]=="DEMOTED_ENTERPRISE_PROCUREMENT_AND_HEAVY_FIELD_SERVICE"
    assert verdicts["CONCERT_LUGGAGE_STORAGE_ROUTER"]=="DEMOTED_CURRENT_STORAGE_PLATFORMS_AND_PHYSICAL_CUSTODY"

def test_state_advances_with_only_scan015_retained():
    state=load(STATE)
    retained={x["formation_id"] for x in state["retained_research_formations"]}
    assert retained=={"ATTRACTION_SCAN_015-F1"}
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_033"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_034"

def test_scan034_prioritizes_payer_or_workaround_evidence_without_mechanism_lock():
    scan=load(SCAN)
    assert scan["next_search_boundary"]=="BROAD_CURRENT_REALITY_REQUIRE_DIRECT_PAYER_OR_REPEATED_WORKAROUND_EVIDENCE_NO_PRIOR_VERTICAL_OR_REQUIRED_MECHANISM_KEEP_COMMERCIAL_HARD_FLOORS"
