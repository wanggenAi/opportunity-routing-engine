import json
from pathlib import Path
from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, AttractionEvidence, attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors
from src.jev_research_advisory import build_research_states

ROOT=Path(__file__).resolve().parents[1]
SCAN_PATH=ROOT/"data"/"research_runs"/"attraction_scan_148.json"
STATE_PATH=ROOT/"data"/"commercial_reset_state.json"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def profile(scan,row):
 raw=row["attraction_profile"]; reg=scan["source_registry"]
 def ev(k): return tuple(AttractionEvidence(source_id=r,claim=reg[r]["claim"]) for r in raw["evidence"][k])
 s=raw["scores"]; f=raw["flags"]
 return AttractionDiscoveryProfile(signal_id=row["formation_id"],reality_pattern=row["evidence_summary"],a_actor=row["title"].split(" -> ")[0],b_actor=row["title"].split(" -> ")[1],candidate_bridge=row["title"],**s,
 a_motion_evidence=ev("a_voluntary_motion"),b_motion_evidence=ev("b_voluntary_motion"),value_jump_evidence=ev("state_dependent_value_jump"),decision_window_evidence=ev("decision_window"),bridge_compression_evidence=ev("bridge_compression"),activation_evidence=ev("activation_ease"),self_propulsion_evidence=ev("self_propulsion"),operator_control_evidence=ev("operator_control"),a_discoverability_evidence=ev("a_discoverability"),b_discoverability_evidence=ev("b_discoverability"),match_resolvability_evidence=ev("match_resolvability"),action_gate_evidence=ev("action_gate_callability"),a_population_replenishment_evidence=ev("a_population_replenishment"),b_population_replenishment_evidence=ev("b_population_replenishment"),recurring_connection_pressure_evidence=ev("recurring_connection_pressure"),recurring_missing_edge_evidence=ev("recurring_missing_edge"),recurring_event_source_evidence=ev("recurring_event_source"),**f)
def test_scan148_guard_and_comparison_profiles():
 scan=load(SCAN_PATH); assert strategic_drift_errors(scan)==[]
 states={r["formation_id"]:attraction_beacon_state(profile(scan,r)) for r in scan["examined_formations"]}
 assert states["ATTRACTION_SCAN_148-F1"] is AttractionBeaconState.HIGH_ATTRACTION_BEACON
 for suffix in ("F2","F3","F4","F5"): assert states[f"ATTRACTION_SCAN_148-{suffix}"] is AttractionBeaconState.LOW_ATTRACTION
 assert [r["formation_id"] for r in scan["high_attraction_beacons"]]==["ATTRACTION_SCAN_148-F1"]
 assert scan["retained_research_formations"]==["ATTRACTION_SCAN_148-F1"]
 assert scan["active_commercial_candidate_promotions"]==[] and scan["active_transaction_unit_promotions"]==[]
def test_scan148_boundary_does_not_reopen_scan143_or_scan144():
 scan=load(SCAN_PATH)
 assert scan["strategic_reboot"]["scan143_factory_inspection_not_inherited"] is True
 assert scan["strategic_reboot"]["scan144_aftermarket_service_not_inherited"] is True
 assert "non-specialist" in scan["comparison_profiles"]["validated_boundary"].lower()
def test_machine_state_scan148():
 st=load(STATE_PATH)
 assert st["last_completed_scan_id"]=="ATTRACTION_SCAN_148"
 assert st["last_completed_scan_file"]=="data/research_runs/attraction_scan_148.json"
 assert st["next_scan_id"]=="ATTRACTION_SCAN_149"
 assert "ATTRACTION_SCAN_148-F1" in st["retained_research_formations"]
 assert st["active_commercial_candidates"]==[] and st["active_transaction_units"]==[] and st["first_external_value_flow"]=="NOT_PROVEN"
 assert st["scan147_broad_reality_shared_capacity"]["exact_head_validation_status"]=="SUCCESS"
 assert st["scan147_broad_reality_shared_capacity"]["final_jev_next_action"]=="ADVANCE_TO_NEXT_SCAN"

def test_scan148_f1_route_consumption_is_authoritative_for_jev():
 scan=load(SCAN_PATH); st=load(STATE_PATH)
 states=build_research_states(scan=scan,commercial_state=st,max_entities=5)
 by_id={x["formation"]["formation_id"]:x for x in states}
 engine=by_id["ATTRACTION_SCAN_148-F1"]["authoritative_engine_context"]
 assert engine["existing_scan_verdict"]=="RETAINED_FOR_JEV_RESEARCH_ROUTING_AFTER_BROAD_REALITY_AND_COMPARISON_PROFILE_VALIDATION"
 assert engine["existing_verdict"].startswith("DEMOTED_AFTER_EXACT_INCUMBENT_PREFLIGHT_")
 assert engine["resolved_in_commercial_state"] is True
 assert engine["existing_closure_authoritative"] is True
