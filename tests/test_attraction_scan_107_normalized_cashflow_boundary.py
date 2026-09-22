import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_107.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan107_requires_same_operator_normalized_cashflow():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_107"
    assert scan["status"] == "COMPLETE"
    assert scan["primary_research_domain"] == "CHINA"
    assert "FIRST_INDEPENDENT_SMALL_OPERATOR_VERIFIED_NET_CASHFLOW_CONTROL_PASS" in scan["search_mode"]
    audit = scan["drift_audit"]
    assert audit["same_operator_and_control_position_binding_required"] is True
    assert audit["owner_shadow_wage_or_replacement_cost_required"] is True
    assert audit["rights_closure_required"] is True
    assert audit["realized_or_bounded_exit_value_required_for_normalization"] is True


def test_scan107_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("CONVENIENCE" in title for title in titles)
    assert any("HOMESTAY" in title for title in titles)
    assert any("LOTTERY" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan107_does_not_stitch_cross_entity_economics():
    scan = load(SCAN)
    f = {x["formation_id"]: x for x in scan["examined_formations"]}

    f1 = f["ATTRACTION_SCAN_107-F1"]
    assert f1["fresh_small_operator_entry_check"].startswith("PASS_")
    assert f1["same_operator_economic_binding_check"].startswith("PARTIAL_PASS_")
    assert f1["owner_labor_check"].startswith("FAIL_")
    assert f1["normalized_margin_check"].startswith("FAIL_TO_CLOSE_")

    f2 = f["ATTRACTION_SCAN_107-F2"]
    assert f2["executed_control_transfer_check"].startswith("PASS_")
    assert f2["same_operator_economic_binding_check"].startswith("FAIL_")
    assert "DIFFERENT_ENTITY" in f2["direct_operating_cost_check"]

    f3 = f["ATTRACTION_SCAN_107-F3"]
    assert f3["fresh_small_operator_entry_check"].startswith("PASS_")
    assert f3["post_transfer_external_economic_continuity_check"].startswith("PARTIAL_PASS_")
    assert f3["owner_labor_check"].startswith("FAIL_")
    assert f3["data_action_rights_check"].startswith("UNKNOWN_TO_PARTIAL_")

    for formation in f.values():
        assert formation["economic_signal"]
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan107_excludes_machine_lightened_examples_without_full_control_packet():
    scan = load(SCAN)
    excluded = {x["observation"]: x["excluded_reason"] for x in scan["excluded_observations"]}
    assert any("SELF_SERVICE_BILLIARD" in key for key in excluded)
    assert any("SHARED_POWER_BANK" in key for key in excluded)


def test_scan107_advances_to_second_independent_same_operator_pass():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_108"
    boundary = scan["next_search_boundary"]
    assert "SECOND_INDEPENDENT_SMALL_OPERATOR_VERIFIED_NET_CASHFLOW_CONTROL_PASS" in boundary
    assert "SAME_OPERATOR_SAME_CONTROL_POSITION_AND_SAME_TIME_WINDOW_BINDING" in boundary
    assert "OWNER_LABOR_OR_EXPLICIT_OUTSOURCED_REPLACEMENT_COST" in boundary
    assert "REALIZED_OR_BOUNDED_EXIT_VALUE" in boundary
    assert "EXCLUDE_SCAN060_TO_107_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary


def test_scan107_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_107"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_107-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_108"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_108"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
