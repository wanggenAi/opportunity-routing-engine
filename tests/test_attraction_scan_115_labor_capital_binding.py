import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_115.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan115_requires_target_ocf_labor_and_total_capital_binding():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_115"
    assert scan["status"] == "COMPLETE"
    assert "EXPLICIT_POST_TRANSFER_OPERATING_CASHFLOW_PLUS_LOW_LABOR_AND_TOTAL_CAPITAL_BINDING_PRIORITY" in scan["search_mode"]
    audit = scan["drift_audit"]
    assert audit["explicit_operating_cashflow_required"] is True
    assert audit["target_fte_or_replacement_service_cost_required"] is True
    assert audit["total_usable_capital_including_working_capital_required"] is True
    assert audit["historical_fte_not_promoted_to_current_fact"] is True
    assert audit["parent_consolidated_ocf_not_promoted_to_target_ocf"] is True


def test_scan115_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {x["title"] for x in scan["examined_formations"]}
    assert any("BUILDING_QUALITY_TESTING" in x for x in titles)
    assert any("HMI_AUDIO_SOC" in x for x in titles)
    assert any("COMMERCIAL_CLEANING_EQUIPMENT" in x for x in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan115_small_equity_price_does_not_bypass_labor_and_capital():
    scan = load(SCAN)
    f1 = {x["formation_id"]: x for x in scan["examined_formations"]}["ATTRACTION_SCAN_115-F1"]
    assert f1["executed_control_transfer_check"].startswith("PASS_")
    assert f1["post_transfer_external_economic_continuity_check"].startswith("PARTIAL_PASS_")
    assert "66_PERSON" in f1["machine_delegatability_check"]
    assert f1["fresh_small_operator_entry_check"].startswith("FAIL_TO_CLOSE_")
    assert f1["verdict"].startswith("DEMOTED_")


def test_scan115_positive_explicit_target_ocf_still_fails_high_control_capital():
    scan = load(SCAN)
    f2 = {x["formation_id"]: x for x in scan["examined_formations"]}["ATTRACTION_SCAN_115-F2"]
    assert f2["executed_control_transfer_check"].startswith("PASS_")
    assert f2["post_transfer_external_economic_continuity_check"].startswith("PASS_")
    assert "EXPLICIT_OPERATING_ACTIVITY_NET_CASH_INFLOW" in f2["post_transfer_external_economic_continuity_check"]
    assert f2["fresh_small_operator_entry_check"].startswith("FAIL_")
    assert f2["owner_labor_check"].startswith("UNKNOWN_")
    assert f2["verdict"].startswith("DEMOTED_")


def test_scan115_target_level_subsidiary_reporting_catches_negative_ocf():
    scan = load(SCAN)
    f3 = {x["formation_id"]: x for x in scan["examined_formations"]}["ATTRACTION_SCAN_115-F3"]
    assert f3["executed_control_transfer_check"].startswith("PASS_")
    assert f3["post_transfer_external_economic_continuity_check"].startswith("FAIL_")
    assert "TARGET_LEVEL_OPERATING_CASHFLOW_NEGATIVE" in f3["post_transfer_external_economic_continuity_check"]
    assert f3["fresh_small_operator_entry_check"].startswith("FAIL_")
    assert f3["owner_labor_check"].startswith("FAIL_")
    assert f3["verdict"].startswith("DEMOTED_")


def test_scan115_advances_to_standalone_target_ledger_priority():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_116"
    boundary = scan["next_search_boundary"]
    assert "STANDALONE_TARGET_LEDGER_PASS" in boundary
    assert "STANDALONE_PUBLIC_REPORTING_OR_IMPORTANT_SUBSIDIARY_LEVEL_FINANCIAL_DISCLOSURE" in boundary
    assert "CURRENT_TARGET_FTE_OR_EXPLICIT_REPLACEMENT_SERVICE_COST" in boundary
    assert "TOTAL_USABLE_CAPITAL" in boundary
    assert "EXCLUDE_SCAN060_TO_115_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary


def test_scan115_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_115"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_115-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_116"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_116"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
