import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_082.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan082_is_second_independent_broad_actor_state_pass():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_082"
    assert scan["status"] == "COMPLETE"
    assert "SECOND_INDEPENDENT_BROAD_CURRENT_REALITY_ACTOR_STATE_CHANGE_FIRST" in scan["search_mode"]
    assert scan["inherited_mechanism_as_requirement"] is False
    assert "NO_JOB_GIG_RFQ_OR_PROCUREMENT_FEED_AS_DISCOVERY_ONTOLOGY" in scan["search_mode"]


def test_scan082_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("CAREGIVER" in title for title in titles)
    assert any("WILDFIRE" in title for title in titles)
    assert any("USED_EV_BATTERY" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan082_fails_closed_on_rights_physical_or_exact_control_surfaces():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    f1 = formations["ATTRACTION_SCAN_082-F1"]
    f2 = formations["ATTRACTION_SCAN_082-F2"]
    f3 = formations["ATTRACTION_SCAN_082-F3"]
    assert "HUMAN" in f1["founder_independence_check"]
    assert "PHYSICAL" in f2["founder_independence_check"]
    assert any("AVILOO" in x for x in f3["exact_incumbent_and_control_surface_preflight"])
    assert all(f["verdict"].startswith("DEMOTED_") for f in scan["examined_formations"])


def test_scan082_changes_evidence_object_not_product_mechanism():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_083"
    boundary = scan["next_search_boundary"]
    assert "BILATERAL_PARTIAL_FLOW_FIRST" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert "NO_JOB_GIG_RFQ_OR_PROCUREMENT_FEED_AS_DISCOVERY_ONTOLOGY" in boundary


def test_scan082_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_082"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_082-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_083"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_083"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
