import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_070.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan070_requires_buyer_built_or_self_hosted_residual_and_zero_promotion():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_070"
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert len(scan["examined_formations"]) == 6
    assert "BUYER_BUILT_OR_SELF_HOSTED_MULTI_PROVIDER_ABSTRACTION" in scan["search_mode"]
    assert all(x["buyer_built_evidence"] for x in scan["examined_formations"])


def test_scan070_distinguishes_custom_control_from_existing_open_control_plane():
    scan = load(SCAN)
    verdicts = " ".join(x["verdict"] for x in scan["examined_formations"])
    learnings = " ".join(scan["scan_learnings"])
    assert "SELF_HOST" in verdicts or "OPEN_SOURCE" in verdicts
    assert "SELF_HOSTING_MUST_NOT_BE_CONFUSED_WITH_BUYER_BUILD" in learnings
    assert "HIDDEN_MECHANISM_ONTOLOGY" in learnings


def test_scan070_resets_scan071_instead_of_narrowing_again():
    scan = load(SCAN)
    state = load(STATE)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_071"
    assert "BROAD_FORMATION_DIVERSE" in scan["next_search_boundary"]
    assert "NO_REQUIRED_ATOMICITY_MULTI_SUPPLIER_ORCHESTRATION_ROUTING_FAILOVER_ABSTRACTION" in scan["next_search_boundary"]
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_070"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_071"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
