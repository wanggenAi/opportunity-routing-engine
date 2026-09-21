import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_032.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan032_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_032"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_scan032_is_broad_reset_not_failure_derived():
    scan=load(SCAN)
    assert scan["search_mode"]=="BROAD_CURRENT_REALITY_RESET_SAMPLE_UNRELATED_DOMAINS_NO_FAILURE_DERIVED_SHAPE_NO_ACTIVE_VERTICAL_OR_MECHANISM_INHERITANCE_KEEP_COMMERCIAL_HARD_FLOORS"
    assert scan["inherited_active_formation_as_seed"] is False
    assert scan["inherited_mechanism_as_requirement"] is False
    assert len(scan["examined_formations"]) >= 6

def test_scan032_does_not_promote_physical_or_expert_service_friction():
    scan=load(SCAN)
    verdicts={x["title"]:x["verdict"] for x in scan["examined_formations"]}
    assert verdicts["SMALL_FARM_AGRICULTURAL_SERVICE_ORCHESTRATOR"]=="DEMOTED_PUBLIC_SERVICE_NETWORK_AND_RECURRING_FIELD_DELIVERY"
    assert verdicts["ASSISTIVE_DEVICE_RENTAL_AVAILABILITY_AND_FIT_ROUTER"]=="DEMOTED_LOCAL_FITTING_DELIVERY_MAINTENANCE_AND_PUBLIC_NETWORK"
    assert verdicts["SHARED_HIGH_END_LAB_CAPACITY_ROUTER"]=="DEMOTED_PUBLIC_OPEN_PLATFORM_AND_EXPERT_TESTING_DEPENDENCE"

def test_state_has_only_scan015_retained_after_scan016_demotion():
    state=load(STATE)
    retained={x["formation_id"] for x in state["retained_research_formations"]}
    assert retained=={"ATTRACTION_SCAN_015-F1"}
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_032"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_033"

def test_scan033_is_second_independent_broad_sample():
    scan=load(SCAN)
    assert scan["next_search_boundary"]=="SECOND_INDEPENDENT_BROAD_CURRENT_REALITY_SAMPLE_UNRELATED_DOMAINS_NO_SCAN032_VERTICAL_INHERITANCE_NO_REQUIRED_MECHANISM_KEEP_COMMERCIAL_HARD_FLOORS"
