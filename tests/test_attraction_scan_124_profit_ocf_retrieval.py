import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_124.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan124_preserves_strict_admission_and_zero_primary_result():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_124"
    assert scan["status"] == "COMPLETE"
    assert scan["zero_primary_admissions"] is True
    assert scan["examined_formations"] == []
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []

    audit = scan["drift_audit"]
    assert audit["strict_current_economic_conjunction_primary_admission"] is True
    assert audit["positive_profit_and_positive_ocf_retrieval_prioritized"] is True
    assert audit["zero_primary_admissions_preserved_without_fabricating_a_formation"] is True


def test_scan124_profit_ocf_positive_retrievals_fail_low_fte_gate():
    scan = load(SCAN)
    rows = {row["entity"]: row for row in scan["screened_current_reports"]}

    for name in [
        "国瑞税务 / 北京国瑞税务师事务所有限公司",
        "恒信通 / 安徽恒信通智能科技股份有限公司",
        "鑫光正 / 青岛鑫光正钢结构股份有限公司",
    ]:
        row = rows[name]
        assert row["revenue_rmb"] > 0
        assert row["net_profit_rmb"] > 0
        assert row["consolidated_ocf_rmb"] > 0
        assert row["current_fte"] > 20
        assert row["admission_result"] == "EXCLUDED_INTRINSICALLY_LOW_FTE_FAIL"


def test_scan124_low_fte_packets_still_fail_profit_or_ocf():
    scan = load(SCAN)
    rows = {row["entity"]: row for row in scan["screened_current_reports"]}

    st_deepsea = rows["ST深海 / 广州深海软件股份有限公司"]
    assert st_deepsea["current_fte"] == 16
    assert st_deepsea["net_profit_rmb"] < 0
    assert st_deepsea["consolidated_ocf_rmb"] > 0

    zeshang = rows["择尚科技 / 无锡择尚科技股份有限公司"]
    assert zeshang["current_fte"] == 14
    assert zeshang["net_profit_rmb"] > 0
    assert zeshang["consolidated_ocf_rmb"] < 0

    shangyang = rows["尚洋信息 / 北京尚洋易捷信息技术股份有限公司"]
    assert shangyang["current_fte"] == 11
    assert shangyang["net_profit_rmb"] < 0
    assert shangyang["consolidated_ocf_rmb"] < 0


def test_scan124_spends_no_control_research_and_keeps_nonmanufacturing_diversity():
    scan = load(SCAN)
    assert len(scan["screened_current_reports"]) == 6
    assert scan["examined_formations"] == []
    excluded = "\n".join(scan["excluded_observations"])
    assert "No control-history deepening" in excluded
    assert scan["drift_audit"]["fresh_nonmanufacturing_routes_included"] is True


def test_scan124_advances_to_joint_signal_scan125_without_relaxing_constitution():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_125"
    boundary = scan["next_search_boundary"]
    assert "STRICT_CURRENT_ECONOMIC_CONJUNCTION_PRIMARY_ADMISSION_REPEAT" in boundary
    assert "JOINT_LOW_FTE_POSITIVE_PROFIT_POSITIVE_OCF_RETRIEVAL_SIGNALS" in boundary
    assert "EXCLUDE_SCAN060_TO_124_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE_FAIL_CLOSED" in boundary


def test_scan124_updates_reset_state_without_changing_last_resolved_formation():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_124"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_122-F2"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_125"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_125"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
