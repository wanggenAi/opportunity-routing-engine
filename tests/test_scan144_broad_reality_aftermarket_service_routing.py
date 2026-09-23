import json
from pathlib import Path

from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, AttractionEvidence, attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors

ROOT = Path(__file__).resolve().parents[1]
SCAN_PATH = ROOT / "data" / "research_runs" / "attraction_scan_144.json"
STATE_PATH = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def build_profile(scan, formation):
    raw = formation["attraction_profile"]
    registry = scan["source_registry"]
    def evs(score_name):
        return tuple(AttractionEvidence(source_id=ref, claim=registry[ref]["claim"]) for ref in raw["evidence"][score_name])
    scores = raw["scores"]
    flags = raw["flags"]
    kwargs = dict(
        signal_id=formation["formation_id"],
        reality_pattern=formation["evidence_summary"],
        a_actor=formation["title"].split(" -> ")[0],
        b_actor=formation["title"].split(" -> ")[1],
        candidate_bridge=formation["title"],
        **scores,
        a_motion_evidence=evs("a_voluntary_motion"),
        b_motion_evidence=evs("b_voluntary_motion"),
        value_jump_evidence=evs("state_dependent_value_jump"),
        decision_window_evidence=evs("decision_window"),
        bridge_compression_evidence=evs("bridge_compression"),
        activation_evidence=evs("activation_ease"),
        self_propulsion_evidence=evs("self_propulsion"),
        operator_control_evidence=evs("operator_control"),
        a_discoverability_evidence=evs("a_discoverability"),
        b_discoverability_evidence=evs("b_discoverability"),
        match_resolvability_evidence=evs("match_resolvability"),
        action_gate_evidence=evs("action_gate_callability"),
        a_population_replenishment_evidence=evs("a_population_replenishment"),
        b_population_replenishment_evidence=evs("b_population_replenishment"),
        recurring_connection_pressure_evidence=evs("recurring_connection_pressure"),
        recurring_missing_edge_evidence=evs("recurring_missing_edge"),
        recurring_event_source_evidence=evs("recurring_event_source"),
        **flags,
    )
    return AttractionDiscoveryProfile(**kwargs)

def test_scan144_passes_strategic_drift_guard():
    scan = load(SCAN_PATH)
    assert scan["scan_id"] == "ATTRACTION_SCAN_144"
    assert strategic_drift_errors(scan) == []
    assert scan["drift_audit"]["scan143_factory_inspection_subproblem_not_used_as_prior"] is True
    assert scan["drift_audit"]["one_marketplace_not_treated_as_population_prevalence"] is True

def test_only_overseas_industrial_aftermarket_field_is_high_attraction():
    scan = load(SCAN_PATH)
    by_id = {row["formation_id"]: row for row in scan["examined_formations"]}
    states = {fid: attraction_beacon_state(build_profile(scan, row)) for fid, row in by_id.items()}
    assert states["ATTRACTION_SCAN_144-F1"] is AttractionBeaconState.HIGH_ATTRACTION_BEACON
    for suffix in ("F2", "F3", "F4", "F5"):
        assert states[f"ATTRACTION_SCAN_144-{suffix}"] is AttractionBeaconState.LOW_ATTRACTION
    assert [row["formation_id"] for row in scan["high_attraction_beacons"]] == ["ATTRACTION_SCAN_144-F1"]

def test_f1_is_regenerative_field_not_transaction_seed():
    scan = load(SCAN_PATH)
    f1 = scan["examined_formations"][0]
    assert f1["seed_kind"] == "BROAD_REALITY_PATTERN"
    assert f1["attraction_profile"]["flags"]["explicit_transaction_seeded"] is False
    gate = f1["regenerative_field_gate"]
    for key in ("actor_a_replenishment","actor_b_replenishment","recurring_connection_pressure","recurring_missing_edge","recurring_event_source"):
        assert gate[key]["state"] == "EVIDENCED"
        assert gate[key]["evidence_refs"]
    assert "MACHINERY-EXPORT-CCCME-20260616" in gate["independent_field_evidence_refs"]
    assert "AUTOMATE-AMERICA-FIELD-SERVICE-202609" in gate["independent_field_evidence_refs"]

def test_machine_state_advances_to_scan144_without_commercial_promotion():
    state = load(STATE_PATH)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_144"
    assert state["last_completed_scan_file"] == "data/research_runs/attraction_scan_144.json"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_145"
    assert "ATTRACTION_SCAN_144-F1" in state["retained_research_formations"]
    resolved = {row["formation_id"]: row["verdict"] for row in state["resolved_research_formations"]}
    assert resolved["ATTRACTION_SCAN_144-F1"].startswith("DEMOTED_EXACT_INCUMBENT_PREFLIGHT_")
    for suffix in ("F2", "F3", "F4", "F5"):
        assert resolved[f"ATTRACTION_SCAN_144-{suffix}"].startswith("DEMOTED_")
    assert state["active_commercial_candidates"] == []
    assert state["active_transaction_units"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
