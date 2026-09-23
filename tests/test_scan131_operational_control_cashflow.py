import json
from pathlib import Path

from src.jev_research_advisory import build_research_states
from tools.run_jev_research_advisory import resolve_scan_path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_131.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan131_operational_control_cashflow_evidence.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan131_is_current_auto_jev_input_and_all_formations_are_closed():
    state = load(STATE)
    path = resolve_scan_path("auto", state, research_dir=ROOT / "data" / "research_runs")
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_131"
    assert path == SCAN
    scan = load(SCAN)
    states = build_research_states(scan=scan, commercial_state=state, max_entities=8)
    assert len(states) == 4
    assert {row["formation"]["formation_id"] for row in states} == {
        "ATTRACTION_SCAN_131-F1", "ATTRACTION_SCAN_131-F2",
        "ATTRACTION_SCAN_131-F3", "ATTRACTION_SCAN_131-F4",
    }
    assert all(row["authoritative_engine_context"]["existing_closure_authoritative"] for row in states)

def test_scan131_retains_nothing_and_never_promotes():
    scan = load(SCAN)
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []
    assert all(row["verdict"].startswith("DEMOTED_") for row in scan["examined_formations"])
    assert scan["first_external_value_flow"] == "NOT_PROVEN"

def test_scan131_enforces_complete_economic_tuple_and_control_boundary():
    scan = load(SCAN)
    assert scan["drift_audit"]["source_bound_transfer_price_required"] is True
    assert scan["drift_audit"]["source_bound_receipt_amount_and_term_required_for_promotion"] is True
    assert scan["drift_audit"]["operational_control_must_transfer_with_asset"] is True
    f1, f2, f3, f4 = scan["examined_formations"]
    assert f1["attraction_brief"]["self_propulsion"].startswith("PASS_")
    assert "10_7M_BUNDLED_CAPITAL" in f1["verdict"]
    assert "NO_PUBLIC_RENT_QUANTUM" in f2["verdict"]
    assert "NO_OPERATING_CONTROL_OR_CASHFLOW_TRANSFERS" in f3["verdict"]
    assert f4["attraction_brief"]["self_propulsion"].startswith("FAIL_")

def test_scan131_evidence_pack_matches_zero_retention_machine_truth():
    state = load(STATE)
    evidence = load(EVIDENCE)
    assert evidence["scan_id"] == "ATTRACTION_SCAN_131"
    assert len(evidence["evidence_packets"]) == 4
    assert evidence["scan_conclusion"].endswith("ZERO_RETAINED_ZERO_COMMERCIAL_PROMOTION")
    assert state["retained_research_formations"] == []
    assert state["active_commercial_candidates"] == []
    assert state["next_scan_id"] == "ATTRACTION_SCAN_132"
