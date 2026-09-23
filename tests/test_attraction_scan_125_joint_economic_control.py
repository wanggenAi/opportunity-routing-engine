import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_125.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan125_uses_joint_retrieval_without_relaxing_admission():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_125"
    assert scan["status"] == "COMPLETE"
    assert scan["zero_primary_admissions"] is False
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    audit = scan["drift_audit"]
    assert audit["joint_low_fte_positive_profit_positive_ocf_retrieval_used"] is True
    assert audit["positive_external_revenue_required"] is True
    assert audit["unknown_external_revenue_fail_closed"] is True


def test_hongqi_is_admitted_then_demoted_on_control_and_custom_delivery():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 1
    f1 = scan["examined_formations"][0]
    assert f1["formation_id"] == "ATTRACTION_SCAN_125-F1"
    assert f1["current_external_revenue_check"].startswith("PASS_")
    assert f1["executed_control_transfer_check"].startswith("FAIL_")
    assert f1["founder_independence_check"].startswith("FAIL_")
    assert f1["direct_operating_cost_check"].startswith("FAIL_")
    assert f1["machine_delegatability_check"].startswith("FAIL_")
    assert f1["verdict"].startswith("DEMOTED_")


def test_yike_joint_signal_fails_closed_on_external_revenue_identity():
    scan = load(SCAN)
    rows = {row["code"]: row for row in scan["screened_current_reports"]}
    yike = rows["873547"]
    assert yike["latest_direct_fte"] == 10
    assert yike["attributable_net_profit_rmb"] > 0
    assert yike["consolidated_ocf_rmb_approx_from_per_share"] > 0
    assert yike["retrieval_joint_signal"] is True
    assert yike["admission_result"] == "EXCLUDED_EXTERNAL_REVENUE_NOT_PROVEN_CURRENT_PERIOD"
    assert "UNKNOWN != PASS" in yike["exclusion_detail"]


def test_fresh_low_fte_partial_matches_fail_economic_legs():
    scan = load(SCAN)
    rows = {row["code"]: row for row in scan["screened_current_reports"]}
    assert rows["873633"]["latest_direct_fte"] == 20
    assert rows["873633"]["consolidated_ocf_rmb_approx_from_per_share"] < 0
    assert rows["872691"]["latest_direct_fte"] == 3
    assert rows["872691"]["consolidated_ocf_rmb_approx_from_per_share"] < 0
    assert rows["400179"]["current_fte"] == 13
    assert rows["400179"]["attributable_net_profit_rmb"] < 0
    assert rows["400179"]["consolidated_ocf_rmb"] < 0
    assert rows["874263"]["latest_direct_fte"] == 15
    assert rows["874263"]["attributable_net_profit_rmb"] < 0


def test_scan125_promotes_replicated_fresh_control_bottleneck_to_scan126_entry_gate():
    scan = load(SCAN)
    audit = scan["drift_audit"]
    assert audit["completed_fresh_operator_control_reproduced_as_bottleneck_by_new_admitted_survivor"] is True
    assert audit["fresh_operator_control_promoted_to_next_scan_primary_admission_gate"] is True
    boundary = scan["next_search_boundary"]
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_126"
    assert "COMPLETED_FRESH_OPERATOR_REPRODUCIBLE_CONTROL_BEFORE_REPORTING_PERIOD_BEFORE_PRIMARY_FORMATION_ADMISSION" in boundary
    assert "EXCLUDE_SCAN060_TO_125_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary


def test_scan125_updates_machine_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_125"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_125-F1"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_126"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_126"
    assert state["parallel_workstreams"]["discovery"]["scan125_earned_cashflow_asset_boundary"] == scan["next_search_boundary"]\n    assert "SCAN126_PRECEDENT_CALIBRATED_BROAD_REALITY" in state["parallel_workstreams"]["discovery"]["search_boundary"]
