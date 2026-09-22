import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_087.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan087_requires_independent_replication_and_participant_control():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_087"
    assert scan["status"] == "COMPLETE"
    assert "INDEPENDENTLY_REPLICATED_PARTICIPANT_CONTROLLED_COMPLETION" in scan["search_mode"]
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["drift_audit"]["independent_replication_floor"].startswith("PASS_")
    assert scan["drift_audit"]["decisive_completion_control_floor"].startswith("PASS_")


def test_scan087_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("TRAVELER_ESIM" in title for title in titles)
    assert any("XFINITY_GATEWAY_ROUTING" in title for title in titles)
    assert any("ROKU_TV_HOME_SURFACE" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan087_each_formation_has_replicated_success_reason_and_open_completion():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert len(formation["available_exact_control_surface"]) >= 2
        assert len(formation["independent_replication"]) >= 2
        assert len(formation["participant_authored_successful_completion"]) >= 2
        assert len(formation["explicit_participant_bypass_or_incompleteness_reason"]) >= 2
        assert formation["bypass_reason_class"]
        assert formation["decisive_completion_control"].startswith("PASS_")
        assert formation["repeated_bilateral_value_transfer"].startswith("PASS_")


def test_scan087_closes_mature_substitutes_without_commercial_promotion():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    assert "MATURE_SELF_SERVICE_CONNECTIVITY_CATEGORY" in formations["ATTRACTION_SCAN_087-F1"]["verdict"]
    assert "XFINITY_ALREADY_SUPPORTS_THE_HANDOFF" in formations["ATTRACTION_SCAN_087-F2"]["verdict"]
    assert "MATURE_SUBSTITUTE_CONTROL_SURFACE" in formations["ATTRACTION_SCAN_087-F3"]["verdict"]
    assert all(f["verdict"].startswith("DEMOTED_") for f in scan["examined_formations"])


def test_scan087_advances_to_multi_component_completion_without_mechanism_inheritance():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_088"
    boundary = scan["next_search_boundary"]
    assert "INDEPENDENTLY_REPLICATED_PARTICIPANT_CONTROLLED_MULTI_COMPONENT_COMPLETION" in boundary
    assert "TWO_OR_MORE_EXISTING_COMPONENTS" in boundary
    assert "NO_SINGLE_CURRENT_CONTROL_SURFACE_OWNS_THE_END_TO_END_OUTCOME" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary


def test_scan087_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_087"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_087-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_088"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_088"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
