import json
import unittest
from pathlib import Path

from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, AttractionEvidence, attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors

ROOT=Path(__file__).resolve().parents[1]
SCAN_PATH=ROOT/"data"/"research_runs"/"attraction_scan_149.json"
STATE_PATH=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def build_profile(scan,row):
    raw=row["attraction_profile"]; registry=scan["source_registry"]
    def ev(key):
        return tuple(AttractionEvidence(source_id=ref,claim=registry[ref]["claim"]) for ref in raw["evidence"][key])
    left,right=row["title"].split(" -> ",1)
    return AttractionDiscoveryProfile(
        signal_id=row["formation_id"],reality_pattern=row["evidence_summary"],a_actor=left,b_actor=right,candidate_bridge=row["title"],
        **raw["scores"],
        a_motion_evidence=ev("a_voluntary_motion"),b_motion_evidence=ev("b_voluntary_motion"),
        value_jump_evidence=ev("state_dependent_value_jump"),decision_window_evidence=ev("decision_window"),
        bridge_compression_evidence=ev("bridge_compression"),activation_evidence=ev("activation_ease"),
        self_propulsion_evidence=ev("self_propulsion"),operator_control_evidence=ev("operator_control"),
        a_discoverability_evidence=ev("a_discoverability"),b_discoverability_evidence=ev("b_discoverability"),
        match_resolvability_evidence=ev("match_resolvability"),action_gate_evidence=ev("action_gate_callability"),
        a_population_replenishment_evidence=ev("a_population_replenishment"),b_population_replenishment_evidence=ev("b_population_replenishment"),
        recurring_connection_pressure_evidence=ev("recurring_connection_pressure"),recurring_missing_edge_evidence=ev("recurring_missing_edge"),
        recurring_event_source_evidence=ev("recurring_event_source"),**raw["flags"]
    )

class Scan149BroadRealityServiceRailsTests(unittest.TestCase):
    def test_scan149_all_profiles_close_and_guard_passes(self):
        scan=load(SCAN_PATH)
        self.assertEqual(strategic_drift_errors(scan),[])
        for row in scan["examined_formations"]:
            self.assertIs(attraction_beacon_state(build_profile(scan,row)),AttractionBeaconState.LOW_ATTRACTION)
        self.assertEqual(scan["high_attraction_beacons"],[])
        self.assertEqual(scan["retained_research_formations"],[])
        self.assertEqual(scan["active_commercial_candidate_promotions"],[])
        self.assertEqual(scan["active_transaction_unit_promotions"],[])

    def test_scan149_is_fresh_and_machine_state_advances(self):
        scan=load(SCAN_PATH); state=load(STATE_PATH)
        self.assertTrue(scan["strategic_reboot"]["scan148_remote_local_execution_not_used_as_prior"])
        self.assertEqual(state["last_completed_scan_id"],"ATTRACTION_SCAN_149")
        self.assertEqual(state["next_scan_id"],"ATTRACTION_SCAN_150")
        self.assertEqual(state["active_commercial_candidates"],[])
        self.assertEqual(state["active_transaction_units"],[])
        self.assertEqual(state["first_external_value_flow"],"NOT_PROVEN")
        self.assertEqual(state["scan148_cross_border_local_execution"]["final_jev_next_action"],"ADVANCE_TO_NEXT_SCAN")

if __name__=="__main__":
    unittest.main()
