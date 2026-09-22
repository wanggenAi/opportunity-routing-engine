import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_084.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan084_is_second_independent_bilateral_partial_flow_pass():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_084"
    assert scan["status"] == "COMPLETE"
    assert "SECOND_INDEPENDENT_BILATERAL_PARTIAL_FLOW_FIRST" in scan["search_mode"]
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["drift_audit"]["discovery_started_from_bilateral_partial_flow"] is True


def test_scan084_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("TRUCK_CAPACITY" in title for title in titles)
    assert any("INDUSTRIAL_RESIDUAL" in title for title in titles)
    assert any("NHS_APPOINTMENT" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan084_requires_real_two_sided_flow_and_connection_pressure():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert formation["actor_a_population"]
        assert formation["actor_b_population"]
        assert len(formation["repeated_partial_flow_evidence"]) >= 2
        assert len(formation["connection_pressure_or_workaround"]) >= 2


def test_scan084_closes_on_exact_network_or_privileged_rights():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    assert any("DAT" in x for x in formations["ATTRACTION_SCAN_084-F1"]["exact_incumbent_and_control_surface_preflight"])
    assert any("Cyrkl" in x for x in formations["ATTRACTION_SCAN_084-F2"]["exact_incumbent_and_control_surface_preflight"])
    assert formations["ATTRACTION_SCAN_084-F3"]["data_action_rights_check"].startswith("FAIL_")
    assert all(f["verdict"].startswith("DEMOTED_") for f in scan["examined_formations"])


def test_scan084_changes_evidence_object_only_after_two_bilateral_passes():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_085"
    boundary = scan["next_search_boundary"]
    assert "PARTICIPANT_AUTHORED_OFF_PLATFORM_OR_MANUAL_BILATERAL_COMPLETION" in boundary
    assert "EXPLICIT_PARTICIPANT_STATED_BYPASS_OR_INCOMPLETENESS_REASON" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary


def test_scan084_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_084"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_084-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_085"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_085"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
