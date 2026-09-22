import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_112.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan112_uses_low_headcount_machine_light_control_priority():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_112"
    assert scan["status"] == "COMPLETE"
    assert "LOW_HEADCOUNT_MACHINE_LIGHT_EXECUTED_CONTROL_PRIORITY" in scan["search_mode"]
    audit = scan["drift_audit"]
    assert audit["low_headcount_machine_light_executed_control_priority_used"] is True
    assert audit["same_operator_and_control_position_binding_required"] is True
    assert audit["executed_control_change_required"] is True
    assert audit["transfer_market_used_only_as_control_validation"].startswith("PASS_")


def test_scan112_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {x["title"] for x in scan["examined_formations"]}
    assert any("SOLAR_SPV" in x for x in titles)
    assert any("HOTEL_PROPERTY_WRAPPER" in x for x in titles)
    assert any("WASTEWATER_CONCESSION" in x for x in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan112_does_not_confuse_low_headcount_with_machine_delivery():
    scan = load(SCAN)
    f = {x["formation_id"]: x for x in scan["examined_formations"]}

    solar = f["ATTRACTION_SCAN_112-F1"]
    assert solar["same_operator_economic_binding_check"].startswith("PASS_")
    assert solar["executed_control_transfer_check"].startswith("FAIL_")
    assert solar["owner_labor_check"].startswith("UNKNOWN_")
    assert solar["machine_delegatability_check"].startswith("PARTIAL_TO_FAIL_")

    hotel = f["ATTRACTION_SCAN_112-F2"]
    assert hotel["founder_independence_check"].startswith("PARTIAL_PASS_")
    assert hotel["machine_delegatability_check"].startswith("FAIL_")
    assert hotel["executed_control_transfer_check"].startswith("FAIL_")

    water = f["ATTRACTION_SCAN_112-F3"]
    assert water["data_action_rights_check"].startswith("PASS_")
    assert water["machine_delegatability_check"].startswith("FAIL_")
    assert water["executed_control_transfer_check"].startswith("FAIL_")


def test_scan112_separates_transfer_path_from_executed_control():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert formation["executed_control_transfer_check"].startswith("FAIL_")
        assert formation["post_transfer_external_economic_continuity_check"].startswith("UNKNOWN_")
        assert formation["verdict"].startswith("DEMOTED_")
    assert any(
        "LISTING_APPROVAL_TRANSFERABILITY" in x
        for x in scan["scan_learnings"]
    )


def test_scan112_advances_to_completed_control_plus_post_transfer_cashflow():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_113"
    boundary = scan["next_search_boundary"]
    assert "EXECUTED_CONTROL_PLUS_POST_TRANSFER_CASHFLOW_PRIORITY" in boundary
    assert "COMPLETED_CONTROLLING_EQUITY_ASSET_LICENSE_OR_CONTRACT_TRANSFER" in boundary
    assert "POST_TRANSFER_POSITIVE_EXTERNAL_CUSTOMER_REVENUE" in boundary
    assert "EXCLUDE_SCAN060_TO_112_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary


def test_scan112_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_112"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_112-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_113"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_113"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
