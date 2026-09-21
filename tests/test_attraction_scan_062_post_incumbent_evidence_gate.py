import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_062.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

def test_scan062_is_second_independent_buyer_workaround_pass():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_062"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_active_formation_as_seed"] is False
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert len(scan["examined_formations"]) == 6
    assert "SECOND_INDEPENDENT" in scan["search_mode"]
    assert "NO_SCAN061_VERTICAL_INHERITANCE" in scan["search_mode"]

def test_scan062_is_formation_diverse():
    scan = load(SCAN)
    titles = {x["title"] for x in scan["examined_formations"]}
    assert titles == {
        "M365_AZURE_EMPLOYEE_LIFECYCLE_MANUAL_HANDOFF",
        "MANUFACTURING_ERP_TO_PHYSICAL_INVENTORY_TRUTH_GAP",
        "DENTAL_INSURANCE_ELIGIBILITY_BENEFIT_MANUAL_VERIFICATION",
        "LAW_FIRM_CASE_STATUS_SPREADSHEET_CONTROL",
        "RESTAURANT_INVENTORY_AND_FOOD_COST_RELIABILITY_GAP",
        "BIOTECH_LAB_REAGENT_CONSUMABLE_INVENTORY_SHADOW_SYSTEM",
    }

def test_scan062_distinguishes_white_space_from_process_tail():
    scan = load(SCAN)
    verdicts = {x["formation_id"]: x["verdict"] for x in scan["examined_formations"]}
    assert "ENTRA_JML" in verdicts["ATTRACTION_SCAN_062-F1"]
    assert "PHYSICAL_EVENT_CAPTURE" in verdicts["ATTRACTION_SCAN_062-F2"]
    assert "DENTAL_ELIGIBILITY" in verdicts["ATTRACTION_SCAN_062-F3"]
    assert "LEGAL_CASE" in verdicts["ATTRACTION_SCAN_062-F4"]
    assert "RESTAURANT_INVENTORY" in verdicts["ATTRACTION_SCAN_062-F5"]
    assert "LAB_INVENTORY_LIMS" in verdicts["ATTRACTION_SCAN_062-F6"]

def test_scan063_escalates_to_post_incumbent_residual_evidence():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_063"
    boundary = scan["next_search_boundary"]
    assert "PERSISTENT_WORKAROUND_AFTER_ACTIVE_OR_PAID_INCUMBENT_ADOPTION_OR_FAILED_SOFTWARE_ATTEMPT" in boundary
    assert "FORMATION_DIVERSE" in boundary
    assert "DIGITAL_OR_DELEGATABLE_RESIDUAL_EDGE" in boundary
    assert "NO_SCAN061_OR_SCAN062_VERTICAL_INHERITANCE" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert "FAIL_CLOSED_PROMOTION" in boundary

def test_state_advances_after_scan062():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_062"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_063"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert {x["formation_id"] for x in state["retained_research_formations"]} == {"ATTRACTION_SCAN_015-F1"}
