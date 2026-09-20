import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_019.json"
MISSION = ROOT / "data" / "research_missions" / "attraction_field_broad_reality.json"
RESET = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan_019_truthfully_retains_zero():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_019"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["high_attraction_beacons"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_scan_019_nearest_misses_are_not_promotions():
    scan = load(SCAN)
    directions = {item["direction"] for item in scan["nearest_misses"]}
    assert "TRAVEL_ESIM_REALIZED_CONNECTIVITY_ROUTING" in directions
    assert "ROADSIDE_ASSISTANCE_NETWORK_META_ROUTER" in directions
    assert "GOLD_REALIZED_PAYOUT_ROUTING" in directions
    assert scan["retained_research_formations"] == []


def test_existing_validation_queue_is_unchanged():
    scan = load(SCAN)
    assert set(scan["parallel_validation_queue"]) == {
        "ATTRACTION_SCAN_015-F1",
        "ATTRACTION_SCAN_016-F1",
    }


def test_scan_020_boundary_requires_passive_user_owned_realization():
    scan = load(SCAN)
    mission = load(MISSION)
    seed_ids = {seed["seed_id"] for seed in mission["seeds"]}
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_020"
    assert scan["next_search_boundary"] == (
        "USER_OWNED_PASSIVE_REALIZATION_TELEMETRY_X_MULTIPLE_PAID_CALLABLE_RAILS_X_"
        "LOW_FRICTION_REPEAT_SWITCH"
    )
    assert "user-owned-passive-realization-telemetry" in seed_ids
    assert "broad-reality-no-active-vertical-inheritance" in seed_ids


def test_portfolio_remains_unpromoted():
    state = load(RESET)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_019"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_020"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
