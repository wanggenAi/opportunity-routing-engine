import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_137.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan137_current_asset_receipts_evidence.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


class Scan137CurrentAssetReceiptsTests(unittest.TestCase):
    def test_scan137_closes_all_four_without_promotion(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        self.assertEqual(scan["scan_id"], "ATTRACTION_SCAN_137")
        self.assertEqual(len(scan["examined_formations"]), 4)
        self.assertEqual(scan["retained_research_formations"], [])
        self.assertEqual(scan["high_attraction_beacons"], [])
        self.assertTrue(scan["zero_primary_admissions"])
        self.assertEqual(scan["active_commercial_candidate_promotions"], [])
        self.assertFalse(scan["commercial_outcome"]["external_value_flow_proven"])

    def test_hard_fail_reasons_are_fail_closed(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        by_id = {item["formation_id"]: item for item in scan["examined_formations"]}
        self.assertIn("4_87_PERCENT", by_id["ATTRACTION_SCAN_137-F1"]["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("3_33_PERCENT", by_id["ATTRACTION_SCAN_137-F2"]["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("UNKNOWN_NOT_PUBLIC", by_id["ATTRACTION_SCAN_137-F3"]["economic_tuple"]["contracted_receipt_amount"])
        self.assertIn("90_PERCENT_OF_MALL_ACTUAL_RENT", by_id["ATTRACTION_SCAN_137-F4"]["economic_tuple"]["contracted_receipt_amount"])
        for item in by_id.values():
            self.assertTrue(item["verdict"].startswith("DEMOTED_"))

    def test_machine_state_advances_to_scan138_without_touching_prior_retained_research(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        self.assertEqual(state["last_completed_scan_id"], "ATTRACTION_SCAN_137")
        self.assertEqual(state["next_scan_id"], "ATTRACTION_SCAN_138")
        self.assertIn("ATTRACTION_SCAN_135-F1", state["retained_research_formations"])
        self.assertIn("ATTRACTION_SCAN_136-F1", state["retained_research_formations"])
        self.assertIn("ATTRACTION_SCAN_136-F2", state["retained_research_formations"])
        self.assertEqual(state["active_commercial_candidates"], [])
        self.assertEqual(state["active_transaction_units"], [])
        self.assertEqual(state["first_external_value_flow"], "NOT_PROVEN")

    def test_scan137_resolutions_use_canonical_object_schema(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        self.assertTrue(all(isinstance(item, dict) for item in state["resolved_research_formations"]))
        resolved = {item["formation_id"]: item for item in state["resolved_research_formations"]}
        for suffix in ("F1", "F2", "F3", "F4"):
            self.assertIn(f"ATTRACTION_SCAN_137-{suffix}", resolved)
        self.assertEqual(state["last_resolved_formation_id"], "ATTRACTION_SCAN_137-F4")

    def test_evidence_has_four_packets(self):
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.assertEqual(evidence["scan_id"], "ATTRACTION_SCAN_137")
        self.assertEqual(len(evidence["evidence_packets"]), 4)

    def test_current_auto_jev_input_resolves_scan137(self):
        from tools.run_jev_research_advisory import resolve_scan_path

        state = json.loads(STATE.read_text(encoding="utf-8"))
        path = resolve_scan_path("auto", state, research_dir=ROOT / "data" / "research_runs")
        self.assertEqual(path, SCAN)


if __name__ == "__main__":
    unittest.main()
