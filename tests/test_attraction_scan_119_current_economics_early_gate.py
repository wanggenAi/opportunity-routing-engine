import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_119.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def formations():
    scan = load(SCAN)
    return {x["formation_id"]: x for x in scan["examined_formations"]}


def test_scan119_enforces_early_current_economics_gates():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_119"
    assert scan["status"] == "COMPLETE"
    audit = scan["drift_audit"]
    assert audit["current_post_control_report_required"] is True
    assert audit["completed_control_before_reporting_period_required"] is True
    assert audit["direct_current_or_latest_intrinsically_low_fte_required"] is True
    assert audit["positive_net_profit_required"] is True
    assert audit["explicit_positive_operating_cashflow_required"] is True
    assert audit["unambiguous_positive_ocf_reconciliation_required"] is True
    assert audit["early_gate_failure_stops_unnecessary_deepening"] is True


def test_scan119_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {x["title"] for x in scan["examined_formations"]}
    assert any("8_FTE_INDIRECT_CONTROL" in x for x in titles)
    assert any("81_26_PERCENT_PROPOSED_CONTROL_TERMINATED" in x for x in titles)
    assert any("15_FTE_MEDIA_CONTROL_COMPLETED_INSIDE_H1" in x for x in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan119_jintian_passes_control_and_low_fte_but_fails_profit_and_ocf():
    f1 = formations()["ATTRACTION_SCAN_119-F1"]
    assert f1["executed_control_transfer_check"].startswith("PASS_")
    assert "2024_10_18" in f1["executed_control_transfer_check"]
    assert f1["owner_labor_check"].startswith("PASS_")
    assert "COUNT_IS_8" in f1["owner_labor_check"]
    assert f1["post_transfer_external_economic_continuity_check"].startswith("FAIL_")
    assert "NET_LOSS_IS_RMB604400_80" in f1["post_transfer_external_economic_continuity_check"]
    assert "NEGATIVE_RMB2_546914_06" in f1["post_transfer_external_economic_continuity_check"]
    assert f1["direct_operating_cost_check"].startswith("FAIL_")


def test_scan119_longjoy_does_not_relabel_signed_acquisition_as_executed_control():
    f2 = formations()["ATTRACTION_SCAN_119-F2"]
    assert f2["executed_control_transfer_check"].startswith("FAIL_")
    assert "TERMINATED_2026_06_09" in f2["executed_control_transfer_check"]
    assert "HAD_NOT_PAID" in f2["executed_control_transfer_check"]
    assert f2["owner_labor_check"].startswith("PASS_")
    assert "COUNT_IS_8" in f2["owner_labor_check"]
    assert f2["post_transfer_external_economic_continuity_check"].startswith("NOT_APPLICABLE_")
    assert f2["normalized_margin_check"].startswith("FAIL_")


def test_scan119_yudu_rejects_intra_period_control_and_project_delivery_early():
    f3 = formations()["ATTRACTION_SCAN_119-F3"]
    assert f3["executed_control_transfer_check"].startswith("FAIL_CLEAN_WINDOW_")
    assert "2026_02_09" in f3["executed_control_transfer_check"]
    assert "INSIDE_2026_H1" in f3["executed_control_transfer_check"]
    assert f3["post_transfer_external_economic_continuity_check"].startswith("FAIL_TO_CLOSE_")
    assert "NEGATIVE_RMB433179_59" in f3["post_transfer_external_economic_continuity_check"]
    assert f3["direct_operating_cost_check"].startswith("FAIL_")
    assert "FIELD_PROMOTION_PROJECT" in f3["direct_operating_cost_check"]


def test_scan119_inverts_scan120_retrieval_order_without_relaxing_control_gate():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_120"
    boundary = scan["next_search_boundary"]
    assert "CURRENT_LOW_FTE_POSITIVE_PROFIT_POSITIVE_OCF_FIRST_THEN_EXECUTED_CONTROL_PASS" in boundary
    assert "COMPLETED_FRESH_OPERATOR_REPRODUCIBLE_CONTROL_BEFORE_REPORTING_PERIOD" in boundary
    assert "EXCLUDE_SCAN060_TO_119_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE_FAIL_CLOSED" in boundary


def test_scan119_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_119"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_119-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_120"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_120"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
