import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_105.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan105_requires_executed_transfer_and_post_transfer_economics():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_105"
    assert scan["status"] == "COMPLETE"
    assert scan["primary_research_domain"] == "CHINA"
    assert "EXECUTED_FRESH_OPERATOR_CONTROL_TRANSFER_PLUS_POST_TRANSFER_EXTERNAL_ECONOMIC_CONTINUITY_PASS" in scan["search_mode"]
    assert scan["drift_audit"]["executed_control_transfer_required"] is True
    assert scan["drift_audit"]["post_transfer_external_economic_continuity_required"] is True
    assert scan["drift_audit"]["fresh_small_operator_entry_required"] is True
    assert scan["drift_audit"]["normalized_economics_required"] is True


def test_scan105_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("GEL_BLASTER" in title for title in titles)
    assert any("PARCEL_STATION" in title for title in titles)
    assert any("SOURCE_CODE" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan105_distinguishes_transfer_money_from_founder_light_asset():
    scan = load(SCAN)
    f = {x["formation_id"]: x for x in scan["examined_formations"]}

    assert f["ATTRACTION_SCAN_105-F1"]["executed_control_transfer_check"].startswith("PASS_")
    assert f["ATTRACTION_SCAN_105-F1"]["post_transfer_external_economic_continuity_check"].startswith("PASS_")
    assert f["ATTRACTION_SCAN_105-F1"]["fresh_small_operator_entry_check"].startswith("FAIL_")
    assert f["ATTRACTION_SCAN_105-F1"]["founder_independence_check"].startswith("FAIL_")

    assert f["ATTRACTION_SCAN_105-F2"]["executed_control_transfer_check"].startswith("PASS_")
    assert f["ATTRACTION_SCAN_105-F2"]["post_transfer_external_economic_continuity_check"].startswith("PASS_")
    assert f["ATTRACTION_SCAN_105-F2"]["fresh_small_operator_entry_check"].startswith("PASS_")
    assert f["ATTRACTION_SCAN_105-F2"]["founder_independence_check"].startswith("FAIL_")
    assert f["ATTRACTION_SCAN_105-F2"]["normalized_margin_check"].startswith("FAIL_")

    assert f["ATTRACTION_SCAN_105-F3"]["executed_control_transfer_check"].startswith("UNKNOWN_TO_PARTIAL_")
    assert f["ATTRACTION_SCAN_105-F3"]["post_transfer_external_economic_continuity_check"].startswith("FAIL_")
    assert f["ATTRACTION_SCAN_105-F3"]["generic_agent_substitutability_check"].startswith("FAIL_")

    for formation in f.values():
        assert formation["economic_signal"]
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan105_repeats_floor_before_another_boundary_change():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_106"
    boundary = scan["next_search_boundary"]
    assert "SECOND_INDEPENDENT_EXECUTED_FRESH_OPERATOR_CONTROL_TRANSFER" in boundary
    assert "POST_TRANSFER_EXTERNAL_ECONOMIC_CONTINUITY" in boundary
    assert "NEW_OPERATOR_FULL_TIME_MANUAL_DELIVERY" in boundary
    assert "EXCLUDE_SCAN060_TO_105_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE" in boundary


def test_scan105_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_105"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_105-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_106"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_106"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
