import json
from pathlib import Path

from src.attraction_discovery import (
    AttractionBeaconState,
    AttractionDiscoveryProfile,
    AttractionEvidence,
    attraction_beacon_state,
)
from src.strategic_drift_guard import strategic_drift_errors

ROOT = Path(__file__).resolve().parents[1]
SCAN_PATH = ROOT / "data" / "research_runs" / "attraction_scan_142.json"
STATE_PATH = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_profile(scan, formation):
    raw = formation["attraction_profile"]
    registry = scan["source_registry"]

    def evs(score_name):
        refs = raw["evidence"][score_name]
        return tuple(AttractionEvidence(source_id=ref, claim=registry[ref]["claim"]) for ref in refs)

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
    if formation.get("generic_agent_substitution_evidence"):
        kwargs["generic_agent_substitution_evidence"] = tuple(
            AttractionEvidence(source_id=ref, claim=registry[ref]["claim"])
            for ref in formation["generic_agent_substitution_evidence"]
        )
    return AttractionDiscoveryProfile(**kwargs)


def test_scan142_passes_machine_strategic_drift_guard():
    scan = load(SCAN_PATH)
    assert scan["scan_id"] == "ATTRACTION_SCAN_142"
    assert strategic_drift_errors(scan) == []


def test_only_vpp_field_is_machine_high_attraction():
    scan = load(SCAN_PATH)
    by_id = {row["formation_id"]: row for row in scan["examined_formations"]}
    states = {fid: attraction_beacon_state(build_profile(scan, row)) for fid, row in by_id.items()}
    assert states["ATTRACTION_SCAN_142-F1"] is AttractionBeaconState.HIGH_ATTRACTION_BEACON
    assert states["ATTRACTION_SCAN_142-F2"] is AttractionBeaconState.LOW_ATTRACTION
    assert states["ATTRACTION_SCAN_142-F3"] is AttractionBeaconState.LOW_ATTRACTION
    assert states["ATTRACTION_SCAN_142-F4"] is AttractionBeaconState.LOW_ATTRACTION
    assert [row["formation_id"] for row in scan["high_attraction_beacons"]] == ["ATTRACTION_SCAN_142-F1"]


def test_vpp_beacon_is_a_regenerative_field_not_a_transaction_seed():
    scan = load(SCAN_PATH)
    f1 = scan["examined_formations"][0]
    assert f1["seed_kind"] == "BROAD_REALITY_PATTERN"
    gate = f1["regenerative_field_gate"]
    for key in (
        "actor_a_replenishment",
        "actor_b_replenishment",
        "recurring_connection_pressure",
        "recurring_missing_edge",
        "recurring_event_source",
    ):
        assert gate[key]["state"] == "EVIDENCED"
        assert gate[key]["evidence_refs"]
    assert gate["independent_field_evidence_refs"]


def test_machine_state_retains_only_scan142_f1_and_never_promotes():
    scan = load(SCAN_PATH)
    state = load(STATE_PATH)
    assert scan["retained_research_formations"] == ["ATTRACTION_SCAN_142-F1"]
    assert "ATTRACTION_SCAN_142-F1" in state["retained_research_formations"]
    resolved = {row["formation_id"]: row["verdict"] for row in state["resolved_research_formations"]}
    for suffix in ("F2", "F3", "F4"):
        assert resolved[f"ATTRACTION_SCAN_142-{suffix}"].startswith("DEMOTED_")
    assert state["active_commercial_candidates"] == []
    assert state["active_transaction_units"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_142"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_143"


def test_scan142_does_not_reactivate_quarantined_proxy_chain():
    state = load(STATE_PATH)
    resolved = {row["formation_id"]: row["verdict"] for row in state["resolved_research_formations"]}
    for formation_id in (
        "ATTRACTION_SCAN_135-F1",
        "ATTRACTION_SCAN_136-F1",
        "ATTRACTION_SCAN_136-F2",
        "ATTRACTION_SCAN_139-F1",
        "ATTRACTION_SCAN_140-F1",
        "ATTRACTION_SCAN_141-F1",
        "ATTRACTION_SCAN_141-F2",
    ):
        assert resolved[formation_id].startswith("CLOSED_STRATEGIC_QUARANTINE_")


def test_source_registry_is_current_and_evidence_bound():
    scan = load(SCAN_PATH)
    assert len(scan["source_registry"]) >= 10
    assert all(v["url"].startswith("https://") for v in scan["source_registry"].values())
    assert scan["drift_audit"]["scan141_asset_cashflow_proxy_not_used_as_prior"] is True
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["active_transaction_unit_promotions"] == []
