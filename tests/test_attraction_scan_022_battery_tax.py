import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_022.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan022_is_broad_and_fail_closed():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_022"
    assert scan["search_mode"] == "FORMATION_DIVERSE_BROAD_REALITY_NO_SCAN021_VERTICAL_INHERITANCE"
    assert scan["inherited_active_formation_as_seed"] is False
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["first_external_value_flow"] == "NOT_PROVEN"


def test_scan022_retains_only_battery_tax_reconciliation_as_research():
    scan = load(SCAN)
    assert scan["retained_research_formations"] == ["ATTRACTION_SCAN_022-F1"]
    f1 = scan["high_attraction_beacons"][0]
    assert f1["formation_id"] == "ATTRACTION_SCAN_022-F1"
    assert f1["mechanism_class"] == "MANDATORY_FINANCIAL_EVIDENCE_RECONCILIATION"
    assert f1["commercial_candidate"] is False
    assert "GENERIC_AGENT_OR_EXCEL_SUBSTITUTABILITY_AFTER_DATA_EXPORT" in f1["decisive_unknowns"]
    assert "EXACT_ERP_TAX_SOFTWARE_INCUMBENT_RESPONSE" in f1["decisive_unknowns"]


def test_scan022_does_not_promote_crowded_agent_security_or_cbam():
    scan = load(SCAN)
    verdicts = {item["title"]: item["verdict"] for item in scan["examined_formations"]}
    assert verdicts["GENERIC_AI_AGENT_SECURITY_TESTING_PLATFORM"] == "DEMOTED_HIGH_DEMAND_LOW_WHITE_SPACE"
    assert verdicts["CBAM_EVIDENCE_AND_VERIFICATION_WORKBENCH"] == "DEMOTED_CURRENT_INCUMBENT_CROWDING"


def test_state_advances_to_scan023_without_commercial_promotion():
    state = load(STATE)
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    assert retained == {
        "ATTRACTION_SCAN_015-F1",
        "ATTRACTION_SCAN_016-F1",
        "ATTRACTION_SCAN_022-F1",
    }
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_022"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_023"
