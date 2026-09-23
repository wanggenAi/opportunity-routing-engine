import json,unittest
from pathlib import Path
from src.attraction_discovery import AttractionDiscoveryProfile,AttractionEvidence,AttractionBeaconState,attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors
ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_163.json"
def load(): return json.loads(SCAN.read_text())
def build(scan,row):
 raw=row["attraction_profile"]; reg=scan["source_registry"]
 def ev(k): return tuple(AttractionEvidence(source_id=x,claim=reg[x]["claim"]) for x in raw["evidence"][k])
 return AttractionDiscoveryProfile(signal_id=row["formation_id"],reality_pattern=row["evidence_summary"],a_actor="recurring overseas verification demand pumps",b_actor="China local field executors",candidate_bridge=row["title"],**raw["scores"],a_motion_evidence=ev("a_voluntary_motion"),b_motion_evidence=ev("b_voluntary_motion"),value_jump_evidence=ev("state_dependent_value_jump"),decision_window_evidence=ev("decision_window"),bridge_compression_evidence=ev("bridge_compression"),activation_evidence=ev("activation_ease"),self_propulsion_evidence=ev("self_propulsion"),operator_control_evidence=ev("operator_control"),a_discoverability_evidence=ev("a_discoverability"),b_discoverability_evidence=ev("b_discoverability"),match_resolvability_evidence=ev("match_resolvability"),action_gate_evidence=ev("action_gate_callability"),a_population_replenishment_evidence=ev("a_population_replenishment"),b_population_replenishment_evidence=ev("b_population_replenishment"),recurring_connection_pressure_evidence=ev("recurring_connection_pressure"),recurring_missing_edge_evidence=ev("recurring_missing_edge"),recurring_event_source_evidence=ev("recurring_event_source"),**raw["flags"])
class T(unittest.TestCase):
 def test_retained_formation_is_independently_regenerative_and_high_attraction(self):
  s=load(); self.assertEqual(strategic_drift_errors(s),[])
  f=s["examined_formations"][0]
  self.assertIs(attraction_beacon_state(build(s,f)),AttractionBeaconState.HIGH_ATTRACTION_BEACON)
  self.assertEqual(s["retained_research_formations"],["ATTRACTION_SCAN_163-F1"])
 def test_paid_tasks_are_downstream_not_ontology(self):
  s=load(); self.assertTrue(s["drift_audit"]["explicit_transaction_seed_not_ontology"]); self.assertTrue(s["drift_audit"]["downstream_paid_tasks_used_only_after_independent_field_evidence"])
  self.assertEqual(s["examined_formations"][0]["regenerative_field_gate"]["seed_kind"],"BROAD_REALITY_PATTERN")
 def test_bootstrap_queue_has_one_preflight_and_two_nonexecution_controls(self):
  q=load()["bootstrap_queue"]; self.assertEqual(len(q),3)
  self.assertEqual(q[0]["current_status"],"PREFLIGHT_READY_NOT_EXECUTION_AUTHORIZED")
  self.assertIn("LOW_MARGIN",q[1]["current_status"]); self.assertIn("REJECT",q[2]["current_status"])
 def test_no_commercial_promotion_or_side_effect(self):
  s=load(); self.assertEqual(s["commercial_candidates"],[]); self.assertEqual(s["active_transaction_units"],[]); self.assertEqual(s["first_external_value_flow"],"NOT_PROVEN"); self.assertFalse(s["external_side_effects_performed"])
if __name__=="__main__": unittest.main()
