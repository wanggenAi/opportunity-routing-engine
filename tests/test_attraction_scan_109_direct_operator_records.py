import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_109.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan109_uses_direct_operator_record_priority_without_lowering_floor():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_109"
    assert scan["status"] == "COMPLETE"
    assert scan["primary_research_domain"] == "CHINA"
    assert "DIRECT_OPERATOR_RECORD_PRIORITY" in scan["search_mode"]
    audit = scan["drift_audit"]
    assert audit["direct_operator_record_priority_used"] is True
    assert audit["same_operator_and_control_position_binding_required"] is True
    assert audit["owner_shadow_wage_or_replacement_cost_required"] is True
    assert audit["rights_closure_required"] is True
    assert audit["realized_or_bounded_exit_value_required_for_normalization"] is True


def test_scan109_is_fresh_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("SHRIMP_HOTPOT" in title for title in titles)
    assert any("PAID_STUDY_ROOM" in title for title in titles)
    assert any("LIQUOR_SHOP" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan109_direct_operator_packets_are_not_overclaimed():
    scan = load(SCAN)
    formations = {x["formation_id"]: x for x in scan["examined_formations"]}

    f1 = formations["ATTRACTION_SCAN_109-F1"]
    assert f1["executed_control_transfer_check"].startswith("PASS_")
    assert f1["post_transfer_external_economic_continuity_check"].startswith("PASS_NEGATIVE")
    assert f1["same_operator_economic_binding_check"].startswith("PARTIAL_PASS_")
    assert f1["founder_independence_check"].startswith("FAIL_")

    f2 = formations["ATTRACTION_SCAN_109-F2"]
    assert f2["executed_control_transfer_check"].startswith("PASS_")
    assert f2["same_operator_economic_binding_check"].startswith("FAIL_")
    assert f2["normalized_margin_check"].startswith("FAIL_TO_CLOSE_")
    assert f2["generic_agent_substitutability_check"].startswith("FAIL_")

    f3 = formations["ATTRACTION_SCAN_109-F3"]
    assert f3["post_transfer_external_economic_continuity_check"].startswith("PASS_")
    assert f3["owner_labor_check"].startswith("FAIL_")
    assert f3["founder_independence_check"].startswith("FAIL_")
    assert f3["generic_agent_substitutability_check"].startswith("FAIL_")

    for formation in formations.values():
        assert formation["economic_signal"]
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan109_preserves_non_stitching_and_rejects_weak_sources():
    scan = load(SCAN)
    excluded = {x["observation"]: x["excluded_reason"] for x in scan["excluded_observations"]}
    assert any("TWO_WAIMAI_FRANCHISE_STORES" in key for key in excluded)
    assert any("CLOUD_UNATTENDED_CONVENIENCE" in key for key in excluded)
    assert any("VENDOR_OR_SEO" in key for key in excluded)


def test_scan109_advances_evidence_method_not_vertical():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_110"
    boundary = scan["next_search_boundary"]
    assert "OUTCOME_COMPLETE_IDENTITY_PACKET_PRIORITY" in boundary
    assert "DIRECT_OPERATOR_RECORD_PLUS_INDEPENDENT_CLOSURE_SETTLEMENT_TRANSFER_OR_OTHER_OUTCOME_DOCUMENT" in boundary
    assert "SAME_OPERATOR_SAME_CONTROL_POSITION_AND_SAME_TIME_WINDOW" in boundary
    assert "EXCLUDE_SCAN060_TO_109_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary


def test_scan109_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_109"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_109-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_110"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_110"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
