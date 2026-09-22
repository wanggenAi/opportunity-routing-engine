import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_118.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def formations():
    scan = load(SCAN)
    return {x["formation_id"]: x for x in scan["examined_formations"]}


def test_scan118_requires_current_post_control_low_fte_positive_ocf():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_118"
    assert scan["status"] == "COMPLETE"
    audit = scan["drift_audit"]
    assert audit["low_fte_positive_ocf_recurring_control_priority_used"] is True
    assert audit["completed_control_before_reporting_period_required"] is True
    assert audit["current_post_control_report_required"] is True
    assert audit["explicit_positive_operating_cashflow_required"] is True
    assert audit["current_or_latest_intrinsically_low_fte_required"] is True
    assert audit["existing_repeatable_nonproject_revenue_required"] is True


def test_scan118_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {x["title"] for x in scan["examined_formations"]}
    assert any("10_FTE_SOFTWARE" in x for x in titles)
    assert any("INFORMATION_TECH_51_PERCENT_CONTROL" in x for x in titles)
    assert any("RELATED_GROUP_67_PERCENT_CONTROL" in x for x in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan118_leyou_does_not_relabel_pre_control_positive_ocf():
    f1 = formations()["ATTRACTION_SCAN_118-F1"]
    assert f1["executed_control_transfer_check"].startswith("PASS_")
    assert "2025_12_29" in f1["executed_control_transfer_check"]
    assert f1["owner_labor_check"].startswith("PASS_")
    assert "10_EMPLOYEES" in f1["owner_labor_check"]
    assert f1["post_transfer_external_economic_continuity_check"].startswith("FAIL_TO_CLOSE_")
    assert "2025_POSITIVE_REVENUE_PROFIT_OCF_ARE_NOT_RELABELED_POST_CONTROL" in f1["post_transfer_external_economic_continuity_check"]


def test_scan118_haitu_preserves_ocf_and_purchase_date_conflict_and_still_fails_labor_capital():
    f2 = formations()["ATTRACTION_SCAN_118-F2"]
    assert f2["executed_control_transfer_check"].startswith("PASS_")
    assert "2026_02_01_PURCHASE_DATE" in f2["executed_control_transfer_check"]
    assert f2["post_transfer_external_economic_continuity_check"].startswith("PARTIAL_PASS_")
    assert "OCF_POSITIVE_RMB3_8282M" in f2["post_transfer_external_economic_continuity_check"]
    assert f2["owner_labor_check"].startswith("FAIL_")
    assert "113_EMPLOYEES" in f2["owner_labor_check"]
    assert f2["fresh_small_operator_entry_check"].startswith("FAIL_")


def test_scan118_taizhong_binds_current_financials_but_fails_ocf_and_fresh_operator():
    f3 = formations()["ATTRACTION_SCAN_118-F3"]
    assert f3["executed_control_transfer_check"].startswith("PASS_")
    assert "RELATED_GROUP_RESTRUCTURING" in f3["executed_control_transfer_check"]
    assert f3["post_transfer_external_economic_continuity_check"].startswith("FAIL_")
    assert "NEGATIVE_RMB43_7289M" in f3["post_transfer_external_economic_continuity_check"]
    assert f3["same_operator_economic_binding_check"].startswith("PASS_")
    assert f3["owner_labor_check"].startswith("FAIL_")
    assert "FTE_IS_323" in f3["owner_labor_check"]
    assert f3["fresh_small_operator_entry_check"].startswith("FAIL_")


def test_scan118_advances_to_current_report_low_fte_unambiguous_positive_ocf_boundary():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_119"
    boundary = scan["next_search_boundary"]
    assert "CURRENT_POST_CONTROL_LOW_FTE_UNAMBIGUOUS_POSITIVE_OCF_RECURRING_CONTROL_PASS" in boundary
    assert "CURRENT_POST_CONTROL_REPORT_AVAILABLE" in boundary
    assert "UNAMBIGUOUS_POSITIVE_OPERATING_CASHFLOW_RECONCILED" in boundary
    assert "EXCLUDE_SCAN060_TO_118_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary


def test_scan118_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_118"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_118-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_119"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_119"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
