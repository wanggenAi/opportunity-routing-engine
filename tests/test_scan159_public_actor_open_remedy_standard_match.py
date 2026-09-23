import json
import unittest
from pathlib import Path

from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, AttractionEvidence, attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors

ROOT=Path(__file__).resolve().parents[1]
SCAN_PATH=ROOT/"data"/"research_runs"/"attraction_scan_159.json"
STATE_PATH=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def build_profile(scan,row):
    raw=row["attraction_profile"]; reg=scan["source_registry"]
    def ev(k):
        return tuple(AttractionEvidence(source_id=r,claim=reg[r]["claim"]) for r in raw["evidence"][k])
    left,right=row["title"].split(" -> ",1)
    return AttractionDiscoveryProfile(
        signal_id=row["formation_id"],reality_pattern=row["evidence_summary"],
        a_actor=left,b_actor=right,candidate_bridge=row["title"],**raw["scores"],
        a_motion_evidence=ev("a_voluntary_motion"),b_motion_evidence=ev("b_voluntary_motion"),
        value_jump_evidence=ev("state_dependent_value_jump"),decision_window_evidence=ev("decision_window"),
        bridge_compression_evidence=ev("bridge_compression"),activation_evidence=ev("activation_ease"),
        self_propulsion_evidence=ev("self_propulsion"),operator_control_evidence=ev("operator_control"),
        a_discoverability_evidence=ev("a_discoverability"),b_discoverability_evidence=ev("b_discoverability"),
        match_resolvability_evidence=ev("match_resolvability"),action_gate_evidence=ev("action_gate_callability"),
        a_population_replenishment_evidence=ev("a_population_replenishment"),
        b_population_replenishment_evidence=ev("b_population_replenishment"),
        recurring_connection_pressure_evidence=ev("recurring_connection_pressure"),
        recurring_missing_edge_evidence=ev("recurring_missing_edge"),
        recurring_event_source_evidence=ev("recurring_event_source"),**raw["flags"]
    )

class Scan159PublicActorOpenRemedyStandardMatchTests(unittest.TestCase):
    def test_guard_and_beacon_closures(self):
        scan=load(SCAN_PATH)
        self.assertEqual(strategic_drift_errors(scan),[])
        for row in scan["examined_formations"]:
            self.assertIs(attraction_beacon_state(build_profile(scan,row)),AttractionBeaconState.LOW_ATTRACTION)
        self.assertEqual(scan["high_attraction_beacons"],[])
        self.assertEqual(scan["retained_research_formations"],[])

    def test_electrical_staffing_near_miss_does_not_relabel_regulator_control(self):
        scan=load(SCAN_PATH)
        row={x["formation_id"]:x for x in scan["examined_formations"]}["ATTRACTION_SCAN_159-F1"]
        self.assertEqual(row["attraction_profile"]["scores"]["a_discoverability"],3)
        self.assertEqual(row["attraction_profile"]["scores"]["b_discoverability"],3)
        self.assertEqual(row["attraction_profile"]["scores"]["decision_window"],3)
        self.assertEqual(row["state_change_gate"]["decisive_action_gate"]["owner_state"],"REGULATOR_OWNED")
        self.assertEqual(row["attraction_profile"]["scores"]["operator_control"],1)
        self.assertIn("ATTRACTION_SCAN_159-F1",scan["near_miss_formations"])

    def test_all_state_change_dimensions_are_evidence_bound(self):
        scan=load(SCAN_PATH)
        for row in scan["examined_formations"]:
            for k in ("event_trace","affected_actor_population","counterparty_population","decisive_action_gate"):
                self.assertEqual(row["state_change_gate"][k]["state"],"EVIDENCED")
                self.assertTrue(row["state_change_gate"][k]["evidence_refs"])

    def test_machine_state_finalizes_scan158_and_advances(self):
        state=load(STATE_PATH); prior=state["scan158_open_remedy_discoverability_gates"]
        self.assertEqual(prior["status"],"MERGED_FINAL_EXACT_HEAD_GREEN_ALL_ROUTES_CLOSED")
        self.assertEqual(prior["final_exact_head_sha"],"24ddc39679ffb5babb9a7ad3930c9768234eb882")
        self.assertEqual(prior["final_repository_ci_run_id"],35889264894)
        self.assertEqual(prior["final_repository_ci_test_count"],804)
        self.assertEqual(prior["final_jev_run_id"],35889264907)
        self.assertEqual(prior["final_jev_artifact_id"],10763458339)
        self.assertEqual(prior["final_jev_effective_route_counts"],{"NO_FURTHER_RESEARCH":5})
        self.assertEqual(prior["merged_pr"],473)
        self.assertEqual(prior["merged_main_sha"],"674e814a9de53620851ee40a5f1ae1c9387e79a5")
        self.assertGreaterEqual(int(state["last_completed_scan_id"].rsplit("_",1)[1]),159)
        self.assertGreaterEqual(int(state["next_scan_id"].rsplit("_",1)[1]),160)

    def test_no_commercial_or_side_effect_promotion(self):
        state=load(STATE_PATH)
        self.assertEqual(state["active_commercial_candidates"],[])
        self.assertEqual(state["active_transaction_units"],[])
        self.assertEqual(state["first_external_value_flow"],"NOT_PROVEN")
        self.assertFalse(state["scan159_public_actor_open_remedy_standard_match"]["external_side_effects_performed"])
        self.assertTrue(state["scan159_public_actor_open_remedy_standard_match"]["certificate_renting_route_forbidden"])

if __name__=="__main__":
    unittest.main()
