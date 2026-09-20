import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MISSION = ROOT / "data" / "research_missions" / "attraction_field_broad_reality.json"
RESET = ROOT / "data" / "commercial_reset_state.json"
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_016.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_validation_wait_does_not_block_broad_discovery():
    mission = load(MISSION)
    policy = mission["discovery_concurrency"]
    assert policy["validation_wait_does_not_block_discovery"] is True
    assert policy["active_formations_must_not_seed_new_broad_scan"] is True
    assert policy["active_formation_validation_queue_is_separate"] is True


def test_active_used_device_formation_is_not_a_broad_scan_seed():
    mission = load(MISSION)
    seed_ids = {seed["seed_id"] for seed in mission["seeds"]}
    assert "realized-payout-not-display-quote" not in seed_ids
    assert "cross-rail-outcome-rights" not in seed_ids
    assert "broad-reality-no-active-vertical-inheritance" in seed_ids


def test_scan_016_is_retained_without_commercial_promotion():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_016"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_beacons"][0]["formation_id"] == "ATTRACTION_SCAN_016-F1"
    assert scan["retained_research_beacons"][0]["commercial_candidate"] is False
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_parallel_portfolio_tracks_both_research_formations():
    state = load(RESET)
    ids = {item["formation_id"] for item in state["retained_research_formations"]}
    assert "ATTRACTION_SCAN_015-F1" in ids
    assert "ATTRACTION_SCAN_016-F1" in ids
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_016"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_017"
    assert state["active_commercial_candidates"] == []
