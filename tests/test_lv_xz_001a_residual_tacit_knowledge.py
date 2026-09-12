import json
import unittest
from pathlib import Path

from src.latent_value_discovery import validate_candidate_record


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data" / "lv_xz_001a_residual_tacit_knowledge_2026-09-12.json"


class LVXZ001AResidualTacitKnowledgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_parent_thesis_is_narrowed_to_residual_knowledge(self):
        value = self.record["hidden_or_underrecognized_value"].lower()
        rationale = self.record["why_value_is_not_recognized_or_realized"].lower()
        self.assertIn("residual", value)
        self.assertIn("current standards/training", rationale)
        self.assertIn("no hidden asset should be presumed", rationale)

    def test_counterevidence_is_preserved(self):
        counterevidence = "\n".join(self.record["counterevidence"]).lower()
        self.assertIn("already transmit", counterevidence)
        self.assertIn("may already capture", counterevidence)

    def test_candidate_remains_blocked_on_stranding_evidence(self):
        self.assertEqual(self.record["claimed_discovery_state"], "COMPLEMENTARITY_HYPOTHESIS")
        self.assertEqual(self.record["known_missing_evidence"], ["STRANDING_BARRIER"])
        errors = validate_candidate_record(self.record)
        self.assertIn("missing:evidence_kind:STRANDING_BARRIER", errors)
        self.assertNotIn("missing:evidence_kind:ORIGIN_STATE", errors)
        self.assertNotIn("missing:evidence_kind:COMPLEMENTARY_STATE", errors)

    def test_validation_is_measurement_first(self):
        validation = self.record["cheapest_decisive_validation"].lower()
        self.assertIn("baseline", validation)
        self.assertIn("improvement", validation)
        self.assertIn("rights", validation)


if __name__ == "__main__":
    unittest.main()
