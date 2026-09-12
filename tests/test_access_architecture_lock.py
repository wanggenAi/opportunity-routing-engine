import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCTRINE = ROOT / "docs" / "LATENT_VALUE_DOCTRINE.md"
FORMAL = ROOT / "docs" / "FORMAL_TRUTH.md"
ACCESS_DOC = ROOT / "docs" / "ACCESS_FEASIBILITY_GATE.md"
ACCESS_DATA = ROOT / "data" / "cycle002_access_feasibility_2026-09-12.json"


class AccessArchitectureLockTests(unittest.TestCase):
    def test_doctrine_separates_value_truth_from_operator_access(self):
        text = DOCTRINE.read_text(encoding="utf-8")
        self.assertIn("Executable value requires operator-access truth", text)
        self.assertIn("VALUE / EXCHANGE TRUTH", text)
        self.assertIn("OperatorEndowment", text)
        self.assertIn("PUBLIC ACTOR = ACCESSIBLE ACTOR", text)

    def test_formal_truth_requires_access_feasibility(self):
        text = FORMAL.read_text(encoding="utf-8")
        self.assertIn("docs/ACCESS_FEASIBILITY_GATE.md", text)
        self.assertIn("Operator access feasibility — LOCKED", text)
        self.assertIn("COUNTERPARTY VISIBLE SURPLUS", text)
        self.assertIn("ACCESS_BLOCKED", text)

    def test_access_doc_requires_backing_and_real_counterparty_gain(self):
        text = ACCESS_DOC.read_text(encoding="utf-8")
        self.assertIn("professional history", text)
        self.assertIn("Backing / legitimacy leverage", text)
        self.assertIn("Counterparty visible surplus", text)
        self.assertIn("PPT / REPORT != HOOK BY DEFAULT", text)
        self.assertIn("LOCAL FIELD PRIOR != UNIVERSAL FACT", text)

    def test_current_candidate_access_states_are_fail_closed(self):
        data = json.loads(ACCESS_DATA.read_text(encoding="utf-8"))
        by_id = {item["candidate_id"]: item for item in data["assessments"]}
        self.assertEqual(by_id["LV-XZ-001A"]["access_state"], "ACCESS_BLOCKED")
        self.assertEqual(by_id["LV-XZ-003A"]["access_state"], "INTRODUCTION_READY")
        self.assertEqual(by_id["LV-XZ-004"]["access_state"], "ACCESS_BLOCKED")
        self.assertEqual(data["operator_profile_storage"], "RUNTIME_PRIVATE_NOT_COMMITTED")
        self.assertIn("COUNTERPARTY_VISIBLE_SURPLUS", data["principle"])


if __name__ == "__main__":
    unittest.main()
