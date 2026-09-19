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

    def test_legacy_validation_ready_claims_are_requalified_under_structural_friction_gate(self):
        ready = [
            candidate
            for candidate in self.candidates
            if candidate.get("claimed_discovery_state") == "VALIDATION_READY"
        ]
        self.assertGreaterEqual(len(ready), 1)
        for candidate in ready:
            errors = validate_candidate_record(candidate)
            self.assertIn("missing:surface_phenomenon_or_friction", errors, candidate["candidate_id"])
            self.assertIn("missing:latent_outcome_hypothesis", errors, candidate["candidate_id"])
            self.assertIn("missing:structural_friction_hypothesis", errors, candidate["candidate_id"])
            self.assertIn("structural_friction_not_evidenced", errors, candidate["candidate_id"])
            self.assertIn("missing:alternative_explanations", errors, candidate["candidate_id"])
            self.assertIn(
                "missing:evidence_kind:STRUCTURAL_FRICTION",
                errors,
                candidate["candidate_id"],
            )
            self.assertIn("missing:causal_descent_record_id", errors, candidate["candidate_id"])
            self.assertIn("missing:causal_stop_reason", errors, candidate["candidate_id"])
            self.assertIn("missing:connection_pressure_hypothesis", errors, candidate["candidate_id"])
            self.assertIn("missing:observed_missing_edge", errors, candidate["candidate_id"])
            self.assertIn("missing:latent_connection_hypothesis", errors, candidate["candidate_id"])
            self.assertIn(
                "missing:evidence_kind:CONNECTION_PRESSURE",
                errors,
                candidate["candidate_id"],
            )
            self.assertIn(
                "missing:evidence_kind:MISSING_EDGE",
                errors,
                candidate["candidate_id"],
            )

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
            # This artifact predates the structural-friction constitution. Preserve its
            # historical declarations, but the current validator must add the new causal
            # evidence dimension rather than silently grandfathering old candidates.
            self.assertTrue(declared.issubset(observed_missing), candidate["candidate_id"])
            self.assertIn("STRUCTURAL_FRICTION", observed_missing, candidate["candidate_id"])
            self.assertIn("CONNECTION_PRESSURE", observed_missing, candidate["candidate_id"])
            self.assertIn("MISSING_EDGE", observed_missing, candidate["candidate_id"])

    def test_candidate_ids_are_unique(self):
        ids = [candidate["candidate_id"] for candidate in self.candidates]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
