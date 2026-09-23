import json
import unittest
from pathlib import Path
from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, AttractionEvidence, attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors
ROOT=Path(__file__).resolve().parents[1]; SCAN_PATH=ROOT/"data"/"research_runs"/"attraction_scan_158.json"; STATE_PATH=ROOT/"data"/"commercial_reset_state.json"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def build_profile(scan,row):
 raw=row["attraction_profile"]; reg=scan["source_registry"]
 def ev(k): return tuple(AttractionEvidence(source_id=r,claim=reg[r]["claim"]) for r in raw["evidence"][k])
 left,right=row["title"].split(" -> ",1)
 return AttractionDiscoveryProfile(signal_id=row["formation_id"],reality_pattern=row["evidence_summary"],a_actor=left,b_actor=right,candidate_bridge=row["title"],**raw["scores"],a_motion_evidence=ev("a_voluntary_motion"),b_motion_evidence=ev("b_voluntary_motion"),value_jump_evidence=ev("state_dependent_value_jump"),decision_window_evidence=ev("decision_window"),bridge_compression_evidence=ev("bridge_compression"),activation_evidence=ev("activation_ease"),self_propulsion_evidence=ev("self_propulsion"),operator_control_evidence=ev("operator_control"),a_discoverability_evidence=ev("a_discoverability"),b_discoverability_evidence=ev("b_discoverability"),match_resolvability_evidence=ev("match_resolvability"),action_gate_evidence=ev("action_gate_callability"),a_population_replenishment_evidence=ev("a_population_replenishment"),b_population_replenishment_evidence=ev("b_population_replenishment"),recurring_connection_pressure_evidence=ev("recurring_connection_pressure"),recurring_missing_edge_evidence=ev("recurring_missing_edge"),recurring_event_source_evidence=ev("recurring_event_source"),**raw["flags"])
class Scan158OpenRemedyDiscoverabilityTests(unittest.TestCase):
 def test_all_profiles_close_and_guard_passes(self):
  scan=load(SCAN_PATH); self.assertEqual(strategic_drift_errors(scan),[])
  for row in scan["examined_formations"]: self.assertIs(attraction_beacon_state(build_profile(scan,row)),AttractionBeaconState.LOW_ATTRACTION)
  self.assertEqual(scan["high_attraction_beacons"],[]); self.assertEqual(scan["retained_research_formations"],[])
 def test_cyber_open_gate_is_preserved_but_not_promoted(self):
  scan=load(SCAN_PATH); row={x["formation_id"]:x for x in scan["examined_formations"]}["ATTRACTION_SCAN_158-F4"]
  self.assertEqual(row["state_change_gate"]["decisive_action_gate"]["owner_state"],"UNOWNED_OPEN")
  self.assertEqual(row["attraction_profile"]["scores"]["a_discoverability"],1)
  self.assertEqual(row["attraction_profile"]["scores"]["match_resolvability"],1)
  self.assertTrue(row["attraction_profile"]["flags"]["expert_matching_required_per_transaction"])
 def test_every_formation_records_state_change_gate(self):
  scan=load(SCAN_PATH)
  for row in scan["examined_formations"]:
   for k in ("event_trace","affected_actor_population","counterparty_population","decisive_action_gate"):
    self.assertEqual(row["state_change_gate"][k]["state"],"EVIDENCED"); self.assertTrue(row["state_change_gate"][k]["evidence_refs"])
 def test_machine_state_finalizes_scan157_and_advances(self):
  s=load(STATE_PATH); p=s["scan157_state_change_action_gate"]
  self.assertEqual(p["status"],"MERGED_FINAL_EXACT_HEAD_GREEN_ALL_ROUTES_CLOSED"); self.assertEqual(p["final_exact_head_sha"],"462ac408679bc6158f4daf409a9f1c92da004dab")
  self.assertEqual(p["final_repository_ci_run_id"],35887993492); self.assertEqual(p["final_repository_ci_test_count"],799); self.assertEqual(p["final_jev_run_id"],35887993544); self.assertEqual(p["final_jev_artifact_id"],10763431838)
  self.assertEqual(p["final_jev_effective_route_counts"],{"NO_FURTHER_RESEARCH":3}); self.assertEqual(p["merged_main_sha"],"828ee532ac999cabc5c22c0d1af6b1d0a205178f")
  self.assertGreaterEqual(int(s["last_completed_scan_id"].rsplit("_",1)[1]),158); self.assertGreaterEqual(int(s["next_scan_id"].rsplit("_",1)[1]),159)
 def test_all_five_resolved_without_commercial_promotion(self):
  s=load(STATE_PATH); resolved={x["formation_id"]:x["verdict"] for x in s["resolved_research_formations"]}
  for suffix in ("F1","F2","F3","F4","F5"): self.assertTrue(resolved[f"ATTRACTION_SCAN_158-{suffix}"].startswith("DEMOTED_"))
  self.assertEqual(s["active_commercial_candidates"],[]); self.assertEqual(s["active_transaction_units"],[]); self.assertEqual(s["first_external_value_flow"],"NOT_PROVEN")
if __name__=="__main__": unittest.main()
