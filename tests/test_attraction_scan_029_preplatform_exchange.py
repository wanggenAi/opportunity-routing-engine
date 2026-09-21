import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_029.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan029_closes_with_zero_retention():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_029"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["high_attraction_beacons"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_preplatform_groups_are_not_mistaken_for_thin_software_edges():
    scan = load(SCAN)
    verdicts = {item["title"]: item["verdict"] for item in scan["examined_formations"]}
    assert verdicts["SHARED_EMPLOYEE_MATCHING_LAYER"] == "DEMOTED_HUMAN_SUPPLY_COMPLIANCE_AND_PLATFORMIZATION"
    assert verdicts["DAZI_GROUP_OPERATING_SYSTEM"] == "DEMOTED_MATURE_EVENT_TOOLS_AND_RECURRING_COMMUNITY_OPERATIONS"
    assert verdicts["SURPLUS_MEAL_GROUP_ROUTER"] == "DEMOTED_EXACT_SURPLUS_FOOD_PLATFORM_AND_PHYSICAL_FULFILLMENT"
    assert verdicts["PARK_SUPPLY_DEMAND_AUTOMATCH"] == "DEMOTED_FREE_PUBLIC_BULLETIN_AND_LEAD_GENERATION_ONLY"


def test_state_advances_to_single_owner_workflow_scan():
    state = load(STATE)
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1", "ATTRACTION_SCAN_016-F1"}
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_029"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_030"


def test_scan030_removes_new_supply_and_marketplace_requirement():
    scan = load(SCAN)
    assert scan["next_search_boundary"] == "CURRENT_SINGLE_OWNER_MANUAL_CROSS_SYSTEM_WORKFLOW_INPUT_AND_ACTION_RIGHTS_ALREADY_OWNED_NO_NEW_SUPPLY_NO_MARKETPLACE_NO_PRIOR_VERTICAL_INHERITANCE"
