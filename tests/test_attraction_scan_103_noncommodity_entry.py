import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_103.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan103_requires_noncommodity_operator_specific_control_and_money():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_103"
    assert scan["status"] == "COMPLETE"
    assert scan["primary_research_domain"] == "CHINA"
    assert "OPERATOR_ACQUIRABLE_NON_COMMODITY_CONTROL_PLUS_EXTERNAL_ECONOMIC_MOTION_PASS" in scan["search_mode"]
    assert scan["drift_audit"]["operator_specific_noncommodity_control_required"] is True
    assert scan["drift_audit"]["operator_acquirable_control_required"] is True
    assert scan["drift_audit"]["external_economic_motion_required"] is True


def test_scan103_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("OPEN_SOURCE_REPUTATION" in title for title in titles)
    assert any("CREATOR_AUDIENCE" in title for title in titles)
    assert any("SEO_SITE" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan103_noncommodity_control_does_not_bypass_entry_acquirability():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}

    assert formations["ATTRACTION_SCAN_103-F1"]["noncommodity_control_check"].startswith("PASS_")
    assert formations["ATTRACTION_SCAN_103-F1"]["operator_acquirability_check"].startswith("FAIL_")

    assert formations["ATTRACTION_SCAN_103-F2"]["noncommodity_control_check"].startswith("PASS_")
    assert formations["ATTRACTION_SCAN_103-F2"]["operator_acquirability_check"].startswith("FAIL_")

    assert formations["ATTRACTION_SCAN_103-F3"]["noncommodity_control_check"].startswith("UNKNOWN_TO_PARTIAL_")
    assert formations["ATTRACTION_SCAN_103-F3"]["operator_acquirability_check"].startswith("FAIL_")

    for formation in formations.values():
        assert formation["economic_signal"]
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan103_requires_second_independent_pass_before_boundary_change():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_104"
    boundary = scan["next_search_boundary"]
    assert "SECOND_INDEPENDENT_OPERATOR_ACQUIRABLE_NON_COMMODITY_CONTROL_PLUS_EXTERNAL_ECONOMIC_MOTION_PASS" in boundary
    assert "FRESH_INDEPENDENT_SMALL_OPERATOR" in boundary
    assert "EXCLUDE_SCAN060_TO_103_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE" in boundary


def test_scan103_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_103"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_103-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_104"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_104"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
