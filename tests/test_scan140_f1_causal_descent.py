import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_140.json"
STATE = ROOT / "data" / "commercial_reset_state.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan140_f1_causal_descent_evidence.json"


class Scan140F1CausalDescentTests(unittest.TestCase):
    def test_live_jev_route_is_recorded_and_consumed(self):
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.assertEqual(evidence["source_jev"]["jev_run_id"], 35842823841)
        self.assertEqual(evidence["source_jev"]["input_scan_id"], "ATTRACTION_SCAN_140")
        self.assertEqual(evidence["source_jev"]["entity_count"], 4)
        self.assertEqual(evidence["source_jev"]["state_fingerprint"], "e2c540f3951363ea7a23")
        self.assertEqual(evidence["source_jev"]["routes"]["ATTRACTION_SCAN_140-F1"], "CAUSAL_DESCENT")
        self.assertTrue(evidence["route_consumed"])
        self.assertEqual(evidence["consumed_routes"], ["CAUSAL_DESCENT", "CAUSAL_DESCENT"])

    def test_supreme_court_reference_case_advances_succession_without_promoting(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        by_id = {item["formation_id"]: item for item in scan["examined_formations"]}
        f1 = by_id["ATTRACTION_SCAN_140-F1"]

        self.assertIn("PUBLIC_SUPREME_COURT_REFERENCE_CASE", f1["economic_tuple"]["post_transfer_receipt_right"])
        self.assertIn("LEGAL_SUCCESSION_SUPPORTED", f1["economic_tuple"]["buyer_receipt_start"])
        self.assertTrue(f1["verdict"].startswith("RETAINED_"))
        self.assertEqual(scan["active_commercial_candidate_promotions"], [])

    def test_first_unprepaid_receipt_and_transfer_event_remain_fail_closed(self):
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        joined = " ".join(evidence["decisive_unknowns_remaining"])
        self.assertIn("auction-completion adjudication service date", joined)
        self.assertIn("first unprepaid rent due date", joined)
        self.assertEqual(
            evidence["formation_status"],
            "RETAINED_RESEARCH_PUBLIC_CAUSAL_DESCENT_EXHAUSTED_BLOCKED_ON_FUTURE_TRANSFER_EVENT_OR_CASE_SPECIFIC_SOURCE_DOCUMENT",
        )
        self.assertFalse(evidence["commercial_promotion"])
        self.assertFalse(evidence["external_contact_performed"])
        self.assertFalse(evidence["bid_authorized"])
        self.assertFalse(evidence["deposit_authorized"])
        self.assertFalse(evidence["purchase_authorized"])

    def test_machine_state_records_route_consumption_and_revalidation_gate(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        followup = state["scan140_f1_causal_descent"]
        self.assertTrue(followup["route_consumed"])
        self.assertEqual(followup["consumed_routes"], ["CAUSAL_DESCENT", "CAUSAL_DESCENT"])
        self.assertEqual(followup["source_exact_head"], "6b57d4c502104e1c6a24f481ddac7aaa52926bdc")
        self.assertEqual(followup["scan141_gate"], "UNBLOCKED_SUBJECT_TO_EXACT_HEAD_CI_AND_LIVE_JEV_NO_NEW_REVERSIBLE_ROUTE_CLASS")
        self.assertEqual(state["active_commercial_candidates"], [])
        self.assertEqual(state["active_transaction_units"], [])
        self.assertEqual(state["first_external_value_flow"], "NOT_PROVEN")


if __name__ == "__main__":
    unittest.main()
