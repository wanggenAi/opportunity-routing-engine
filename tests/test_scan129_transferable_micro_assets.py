import json
from pathlib import Path

from src.jev_research_advisory import build_research_states
from tools.run_jev_research_advisory import resolve_scan_path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_129.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan129_transferable_micro_assets_evidence.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan129_is_current_auto_jev_input_with_one_open_retained_formation():
    state = load(STATE)
    path = resolve_scan_path("auto", state, research_dir=ROOT / "data" / "research_runs")
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_129"
    assert path == SCAN
    scan = load(SCAN)
    states = build_research_states(scan=scan, commercial_state=state, max_entities=8)
    assert len(states) == 4
    by_id = {row["formation"]["formation_id"]: row for row in states}
    assert by_id["ATTRACTION_SCAN_129-F1"]["authoritative_engine_context"]["existing_closure_authoritative"] is False
    assert by_id["ATTRACTION_SCAN_129-F1"]["authoritative_engine_context"]["already_retained_for_research"] is True
    assert all(
        by_id[f"ATTRACTION_SCAN_129-F{i}"]["authoritative_engine_context"]["existing_closure_authoritative"]
        for i in (2, 3, 4)
    )

def test_scan129_retains_only_f1_and_never_promotes_it():
    scan = load(SCAN)
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == ["ATTRACTION_SCAN_129-F1"]
    assert scan["high_attraction_beacons"] == ["ATTRACTION_SCAN_129-F1"]
    assert scan["examined_formations"][0]["verdict"].startswith("RETAINED_RESEARCH_ONLY_")
    assert all(
        row["verdict"].startswith("DEMOTED_")
        for row in scan["examined_formations"][1:]
    )
    assert scan["first_external_value_flow"] == "NOT_PROVEN"

def test_scan129_f1_requires_transaction_diligence_and_compliant_payment():
    scan = load(SCAN)
    f1 = scan["examined_formations"][0]
    required = {
        "SELLER_PROVIDED_LAST_90_DAY_ORDER_COUNT_GROSS_REVENUE_REFUNDS_AND_SETTLEMENT_EVIDENCE",
        "TRAFFIC_SOURCE_BREAKDOWN_AND_DIRECT_ORGANIC_SHARE",
        "SELLER_RECURRING_WEEKLY_OPERATING_HOURS_AND_MANUAL_DISTRIBUTOR_DEPENDENCE",
        "DOMAIN_CODE_DATABASE_PROMPTS_CONTENT_AND_CUSTOMER_DATA_TRANSFER_SCOPE_AND_IP_RIGHTS",
        "HOSTING_LLM_PAYMENT_AND_OTHER_MONTHLY_COSTS",
        "COMPLIANT_NON_CRYPTO_PAYMENT_PATH_FOR_A_CHINA_OPERATOR",
    }
    assert required == set(f1["decisive_unknowns"])
    assert f1["attraction_brief"]["legal_payment_compliance"].startswith("FAIL_")
    assert "NO_PURCHASE" in f1["verdict"]

def test_scan129_evidence_pack_matches_machine_truth():
    state = load(STATE)
    evidence = load(EVIDENCE)
    assert evidence["scan_id"] == "ATTRACTION_SCAN_129"
    assert len(evidence["evidence_packets"]) == 4
    assert evidence["retained_research_formation"] == "ATTRACTION_SCAN_129-F1"
    assert evidence["scan_conclusion"].endswith("ZERO_COMMERCIAL_PROMOTION")
    assert state["retained_research_formations"] == ["ATTRACTION_SCAN_129-F1"]
    assert state["active_commercial_candidates"] == []
    assert state["next_scan_id"] == "ATTRACTION_SCAN_130"
