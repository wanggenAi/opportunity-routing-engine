import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_086.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan086_is_second_independent_participant_authored_bypass_pass():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_086"
    assert scan["status"] == "COMPLETE"
    assert "SECOND_INDEPENDENT_PARTICIPANT_AUTHORED_CONTROL_SURFACE_BYPASS" in scan["search_mode"]
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["drift_audit"]["discovery_started_from_participant_authored_bypass"] is True


def test_scan086_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("VACATION_RENTAL_DIRECT_BOOKING" in title for title in titles)
    assert any("EV_SMART_CHARGING" in title for title in titles)
    assert any("PARCEL_LOCKER" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan086_requires_exact_surface_completion_reason_and_reason_class():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert formation["actor_a_population"]
        assert formation["actor_b_population"]
        assert len(formation["available_exact_control_surface"]) >= 2
        assert len(formation["participant_authored_manual_or_off_platform_completion"]) >= 2
        assert len(formation["explicit_participant_bypass_or_incompleteness_reason"]) >= 2
        assert formation["bypass_reason_class"]
        assert formation["repeated_bilateral_value_transfer"].startswith("PASS_")


def test_scan086_closes_all_three_without_commercial_promotion():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    assert "MATURE_PMS_CATEGORY" in formations["ATTRACTION_SCAN_086-F1"]["verdict"]
    assert "PROVIDER_PRIVILEGE" in formations["ATTRACTION_SCAN_086-F2"]["verdict"]
    assert "POSTAL_IDENTITY_CUSTODY" in formations["ATTRACTION_SCAN_086-F3"]["verdict"]
    assert all(f["verdict"].startswith("DEMOTED_") for f in scan["examined_formations"])


def test_scan086_two_pass_synthesis_advances_evidence_floor_without_mechanism_inheritance():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_087"
    assert "TWO_INDEPENDENT_PARTICIPANT_AUTHORED_BYPASS_PASSES" in scan["drift_audit"]["second_pass_signal_assessment"]
    boundary = scan["next_search_boundary"]
    assert "INDEPENDENTLY_REPLICATED_PARTICIPANT_CONTROLLED_COMPLETION" in boundary
    assert "DECISIVE_COMPLETION_WITHOUT_INCUMBENT_PRIVILEGED_FALLBACK_OR_MANUAL_EXCEPTION" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary


def test_scan086_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_086"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_086-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_087"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_087"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
