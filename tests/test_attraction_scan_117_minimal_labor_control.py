import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_117.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def formations():
    scan = load(SCAN)
    return {x["formation_id"]: x for x in scan["examined_formations"]}


def test_scan117_uses_intrinsically_low_current_fte_boundary():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_117"
    assert scan["status"] == "COMPLETE"
    audit = scan["drift_audit"]
    assert audit["intrinsically_low_current_fte_priority_used"] is True
    assert audit["completed_control_change_required"] is True
    assert audit["clean_post_control_time_window_required"] is True
    assert audit["explicit_operating_cashflow_required"] is True
    assert audit["current_target_fte_required"] is True
    assert audit["no_project_field_manufacturing_after_sales_delivery_required"] is True


def test_scan117_remains_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {x["title"] for x in scan["examined_formations"]}
    assert any("SOFTWARE_RECYCLING" in x for x in titles)
    assert any("TRANSITIONAL_PUBLIC_SHELL" in x for x in titles)
    assert any("BAMBOO_MATERIALS" in x for x in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan117_tianwu_closes_low_fte_and_completed_control_but_fails_positive_ocf():
    f1 = formations()["ATTRACTION_SCAN_117-F1"]
    assert f1["executed_control_transfer_check"].startswith("PASS_")
    assert "99_9920_PERCENT" in f1["executed_control_transfer_check"]
    assert f1["owner_labor_check"].startswith("PASS_")
    assert "FTE_IS_11" in f1["owner_labor_check"]
    assert f1["post_transfer_external_economic_continuity_check"].startswith("FAIL_")
    assert "OPERATING_CASHFLOW_PER_SHARE_IS_NEGATIVE" in f1["post_transfer_external_economic_continuity_check"]
    assert f1["verdict"].startswith("DEMOTED_")


def test_scan117_henglilai_does_not_project_transitional_four_fte_shell_forward():
    f2 = formations()["ATTRACTION_SCAN_117-F2"]
    assert f2["executed_control_transfer_check"].startswith("FAIL_TO_CLOSE_")
    assert f2["owner_labor_check"].startswith("PASS_")
    assert "FTE_IS_4" in f2["owner_labor_check"]
    assert f2["post_transfer_external_economic_continuity_check"].startswith("FAIL_")
    assert "ZERO_REVENUE" in f2["post_transfer_external_economic_continuity_check"]
    assert f2["machine_delegatability_check"].startswith("FAIL_")


def test_scan117_yangzhu_rejects_temporary_voting_control_and_current_labor():
    f3 = formations()["ATTRACTION_SCAN_117-F3"]
    assert f3["executed_control_transfer_check"].startswith("PARTIAL_PASS_")
    assert "TIME_LIMITED_VOTING_RIGHT_DELEGATION" in f3["executed_control_transfer_check"]
    assert f3["owner_labor_check"].startswith("FAIL_")
    assert "FTE_IS_142" in f3["owner_labor_check"]
    assert f3["post_transfer_external_economic_continuity_check"].startswith("FAIL_TO_CLOSE_")
    assert f3["fresh_small_operator_entry_check"].startswith("FAIL_")


def test_scan117_advances_to_low_fte_positive_ocf_recurring_control_boundary():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_118"
    boundary = scan["next_search_boundary"]
    assert "LOW_FTE_POSITIVE_OCF_RECURRING_CONTROL_PASS" in boundary
    assert "EXISTING_RECURRING_LICENSE_ROYALTY_SUBSCRIPTION_AUTOMATED_TRANSACTION_OR_OTHER_REPEATABLE_NONPROJECT_FLOW" in boundary
    assert "EXCLUDE_SCAN060_TO_117_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary


def test_scan117_updates_reset_state_without_promotion():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_117"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_117-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_118"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_118"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
