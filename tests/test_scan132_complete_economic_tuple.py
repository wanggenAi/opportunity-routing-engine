import json
from pathlib import Path

from src.jev_research_advisory import build_research_states
from tools.run_jev_research_advisory import resolve_scan_path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_132.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan132_complete_economic_tuple_evidence.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan132_is_current_auto_jev_input_and_all_formations_are_closed():
    state = load(STATE)
    path = resolve_scan_path("auto", state, research_dir=ROOT / "data" / "research_runs")
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_132"
    assert path == SCAN
    scan = load(SCAN)
    states = build_research_states(scan=scan, commercial_state=state, max_entities=8)
    assert len(states) == 4
    assert {row["formation"]["formation_id"] for row in states} == {
        "ATTRACTION_SCAN_132-F1", "ATTRACTION_SCAN_132-F2",
        "ATTRACTION_SCAN_132-F3", "ATTRACTION_SCAN_132-F4",
    }
    assert all(row["authoritative_engine_context"]["existing_closure_authoritative"] for row in states)

def test_scan132_retains_nothing_and_never_promotes():
    scan = load(SCAN)
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []
    assert all(row["verdict"].startswith("DEMOTED_") for row in scan["examined_formations"])
    assert scan["first_external_value_flow"] == "NOT_PROVEN"

def test_scan132_complete_tuple_gates_are_independent():
    scan = load(SCAN)
    assert scan["drift_audit"]["complete_economic_tuple_required"] is True
    assert scan["drift_audit"]["receipt_amount_cannot_be_hidden_or_inferred"] is True
    assert scan["drift_audit"]["post_transfer_cashflow_right_must_be_explicit"] is True
    assert scan["drift_audit"]["low_recurring_human_delivery_independent_gate"] is True
    f1, f2, f3, f4 = scan["examined_formations"]
    assert f1["economic_tuple"]["contracted_receipt_amount"].startswith("NOT_PUBLIC")
    assert f2["economic_tuple"]["contracted_receipt_amount"] == "RMB_3700_PER_MONTH"
    assert f3["economic_tuple"]["post_transfer_receipt_right"].startswith("FAIL_")
    assert f4["economic_tuple"]["low_recurring_human_delivery"].startswith("FAIL_")

def test_scan132_evidence_pack_matches_zero_retention_machine_truth():
    state = load(STATE)
    evidence = load(EVIDENCE)
    assert evidence["scan_id"] == "ATTRACTION_SCAN_132"
    assert len(evidence["evidence_packets"]) == 4
    assert evidence["scan_conclusion"].endswith("ZERO_RETAINED_ZERO_COMMERCIAL_PROMOTION")
    assert state["retained_research_formations"] == []
    assert state["active_commercial_candidates"] == []
    assert state["next_scan_id"] == "ATTRACTION_SCAN_133"
