import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_122.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def formations():
    scan = load(SCAN)
    return {x["formation_id"]: x for x in scan["examined_formations"]}


def test_scan122_enforces_strict_current_economic_primary_admission():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_122"
    assert scan["status"] == "COMPLETE"
    audit = scan["drift_audit"]
    assert audit["strict_current_economic_conjunction_primary_admission"] is True
    assert audit["current_same_entity_report_required"] is True
    assert audit["direct_current_or_latest_intrinsically_low_fte_required"] is True
    assert audit["positive_external_revenue_required"] is True
    assert audit["related_party_captive_revenue_not_counted_as_external"] is True
    assert audit["positive_net_profit_required"] is True
    assert audit["explicit_positive_consolidated_operating_cashflow_required"] is True
    assert audit["partial_matches_recorded_as_excluded_observations"] is True
    assert audit["control_history_deepened_only_for_full_current_economic_survivors"] is True


def test_scan122_does_not_fabricate_a_fixed_primary_count():
    scan = load(SCAN)
    assert scan["drift_audit"]["no_arbitrary_fixed_primary_formation_count"] is True
    assert len(scan["examined_formations"]) == 2
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan122_huada_passes_economics_then_fails_control_and_delivery():
    f1 = formations()["ATTRACTION_SCAN_122-F1"]
    assert f1["owner_labor_check"].startswith("PASS_")
    assert "COUNT_IS_17" in f1["owner_labor_check"]
    assert f1["same_operator_economic_binding_check"].startswith("PASS_")
    assert "RMB48_034_052_28" in f1["same_operator_economic_binding_check"]
    assert "RMB1_706_441_35" in f1["same_operator_economic_binding_check"]
    assert "RMB20_230_573_56" in f1["same_operator_economic_binding_check"]
    assert f1["executed_control_transfer_check"].startswith("FAIL_")
    assert f1["fresh_small_operator_entry_check"].startswith("FAIL_")
    assert f1["direct_operating_cost_check"].startswith("FAIL_")
    assert f1["founder_independence_check"].startswith("FAIL_")
    assert f1["verdict"].startswith("DEMOTED_")


def test_scan122_kangmeifeng_passes_economics_then_fails_fresh_operator_reproducibility():
    f2 = formations()["ATTRACTION_SCAN_122-F2"]
    assert f2["owner_labor_check"].startswith("PASS_")
    assert "COUNT_IS_15" in f2["owner_labor_check"]
    assert f2["same_operator_economic_binding_check"].startswith("PASS_")
    assert "RMB8_719_805_71" in f2["same_operator_economic_binding_check"]
    assert "RMB1_423_975_92" in f2["same_operator_economic_binding_check"]
    assert "RMB1_587_115_80" in f2["same_operator_economic_binding_check"]
    assert f2["executed_control_transfer_check"].startswith("FAIL_")
    assert f2["fresh_small_operator_entry_check"].startswith("FAIL_")
    assert f2["direct_operating_cost_check"].startswith("FAIL_")
    assert f2["founder_independence_check"].startswith("FAIL_")
    assert f2["verdict"].startswith("DEMOTED_")


def test_scan122_excludes_related_party_captive_revenue_and_partial_economic_matches():
    scan = load(SCAN)
    excluded = "\n".join(scan["excluded_observations"])
    assert "Jinkun Zhiliang" in excluded
    assert "all H1 revenue" in excluded
    assert "Huayi Shares" in excluded
    assert "Wali Technology" in excluded
    assert "Lunan Data" in excluded
    assert "No control-history deepening" in excluded


def test_scan122_repeats_before_promoting_control_to_an_admission_gate():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_123"
    boundary = scan["next_search_boundary"]
    assert "STRICT_CURRENT_ECONOMIC_CONJUNCTION_PRIMARY_ADMISSION_REPEAT" in boundary
    assert "CHECK_COMPLETED_FRESH_OPERATOR_REPRODUCIBLE_CONTROL_FIRST" in boundary
    assert "INCLUDE_FRESH_NONMANUFACTURING_ROUTES_WITHOUT_RELAXING_GATES" in boundary
    assert "EXCLUDE_SCAN060_TO_122_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE_FAIL_CLOSED" in boundary


def test_scan122_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_122"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_122-F2"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_123"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_123"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
