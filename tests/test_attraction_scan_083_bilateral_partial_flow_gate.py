import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_083.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan083_starts_from_observed_bilateral_partial_flow():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_083"
    assert scan["status"] == "COMPLETE"
    assert "BILATERAL_PARTIAL_FLOW_FIRST" in scan["search_mode"]
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["drift_audit"]["discovery_started_from_bilateral_partial_flow"] is True
    assert scan["drift_audit"]["replenishing_a_and_b_populations_required"] is True


def test_scan083_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("SURPLUS_FOOD" in title for title in titles)
    assert any("SURPLUS_SOIL" in title for title in titles)
    assert any("EV_CHARGER" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan083_requires_two_replenishing_sides_and_real_flow_evidence():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert formation["actor_a_population"]
        assert formation["actor_b_population"]
        assert len(formation["repeated_partial_flow_evidence"]) >= 2
        assert len(formation["connection_pressure_or_workaround"]) >= 2


def test_scan083_fails_closed_on_current_exact_control_surfaces():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    assert any("MealConnect" in x for x in formations["ATTRACTION_SCAN_083-F1"]["exact_incumbent_and_control_surface_preflight"])
    assert any("Soil Connect" in x for x in formations["ATTRACTION_SCAN_083-F2"]["exact_incumbent_and_control_surface_preflight"])
    assert any("JustPark" in x for x in formations["ATTRACTION_SCAN_083-F3"]["exact_incumbent_and_control_surface_preflight"])
    assert all(f["verdict"].startswith("DEMOTED_") for f in scan["examined_formations"])


def test_scan083_requires_second_independent_bilateral_pass():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_084"
    boundary = scan["next_search_boundary"]
    assert "SECOND_INDEPENDENT_BILATERAL_PARTIAL_FLOW_FIRST" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary


def test_scan083_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_083"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_083-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_084"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_084"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
