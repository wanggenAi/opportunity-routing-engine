import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_089.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan089_requires_replicated_paid_cross_component_coordination():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_089"
    assert scan["status"] == "COMPLETE"
    assert "INDEPENDENTLY_REPLICATED_PAID_CROSS_COMPONENT_COORDINATION" in scan["search_mode"]
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["drift_audit"]["independent_replication_floor"].startswith("PASS_")
    assert scan["drift_audit"]["paid_coordination_floor"].startswith("PASS_")


def test_scan089_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("AWARD_TRAVEL" in title for title in titles)
    assert any("FINANCIAL_AGGREGATION" in title for title in titles)
    assert any("WORKOUT_DATA_SYNC" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan089_each_formation_has_actual_coordination_payment_and_multiple_components():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert len(formation["existing_components"]) >= 2
        assert len(formation["independent_replication"]) >= 2
        assert len(formation["participant_authored_successful_completion"]) >= 2
        assert len(formation["explicit_participant_incompleteness_reason"]) >= 2
        assert formation["actual_cross_component_coordination_payment_check"].startswith("PASS_")
        assert formation["manual_multi_component_completion_check"].startswith("PASS_")
        assert formation["no_single_current_control_surface_check"].startswith("PASS_")
        assert formation["decisive_completion_control"].startswith("PASS_")


def test_scan089_closes_exact_paid_incumbents_and_rights_bound_residuals():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    assert "SEATS_AERO_ALREADY_OWNS_THE_EXACT_SEARCH_ALERTING_LAYER" in formations["ATTRACTION_SCAN_089-F1"]["verdict"]
    assert "MONARCH_ALREADY_OWNS_THE_EXACT_SUBSCRIPTION_AGGREGATION_LAYER" in formations["ATTRACTION_SCAN_089-F2"]["verdict"]
    assert "HEALTHFIT_AND_RUNGAP_ALREADY_OWN_THE_EXACT_COORDINATION_FUNCTION" in formations["ATTRACTION_SCAN_089-F3"]["verdict"]
    assert all(f["verdict"].startswith("DEMOTED_") for f in formations.values())
    assert all(f["data_action_rights_check"].startswith("FAIL_") for f in formations.values())
    assert all(f["normalized_margin_check"].startswith("FAIL_") for f in formations.values())


def test_scan089_runs_second_paid_coordination_pass_before_new_mechanism():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_090"
    boundary = scan["next_search_boundary"]
    assert "SECOND_INDEPENDENT_PASS" in boundary
    assert "INDEPENDENTLY_REPLICATED_PAID_CROSS_COMPONENT_COORDINATION" in boundary
    assert "ACTUAL_PAYMENT_TO_A_DISTINCT_NON_INCUMBENT_SOFTWARE_OR_SERVICE" in boundary
    assert "NO_SINGLE_CURRENT_CONTROL_SURFACE_OWNS_THE_END_TO_END_OUTCOME" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary


def test_scan089_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_089"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_089-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_090"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_090"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
