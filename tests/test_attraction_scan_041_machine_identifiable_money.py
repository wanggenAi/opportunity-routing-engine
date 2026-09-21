import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_041.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan041_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_041"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_scan041_tests_identification_action_and_incumbent_pressure():
    rows=load(SCAN)["examined_formations"]
    assert len(rows)==6
    assert all(row["recent_change"] for row in rows)
    assert all(row["monetary_value"] for row in rows)
    assert all(row["beneficiary_identification"] for row in rows)
    assert all(row["operator_accessibility"] for row in rows)
    assert all(row["incumbent_preflight"] for row in rows)
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_scan041_includes_fast_absorption_and_automatic_kills():
    verdicts={row["verdict"] for row in load(SCAN)["examined_formations"]}
    assert "DEMOTED_FAST_INCUMBENT_ABSORPTION_OF_NEW_NATIVE_ACTION_API" in verdicts
    assert any("AUTOMATIC" in verdict for verdict in verdicts)

def test_state_advances_to_scan042():
    state=load(STATE)
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_041"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_042"
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"

def test_scan042_resets_out_of_recovery_ontology():
    boundary=load(SCAN)["next_search_boundary"]
    assert "HIGH_COST_OPERATIONAL_STATE_CHANGE" in boundary
    assert "PRECOMMITTED_OR_OBSERVED_BUDGET" in boundary
    assert "MACHINE_EXECUTABLE_DIGITAL_DELIVERY" in boundary
    assert "EXCLUDE_CLAIMS_REFUNDS_GRANTS_TAX_RELIEF" in boundary
