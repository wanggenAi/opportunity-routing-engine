import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_095.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan095_uses_participant_authored_current_reality_source_shift():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_095"
    assert scan["status"] == "COMPLETE"
    assert scan["discovery_source_reset"] is True
    assert scan["inherited_mechanism_as_requirement"] is False
    assert "PARTICIPANT_AUTHORED_CURRENT_REALITY_SOURCE_SHIFT" in scan["search_mode"]
    assert "INDEPENDENT_OBJECTIVE_CORROBORATION" in scan["search_mode"]
    assert "NO_JOB_GIG_RFQ_OR_PROCUREMENT_FEED_AS_DISCOVERY_ONTOLOGY" in scan["search_mode"]


def test_scan095_binds_participant_and_objective_evidence_before_preflight():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    for formation in scan["examined_formations"]:
        assert formation["observed_actor_state_change_evidence"]
        assert formation["objective_endowment_or_underuse_evidence"]
        assert formation["observed_behavior_or_workaround_evidence"]
        assert formation["contradiction_or_partial_flow_evidence"]
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan095_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("EV_CHARGING" in title for title in titles)
    assert any("PACKAGE_ROOM" in title for title in titles)
    assert any("COI_COLLECTION" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan095_preserves_control_rights_and_substitutability_floors():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    ev = formations["ATTRACTION_SCAN_095-F1"]
    package = formations["ATTRACTION_SCAN_095-F2"]
    coi = formations["ATTRACTION_SCAN_095-F3"]
    assert ev["founder_independence_check"].startswith("FAIL_")
    assert ev["data_action_rights_check"].startswith("FAIL_")
    assert package["data_action_rights_check"].startswith("FAIL_")
    assert package["machine_delegatability_check"].startswith("PARTIAL_")
    assert coi["machine_delegatability_check"].startswith("PASS_")
    assert coi["normalized_margin_check"].startswith("FAIL_")


def test_scan095_repeats_source_shift_before_deriving_new_mechanism():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_096"
    boundary = scan["next_search_boundary"]
    assert "SECOND_INDEPENDENT_PARTICIPANT_AUTHORED_CURRENT_REALITY_SOURCE_SHIFT" in boundary
    assert "EXCLUDE_SCAN060_TO_095_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert scan["drift_audit"]["response"].startswith(
        "REPEAT_PARTICIPANT_AUTHORED_CURRENT_REALITY_SOURCE_SHIFT_IN_SCAN096"
    )


def test_scan095_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_095"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_095-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_096"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_096"
    assert (
        state["parallel_workstreams"]["discovery"]["search_boundary"]
        == scan["next_search_boundary"]
    )
