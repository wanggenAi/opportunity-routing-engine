import json
import unittest
from pathlib import Path

from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, AttractionEvidence, attraction_beacon_state
from src.strategic_drift_guard import strategic_drift_errors

ROOT = Path(__file__).resolve().parents[1]
SCAN_PATH = ROOT / "data" / "research_runs" / "attraction_scan_149.json"
STATE_PATH = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def profile(scan, row):
    raw = row["attraction_profile"]
    registry = scan["source_registry"]
    def ev(key):
        return tuple(AttractionEvidence(source_id=ref, claim=registry[ref]["claim"]) for ref in raw["evidence"][key])
    left, right = row["title"].split(" -> ", 1)
    return AttractionDiscoveryProfile(
        signal_id=row["formation_id"],
        reality_pattern=row["evidence_summary"],
        a_actor=left,
        b_actor=right,
        candidate_bridge=row["title"],
        **raw["scores"],
        a_motion_evidence=ev("a_voluntary_motion"),
        b_motion_evidence=ev("b_voluntary_motion"),
        value_jump_evidence=ev("state_dependent_value_jump"),
        decision_window_evidence=ev("decision_window"),
        bridge_compression_evidence=ev("bridge_compression"),
        activation_evidence=ev("activation_ease"),
        self_propulsion_evidence=ev("self_propulsion"),
        operator_control_evidence=ev("operator_control"),
        a_discoverability_evidence=ev("a_discoverability"),
        b_discoverability_evidence=ev("b_discoverability"),
        match_resolvability_evidence=ev("match_resolvability"),
        action_gate_evidence=ev("action_gate_callability"),
        a_population_replenishment_evidence=ev("a_population_replenishment"),
        b_population_replenishment_evidence=ev("b_population_replenishment"),
        recurring_connection_pressure_evidence=ev("recurring_connection_pressure"),
        recurring_missing_edge_evidence=ev("recurring_missing_edge"),
        recurring_event_source_evidence=ev("recurring_event_source"),
        **raw["flags"],
    )

class Scan149BroadRealityObservableControlSurfacesTests(unittest.TestCase):
    def test_guard_and_zero_retention(self):
        scan = load(SCAN_PATH)
        self.assertEqual(scan["scan_id"], "ATTRACTION_SCAN_149")
        self.assertEqual(strategic_drift_errors(scan), [])
        self.assertTrue(all(attraction_beacon_state(profile(scan, row)) is AttractionBeaconState.LOW_ATTRACTION for row in scan["examined_formations"]))
        self.assertEqual(scan["high_attraction_beacons"], [])
        self.assertEqual(scan["retained_research_formations"], [])
        self.assertEqual(scan["active_commercial_candidate_promotions"], [])
        self.assertEqual(scan["active_transaction_unit_promotions"], [])

    def test_fresh_domains_do_not_rescue_scan148(self):
        scan = load(SCAN_PATH)
        self.assertTrue(scan["strategic_reboot"]["scan148_cross_border_local_execution_not_inherited"])
        self.assertTrue(scan["drift_audit"]["scan148_cross_border_local_execution_not_used_as_prior"])
        titles = " ".join(row["title"].lower() for row in scan["examined_formations"])
        self.assertNotIn("bounded non-specialist china-side physical tasks", titles)

    def test_machine_state_reconciles_scan148_and_advances_scan149(self):
        state = load(STATE_PATH)
        self.assertEqual(state["last_completed_scan_id"], "ATTRACTION_SCAN_149")
        self.assertEqual(state["last_completed_scan_file"], "data/research_runs/attraction_scan_149.json")
        self.assertEqual(state["next_scan_id"], "ATTRACTION_SCAN_150")
        self.assertEqual(state["active_commercial_candidates"], [])
        self.assertEqual(state["active_transaction_units"], [])
        self.assertEqual(state["first_external_value_flow"], "NOT_PROVEN")
        scan148 = state["scan148_cross_border_local_execution"]
        self.assertEqual(scan148["exact_head_validation_status"], "SUCCESS")
        self.assertEqual(scan148["final_repository_ci_run_id"], 35876703035)
        self.assertEqual(scan148["final_jev_run_id"], 35876703208)
        self.assertEqual(scan148["final_jev_effective_route_counts"], {"NO_FURTHER_RESEARCH": 5})
        self.assertEqual(scan148["merged_main_sha"], "c9e364c294af847095842dc0520234376689fc86")

    def test_scan149_all_five_are_authoritatively_resolved(self):
        state = load(STATE_PATH)
        resolved = {row["formation_id"]: row["verdict"] for row in state["resolved_research_formations"]}
        for suffix in ("F1","F2","F3","F4","F5"):
            self.assertTrue(resolved[f"ATTRACTION_SCAN_149-{suffix}"].startswith("DEMOTED_"))
        scan149 = state["scan149_broad_reality_observable_control_surfaces"]
        self.assertEqual(len(scan149["authoritative_closures"]), 5)
        self.assertEqual(scan149["retained_research_formations"], [])

if __name__ == "__main__":
    unittest.main()
