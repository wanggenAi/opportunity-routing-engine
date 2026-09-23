import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "commercial_reset_state.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan136_f1_f2_routing_followup_evidence.json"


class Scan136RoutingFollowupTests(unittest.TestCase):
    def test_latest_main_jev_routes_are_consumed_fail_closed(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        followup = state["scan136_f1_f2_routing_followup"]

        self.assertEqual(evidence["scan_id"], "ATTRACTION_SCAN_136")
        self.assertEqual(evidence["source_jev"]["jev_run_id"], 35830677629)
        self.assertEqual(
            evidence["source_jev"]["routes"]["ATTRACTION_SCAN_136-F1"],
            "EXACT_INCUMBENT_PREFLIGHT",
        )
        self.assertEqual(
            evidence["source_jev"]["routes"]["ATTRACTION_SCAN_136-F2"],
            "CAUSAL_DESCENT",
        )
        self.assertEqual(
            evidence["source_jev"]["latest_exact_head"]["routes"]["ATTRACTION_SCAN_136-F1"],
            "CAUSAL_DESCENT",
        )
        self.assertEqual(
            evidence["source_jev"]["latest_exact_head"]["routes"]["ATTRACTION_SCAN_136-F2"],
            "CAUSAL_DESCENT",
        )
        self.assertTrue(followup["route_consumed"])
        self.assertEqual(
            followup["consumed_f1_routes"],
            ["EXACT_INCUMBENT_PREFLIGHT", "CAUSAL_DESCENT"],
        )
        self.assertEqual(followup["consumed_f2_routes"], ["CAUSAL_DESCENT"])
        self.assertEqual(followup["latest_jev_run_id"], 35832460027)
        self.assertEqual(len(followup["route_history"]), 2)
        self.assertEqual(followup["public_research_resolution"], "EXHAUSTED_FOR_F1_F2")
        self.assertTrue(followup["scan137_gate_unblocked"])
        self.assertFalse(followup["external_contact_performed"])
        self.assertFalse(followup["commercial_promotion"])
        self.assertFalse(followup["bid_authorized"])
        self.assertFalse(followup["deposit_authorized"])
        self.assertFalse(followup["purchase_authorized"])

    def test_f1_f2_remain_research_only_at_external_evidence_boundary(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        by_id = {item["formation_id"]: item for item in evidence["formations"]}

        for formation_id in ("ATTRACTION_SCAN_136-F1", "ATTRACTION_SCAN_136-F2"):
            item = by_id[formation_id]
            self.assertEqual(item["public_research_resolution"], "EXHAUSTED")
            self.assertTrue(item["formation_status"].startswith("RETAINED_RESEARCH_BLOCKED_"))
            self.assertFalse(item["external_contact_performed"])
            self.assertFalse(item["commercial_promotion"])
            self.assertIn(formation_id, state["retained_research_formations"])

        self.assertEqual(state["scan136"]["exact_head_validation_status"], "SUCCESS")
        self.assertEqual(state["scan136"]["jev_route_status"], "CONSUMED")
        self.assertEqual(state["next_scan_id"], "ATTRACTION_SCAN_137")
        self.assertEqual(state["active_commercial_candidates"], [])
        self.assertEqual(state["active_transaction_units"], [])
        self.assertEqual(state["first_external_value_flow"], "NOT_PROVEN")

    def test_authoritative_scan136_closures_are_not_reopened(self):
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.assertEqual(
            evidence["authoritative_closures_preserved"],
            ["ATTRACTION_SCAN_136-F3", "ATTRACTION_SCAN_136-F4"],
        )


if __name__ == "__main__":
    unittest.main()
