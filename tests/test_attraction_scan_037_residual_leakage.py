import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_037.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan037_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_037"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_residual_leakage_is_causally_classified_not_treated_as_white_space():
    scan=load(SCAN)
    rows=scan["examined_formations"]
    assert len(rows)==6
    assert all(row["observed_residual_leakage"] for row in rows)
    assert all(row["residual_leakage_classification"] for row in rows)
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_state_keeps_only_scan015_and_advances_to_scan038():
    state=load(STATE)
    retained={x["formation_id"] for x in state["retained_research_formations"]}
    assert retained=={"ATTRACTION_SCAN_015-F1"}
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_037"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_038"

def test_scan038_requires_structural_post_incumbent_gap():
    scan=load(SCAN)
    boundary=scan["next_search_boundary"]
    assert "STRUCTURAL_CONTROL_RIGHT_DATA_RIGHT_OR_CROSS_SYSTEM_ACTION_GAP" in boundary
    assert "NOT_ADOPTION_IMPLEMENTATION_OR_DISCIPLINE" in boundary
