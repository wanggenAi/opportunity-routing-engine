import json
import tempfile
import unittest
from pathlib import Path

from src.emergent_taxonomy import assess_emergent_concept
from src.live_resource_signals import AvailabilityState, PermissionState
from src.observation_fabric import (
    EvidenceRef,
    ObservationEnvelope,
    SemanticClaim,
    project_to_resource_signal,
    semantic_observations_from_envelope,
)
from src.observation_import import envelope_from_record, load_observations
from src.observation_store import SQLiteObservationStore
from src.sensor_registry import SensorCandidate, assess_sensor_candidate


class ObservationFabricTests(unittest.TestCase):
    def _envelope(self, **overrides):
        payload = dict(
            observation_id="obs-1",
            source_id="FIXTURE_CN_TEXT",
            source_record_id="record-1",
            source_locator="fixture://record-1",
            source_origin_geography="CN-JS-XZ",
            relevance_geographies=("CN-JS-XZ",),
            source_tier="REVIEWED_FIXTURE",
            observed_at="2026-09-14T01:00:00+00:00",
            retrieved_at="2026-09-14T01:01:00+00:00",
            parser_version="test.v1",
            raw_payload_hash="a" * 64,
            sampling_boundary="SINGLE_REVIEWED_FIXTURE_ITEM",
            evidence=(EvidenceRef("e1", "fixture://record-1", "explicit evidence"),),
            claims=(
                SemanticClaim(
                    claim_id="c1",
                    primitive="BEHAVIOR",
                    concept="future.unknown_behavior_2030",
                    epistemic_status="OBSERVED",
                    evidence_refs=("e1",),
                    value=True,
                    actor_id="actor-1",
                    geography="CN-JS-XZ",
                ),
            ),
            actor_ids=("actor-1",),
            unknown_fields=("payer",),
        )
        payload.update(overrides)
        return ObservationEnvelope(**payload)

    def test_unknown_concept_is_accepted_without_core_ontology_change(self):
        envelope = self._envelope()
        semantic = semantic_observations_from_envelope(envelope)
        self.assertEqual(semantic[0].concept, "future.unknown_behavior_2030")

    def test_unknown_primitive_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown semantic primitive"):
            self._envelope(
                claims=(
                    SemanticClaim(
                        "c1", "MORAL_GOODNESS", "good_person", "OBSERVED", ("e1",)
                    ),
                )
            )

    def test_missing_source_provenance_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "requires evidence"):
            self._envelope(evidence=())

    def test_invalid_time_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            self._envelope(observed_at="2026-09-14T01:00:00")

    def test_aggregate_macro_observation_does_not_require_actor(self):
        envelope = self._envelope(
            actor_ids=(),
            claims=(
                SemanticClaim(
                    "flow",
                    "FLOW",
                    "macro.retail_sales_yoy",
                    "OBSERVED",
                    ("e1",),
                    value=-1.2,
                    geography="CN",
                ),
            ),
            source_origin_geography="CN",
            relevance_geographies=("CN",),
        )
        self.assertEqual(envelope.actor_ids, ())
        self.assertIsNone(project_to_resource_signal(envelope))

    def test_reported_or_inferred_claims_are_not_upgraded_by_resource_projection(self):
        envelope = self._envelope(
            claims=(
                SemanticClaim(
                    "reported-cap",
                    "CAPABILITY",
                    "capability.claimed_only",
                    "REPORTED",
                    ("e1",),
                    value=True,
                    actor_id="actor-1",
                ),
                SemanticClaim(
                    "inferred-friction",
                    "FRICTION",
                    "friction.hypothesis_only",
                    "INFERRED",
                    ("e1",),
                    value=True,
                    actor_id="actor-1",
                    inference_depth=1,
                ),
            )
        )
        self.assertIsNone(project_to_resource_signal(envelope))

    def test_observed_resource_projection_cannot_create_availability_or_permission(self):
        envelope = self._envelope(
            claims=(
                SemanticClaim(
                    "cap",
                    "CAPABILITY",
                    "capability.local_delivery",
                    "OBSERVED",
                    ("e1",),
                    value=True,
                    actor_id="actor-1",
                ),
            )
        )
        signal = project_to_resource_signal(envelope)
        self.assertIsNotNone(signal)
        self.assertEqual(signal.availability, AvailabilityState.UNKNOWN)
        self.assertEqual(signal.permission, PermissionState.UNKNOWN)

    def test_foreign_observation_remains_global_auxiliary(self):
        envelope = self._envelope(
            source_id="FIXTURE_GLOBAL_TEXT",
            source_origin_geography="GLOBAL",
            relevance_geographies=("CN",),
        )
        self.assertEqual(envelope.research_lane, "GLOBAL_AUXILIARY")

    def test_contradictory_evidence_is_preserved(self):
        envelope = self._envelope(
            evidence=(
                EvidenceRef("e1", "fixture://record-1", "claim"),
                EvidenceRef("e2", "fixture://record-2", "counterevidence"),
            ),
            contradiction_refs=("e2",),
            claims=(
                SemanticClaim(
                    "c1",
                    "PERCEPTION",
                    "consumer.spending_caution_claim",
                    "REPORTED",
                    ("e1",),
                    contradiction_refs=("e2",),
                ),
            ),
        )
        self.assertEqual(envelope.contradiction_refs, ("e2",))
        self.assertEqual(envelope.claims[0].contradiction_refs, ("e2",))

    def test_missing_remains_unknown_not_zero_or_false(self):
        envelope = self._envelope(unknown_fields=("payer", "population_prevalence"))
        rendered = envelope.as_dict()
        self.assertIn("payer", rendered["unknown_fields"])
        self.assertNotIn("payer", {claim.concept for claim in envelope.claims})

    def test_one_social_post_cannot_satisfy_emergent_taxonomy_gate(self):
        envelope = self._envelope(
            source_id="FIXTURE_SINGLE_SOCIAL_POST",
            claims=(
                SemanticClaim(
                    "c1",
                    "PERCEPTION",
                    "social.everyone_is_saving_money_claim",
                    "REPORTED",
                    ("e1",),
                    actor_id="actor-1",
                ),
            ),
        )
        semantic = semantic_observations_from_envelope(envelope)
        assessment = assess_emergent_concept(
            "social.everyone_is_saving_money_claim", semantic
        )
        self.assertEqual(assessment.state, "CANDIDATE")
        self.assertIn("INSUFFICIENT_SOURCE_DIVERSITY", assessment.reasons)
        self.assertIn("INSUFFICIENT_ACTOR_DIVERSITY", assessment.reasons)
        self.assertIn("INSUFFICIENT_TIME_PERSISTENCE", assessment.reasons)

    def test_future_platform_2030_can_join_registry_without_kernel_change(self):
        candidate = SensorCandidate(
            source_id="FUTURE_PLATFORM_2030",
            name="FuturePlatform2030",
            base_url="https://future.example",
            origin_geography="GLOBAL",
            relevance_geographies=("CN",),
            observable_dimensions=("BEHAVIOR", "PERCEPTION"),
            collection_mode="UNKNOWN",
            provenance_refs=("registry-review-2030",),
            china_relevance_evidence_refs=("china-relation-review-2030",),
            unique_signal_value="novel public behavior surface",
        )
        assessment = assess_sensor_candidate(candidate)
        self.assertTrue(assessment["qualified"])
        self.assertFalse(assessment["automation_ready"])

    def test_sensor_qualification_does_not_change_observation_truth(self):
        envelope = self._envelope()
        semantic = semantic_observations_from_envelope(envelope)
        self.assertEqual(semantic[0].primitive, "BEHAVIOR")
        self.assertEqual(envelope.claims[0].epistemic_status, "OBSERVED")

    def test_structured_import_rejects_downstream_permission_or_availability_fields(self):
        payload = self._envelope().as_dict()
        payload["permission"] = "ALLOWED"
        with self.assertRaisesRegex(ValueError, "unknown observation fields"):
            envelope_from_record(payload)
        payload.pop("permission")
        payload["availability"] = "CONFIRMED"
        with self.assertRaisesRegex(ValueError, "unknown observation fields"):
            envelope_from_record(payload)

    def test_json_and_jsonl_import_are_deterministic(self):
        record = self._envelope().as_dict()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            json_path = root / "observations.json"
            json_path.write_text(json.dumps([record]), encoding="utf-8")
            jsonl_path = root / "observations.jsonl"
            jsonl_path.write_text(json.dumps(record) + "\n", encoding="utf-8")
            self.assertEqual(load_observations(json_path), load_observations(jsonl_path))


