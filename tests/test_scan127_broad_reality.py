import json
from pathlib import Path

from src.jev_research_advisory import build_research_states
from tools.run_jev_research_advisory import resolve_scan_path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_127.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan127_broad_reality_evidence.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan127_is_current_canonical_auto_jev_input():
    state = load(STATE)
    path = resolve_scan_path("auto", state, research_dir=ROOT / "data" / "research_runs")
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_127"
    assert path == SCAN


def test_scan127_is_formation_diverse_and_does_not_recycle_scan126():
    scan = load(SCAN)
    titles = [row["title"] for row in scan["examined_formations"]]
    assert scan["status"] == "COMPLETE"
    assert len(titles) == 4
    assert scan["inherited_active_formation_as_seed"] is False
    assert scan["inherited_mechanism_as_requirement"] is False
    assert scan["drift_audit"]["inherited_scan124_or_125_primary_signal"] is False
    assert scan["drift_audit"]["inherited_scan126_ground_truth_execution_mechanism"] is False
    joined = " ".join(titles)
    assert "GROUND_TRUTH_EXECUTION" not in joined
    assert "CHINA_HELPER" not in joined


def test_scan127_fails_closed_with_no_retained_or_promoted_formation():
    scan = load(SCAN)
    state = load(STATE)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert state["active_commercial_candidates"] == []
    assert state["retained_research_formations"] == []
    assert all(row["verdict"].startswith("DEMOTED_") for row in scan["examined_formations"])


def test_scan127_exposes_four_authoritatively_closed_entities_to_jev():
    scan = load(SCAN)
    state = load(STATE)
    states = build_research_states(scan=scan, commercial_state=state, max_entities=8)
    assert len(states) == 4
    ids = {row["formation"]["formation_id"] for row in states}
    assert ids == {
        "ATTRACTION_SCAN_127-F1",
        "ATTRACTION_SCAN_127-F2",
        "ATTRACTION_SCAN_127-F3",
        "ATTRACTION_SCAN_127-F4",
    }
    assert all(
        row["authoritative_engine_context"]["existing_closure_authoritative"]
        for row in states
    )


def test_every_scan127_formation_records_all_attraction_hard_gate_dimensions():
    scan = load(SCAN)
    required = {
        "a_side",
        "a_side_evidence",
        "b_side",
        "b_side_evidence",
        "operator",
        "operator_non_labor_test",
        "connection_wow",
        "activation_friction",
        "self_propulsion",
        "a_discoverability",
        "b_discoverability",
        "match_resolvability",
        "action_gate",
        "router_distinctiveness",
        "generic_agent_substitution",
    }
    for row in scan["examined_formations"]:
        assert required <= set(row["attraction_brief"])


def test_scan127_evidence_pack_maps_four_fresh_packets_and_zero_retention():
    evidence = load(EVIDENCE)
    scan = load(SCAN)
    assert evidence["scan_id"] == scan["scan_id"]
    assert len(evidence["evidence_packets"]) == 4
    assert evidence["scan_conclusion"].endswith("ZERO_RETAINED_NO_COMMERCIAL_PROMOTION")
    assert evidence["next_scan_id"] == "ATTRACTION_SCAN_128"
