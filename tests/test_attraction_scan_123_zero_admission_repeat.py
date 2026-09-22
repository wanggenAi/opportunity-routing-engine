import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_123.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan123_preserves_strict_admission_without_fabricating_a_formation():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_123"
    assert scan["status"] == "COMPLETE"
    assert scan["zero_primary_admissions"] is True
    assert scan["examined_formations"] == []
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []

    audit = scan["drift_audit"]
    assert audit["strict_current_economic_conjunction_primary_admission"] is True
    assert audit["independent_repeat_of_scan122"] is True
    assert audit["zero_primary_admissions_preserved_without_fabricating_a_formation"] is True
    assert audit["no_arbitrary_fixed_primary_formation_count"] is True


def test_scan123_includes_fresh_nonmanufacturing_routes_but_none_pass_all_economic_legs():
    scan = load(SCAN)
    rows = {row["entity"]: row for row in scan["screened_current_reports"]}
    assert len(rows) == 6

    mokylin = rows["墨麟股份 / 深圳墨麟科技股份有限公司"]
    assert mokylin["current_fte"] == 10
    assert mokylin["revenue_rmb"] > 0
    assert mokylin["net_profit_rmb"] < 0
    assert mokylin["consolidated_ocf_rmb"] < 0

    qianxiang = rows["千想传媒"]
    assert qianxiang["current_fte"] == 19
    assert qianxiang["revenue_rmb"] > 0
    assert qianxiang["net_profit_rmb"] > 0
    assert qianxiang["consolidated_ocf_rmb"] < 0

    zhongshi = rows["中食花泽"]
    assert zhongshi["current_fte"] == 16
    assert zhongshi["revenue_rmb"] > 0
    assert zhongshi["net_profit_rmb"] < 0
    assert zhongshi["consolidated_ocf_rmb"] > 0

    game_routes = [
        row for row in rows.values()
        if "NETWORK_GAME" in row["route_class"]
    ]
    assert len(game_routes) == 2
    assert scan["drift_audit"]["fresh_nonmanufacturing_routes_included"] is True


def test_scan123_records_only_early_exclusions_and_spends_no_control_research():
    scan = load(SCAN)
    excluded = "\n".join(scan["excluded_observations"])
    for name in ["墨麟股份", "千想传媒", "中食花泽", "正扬股份", "ST义众实", "壹柒伍"]:
        assert name in excluded
    assert "No control-history deepening" in excluded
    assert scan["examined_formations"] == []


def test_scan123_does_not_promote_control_gate_without_a_second_survivor():
    scan = load(SCAN)
    audit = scan["drift_audit"]
    assert audit[
        "completed_fresh_operator_control_not_promoted_to_entry_gate_without_second_survivor"
    ] is True
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_124"
    boundary = scan["next_search_boundary"]
    assert "STRICT_CURRENT_ECONOMIC_CONJUNCTION_PRIMARY_ADMISSION_REPEAT" in boundary
    assert "PRIORITIZE_POSITIVE_PROFIT_AND_POSITIVE_OCF_RETRIEVAL_SIGNALS" in boundary
    assert "EXCLUDE_SCAN060_TO_123_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE_FAIL_CLOSED" in boundary


def test_scan123_updates_reset_state_without_changing_last_resolved_formation():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_123"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_122-F2"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_124"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_124"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
