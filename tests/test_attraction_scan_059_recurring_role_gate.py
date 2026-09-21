import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_059.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

def test_scan059_is_second_broad_pass_with_strong_recurring_spend():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_059"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert len(scan["examined_formations"]) == 6
    assert all(x["verdict"].startswith("DEMOTED_") for x in scan["examined_formations"])
    assert all(("6_PLUS_MONTH" in x["evidence_class"] or "CONTRACT_TO_HIRE" in x["evidence_class"]) for x in scan["examined_formations"])

def test_scan059_is_formation_diverse_and_does_not_reuse_scan058_verticals():
    scan = load(SCAN)
    titles = {x["title"] for x in scan["examined_formations"]}
    assert titles == {
        "RECURRING_QUICKBOOKS_MONTH_END_CLOSE_AND_RECONCILIATION",
        "HIGH_VOLUME_RECRUITING_COORDINATION_AND_FIRST_ROUND_SCREENING",
        "ONGOING_MEDICAL_BILLING_CLAIMS_AND_PAYER_FOLLOW_UP",
        "AFFILIATE_AND_CREATOR_PARTNER_RECRUITMENT_MANAGEMENT",
        "WARM_LEAD_OUTBOUND_APPOINTMENT_SETTING",
        "MULTI_BRAND_KLAVIYO_EMAIL_MARKETING_OWNERSHIP",
    }
    forbidden = ("COI", "RFP", "CATALOG", "RENT_MANAGER", "EXPORT", "SOC2")
    assert all(not any(term in title for term in forbidden) for title in titles)

def test_scan059_closures_separate_native_machine_layer_from_human_residual():
    scan = load(SCAN)
    verdicts = {x["formation_id"]: x["verdict"] for x in scan["examined_formations"]}
    assert "ACCOUNTING_AI" in verdicts["ATTRACTION_SCAN_059-F1"]
    assert "AI_RECRUITING_AUTOMATION" in verdicts["ATTRACTION_SCAN_059-F2"]
    assert "RCM_AUTOMATION" in verdicts["ATTRACTION_SCAN_059-F3"]
    assert "PARTNERSHIP_DISCOVERY_AUTOMATION" in verdicts["ATTRACTION_SCAN_059-F4"]
    assert "OUTBOUND_VOICE_AI" in verdicts["ATTRACTION_SCAN_059-F5"]
    assert "EMAIL_MARKETING_AI" in verdicts["ATTRACTION_SCAN_059-F6"]

def test_scan060_changes_evidence_source_instead_of_deriving_new_mechanism():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_060"
    boundary = scan["next_search_boundary"]
    assert "NON_ROLE_BUYING_SIGNALS" in boundary
    assert "REPEAT_PURCHASE_OR_PRODUCTIZED_SERVICE_SPEND" in boundary
    assert "NO_JOB_POSTING_AS_SOLE_PAYER_EVIDENCE" in boundary
    assert "NO_SCAN058_OR_SCAN059_VERTICAL_INHERITANCE" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert "FAIL_CLOSED_PROMOTION" in boundary

def test_state_advances_after_scan059():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_059"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_060"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert {x["formation_id"] for x in state["retained_research_formations"]} == {"ATTRACTION_SCAN_015-F1"}
