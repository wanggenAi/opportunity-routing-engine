import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_028.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan028_closes_with_zero_retention():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_028"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["high_attraction_beacons"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_scan028_is_behavior_first_not_recovery_or_router_seeded():
    scan = load(SCAN)
    assert scan["search_mode"] == "CURRENT_EMERGENT_BEHAVIOR_AND_NEW_WORKFLOW_FORMATIONS_NO_COST_REFUND_REBATE_RECOVERY_OR_PRIOR_MECHANISM_INHERITANCE"
    assert scan["inherited_active_formation_as_seed"] is False
    assert scan["inherited_mechanism_as_requirement"] is False


def test_new_behaviors_are_not_mistaken_for_white_space():
    scan = load(SCAN)
    verdicts = {item["title"]: item["verdict"] for item in scan["examined_formations"]}
    assert verdicts["AI_SERVICE_DELIVERABLE_ACCEPTANCE_LAYER"] == "DEMOTED_PLATFORM_DISPUTE_CONTROL_AND_FAST_QA_PRODUCTIZATION"
    assert verdicts["EMBODIED_DATA_CROWD_COLLECTION_MARKETPLACE"] == "DEMOTED_MULTIPLE_CURRENT_PLATFORM_INCUMBENTS"
    assert verdicts["CHINA_AGENT_TO_HUMAN_EXECUTION_MARKETPLACE"] == "DEMOTED_GLOBAL_EXACT_MARKETPLACE_FORMATION_AND_WHOLE_MARKETPLACE_REQUIREMENT"
    assert verdicts["ONE_PERSON_CROSS_BORDER_AGENT_OPERATING_SYSTEM"] == "DEMOTED_PLATFORM_NATIVE_AGENT_INTERNALIZATION"


def test_state_advances_to_preplatform_behavior_scan_without_new_candidate():
    state = load(STATE)
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1", "ATTRACTION_SCAN_016-F1"}
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_028"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_029"


def test_scan029_boundary_prioritizes_self_organized_preplatform_behavior():
    scan = load(SCAN)
    assert scan["next_search_boundary"] == "CURRENT_SELF_ORGANIZED_PRE_PLATFORM_BEHAVIOR_WITH_REAL_EXCHANGE_NO_DOMINANT_CONTROL_SURFACE_NO_PRIOR_VERTICAL_OR_MECHANISM_INHERITANCE"
