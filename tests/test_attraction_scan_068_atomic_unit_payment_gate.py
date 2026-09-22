import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_068.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan068_requires_atomic_payment_attribution_and_zero_promotion():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_068"
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert len(scan["examined_formations"]) == 6
    assert "UNIT_OR_TASK_LEVEL_PRICE_ATTRIBUTION" in scan["search_mode"]
    assert all(len(x["confirmed_atomic_payments"]) >= 2 for x in scan["examined_formations"])


def test_scan068_separates_atomic_economics_from_white_space():
    scan = load(SCAN)
    learnings = " ".join(scan["scan_learnings"])
    verdicts = " ".join(x["verdict"] for x in scan["examined_formations"])
    assert "API_UTILITY" in learnings or "METER" in learnings or "COMMODITY" in verdicts
    assert "HUMAN" in verdicts
    assert "ORCHESTRATION" in learnings or "ORCHESTRATION" in verdicts


def test_scan068_advances_to_observed_multi_supplier_spend_floor():
    scan = load(SCAN)
    state = load(STATE)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_069"
    assert "CONCURRENT_PAID_SUPPLIERS" in scan["next_search_boundary"]
    assert "BUYER_CONTROLLED_SWITCHING_OR_FALLBACK" in scan["next_search_boundary"]
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_068"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_069"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
