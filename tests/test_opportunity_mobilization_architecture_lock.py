import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "docs" / "FORMAL_TRUTH.md"
SCORECARD = ROOT / "docs" / "OPPORTUNITY_SCORECARD.md"
MOBILIZATION = ROOT / "docs" / "OPPORTUNITY_MOBILIZATION_GATE.md"


class OpportunityMobilizationArchitectureLockTests(unittest.TestCase):
    def test_mobilization_gate_is_canonical_and_downstream_of_reality_truth(self):
        text = MOBILIZATION.read_text(encoding="utf-8")
        self.assertIn("MOBILIZATION POTENTIAL", text)
        self.assertIn("REALITY VALIDITY", text)
        self.assertIn("Bilateral Pull", text)
        self.assertIn("self_propulsion", text)
        self.assertIn("operator_exit", text)
        self.assertIn("根哥搭桥，不背人过河", text)

    def test_scorecard_requires_mobilization_before_current_stage_priority(self):
        text = SCORECARD.read_text(encoding="utf-8")
        self.assertIn("docs/OPPORTUNITY_MOBILIZATION_GATE.md", text)
        self.assertIn("G7 — Mobilization potential", text)
        self.assertIn("bilateral pull", text)
        self.assertIn("operator exit", text)

    def test_formal_truth_keeps_mobilization_gate_in_canonical_chain(self):
        text = FORMAL.read_text(encoding="utf-8")
        self.assertIn("docs/OPPORTUNITY_MOBILIZATION_GATE.md", text)
        self.assertIn("Mobilization potential — LOCKED", text)
        self.assertIn("REALITY VALIDITY != MOBILIZATION POTENTIAL", text)


if __name__ == "__main__":
    unittest.main()
