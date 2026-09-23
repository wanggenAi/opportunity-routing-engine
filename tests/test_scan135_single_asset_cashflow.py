import json
from pathlib import Path

from src.jev_research_advisory import build_research_states
from tools.run_jev_research_advisory import resolve_scan_path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_135.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan135_single_asset_cashflow_evidence.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan135_is_current_auto_jev_input_with_one_open_research_formation():
    state = load(STATE)
    path = resolve_scan_path("auto", state, research_dir=ROOT / "data" / "research_runs")
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_135"
    assert path == SCAN
    scan = load(SCAN)
    states = build_research_states(scan=scan, commercial_state=state, max_entities=8)
    assert len(states) == 4
    rows = {row["formation"]["formation_id"]: row for row in states}
    assert rows["ATTRACTION_SCAN_135-F1"]["authoritative_engine_context"]["existing_closure_authoritative"] is False
    assert rows["ATTRACTION_SCAN_135-F1"]["authoritative_engine_context"]["already_retained_for_research"] is True
    for formation_id in ("ATTRACTION_SCAN_135-F2", "ATTRACTION_SCAN_135-F3", "ATTRACTION_SCAN_135-F4"):
        assert rows[formation_id]["authoritative_engine_context"]["existing_closure_authoritative"] is True

def test_scan135_retains_f1_for_research_only_and_never_promotes():
    scan = load(SCAN)
    assert scan["status"] == "COMPLETE"
    assert scan["retained_research_formations"] == ["ATTRACTION_SCAN_135-F1"]
    assert scan["active_commercial_candidate_promotions"] == []
    assert len(scan["high_attraction_beacons"]) == 1
    assert scan["high_attraction_beacons"][0]["commercial_candidate"] is False
    assert scan["examined_formations"][0]["verdict"].startswith("RETAINED_FOR_CHEAP_FALSIFICATION")
    assert all(row["verdict"].startswith("DEMOTED_") for row in scan["examined_formations"][1:])
    assert scan["first_external_value_flow"] == "NOT_PROVEN"

def test_scan135_f1_clears_public_cashflow_threshold_but_keeps_diligence_unknowns_open():
    scan = load(SCAN)
    f1 = scan["examined_formations"][0]
    econ = f1["economic_tuple"]
    assert econ["acquisition_price"] == "RMB_650304_CURRENT_CHANGE_SALE_FLOOR"
    assert econ["contracted_receipt_amount"] == "RMB_3000_PER_MONTH"
    assert econ["buyer_receipt_end"] == "LEASE_END_2030-11-20"
    assert econ["post_transfer_receipt_right"].startswith("PASS_")
    assert "5_54_PERCENT" in econ["receipt_to_entry_economics"]
    assert econ["unprepaid_receipt_status"].startswith("PARTIAL_PASS")
    assert len(f1["decisive_unknowns"]) >= 4
    assert f1["attraction_brief"]["action_gate"].startswith("RESEARCH_OPEN")

def test_scan135_comparators_fail_independent_hard_gates():
    scan = load(SCAN)
    f2, f3, f4 = scan["examined_formations"][1:]
    assert "2027-02-28" in f2["evidence_summary"]
    assert f2["economic_tuple"]["unprepaid_receipt_status"].startswith("FAIL_")
    assert f3["economic_tuple"]["buyer_receipt_end"] == "LEASE_END_2027-07-19"
    assert f4["economic_tuple"]["contracted_receipt_amount"].startswith("NOT_PUBLIC")
    assert f4["economic_tuple"]["receipt_to_entry_economics"].startswith("UNKNOWN")

def test_scan135_machine_truth_keeps_research_retention_separate_from_commercial_state():
    state = load(STATE)
    evidence = load(EVIDENCE)
    assert evidence["scan_id"] == "ATTRACTION_SCAN_135"
    assert len(evidence["evidence_packets"]) == 4
    assert "ONE_RETAINED_RESEARCH_FORMATION" in evidence["scan_conclusion"]
    assert state["retained_research_formations"] == ["ATTRACTION_SCAN_135-F1"]
    assert state["active_commercial_candidates"] == []
    assert state["active_transaction_units"] == []
    assert state["next_scan_id"] == "ATTRACTION_SCAN_136"
