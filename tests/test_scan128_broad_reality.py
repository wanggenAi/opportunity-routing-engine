import json
from pathlib import Path

from src.jev_research_advisory import build_research_states
from tools.run_jev_research_advisory import resolve_scan_path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_128.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan128_broad_reality_evidence.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan128_auto_resolution_and_entity_count():
    state = load(STATE)
    path = resolve_scan_path("auto", state, research_dir=ROOT / "data" / "research_runs")
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_128"
    assert path == SCAN
    scan = load(SCAN)
    states = build_research_states(scan=scan, commercial_state=state, max_entities=8)
    assert len(states) == 4
    assert {row["formation"]["formation_id"] for row in states} == {
        "ATTRACTION_SCAN_128-F1", "ATTRACTION_SCAN_128-F2",
        "ATTRACTION_SCAN_128-F3", "ATTRACTION_SCAN_128-F4",
    }
    assert all(row["authoritative_engine_context"]["existing_closure_authoritative"] for row in states)

def test_scan128_is_fresh_formation_diverse_and_fail_closed():
    scan = load(SCAN)
    assert scan["status"] == "COMPLETE"
    assert len(scan["examined_formations"]) == 4
    assert scan["inherited_active_formation_as_seed"] is False
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["drift_audit"]["inherited_scan124_or_125_primary_signal"] is False
    assert scan["drift_audit"]["inherited_scan126_ground_truth_execution_mechanism"] is False
    assert scan["drift_audit"]["inherited_scan127_regulatory_enterprise_infrastructure_formation"] is False
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert all(row["verdict"].startswith("DEMOTED_") for row in scan["examined_formations"])

def test_scan128_hard_gate_schema_and_evidence_pack():
    scan = load(SCAN)
    required = {"a_side","a_side_evidence","b_side","b_side_evidence","operator",
                "operator_non_labor_test","connection_wow","activation_friction",
                "self_propulsion","a_discoverability","b_discoverability",
                "match_resolvability","action_gate","router_distinctiveness",
                "generic_agent_substitution"}
    assert all(required <= set(row["attraction_brief"]) for row in scan["examined_formations"])
    evidence = load(EVIDENCE)
    assert evidence["scan_id"] == "ATTRACTION_SCAN_128"
    assert len(evidence["evidence_packets"]) == 4
    assert evidence["scan_conclusion"].endswith("ZERO_RETAINED_NO_COMMERCIAL_PROMOTION")
    assert evidence["next_scan_id"] == "ATTRACTION_SCAN_129"
