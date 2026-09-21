import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_060.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

def test_scan060_uses_non_role_purchase_evidence():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_060"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert len(scan["examined_formations"]) == 6
    assert all("JOB_POSTING" not in x["evidence_class"] for x in scan["examined_formations"])
    assert all(
        any(token in x["evidence_class"] for token in ("MONTHLY", "PURCHASE", "PRODUCTIZED"))
        for x in scan["examined_formations"]
    )

def test_scan060_is_formation_diverse():
    scan = load(SCAN)
    titles = {x["title"] for x in scan["examined_formations"]}
    assert titles == {
        "MONTHLY_WORDPRESS_CARE_AND_MAINTENANCE_PLAN",
        "MONTHLY_DEDICATED_GENERAL_VIRTUAL_ASSISTANT_SUBSCRIPTION",
        "UNLIMITED_GRAPHIC_AND_PRESENTATION_DESIGN_SUBSCRIPTION",
        "PODCAST_AUDIO_POSTPRODUCTION_PER_EPISODE_AND_MONTHLY_PLAN",
        "MANAGED_QA_AS_A_SERVICE_MONTHLY_OUTCOME_SUBSCRIPTION",
        "ON_DEMAND_CAD_DRAFTING_AND_ENGINEERING_DESIGN_PURCHASE",
    }

def test_scan060_closes_incumbent_service_or_human_residual_traps():
    scan = load(SCAN)
    verdicts = {x["formation_id"]: x["verdict"] for x in scan["examined_formations"]}
    assert "MANAGED_WORDPRESS_CARE" in verdicts["ATTRACTION_SCAN_060-F1"]
    assert "HUMAN_CAPACITY_SUBSCRIPTION" in verdicts["ATTRACTION_SCAN_060-F2"]
    assert "DESIGN_SUBSCRIPTION" in verdicts["ATTRACTION_SCAN_060-F3"]
    assert "AI_PODCAST_POSTPRODUCTION" in verdicts["ATTRACTION_SCAN_060-F4"]
    assert "MANAGED_QA_OUTCOME_CATEGORY" in verdicts["ATTRACTION_SCAN_060-F5"]
    assert "ENGINEERING_JUDGMENT_LIABILITY" in verdicts["ATTRACTION_SCAN_060-F6"]

def test_scan061_moves_observation_point_to_buyer_side_workarounds():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_061"
    boundary = scan["next_search_boundary"]
    assert "BUYER_SIDE_REPEATED_WORKAROUND_SPEND" in boundary
    assert "NO_JOB_POSTING_AS_SOLE_SIGNAL" in boundary
    assert "NO_EXISTING_PRODUCTIZED_SERVICE_AS_PRIMARY_SIGNAL" in boundary
    assert "NO_SCAN058_TO_SCAN060_VERTICAL_INHERITANCE" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert "FAIL_CLOSED_PROMOTION" in boundary

def test_state_advances_after_scan060():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_060"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_061"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert {x["formation_id"] for x in state["retained_research_formations"]} == {"ATTRACTION_SCAN_015-F1"}
