import json
import unittest
from pathlib import Path

from src.jev_research_advisory import build_research_states
from tools.run_jev_research_advisory import resolve_scan_path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_135.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan135_single_asset_cashflow_evidence.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class Scan135SingleAssetCashflowTests(unittest.TestCase):
    def test_scan135_explicit_jev_input_preserves_historical_research_state(self):
        state = load(STATE)
        path = resolve_scan_path(str(SCAN), state, research_dir=ROOT / "data" / "research_runs")
        self.assertEqual(path, SCAN)
        scan = load(SCAN)
        states = build_research_states(scan=scan, commercial_state=state, max_entities=8)
        self.assertEqual(len(states), 4)
        rows = {row["formation"]["formation_id"]: row for row in states}
        self.assertFalse(rows["ATTRACTION_SCAN_135-F1"]["authoritative_engine_context"]["existing_closure_authoritative"])
        self.assertTrue(rows["ATTRACTION_SCAN_135-F1"]["authoritative_engine_context"]["already_retained_for_research"])
        for formation_id in ("ATTRACTION_SCAN_135-F2", "ATTRACTION_SCAN_135-F3", "ATTRACTION_SCAN_135-F4"):
            self.assertTrue(rows[formation_id]["authoritative_engine_context"]["existing_closure_authoritative"])

    def test_retains_f1_for_research_only_and_never_promotes(self):
        scan = load(SCAN)
        self.assertEqual(scan["status"], "COMPLETE")
        self.assertEqual(scan["retained_research_formations"], ["ATTRACTION_SCAN_135-F1"])
        self.assertEqual(scan["active_commercial_candidate_promotions"], [])
        self.assertEqual(len(scan["high_attraction_beacons"]), 1)
        self.assertFalse(scan["high_attraction_beacons"][0]["commercial_candidate"])
        self.assertTrue(scan["examined_formations"][0]["verdict"].startswith("RETAINED_FOR_CHEAP_FALSIFICATION"))
        self.assertTrue(all(row["verdict"].startswith("DEMOTED_") for row in scan["examined_formations"][1:]))
        self.assertEqual(scan["first_external_value_flow"], "NOT_PROVEN")

    def test_f1_clears_public_cashflow_threshold_but_keeps_diligence_unknowns_open(self):
        scan = load(SCAN)
        f1 = scan["examined_formations"][0]
        econ = f1["economic_tuple"]
        self.assertEqual(econ["acquisition_price"], "RMB_650304_CURRENT_CHANGE_SALE_FLOOR")
        self.assertEqual(econ["contracted_receipt_amount"], "RMB_3000_PER_MONTH")
        self.assertEqual(econ["buyer_receipt_end"], "LEASE_END_2030-11-20")
        self.assertTrue(econ["post_transfer_receipt_right"].startswith("PASS_"))
        self.assertIn("5_54_PERCENT", econ["receipt_to_entry_economics"])
        self.assertTrue(econ["unprepaid_receipt_status"].startswith("PARTIAL_PASS"))
        self.assertGreaterEqual(len(f1["decisive_unknowns"]), 4)
        self.assertTrue(f1["attraction_brief"]["action_gate"].startswith("RESEARCH_OPEN"))

    def test_comparators_fail_independent_hard_gates(self):
        scan = load(SCAN)
        f2, f3, f4 = scan["examined_formations"][1:]
        self.assertIn("2027-02-28", f2["evidence_summary"])
        self.assertTrue(f2["economic_tuple"]["unprepaid_receipt_status"].startswith("FAIL_"))
        self.assertEqual(f3["economic_tuple"]["buyer_receipt_end"], "LEASE_END_2027-07-19")
        self.assertTrue(f4["economic_tuple"]["contracted_receipt_amount"].startswith("NOT_PUBLIC"))
        self.assertTrue(f4["economic_tuple"]["receipt_to_entry_economics"].startswith("UNKNOWN"))

    def test_machine_truth_keeps_research_retention_separate_from_commercial_state(self):
        state = load(STATE)
        evidence = load(EVIDENCE)
        self.assertEqual(evidence["scan_id"], "ATTRACTION_SCAN_135")
        self.assertEqual(len(evidence["evidence_packets"]), 4)
        self.assertIn("ONE_RETAINED_RESEARCH_FORMATION", evidence["scan_conclusion"])
        self.assertIn("ATTRACTION_SCAN_135-F1", state["retained_research_formations"])
        self.assertEqual(state["active_commercial_candidates"], [])
        self.assertEqual(state["active_transaction_units"], [])
        self.assertIn("next_scan_id", state)
        self.assertFalse(state["scan135_single_asset_cashflow"]["commercial_promotion"])
        self.assertFalse(state["scan135_single_asset_cashflow"]["bid_authorized"])
        self.assertFalse(state["scan135_single_asset_cashflow"]["deposit_authorized"])
        self.assertFalse(state["scan135_single_asset_cashflow"]["purchase_authorized"])


if __name__ == "__main__":
    unittest.main()
