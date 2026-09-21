import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_042.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan042_closes_with_zero_retention():
    scan=load(SCAN)
    assert scan["scan_id"]=="ATTRACTION_SCAN_042"
    assert scan["active_commercial_candidate_promotions"]==[]
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["first_external_value_flow"]=="NOT_PROVEN"

def test_scan042_tests_forced_operational_changes():
    rows=load(SCAN)["examined_formations"]
    assert len(rows)==6
    assert all(row["state_change"] for row in rows)
    assert all(row["operational_cost"] for row in rows)
    assert all(row["existing_budget_signal"] for row in rows)
    assert all(row["machine_delivery"] for row in rows)
    assert all(row["control_surface"] for row in rows)
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_scan042_detects_platform_and_generic_migration_kills():
    verdicts={row["verdict"] for row in load(SCAN)["examined_formations"]}
    assert "DEMOTED_PLATFORM_NATIVE_UPGRADE_OWNS_THE_VALUE_LOOP" in verdicts
    assert any("GENERIC" in verdict for verdict in verdicts)
    assert any("DROP_IN" in verdict for verdict in verdicts)

def test_state_advances_to_scan043():
    state=load(STATE)
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_042"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_043"
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"

def test_scan043_requires_paid_workaround_and_compounding_asset():
    boundary=load(SCAN)["next_search_boundary"]
    assert "DIRECT_PAYER_OR_REPEATED_WORKAROUND_EVIDENCE" in boundary
    assert "DISTINCT_COMPOUNDING_OPERATOR_ASSET" in boundary
    assert "EXCLUDE_CLAIMS_REFUNDS_GRANTS_TAX_RELIEF_VENDOR_DEPRECATION_AND_GENERIC_MIGRATION" in boundary
