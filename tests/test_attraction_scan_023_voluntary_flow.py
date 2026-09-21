import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_023.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan023_starts_from_voluntary_energy_not_policy_or_active_vertical():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_023"
    assert scan["search_mode"] == "VOLUNTARY_ENERGY_FIRST_BROAD_REALITY_NO_POLICY_OR_ACTIVE_VERTICAL_INHERITANCE"
    assert scan["inherited_active_formation_as_seed"] is False
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["policy_text_used_as_primary_seed"] is False


def test_scan023_has_zero_false_promotions_or_retention():
    scan = load(SCAN)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["high_attraction_beacons"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_scan023_kills_hot_whole_marketplace_shapes_on_control_and_delivery():
    scan = load(SCAN)
    verdicts = {item["title"]: item["verdict"] for item in scan["examined_formations"]}
    assert verdicts["ROBOT_EVENT_RENTAL_META_ROUTER"] == "DEMOTED_INCUMBENT_MATCHING_AND_HUMAN_DELIVERY"
    assert verdicts["INBOUND_VISITOR_LOCAL_LIFE_ORCHESTRATOR"] == "DEMOTED_CONTROL_SURFACE_INTERNALIZED"
    assert verdicts["AI_GLASSES_CROSS_BRAND_TRY_BEFORE_BUY_NETWORK"] == "DEMOTED_VENDOR_AND_RETAIL_CHANNEL_INTERNALIZATION"
    assert verdicts["EVENT_DAY_MICROSERVICE_CAPACITY_ROUTER"] == "DEMOTED_DISCOVERY_RAIL_CROWDED_AND_HUMAN_DELIVERY"
    assert verdicts["HOME_CARE_TRUST_AND_CAPACITY_ROUTER"] == "DEMOTED_RECURRING_HUMAN_DELIVERY_AND_PUBLIC_TRUST_RAIL"


def test_state_advances_to_scan024_without_losing_independent_validation_queue():
    state = load(STATE)
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    validation = {item["formation_id"] for item in state["parallel_workstreams"]["validation"]}
    assert retained == {"ATTRACTION_SCAN_015-F1", "ATTRACTION_SCAN_016-F1"}
    assert validation == {"ATTRACTION_SCAN_015-F1", "ATTRACTION_SCAN_016-F1"}
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_023"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_024"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == (
        "HIGH_ENERGY_EXISTING_FLOWS_FIND_UNOWNED_MICRO_EDGES_NO_WHOLE_MARKETPLACE_OR_POLICY_PRIOR"
    )
