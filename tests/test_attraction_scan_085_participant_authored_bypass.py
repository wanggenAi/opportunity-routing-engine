import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_085.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan085_is_participant_authored_control_surface_bypass_first():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_085"
    assert scan["status"] == "COMPLETE"
    assert "PARTICIPANT_AUTHORED_CONTROL_SURFACE_BYPASS_FIRST" in scan["search_mode"]
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["drift_audit"]["discovery_started_from_participant_authored_bypass"] is True


def test_scan085_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("RESTAURANT_DIRECT_ORDER" in title for title in titles)
    assert any("OFF_PLATFORM_TICKET" in title for title in titles)
    assert any("AIRLINE_ITINERARY_CHANGE" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan085_requires_exact_surface_observed_bypass_and_explicit_reason():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert formation["actor_a_population"]
        assert formation["actor_b_population"]
        assert len(formation["available_exact_control_surface"]) >= 2
        assert len(formation["participant_authored_manual_or_off_platform_completion"]) >= 2
        assert len(formation["explicit_participant_bypass_or_incompleteness_reason"]) >= 2
        assert formation["repeated_bilateral_value_transfer"].startswith("PASS_")


def test_scan085_closes_without_confusing_bypass_with_white_space():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    assert "DIRECT_ORDERING_RAILS" in formations["ATTRACTION_SCAN_085-F1"]["verdict"]
    assert "TRANSFER_RIGHTS" in formations["ATTRACTION_SCAN_085-F2"]["verdict"]
    assert formations["ATTRACTION_SCAN_085-F3"]["data_action_rights_check"].startswith("FAIL_")
    assert all(f["verdict"].startswith("DEMOTED_") for f in scan["examined_formations"])


def test_scan085_requires_second_independent_bypass_pass_before_new_boundary():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_086"
    boundary = scan["next_search_boundary"]
    assert "SECOND_INDEPENDENT_PARTICIPANT_AUTHORED" in boundary
    assert "EXPLICIT_PARTICIPANT_STATED_BYPASS_OR_INCOMPLETENESS_REASON" in boundary
    assert "RECORD_REASON_CLASS" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary


def test_scan085_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_085"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_085-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_086"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_086"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
