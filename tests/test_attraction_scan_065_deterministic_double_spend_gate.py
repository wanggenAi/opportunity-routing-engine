import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_065.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan065_requires_deterministic_machine_verifiable_double_spend():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_065"
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert len(scan["examined_formations"]) == 6
    assert "DETERMINISTIC_REPEATABLE_EXECUTION" in scan["search_mode"]
    assert "OBJECTIVE_MACHINE_VERIFIABLE_OUTPUT" in scan["search_mode"]


def test_scan065_closes_on_native_or_mature_productized_control_surfaces():
    scan = load(SCAN)
    verdicts = {x["formation_id"]: x["verdict"] for x in scan["examined_formations"]}
    assert "NATIVE_AND_MATURE_THIRD_PARTY_REPRICER_CATEGORY" in verdicts["ATTRACTION_SCAN_065-F1"]
    assert "NATIVE_DUPLICATE_RULES" in verdicts["ATTRACTION_SCAN_065-F2"]
    assert "DENSE_APP_MARKET" in verdicts["ATTRACTION_SCAN_065-F3"]
    assert "NATIVE_SMART_DISPUTES" in verdicts["ATTRACTION_SCAN_065-F4"]
    assert "NATIVE_MICROSOFT_365_BACKUP" in verdicts["ATTRACTION_SCAN_065-F5"]
    assert "NATIVE_RECEIPT_CAPTURE" in verdicts["ATTRACTION_SCAN_065-F6"]


def test_scan066_requires_pre_category_productization_buyer_evidence():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_066"
    boundary = scan["next_search_boundary"]
    assert "AT_LEAST_TWO_INDEPENDENT_BUYER_SIGNALS" in boundary
    assert "NOT_ALREADY_A_NAMED_MATURE_APP_SAAS_OR_MANAGED_SERVICE_CATEGORY" in boundary
    assert "EXACT_NATIVE_MARKETPLACE_AND_ROADMAP_PREFLIGHT" in boundary
    assert "FAIL_CLOSED_PROMOTION" in boundary


def test_state_advances_after_scan065():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_065"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_066"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert {x["formation_id"] for x in state["retained_research_formations"]} == {"ATTRACTION_SCAN_015-F1"}
