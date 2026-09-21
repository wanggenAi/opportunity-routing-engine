import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_045.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan045_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_045"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_scan045_requires_day_one_asset_and_rights():
    rows=load(SCAN)["examined_formations"]
    assert len(rows)==6
    required=("payer_evidence","day_one_value","execution_created_asset","permission_and_sensitivity","cold_start_test","incumbent_preflight","verdict")
    assert all(all(row.get(key) for key in required) for row in rows)
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_scan045_contains_both_incumbent_and_rights_failure_modes():
    verdicts=" ".join(row["verdict"] for row in load(SCAN)["examined_formations"])
    assert "MATURE" in verdicts or "SCALED" in verdicts
    assert "RIGHTS" in verdicts or "IDENTITY" in verdicts or "PLATFORM_CONTROLLED" in verdicts

def test_state_advances_to_scan046():
    state=load(STATE)
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_045"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_046"
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"

def test_scan046_resets_to_observed_paid_microflows():
    boundary=load(SCAN)["next_search_boundary"]
    assert "PAID_OR_CONTRACTED_MICRO_FLOW" in boundary
    assert "SPARSE_SPECIALIZED_SUPPLY_OR_EARLY_CATEGORY_FORMATION" in boundary
    assert "NO_REQUIRED_VERTICAL_OR_MECHANISM" in boundary
