import json
import unittest
from pathlib import Path

from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, AttractionEvidence, attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors

ROOT=Path(__file__).resolve().parents[1]
SCAN_PATH=ROOT/"data"/"research_runs"/"attraction_scan_157.json"
STATE_PATH=ROOT/"data"/"commercial_reset_state.json"

def load(path): return json.loads(path.read_text(encoding="utf-8"))
def build_profile(scan,row):
    raw=row["attraction_profile"]; registry=scan["source_registry"]
    def ev(key): return tuple(AttractionEvidence(source_id=ref,claim=registry[ref]["claim"]) for ref in raw["evidence"][key])
    left,right=row["title"].split(" -> ",1)
    return AttractionDiscoveryProfile(signal_id=row["formation_id"],reality_pattern=row["evidence_summary"],a_actor=left,b_actor=right,candidate_bridge=row["title"],**raw["scores"],
        a_motion_evidence=ev("a_voluntary_motion"),b_motion_evidence=ev("b_voluntary_motion"),value_jump_evidence=ev("state_dependent_value_jump"),decision_window_evidence=ev("decision_window"),bridge_compression_evidence=ev("bridge_compression"),activation_evidence=ev("activation_ease"),self_propulsion_evidence=ev("self_propulsion"),operator_control_evidence=ev("operator_control"),a_discoverability_evidence=ev("a_discoverability"),b_discoverability_evidence=ev("b_discoverability"),match_resolvability_evidence=ev("match_resolvability"),action_gate_evidence=ev("action_gate_callability"),a_population_replenishment_evidence=ev("a_population_replenishment"),b_population_replenishment_evidence=ev("b_population_replenishment"),recurring_connection_pressure_evidence=ev("recurring_connection_pressure"),recurring_missing_edge_evidence=ev("recurring_missing_edge"),recurring_event_source_evidence=ev("recurring_event_source"),**raw["flags"])

class Scan157EventTriggerUnownedActionGateTests(unittest.TestCase):
    def test_all_profiles_close_and_guard_passes(self):
        scan=load(SCAN_PATH)
        self.assertEqual(strategic_drift_errors(scan),[])
        for row in scan["examined_formations"]:
            self.assertIs(attraction_beacon_state(build_profile(scan,row)),AttractionBeaconState.LOW_ATTRACTION)
        self.assertEqual(scan["high_attraction_beacons"],[])
        self.assertEqual(scan["retained_research_formations"],[])

    def test_public_event_trace_does_not_fake_operator_control(self):
        scan=load(SCAN_PATH)
        self.assertTrue(scan["drift_audit"]["event_trigger_not_assumed_to_imply_unowned_action_gate"])
        for row in scan["examined_formations"]:
            self.assertEqual(row["attraction_profile"]["scores"]["operator_control"],1)
            self.assertEqual(row["attraction_profile"]["scores"]["recurring_missing_edge"],1)

    def test_no_explicit_transaction_became_the_search_ontology(self):
        scan=load(SCAN_PATH)
        self.assertTrue(scan["drift_audit"]["explicit_transaction_seed_not_ontology"])
        for row in scan["examined_formations"]:
            self.assertFalse(row["attraction_profile"]["flags"]["explicit_transaction_seeded"])

    def test_machine_state_finalizes_scan156_and_advances(self):
        state=load(STATE_PATH)
        prior=state["scan156_control_surface_gap_fresh_domains"]
        self.assertEqual(prior["status"],"MERGED_FINAL_EXACT_HEAD_GREEN_ALL_ROUTES_CLOSED")
        self.assertEqual(prior["final_exact_head_sha"],"b5496213904f69e58b78adcdf39afbdc1cbda0f2")
        self.assertEqual(prior["final_repository_ci_run_id"],35886932220)
        self.assertEqual(prior["final_repository_ci_test_job_id"],107269347142)
        self.assertEqual(prior["final_repository_ci_test_count"],793)
        self.assertEqual(prior["final_jev_run_id"],35886932262)
        self.assertEqual(prior["final_jev_artifact_id"],10763196922)
        self.assertEqual(prior["final_jev_effective_route_counts"],{"NO_FURTHER_RESEARCH":5})
        self.assertEqual(prior["merged_main_sha"],"e32757d5ce8200a4bc5bfdefed792fe7c6314a26")
        self.assertGreaterEqual(int(state["last_completed_scan_id"].rsplit("_",1)[1]),157)
        self.assertGreaterEqual(int(state["next_scan_id"].rsplit("_",1)[1]),158)
        self.assertEqual(state["active_commercial_candidates"],[])
        self.assertEqual(state["active_transaction_units"],[])
        self.assertEqual(state["first_external_value_flow"],"NOT_PROVEN")

    def test_all_five_are_authoritatively_resolved(self):
        state=load(STATE_PATH); resolved={x["formation_id"]:x["verdict"] for x in state["resolved_research_formations"]}
        for suffix in ("F1","F2","F3","F4","F5"): self.assertTrue(resolved[f"ATTRACTION_SCAN_157-{suffix}"].startswith("DEMOTED_"))
        self.assertEqual(len(state["scan157_event_trigger_unowned_action_gates"]["authoritative_closures"]),5)

if __name__=="__main__": unittest.main()
