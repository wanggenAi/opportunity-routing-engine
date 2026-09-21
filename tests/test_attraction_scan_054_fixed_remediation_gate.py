import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_054.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

def test_scan054_closes_six_fixed_remediation_money_loops_without_promotion():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_054"
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"
    rows = scan["examined_formations"]
    assert len(rows) == 6
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_scan054_requires_operator_control_not_merely_fixed_economics():
    scan = load(SCAN)
    verdicts = {row["formation_id"]: row["verdict"] for row in scan["examined_formations"]}
    assert "PRECHARGEBACK_AUTOMATION_CONTROL_SURFACE" in verdicts["ATTRACTION_SCAN_054-F1"]
    assert "UPSTREAM_IDEMPOTENCY_PREVENTION" in verdicts["ATTRACTION_SCAN_054-F2"]
    assert "EXTERNAL_COUNTERPARTY_DEPENDENCE" in verdicts["ATTRACTION_SCAN_054-F3"]
    assert "PLATFORM_NATIVE_AUTOMATION_APPROVAL" in verdicts["ATTRACTION_SCAN_054-F4"]
    assert "PLATFORM_OWNED_DETECTION_APPROVAL" in verdicts["ATTRACTION_SCAN_054-F5"]
    assert "PROVIDER_CLAIM_APPROVAL" in verdicts["ATTRACTION_SCAN_054-F6"]

def test_scan054_exits_recovery_family_for_scan055():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_055"
    boundary = scan["next_search_boundary"]
    assert "NON_RECOVERY" in boundary
    assert "SINGLE_STATE_TRANSITION" in boundary
    assert "FIXED_MACHINE_ACTION" in boundary
    assert "DIRECT_PAYER_MARGIN_OR_REVENUE_OUTCOME" in boundary
    assert "NO_REFUND_REIMBURSEMENT_CREDIT_DISPUTE_FAMILY" in boundary

def test_state_advances_after_scan054():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_054"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_055"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    retained = {x["formation_id"] for x in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1"}
