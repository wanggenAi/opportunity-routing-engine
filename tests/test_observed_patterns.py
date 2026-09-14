import unittest

from src.observation_fabric import EvidenceRef, ObservationEnvelope, SemanticClaim
from src.observed_patterns import (
    BUSINESS_PROMOTION,
    ORDERING_BASIS,
    PatternGate,
    build_observed_patterns,
    summarize_observed_patterns,
)


class ObservedPatternTests(unittest.TestCase):
    def _envelope(
        self,
        index: int,
        *,
        concept: str = "PUBLIC_LISTING_REPEATED",
        primitive: str = "CHANGE",
        source_id: str = "SOURCE_A",
        actor_id: str | None = "actor-a",
        day: int = 14,
        epistemic_status: str = "OBSERVED",
    ) -> ObservationEnvelope:
        observation_id = f"obs-{index}"
        evidence_id = f"e-{index}"
        actor_ids = (actor_id,) if actor_id else ()
        return ObservationEnvelope(
            observation_id=observation_id,
            source_id=source_id,
            source_record_id=f"record-{index}",
            source_locator=f"https://example.test/{index}",
            source_origin_geography="CN-JS-XZ",
            relevance_geographies=("CN-JS-XZ",),
            source_tier="TEST_FIXTURE",
            observed_at=f"2026-09-{day:02d}T01:00:00+08:00",
            retrieved_at=f"2026-09-{day:02d}T02:00:00+08:00",
            parser_version="test.v1",
            raw_payload_hash=(f"{index:064x}"[-64:]),
            sampling_boundary="TEST_ONLY",
            evidence=(EvidenceRef(evidence_id, f"https://example.test/{index}"),),
            claims=(
                SemanticClaim(
                    claim_id=f"claim-{index}",
                    primitive=primitive,
                    concept=concept,
                    epistemic_status=epistemic_status,
                    evidence_refs=(evidence_id,),
                    actor_id=actor_id,
                    geography="CN-JS-XZ",
                    inference_depth=1 if epistemic_status == "INFERRED" else 0,
                ),
            ),
            actor_ids=actor_ids,
        )

    def test_recurrence_actor_diversity_and_time_persistence_promote_only_pattern_state(self):
        envelopes = (
            self._envelope(1, actor_id="actor-a", day=13),
            self._envelope(2, actor_id="actor-b", day=13),
            self._envelope(3, actor_id="actor-a", day=14),
        )
        patterns = build_observed_patterns(envelopes)
        self.assertEqual(len(patterns), 1)
        pattern = patterns[0]
        self.assertEqual(pattern.state, "OBSERVED_PATTERN")
        self.assertEqual(pattern.observation_count, 3)
        self.assertEqual(pattern.actor_count, 2)
        self.assertEqual(pattern.period_count, 2)
        self.assertEqual(pattern.business_promotion, BUSINESS_PROMOTION)
        self.assertIn("LATENT_VALUE_NOT_ESTABLISHED", pattern.downstream_unknowns)
        self.assertIn("PAYER_NOT_ESTABLISHED", pattern.downstream_unknowns)
        self.assertIn("COMPOUNDING_NOT_ESTABLISHED", pattern.downstream_unknowns)

    def test_duplicate_current_identity_cannot_manufacture_recurrence(self):
        envelope = self._envelope(1)
        pattern = build_observed_patterns((envelope, envelope))[0]
        self.assertEqual(pattern.observation_count, 1)
        self.assertEqual(pattern.state, "UNBOUND")
        self.assertIn("INSUFFICIENT_OBSERVATION_RECURRENCE", pattern.missing_pattern_evidence)

    def test_reported_and_inferred_claims_cannot_satisfy_pattern_gate(self):
        envelopes = (
            self._envelope(1, epistemic_status="REPORTED", actor_id="actor-a", day=13),
            self._envelope(2, epistemic_status="INFERRED", actor_id="actor-b", day=14),
            self._envelope(3, epistemic_status="INFERRED", actor_id="actor-c", day=15),
        )
        pattern = build_observed_patterns(envelopes)[0]
        self.assertEqual(pattern.observation_count, 0)
        self.assertEqual(pattern.state, "UNBOUND")
        self.assertIn("REPORTED_CLAIMS_EXCLUDED_FROM_PATTERN_GATE", pattern.evidence_cautions)
        self.assertIn("INFERRED_CLAIMS_EXCLUDED_FROM_PATTERN_GATE", pattern.evidence_cautions)

    def test_exact_concepts_are_not_semantically_merged(self):
        envelopes = (
            self._envelope(1, concept="PUBLIC_LISTING_REPEATED"),
            self._envelope(2, concept="REPEATED_ASSET_LISTING"),
        )
        patterns = build_observed_patterns(envelopes)
        self.assertEqual(len(patterns), 2)
        self.assertEqual(
            {item.concept for item in patterns},
            {"PUBLIC_LISTING_REPEATED", "REPEATED_ASSET_LISTING"},
        )

    def test_actorless_repeated_events_remain_unbound_under_default_gate(self):
        envelopes = (
            self._envelope(1, actor_id=None, day=13),
            self._envelope(2, actor_id=None, day=14),
            self._envelope(3, actor_id=None, day=14),
        )
        pattern = build_observed_patterns(envelopes)[0]
        self.assertEqual(pattern.observation_count, 3)
        self.assertEqual(pattern.actor_count, 0)
        self.assertEqual(pattern.state, "UNBOUND")
        self.assertIn("INSUFFICIENT_ACTOR_DIVERSITY", pattern.missing_pattern_evidence)

    def test_source_diversity_is_configurable_and_single_source_is_disclosed(self):
        envelopes = (
            self._envelope(1, actor_id="actor-a", day=13),
            self._envelope(2, actor_id="actor-b", day=13),
            self._envelope(3, actor_id="actor-a", day=14),
        )
        default_pattern = build_observed_patterns(envelopes)[0]
        self.assertEqual(default_pattern.state, "OBSERVED_PATTERN")
        self.assertIn("SINGLE_SOURCE_ONLY", default_pattern.evidence_cautions)

        strict_pattern = build_observed_patterns(
            envelopes,
            gate=PatternGate(min_sources=2),
        )[0]
        self.assertEqual(strict_pattern.state, "UNBOUND")
        self.assertIn("INSUFFICIENT_SOURCE_DIVERSITY", strict_pattern.missing_pattern_evidence)

    def test_summary_explicitly_refuses_commercial_ranking_or_promotion(self):
        envelopes = (
            self._envelope(1, actor_id="actor-a", day=13),
            self._envelope(2, actor_id="actor-b", day=13),
            self._envelope(3, actor_id="actor-a", day=14),
        )
        summary = summarize_observed_patterns(envelopes, source_observation_run_id=123)
        self.assertEqual(summary["ordering_basis"], ORDERING_BASIS)
        self.assertEqual(summary["business_promotion"], "NOT_PROMOTED")
        self.assertEqual(summary["source_observation_run_id"], 123)
        self.assertEqual(summary["observed_pattern_count"], 1)
        self.assertNotIn("commercial_score", summary["patterns"][0])
        self.assertNotIn("opportunity_score", summary["patterns"][0])


if __name__ == "__main__":
    unittest.main()
