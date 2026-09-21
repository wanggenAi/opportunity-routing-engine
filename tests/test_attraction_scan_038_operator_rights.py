import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_038.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan038_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_038"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_every_formation_tests_structural_gap_and_operator_rights():
    scan=load(SCAN)
    rows=scan["examined_formations"]
    assert len(rows)==6
    assert all(row["structural_gap"] for row in rows)
    assert all(row["operator_rights_assessment"] for row in rows)
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_state_advances_to_scan039_without_new_candidate():
    state=load(STATE)
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_038"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_039"
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"

def test_scan039_requires_operator_accessible_rights():
    scan=load(SCAN)
    boundary=scan["next_search_boundary"]
    assert "OPERATOR_ACCESSIBLE_RIGHTS_OR_DATA_POSITION" in boundary
    assert "NOT_ALREADY_BUNDLED_BY_INCUMBENT_NETWORK_PLATFORM_REGULATED_ACTOR_OR_ENDPOINT_OWNER" in boundary
