import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_116.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def formations():
    scan = load(SCAN)
    return {x["formation_id"]: x for x in scan["examined_formations"]}


def test_scan116_uses_standalone_target_ledger_and_exact_time_window():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_116"
    assert scan["status"] == "COMPLETE"
    assert scan["drift_audit"]["standalone_target_ledger_priority_used"] is True
    assert scan["drift_audit"]["clean_post_control_time_window_required"] is True
    assert scan["drift_audit"]["current_target_fte_or_replacement_service_cost_required"] is True
    assert scan["drift_audit"]["mixed_period_economics_not_promoted_to_post_control_fact"] is True
    assert scan["drift_audit"]["nominal_control_transaction_not_promoted_to_total_usable_capital"] is True


def test_scan116_remains_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {x["title"] for x in scan["examined_formations"]}
    assert any("COAL_ENTERPRISE_SOFTWARE" in x for x in titles)
    assert any("INDUSTRIAL_AUTOMATION" in x for x in titles)
    assert any("MATERIALS_ELECTRONICS" in x for x in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan116_jiuheng_closes_positive_ocf_low_assets_but_fails_current_labor():
    f1 = formations()["ATTRACTION_SCAN_116-F1"]
    assert f1["executed_control_transfer_check"].startswith("PASS_")
    assert f1["post_transfer_external_economic_continuity_check"].startswith("PASS_")
    assert "EXPLICIT_OPERATING_CASHFLOW" in f1["post_transfer_external_economic_continuity_check"]
    assert "28_TECHNICAL" in f1["owner_labor_check"]
    assert f1["owner_labor_check"].startswith("FAIL_")
    assert f1["machine_delegatability_check"].startswith("FAIL_")
    assert f1["verdict"].startswith("DEMOTED_")


def test_scan116_huacheng_exposes_non_reproducible_control_and_negative_cashflow():
    f2 = formations()["ATTRACTION_SCAN_116-F2"]
    assert f2["executed_control_transfer_check"].startswith("PASS_")
    assert "PREEXISTING_40_52_PERCENT_CONCERT_PARTY_POSITION" in f2["executed_control_transfer_check"]
    assert f2["post_transfer_external_economic_continuity_check"].startswith("FAIL_")
    assert "NEGATIVE_NET_PROFIT" in f2["post_transfer_external_economic_continuity_check"]
    assert "NEGATIVE_EXPLICIT_OPERATING_CASHFLOW" in f2["post_transfer_external_economic_continuity_check"]
    assert "212" in f2["owner_labor_check"]
    assert f2["fresh_small_operator_entry_check"].startswith("FAIL_")


def test_scan116_feitian_does_not_stitch_mixed_period_into_post_control_fact():
    f3 = formations()["ATTRACTION_SCAN_116-F3"]
    assert f3["executed_control_transfer_check"].startswith("PASS_")
    assert f3["post_transfer_external_economic_continuity_check"].startswith("UNKNOWN_")
    assert "STRADDLE_THE_CONTROL_DATE" in f3["post_transfer_external_economic_continuity_check"]
    assert f3["same_operator_economic_binding_check"].startswith("FAIL_TO_CLOSE_")
    assert f3["owner_labor_check"].startswith("UNKNOWN_")
    assert f3["fresh_small_operator_entry_check"].startswith("FAIL_")


def test_scan116_advances_to_intrinsically_low_current_labor_boundary():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_117"
    boundary = scan["next_search_boundary"]
    assert "MINIMAL_LABOR_STANDALONE_LEDGER_PASS" in boundary
    assert "CURRENT_TARGET_FTE_DISCLOSED_AND_INTRINSICALLY_LOW" in boundary
    assert "WITHOUT_PROJECT_IMPLEMENTATION_FIELD_MANUFACTURING_OR_AFTER_SALES_DELIVERY" in boundary
    assert "CONTROL_SURFACE_REPRODUCIBLE_BY_A_FRESH_OPERATOR" in boundary
    assert "EXCLUDE_SCAN060_TO_116_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary


def test_scan116_updates_reset_state_without_promotion():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_116"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_116-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_117"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_117"
