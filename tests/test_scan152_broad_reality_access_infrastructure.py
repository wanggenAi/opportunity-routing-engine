import json
import unittest
from pathlib import Path

from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, AttractionEvidence, attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors

ROOT=Path(__file__).resolve().parents[1]
SCAN_PATH=ROOT/"data"/"research_runs"/"attraction_scan_152.json"
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

class Scan152BroadRealityAccessInfrastructureTests(unittest.TestCase):
    def test_all_profiles_close_and_guard_passes(self):
        scan=load(SCAN_PATH)
        self.assertEqual(strategic_drift_errors(scan),[])
        for row in scan["examined_formations"]:
            self.assertIs(attraction_beacon_state(build_profile(scan,row)),AttractionBeaconState.LOW_ATTRACTION)
        self.assertEqual(scan["high_attraction_beacons"],[])
        self.assertEqual(scan["retained_research_formations"],[])
        self.assertEqual(scan["active_commercial_candidate_promotions"],[])
        self.assertEqual(scan["active_transaction_unit_promotions"],[])

    def test_overseas_warehouse_residual_friction_is_preserved_not_auto_killed(self):
        scan=load(SCAN_PATH)
        row={x["formation_id"]:x for x in scan["examined_formations"]}["ATTRACTION_SCAN_152-F4"]
        scores=row["attraction_profile"]["scores"]
        self.assertEqual(scores["recurring_missing_edge"],2)
        self.assertEqual(scores["match_resolvability"],1)
        self.assertEqual(scores["action_gate_callability"],1)
        self.assertTrue(row["attraction_profile"]["flags"]["expert_matching_required_per_transaction"])
        self.assertTrue(scan["drift_audit"]["incumbent_presence_not_used_as_automatic_kill"])
        self.assertTrue(scan["drift_audit"]["residual_overseas_warehouse_friction_preserved"])

    def test_compute_generic_routing_is_not_mistaken_for_distinct_router(self):
        scan=load(SCAN_PATH)
        row={x["formation_id"]:x for x in scan["examined_formations"]}["ATTRACTION_SCAN_152-F3"]
        self.assertEqual(row["attraction_profile"]["scores"]["action_gate_callability"],3)
        self.assertEqual(row["attraction_profile"]["scores"]["recurring_missing_edge"],1)
        self.assertTrue(row["attraction_profile"]["flags"]["generic_agent_substitutable"])

    def test_machine_state_reconciles_scan151_and_advances(self):
        state=load(STATE_PATH)
        self.assertEqual(state["last_completed_scan_id"],"ATTRACTION_SCAN_152")
        self.assertEqual(state["next_scan_id"],"ATTRACTION_SCAN_153")
        self.assertEqual(state["active_commercial_candidates"],[])
        self.assertEqual(state["active_transaction_units"],[])
        self.assertEqual(state["first_external_value_flow"],"NOT_PROVEN")
        prior=state["scan151_broad_reality_direct_service_platforms"]
        self.assertEqual(prior["final_exact_head_sha"],"9515f7ff88e3dec54c0a6b92d49e15f5dde67370")
        self.assertEqual(prior["final_repository_ci_run_id"],35879899892)
        self.assertEqual(prior["final_repository_ci_test_count"],769)
        self.assertEqual(prior["final_jev_run_id"],35879899900)
        self.assertEqual(prior["final_jev_artifact_id"],10758929493)
        self.assertEqual(prior["final_jev_effective_route_counts"],{"NO_FURTHER_RESEARCH":5})
        self.assertEqual(prior["merged_main_sha"],"5ee5967a1ec4a542943ca8ae715d9f085e686359")

    def test_all_five_are_authoritatively_resolved(self):
        state=load(STATE_PATH)
        resolved={row["formation_id"]:row["verdict"] for row in state["resolved_research_formations"]}
        for suffix in ("F1","F2","F3","F4","F5"):
            self.assertTrue(resolved[f"ATTRACTION_SCAN_152-{suffix}"].startswith("DEMOTED_"))
        self.assertEqual(len(state["scan152_broad_reality_access_infrastructure"]["authoritative_closures"]),5)

if __name__=="__main__":
    unittest.main()
