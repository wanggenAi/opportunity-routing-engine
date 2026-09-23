import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "commercial_reset_state.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan139_f1_causal_descent_evidence.json"


class Scan139F1CausalDescentTests(unittest.TestCase):
    def test_live_jev_causal_route_is_consumed_fail_closed(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        followup = state["scan139_f1_causal_descent"]

        self.assertEqual(evidence["scan_id"], "ATTRACTION_SCAN_139")
        self.assertEqual(evidence["source_jev"]["jev_run_id"], 35839247533)
        self.assertEqual(evidence["source_jev"]["input_scan_id"], "ATTRACTION_SCAN_139")
        self.assertEqual(evidence["source_jev"]["entity_count"], 4)
        self.assertEqual(evidence["source_jev"]["state_fingerprint"], "e4427727ac809edaab75")
        self.assertEqual(evidence["source_jev"]["routes"]["ATTRACTION_SCAN_139-F1"], "CAUSAL_DESCENT")
        self.assertTrue(evidence["route_consumed"])
        self.assertEqual(evidence["consumed_routes"], ["CAUSAL_DESCENT"])
        self.assertTrue(followup["route_consumed"])
        self.assertFalse(followup["external_contact_performed"])
        self.assertFalse(followup["commercial_promotion"])

    def test_f1_remains_research_only_at_external_evidence_boundary(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))

        self.assertEqual(evidence["public_research_resolution"], "EXHAUSTED")
        self.assertEqual(
            evidence["formation_status"],
            "RETAINED_RESEARCH_BLOCKED_ON_EXTERNAL_WRITTEN_OR_SOURCE_DOCUMENT_DILIGENCE",
        )
        self.assertIn("ATTRACTION_SCAN_139-F1", state["retained_research_formations"])
        self.assertEqual(state["active_commercial_candidates"], [])
        self.assertEqual(state["active_transaction_units"], [])
        self.assertEqual(state["first_external_value_flow"], "NOT_PROVEN")

    def test_surface_yield_is_not_promoted_without_buyer_receipt_cursor(self):
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))

        self.assertIn("6_90_PERCENT", evidence["causal_descent_resolution"])
        self.assertIn("BUYER_RECEIPT_START", evidence["causal_descent_resolution"])
        self.assertIn("PREPAYMENT_CURSOR", evidence["causal_descent_resolution"])
        self.assertIn("2028-09-30", " ".join(evidence["causal_chain"]))
        self.assertFalse(evidence["bid_authorized"])
        self.assertFalse(evidence["deposit_authorized"])
        self.assertFalse(evidence["purchase_authorized"])

    def test_scan140_gate_history_remains_valid_after_successor_scan_progress(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        followup = state["scan139_f1_causal_descent"]

        self.assertEqual(
            followup["scan140_gate"],
            "UNBLOCKED_SUBJECT_TO_EXACT_HEAD_CI_AND_LIVE_JEV_NO_NEW_ROUTE_CLASS",
        )
        self.assertEqual(followup["final_scan140_gate_validation"], "SUCCESS")
        self.assertGreaterEqual(
            int(state["next_scan_id"].rsplit("_", 1)[-1]),
            140,
        )


if __name__ == "__main__":
    unittest.main()
