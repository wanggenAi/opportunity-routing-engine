import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_100.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan100_repeats_operator_control_advantage_independently():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_100"
    assert scan["status"] == "COMPLETE"
    assert scan["primary_research_domain"] == "CHINA"
    assert "SECOND_INDEPENDENT_OPERATOR_CONTROL_ADVANTAGE_EVIDENCE_PASS" in scan["search_mode"]
    assert scan["drift_audit"]["operator_control_advantage_evidence_required"] is True


def test_scan100_is_fresh_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("ICP_ACCESS_FILING" in title for title in titles)
    assert any("APPLE_DEVELOPER" in title for title in titles)
    assert any("PARCEL_PICKUP_DATA" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan100_distinguishes_control_existence_from_operator_acquirability():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    assert formations["ATTRACTION_SCAN_100-F1"]["data_action_rights_check"].startswith("PARTIAL_PASS")
    assert formations["ATTRACTION_SCAN_100-F2"]["data_action_rights_check"].startswith("PARTIAL_PASS")
    assert formations["ATTRACTION_SCAN_100-F3"]["data_action_rights_check"].startswith("FAIL_")
    for formation in formations.values():
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan100_advances_evidence_priority_without_inheriting_product_mechanism():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_101"
    boundary = scan["next_search_boundary"]
    assert "OPERATOR_ACQUIRABLE_CONTROL_ASSET_EVIDENCE_FIRST" in boundary
    assert "EXTERNAL_ECONOMIC_MOTION" in boundary
    assert "STANDARDIZED_LEGAL_CHANNELS" in boundary
    assert "EXCLUDE_SCAN060_TO_100_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_PRODUCT_MECHANISM_INHERITANCE" in boundary


def test_scan100_updates_reset_state_without_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_100"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_100-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_101"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_101"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
