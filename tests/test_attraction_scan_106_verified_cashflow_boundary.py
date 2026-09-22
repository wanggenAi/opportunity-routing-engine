import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_106.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan106_repeats_executed_transfer_continuity_floor():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_106"
    assert scan["status"] == "COMPLETE"
    assert scan["primary_research_domain"] == "CHINA"
    assert "SECOND_INDEPENDENT_EXECUTED_FRESH_OPERATOR_CONTROL_TRANSFER" in scan["search_mode"]
    assert scan["drift_audit"]["executed_control_transfer_required"] is True
    assert scan["drift_audit"]["post_transfer_external_economic_continuity_required"] is True
    assert scan["drift_audit"]["new_operator_full_time_manual_delivery_explicit_fail"] is True


def test_scan106_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("SODIUM_ION" in title for title in titles)
    assert any("HERITAGE_IP" in title for title in titles)
    assert any("SOLAR_PROJECT" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan106_distinguishes_external_motion_from_small_operator_fit():
    scan = load(SCAN)
    f = {x["formation_id"]: x for x in scan["examined_formations"]}

    assert f["ATTRACTION_SCAN_106-F1"]["executed_control_transfer_check"].startswith("PASS_")
    assert f["ATTRACTION_SCAN_106-F1"]["post_transfer_external_economic_continuity_check"].startswith("PARTIAL_PASS_")
    assert f["ATTRACTION_SCAN_106-F1"]["founder_independence_check"].startswith("FAIL_")

    assert f["ATTRACTION_SCAN_106-F2"]["executed_control_transfer_check"].startswith("PASS_")
    assert f["ATTRACTION_SCAN_106-F2"]["post_transfer_external_economic_continuity_check"].startswith("PASS_")
    assert f["ATTRACTION_SCAN_106-F2"]["fresh_small_operator_entry_check"].startswith("FAIL_")

    assert f["ATTRACTION_SCAN_106-F3"]["executed_control_transfer_check"].startswith("PASS_")
    assert f["ATTRACTION_SCAN_106-F3"]["post_transfer_external_economic_continuity_check"].startswith("UNKNOWN_TO_PARTIAL_")
    assert f["ATTRACTION_SCAN_106-F3"]["fresh_small_operator_entry_check"].startswith("FAIL_")

    for formation in f.values():
        assert formation["economic_signal"]
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan106_advances_to_verified_net_cashflow_boundary():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_107"
    boundary = scan["next_search_boundary"]
    assert "FRESH_SMALL_OPERATOR_VERIFIED_NET_CASHFLOW_CONTROL_PASS" in boundary
    assert "POST_TRANSFER_RECEIVED_EXTERNAL_CUSTOMER_REVENUE" in boundary
    assert "DIRECT_OPERATING_COSTS_OWNER_LABOR" in boundary
    assert "NO_LARGE_ORGANIZATION_OR_INFRASTRUCTURE_CAPITAL_DEPENDENCE" in boundary
    assert "EXCLUDE_SCAN060_TO_106_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary


def test_scan106_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_106"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_106-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_107"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_107"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
