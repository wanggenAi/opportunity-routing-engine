import json
import unittest
from pathlib import Path

from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, AttractionEvidence, attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors

ROOT=Path(__file__).resolve().parents[1]
SCAN_PATH=ROOT/"data"/"research_runs"/"attraction_scan_155.json"
STATE_PATH=ROOT/"data"/"commercial_reset_state.json"

def load(path): return json.loads(path.read_text(encoding="utf-8"))
def build_profile(scan,row):
    raw=row["attraction_profile"]; registry=scan["source_registry"]
    def ev(key): return tuple(AttractionEvidence(source_id=ref,claim=registry[ref]["claim"]) for ref in raw["evidence"][key])
    left,right=row["title"].split(" -> ",1)
    return AttractionDiscoveryProfile(signal_id=row["formation_id"],reality_pattern=row["evidence_summary"],a_actor=left,b_actor=right,candidate_bridge=row["title"],**raw["scores"],
        a_motion_evidence=ev("a_voluntary_motion"),b_motion_evidence=ev("b_voluntary_motion"),value_jump_evidence=ev("state_dependent_value_jump"),decision_window_evidence=ev("decision_window"),bridge_compression_evidence=ev("bridge_compression"),activation_evidence=ev("activation_ease"),self_propulsion_evidence=ev("self_propulsion"),operator_control_evidence=ev("operator_control"),a_discoverability_evidence=ev("a_discoverability"),b_discoverability_evidence=ev("b_discoverability"),match_resolvability_evidence=ev("match_resolvability"),action_gate_evidence=ev("action_gate_callability"),a_population_replenishment_evidence=ev("a_population_replenishment"),b_population_replenishment_evidence=ev("b_population_replenishment"),recurring_connection_pressure_evidence=ev("recurring_connection_pressure"),recurring_missing_edge_evidence=ev("recurring_missing_edge"),recurring_event_source_evidence=ev("recurring_event_source"),generic_agent_substitution_evidence=ev("bridge_compression") if raw["flags"].get("generic_agent_substitutable") else (),**raw["flags"])

class Scan155FailureWorkaroundFreshDomainTests(unittest.TestCase):
    def test_all_profiles_close_and_guard_passes(self):
        scan=load(SCAN_PATH)
        self.assertEqual(strategic_drift_errors(scan),[])
        for row in scan["examined_formations"]:
            self.assertIs(attraction_beacon_state(build_profile(scan,row)),AttractionBeaconState.LOW_ATTRACTION)
        self.assertEqual(scan["high_attraction_beacons"],[])
        self.assertEqual(scan["retained_research_formations"],[])

    def test_ev_failure_is_preserved_without_faking_operator_control(self):
        scan=load(SCAN_PATH); rows={x["formation_id"]:x for x in scan["examined_formations"]}
        self.assertEqual(rows["ATTRACTION_SCAN_155-F2"]["attraction_profile"]["scores"]["recurring_missing_edge"],2)
        self.assertEqual(rows["ATTRACTION_SCAN_155-F2"]["attraction_profile"]["scores"]["operator_control"],1)
        self.assertTrue(scan["drift_audit"]["residual_ev_charging_failure_preserved"])

    def test_platformized_fields_do_not_fake_missing_edges(self):
        scan=load(SCAN_PATH); rows={x["formation_id"]:x for x in scan["examined_formations"]}
        for fid in ("ATTRACTION_SCAN_155-F1","ATTRACTION_SCAN_155-F3","ATTRACTION_SCAN_155-F4","ATTRACTION_SCAN_155-F5"):
            self.assertEqual(rows[fid]["attraction_profile"]["scores"]["recurring_missing_edge"],1)

    def test_machine_state_finalizes_scan154_and_advances(self):
        state=load(STATE_PATH)
        prior=state["scan154_failure_workaround_first"]
        self.assertEqual(prior["status"],"MERGED_FINAL_EXACT_HEAD_GREEN_ALL_ROUTES_CLOSED")
        self.assertEqual(prior["final_exact_head_sha"],"94811b6f62598b20b3aaf1ee081188798e6ce8ae")
        self.assertEqual(prior["final_repository_ci_run_id"],35884382382)
        self.assertEqual(prior["final_repository_ci_test_job_id"],107260670704)
        self.assertEqual(prior["final_repository_ci_test_count"],783)
        self.assertEqual(prior["final_jev_run_id"],35884382385)
        self.assertEqual(prior["final_jev_artifact_id"],10761597741)
        self.assertEqual(prior["final_jev_effective_route_counts"],{"NO_FURTHER_RESEARCH":5})
        self.assertEqual(prior["merged_main_sha"],"1041b296d0990c3b7cf526a71436c1e7abbcacd7")
        self.assertEqual(state["last_completed_scan_id"],"ATTRACTION_SCAN_155")
        self.assertEqual(state["next_scan_id"],"ATTRACTION_SCAN_156")
        self.assertEqual(state["active_commercial_candidates"],[])
        self.assertEqual(state["active_transaction_units"],[])
        self.assertEqual(state["first_external_value_flow"],"NOT_PROVEN")

    def test_all_five_are_authoritatively_resolved(self):
        state=load(STATE_PATH); resolved={x["formation_id"]:x["verdict"] for x in state["resolved_research_formations"]}
        for suffix in ("F1","F2","F3","F4","F5"): self.assertTrue(resolved[f"ATTRACTION_SCAN_155-{suffix}"].startswith("DEMOTED_"))
        self.assertEqual(len(state["scan155_failure_workaround_fresh_domains"]["authoritative_closures"]),5)

if __name__=="__main__": unittest.main()
