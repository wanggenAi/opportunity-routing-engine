import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_040.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan040_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_040"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_scan040_tests_recent_money_against_action_and_incumbent_gates():
    scan=load(SCAN)
    rows=scan["examined_formations"]
    assert len(rows)==6
    assert all(row["recent_change"] for row in rows)
    assert all(row["monetary_value"] for row in rows)
    assert all(row["operator_accessibility"] for row in rows)
    assert all(row["incumbent_preflight"] for row in rows)
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_scan040_contains_automatic_and_advisor_failure_modes():
    verdicts={row["verdict"] for row in load(SCAN)["examined_formations"]}
    assert "DEMOTED_AUTOMATIC_PAYOUT_REMOVES_OPERATOR_ACTION_EDGE" in verdicts
    assert any("ADVISORY" in verdict or "CONSULTANCY" in verdict for verdict in verdicts)

def test_state_advances_to_scan041():
    state=load(STATE)
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_040"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_041"
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"

def test_scan041_requires_machine_identifiable_high_value_nonautomatic_edge():
    boundary=load(SCAN)["next_search_boundary"]
    assert "NON_AUTOMATIC_DETERMINISTIC_HIGH_VALUE" in boundary
    assert "MACHINE_IDENTIFIABLE" in boundary
    assert "NO_EXACT_APPLICATION_RECOVERY_OR_ADVISORY_INCUMBENT" in boundary
    assert "NO_RECURRING_EXPERT_DELIVERY" in boundary
