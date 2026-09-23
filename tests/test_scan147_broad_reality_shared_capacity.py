import json
from pathlib import Path
from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, AttractionEvidence, attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors

ROOT=Path(__file__).resolve().parents[1]
SCAN_PATH=ROOT/"data"/"research_runs"/"attraction_scan_147.json"
STATE_PATH=ROOT/"data"/"commercial_reset_state.json"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def profile(scan,row):
 raw=row["attraction_profile"]; reg=scan["source_registry"]
 def ev(k): return tuple(AttractionEvidence(source_id=r,claim=reg[r]["claim"]) for r in raw["evidence"][k])
 s=raw["scores"];f=raw["flags"]
 return AttractionDiscoveryProfile(signal_id=row["formation_id"],reality_pattern=row["evidence_summary"],a_actor=row["title"].split(" -> ")[0],b_actor=row["title"].split(" -> ")[1],candidate_bridge=row["title"],**s,
 a_motion_evidence=ev("a_voluntary_motion"),b_motion_evidence=ev("b_voluntary_motion"),value_jump_evidence=ev("state_dependent_value_jump"),decision_window_evidence=ev("decision_window"),bridge_compression_evidence=ev("bridge_compression"),activation_evidence=ev("activation_ease"),self_propulsion_evidence=ev("self_propulsion"),operator_control_evidence=ev("operator_control"),a_discoverability_evidence=ev("a_discoverability"),b_discoverability_evidence=ev("b_discoverability"),match_resolvability_evidence=ev("match_resolvability"),action_gate_evidence=ev("action_gate_callability"),a_population_replenishment_evidence=ev("a_population_replenishment"),b_population_replenishment_evidence=ev("b_population_replenishment"),recurring_connection_pressure_evidence=ev("recurring_connection_pressure"),recurring_missing_edge_evidence=ev("recurring_missing_edge"),recurring_event_source_evidence=ev("recurring_event_source"),**f)
def test_scan147_guard_and_low_attraction():
 scan=load(SCAN_PATH);assert strategic_drift_errors(scan)==[]
 assert all(attraction_beacon_state(profile(scan,r)) is AttractionBeaconState.LOW_ATTRACTION for r in scan["examined_formations"])
 assert scan["high_attraction_beacons"]==[] and scan["retained_research_formations"]==[]
def test_machine_state_scan147():
 st=load(STATE_PATH);assert st["last_completed_scan_id"]=="ATTRACTION_SCAN_147";assert st["last_completed_scan_file"]=="data/research_runs/attraction_scan_147.json";assert st["next_scan_id"]=="ATTRACTION_SCAN_148"
 resolved={x["formation_id"]:x["verdict"] for x in st["resolved_research_formations"]}
 for suffix in ("F1","F2","F3","F4","F5"): assert resolved[f"ATTRACTION_SCAN_147-{suffix}"].startswith("DEMOTED_")
 assert st["active_commercial_candidates"]==[] and st["active_transaction_units"]==[] and st["first_external_value_flow"]=="NOT_PROVEN"
