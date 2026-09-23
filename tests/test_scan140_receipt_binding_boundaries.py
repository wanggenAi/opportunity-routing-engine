import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_140.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan140_receipt_binding_boundaries_evidence.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


class Scan140ReceiptBindingBoundaryTests(unittest.TestCase):
    def test_scan140_retains_only_weiyuan_and_never_promotes(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        self.assertEqual(scan["scan_id"], "ATTRACTION_SCAN_140")
        self.assertEqual(len(scan["examined_formations"]), 4)
        self.assertEqual(scan["retained_research_formations"], ["ATTRACTION_SCAN_140-F1"])
        self.assertFalse(scan["zero_primary_admissions"])
        self.assertEqual(scan["active_commercial_candidate_promotions"], [])
        self.assertEqual(scan["commercial_outcome"]["active_commercial_candidate_count"], 0)

    def test_weiyuan_preserves_fail_closed_receipt_boundary_after_route_followup(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        by_id = {item["formation_id"]: item for item in scan["examined_formations"]}
        f1 = by_id["ATTRACTION_SCAN_140-F1"]
        self.assertIn("16_15_PERCENT", f1["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("UNKNOWN", f1["economic_tuple"]["buyer_receipt_start"])
        self.assertIn(
            "PUBLIC_SUPREME_COURT_REFERENCE_CASE",
            f1["economic_tuple"]["post_transfer_receipt_right"],
        )
        self.assertIn(
            "PREPAID_RENT_APPORTIONMENT_REMAINS_UNBOUND",
            f1["economic_tuple"]["post_transfer_receipt_right"],
        )
        self.assertTrue(f1["verdict"].startswith("RETAINED_"))

    def test_three_comparators_close_on_independent_receipt_binding_failures(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        by_id = {item["formation_id"]: item for item in scan["examined_formations"]}
        self.assertIn("25_PERCENT", by_id["ATTRACTION_SCAN_140-F2"]["economic_tuple"]["acquisition_price"])
        self.assertIn("UNKNOWN", by_id["ATTRACTION_SCAN_140-F3"]["economic_tuple"]["contracted_receipt_amount"])
        self.assertIn("FULLY_PREPAID", by_id["ATTRACTION_SCAN_140-F4"]["economic_tuple"]["unprepaid_receipt_status"])
        for suffix in ("F2", "F3", "F4"):
            self.assertTrue(by_id[f"ATTRACTION_SCAN_140-{suffix}"]["verdict"].startswith("DEMOTED_"))

    def test_machine_state_preserves_scan140_historical_checkpoint(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        checkpoint = state["scan140_receipt_binding_boundaries"]
        self.assertEqual(checkpoint["next_scan_id"], "ATTRACTION_SCAN_141")
        self.assertEqual(checkpoint["retained_research_formations"], ["ATTRACTION_SCAN_140-F1"])
        self.assertEqual(
            checkpoint["authoritative_closures"],
            [
                "ATTRACTION_SCAN_140-F2",
                "ATTRACTION_SCAN_140-F3",
                "ATTRACTION_SCAN_140-F4",
            ],
        )
        self.assertEqual(
            checkpoint["exact_head_validation_status"],
            "FINAL_EXACT_HEAD_REPOSITORY_CI_AND_LIVE_JEV_SUCCESS",
        )
        self.assertEqual(checkpoint["merged_pr"], 450)
        self.assertEqual(
            checkpoint["merged_main_sha"],
            "8a55703f92fbd52b53c41947b04d9fb3bd2b48e4",
        )
        self.assertIn("ATTRACTION_SCAN_140-F1", state["retained_research_formations"])
        self.assertIn("ATTRACTION_SCAN_141-F1", state["retained_research_formations"])
        resolved = {item["formation_id"]: item["verdict"] for item in state["resolved_research_formations"]}
        self.assertTrue(resolved["ATTRACTION_SCAN_140-F1"].startswith("CLOSED_STRATEGIC_QUARANTINE_"))
        self.assertTrue(resolved["ATTRACTION_SCAN_141-F1"].startswith("CLOSED_STRATEGIC_QUARANTINE_"))
        self.assertTrue(resolved["ATTRACTION_SCAN_141-F2"].startswith("CLOSED_STRATEGIC_QUARANTINE_"))
        self.assertEqual(state["last_completed_scan_id"], "ATTRACTION_SCAN_141")
        self.assertEqual(state["next_scan_id"], "ATTRACTION_SCAN_142")
        incident = state["strategic_drift_incident"]
        self.assertEqual(incident["quarantined_pr"], 451)
        self.assertEqual(incident["quarantined_pr_state"], "MERGED_AUDIT_ONLY")
        self.assertEqual(incident["quarantined_scan_id"], "ATTRACTION_SCAN_141")
        self.assertTrue(incident["do_not_use_quarantined_scan141_as_strategy"])
        self.assertEqual(state["active_commercial_candidates"], [])
        self.assertEqual(state["active_transaction_units"], [])
        self.assertEqual(state["first_external_value_flow"], "NOT_PROVEN")

    def test_evidence_has_four_primary_packets_and_three_diversity_checks(self):
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.assertEqual(evidence["scan_id"], "ATTRACTION_SCAN_140")
        self.assertEqual(len(evidence["evidence_packets"]), 4)
        self.assertEqual(len(evidence["excluded_evidence"]), 3)

    def test_auto_jev_has_advanced_beyond_scan140(self):
        from tools.run_jev_research_advisory import resolve_scan_path

        state = json.loads(STATE.read_text(encoding="utf-8"))
        path = resolve_scan_path("auto", state, research_dir=ROOT / "data" / "research_runs")
        self.assertNotEqual(path, SCAN)


if __name__ == "__main__":
    unittest.main()
