import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_048.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan048_tests_six_event_driven_money_loops_and_promotes_none():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_048"
    assert len(scan["examined_formations"]) == 6
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"

def test_scan048_all_close_on_exact_control_surface_saturation():
    scan = load(SCAN)
    assert all(row["verdict"].startswith("DEMOTED_") for row in scan["examined_formations"])
    verdicts = " ".join(row["verdict"] for row in scan["examined_formations"])
    assert "DEDUCTION" in verdicts
    assert "CHARGEBACK" in verdicts
    assert "COI" in verdicts
    assert "FREIGHT" in verdicts
    assert "LIEN" in verdicts
    assert "PRM" in verdicts

def test_scan048_preserves_cpg_deduction_as_shape_proof_not_candidate():
    scan = load(SCAN)
    row = next(item for item in scan["examined_formations"] if item["title"] == "CPG_RETAIL_DEDUCTION_RECOVERY")
    assert "paying CPG brands" in row["evidence_summary"]
    assert row["verdict"].startswith("DEMOTED_")
    assert scan["high_attraction_beacons"] == []

def test_scan049_moves_to_recently_created_paid_workflows():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_049"
    boundary = scan["next_search_boundary"]
    assert "SINCE_2026_07_01" in boundary
    assert "FULL_LOOP_PRODUCT_SATURATION_PREFLIGHT_FIRST" in boundary
    assert "NO_SCAN048_VERTICAL_INHERITANCE" in boundary

def test_state_advances_to_scan049_without_new_retention():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_048"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_049"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1"}
