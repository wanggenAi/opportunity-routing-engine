import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_139.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan139_source_bound_receipts_evidence.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


class Scan139SourceBoundReceiptsTests(unittest.TestCase):
    def test_scan139_retains_only_sandu_for_research_and_never_promotes(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        self.assertEqual(scan["scan_id"], "ATTRACTION_SCAN_139")
        self.assertEqual(len(scan["examined_formations"]), 4)
        self.assertEqual(scan["retained_research_formations"], ["ATTRACTION_SCAN_139-F1"])
        self.assertFalse(scan["zero_primary_admissions"])
        self.assertEqual(scan["active_commercial_candidate_promotions"], [])
        self.assertEqual(scan["commercial_outcome"]["active_commercial_candidate_count"], 0)

    def test_sandu_retention_preserves_unknown_buyer_receipt_fields(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        by_id = {item["formation_id"]: item for item in scan["examined_formations"]}
        f1 = by_id["ATTRACTION_SCAN_139-F1"]
        self.assertIn("6_90_PERCENT", f1["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("UNKNOWN", f1["economic_tuple"]["buyer_receipt_start"])
        self.assertIn("UNKNOWN", f1["economic_tuple"]["post_transfer_receipt_right"])
        self.assertTrue(f1["verdict"].startswith("RETAINED_"))

    def test_closed_comparators_keep_independent_hard_failures(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        by_id = {item["formation_id"]: item for item in scan["examined_formations"]}
        self.assertIn("UNKNOWN_PUBLIC_NOTICE", by_id["ATTRACTION_SCAN_139-F2"]["economic_tuple"]["contracted_receipt_amount"])
        self.assertIn("3_46_PERCENT", by_id["ATTRACTION_SCAN_139-F3"]["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("RMB_627210000", by_id["ATTRACTION_SCAN_139-F4"]["economic_tuple"]["acquisition_price"])
        for suffix in ("F2", "F3", "F4"):
            self.assertTrue(by_id[f"ATTRACTION_SCAN_139-{suffix}"]["verdict"].startswith("DEMOTED_"))

    def test_machine_state_preserves_scan139_truth_after_successor_scans(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        historical = state["scan139_source_bound_receipts"]
        self.assertEqual(
            historical["canonical_scan_artifact"],
            "data/research_runs/attraction_scan_139.json",
        )
        self.assertEqual(historical["retained_research_formations"], ["ATTRACTION_SCAN_139-F1"])
        self.assertIn("ATTRACTION_SCAN_139-F1", state["retained_research_formations"])
        self.assertIn("ATTRACTION_SCAN_135-F1", state["retained_research_formations"])
        self.assertGreaterEqual(
            int(state["last_completed_scan_id"].rsplit("_", 1)[-1]),
            139,
        )
        self.assertGreaterEqual(
            int(state["next_scan_id"].rsplit("_", 1)[-1]),
            140,
        )
        self.assertEqual(state["active_commercial_candidates"], [])
        self.assertEqual(state["active_transaction_units"], [])
        self.assertEqual(state["first_external_value_flow"], "NOT_PROVEN")

    def test_evidence_has_four_primary_packets_and_three_diversity_checks(self):
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.assertEqual(evidence["scan_id"], "ATTRACTION_SCAN_139")
        self.assertEqual(len(evidence["evidence_packets"]), 4)
        self.assertEqual(len(evidence["excluded_evidence"]), 3)

    def test_explicit_historical_jev_input_resolves_scan139_after_successor_scans(self):
        from tools.run_jev_research_advisory import resolve_scan_path

        state = json.loads(STATE.read_text(encoding="utf-8"))
        path = resolve_scan_path(
            str(SCAN),
            state,
            research_dir=ROOT / "data" / "research_runs",
        )
        self.assertEqual(path, SCAN)


if __name__ == "__main__":
    unittest.main()
