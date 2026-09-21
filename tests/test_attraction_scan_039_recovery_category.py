import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_039.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan039_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_039"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_operator_accessible_formations_still_get_exact_incumbent_preflight():
    scan=load(SCAN)
    rows=scan["examined_formations"]
    assert len(rows)==6
    assert all(row["operator_accessibility"] for row in rows)
    assert all(row["incumbent_preflight"] for row in rows)
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_state_advances_to_scan040():
    state=load(STATE)
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_039"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_040"
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"

def test_scan040_targets_recent_entitlement_change():
    scan=load(SCAN)
    boundary=scan["next_search_boundary"]
    assert "RECENTLY_CREATED_OR_EXPANDED_MONETARY_ENTITLEMENT_RULE_POLICY_OR_CONTRACT_CHANGE" in boundary
    assert "EXACT_END_TO_END_INCUMBENT_PREFLIGHT" in boundary
