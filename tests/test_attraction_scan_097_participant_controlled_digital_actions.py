import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_097.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan097_is_first_participant_controlled_digital_actions_pass():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_097"
    assert scan["status"] == "COMPLETE"
    assert scan["primary_research_domain"] == "CHINA"
    assert "FIRST_PARTICIPANT_CONTROLLED_DIGITAL_ACTION_RIGHTS_PASS" in scan["search_mode"]
    assert scan["drift_audit"]["participant_controlled_digital_action_rights_required"] is True


def test_scan097_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("DIGITAL_INVOICE" in title for title in titles)
    assert any("CREATOR_PUBLISHING" in title for title in titles)
    assert any("ANDROID_MULTI_STORE" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan097_prefers_digitally_executable_participant_rights():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert formation["observed_actor_state_change_evidence"]
        assert formation["objective_endowment_or_underuse_evidence"]
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert "PASS" in formation["machine_delegatability_check"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan097_kills_exact_and_generic_agent_substitutes():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    assert formations["ATTRACTION_SCAN_097-F1"]["generic_agent_substitutability_check"].startswith("FAIL_")
    assert formations["ATTRACTION_SCAN_097-F2"]["generic_agent_substitutability_check"].startswith("FAIL_")
    assert formations["ATTRACTION_SCAN_097-F3"]["normalized_margin_check"].startswith("FAIL_")


def test_scan097_requires_second_independent_digital_action_pass():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_098"
    boundary = scan["next_search_boundary"]
    assert "SECOND_INDEPENDENT_PARTICIPANT_CONTROLLED_DIGITAL_ACTION_RIGHTS_PASS" in boundary
    assert "OPEN_SOURCE_SUBSTITUTE" in boundary
    assert "EXCLUDE_SCAN060_TO_097_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE" in boundary


def test_scan097_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_097"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_097-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_098"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_098"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
