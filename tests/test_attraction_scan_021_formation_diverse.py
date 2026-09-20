import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_021.json"
RESET = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan_021_is_formation_diverse_and_not_mechanism_locked():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_021"
    assert scan["search_mode"] == "FORMATION_DIVERSE_CLEAN_SLATE_ATTRACTION"
    assert scan["inherited_active_formation_as_seed"] is False
    assert scan["inherited_mechanism_as_requirement"] is False


def test_scan_021_does_not_fake_commercial_promotion():
    scan = load(SCAN)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_scan_021_retains_non_router_rights_execution_beacon_only_as_research():
    scan = load(SCAN)
    ids = {item["formation_id"] for item in scan["high_attraction_beacons"]}
    assert ids == {"ATTRACTION_SCAN_021-F1"}
    f1 = scan["high_attraction_beacons"][0]
    assert f1["mechanism_class"] == "RIGHTS_EXECUTION_COMPILATION"
    assert f1["commercial_candidate"] is False
    assert "EXACT_PAYER_WILLINGNESS_FOR_SELF_SERVE_COMPLAINT_PACKET_COMPILATION" in f1["decisive_unknowns"]
    assert "NON_LAW_FIRM_PRODUCT_BOUNDARY_FOR_RULE_APPLICATION_AND_DOCUMENT_GENERATION" in f1["decisive_unknowns"]


def test_generic_shared_manufacturing_is_not_promoted():
    scan = load(SCAN)
    generic = next(
        item for item in scan["examined_formations"]
        if item["title"] == "GENERIC_SHARED_MANUFACTURING_CAPACITY_PLATFORM"
    )
    assert generic["verdict"] == "DEMOTED_INCUMBENT_CROWDED"


def test_reset_state_advances_without_losing_prior_validation_queue():
    state = load(RESET)
    ids = {item["formation_id"] for item in state["retained_research_formations"]}
    assert ids == {
        "ATTRACTION_SCAN_015-F1",
        "ATTRACTION_SCAN_016-F1",
        "ATTRACTION_SCAN_021-F1",
    }
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_021"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_022"
