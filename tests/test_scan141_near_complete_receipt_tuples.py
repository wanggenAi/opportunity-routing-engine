import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_141.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

class Scan141Tests(unittest.TestCase):
    def test_scan141_shape(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        self.assertEqual(scan["scan_id"], "ATTRACTION_SCAN_141")
        self.assertEqual(len(scan["examined_formations"]), 4)
        self.assertEqual(scan["retained_research_formations"], ["ATTRACTION_SCAN_141-F1", "ATTRACTION_SCAN_141-F2"])
        self.assertEqual(scan["active_commercial_candidate_promotions"], [])

    def test_mianyang_and_wuhu_remain_research_only(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        by_id = {x["formation_id"]: x for x in scan["examined_formations"]}
        self.assertIn("8_43_PERCENT", by_id["ATTRACTION_SCAN_141-F1"]["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("UNKNOWN", by_id["ATTRACTION_SCAN_141-F1"]["economic_tuple"]["buyer_receipt_end"])
        self.assertIn("UNKNOWN", by_id["ATTRACTION_SCAN_141-F2"]["economic_tuple"]["buyer_receipt_start"])
        self.assertTrue(by_id["ATTRACTION_SCAN_141-F1"]["verdict"].startswith("RETAINED_"))
        self.assertTrue(by_id["ATTRACTION_SCAN_141-F2"]["verdict"].startswith("RETAINED_"))

    def test_comparators_demote_on_distinct_gates(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        by_id = {x["formation_id"]: x for x in scan["examined_formations"]}
        self.assertIn("4_16_PERCENT", by_id["ATTRACTION_SCAN_141-F3"]["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("UNKNOWN_CURRENT_CHANGE_SALE_PRICE", by_id["ATTRACTION_SCAN_141-F4"]["economic_tuple"]["acquisition_price"])
        self.assertTrue(by_id["ATTRACTION_SCAN_141-F3"]["verdict"].startswith("DEMOTED_"))
        self.assertTrue(by_id["ATTRACTION_SCAN_141-F4"]["verdict"].startswith("DEMOTED_"))

    def test_auto_jev_resolves_scan141(self):
        from tools.run_jev_research_advisory import resolve_scan_path
        state = json.loads(STATE.read_text(encoding="utf-8"))
        path = resolve_scan_path("auto", state, research_dir=ROOT / "data" / "research_runs")
        self.assertEqual(path, SCAN)

if __name__ == "__main__":
    unittest.main()
