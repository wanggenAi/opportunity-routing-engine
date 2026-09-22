import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_102.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan102_repeats_operator_acquirability_and_external_economics():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_102"
    assert scan["status"] == "COMPLETE"
    assert scan["primary_research_domain"] == "CHINA"
    assert "SECOND_INDEPENDENT_OPERATOR_ACQUIRABLE_CONTROL_PLUS_EXTERNAL_ECONOMIC_MOTION_PASS" in scan["search_mode"]
    assert scan["drift_audit"]["operator_acquirable_control_required"] is True
    assert scan["drift_audit"]["external_economic_motion_required"] is True


def test_scan102_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("SELF_SERVICE_CAR_WASH" in title for title in titles)
    assert any("EV_CHARGING" in title for title in titles)
    assert any("GROUP_EXPENSE_MINIPROGRAM" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan102_all_examined_controls_are_acquirable_and_money_bound():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert formation["operator_acquirability_check"].startswith("PASS_")
        assert formation["economic_signal"]
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan102_derives_noncommodity_operator_specific_next_boundary():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_103"
    boundary = scan["next_search_boundary"]
    assert "OPERATOR_ACQUIRABLE_NON_COMMODITY_CONTROL_PLUS_EXTERNAL_ECONOMIC_MOTION_PASS" in boundary
    assert "OPERATOR_SPECIFIC_ASYMMETRY_OR_COMPOUNDING_DISTRIBUTION" in boundary
    assert "EXCLUDE_SCAN060_TO_102_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE" in boundary


def test_scan102_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_102"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_102-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_103"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_103"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
