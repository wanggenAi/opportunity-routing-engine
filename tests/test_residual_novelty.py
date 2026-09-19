import unittest
from src.emergent_taxonomy import ReviewedConceptAlignment
from src.observation_fabric import EvidenceRef, ObservationEnvelope, SemanticClaim
from src.residual_novelty import (
    ModelClusterSuggestion,
    assess_model_cluster_suggestion,
    bind_reviewed_alignment_to_residual_pool,
    build_residual_pool,
    model_cluster_suggestion_from_dict,
    summarize_residual_novelty,
)




class ResidualNoveltyTests(unittest.TestCase):
    def _envelope(
        self,
        index: int,
        *,
        concept: str,
        source_id: str | None = None,
        actor_id: str | None = None,
        day: int | None = None,
        epistemic_status: str = "OBSERVED",
        primitive: str = "BEHAVIOR",
    ) -> ObservationEnvelope:
        source = source_id or f"SOURCE_{index}"
        actor = actor_id or f"actor-{index}"
        observed_day = day or (10 + index)
        evidence_id = f"e-{index}"
        return ObservationEnvelope(
            observation_id=f"obs-{index}",
            source_id=source,
            source_record_id=f"record-{index}",
            source_locator=f"https://example.test/{index}",
            source_origin_geography="CN",
            relevance_geographies=("CN",),
            source_tier="TEST_FIXTURE",
            observed_at=f"2026-09-{observed_day:02d}T01:00:00+08:00",
            retrieved_at=f"2026-09-{observed_day:02d}T02:00:00+08:00",
            parser_version="test.v1",
            raw_payload_hash=f"{index:064x}"[-64:],
            sampling_boundary="TEST_ONLY",
            evidence=(EvidenceRef(evidence_id, f"https://example.test/{index}"),),
            claims=(
                SemanticClaim(
                    claim_id=f"claim-{index}",
                    primitive=primitive,
                    concept=concept,
                    epistemic_status=epistemic_status,
                    evidence_refs=(evidence_id,),
                    actor_id=actor,
                    geography="CN",
                    inference_depth=1 if epistemic_status == "INFERRED" else 0,
                ),
            ),
            actor_ids=(actor,),
        )

    @staticmethod
    def _ref(envelope: ObservationEnvelope) -> str:
        claim = envelope.claims[0]
        return f"{envelope.source_id}::{envelope.observation_id}::{claim.claim_id}"

    def _clusterable_envelopes(self):
        return (
            self._envelope(1, concept="SOURCE_CONCEPT_A", day=11),
            self._envelope(2, concept="SOURCE_CONCEPT_A", day=12),
            self._envelope(3, concept="SOURCE_CONCEPT_B", day=13),
            self._envelope(4, concept="SOURCE_CONCEPT_B", day=14),
        )

    def test_reported_claim_remains_in_residual_lineage_even_when_exact_pattern_gate_excludes_it(self):
        envelope = self._envelope(
            1,
            concept="REPORTED_SOURCE_NATIVE_CONCEPT",
            epistemic_status="REPORTED",
        )
        pool = build_residual_pool((envelope,))
        self.assertEqual(len(pool), 1)
        atom = pool[0]
        self.assertEqual(atom.exact_pattern_state, "UNBOUND")
        self.assertEqual(atom.epistemic_counts, {"REPORTED": 1})
        self.assertEqual(atom.claim_count, 1)
        self.assertEqual(atom.usable_non_inferred_claim_count, 1)
        self.assertEqual(atom.supporting_claim_refs, (self._ref(envelope),))
        self.assertEqual(atom.taxonomy_promotion, "NOT_PROMOTED")
        self.assertEqual(atom.business_promotion, "NOT_PROMOTED")

    def test_evidence_sufficient_model_cluster_still_waits_for_explicit_semantic_review(self):
        envelopes = self._clusterable_envelopes()
        pool = build_residual_pool(envelopes)
        suggestion = ModelClusterSuggestion(
            suggestion_id="suggestion:test-cluster",
            proposed_concept="POSSIBLE_SHARED_BEHAVIOR",
            primitive="BEHAVIOR",
            supporting_claim_refs=tuple(self._ref(item) for item in envelopes),
            rationale="Synthetic grouping suggestion only.",
        )
        result = assess_model_cluster_suggestion(suggestion, envelopes, pool)
        self.assertEqual(result.state, "AWAITING_EXPLICIT_SEMANTIC_REVIEW")
        self.assertEqual(result.observation_count, 4)
        self.assertEqual(result.source_count, 4)
        self.assertEqual(result.actor_count, 4)
        self.assertEqual(result.period_count, 4)
        self.assertEqual(result.source_concept_count, 2)
        self.assertEqual(result.semantic_coherence_state, "UNREVIEWED")
        self.assertFalse(result.automatic_alignment_creation)
        self.assertEqual(result.taxonomy_promotion, "NOT_PROMOTED")
        self.assertEqual(result.business_promotion, "NOT_PROMOTED")

    def test_inferred_claim_cannot_bootstrap_model_cluster_readiness(self):
        base = list(self._clusterable_envelopes())
        base[3] = self._envelope(
            4,
            concept="SOURCE_CONCEPT_B",
            day=14,
            epistemic_status="INFERRED",
        )
        envelopes = tuple(base)
        pool = build_residual_pool(envelopes)
        suggestion = ModelClusterSuggestion(
            suggestion_id="suggestion:inferred-does-not-count",
            proposed_concept="POSSIBLE_SHARED_BEHAVIOR",
            primitive="BEHAVIOR",
            supporting_claim_refs=tuple(self._ref(item) for item in envelopes),
            rationale="Synthetic grouping suggestion only.",
        )
        result = assess_model_cluster_suggestion(suggestion, envelopes, pool)
        self.assertEqual(result.state, "INSUFFICIENT_EVIDENCE")
        self.assertEqual(result.observation_count, 3)
        self.assertIn("INSUFFICIENT_OBSERVATION_COUNT", result.reasons)
        self.assertEqual(result.epistemic_counts["INFERRED"], 1)

    def test_model_suggestion_schema_rejects_truth_smuggling(self):
        with self.assertRaisesRegex(ValueError, "unknown model cluster suggestion fields"):
            model_cluster_suggestion_from_dict(
                {
                    "suggestion_id": "suggestion:bad",
                    "proposed_concept": "BAD",
                    "primitive": "BEHAVIOR",
                    "supporting_claim_refs": ["x::y::z"],
                    "rationale": "Bad fixture.",
                    "payer": "invented-payer",
                }
            )

    def test_explicit_reviewed_alignment_can_be_evidence_ready_without_taxonomy_promotion(self):
        envelopes = self._clusterable_envelopes()
        pool = build_residual_pool(envelopes)
        alignment = ReviewedConceptAlignment(
            alignment_id="alignment:test-reviewed",
            candidate_concept="REVIEWED_SHARED_BEHAVIOR",
            primitive="BEHAVIOR",
            definition="Reviewed semantic grouping for a synthetic test.",
            boundary="Does not create taxonomy, payer, demand, route or opportunity truth.",
            counterexamples=("The two source concepts diverge under broader evidence.",),
            supporting_claim_refs=tuple(self._ref(item) for item in envelopes),
            alignment_rationale="Explicit human/agent review found a coherent grouping for test purposes.",
        )
        result = bind_reviewed_alignment_to_residual_pool(alignment, envelopes, pool)
        self.assertEqual(result.state, "PROMOTION_REVIEW_READY")
        self.assertEqual(result.semantic_coherence_state, "EXPLICITLY_REVIEWED")
        self.assertEqual(set(result.source_concepts), {"SOURCE_CONCEPT_A", "SOURCE_CONCEPT_B"})
        self.assertEqual(len(result.source_residual_ids), 2)
        self.assertEqual(result.taxonomy_promotion, "NOT_PROMOTED")
        self.assertEqual(result.business_promotion, "NOT_PROMOTED")

    def test_summary_with_model_suggestion_never_auto_creates_alignment(self):
        envelopes = self._clusterable_envelopes()
        suggestion = ModelClusterSuggestion(
            suggestion_id="suggestion:summary",
            proposed_concept="POSSIBLE_SHARED_BEHAVIOR",
            primitive="BEHAVIOR",
            supporting_claim_refs=tuple(self._ref(item) for item in envelopes),
            rationale="Synthetic grouping suggestion only.",
        )
        summary = summarize_residual_novelty(envelopes, model_suggestions=(suggestion,))
        self.assertEqual(summary["model_suggestion_state_counts"], {"AWAITING_EXPLICIT_SEMANTIC_REVIEW": 1})
        self.assertEqual(summary["automatic_alignment_creation_count"], 0)
        self.assertEqual(summary["automatic_taxonomy_promotion_count"], 0)
        self.assertEqual(summary["taxonomy_promotion"], "NOT_PROMOTED")


if __name__ == "__main__":
    unittest.main()
