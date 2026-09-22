import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_090.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan090_repeats_paid_coordination_floor_without_raising_it_early():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_090"
    assert scan["status"] == "COMPLETE"
    assert scan["search_mode"].startswith("SECOND_INDEPENDENT_PASS_")
    assert "PAID_CROSS_COMPONENT_COORDINATION" in scan["search_mode"]
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["drift_audit"]["two_pass_assessment"].startswith("PASS_")


def test_scan090_is_fresh_and_formation_diverse():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("CROSS_SAAS" in title for title in titles)
    assert any("CREDENTIAL" in title for title in titles)
    assert any("CALENDAR" in title for title in titles)
    assert scan["drift_audit"]["formation_diversity"].startswith("PASS_")
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan090_each_formation_has_replicated_actual_coordination_payment():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert len(formation["existing_components"]) >= 2
        assert len(formation["independent_replication"]) >= 2
        assert len(formation["participant_authored_successful_completion"]) >= 2
        assert len(formation["explicit_participant_incompleteness_reason"]) >= 2
        assert formation["actual_cross_component_coordination_payment_check"].startswith("PASS_")
        assert formation["manual_multi_component_completion_check"].startswith("PASS_")
        assert formation["no_single_current_control_surface_check"].startswith("PASS_")
        assert formation["decisive_completion_control"].startswith("PASS_")


def test_scan090_closes_mature_paid_middle_layers():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    assert "ZAPIER_AND_PEER_AUTOMATION_PLATFORMS_ALREADY_OWN" in formations["ATTRACTION_SCAN_090-F1"]["verdict"]
    assert "MATURE_PASSWORD_MANAGERS_ALREADY_OWN" in formations["ATTRACTION_SCAN_090-F2"]["verdict"]
    assert "FANTASTICAL_ALREADY_OWNS" in formations["ATTRACTION_SCAN_090-F3"]["verdict"]
    assert all(f["verdict"].startswith("DEMOTED_") for f in formations.values())
    assert all(f["data_action_rights_check"].startswith("FAIL_") for f in formations.values())
    assert all(f["normalized_margin_check"].startswith("FAIL_") for f in formations.values())


def test_scan090_derives_residual_failure_plus_second_cost_only_after_two_passes():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_091"
    boundary = scan["next_search_boundary"]
    assert "PAID_COORDINATOR_RESIDUAL_FAILURE" in boundary
    assert "COMPENSATING_SECOND_LAYER_COST" in boundary
    assert "ACTUAL_ADDITIONAL_PAYMENT_TO_A_SECOND_DISTINCT_SERVICE_PROVIDER" in boundary
    assert "REPEATED_EXPLICITLY_QUANTIFIED_MANUAL_WORKAROUND_COST" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert any("SCAN089_AND_SCAN090_TOGETHER" in x for x in scan["scan_learnings"])


def test_scan090_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_090"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_090-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_091"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_091"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
