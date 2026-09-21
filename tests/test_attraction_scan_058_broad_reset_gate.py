import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_058.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(p):
    return json.loads(p.read_text())

def test_scan058_is_broad_reset_and_closes_six_paid_outcomes():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_058"
    assert scan["status"]=="COMPLETE"
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["retained_research_formations"]==[]
    assert len(scan["examined_formations"])==6
    assert all(x["verdict"].startswith("DEMOTED_") for x in scan["examined_formations"])

def test_scan058_failure_modes_are_formation_diverse_not_one_trigger_ontology():
    scan=load(SCAN)
    verdicts={x["formation_id"]:x["verdict"] for x in scan["examined_formations"]}
    assert "COI_COMPLIANCE_CONTROL_SURFACE" in verdicts["ATTRACTION_SCAN_058-F1"]
    assert "COMPANY_SPECIFIC_JUDGMENT" in verdicts["ATTRACTION_SCAN_058-F2"]
    assert "LOW_UNIT_LABOR_ECONOMICS" in verdicts["ATTRACTION_SCAN_058-F3"]
    assert "OFFICIAL_EXACT_RENT_MANAGER_LEASE_AI_INTEGRATION" in verdicts["ATTRACTION_SCAN_058-F4"]
    assert "TRADE_EXPERT_TAIL" in verdicts["ATTRACTION_SCAN_058-F5"]
    assert "EXPERT_AND_AUDITOR_TAIL" in verdicts["ATTRACTION_SCAN_058-F6"]

def test_scan058_keeps_scan059_broad_for_second_pass():
    scan=load(SCAN)
    assert scan["next_scan_id"]=="ATTRACTION_SCAN_059"
    b=scan["next_search_boundary"]
    assert "BROAD_CURRENT_PAID_OUTCOMES_FORMATION_DIVERSE_SECOND_PASS" in b
    assert "STRONG_RECURRING_SPEND_OR_CONTRACT_TO_HIRE_EVIDENCE" in b
    assert "NO_SCAN058_VERTICAL_INHERITANCE" in b
    assert "NO_MECHANISM_INHERITANCE" in b
    assert "FAIL_CLOSED_PROMOTION" in b

def test_state_advances_after_scan058():
    state=load(STATE)
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_058"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_059"
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"
    assert {x["formation_id"] for x in state["retained_research_formations"]}=={"ATTRACTION_SCAN_015-F1"}
