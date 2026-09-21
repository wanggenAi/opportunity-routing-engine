import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_043.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan043_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_043"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_scan043_requires_payer_and_asset_evidence():
    rows=load(SCAN)["examined_formations"]
    assert len(rows)==6
    assert all(row["payer_evidence"] for row in rows)
    assert all(row["repeated_workaround"] for row in rows)
    assert all(row["machine_delivery"] for row in rows)
    assert all(row["compounding_asset_test"] for row in rows)
    assert all(row["incumbent_preflight"] for row in rows)
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_scan015_email_checkpoint_is_fail_closed_not_denial():
    checkpoint=load(SCAN)["validation_checkpoint"]
    assert checkpoint["incoming_written_provider_responses"]==0
    assert len(checkpoint["wave1_sent_targets"])==2
    assert "NO_RESPONSE_IS_NOT_DENIAL" in checkpoint["verdict"]

def test_state_advances_to_scan044():
    state=load(STATE)
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_043"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_044"
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"

def test_scan044_demands_execution_created_asset():
    boundary=load(SCAN)["next_search_boundary"]
    assert "EACH_EXECUTION_CREATES_OR_STRENGTHENS_OPERATOR_OWNED_REUSABLE_ASSET" in boundary
    assert "WITH_LEGAL_REUSE" in boundary
    assert "NO_MATURE_INCUMBENT_SAME_ASSET" in boundary
