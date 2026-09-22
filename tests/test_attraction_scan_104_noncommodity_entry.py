import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_104.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan104_repeats_noncommodity_floor_with_explicit_fresh_entry():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_104"
    assert scan["status"] == "COMPLETE"
    assert scan["primary_research_domain"] == "CHINA"
    assert "SECOND_INDEPENDENT_OPERATOR_ACQUIRABLE_NON_COMMODITY_CONTROL_PLUS_EXTERNAL_ECONOMIC_MOTION_PASS" in scan["search_mode"]
    assert scan["drift_audit"]["operator_specific_noncommodity_control_required"] is True
    assert scan["drift_audit"]["fresh_operator_entry_acquirability_required"] is True
    assert scan["drift_audit"]["external_economic_motion_required"] is True


def test_scan104_is_fresh_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("APP_WITH_INSTALLED_USER_BASE" in title for title in titles)
    assert any("FIGMA_PLUGIN" in title for title in titles)
    assert any("PUBLISHER_OPERATED_MINIGAME" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan104_transferability_does_not_bypass_verification_or_platform_control():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}

    assert formations["ATTRACTION_SCAN_104-F1"]["operator_acquirability_check"].startswith("PARTIAL_PASS_")
    assert "NOT_PUBLICLY_VERIFIABLE" in formations["ATTRACTION_SCAN_104-F1"]["verdict"]

    assert formations["ATTRACTION_SCAN_104-F2"]["noncommodity_control_check"].startswith("PASS_")
    assert formations["ATTRACTION_SCAN_104-F2"]["operator_acquirability_check"].startswith("FAIL_DECISIVE_")
    assert "NONTRANSFERABLE" in formations["ATTRACTION_SCAN_104-F2"]["verdict"]

    assert formations["ATTRACTION_SCAN_104-F3"]["operator_acquirability_check"].startswith("PARTIAL_PASS_")
    assert "PUBLISHER_ALREADY_OWNS_THE_ORCHESTRATION_LAYER" in formations["ATTRACTION_SCAN_104-F3"]["verdict"]

    for formation in formations.values():
        assert formation["economic_signal"]
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert formation["fresh_operator_entry_acquirability_check"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan104_advances_only_to_executed_transfer_continuity_evidence():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_105"
    boundary = scan["next_search_boundary"]
    assert "EXECUTED_FRESH_OPERATOR_CONTROL_TRANSFER" in boundary
    assert "POST_TRANSFER_EXTERNAL_ECONOMIC_CONTINUITY" in boundary
    assert "EXCLUDE_SCAN060_TO_104_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE" in boundary


def test_scan104_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_104"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_104-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_105"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_105"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
