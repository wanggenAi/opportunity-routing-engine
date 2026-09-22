import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_071.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan071_is_broad_budget_reset_without_mechanism_inheritance():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_071"
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert len(scan["examined_formations"]) == 6
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["budget_source_policy"] == "DOWNSTREAM_BUDGET_EVIDENCE_NOT_DISCOVERY_ONTOLOGY"
    assert "BROAD_FORMATION_DIVERSE" in scan["search_mode"]
    assert "NO_REQUIRED_ATOMICITY_MULTI_SUPPLIER_ORCHESTRATION_ROUTING_FAILOVER_ABSTRACTION" in scan["search_mode"]


def test_scan071_runs_current_commercial_hard_floor_preflight():
    scan = load(SCAN)
    required = {
        "buyer_budget_evidence",
        "formation_frame",
        "exact_incumbent_preflight",
        "founder_independence_check",
        "data_action_rights_check",
        "normalized_margin_check",
        "verdict",
        "evidence_summary",
    }
    for formation in scan["examined_formations"]:
        assert required.issubset(formation)
        assert formation["buyer_budget_evidence"]
        assert formation["exact_incumbent_preflight"]
        assert formation["founder_independence_check"]
        assert formation["data_action_rights_check"]
        assert formation["normalized_margin_check"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan071_keeps_scan072_broad_instead_of_deriving_new_mechanism():
    scan = load(SCAN)
    state = load(STATE)
    learnings = " ".join(scan["scan_learnings"])
    assert "DIRECT_CURRENT_BUYER_BUDGET_IS_STRONG_ECONOMIC_EVIDENCE_BUT_NOT_WHITE_SPACE_BY_ITSELF" in learnings
    assert "ONE_BROAD_RESET_PASS_IS_NOT_ENOUGH_TO_DERIVE_A_NEW_MECHANISM_ONTOLOGY" in learnings
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_072"
    assert "BROAD_FORMATION_DIVERSE" in scan["next_search_boundary"]
    assert "NO_REQUIRED_MECHANISM_PRODUCT_SHAPE" in scan["next_search_boundary"]
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_071"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_072"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
