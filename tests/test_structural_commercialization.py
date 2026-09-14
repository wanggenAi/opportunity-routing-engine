import json
import unittest
from pathlib import Path

from src.latent_value_discovery import validate_candidate_record
from src.structural_commercialization import (
    assess_structural_commercialization,
    evidence_from_dict,
    summarize_assessment,
)


RUN_DIR = Path("data/research_runs/COMMERCIAL_STRUCTURE_PROBE_003_2026-09-14")


class StructuralCommercializationTests(unittest.TestCase):
    def _records(self):
        payload = json.loads((RUN_DIR / "evidence.json").read_text(encoding="utf-8"))
        return payload, tuple(evidence_from_dict(item) for item in payload["evidence"])

    def test_candidate_is_latent_value_validation_ready_but_not_business_truth(self):
        candidate = json.loads((RUN_DIR / "candidate.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_candidate_record(candidate), [])
        self.assertEqual(candidate["source_mode"], "LATENT_VALUE_DISCOVERY")
        self.assertNotIn("business_promotion", candidate)
        self.assertNotIn("opportunity_score", candidate)

    def test_real_evidence_reaches_structure_validation_ready_only(self):
        payload, records = self._records()
        assessment = assess_structural_commercialization(
            candidate_id="LV-STRUCTURE-IDLE-ASSET-REPURPOSING-001",
            candidate_concept=payload["candidate_concept"],
            source_taxonomy_state="PROMOTION_REVIEW_READY",
            evidence=records,
        )
        self.assertEqual(assessment.commercial_structure_state, "STRUCTURE_VALIDATION_READY")
        self.assertEqual(assessment.missing_dimensions, ("COMPOUNDING",))
        self.assertEqual(assessment.business_promotion, "NOT_PROMOTED")
        for dimension in (
            "STANDARDIZABILITY",
            "COMPLEMENTARY_ACTOR_STRUCTURE",
            "REGENERATING_EVENT_FLOW",
            "REPEAT_MONETIZATION",
        ):
            self.assertEqual(assessment.dimensions[dimension].state, "EVIDENCED")
        self.assertEqual(assessment.dimensions["COMPOUNDING"].state, "UNKNOWN")

    def test_digital_platform_claim_alone_cannot_prove_compounding(self):
        payload, records = self._records()
        assessment = assess_structural_commercialization(
            candidate_id="x",
            candidate_concept=payload["candidate_concept"],
            source_taxonomy_state="PROMOTION_REVIEW_READY",
            evidence=records,
        )
        self.assertEqual(assessment.dimensions["COMPOUNDING"].state, "UNKNOWN")
        self.assertFalse(any(item.outcome_linked_improvement for item in records))

    def test_repeat_monetization_requires_two_independent_payment_sources(self):
        _, records = self._records()
        reduced = tuple(item for item in records if item.evidence_id != "money-hunan-framework-fee" and item.evidence_id != "money-nanjing-market-transactions")
        assessment = assess_structural_commercialization(
            candidate_id="x",
            candidate_concept="IDLE_ASSET_SCENARIO_REPURPOSING",
            source_taxonomy_state="PROMOTION_REVIEW_READY",
            evidence=reduced,
        )
        self.assertEqual(assessment.dimensions["REPEAT_MONETIZATION"].state, "UNKNOWN")
        self.assertEqual(assessment.commercial_structure_state, "STRUCTURE_HYPOTHESIS")

    def test_summary_has_no_commercial_score_or_route_promotion(self):
        payload, records = self._records()
        assessment = assess_structural_commercialization(
            candidate_id="x",
            candidate_concept=payload["candidate_concept"],
            source_taxonomy_state="PROMOTION_REVIEW_READY",
            evidence=records,
        )
        summary = summarize_assessment(assessment, records)
        rendered = json.dumps(summary, ensure_ascii=False)
        self.assertNotIn("opportunity_score", rendered)
        self.assertNotIn("commercial_score", rendered)
        self.assertNotIn("ROUTE_TESTABLE", rendered)
        self.assertEqual(summary["business_promotion"], "NOT_PROMOTED")


if __name__ == "__main__":
    unittest.main()
