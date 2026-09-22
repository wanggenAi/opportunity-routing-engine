import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_092.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan092_repeats_residual_second_cost_floor_as_second_pass():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_092"
    assert scan["status"] == "COMPLETE"
    assert scan["search_mode"].startswith("SECOND_INDEPENDENT_PASS_")
    assert "PAID_COORDINATOR_RESIDUAL_FAILURE" in scan["search_mode"]
    assert "SECOND_LAYER_COST" in scan["search_mode"]
    assert scan["inherited_mechanism_as_requirement"] is False


def test_scan092_is_fresh_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("FIGMA" in title for title in titles)
    assert any("WEBFLOW" in title for title in titles)
    assert any("LIGHTROOM" in title for title in titles)
    assert scan["drift_audit"]["formation_diversity"].startswith("PASS_")
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan092_preserves_strict_executed_cost_and_same_outcome_truth():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}

    figma = formations["ATTRACTION_SCAN_092-F1"]
    assert figma["replicated_paid_residual_second_cost_check"].startswith("PARTIAL_FAIL_")

    webflow = formations["ATTRACTION_SCAN_092-F2"]
    assert webflow["replicated_paid_residual_second_cost_check"].startswith("FAIL_")

    lightroom = formations["ATTRACTION_SCAN_092-F3"]
    assert lightroom["second_layer_economic_cost_check"].startswith("PASS_")
    assert lightroom["residual_failure_after_payment_check"].startswith("PARTIAL_FAIL_")
    assert "ADJACENT_RESILIENCE" in lightroom["evidence_class"]


def test_scan092_double_spend_does_not_override_control_surface_kills():
    scan = load(SCAN)
    assert all(
        f["verdict"].startswith("DEMOTED_")
        for f in scan["examined_formations"]
    )
    assert all(
        f["data_action_rights_check"].startswith("FAIL_")
        for f in scan["examined_formations"]
    )


def test_scan092_two_pass_learning_resets_discovery_source():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_093"
    boundary = scan["next_search_boundary"]
    assert boundary.startswith("BROAD_CURRENT_REALITY_SOURCE_RESET_")
    assert "WITHOUT_STARTING_FROM_EXISTING_PAID_PRODUCTS" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert scan["drift_audit"]["response"].startswith(
        "RESET_DISCOVERY_SOURCE_TO_BROAD_CURRENT_REALITY"
    )
    assert any(
        "TWO_INDEPENDENT_RESIDUAL_SECOND_COST_PASSES" in x
        for x in scan["scan_learnings"]
    )


def test_scan092_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_092"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_092-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_093"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_093"
    assert (
        state["parallel_workstreams"]["discovery"]["search_boundary"]
        == scan["next_search_boundary"]
    )
