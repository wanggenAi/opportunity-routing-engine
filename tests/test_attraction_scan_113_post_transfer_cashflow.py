import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_113.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan113_uses_executed_control_plus_post_transfer_cashflow_priority():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_113"
    assert scan["status"] == "COMPLETE"
    assert "EXECUTED_CONTROL_PLUS_POST_TRANSFER_CASHFLOW_PRIORITY" in scan["search_mode"]
    audit = scan["drift_audit"]
    assert audit["executed_control_plus_post_transfer_cashflow_priority_used"] is True
    assert audit["executed_control_change_required"] is True
    assert audit["purchase_date_to_period_end_cashflow_required"] is True
    assert audit["low_human_service_required"] is True


def test_scan113_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {x["title"] for x in scan["examined_formations"]}
    assert any("HEALTHCARE_INFORMATION_AI_SOFTWARE" in x for x in titles)
    assert any("FABLESS_SENSOR_CHIP" in x for x in titles)
    assert any("RENEWABLE_O_AND_M_PLATFORM" in x for x in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan113_separates_profit_from_cash_generation():
    scan = load(SCAN)
    f = {x["formation_id"]: x for x in scan["examined_formations"]}
    for fid in ("ATTRACTION_SCAN_113-F1", "ATTRACTION_SCAN_113-F2"):
        x = f[fid]
        assert x["executed_control_transfer_check"].startswith("PASS_")
        assert x["post_transfer_external_economic_continuity_check"].startswith("PARTIAL_PASS_")
        assert "NEGATIVE" in x["post_transfer_external_economic_continuity_check"]
        assert x["normalized_margin_check"].startswith("FAIL_TO_CLOSE_")
        assert x["verdict"].startswith("DEMOTED_")


def test_scan113_platform_does_not_hide_field_service_dependency():
    scan = load(SCAN)
    x = {f["formation_id"]: f for f in scan["examined_formations"]}["ATTRACTION_SCAN_113-F3"]
    assert x["executed_control_transfer_check"].startswith("PASS_")
    assert x["same_operator_economic_binding_check"].startswith("PARTIAL_PASS_")
    assert x["owner_labor_check"].startswith("FAIL_TO_CLOSE_")
    assert x["machine_delegatability_check"].startswith("FAIL_")
    assert "FIELD_ENGINEERS" in x["machine_delegatability_check"]


def test_scan113_advances_to_positive_post_transfer_operating_cashflow():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_114"
    boundary = scan["next_search_boundary"]
    assert "COMPLETED_CONTROL_POSITIVE_POST_TRANSFER_OPERATING_CASHFLOW" in boundary
    assert "POSITIVE_OPERATING_CASHFLOW" in boundary
    assert "EXPLICIT_FTE_OR_REPLACEMENT_SERVICE_COST" in boundary
    assert "EXCLUDE_SCAN060_TO_113_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary


def test_scan113_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_113"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_113-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_114"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_114"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
