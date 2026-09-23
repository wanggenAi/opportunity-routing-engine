import json
from pathlib import Path

from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, AttractionEvidence, attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors

ROOT = Path(__file__).resolve().parents[1]
SCAN_PATH = ROOT / "data" / "research_runs" / "attraction_scan_146.json"
STATE_PATH = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def build_profile(scan, formation):
    raw=formation["attraction_profile"]; registry=scan["source_registry"]
    def evs(k):
        return tuple(AttractionEvidence(source_id=r, claim=registry[r]["claim"]) for r in raw["evidence"][k])
    s=raw["scores"]; f=raw["flags"]
    return AttractionDiscoveryProfile(
        signal_id=formation["formation_id"], reality_pattern=formation["evidence_summary"],
        a_actor=formation["title"].split(" -> ")[0], b_actor=formation["title"].split(" -> ")[1],
        candidate_bridge=formation["title"], **s,
        a_motion_evidence=evs("a_voluntary_motion"), b_motion_evidence=evs("b_voluntary_motion"),
        value_jump_evidence=evs("state_dependent_value_jump"), decision_window_evidence=evs("decision_window"),
        bridge_compression_evidence=evs("bridge_compression"), activation_evidence=evs("activation_ease"),
        self_propulsion_evidence=evs("self_propulsion"), operator_control_evidence=evs("operator_control"),
        a_discoverability_evidence=evs("a_discoverability"), b_discoverability_evidence=evs("b_discoverability"),
        match_resolvability_evidence=evs("match_resolvability"), action_gate_evidence=evs("action_gate_callability"),
        a_population_replenishment_evidence=evs("a_population_replenishment"), b_population_replenishment_evidence=evs("b_population_replenishment"),
        recurring_connection_pressure_evidence=evs("recurring_connection_pressure"), recurring_missing_edge_evidence=evs("recurring_missing_edge"),
        recurring_event_source_evidence=evs("recurring_event_source"), **f
    )

def test_scan146_passes_strategic_drift_guard():
    scan=load(SCAN_PATH)
    assert scan["scan_id"]=="ATTRACTION_SCAN_146"
    assert strategic_drift_errors(scan)==[]
    assert scan["drift_audit"]["scan145_current_service_fields_not_used_as_prior"] is True
    assert scan["drift_audit"]["incumbent_presence_evaluated_before_retention"] is True

def test_scan146_has_no_high_attraction_beacon():
    scan=load(SCAN_PATH)
    states={row["formation_id"]:attraction_beacon_state(build_profile(scan,row)) for row in scan["examined_formations"]}
    assert all(state is AttractionBeaconState.LOW_ATTRACTION for state in states.values())
    assert scan["high_attraction_beacons"]==[]
    assert scan["retained_research_formations"]==[]
    assert scan["zero_primary_admissions"] is True

def test_machine_state_closes_all_scan146_formations_without_promotion():
    state=load(STATE_PATH)
    assert state["last_completed_scan_id"]=="ATTRACTION_SCAN_146"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_147"
    resolved={row["formation_id"]:row["verdict"] for row in state["resolved_research_formations"]}
    for suffix in ("F1","F2","F3","F4","F5"):
        assert resolved[f"ATTRACTION_SCAN_146-{suffix}"].startswith("DEMOTED_")
    assert state["active_commercial_candidates"]==[]
    assert state["active_transaction_units"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"
