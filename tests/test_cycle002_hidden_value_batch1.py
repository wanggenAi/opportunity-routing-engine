import json
import unittest
from pathlib import Path

from src.latent_value_discovery import validate_candidate_record


ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "data" / "cycle002_hidden_value_batch1_2026-09-12.json"


class Cycle002HiddenValueBatch1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(BATCH.read_text(encoding="utf-8"))
        cls.candidates = cls.payload["candidates"]

    def test_batch_is_not_empty_and_has_no_explicit_demand_candidates(self):
        self.assertGreaterEqual(len(self.candidates), 5)
        for candidate in self.candidates:
            self.assertNotEqual(candidate.get("source_mode"), "EXPLICIT_DEMAND")

    def test_validation_ready_claims_have_all_required_evidence_dimensions(self):
        ready = [
            candidate
            for candidate in self.candidates
            if candidate.get("claimed_discovery_state") == "VALIDATION_READY"
        ]
        self.assertGreaterEqual(len(ready), 1)
        for candidate in ready:
            self.assertEqual(validate_candidate_record(candidate), [], candidate["candidate_id"])
            self.assertEqual(candidate.get("known_missing_evidence"), [])

    def test_lower_maturity_candidates_fail_closed_on_declared_missing_evidence(self):
        lower = [
            candidate
            for candidate in self.candidates
            if candidate.get("claimed_discovery_state") != "VALIDATION_READY"
        ]
        self.assertGreaterEqual(len(lower), 1)
        for candidate in lower:
            errors = validate_candidate_record(candidate)
            declared = set(candidate.get("known_missing_evidence", []))
            observed_missing = {
                error.removeprefix("missing:evidence_kind:")
                for error in errors
                if error.startswith("missing:evidence_kind:")
            }
            self.assertEqual(observed_missing, declared, candidate["candidate_id"])

    def test_candidate_ids_are_unique(self):
        ids = [candidate["candidate_id"] for candidate in self.candidates]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
