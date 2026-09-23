import json
import unittest
from pathlib import Path

from src.attraction_discovery import (
    AttractionBeaconState,
    AttractionDiscoveryProfile,
    AttractionEvidence,
    attraction_beacon_state,
)
from src.jev_research_advisory import build_research_states
from src.strategic_drift_guard import strategic_drift_errors


ROOT = Path(__file__).resolve().parents[1]
SCAN_PATH = ROOT / "data" / "research_runs" / "attraction_scan_148.json"
STATE_PATH = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def profile(scan, row):
    raw = row["attraction_profile"]
    registry = scan["source_registry"]

    def evidence(key):
        return tuple(
            AttractionEvidence(source_id=ref, claim=registry[ref]["claim"])
            for ref in raw["evidence"][key]
        )

    scores = raw["scores"]
    flags = raw["flags"]
    left, right = row["title"].split(" -> ", 1)
    return AttractionDiscoveryProfile(
        signal_id=row["formation_id"],
        reality_pattern=row["evidence_summary"],
        a_actor=left,
        b_actor=right,
        candidate_bridge=row["title"],
        **scores,
        a_motion_evidence=evidence("a_voluntary_motion"),
        b_motion_evidence=evidence("b_voluntary_motion"),
        value_jump_evidence=evidence("state_dependent_value_jump"),
        decision_window_evidence=evidence("decision_window"),
        bridge_compression_evidence=evidence("bridge_compression"),
        activation_evidence=evidence("activation_ease"),
        self_propulsion_evidence=evidence("self_propulsion"),
        operator_control_evidence=evidence("operator_control"),
        a_discoverability_evidence=evidence("a_discoverability"),
        b_discoverability_evidence=evidence("b_discoverability"),
        match_resolvability_evidence=evidence("match_resolvability"),
        action_gate_evidence=evidence("action_gate_callability"),
        a_population_replenishment_evidence=evidence("a_population_replenishment"),
        b_population_replenishment_evidence=evidence("b_population_replenishment"),
        recurring_connection_pressure_evidence=evidence("recurring_connection_pressure"),
        recurring_missing_edge_evidence=evidence("recurring_missing_edge"),
        recurring_event_source_evidence=evidence("recurring_event_source"),
        **flags,
    )


class Scan148CrossBorderLocalExecutionTests(unittest.TestCase):
    def test_guard_and_comparison_profiles(self):
        scan = load(SCAN_PATH)
        self.assertEqual(strategic_drift_errors(scan), [])

        states = {
            row["formation_id"]: attraction_beacon_state(profile(scan, row))
            for row in scan["examined_formations"]
        }
        self.assertIs(
            states["ATTRACTION_SCAN_148-F1"],
            AttractionBeaconState.HIGH_ATTRACTION_BEACON,
        )
        for suffix in ("F2", "F3", "F4", "F5"):
            self.assertIs(
                states[f"ATTRACTION_SCAN_148-{suffix}"],
                AttractionBeaconState.LOW_ATTRACTION,
            )

        self.assertEqual(
            [row["formation_id"] for row in scan["high_attraction_beacons"]],
            ["ATTRACTION_SCAN_148-F1"],
        )
        self.assertEqual(
            scan["retained_research_formations"],
            ["ATTRACTION_SCAN_148-F1"],
        )
        self.assertEqual(scan["active_commercial_candidate_promotions"], [])
        self.assertEqual(scan["active_transaction_unit_promotions"], [])

    def test_boundary_does_not_reopen_scan143_or_scan144(self):
        scan = load(SCAN_PATH)
        self.assertTrue(
            scan["strategic_reboot"]["scan143_factory_inspection_not_inherited"]
        )
        self.assertTrue(
            scan["strategic_reboot"]["scan144_aftermarket_service_not_inherited"]
        )
        boundary = scan["comparison_profiles"]["validated_boundary"].lower()
        self.assertIn("specialist inspection", boundary)
        self.assertIn("low-risk lawful bounded", boundary)

    def test_machine_state_scan148_and_scan147_reconciliation(self):
        state = load(STATE_PATH)
        last_scan_number = int(state["last_completed_scan_id"].rsplit("_", 1)[-1])
        next_scan_number = int(state["next_scan_id"].rsplit("_", 1)[-1])
        self.assertGreaterEqual(last_scan_number, 148)
        self.assertGreaterEqual(next_scan_number, 149)
        self.assertIn(
            "ATTRACTION_SCAN_148-F1",
            state["retained_research_formations"],
        )
        self.assertEqual(state["active_commercial_candidates"], [])
        self.assertEqual(state["active_transaction_units"], [])
        self.assertEqual(state["first_external_value_flow"], "NOT_PROVEN")
        scan147 = state["scan147_broad_reality_shared_capacity"]
        self.assertEqual(scan147["exact_head_validation_status"], "SUCCESS")
        self.assertEqual(scan147["final_jev_next_action"], "ADVANCE_TO_NEXT_SCAN")
        scan148 = state["scan148_cross_border_local_execution"]
        self.assertEqual(
            scan148["status"],
            "MERGED_FINAL_EXACT_HEAD_GREEN_ALL_ROUTES_CLOSED",
        )
        self.assertEqual(scan148["final_jev_next_action"], "ADVANCE_TO_NEXT_SCAN")

    def test_f1_route_consumption_is_authoritative_for_jev(self):
        scan = load(SCAN_PATH)
        state = load(STATE_PATH)
        states = build_research_states(
            scan=scan,
            commercial_state=state,
            max_entities=5,
        )
        by_id = {
            item["formation"]["formation_id"]: item
            for item in states
        }
        engine = by_id["ATTRACTION_SCAN_148-F1"]["authoritative_engine_context"]
        self.assertEqual(
            engine["existing_scan_verdict"],
            "RETAINED_FOR_JEV_RESEARCH_ROUTING_AFTER_BROAD_REALITY_AND_COMPARISON_PROFILE_VALIDATION",
        )
        self.assertTrue(
            engine["existing_verdict"].startswith(
                "DEMOTED_AFTER_EXACT_INCUMBENT_PREFLIGHT_"
            )
        )
        self.assertTrue(engine["resolved_in_commercial_state"])
        self.assertTrue(engine["existing_closure_authoritative"])


if __name__ == "__main__":
    unittest.main()
