import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_121.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def formations():
    scan = load(SCAN)
    return {x["formation_id"]: x for x in scan["examined_formations"]}


def test_scan121_repeats_economics_first_without_lowering_the_floor():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_121"
    assert scan["status"] == "COMPLETE"
    audit = scan["drift_audit"]
    assert audit["retrieval_order_current_economics_first"] is True
    assert audit["independent_durability_repeat_of_scan120"] is True
    assert audit["current_same_entity_report_required"] is True
    assert audit["direct_current_or_latest_intrinsically_low_fte_required"] is True
    assert audit["positive_external_revenue_required"] is True
    assert audit["positive_net_profit_required"] is True
    assert audit["explicit_positive_operating_cashflow_required"] is True
    assert audit["control_history_deepened_only_after_full_current_economic_conjunction_passes"] is True
    assert audit["early_gate_failure_stops_unnecessary_control_research"] is True


def test_scan121_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {x["title"] for x in scan["examined_formations"]}
    assert any("6_FTE_ECOMMERCE_OPERATOR" in x for x in titles)
    assert any("20_FTE_SYSTEM_INTEGRATOR" in x for x in titles)
    assert any("16_FTE_SEED_COMPANY" in x for x in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan121_canyou_fails_profit_and_ocf_despite_six_fte_and_revenue():
    f1 = formations()["ATTRACTION_SCAN_121-F1"]
    assert f1["owner_labor_check"].startswith("PASS_")
    assert "COUNT_IS_6" in f1["owner_labor_check"]
    assert f1["executed_control_transfer_check"].startswith("NOT_REACHED_")
    assert f1["post_transfer_external_economic_continuity_check"].startswith("FAIL_")
    assert "RMB141509_43" in f1["post_transfer_external_economic_continuity_check"]
    assert "RMB328028_67" in f1["post_transfer_external_economic_continuity_check"]
    assert "RMB116902_77" in f1["post_transfer_external_economic_continuity_check"]
    assert f1["direct_operating_cost_check"].startswith("FAIL_")


def test_scan121_xinrui_does_not_treat_positive_ocf_as_positive_profit():
    f2 = formations()["ATTRACTION_SCAN_121-F2"]
    assert f2["owner_labor_check"].startswith("PASS_")
    assert "COUNT_IS_20" in f2["owner_labor_check"]
    assert f2["executed_control_transfer_check"].startswith("NOT_REACHED_")
    assert f2["post_transfer_external_economic_continuity_check"].startswith("FAIL_")
    assert "RMB8_954_007_84" in f2["post_transfer_external_economic_continuity_check"]
    assert "RMB2_132_609_70" in f2["post_transfer_external_economic_continuity_check"]
    assert "RMB878305_63" in f2["post_transfer_external_economic_continuity_check"]
    assert f2["normalized_margin_check"].startswith("FAIL_")


def test_scan121_jinante_requires_positive_consolidated_ocf_after_profit_passes():
    f3 = formations()["ATTRACTION_SCAN_121-F3"]
    assert f3["owner_labor_check"].startswith("PASS_")
    assert "COUNT_IS_16" in f3["owner_labor_check"]
    assert f3["executed_control_transfer_check"].startswith("NOT_REACHED_")
    assert f3["post_transfer_external_economic_continuity_check"].startswith("FAIL_")
    assert "RMB11_335_117_86" in f3["post_transfer_external_economic_continuity_check"]
    assert "RMB528888_03" in f3["post_transfer_external_economic_continuity_check"]
    assert "RMB711001_01" in f3["post_transfer_external_economic_continuity_check"]
    assert f3["normalized_margin_check"].startswith("FAIL_")


def test_scan121_advances_scan122_to_strict_primary_admission_gate():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_122"
    boundary = scan["next_search_boundary"]
    assert "STRICT_CURRENT_ECONOMIC_CONJUNCTION_PRIMARY_ADMISSION" in boundary
    assert "RECORD_PARTIAL_MATCHES_ONLY_AS_EXCLUDED_OBSERVATIONS" in boundary
    assert "COMPLETED_FRESH_OPERATOR_REPRODUCIBLE_CONTROL_BEFORE_REPORTING_PERIOD" in boundary
    assert "EXCLUDE_SCAN060_TO_121_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE_FAIL_CLOSED" in boundary


def test_scan121_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_121"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_121-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_122"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_122"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
