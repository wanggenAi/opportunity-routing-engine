import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_110.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan110_uses_outcome_complete_identity_packet_priority():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_110"
    assert scan["status"] == "COMPLETE"
    assert scan["primary_research_domain"] == "CHINA"
    assert "OUTCOME_COMPLETE_IDENTITY_PACKET_PRIORITY" in scan["search_mode"]
    audit = scan["drift_audit"]
    assert audit["outcome_complete_identity_packet_priority_used"] is True
    assert audit["same_operator_and_control_position_binding_required"] is True
    assert audit["owner_shadow_wage_or_replacement_cost_required"] is True
    assert audit["rights_closure_required"] is True
    assert audit["realized_or_bounded_exit_value_required_for_normalization"] is True


def test_scan110_is_fail_closed_and_formation_diverse():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("TEA_FRANCHISE" in x for x in titles)
    assert any("IP_GUIDANCE_LIABILITY" in x for x in titles)
    assert any("BEER_SALES_INCENTIVE" in x for x in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan110_does_not_confuse_legal_outcome_with_operating_cashflow():
    scan = load(SCAN)
    f = {x["formation_id"]: x for x in scan["examined_formations"]}

    assert f["ATTRACTION_SCAN_110-F1"]["executed_control_transfer_check"].startswith("PASS_")
    assert f["ATTRACTION_SCAN_110-F1"]["post_transfer_external_economic_continuity_check"].startswith("UNKNOWN_")
    assert f["ATTRACTION_SCAN_110-F1"]["normalized_margin_check"].startswith("FAIL_TO_CLOSE_")

    assert f["ATTRACTION_SCAN_110-F2"]["same_operator_economic_binding_check"].startswith("PARTIAL_PASS_")
    assert f["ATTRACTION_SCAN_110-F2"]["data_action_rights_check"].startswith("FAIL_")
    assert f["ATTRACTION_SCAN_110-F2"]["normalized_margin_check"].startswith("FAIL_TO_CLOSE_")

    assert f["ATTRACTION_SCAN_110-F3"]["post_transfer_external_economic_continuity_check"].startswith("FAIL_TO_CLOSE_")
    assert f["ATTRACTION_SCAN_110-F3"]["same_operator_economic_binding_check"].startswith("PARTIAL_PASS_")
    assert f["ATTRACTION_SCAN_110-F3"]["normalized_margin_check"].startswith("FAIL_TO_CLOSE_")

    for formation in f.values():
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan110_excludes_weak_or_unbound_outcome_packets():
    scan = load(SCAN)
    excluded = {x["observation"]: x["excluded_reason"] for x in scan["excluded_observations"]}
    assert any("MARTIAL_ARTS" in x for x in excluded)
    assert any("TWO_STORE_OR_MULTI_VICTIM" in x for x in excluded)
    assert any("LAW_FIRM_MARKETING" in x for x in excluded)


def test_scan110_advances_to_auditable_ledger_plus_outcome_method():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_111"
    boundary = scan["next_search_boundary"]
    assert "AUDITABLE_LEDGER_PLUS_OUTCOME_PACKET_PRIORITY" in boundary
    assert "AUDITABLE_RECEIVED_CUSTOMER_REVENUE" in boundary
    assert "INDEPENDENT_EXIT_SETTLEMENT_TRANSFER_OR_RESIDUAL_EVIDENCE" in boundary
    assert "EXCLUDE_SCAN060_TO_110_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary


def test_scan110_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_110"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_110-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_111"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_111"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