class ObservationStoreTests(unittest.TestCase):
    def _envelope(self, **overrides):
        payload = dict(
            observation_id="obs-store-1",
            source_id="FIXTURE_STORE",
            source_record_id="r1",
            source_locator="fixture://store/r1",
            source_origin_geography="CN-JS-XZ",
            relevance_geographies=("CN-JS-XZ",),
            source_tier="REVIEWED_FIXTURE",
            observed_at="2026-09-14T01:00:00+00:00",
            retrieved_at="2026-09-14T01:01:00+00:00",
            parser_version="test.v1",
            raw_payload_hash="b" * 64,
            sampling_boundary="SINGLE_REVIEWED_FIXTURE_ITEM",
            evidence=(EvidenceRef("e1", "fixture://store/r1", "evidence"),),
            claims=(
                SemanticClaim(
                    "c1",
                    "CHANGE",
                    "orders.increased",
                    "OBSERVED",
                    ("e1",),
                    actor_id="factory-1",
                    geography="CN-JS-XZ",
                ),
            ),
            actor_ids=("factory-1",),
        )
        payload.update(overrides)
        return ObservationEnvelope(**payload)

    def test_duplicate_ingestion_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteObservationStore(Path(tmp) / "obs.db") as store:
                envelope = self._envelope()
                self.assertEqual(store.ingest(envelope).kind, "FIRST_SEEN")
                self.assertEqual(store.ingest(envelope).kind, "DUPLICATE")
                self.assertEqual(len(store.history(envelope.source_id, envelope.observation_id)), 1)

    def test_revision_preserves_history_and_updates_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteObservationStore(Path(tmp) / "obs.db") as store:
                first = self._envelope()
                revised = self._envelope(
                    retrieved_at="2026-09-14T02:01:00+00:00",
                    raw_payload_hash="c" * 64,
                    evidence=(EvidenceRef("e1", "fixture://store/r1", "revised evidence"),),
                )
                store.ingest(first)
                self.assertEqual(store.ingest(revised).kind, "REVISION")
                self.assertEqual(len(store.history(first.source_id, first.observation_id)), 2)
                self.assertEqual(
                    store.current(first.source_id, first.observation_id).raw_payload_hash,
                    "c" * 64,
                )

    def test_out_of_order_revision_is_archived_but_cannot_roll_back_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteObservationStore(Path(tmp) / "obs.db") as store:
                current = self._envelope(retrieved_at="2026-09-14T03:00:00+00:00")
                older = self._envelope(
                    retrieved_at="2026-09-14T02:00:00+00:00",
                    raw_payload_hash="d" * 64,
                )
                store.ingest(current)
                self.assertEqual(store.ingest(older).kind, "OUT_OF_ORDER")
                self.assertEqual(
                    store.current(current.source_id, current.observation_id).retrieved_at,
                    "2026-09-14T03:00:00+00:00",
                )
                self.assertEqual(len(store.history(current.source_id, current.observation_id)), 2)

    def test_query_by_source_actor_primitive_concept_time_and_geography(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteObservationStore(Path(tmp) / "obs.db") as store:
                envelope = self._envelope()
                store.ingest(envelope)
                self.assertEqual(len(store.query(source_id="FIXTURE_STORE")), 1)
                self.assertEqual(len(store.query(actor_id="factory-1")), 1)
                self.assertEqual(len(store.query(primitive="CHANGE")), 1)
                self.assertEqual(len(store.query(concept="orders.increased")), 1)
                self.assertEqual(len(store.query(geography="CN-JS-XZ")), 1)
                self.assertEqual(
                    len(store.query(observed_from="2026-09-14T00:00:00+00:00")), 1
                )
                self.assertEqual(
                    len(store.query(observed_to="2026-09-14T00:00:00+00:00")), 0
                )


if __name__ == "__main__":
    unittest.main()
