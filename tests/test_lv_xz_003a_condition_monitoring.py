import json
import unittest
from pathlib import Path

from src.latent_value_discovery import validate_candidate_record


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data" / "lv_xz_003a_condition_monitoring_bundle_2026-09-12.json"


class LVXZ003AConditionMonitoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_specific_bundle_is_not_overpromoted(self):
        self.assertEqual(
            self.record["claimed_discovery_state"],
            "COMPLEMENTARITY_HYPOTHESIS",
        )
        self.assertEqual(self.record["known_missing_evidence"], ["STRANDING_BARRIER"])

    def test_research_capability_does_not_satisfy_stranding_barrier(self):
        errors = validate_candidate_record(self.record)
        self.assertIn("missing:evidence_kind:STRANDING_BARRIER", errors)
        self.assertNotIn("missing:evidence_kind:ORIGIN_STATE", errors)
        self.assertNotIn("missing:evidence_kind:COMPLEMENTARY_STATE", errors)

    def test_transferability_is_explicitly_unknown(self):
        unknowns = "\n".join(self.record["explicit_unknowns"])
        self.assertIn("transferable", unknowns)
        self.assertIn("combined", unknowns)
        self.assertIn("willingness", unknowns)

    def test_bundle_is_not_explicit_demand_execution(self):
        self.assertEqual(self.record["source_mode"], "LATENT_VALUE_DISCOVERY")


if __name__ == "__main__":
    unittest.main()
