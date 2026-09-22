import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_069.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan069_requires_actual_multi_supplier_behavior_and_zero_promotion():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_069"
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert len(scan["examined_formations"]) == 6
    assert "CONCURRENT_PAID_SUPPLIERS" in scan["search_mode"]
    assert all(len(x["concurrent_supplier_evidence"]) >= 2 for x in scan["examined_formations"])


def test_scan069_does_not_upgrade_benchmarks_or_vendor_count_to_production_concurrency():
    scan = load(SCAN)
    learnings = " ".join(scan["scan_learnings"])
    verdicts = " ".join(x["verdict"] for x in scan["examined_formations"])
    assert "BENCHMARKING_OR_PILOTS" in learnings
    assert "ORCHESTRATION" in verdicts
    assert "PAID_CONCURRENT" in verdicts or "CONCURRENT_MULTI_PSP" in verdicts


def test_scan069_advances_to_buyer_built_abstraction_residual():
    scan = load(SCAN)
    state = load(STATE)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_070"
    assert "BUYER_BUILT_OR_SELF_HOSTED_MULTI_PROVIDER_ABSTRACTION" in scan["next_search_boundary"]
    assert "EXPLICIT_REJECTION_BYPASS_OR_CONTROL_REASON" in scan["next_search_boundary"]
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_069"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_070"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
