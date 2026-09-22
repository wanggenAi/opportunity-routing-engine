import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_098.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan098_is_second_participant_controlled_digital_actions_pass():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_098"
    assert scan["status"] == "COMPLETE"
    assert scan["primary_research_domain"] == "CHINA"
    assert "SECOND_INDEPENDENT_PARTICIPANT_CONTROLLED_DIGITAL_ACTION_RIGHTS_PASS" in scan["search_mode"]
    assert scan["drift_audit"]["participant_controlled_digital_action_rights_required"] is True


def test_scan098_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("INTERNAL_MARKETING" in title for title in titles)
    assert any("SMS_OTP_ROUTING" in title for title in titles)
    assert any("WORKTREE_LOCAL_ASSET" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan098_all_formations_have_current_reality_and_incumbent_preflight():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert formation["observed_actor_state_change_evidence"]
        assert formation["objective_endowment_or_underuse_evidence"]
        assert formation["observed_behavior_or_workaround_evidence"]
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert "PASS" in formation["machine_delegatability_check"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan098_kills_generic_or_exact_substitution():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    assert formations["ATTRACTION_SCAN_098-F1"]["generic_agent_substitutability_check"].startswith("FAIL_")
    assert formations["ATTRACTION_SCAN_098-F2"]["normalized_margin_check"].startswith("FAIL_")
    assert formations["ATTRACTION_SCAN_098-F3"]["generic_agent_substitutability_check"].startswith("FAIL_")


def test_scan098_advances_evidence_priority_after_two_passes():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_099"
    boundary = scan["next_search_boundary"]
    assert "OPERATOR_CONTROL_ADVANTAGE_EVIDENCE_FIRST" in boundary
    assert "PARTICIPANT_CREDENTIALS_GENERIC_AGENTS_ACTIVE_OPEN_SOURCE_TOOLS_AND_MATURE_WORKFLOW_PLATFORMS" in boundary
    assert "EXCLUDE_SCAN060_TO_098_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE" in boundary


def test_scan098_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_098"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_098-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_099"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_099"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
