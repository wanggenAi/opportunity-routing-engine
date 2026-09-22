import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_067.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan067_requires_confirmed_external_money_motion_and_zero_promotion():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_067"
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert len(scan["examined_formations"]) == 6
    assert "TWO_INDEPENDENT_CONFIRMED_EXTERNAL_MONEY_MOTIONS" in scan["search_mode"]
    assert all(len(x["confirmed_external_money_motions"]) >= 2 for x in scan["examined_formations"])


def test_scan067_separates_provider_payment_from_atomic_unit_payment():
    scan = load(SCAN)
    learnings = " ".join(scan["scan_learnings"])
    assert "UNBUNDLED_ATOMIC_EXECUTION_UNIT" in learnings
    assert "PAYMENT_ATTRIBUTABLE" in learnings
    verdicts = " ".join(x["verdict"] for x in scan["examined_formations"])
    assert "MATURE" in verdicts
    assert "HUMAN" in verdicts or "JUDGMENT" in verdicts


def test_scan067_advances_to_unit_attributed_payment_floor():
    scan = load(SCAN)
    state = load(STATE)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_068"
    assert "UNBUNDLED_ATOMIC_EXECUTION_UNIT" in scan["next_search_boundary"]
    assert "UNIT_OR_TASK_LEVEL_PRICE_ATTRIBUTION" in scan["next_search_boundary"]
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_067"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_068"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
