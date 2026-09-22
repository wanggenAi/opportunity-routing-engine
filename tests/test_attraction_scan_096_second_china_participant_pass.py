import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_096.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan096_is_second_china_participant_authored_pass():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_096"
    assert scan["status"] == "COMPLETE"
    assert scan["primary_research_domain"] == "CHINA"
    assert scan["research_target_geography"] == "CHINA"
    assert "SECOND_INDEPENDENT_PARTICIPANT_AUTHORED_CHINA_CURRENT_REALITY_SOURCE_SHIFT" in scan["search_mode"]
    assert "NO_JOB_GIG_RFQ_OR_PROCUREMENT_FEED_AS_DISCOVERY_ONTOLOGY" in scan["search_mode"]


def test_scan096_is_fresh_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("BULKY_FURNITURE" in title for title in titles)
    assert any("IMAGING_AND_TEST_RESULT_PORTABILITY" in title for title in titles)
    assert any("AGRICULTURAL_MACHINERY" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan096_binds_participant_and_objective_evidence_before_mechanism():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert formation["observed_actor_state_change_evidence"]
        assert formation["objective_endowment_or_underuse_evidence"]
        assert formation["observed_behavior_or_workaround_evidence"]
        assert formation["contradiction_or_partial_flow_evidence"]
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan096_uses_jiangsu_xuzhou_execution_lens_without_forcing_promotion():
    scan = load(SCAN)
    f3 = {f["formation_id"]: f for f in scan["examined_formations"]}["ATTRACTION_SCAN_096-F3"]
    assert "XUZHOU" in f3["normalized_margin_check"]
    assert "MALIDUO" in f3["exact_incumbent_and_control_surface_preflight"][0].upper()
    assert f3["verdict"].startswith("DEMOTED_")


def test_scan096_derives_control_surface_evidence_priority_not_product():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_097"
    boundary = scan["next_search_boundary"]
    assert "PARTICIPANT_CONTROLLED_DIGITAL_ACTION_RIGHTS_FIRST" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE" in boundary
    assert "EXCLUDE_SCAN060_TO_096_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert scan["drift_audit"]["response"].startswith(
        "SHIFT_SCAN097_ENTRY_TO_PARTICIPANT_CONTROLLED_DIGITAL_ACTION_RIGHTS_FIRST"
    )


def test_scan096_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_096"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_096-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_097"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_097"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
