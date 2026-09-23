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

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_165.json"
PREFLIGHT=ROOT/"data"/"research_runs"/"scan165_9610_exact_incumbent_preflight.json"

def load(path):
    return json.loads(path.read_text())

def build_profile(scan,row):
    raw=row["attraction_profile"]
    registry=scan["source_registry"]
    def ev(key):
        return tuple(
            AttractionEvidence(source_id=ref,claim=registry[ref]["claim"])
            for ref in raw["evidence"][key]
        )
    return AttractionDiscoveryProfile(
        signal_id=row["formation_id"],
        reality_pattern=row["evidence_summary"],
        a_actor="cross-border ecommerce enterprise with a 9610 overseas return batch",
        b_actor="eligible China return ports and supervised logistics rails",
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

class Scan165CrossCustomsReturnRoutingTests(unittest.TestCase):
    def test_scan165_closes_retained_beacon_after_exact_preflight(self):
        scan=load(SCAN)
        self.assertEqual(strategic_drift_errors(scan),[])
        self.assertEqual(scan["retained_research_formations"],[])
        self.assertEqual(scan["high_attraction_beacons"],[])
        f1=scan["examined_formations"][0]
        self.assertIs(attraction_beacon_state(build_profile(scan,f1)),AttractionBeaconState.LOW_ATTRACTION)
        self.assertIn("POLICY_OPTIONALITY_IS_REAL",f1["verdict"])

    def test_preflight_corrects_route_control_and_match_claims(self):
        scan=load(SCAN)
        f1=scan["examined_formations"][0]
        self.assertEqual(f1["attraction_profile"]["scores"]["operator_control"],1)
        self.assertEqual(f1["attraction_profile"]["scores"]["match_resolvability"],1)
        self.assertEqual(f1["attraction_profile"]["scores"]["action_gate_callability"],1)
        self.assertEqual(f1["attraction_profile"]["scores"]["recurring_missing_edge"],1)
        self.assertEqual(
            f1["state_change_gate"]["decisive_action_gate"]["owner_state"],
            "FRAGMENTED_PLATFORM_LOGISTICS_SITE_CUSTOMS_CONTROL",
        )

    def test_jev_exact_incumbent_route_was_consumed(self):
        scan=load(SCAN)
        preflight=load(PREFLIGHT)
        self.assertEqual(
            scan["exact_incumbent_preflight"]["effective_route"],
            "EXACT_INCUMBENT_PREFLIGHT",
        )
        self.assertEqual(
            preflight["preflight_result"],
            "FAIL_DISTINCT_CALLABLE_ROUTING_SURFACE",
        )
        self.assertEqual(
            set(scan["authoritative_closures"]),
            {
                "ATTRACTION_SCAN_165-F1",
                "ATTRACTION_SCAN_165-F2",
                "ATTRACTION_SCAN_165-F3",
                "ATTRACTION_SCAN_165-F4",
                "ATTRACTION_SCAN_165-F5",
            },
        )

    def test_no_commercial_promotion_or_side_effect(self):
        scan=load(SCAN)
        self.assertEqual(scan["bootstrap_queue"],[])
        self.assertEqual(scan["commercial_candidates"],[])
        self.assertEqual(scan["active_transaction_units"],[])
        self.assertEqual(scan["first_external_value_flow"],"NOT_PROVEN")
        self.assertFalse(scan["external_side_effects_performed"])

if __name__=="__main__":
    unittest.main()
