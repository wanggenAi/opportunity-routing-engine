import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_081.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan081_resets_upstream_to_actor_state_change_not_procurement_ontology():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_081"
    assert scan["status"] == "COMPLETE"
    assert scan["discovery_source_reset"] is True
    assert scan["inherited_mechanism_as_requirement"] is False
    assert "ACTOR_STATE_CHANGE_FIRST" in scan["search_mode"]
    assert "NO_JOB_GIG_RFQ_OR_PROCUREMENT_FEED_AS_DISCOVERY_ONTOLOGY" in scan["search_mode"]


def test_scan081_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("CARBON_DATA" in title for title in titles)
    assert any("EINVOICE" in title for title in titles)
    assert any("AI_AGENT_IDENTITY" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []


def test_scan081_fails_closed_on_exact_control_surfaces():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    f1 = formations["ATTRACTION_SCAN_081-F1"]
    f2 = formations["ATTRACTION_SCAN_081-F2"]
    f3 = formations["ATTRACTION_SCAN_081-F3"]
    assert any("KICOX" in x for x in f1["exact_incumbent_and_control_surface_preflight"])
    assert any("accredited" in x.lower() for x in f2["exact_incumbent_and_control_surface_preflight"])
    assert any("Microsoft Entra Agent ID" in x for x in f3["exact_incumbent_and_control_surface_preflight"])
    assert all(f["verdict"].startswith("DEMOTED_") for f in scan["examined_formations"])


def test_scan081_does_not_convert_stated_budget_or_security_pain_into_external_value_flow():
    scan = load(SCAN)
    f1, _, f3 = scan["examined_formations"]
    assert any("not proof of executed recurring payment" in x.lower() for x in f1["economic_signal"])
    assert any("does not treat security concern" in x.lower() for x in f3["economic_signal"])
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_scan081_requires_second_independent_broad_reality_pass_before_new_boundary():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_082"
    boundary = scan["next_search_boundary"]
    assert "SECOND_INDEPENDENT_BROAD_CURRENT_REALITY_ACTOR_STATE_CHANGE_FIRST" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert "NO_JOB_GIG_RFQ_OR_PROCUREMENT_FEED_AS_DISCOVERY_ONTOLOGY" in boundary


def test_scan081_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_081"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_081-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_082"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_082"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
