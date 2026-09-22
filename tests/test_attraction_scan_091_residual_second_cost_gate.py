import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_091.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan091_raises_to_residual_failure_plus_executed_second_cost():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_091"
    assert scan["status"] == "COMPLETE"
    assert scan["search_mode"].startswith("FIRST_PASS_")
    assert "PAID_COORDINATOR_RESIDUAL_FAILURE" in scan["search_mode"]
    assert "SECOND_LAYER_COST" in scan["search_mode"]
    assert scan["inherited_mechanism_as_requirement"] is False


def test_scan091_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("ECOMMERCE" in title for title in titles)
    assert any("COLD_EMAIL" in title for title in titles)
    assert any("HOME_ASSISTANT" in title for title in titles)
    assert scan["drift_audit"]["formation_diversity"].startswith("PASS_")
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan091_enforces_strict_double_cost_truth():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}

    ecommerce = formations["ATTRACTION_SCAN_091-F1"]
    assert ecommerce["second_layer_economic_cost_check"].startswith("PASS_")
    assert ecommerce["replicated_paid_residual_second_cost_check"].startswith(
        "PARTIAL_FAIL_"
    )

    outbound = formations["ATTRACTION_SCAN_091-F2"]
    assert outbound["paid_coordinator_check"].startswith("PASS_")
    assert outbound["residual_failure_after_payment_check"].startswith("PASS_")
    assert outbound["second_layer_economic_cost_check"].startswith("PASS_")
    assert outbound["replicated_paid_residual_second_cost_check"].startswith("PASS_")

    smart_home = formations["ATTRACTION_SCAN_091-F3"]
    assert smart_home["second_layer_economic_cost_check"].startswith("FAIL_")
    assert smart_home["replicated_paid_residual_second_cost_check"].startswith("FAIL_")
    assert "FUTURE" in smart_home["verdict"] or "NOT_YET_EXECUTED" in smart_home["verdict"]


def test_scan091_double_cost_does_not_override_control_surface_kills():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}

    outbound = formations["ATTRACTION_SCAN_091-F2"]
    assert outbound["no_single_current_control_surface_check"].startswith("FAIL_")
    assert outbound["data_action_rights_check"].startswith("FAIL_")
    assert outbound["normalized_margin_check"].startswith("FAIL_")

    assert all(
        f["verdict"].startswith("DEMOTED_")
        for f in scan["examined_formations"]
    )


def test_scan091_repeats_same_floor_before_deriving_another_signal():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_092"
    boundary = scan["next_search_boundary"]
    assert boundary.startswith("SECOND_INDEPENDENT_PASS_")
    assert "PAID_COORDINATOR_RESIDUAL_FAILURE" in boundary
    assert "ACTUAL_EXECUTED_ADDITIONAL_PAYMENT" in boundary
    assert "FUTURE_PLANNED_OR_CATEGORY_LEVEL_COST_DOES_NOT_PASS" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert any(
        "ONE_PASS_IS_INSUFFICIENT" in x
        for x in scan["scan_learnings"]
    )


def test_scan091_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_091"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_091-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_092"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_092"
    assert (
        state["parallel_workstreams"]["discovery"]["search_boundary"]
        == scan["next_search_boundary"]
    )
