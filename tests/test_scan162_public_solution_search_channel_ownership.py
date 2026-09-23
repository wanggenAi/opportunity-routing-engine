import json
import unittest
from pathlib import Path
from src.attraction_discovery import AttractionBeaconState,AttractionDiscoveryProfile,AttractionEvidence,attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors

ROOT=Path(__file__).resolve().parents[1]
SCAN_PATH=ROOT/"data"/"research_runs"/"attraction_scan_162.json"
STATE_PATH=ROOT/"data"/"commercial_reset_state.json"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def build_profile(scan,row):
 raw=row["attraction_profile"]; reg=scan["source_registry"]
 def ev(k): return tuple(AttractionEvidence(source_id=r,claim=reg[r]["claim"]) for r in raw["evidence"][k])
 left,right=row["title"].split(" -> ",1)
 return AttractionDiscoveryProfile(signal_id=row["formation_id"],reality_pattern=row["evidence_summary"],a_actor=left,b_actor=right,candidate_bridge=row["title"],**raw["scores"],
  a_motion_evidence=ev("a_voluntary_motion"),b_motion_evidence=ev("b_voluntary_motion"),value_jump_evidence=ev("state_dependent_value_jump"),decision_window_evidence=ev("decision_window"),bridge_compression_evidence=ev("bridge_compression"),activation_evidence=ev("activation_ease"),self_propulsion_evidence=ev("self_propulsion"),operator_control_evidence=ev("operator_control"),a_discoverability_evidence=ev("a_discoverability"),b_discoverability_evidence=ev("b_discoverability"),match_resolvability_evidence=ev("match_resolvability"),action_gate_evidence=ev("action_gate_callability"),a_population_replenishment_evidence=ev("a_population_replenishment"),b_population_replenishment_evidence=ev("b_population_replenishment"),recurring_connection_pressure_evidence=ev("recurring_connection_pressure"),recurring_missing_edge_evidence=ev("recurring_missing_edge"),recurring_event_source_evidence=ev("recurring_event_source"),**raw["flags"])
class Scan162Tests(unittest.TestCase):
 def test_guard_and_all_examined_formations_are_low(self):
  scan=load(SCAN_PATH); self.assertEqual(strategic_drift_errors(scan),[])
  for row in scan["examined_formations"]: self.assertIs(attraction_beacon_state(build_profile(scan,row)),AttractionBeaconState.LOW_ATTRACTION)
  self.assertEqual(scan["high_attraction_beacons"],[]); self.assertEqual(scan["retained_research_formations"],[])
 def test_publication_channel_ownership_is_preserved(self):
  scan=load(SCAN_PATH)
  for fid in ("ATTRACTION_SCAN_162-F1","ATTRACTION_SCAN_162-F2","ATTRACTION_SCAN_162-F4","ATTRACTION_SCAN_162-F5"):
   row={x["formation_id"]:x for x in scan["examined_formations"]}[fid]
   self.assertEqual(row["attraction_profile"]["scores"]["operator_control"],1)
   self.assertEqual(row["attraction_profile"]["scores"]["recurring_missing_edge"],1)
  self.assertTrue(scan["drift_audit"]["publication_channel_matchmaking_owner_checked"])
 def test_department_followup_is_not_unowned(self):
  scan=load(SCAN_PATH); row={x["formation_id"]:x for x in scan["examined_formations"]}["ATTRACTION_SCAN_162-F3"]
  self.assertEqual(row["state_change_gate"]["decisive_action_gate"]["owner_state"],"GOVERNMENT_LONG_TERM_COORDINATION_MECHANISM_OWNED")
 def test_machine_state_finalizes_scan161(self):
  state=load(STATE_PATH); prior=state["scan161_expansion_modular_operations"]
  self.assertEqual(prior["status"],"MERGED_FINAL_EXACT_HEAD_GREEN_ALL_ROUTES_CLOSED")
  self.assertEqual(prior["final_exact_head_sha"],"f8da3db448b36035fd42e18296f1f2348912b53f")
  self.assertEqual(prior["final_repository_ci_run_id"],35893628264); self.assertEqual(prior["final_repository_ci_test_count"],822)
  self.assertEqual(prior["final_jev_run_id"],35893628276); self.assertEqual(prior["final_jev_artifact_id"],10765264893)
  self.assertEqual(prior["merged_pr"],476); self.assertEqual(prior["merged_main_sha"],"682a65733877c3a51ed2e815aac24288a3b5dd9c")
  self.assertGreaterEqual(int(state["last_completed_scan_id"].rsplit("_",1)[1]),162); self.assertGreaterEqual(int(state["next_scan_id"].rsplit("_",1)[1]),163)
 def test_no_commercial_promotion(self):
  state=load(STATE_PATH); self.assertEqual(state["active_commercial_candidates"],[]); self.assertEqual(state["active_transaction_units"],[]); self.assertEqual(state["first_external_value_flow"],"NOT_PROVEN")
  current=state["scan162_public_solution_search_channel_ownership"]; self.assertFalse(current["commercial_promotion"]); self.assertFalse(current["external_side_effects_performed"])
if __name__=="__main__": unittest.main()
