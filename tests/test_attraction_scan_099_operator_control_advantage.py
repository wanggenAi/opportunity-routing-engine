import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_099.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan099_uses_operator_control_advantage_evidence_first():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_099"
    assert scan["status"] == "COMPLETE"
    assert scan["primary_research_domain"] == "CHINA"
    assert "OPERATOR_CONTROL_ADVANTAGE_EVIDENCE_FIRST" in scan["search_mode"]
    assert scan["drift_audit"]["operator_control_advantage_evidence_required"] is True


def test_scan099_is_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("MERCHANT_OF_RECORD" in title for title in titles)
    assert any("CREDENTIAL" in title for title in titles)
    assert any("FOREIGN_AI_SUBSCRIPTION" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan099_control_advantages_are_real_but_not_unowned():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    assert "PASS_FOR_CONTROL_ADVANTAGE" in formations["ATTRACTION_SCAN_099-F1"]["generic_agent_substitutability_check"]
    assert "PASS_FOR_THE_SECRET_HOLDING_BOUNDARY" in formations["ATTRACTION_SCAN_099-F2"]["generic_agent_substitutability_check"]
    assert formations["ATTRACTION_SCAN_099-F3"]["data_action_rights_check"].startswith("FAIL_")
    for formation in formations.values():
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan099_requires_second_independent_control_pass():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_100"
    boundary = scan["next_search_boundary"]
    assert "SECOND_INDEPENDENT_OPERATOR_CONTROL_ADVANTAGE_EVIDENCE_PASS" in boundary
    assert "NATIVE_UPSTREAM_CONTROLS" in boundary
    assert "EXCLUDE_SCAN060_TO_099_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE" in boundary


def test_scan099_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_099"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_099-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_100"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_100"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
