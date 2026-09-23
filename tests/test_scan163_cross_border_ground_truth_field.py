import json
import unittest
from pathlib import Path

from src.attraction_discovery import (
    AttractionBeaconState,
    AttractionDiscoveryProfile,
    AttractionEvidence,
    attraction_beacon_state,
)
from src.strategic_drift_guard import strategic_drift_errors

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_163.json"
PREFLIGHT = ROOT / "data" / "research_runs" / "scan163_exact_incumbent_preflight.json"


def load(path=SCAN):
    return json.loads(path.read_text())


def build_profile(scan, row):
    raw = row["attraction_profile"]
    registry = scan["source_registry"]

    def ev(key):
        return tuple(
            AttractionEvidence(source_id=ref, claim=registry[ref]["claim"])
            for ref in raw["evidence"][key]
        )

    return AttractionDiscoveryProfile(
        signal_id=row["formation_id"],
        reality_pattern=row["evidence_summary"],
        a_actor="recurring overseas verification demand pumps",
        b_actor="China local field executors",
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


class Scan163CrossBorderGroundTruthFieldTests(unittest.TestCase):
    def test_final_scan_has_no_retained_beacon_after_exact_incumbent_preflight(self):
        scan = load()
        self.assertEqual(strategic_drift_errors(scan), [])
        self.assertEqual(scan["high_attraction_beacons"], [])
        self.assertEqual(scan["retained_research_formations"], [])
        f1 = scan["examined_formations"][0]
        self.assertIs(
            attraction_beacon_state(build_profile(scan, f1)),
            AttractionBeaconState.LOW_ATTRACTION,
        )
        self.assertIn("EXACT_INCUMBENT_PREFLIGHT", f1["verdict"])

    def test_field_was_independently_rederived_before_downstream_tasks(self):
        scan = load()
        self.assertTrue(scan["drift_audit"]["regenerative_field_revalidated"])
        self.assertTrue(scan["drift_audit"]["explicit_transaction_seed_not_ontology"])
        self.assertTrue(
            scan["drift_audit"]["downstream_paid_tasks_used_only_after_independent_field_evidence"]
        )
        self.assertEqual(
            scan["examined_formations"][0]["regenerative_field_gate"]["seed_kind"],
            "BROAD_REALITY_PATTERN",
        )

    def test_jev_preflight_was_consumed_into_authoritative_closure(self):
        scan = load()
        preflight = load(PREFLIGHT)
        self.assertEqual(preflight["preflight_result"], "FAIL_DISTINCT_OPERATOR_POSITION")
        self.assertEqual(
            scan["exact_incumbent_preflight"]["triggering_effective_route"],
            "EXACT_INCUMBENT_PREFLIGHT",
        )
        self.assertEqual(
            scan["examined_formations"][0]["state_change_gate"]["decisive_action_gate"]["owner_state"],
            "EXACT_INCUMBENT_SERVICE_LAYER_OWNED",
        )
        self.assertEqual(
            set(scan["authoritative_closures"]),
            {
                "ATTRACTION_SCAN_163-F1",
                "ATTRACTION_SCAN_163-F2",
                "ATTRACTION_SCAN_163-F3",
            },
        )

    def test_bootstrap_queue_does_not_spend_founder_capital_after_closure(self):
        queue = load()["bootstrap_queue"]
        self.assertEqual(len(queue), 3)
        self.assertIn("DO_NOT_EXECUTE", queue[0]["current_status"])
        self.assertIn("EVIDENCE_ONLY", queue[1]["current_status"])
        self.assertIn("REJECT", queue[2]["current_status"])

    def test_no_commercial_promotion_or_external_side_effect(self):
        scan = load()
        self.assertEqual(scan["commercial_candidates"], [])
        self.assertEqual(scan["active_transaction_units"], [])
        self.assertEqual(scan["first_external_value_flow"], "NOT_PROVEN")
        self.assertFalse(scan["external_side_effects_performed"])


if __name__ == "__main__":
    unittest.main()
