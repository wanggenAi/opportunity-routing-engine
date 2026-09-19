import unittest

from src.structural_commercialization import assess_structural_commercialization, evidence_from_dict, summarize_assessment


def _records():
    raw = [
        {"evidence_id":"std-1","dimension":"STANDARDIZABILITY","source_id":"s1","source_url":"https://example.test/1","claim":"Synthetic reusable process.","geography":"CN","observed_at":"2026-09-18","direct_process_specification":True},
        {"evidence_id":"std-2","dimension":"STANDARDIZABILITY","source_id":"s2","source_url":"https://example.test/2","claim":"Independent synthetic process evidence.","geography":"CN","observed_at":"2026-09-19"},
        {"evidence_id":"actor-1","dimension":"COMPLEMENTARY_ACTOR_STRUCTURE","source_id":"s3","source_url":"https://example.test/3","claim":"Synthetic actor roles.","geography":"CN","observed_at":"2026-09-18","actor_roles":["RESOURCE_OWNER","OPERATOR"]},
        {"evidence_id":"actor-2","dimension":"COMPLEMENTARY_ACTOR_STRUCTURE","source_id":"s4","source_url":"https://example.test/4","claim":"Synthetic beneficiary role.","geography":"CN","observed_at":"2026-09-19","actor_roles":["BENEFICIARY"]},
        {"evidence_id":"event-1","dimension":"REGENERATING_EVENT_FLOW","source_id":"s5","source_url":"https://example.test/5","claim":"Synthetic recurring event one.","geography":"CN","observed_at":"2026-09-18","event_types":["EVENT_A"]},
        {"evidence_id":"event-2","dimension":"REGENERATING_EVENT_FLOW","source_id":"s6","source_url":"https://example.test/6","claim":"Synthetic recurring event two.","geography":"CN","observed_at":"2026-09-19","event_types":["EVENT_B"]},
        {"evidence_id":"pay-1","dimension":"REPEAT_MONETIZATION","source_id":"s7","source_url":"https://example.test/7","claim":"Synthetic accepted payment basis.","geography":"CN","observed_at":"2026-09-18","payment_basis":"accepted fee","economic_exchange_observed":True},
        {"evidence_id":"pay-2","dimension":"REPEAT_MONETIZATION","source_id":"s8","source_url":"https://example.test/8","claim":"Independent synthetic accepted payment basis.","geography":"CN","observed_at":"2026-09-19","payment_basis":"accepted transaction fee","economic_exchange_observed":True},
    ]
    return tuple(evidence_from_dict(item) for item in raw)


class StructuralCommercializationTests(unittest.TestCase):
    def test_synthetic_evidence_reaches_structure_validation_ready_only(self):
        records = _records()
        assessment = assess_structural_commercialization(
            candidate_id="SYNTHETIC", candidate_concept="SYNTHETIC_STRUCTURE",
            source_taxonomy_state="PROMOTION_REVIEW_READY", evidence=records,
        )
        self.assertEqual(assessment.commercial_structure_state, "STRUCTURE_VALIDATION_READY")
        self.assertEqual(assessment.missing_dimensions, ("COMPOUNDING",))
        self.assertEqual(assessment.business_promotion, "NOT_PROMOTED")

    def test_digital_platform_claim_is_not_needed_and_compounding_stays_unknown(self):
        records = _records()
        assessment = assess_structural_commercialization(
            candidate_id="SYNTHETIC", candidate_concept="SYNTHETIC_STRUCTURE",
            source_taxonomy_state="PROMOTION_REVIEW_READY", evidence=records,
        )
        self.assertEqual(assessment.dimensions["COMPOUNDING"].state, "UNKNOWN")
        self.assertFalse(any(item.outcome_linked_improvement for item in records))

    def test_repeat_monetization_requires_two_independent_payment_sources(self):
        records = tuple(item for item in _records() if item.evidence_id != "pay-2")
        assessment = assess_structural_commercialization(
            candidate_id="SYNTHETIC", candidate_concept="SYNTHETIC_STRUCTURE",
            source_taxonomy_state="PROMOTION_REVIEW_READY", evidence=records,
        )
        self.assertEqual(assessment.dimensions["REPEAT_MONETIZATION"].state, "UNKNOWN")
        self.assertEqual(assessment.commercial_structure_state, "STRUCTURE_HYPOTHESIS")

    def test_summary_has_no_commercial_score_or_route_promotion(self):
        records = _records()
        assessment = assess_structural_commercialization(
            candidate_id="SYNTHETIC", candidate_concept="SYNTHETIC_STRUCTURE",
            source_taxonomy_state="PROMOTION_REVIEW_READY", evidence=records,
        )
        summary = summarize_assessment(assessment, records)
        rendered = str(summary)
        self.assertNotIn("opportunity_score", rendered)
        self.assertNotIn("commercial_score", rendered)
        self.assertNotIn("route_testable", rendered)
        self.assertEqual(summary["business_promotion"], "NOT_PROMOTED")
        self.assertIn("STRUCTURE_VALIDATION_READY_NE_ROUTE_TESTABLE", summary["governing_invariants"])


if __name__ == "__main__":
    unittest.main()
