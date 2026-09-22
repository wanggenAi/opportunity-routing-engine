import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_120.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def formations():
    scan = load(SCAN)
    return {x["formation_id"]: x for x in scan["examined_formations"]}


def test_scan120_inverts_retrieval_order_without_lowering_the_floor():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_120"
    assert scan["status"] == "COMPLETE"
    audit = scan["drift_audit"]
    assert audit["retrieval_order_inverted_to_current_economics_first"] is True
    assert audit["current_same_entity_report_required"] is True
    assert audit["direct_current_or_latest_intrinsically_low_fte_required"] is True
    assert audit["positive_external_revenue_required"] is True
    assert audit["positive_net_profit_required"] is True
    assert audit["explicit_positive_operating_cashflow_required"] is True
    assert audit["control_history_deepened_only_after_current_economics_pass"] is True
    assert audit["fresh_operator_reproducibility_required"] is True


def test_scan120_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {x["title"] for x in scan["examined_formations"]}
    assert any("10_FTE_POSITIVE_PROFIT_POSITIVE_OCF_FRESH_35_PERCENT_CONTROL" in x for x in titles)
    assert any("12_FTE_POSITIVE_PROFIT_POSITIVE_OCF_INTERNET_AD_MEDIA_BUYING" in x for x in titles)
    assert any("8_FTE_POSITIVE_OCF_BUT_ZERO_EXTERNAL_REVENUE" in x for x in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan120_tianlu_is_a_real_economics_and_fresh_control_survivor_but_not_founder_light():
    f1 = formations()["ATTRACTION_SCAN_120-F1"]
    assert f1["executed_control_transfer_check"].startswith("PASS_")
    assert "35_PERCENT_CONTROL" in f1["executed_control_transfer_check"]
    assert "RMB1_1511M" in f1["executed_control_transfer_check"]
    assert f1["post_transfer_external_economic_continuity_check"].startswith("PASS_")
    assert "RMB3_045_201_52" in f1["post_transfer_external_economic_continuity_check"]
    assert "RMB2_318_577_59" in f1["post_transfer_external_economic_continuity_check"]
    assert "RMB3_886_851_84" in f1["post_transfer_external_economic_continuity_check"]
    assert f1["owner_labor_check"].startswith("PASS_")
    assert "COUNT_IS_10" in f1["owner_labor_check"]
    assert f1["founder_independence_check"].startswith("FAIL_")
    assert f1["machine_delegatability_check"].startswith("FAIL_")


def test_scan120_huajin_passes_current_economics_but_fails_fresh_operator_control():
    f2 = formations()["ATTRACTION_SCAN_120-F2"]
    assert f2["owner_labor_check"].startswith("PASS_")
    assert "COUNT_IS_12" in f2["owner_labor_check"]
    assert f2["executed_control_transfer_check"].startswith("FAIL_")
    assert "LONGSTANDING" in f2["executed_control_transfer_check"]
    assert "SINCE_2009" in f2["executed_control_transfer_check"]
    assert f2["post_transfer_external_economic_continuity_check"].startswith("NOT_APPLICABLE_")
    signal = " ".join(f2["economic_signal"])
    assert "RMB97,644,344.98" in signal
    assert "RMB805,499.59" in signal
    assert "RMB4,177,203.45" in signal


def test_scan120_jiazhi_does_not_treat_positive_ocf_as_customer_cashflow():
    f3 = formations()["ATTRACTION_SCAN_120-F3"]
    assert f3["owner_labor_check"].startswith("PASS_")
    assert "COUNT_IS_8" in f3["owner_labor_check"]
    assert f3["executed_control_transfer_check"].startswith("NOT_REACHED_")
    assert f3["post_transfer_external_economic_continuity_check"].startswith("FAIL_")
    assert "EXTERNAL_REVENUE_IS_ZERO" in f3["post_transfer_external_economic_continuity_check"]
    assert "POSITIVE_OCF_RMB288498_70" in f3["post_transfer_external_economic_continuity_check"]
    assert f3["normalized_margin_check"].startswith("FAIL_")


def test_scan120_repeats_retrieval_order_in_scan121_before_further_narrowing():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_121"
    boundary = scan["next_search_boundary"]
    assert "CURRENT_LOW_FTE_POSITIVE_PROFIT_POSITIVE_OCF_FIRST_THEN_EXECUTED_CONTROL_PASS_REPEAT_DURABILITY" in boundary
    assert "COMPLETED_FRESH_OPERATOR_REPRODUCIBLE_CONTROL_BEFORE_REPORTING_PERIOD" in boundary
    assert "EXCLUDE_SCAN060_TO_120_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE_FAIL_CLOSED" in boundary


def test_scan120_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_120"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_120-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_121"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_121"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
