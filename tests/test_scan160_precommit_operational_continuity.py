import json
import unittest
from pathlib import Path

from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, AttractionEvidence, attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors

ROOT=Path(__file__).resolve().parents[1]
SCAN_PATH=ROOT/"data"/"research_runs"/"attraction_scan_160.json"
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

class Scan160PrecommitOperationalContinuityTests(unittest.TestCase):
    def test_guard_and_all_examined_formations_remain_low(self):
        scan=load(SCAN_PATH)
        self.assertEqual(strategic_drift_errors(scan),[])
        for row in scan["examined_formations"]:
            self.assertIs(attraction_beacon_state(build_profile(scan,row)),AttractionBeaconState.LOW_ATTRACTION)
        self.assertEqual(scan["high_attraction_beacons"],[])
        self.assertEqual(scan["retained_research_formations"],[])

    def test_power_continuity_near_miss_preserves_expert_integration_floor(self):
        scan=load(SCAN_PATH)
        row={x["formation_id"]:x for x in scan["examined_formations"]}["ATTRACTION_SCAN_160-F1"]
        self.assertEqual(row["attraction_profile"]["scores"]["a_discoverability"],3)
        self.assertEqual(row["attraction_profile"]["scores"]["b_discoverability"],3)
        self.assertEqual(row["attraction_profile"]["scores"]["decision_window"],3)
        self.assertEqual(row["attraction_profile"]["scores"]["match_resolvability"],1)
        self.assertTrue(row["attraction_profile"]["flags"]["expert_matching_required_per_transaction"])
        self.assertIn("ATTRACTION_SCAN_160-F1",scan["near_miss_formations"])

    def test_water_scan_never_substitutes_drinking_water_for_process_water(self):
        scan=load(SCAN_PATH)
        row={x["formation_id"]:x for x in scan["examined_formations"]}["ATTRACTION_SCAN_160-F2"]
        self.assertEqual(row["state_change_gate"]["counterparty_population"]["state"],"UNKNOWN")
        self.assertIn("DRINKING_WATER",row["verdict"])
        self.assertTrue(scan["drift_audit"]["industrial_drinking_water_substitution_forbidden"])

    def test_gas_scan_fails_closed_on_safe_counterparty_unknown(self):
        scan=load(SCAN_PATH)
        row={x["formation_id"]:x for x in scan["examined_formations"]}["ATTRACTION_SCAN_160-F3"]
        self.assertEqual(row["state_change_gate"]["counterparty_population"]["state"],"UNKNOWN")
        self.assertTrue(row["attraction_profile"]["flags"]["expert_matching_required_per_transaction"])
        self.assertTrue(scan["drift_audit"]["hazardous_or_safety_sensitive_work_not_routed_as_generic_match"])

    def test_machine_state_finalizes_scan159_and_advances(self):
        state=load(STATE_PATH); prior=state["scan159_public_actor_open_remedy_standard_match"]
        self.assertEqual(prior["status"],"MERGED_FINAL_EXACT_HEAD_GREEN_ALL_ROUTES_CLOSED")
        self.assertEqual(prior["final_exact_head_sha"],"48701d753b509464ff7e260217e216460fec9cb7")
        self.assertEqual(prior["final_repository_ci_run_id"],35891248498)
        self.assertEqual(prior["final_repository_ci_test_count"],809)
        self.assertEqual(prior["final_jev_run_id"],35891248206)
        self.assertEqual(prior["final_jev_artifact_id"],10764344044)
        self.assertEqual(prior["final_jev_effective_route_counts"],{"NO_FURTHER_RESEARCH":5})
        self.assertEqual(prior["merged_pr"],474)
        self.assertEqual(prior["merged_main_sha"],"d503355a5a12776075dea543b18f0542f2402a79")
        self.assertGreaterEqual(int(state["last_completed_scan_id"].rsplit("_",1)[1]),160)
        self.assertGreaterEqual(int(state["next_scan_id"].rsplit("_",1)[1]),161)

    def test_no_commercial_or_external_side_effect_promotion(self):
        state=load(STATE_PATH)
        self.assertEqual(state["active_commercial_candidates"],[])
        self.assertEqual(state["active_transaction_units"],[])
        self.assertEqual(state["first_external_value_flow"],"NOT_PROVEN")
        current=state["scan160_precommit_operational_continuity"]
        self.assertFalse(current["commercial_promotion"])
        self.assertFalse(current["external_side_effects_performed"])

if __name__=="__main__":
    unittest.main()
