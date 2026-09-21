import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_057.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

def test_scan057_closes_six_niche_external_trigger_loops_without_promotion():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_057"
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"
    rows = scan["examined_formations"]
    assert len(rows) == 6
    assert all(row["verdict"].startswith("DEMOTED_") for row in rows)

def test_scan057_exact_products_absorb_each_cross_system_rule():
    scan = load(SCAN)
    verdicts = {row["formation_id"]: row["verdict"] for row in scan["examined_formations"]}
    assert "DOWNTIME_TO_AD_CONTROL_SURFACE" in verdicts["ATTRACTION_SCAN_057-F1"]
    assert "BLACKLIST_MONITORING_AND_AUTOPAUSE" in verdicts["ATTRACTION_SCAN_057-F2"]
    assert "SUPPLIER_COST_TO_PRICE_AUTOMATION" in verdicts["ATTRACTION_SCAN_057-F3"]
    assert "CAPACITY_AWARE_AD_CONTROL_SURFACE" in verdicts["ATTRACTION_SCAN_057-F4"]
    assert "SUPPLIER_AVAILABILITY_SYNC" in verdicts["ATTRACTION_SCAN_057-F5"]
    assert "PAYMENT_GATEWAY_FAILOVER" in verdicts["ATTRACTION_SCAN_057-F6"]

def test_scan057_resets_mechanism_inheritance_for_scan058():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_058"
    boundary = scan["next_search_boundary"]
    assert "BROAD_CURRENT_PAID_OUTCOMES_FORMATION_DIVERSE" in boundary
    assert "NO_EXCEPTION_REMEDIATION" in boundary
    assert "NO_FIXED_STATE_TRANSITION" in boundary
    assert "NO_EXTERNAL_TRIGGER_MECHANISM_INHERITANCE" in boundary
    assert "FAIL_CLOSED_PROMOTION" in boundary

def test_state_advances_after_scan057():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_057"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_058"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    retained = {x["formation_id"] for x in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1"}
