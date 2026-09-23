import json
import unittest
from pathlib import Path

from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, AttractionEvidence, attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors

ROOT=Path(__file__).resolve().parents[1]
SCAN_PATH=ROOT/"data"/"research_runs"/"attraction_scan_151.json"
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

class Scan151BroadRealityDirectServicePlatformsTests(unittest.TestCase):
    def test_all_profiles_close_and_guard_passes(self):
        scan=load(SCAN_PATH)
        self.assertEqual(strategic_drift_errors(scan),[])
        for row in scan["examined_formations"]:
            self.assertIs(attraction_beacon_state(build_profile(scan,row)),AttractionBeaconState.LOW_ATTRACTION)
        self.assertEqual(scan["high_attraction_beacons"],[])
        self.assertEqual(scan["retained_research_formations"],[])
        self.assertEqual(scan["active_commercial_candidate_promotions"],[])
        self.assertEqual(scan["active_transaction_unit_promotions"],[])

    def test_exact_platform_loops_are_not_reclassified_as_missing_edges(self):
        scan=load(SCAN_PATH)
        by_id={row["formation_id"]:row for row in scan["examined_formations"]}
        self.assertEqual(by_id["ATTRACTION_SCAN_151-F3"]["attraction_profile"]["scores"]["recurring_missing_edge"],1)
        self.assertEqual(by_id["ATTRACTION_SCAN_151-F5"]["attraction_profile"]["scores"]["recurring_missing_edge"],1)
        self.assertIn("assuming carrier responsibility",scan["source_registry"]["FREIGHT-MOT-20260126"]["claim"])
        self.assertIn("audits and verifies vulnerabilities",scan["source_registry"]["SECURITY-VULBOX-FLASH-20260923"]["claim"])

    def test_machine_state_reconciles_scan150_and_advances(self):
        state=load(STATE_PATH)
        self.assertEqual(state["last_completed_scan_id"],"ATTRACTION_SCAN_151")
        self.assertEqual(state["next_scan_id"],"ATTRACTION_SCAN_152")
        self.assertEqual(state["active_commercial_candidates"],[])
        self.assertEqual(state["active_transaction_units"],[])
        self.assertEqual(state["first_external_value_flow"],"NOT_PROVEN")
        scan150=state["scan150_broad_reality_controlled_interfaces"]
        self.assertEqual(scan150["final_exact_head_sha"],"2eef8bcca85b8e7aff45350089caba45860f2a43")
        self.assertEqual(scan150["final_repository_ci_run_id"],35879006327)
        self.assertEqual(scan150["final_jev_run_id"],35879006323)
        self.assertEqual(scan150["final_jev_effective_route_counts"],{"NO_FURTHER_RESEARCH":5})
        self.assertEqual(scan150["merged_main_sha"],"7964aa4809f41e748f083ed431a47fc89ff548ad")

    def test_all_five_are_authoritatively_resolved(self):
        state=load(STATE_PATH)
        resolved={row["formation_id"]:row["verdict"] for row in state["resolved_research_formations"]}
        for suffix in ("F1","F2","F3","F4","F5"):
            self.assertTrue(resolved[f"ATTRACTION_SCAN_151-{suffix}"].startswith("DEMOTED_"))
        self.assertEqual(len(state["scan151_broad_reality_direct_service_platforms"]["authoritative_closures"]),5)

if __name__=="__main__":
    unittest.main()
