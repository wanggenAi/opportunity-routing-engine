import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCTRINE = ROOT / "docs" / "LATENT_VALUE_DOCTRINE.md"
FORMAL = ROOT / "docs" / "FORMAL_TRUTH.md"
ACCESS_DOC = ROOT / "docs" / "ACCESS_FEASIBILITY_GATE.md"
RESET_STATE = ROOT / "data" / "commercial_reset_state.json"


class AccessArchitectureLockTests(unittest.TestCase):
    def test_doctrine_separates_value_truth_access_and_visible_surplus(self):
        text = DOCTRINE.read_text(encoding="utf-8")
        self.assertIn("Executable value requires operator-access truth and counterpart-visible surplus", text)
        self.assertIn("COUNTERPARTY VISIBLE SURPLUS", text)
        self.assertIn("OperatorEndowment", text)
        self.assertIn("PUBLIC ACTOR = ACCESSIBLE ACTOR", text)
        self.assertIn("ANALYSIS != SURPLUS", text)
        self.assertIn("constitutional section overrides it", text)

    def test_formal_truth_keeps_access_gate_canonical(self):
        text = FORMAL.read_text(encoding="utf-8")
        self.assertIn("docs/ACCESS_FEASIBILITY_GATE.md", text)
        self.assertIn("Operator access feasibility — LOCKED", text)
        self.assertIn("ACCESS_BLOCKED", text)
        self.assertIn("REACHABILITY GATE", text)
        self.assertIn("Only Reachability **A/B**", text)

    def test_access_doc_requires_backing_and_real_counterparty_gain(self):
        text = ACCESS_DOC.read_text(encoding="utf-8")
        self.assertIn("professional history", text)
        self.assertIn("Backing / legitimacy leverage", text)
        self.assertIn("Counterparty visible surplus", text)
        self.assertIn("PPT / REPORT != HOOK BY DEFAULT", text)
        self.assertIn("LOCAL FIELD PRIOR != UNIVERSAL FACT", text)
        self.assertIn("Reachability Gate", text)
        self.assertIn("can_contact_within_24h", text)
        self.assertIn("can_physically_verify_within_72h", text)
        self.assertIn("Only **A/B**", text)

    def test_clean_slate_has_no_inherited_candidate_access_state(self):
        data = json.loads(RESET_STATE.read_text(encoding="utf-8"))
        self.assertEqual(data["active_commercial_candidates"], [])
        self.assertEqual(data["active_transaction_units"], [])
        self.assertEqual(data["active_parent_formations"], [])
        self.assertEqual(data["inherited_watchlist"], [])
        self.assertEqual(data["historical_case_policy"], "GIT_HISTORY_ONLY_NOT_ACTIVE_INPUT")



if __name__ == "__main__":
    unittest.main()
