import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_044.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan044_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_044"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_scan044_tests_asset_creation_ownership_and_reuse():
    rows=load(SCAN)["examined_formations"]
    assert len(rows)==6
    assert all(row["payer_evidence"] for row in rows)
    assert all(row["execution_created_asset"] for row in rows)
    assert all(row["ownership_and_reuse"] for row in rows)
    assert all(row["incumbent_preflight"] for row in rows)
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_scan044_contains_true_network_effect_but_incumbent_kill():
    fraud=next(row for row in load(SCAN)["examined_formations"] if row["title"]=="CROSS_MERCHANT_FRAUD_NETWORK")
    assert "true cross-customer compounding asset" in fraud["ownership_and_reuse"]
    assert "MATURE_FRAUD_PLATFORMS" in fraud["verdict"]

def test_state_advances_to_scan045():
    state=load(STATE)
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_044"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_045"
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"

def test_scan045_requires_day_one_value_and_permissioned_asset():
    boundary=load(SCAN)["next_search_boundary"]
    assert "SINGLE_CUSTOMER_DAY_ONE_VALUE" in boundary
    assert "PERMISSIONED_NON_SENSITIVE_CROSS_CUSTOMER_REUSABLE_ASSET_AS_BYPRODUCT" in boundary
    assert "NO_NETWORK_COLD_START_DEPENDENCE" in boundary
