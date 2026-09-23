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

def test_scan129_is_current_auto_jev_input_and_all_formations_are_closed():
    state = load(STATE)
    path = resolve_scan_path("auto", state, research_dir=ROOT / "data" / "research_runs")
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_129"
    assert path == SCAN
    scan = load(SCAN)
    states = build_research_states(scan=scan, commercial_state=state, max_entities=8)
    assert len(states) == 4
    assert {row["formation"]["formation_id"] for row in states} == {
        "ATTRACTION_SCAN_129-F1", "ATTRACTION_SCAN_129-F2",
        "ATTRACTION_SCAN_129-F3", "ATTRACTION_SCAN_129-F4",
    }
    assert all(row["authoritative_engine_context"]["existing_closure_authoritative"] for row in states)

def test_scan129_retains_nothing_and_never_promotes():
    scan = load(SCAN)
    assert scan["status"] == "COMPLETE"
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []
    assert all(row["verdict"].startswith("DEMOTED_") for row in scan["examined_formations"])
    assert scan["first_external_value_flow"] == "NOT_PROVEN"

def test_scan129_f1_rejects_inferred_domain_and_fails_china_content_gate():
    scan = load(SCAN)
    f1 = scan["examined_formations"][0]
    assert f1["formation_id"] == "ATTRACTION_SCAN_129-F1"
    assert f1["verdict"] == (
        "DEMOTED_CURRENT_AI_TAROT_ASSET_FAILS_CHINA_CONTENT_COMPLIANCE_"
        "AND_LACKS_INDEPENDENT_PAID_FLOW_EVIDENCE"
    )
    assert f1["attraction_brief"]["b_discoverability"].startswith("FAIL_")
    assert f1["attraction_brief"]["regulatory_content_compliance"].startswith("FAIL_")
    assert any("website address" in item for item in f1["exact_disconfirmation"])
    assert any("shaibar.com" in item for item in f1["exact_disconfirmation"])
    assert scan["drift_audit"]["independent_live_asset_identity_required"] is True
    assert scan["drift_audit"]["inferred_domain_identity_rejected"] is True

def test_scan129_evidence_pack_matches_zero_retention_machine_truth():
    state = load(STATE)
    evidence = load(EVIDENCE)
    assert evidence["scan_id"] == "ATTRACTION_SCAN_129"
    assert len(evidence["evidence_packets"]) == 4
    assert "retained_research_formation" not in evidence
    assert evidence["scan_conclusion"].endswith("ZERO_RETAINED_ZERO_COMMERCIAL_PROMOTION")
    assert state["retained_research_formations"] == []
    assert state["active_commercial_candidates"] == []
    assert state["next_scan_id"] == "ATTRACTION_SCAN_130"
