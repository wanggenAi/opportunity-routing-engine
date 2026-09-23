import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "commercial_reset_state.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan135_f1_causal_descent_evidence.json"


class Scan135F1CausalDescentTests(unittest.TestCase):
    def test_public_route_is_consumed_without_commercial_promotion(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        followup = state["scan135_f1_causal_descent"]

        self.assertEqual(evidence["formation_id"], "ATTRACTION_SCAN_135-F1")
        self.assertEqual(evidence["public_research_resolution"], "EXHAUSTED")
        self.assertFalse(evidence["external_contact_performed"])
        self.assertFalse(evidence["commercial_promotion"])
        self.assertFalse(evidence["bid_authorized"])
        self.assertFalse(evidence["deposit_authorized"])
        self.assertFalse(evidence["purchase_authorized"])

        self.assertTrue(followup["jev_route_consumed"])
        self.assertEqual(followup["public_research_resolution"], "EXHAUSTED")
        self.assertEqual(
            followup["formation_status"],
            "RETAINED_RESEARCH_BLOCKED_ON_EXTERNAL_WRITTEN_EVIDENCE",
        )
        self.assertTrue(followup["scan136_gate_unblocked"])
        self.assertFalse(followup["external_contact_authorized"])
        self.assertEqual(state["retained_research_formations"], ["ATTRACTION_SCAN_135-F1"])
        self.assertEqual(state["active_commercial_candidates"], [])
        self.assertEqual(state["active_transaction_units"], [])
        self.assertEqual(state["next_scan_id"], "ATTRACTION_SCAN_136")


if __name__ == "__main__":
    unittest.main()
