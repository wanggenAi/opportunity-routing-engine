import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_020.json"
MISSION = ROOT / "data" / "research_missions" / "attraction_field_broad_reality.json"
RESET = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan_020_detects_and_corrects_mechanism_bias():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_020"
    assert scan["search_mechanism_bias"] == "DETECTED_AND_CORRECTED"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan_021_is_formation_diverse_not_router_locked():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_021"
    assert scan["next_search_boundary"] == "FORMATION_DIVERSE_CLEAN_SLATE_ATTRACTION"


def test_recent_router_mechanism_seeds_are_removed_from_broad_mission():
    mission = load(MISSION)
    ids = {seed["seed_id"] for seed in mission["seeds"]}
    forbidden = {
        "user-owned-passive-realization-telemetry",
        "self-revealing-paid-rails-outcome-uncertainty",
        "cross-domain-transient-state-join",
        "outcome-asset-not-public-parameter-graph",
        "transaction-generated-acceptance-graph",
        "paid-ugly-workaround",
        "state-dependent-repricing",
        "dense-digital-exhaust-bilateral",
        "platform-leakage-offplatform",
        "repeat-route-compounds",
    }
    assert ids.isdisjoint(forbidden)


def test_formation_diverse_seeds_exist():
    mission = load(MISSION)
    ids = {seed["seed_id"] for seed in mission["seeds"]}
    required = {
        "formation-diversity-no-mechanism-inheritance",
        "distribution-access-breakthrough",
        "trust-proof-as-bridge",
        "shared-infrastructure-unlocks-small-actor",
        "coordination-compression-with-existing-payment",
        "compliance-transition-machine-service",
        "pooled-bargaining-or-demand-aggregation",
    }
    assert required.issubset(ids)


def test_existing_validation_queue_and_truth_are_preserved():
    state = load(RESET)
    ids = {item["formation_id"] for item in state["retained_research_formations"]}
    assert ids == {"ATTRACTION_SCAN_015-F1", "ATTRACTION_SCAN_016-F1"}
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_020"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_021"
