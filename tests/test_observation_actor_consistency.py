import unittest

from src.observation_fabric import EvidenceRef, ObservationEnvelope, SemanticClaim


class ObservationActorConsistencyTests(unittest.TestCase):
    def test_claim_actor_must_be_declared_for_actor_queries(self):
        with self.assertRaisesRegex(ValueError, "claim actor_id must be declared"):
            ObservationEnvelope(
                observation_id="actor-index-1",
                source_id="FIXTURE",
                source_record_id="r1",
                source_locator="fixture://r1",
                source_origin_geography="CN",
                relevance_geographies=("CN",),
                source_tier="REVIEWED_FIXTURE",
                observed_at="2026-09-14T00:00:00+08:00",
                retrieved_at="2026-09-14T00:01:00+08:00",
                parser_version="test.v1",
                raw_payload_hash="a" * 64,
                sampling_boundary="TEST_ONLY",
                evidence=(EvidenceRef("e1", "fixture://r1#e1"),),
                claims=(
                    SemanticClaim(
                        claim_id="c1",
                        primitive="BEHAVIOR",
                        concept="behavior.test",
                        epistemic_status="OBSERVED",
                        evidence_refs=("e1",),
                        actor_id="actor-claim-only",
                    ),
                ),
                actor_ids=(),
            )

    def test_actorless_aggregate_claim_remains_valid(self):
        envelope = ObservationEnvelope(
            observation_id="aggregate-1",
            source_id="FIXTURE_MACRO",
            source_record_id="m1",
            source_locator="fixture://macro/m1",
            source_origin_geography="CN",
            relevance_geographies=("CN",),
            source_tier="REVIEWED_FIXTURE",
            observed_at="2026-09-14T00:00:00+08:00",
            retrieved_at="2026-09-14T00:01:00+08:00",
            parser_version="test.v1",
            raw_payload_hash="b" * 64,
            sampling_boundary="AGGREGATE_TEST_ONLY",
            evidence=(EvidenceRef("e1", "fixture://macro/m1#e1"),),
            claims=(
                SemanticClaim(
                    claim_id="c1",
                    primitive="FLOW",
                    concept="macro.aggregate.test",
                    epistemic_status="OBSERVED",
                    evidence_refs=("e1",),
                    geography="CN",
                ),
            ),
            actor_ids=(),
        )
        self.assertEqual(envelope.actor_ids, ())


if __name__ == "__main__":
    unittest.main()
