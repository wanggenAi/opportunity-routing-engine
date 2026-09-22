import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_114.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan114_requires_explicit_operating_cashflow_not_generic_cashflow():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_114"
    assert scan["status"] == "COMPLETE"
    assert "EXPLICIT_POSITIVE_OPERATING_CASHFLOW_NOT_GENERIC_CASHFLOW" in scan["search_mode"]
    audit = scan["drift_audit"]
    assert audit["explicit_operating_cashflow_required"] is True
    assert audit["generic_cashflow_is_not_operating_cashflow"] is True
    assert audit["bounded_acquisition_and_working_capital_required"] is True


def test_scan114_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {x["title"] for x in scan["examined_formations"]}
    assert any("IMPORT_EXPORT_TRADING" in x for x in titles)
    assert any("MICROGRID_EPC" in x for x in titles)
    assert any("PROPERTY_MANAGEMENT" in x for x in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan114_separates_generic_cashflow_from_operating_cashflow():
    scan = load(SCAN)
    f = {x["formation_id"]: x for x in scan["examined_formations"]}
    for fid in ("ATTRACTION_SCAN_114-F1", "ATTRACTION_SCAN_114-F3"):
        x = f[fid]
        assert x["executed_control_transfer_check"].startswith("PASS_")
        assert x["post_transfer_external_economic_continuity_check"].startswith("PARTIAL_PASS_")
        assert "OPERATING_CASHFLOW" in x["post_transfer_external_economic_continuity_check"]
        assert x["normalized_margin_check"].startswith("FAIL_TO_CLOSE_")
        assert x["verdict"].startswith("DEMOTED_")


def test_scan114_proves_positive_explicit_ocf_can_still_fail_human_delivery():
    scan = load(SCAN)
    x = {f["formation_id"]: f for f in scan["examined_formations"]}["ATTRACTION_SCAN_114-F2"]
    assert x["executed_control_transfer_check"].startswith("PASS_")
    assert x["post_transfer_external_economic_continuity_check"].startswith("PASS_")
    assert "EXPLICIT_OPERATING_CASHFLOW" in x["post_transfer_external_economic_continuity_check"]
    assert x["fresh_small_operator_entry_check"].startswith("FAIL_")
    assert x["owner_labor_check"].startswith("FAIL_")
    assert x["machine_delegatability_check"].startswith("FAIL_")
    assert "EPC" in x["machine_delegatability_check"]


def test_scan114_advances_to_low_fte_total_capital_binding():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_115"
    boundary = scan["next_search_boundary"]
    assert "EXPLICIT_POST_TRANSFER_OPERATING_CASHFLOW_PLUS_LOW_LABOR_AND_TOTAL_CAPITAL_BINDING_PRIORITY" in boundary
    assert "TARGET_FTE_OR_EXPLICIT_REPLACEMENT_SERVICE_COST" in boundary
    assert "TOTAL_USABLE_CAPITAL_INCLUDING_WORKING_CAPITAL" in boundary
    assert "EXCLUDE_SCAN060_TO_114_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary


def test_scan114_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_114"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_114-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_115"
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_115"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
