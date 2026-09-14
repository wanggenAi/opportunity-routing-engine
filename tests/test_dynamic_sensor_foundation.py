import unittest

from src.emergent_taxonomy import assess_emergent_concept
from src.geographic_focus import classify_signal_focus
from src.semantic_kernel import SemanticObservation, validate_open_concept_namespace


class DynamicSensorFoundationTests(unittest.TestCase):
    def _obs(self, idx, concept, source, actor, day):
        return SemanticObservation(
            observation_id=f"obs-{idx}",
            primitive="FRICTION",
            concept=concept,
            source_id=source,
            observed_at=f"2026-09-{day:02d}T10:00:00+08:00",
            evidence_refs=(f"ref-{idx}",),
            actor_id=actor,
            geography="CN",
        )

    def test_open_namespace_accepts_new_concept_without_enum_change(self):
        concept = "AI_AGENT_PERMISSION_FRICTION_2031"
        items = validate_open_concept_namespace(
            [self._obs(1, concept, "source-a", "actor-a", 1)]
        )
        self.assertEqual(items[0].concept, concept)

    def test_emergent_concept_requires_repetition_diversity_and_time(self):
        concept = "NEW_SOCIAL_RESOURCE_PATTERN"
        observations = [
            self._obs(1, concept, "source-a", "actor-a", 1),
            self._obs(2, concept, "source-a", "actor-b", 1),
            self._obs(3, concept, "source-b", "actor-a", 2),
            self._obs(4, concept, "source-b", "actor-b", 2),
        ]
        result = assess_emergent_concept(concept, observations)
        self.assertEqual(result.state, "PROMOTION_REVIEW_READY")
        self.assertEqual(result.source_count, 2)
        self.assertEqual(result.actor_count, 2)
        self.assertEqual(result.period_count, 2)

    def test_emergent_concept_does_not_promote_single_source_spike(self):
        concept = "VIRAL_SPIKE"
        observations = [
            self._obs(1, concept, "same-source", "actor-a", 1),
            self._obs(2, concept, "same-source", "actor-b", 1),
            self._obs(3, concept, "same-source", "actor-c", 1),
            self._obs(4, concept, "same-source", "actor-d", 1),
        ]
        result = assess_emergent_concept(concept, observations)
        self.assertEqual(result.state, "CANDIDATE")
        self.assertIn("INSUFFICIENT_SOURCE_DIVERSITY", result.reasons)
        self.assertIn("INSUFFICIENT_TIME_PERSISTENCE", result.reasons)

    def test_domestic_signal_is_primary(self):
        result = classify_signal_focus(
            {
                "signal_id": "cn-1",
                "origin_geography": "CN-JS-XZ",
                "evidence_refs": ["ref-a"],
            }
        )
        self.assertEqual(result["lane"], "DOMESTIC_PRIMARY")
        self.assertFalse(result["cross_border_exception_candidate"])

    def test_foreign_signal_is_auxiliary_not_domestic_truth(self):
        result = classify_signal_focus(
            {
                "signal_id": "global-1",
                "origin_geography": "US",
                "evidence_refs": ["reddit-thread"],
                "china_relevance_evidence": ["mentions-china-product"],
            }
        )
        self.assertEqual(result["lane"], "GLOBAL_AUXILIARY")
        self.assertEqual(result["next_action"], "GENERATE_TRANSFER_HYPOTHESIS_ONLY")

    def test_foreign_signal_without_china_relation_stays_unbound(self):
        result = classify_signal_focus(
            {
                "signal_id": "global-2",
                "origin_geography": "GB",
                "evidence_refs": ["source-ref"],
            }
        )
        self.assertEqual(result["lane"], "GLOBAL_UNBOUND")

    def test_cross_border_is_exception_only_and_requires_direct_evidence(self):
        weak = classify_signal_focus(
            {
                "signal_id": "x-weak",
                "origin_geography": "SG",
                "evidence_refs": ["ref-a"],
                "china_relevance_evidence": ["ref-b"],
                "domestic_execution_evidence": ["ref-c"],
            }
        )
        strong = classify_signal_focus(
            {
                "signal_id": "x-strong",
                "origin_geography": "SG",
                "evidence_refs": ["ref-a"],
                "china_relevance_evidence": ["ref-b"],
                "domestic_execution_evidence": ["ref-c"],
                "cross_border_direct_transaction_evidence": ["ref-d"],
            }
        )
        self.assertFalse(weak["cross_border_exception_candidate"])
        self.assertTrue(strong["cross_border_exception_candidate"])
        self.assertEqual(strong["cross_border_mode"], "EXCEPTION_ONLY")


if __name__ == "__main__":
    unittest.main()
