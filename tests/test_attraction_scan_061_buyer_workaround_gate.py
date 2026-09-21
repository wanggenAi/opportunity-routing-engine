import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_061.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

def test_scan061_starts_from_buyer_side_workarounds():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_061"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert len(scan["examined_formations"]) == 6
    assert all("BUYER_SIDE" in x["evidence_class"] for x in scan["examined_formations"])
    assert "NO_EXISTING_PRODUCTIZED_SERVICE_AS_PRIMARY_SIGNAL" in scan["search_mode"]

def test_scan061_is_formation_diverse():
    scan = load(SCAN)
    titles = {x["title"] for x in scan["examined_formations"]}
    assert titles == {
        "MULTI_MARKETPLACE_INVENTORY_MANUAL_RECONCILIATION",
        "SHORT_TERM_RENTAL_CALENDAR_CLEANER_PRICING_STACK",
        "MULTI_BUSINESS_LOW_VOLUME_ACCOUNTING_CONSOLIDATION",
        "SOLO_ACCOUNTING_PRACTICE_SOFTWARE_STACK_CONSOLIDATION",
        "CONSTRUCTION_CREW_SCHEDULING_EXCEL_PLUS_QUICKBOOKS_WORKAROUND",
        "PODCAST_PRODUCTION_DISTRIBUTION_SUBSCRIPTION_SPRAWL",
    }

def test_scan061_closes_exact_control_surfaces():
    scan = load(SCAN)
    verdicts = {x["formation_id"]: x["verdict"] for x in scan["examined_formations"]}
    assert "MULTICHANNEL_INVENTORY_SYNC" in verdicts["ATTRACTION_SCAN_061-F1"]
    assert "STR_OPERATIONS" in verdicts["ATTRACTION_SCAN_061-F2"]
    assert "MULTI_COMPANY_ACCOUNTING" in verdicts["ATTRACTION_SCAN_061-F3"]
    assert "ACCOUNTING_PRACTICE_MANAGEMENT" in verdicts["ATTRACTION_SCAN_061-F4"]
    assert "CREW_SCHEDULING" in verdicts["ATTRACTION_SCAN_061-F5"]
    assert "PODCAST" in verdicts["ATTRACTION_SCAN_061-F6"]

def test_scan062_runs_second_independent_buyer_workaround_sample():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_062"
    boundary = scan["next_search_boundary"]
    assert "SECOND_INDEPENDENT" in boundary
    assert "BUYER_SIDE_REPEATED_WORKAROUND_SPEND" in boundary
    assert "NO_SELLER_DEFINED_CATEGORY_AS_PRIMARY_SIGNAL" in boundary
    assert "NO_SCAN061_VERTICAL_INHERITANCE" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert "FAIL_CLOSED_PROMOTION" in boundary

def test_state_advances_after_scan061():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_061"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_062"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert {x["formation_id"] for x in state["retained_research_formations"]} == {"ATTRACTION_SCAN_015-F1"}
