import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_111.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

def test_scan111_uses_auditable_ledger_plus_outcome_priority():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_111"
    assert scan["status"]=="COMPLETE"
    assert "AUDITABLE_LEDGER_PLUS_OUTCOME_PACKET_PRIORITY" in scan["search_mode"]
    a=scan["drift_audit"]
    assert a["auditable_ledger_plus_outcome_priority_used"] is True
    assert a["same_operator_and_control_position_binding_required"] is True
    assert a["owner_shadow_wage_or_replacement_cost_required"] is True
    assert a["executed_control_change_required"] is True

def test_scan111_is_diverse_and_fail_closed():
    scan=load(SCAN)
    assert len(scan["examined_formations"])==3
    titles={x["title"] for x in scan["examined_formations"]}
    assert any("RESTAURANT_PARTNERSHIP" in x for x in titles)
    assert any("MICRO_REAL_ESTATE" in x for x in titles)
    assert any("ZERO_EMPLOYEE_TECH" in x for x in titles)
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["high_attraction_beacons"]==[]

def test_scan111_does_not_overclaim_lifecycle_settlement_as_clean_pnl():
    scan=load(SCAN)
    f={x["formation_id"]:x for x in scan["examined_formations"]}
    r=f["ATTRACTION_SCAN_111-F1"]
    assert r["owner_labor_check"].startswith("PASS_")
    assert r["founder_independence_check"].startswith("FAIL_")
    assert r["same_operator_economic_binding_check"].startswith("PARTIAL_PASS_")
    assert any("706335_70" in x for x in scan["scan_learnings"])

def test_scan111_separates_control_transfer_from_value_flow():
    scan=load(SCAN)
    f={x["formation_id"]:x for x in scan["examined_formations"]}
    x=f["ATTRACTION_SCAN_111-F2"]
    assert x["executed_control_transfer_check"].startswith("PASS_")
    assert x["post_transfer_external_economic_continuity_check"].startswith("FAIL_")
    assert x["normalized_margin_check"].startswith("FAIL_")
    y=f["ATTRACTION_SCAN_111-F3"]
    assert y["executed_control_transfer_check"].startswith("FAIL_")
    assert y["data_action_rights_check"].startswith("FAIL_")
    assert y["normalized_margin_check"].startswith("FAIL_")

def test_scan111_advances_to_low_headcount_machine_light_control_priority():
    scan=load(SCAN)
    assert scan["next_scan_id"]=="ATTRACTION_SCAN_112"
    b=scan["next_search_boundary"]
    assert "LOW_HEADCOUNT_MACHINE_LIGHT_EXECUTED_CONTROL_PRIORITY" in b
    assert "AUDITED_POSITIVE_EXTERNAL_CUSTOMER_REVENUE" in b
    assert "EXECUTED_CONTROLLING_EQUITY_ASSET_LICENSE_OR_CONTRACT_TRANSFER" in b
    assert "EXCLUDE_SCAN060_TO_111_FORMATIONS_AND_PRIMARY_SIGNALS" in b

def test_scan111_updates_reset_state_without_promotion():
    scan=load(SCAN); state=load(STATE)
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_111"
    assert state["last_resolved_formation_id"]=="ATTRACTION_SCAN_111-F3"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_112"
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"]=="ATTRACTION_SCAN_112"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"]==scan["next_search_boundary"]
