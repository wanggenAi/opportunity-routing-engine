import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.structural_commercialization import assess_structural_commercialization, evidence_from_dict


RUN_DIR = Path("data/research_runs/ELDERCARE_STRUCTURE_PROBE_005_2026-09-14")


class EldercareStructureProbe005Tests(unittest.TestCase):
    def _records(self):
        payload = json.loads((RUN_DIR / "evidence.json").read_text(encoding="utf-8"))
        records = tuple(evidence_from_dict(item) for item in payload["evidence"])
        return payload, records

    def test_first_four_dimensions_are_evidenced_compounding_remains_unknown(self):
        payload, records = self._records()
        assessment = assess_structural_commercialization(
            candidate_id=payload["candidate_id"],
            candidate_concept=payload["candidate_concept"],
            source_taxonomy_state="PROMOTION_REVIEW_READY",
            evidence=records,
        )
        self.assertEqual(assessment.commercial_structure_state, "STRUCTURE_VALIDATION_READY")
        self.assertEqual(assessment.missing_dimensions, ("COMPOUNDING",))
        for dimension in (
            "STANDARDIZABILITY",
            "COMPLEMENTARY_ACTOR_STRUCTURE",
            "REGENERATING_EVENT_FLOW",
            "REPEAT_MONETIZATION",
        ):
            self.assertEqual(assessment.dimensions[dimension].state, "EVIDENCED")
        self.assertEqual(assessment.dimensions["COMPOUNDING"].state, "UNKNOWN")
        self.assertEqual(assessment.business_promotion, "NOT_PROMOTED")

    def test_signed_contracts_are_not_settlement_and_digital_efficiency_is_not_compounding(self):
        _, records = self._records()
        paid = [item for item in records if item.dimension == "REPEAT_MONETIZATION"]
        self.assertGreaterEqual(len({item.source_id for item in paid if item.economic_exchange_observed}), 2)
        self.assertTrue(all("NOT_SETTLEMENT" in item.payment_basis for item in paid if item.economic_exchange_observed))
        compounding = [item for item in records if item.dimension == "COMPOUNDING"]
        self.assertGreaterEqual(len(compounding), 2)
        self.assertFalse(any(item.outcome_linked_improvement for item in compounding))

    def test_generic_builder_accepts_reviewed_structural_concept_without_latent_value_candidate(self):
        payload, _ = self._records()
        recurrence = {
            "run_id": "BROAD_DISCOVERY_RUN_002_OBSERVATION_REVIEW_2026-09-14",
            "taxonomy_promotion": "NOT_PROMOTED",
            "business_promotion": "NOT_PROMOTED",
            "assessments": [
                {
                    "candidate_concept": payload["candidate_concept"],
                    "state": "PROMOTION_REVIEW_READY",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            recurrence_path = tmp_path / "recurrence.json"
            output_path = tmp_path / "assessment.json"
            recurrence_path.write_text(json.dumps(recurrence), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_commercial_structure_probe.py",
                    "--recurrence",
                    str(recurrence_path),
                    "--evidence",
                    str(RUN_DIR / "evidence.json"),
                    "--output",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            built = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(built["candidate_class"], "REVIEWED_STRUCTURAL_CONCEPT")
        self.assertEqual(built["candidate_validation_state"], "ONTOLOGY_REVIEW_READY")
        self.assertEqual(built["commercial_structure_state"], "STRUCTURE_VALIDATION_READY")
        self.assertEqual(built["missing_dimensions"], ["COMPOUNDING"])
        self.assertEqual(built["business_promotion"], "NOT_PROMOTED")
        self.assertIn("SIGNED_CONTRACT_NE_SETTLEMENT", built["truth_boundaries"])


if __name__ == "__main__":
    unittest.main()
