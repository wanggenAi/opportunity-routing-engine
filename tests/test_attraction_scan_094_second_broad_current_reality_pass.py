import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_094.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan094_is_second_independent_broad_current_reality_pass():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_094"
    assert scan["status"] == "COMPLETE"
    assert scan["discovery_source_reset"] is True
    assert scan["inherited_mechanism_as_requirement"] is False
    assert "SECOND_INDEPENDENT_BROAD_CURRENT_REALITY_SOURCE_RESET" in scan["search_mode"]
    assert "NO_JOB_GIG_RFQ_OR_PROCUREMENT_FEED_AS_DISCOVERY_ONTOLOGY" in scan["search_mode"]


def test_scan094_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("FRANCE_B2B_EINVOICING" in title for title in titles)
    assert any("US_PRIOR_AUTHORIZATION" in title for title in titles)
    assert any("STRANDED_OFFICE_ASSET" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan094_binds_reality_evidence_before_commercial_preflight():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert formation["observed_actor_state_change_evidence"]
        assert formation["objective_endowment_or_underuse_evidence"]
        assert formation["observed_behavior_or_workaround_evidence"]
        assert formation["contradiction_or_partial_flow_evidence"]
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan094_preserves_rights_and_execution_floors():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    france = formations["ATTRACTION_SCAN_094-F1"]
    prior_auth = formations["ATTRACTION_SCAN_094-F2"]
    office = formations["ATTRACTION_SCAN_094-F3"]
    assert france["machine_delegatability_check"].startswith("PASS_")
    assert "APPROVED_PLATFORM" in france["data_action_rights_check"]
    assert prior_auth["machine_delegatability_check"].startswith("PARTIAL_")
    assert "PAYER" in prior_auth["data_action_rights_check"]
    assert office["machine_delegatability_check"].startswith("PARTIAL_")
    assert office["founder_independence_check"].startswith("FAIL_")


def test_scan094_changes_evidence_source_not_product_mechanism():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_095"
    boundary = scan["next_search_boundary"]
    assert "PARTICIPANT_AUTHORED_CURRENT_REALITY_SOURCE_SHIFT" in boundary
    assert "INDEPENDENT_OBJECTIVE_CORROBORATION" in boundary
    assert "EXCLUDE_SCAN060_TO_094_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert scan["drift_audit"]["response"].startswith(
        "SHIFT_SCAN095_SOURCE_PRIORITY_TO_DIRECT_PARTICIPANT_AUTHORED"
    )


def test_scan094_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_094"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_094-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_095"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_095"
    assert (
        state["parallel_workstreams"]["discovery"]["search_boundary"]
        == scan["next_search_boundary"]
    )
