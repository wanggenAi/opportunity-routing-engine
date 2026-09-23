import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_136.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan136_current_asset_receipts_evidence.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


class Scan136CurrentAssetReceiptsTests(unittest.TestCase):
    def test_scan136_retains_only_two_research_formations(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        self.assertEqual(scan["scan_id"], "ATTRACTION_SCAN_136")
        self.assertEqual(len(scan["examined_formations"]), 4)
        self.assertEqual(
            scan["retained_research_formations"],
            ["ATTRACTION_SCAN_136-F1", "ATTRACTION_SCAN_136-F2"],
        )
        self.assertEqual(scan["active_commercial_candidate_promotions"], [])
        self.assertFalse(scan["commercial_outcome"]["external_value_flow_proven"])

    def test_f1_and_f2_are_research_only_and_f3_f4_are_hard_closed(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        by_id = {item["formation_id"]: item for item in scan["examined_formations"]}
        self.assertTrue(by_id["ATTRACTION_SCAN_136-F1"]["verdict"].startswith("RETAINED_"))
        self.assertTrue(by_id["ATTRACTION_SCAN_136-F2"]["verdict"].startswith("RETAINED_"))
        self.assertTrue(by_id["ATTRACTION_SCAN_136-F3"]["verdict"].startswith("DEMOTED_"))
        self.assertTrue(by_id["ATTRACTION_SCAN_136-F4"]["verdict"].startswith("DEMOTED_"))
        self.assertIn("7_86_PERCENT", by_id["ATTRACTION_SCAN_136-F1"]["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("16_15_PERCENT", by_id["ATTRACTION_SCAN_136-F2"]["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("1_58_PERCENT", by_id["ATTRACTION_SCAN_136-F3"]["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("3_62", by_id["ATTRACTION_SCAN_136-F4"]["economic_tuple"]["receipt_to_entry_economics"])

    def test_machine_state_tracks_scan136_without_commercial_promotion(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        self.assertEqual(state["last_completed_scan_id"], "ATTRACTION_SCAN_136")
        self.assertEqual(state["next_scan_id"], "ATTRACTION_SCAN_137")
        self.assertIn("ATTRACTION_SCAN_136-F1", state["retained_research_formations"])
        self.assertIn("ATTRACTION_SCAN_136-F2", state["retained_research_formations"])
        self.assertEqual(state["active_commercial_candidates"], [])
        self.assertEqual(state["active_transaction_units"], [])
        self.assertEqual(state["first_external_value_flow"], "NOT_PROVEN")

    def test_evidence_has_four_packets(self):
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.assertEqual(evidence["scan_id"], "ATTRACTION_SCAN_136")
        self.assertEqual(len(evidence["evidence_packets"]), 4)

    def test_current_auto_jev_input_resolves_scan136(self):
        from tools.run_jev_research_advisory import resolve_scan_path

        state = json.loads(STATE.read_text(encoding="utf-8"))
        path = resolve_scan_path("auto", state, research_dir=ROOT / "data" / "research_runs")
        self.assertEqual(path, SCAN)

    def test_resolved_research_formations_preserve_object_schema(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        self.assertTrue(all(isinstance(item, dict) for item in state["resolved_research_formations"]))
        resolved = {item["formation_id"]: item for item in state["resolved_research_formations"]}
        self.assertIn("ATTRACTION_SCAN_136-F3", resolved)
        self.assertIn("ATTRACTION_SCAN_136-F4", resolved)
        self.assertEqual(state["last_resolved_formation_id"], "ATTRACTION_SCAN_136-F4")


if __name__ == "__main__":
    unittest.main()
