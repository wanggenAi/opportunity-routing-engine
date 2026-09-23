import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_126.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan126_promotes_fresh_control_to_admission_and_preserves_zero_result():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_126"
    assert scan["status"] == "COMPLETE"
    assert scan["zero_primary_admissions"] is True
    assert scan["examined_formations"] == []
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    audit = scan["drift_audit"]
    assert audit["completed_fresh_operator_control_primary_admission_gate"] is True
    assert audit["control_must_precede_reporting_period"] is True
    assert audit["zero_primary_admissions_preserved_without_fabricating_a_formation"] is True


def test_shengchu_is_nearest_packet_but_fails_current_profit():
    scan = load(SCAN)
    rows = {row["code"]: row for row in scan["screened_current_reports"]}
    row = rows["430572"]
    assert row["control_before_reporting_period"] is True
    assert row["fresh_operator_control_signal"] is True
    assert row["current_fte"] == 9
    assert row["revenue_rmb"] > 0
    assert row["consolidated_ocf_rmb"] > 0
    assert row["attributable_net_profit_rmb"] < 0
    assert row["admission_result"] == "EXCLUDED_NET_PROFIT_FAIL"


def test_control_gate_rejects_in_period_or_nonultimate_changes():
    scan = load(SCAN)
    rows = {row["code"]: row for row in scan["screened_current_reports"]}
    zhc = rows["874647"]
    assert zhc["control_before_reporting_period"] is False
    assert zhc["net_profit_rmb"] > 0
    assert zhc["consolidated_ocf_rmb"] > 0
    assert zhc["current_fte"] == 397
    tonghai = rows["833930"]
    assert tonghai["fresh_operator_control_signal"] is False
    assert "NO_FRESH_ULTIMATE_CONTROL" in tonghai["admission_result"]


def test_fresh_control_does_not_override_low_fte_profit_or_ocf():
    scan = load(SCAN)
    rows = {row["code"]: row for row in scan["screened_current_reports"]}
    tangbang = rows["832765"]
    assert tangbang["fresh_operator_control_signal"] is True
    assert tangbang["current_fte"] == 27
    assert tangbang["attributable_net_profit_rmb"] < 0
    assert tangbang["consolidated_ocf_rmb"] < 0
    longchuang = rows["870895"]
    assert longchuang["current_fte"] == 26
    assert longchuang["attributable_net_profit_rmb"] < 0
    assert longchuang["consolidated_ocf_rmb"] < 0
    gaohua = rows["833063"]
    assert gaohua["net_profit_rmb"] < 0
    assert gaohua["consolidated_ocf_rmb"] < 0


def test_scan126_advances_same_constitution_with_tighter_scan127_retrieval():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_127"
    boundary = scan["next_search_boundary"]
    assert "COMPLETED_FRESH_OPERATOR_REPRODUCIBLE_ULTIMATE_CONTROL_BEFORE_REPORTING_PERIOD" in boundary
    assert "INTRINSICALLY_LOW_FTE" in boundary
    assert "POSITIVE_EXTERNAL_REVENUE" in boundary
    assert "POSITIVE_NET_PROFIT" in boundary
    assert "POSITIVE_CONSOLIDATED_OPERATING_CASHFLOW" in boundary
    assert "EXCLUDE_SCAN060_TO_126_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary


def test_scan126_updates_machine_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_126"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_125-F1"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_127"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_127"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
