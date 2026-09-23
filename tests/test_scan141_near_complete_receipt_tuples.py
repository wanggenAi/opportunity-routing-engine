import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_141.json"
STATE = ROOT / "data" / "commercial_reset_state.json"
ROUTE_EVIDENCE = ROOT / "data" / "research_runs" / "scan141_f1_f2_route_consumption_evidence.json"


class Scan141Tests(unittest.TestCase):
    def test_scan141_shape(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        self.assertEqual(scan["scan_id"], "ATTRACTION_SCAN_141")
        self.assertEqual(len(scan["examined_formations"]), 4)
        self.assertEqual(scan["retained_research_formations"], ["ATTRACTION_SCAN_141-F1", "ATTRACTION_SCAN_141-F2"])
        self.assertEqual(scan["active_commercial_candidate_promotions"], [])

    def test_mianyang_and_wuhu_remain_research_only_after_route_consumption(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        by_id = {x["formation_id"]: x for x in scan["examined_formations"]}
        self.assertIn("8_43_PERCENT", by_id["ATTRACTION_SCAN_141-F1"]["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("UNKNOWN", by_id["ATTRACTION_SCAN_141-F1"]["economic_tuple"]["buyer_receipt_end"])
        self.assertIn("PUBLIC_CAUSAL_DESCENT_EXHAUSTED", by_id["ATTRACTION_SCAN_141-F1"]["verdict"])
        self.assertIn("UNKNOWN", by_id["ATTRACTION_SCAN_141-F2"]["economic_tuple"]["buyer_receipt_start"])
        self.assertIn("EXACT_INCUMBENT_PREFLIGHT_EXHAUSTED", by_id["ATTRACTION_SCAN_141-F2"]["verdict"])
        self.assertIn("PRIORITY_RIGHT_HOLDER_ROLE_NOT_BOUND", by_id["ATTRACTION_SCAN_141-F2"]["economic_tuple"]["counterparty"])
        self.assertTrue(any("priority purchaser" in item.lower() for item in by_id["ATTRACTION_SCAN_141-F2"]["exact_disconfirmation"]))

    def test_comparators_demote_on_distinct_gates(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        by_id = {x["formation_id"]: x for x in scan["examined_formations"]}
        self.assertIn("4_16_PERCENT", by_id["ATTRACTION_SCAN_141-F3"]["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("UNKNOWN_CURRENT_CHANGE_SALE_PRICE", by_id["ATTRACTION_SCAN_141-F4"]["economic_tuple"]["acquisition_price"])
        self.assertTrue(by_id["ATTRACTION_SCAN_141-F3"]["verdict"].startswith("DEMOTED_"))
        self.assertTrue(by_id["ATTRACTION_SCAN_141-F4"]["verdict"].startswith("DEMOTED_"))

    def test_route_consumption_records_exact_jev_routes_and_no_promotion(self):
        evidence = json.loads(ROUTE_EVIDENCE.read_text(encoding="utf-8"))
        routes = {x["formation_id"]: x for x in evidence["route_consumption"]}
        self.assertEqual(routes["ATTRACTION_SCAN_141-F1"]["effective_research_route"], "CAUSAL_DESCENT")
        self.assertEqual(routes["ATTRACTION_SCAN_141-F2"]["effective_research_route"], "EXACT_INCUMBENT_PREFLIGHT")
        self.assertIn("EXHAUSTED", routes["ATTRACTION_SCAN_141-F1"]["resolution"])
        self.assertIn("EXHAUSTED", routes["ATTRACTION_SCAN_141-F2"]["resolution"])
        self.assertEqual(evidence["active_commercial_candidate_count"], 0)
        self.assertEqual(evidence["first_external_value_flow"], "NOT_PROVEN")
        self.assertFalse(evidence["external_contact_performed"])

    def test_machine_state_points_to_scan141_and_records_consumed_routes(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        checkpoint = state["scan141_near_complete_receipt_tuples"]
        current_no = int(state["last_completed_scan_id"].removeprefix("ATTRACTION_SCAN_"))
        self.assertGreater(current_no, 141)
        self.assertEqual(
            state["last_completed_scan_file"],
            f"data/research_runs/attraction_scan_{current_no}.json",
        )
        self.assertEqual(state["next_scan_id"], f"ATTRACTION_SCAN_{current_no + 1}")
        self.assertEqual(checkpoint["jev_routes"]["ATTRACTION_SCAN_141-F1"], "CAUSAL_DESCENT")
        self.assertEqual(checkpoint["jev_routes"]["ATTRACTION_SCAN_141-F2"], "EXACT_INCUMBENT_PREFLIGHT")
        self.assertIn("CONSUMED", checkpoint["jev_route_status"])
        self.assertEqual(state["active_commercial_candidates"], [])
        self.assertEqual(state["active_transaction_units"], [])
        self.assertEqual(state["first_external_value_flow"], "NOT_PROVEN")

    def test_auto_jev_advances_beyond_historical_scan141(self):
        from tools.run_jev_research_advisory import resolve_scan_path

        state = json.loads(STATE.read_text(encoding="utf-8"))
        path = resolve_scan_path("auto", state, research_dir=ROOT / "data" / "research_runs")
        expected = ROOT / state["last_completed_scan_file"]
        self.assertEqual(path, expected)
        self.assertNotEqual(path, SCAN)


if __name__ == "__main__":
    unittest.main()
