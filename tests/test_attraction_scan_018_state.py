import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_018.json"
MISSION = ROOT / "data" / "research_missions" / "attraction_field_broad_reality.json"
RESET = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan_018_allows_zero_retention_after_exception_falsification():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_018"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["high_attraction_beacons"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_existing_validation_queue_survives_scan_018():
    scan = load(SCAN)
    assert set(scan["parallel_validation_queue"]) == {
        "ATTRACTION_SCAN_015-F1",
        "ATTRACTION_SCAN_016-F1",
    }


def test_scan_019_boundary_requires_paid_callable_outcome_uncertainty():
    scan = load(SCAN)
    mission = load(MISSION)
    seed_ids = {seed["seed_id"] for seed in mission["seeds"]}
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_019"
    assert scan["next_search_boundary"] == (
        "SELF_REVEALING_HIGH_INTENT_X_MULTIPLE_PAID_CALLABLE_RAILS_X_"
        "POST_EXECUTION_OUTCOME_UNCERTAINTY"
    )
    assert "self-revealing-paid-rails-outcome-uncertainty" in seed_ids
    assert "broad-reality-no-active-vertical-inheritance" in seed_ids


def test_scan_018_does_not_promote_exception_urgency_into_candidate_truth():
    scan = load(SCAN)
    learnings = set(scan["scan_learnings"])
    assert "TRANSIENT_EXCEPTION_VALUE_DOES_NOT_IMPLY_AN_UNOWNED_ROUTING_LAYER" in learnings
    assert "CROSS_DOMAIN_JOIN_ALONE_IS_NOT_DISTINCT_OPERATOR_CONTROL" in learnings


def test_portfolio_remains_truthfully_unpromoted():
    state = load(RESET)
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_018"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_019"
