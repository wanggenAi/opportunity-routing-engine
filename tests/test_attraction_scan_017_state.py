import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_017.json"
MISSION = ROOT / "data" / "research_missions" / "attraction_field_broad_reality.json"
RESET = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan_017_allows_truthful_zero_retention():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_017"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["high_attraction_beacons"] == []
    assert scan["retained_research_formations"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_scan_017_does_not_drop_existing_validation_queue():
    scan = load(SCAN)
    assert set(scan["parallel_validation_queue"]) == {
        "ATTRACTION_SCAN_015-F1",
        "ATTRACTION_SCAN_016-F1",
    }


def test_scan_018_boundary_is_cross_domain_not_vertical_inheritance():
    scan = load(SCAN)
    mission = load(MISSION)
    seed_ids = {seed["seed_id"] for seed in mission["seeds"]}
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_018"
    assert (
        scan["next_search_boundary"]
        == "TIME_SENSITIVE_CROSS_DOMAIN_STATE_JOIN_BETWEEN_MATURE_INDEPENDENT_PLATFORMS"
    )
    assert "cross-domain-transient-state-join" in seed_ids
    assert "broad-reality-no-active-vertical-inheritance" in seed_ids


def test_current_portfolio_still_has_no_commercial_candidate():
    state = load(RESET)
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    ids = {item["formation_id"] for item in state["retained_research_formations"]}
    assert ids == {"ATTRACTION_SCAN_015-F1", "ATTRACTION_SCAN_016-F1"}
