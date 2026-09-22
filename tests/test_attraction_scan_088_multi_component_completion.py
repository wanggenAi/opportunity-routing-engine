import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_088.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan088_requires_replicated_participant_controlled_multi_component_completion():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_088"
    assert scan["status"] == "COMPLETE"
    assert "INDEPENDENTLY_REPLICATED_PARTICIPANT_CONTROLLED_MULTI_COMPONENT_COMPLETION" in scan["search_mode"]
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["drift_audit"]["independent_replication_floor"].startswith("PASS_")
    assert scan["drift_audit"]["multi_component_floor"].startswith("PASS_")


def test_scan088_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("EV_ROAD_TRIP" in title for title in titles)
    assert any("FLIGHT_DISRUPTION" in title for title in titles)
    assert any("HOME_BATTERY" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan088_each_formation_has_replicated_success_reason_and_multiple_components():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert len(formation["existing_components"]) >= 2
        assert len(formation["independent_replication"]) >= 2
        assert len(formation["participant_authored_successful_completion"]) >= 2
        assert len(formation["explicit_participant_incompleteness_reason"]) >= 2
        assert formation["manual_multi_component_completion_check"].startswith("PASS_")
        assert formation["decisive_completion_control"].startswith("PASS_")
        assert formation["repeated_bilateral_value_transfer"].startswith("PASS_")


def test_scan088_closes_current_aggregation_rights_and_generic_control_false_positives():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    assert "MATURE_EV_PLANNING_AND_CROSS_NETWORK_PAYMENT_AGGREGATORS" in formations["ATTRACTION_SCAN_088-F1"]["verdict"]
    assert "AUTHORITATIVE_TICKET_ACTION_REMAINS_AIRLINE_OR_AGENT_RIGHTS_BOUND" in formations["ATTRACTION_SCAN_088-F2"]["verdict"]
    assert "HOME_ASSISTANT_ALREADY_PROVIDES_A_GENERIC_CROSS_VENDOR_CONTROL_SURFACE" in formations["ATTRACTION_SCAN_088-F3"]["verdict"]
    assert all(f["verdict"].startswith("DEMOTED_") for f in scan["examined_formations"])
    assert formations["ATTRACTION_SCAN_088-F1"]["no_single_current_control_surface_check"].startswith("PASS_")
    assert formations["ATTRACTION_SCAN_088-F2"]["no_single_current_control_surface_check"].startswith("PASS_")
    assert formations["ATTRACTION_SCAN_088-F3"]["no_single_current_control_surface_check"].startswith("FAIL_")


def test_scan088_requires_payment_for_coordination_next():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_089"
    boundary = scan["next_search_boundary"]
    assert "INDEPENDENTLY_REPLICATED_PAID_CROSS_COMPONENT_COORDINATION" in boundary
    assert "ACTUAL_PAYMENT_TO_A_DISTINCT_NON_INCUMBENT_SOFTWARE_OR_SERVICE" in boundary
    assert "TWO_OR_MORE_EXISTING_COMPONENTS" in boundary
    assert "NO_SINGLE_CURRENT_CONTROL_SURFACE_OWNS_THE_END_TO_END_OUTCOME" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert all(f["cross_component_coordination_payment_check"].startswith("FAIL_") for f in scan["examined_formations"])


def test_scan088_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_088"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_088-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_089"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_089"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
