import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_138.json"
EVIDENCE = ROOT / "data" / "research_runs" / "scan138_diverse_current_receipts_evidence.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


class Scan138DiverseCurrentReceiptsTests(unittest.TestCase):
    def test_scan138_has_four_closed_primary_formations_and_no_promotion(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        self.assertEqual(scan["scan_id"], "ATTRACTION_SCAN_138")
        self.assertEqual(len(scan["examined_formations"]), 4)
        self.assertEqual(scan["retained_research_formations"], [])
        self.assertEqual(scan["high_attraction_beacons"], [])
        self.assertTrue(scan["zero_primary_admissions"])
        self.assertEqual(scan["active_commercial_candidate_promotions"], [])
        self.assertTrue(all(item["verdict"].startswith("DEMOTED_") for item in scan["examined_formations"]))

    def test_scan138_preserves_fail_closed_economic_and_rights_gates(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        by_id = {item["formation_id"]: item for item in scan["examined_formations"]}
        self.assertIn("3_44_PERCENT", by_id["ATTRACTION_SCAN_138-F1"]["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("4_40_PERCENT", by_id["ATTRACTION_SCAN_138-F2"]["economic_tuple"]["receipt_to_entry_economics"])
        self.assertIn("UNKNOWN_NOT_PUBLIC", by_id["ATTRACTION_SCAN_138-F3"]["economic_tuple"]["contracted_receipt_amount"])
        self.assertIn("UNREGISTERED", by_id["ATTRACTION_SCAN_138-F4"]["evidence_class"])
        self.assertIn("UNKNOWN", by_id["ATTRACTION_SCAN_138-F4"]["economic_tuple"]["buyer_receipt_start"])

    def test_rooftop_pv_probe_is_not_promoted(self):
        scan = json.loads(SCAN.read_text(encoding="utf-8"))
        probes = {item["observation"]: item for item in scan["excluded_observations"]}
        heze = probes["CURRENT_HEZE_TIANYING_INDUSTRIAL_ASSET_WITH_ROOFTOP_PV_LEASE"]
        self.assertIn("2030-10-31", heze["reason"])
        self.assertIn("annual rent amount", heze["reason"])
        self.assertEqual(scan["retained_research_formations"], [])

    def test_machine_state_preserves_historical_scan138_without_pinning_global_progress(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        historical = state["scan138_diverse_current_receipts"]
        self.assertEqual(historical["retained_count"], 0)
        self.assertFalse(historical["commercial_promotion"])
        self.assertEqual(historical["next_scan_id"], "ATTRACTION_SCAN_139")
        self.assertIn("ATTRACTION_SCAN_135-F1", state["retained_research_formations"])
        self.assertIn("ATTRACTION_SCAN_136-F1", state["retained_research_formations"])
        self.assertIn("ATTRACTION_SCAN_136-F2", state["retained_research_formations"])
        self.assertEqual(state["active_commercial_candidates"], [])
        self.assertEqual(state["active_transaction_units"], [])
        self.assertEqual(state["first_external_value_flow"], "NOT_PROVEN")

    def test_evidence_has_four_primary_packets_and_one_diversity_probe(self):
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.assertEqual(evidence["scan_id"], "ATTRACTION_SCAN_138")
        self.assertEqual(len(evidence["evidence_packets"]), 4)
        self.assertEqual(len(evidence["excluded_evidence"]), 1)

    def test_explicit_historical_jev_input_resolves_scan138(self):
        from tools.run_jev_research_advisory import resolve_scan_path

        state = json.loads(STATE.read_text(encoding="utf-8"))
        path = resolve_scan_path(str(SCAN), state, research_dir=ROOT / "data" / "research_runs")
        self.assertEqual(path, SCAN)


if __name__ == "__main__":
    unittest.main()
