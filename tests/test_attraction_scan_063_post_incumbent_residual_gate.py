import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_063.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

def test_scan063_requires_post_incumbent_residual_evidence():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_063"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_active_formation_as_seed"] is False
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert len(scan["examined_formations"]) == 6
    assert "PERSISTENT_WORKAROUND_AFTER_ACTIVE_OR_PAID_INCUMBENT_ADOPTION_OR_FAILED_SOFTWARE_ATTEMPT" in scan["search_mode"]

def test_scan063_is_formation_diverse():
    scan = load(SCAN)
    titles = {x["title"] for x in scan["examined_formations"]}
    assert titles == {
        "SALESFORCE_OUTLOOK_ACTIVITY_CAPTURE_RESIDUAL_WORKAROUND",
        "JIRA_ADVANCED_PLANS_PORTFOLIO_CAPACITY_SHADOW_EXCEL",
        "WORKDAY_FINANCIALS_EXCEL_REPORTING_RESIDUAL",
        "SERVICENOW_ROLE_AWARE_GUIDANCE_MAINTENANCE",
        "EPIC_COGITO_ADHOC_SQL_TO_EXCEL_ANALYST_WORKAROUND",
        "OPERA_CLOUD_FRONT_DESK_CHECKIN_MANUAL_DEFERRAL",
    }

def test_scan063_checks_active_absorption_not_static_incumbents_only():
    scan = load(SCAN)
    verdicts = {x["formation_id"]: x["verdict"] for x in scan["examined_formations"]}
    assert "ACTIVE_NATIVE_ARCHITECTURE_MIGRATION" in verdicts["ATTRACTION_SCAN_063-F1"]
    assert "NATIVE_JIRA_PLANS" in verdicts["ATTRACTION_SCAN_063-F2"]
    assert "OFFICIAL_OFFICECONNECT" in verdicts["ATTRACTION_SCAN_063-F3"]
    assert "DYNAMIC_GUIDANCE" in verdicts["ATTRACTION_SCAN_063-F4"]
    assert "COGITO_SELF_SERVICE" in verdicts["ATTRACTION_SCAN_063-F5"]
    assert "NATIVE_PREREGISTRATION" in verdicts["ATTRACTION_SCAN_063-F6"]

def test_scan064_escalates_to_parallel_double_spend():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_064"
    boundary = scan["next_search_boundary"]
    assert "ACTIVE_OR_PAID_INCUMBENT_PLUS_SEPARATE_RECURRING_EXTERNAL_WORKAROUND_SPEND" in boundary
    assert "FORMATION_DIVERSE" in boundary
    assert "EXACT_INCUMBENT_AND_ROADMAP_PREFLIGHT" in boundary
    assert "NO_SCAN061_TO_SCAN063_VERTICAL_INHERITANCE" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert "FAIL_CLOSED_PROMOTION" in boundary

def test_state_advances_after_scan063():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_063"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_064"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert {x["formation_id"] for x in state["retained_research_formations"]} == {"ATTRACTION_SCAN_015-F1"}
