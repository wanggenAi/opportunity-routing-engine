import unittest
from datetime import date

from src.psychology_tracker import (
    PSYCHOLOGY_DIMENSIONS,
    PSYCHOLOGY_SEED_CONCEPTS,
    PsychologySignal,
    aggregate_snapshot,
)


class PsychologyTrackerTests(unittest.TestCase):
    def _signal(
        self,
        idx: int,
        *,
        concept: str,
        source_type: str = "D_SOCIAL_MEDIA_LANGUAGE",
        primitive: str = "PERCEPTION",
        behavior: float = 0.0,
        money: float = 0.0,
        representative: bool = False,
        representative_share=None,
        sample_size=None,
        source_day: int | None = None,
    ) -> PsychologySignal:
        day = source_day or (10 + idx)
        key_refs = [f"evidence:signal-{idx}"]
        behavior_refs = ()
        money_refs = ()
        representative_refs = ()
        if behavior > 0:
            ref = f"evidence:behavior-{idx}"
            key_refs.append(ref)
            behavior_refs = (ref,)
        if money > 0:
            ref = f"evidence:money-{idx}"
            key_refs.append(ref)
            money_refs = (ref,)
        if representative:
            ref = f"evidence:representative-method-{idx}"
            key_refs.append(ref)
            representative_refs = (ref,)
        return PsychologySignal(
            signal_id=f"signal-{idx}",
            observed_at=date(2026, 9, day),
            source_date=date(2026, 9, day),
            source_type=source_type,
            source_name=f"source-{idx}",
            geography="CN",
            actor_segment="CONSUMERS",
            psychology_dimension=concept,
            direction=0.8,
            intensity=0.8,
            behavior_corroboration=behavior,
            money_corroboration=money,
            representative_sample=representative,
            representative_share=representative_share,
            sample_size=sample_size,
            provenance_quality="HIGH",
            semantic_primitive=primitive,
            key_evidence_refs=tuple(key_refs),
            behavior_evidence_refs=behavior_refs,
            money_evidence_refs=money_refs,
            representative_evidence_refs=representative_refs,
        )

    def test_signal_requires_source_evidence_lineage(self):
        with self.assertRaisesRegex(ValueError, "key_evidence_refs is required"):
            PsychologySignal(
                signal_id="no-lineage",
                observed_at=date(2026, 9, 10),
                source_date=date(2026, 9, 10),
                source_type="D_SOCIAL_MEDIA_LANGUAGE",
                source_name="source",
                geography="CN",
                actor_segment="CONSUMERS",
                psychology_dimension="OPEN_CONCEPT",
                direction=0.5,
                intensity=0.5,
            )

    def test_nonzero_behavior_and_money_corroboration_require_bound_refs(self):
        base = dict(
            signal_id="naked-corroboration",
            observed_at=date(2026, 9, 10),
            source_date=date(2026, 9, 10),
            source_type="A_HARD_MONEY_BEHAVIOR",
            source_name="source",
            geography="CN",
            actor_segment="CONSUMERS",
            psychology_dimension="OPEN_CONCEPT",
            direction=0.5,
            intensity=0.5,
            key_evidence_refs=("evidence:source",),
        )
        with self.assertRaisesRegex(ValueError, "behavior_evidence_refs"):
            PsychologySignal(**base, behavior_corroboration=0.8)
        with self.assertRaisesRegex(ValueError, "money_evidence_refs"):
            PsychologySignal(**base, money_corroboration=0.8)

    def test_specialized_refs_must_be_part_of_signal_lineage(self):
        with self.assertRaisesRegex(ValueError, "must be included in key_evidence_refs"):
            PsychologySignal(
                signal_id="detached-evidence",
                observed_at=date(2026, 9, 10),
                source_date=date(2026, 9, 10),
                source_type="A_HARD_MONEY_BEHAVIOR",
                source_name="source",
                geography="CN",
                actor_segment="CONSUMERS",
                psychology_dimension="OPEN_CONCEPT",
                direction=0.5,
                intensity=0.5,
                behavior_corroboration=0.8,
                key_evidence_refs=("evidence:source",),
                behavior_evidence_refs=("evidence:detached",),
            )

    def test_novel_concept_is_accepted_without_seed_enum_change(self):
        concept = "POST_2030_DECISION_DEFERRAL_FRICTION"
        self.assertNotIn(concept, PSYCHOLOGY_SEED_CONCEPTS)
        signal = self._signal(1, concept=concept)
        self.assertEqual(signal.concept, concept)
        snapshot = aggregate_snapshot(
            [signal],
            as_of=date(2026, 9, 20),
            geography="CN",
            actor_segment="CONSUMERS",
            psychology_dimension=concept,
        )
        self.assertEqual(snapshot.concept, concept)
        self.assertEqual(snapshot.signal_count, 1)
        self.assertEqual(snapshot.semantic_primitive, "PERCEPTION")
        self.assertEqual(snapshot.supporting_evidence_refs, ("evidence:signal-1",))

    def test_legacy_dimensions_name_is_seed_alias_not_validation_boundary(self):
        self.assertIs(PSYCHOLOGY_DIMENSIONS, PSYCHOLOGY_SEED_CONCEPTS)
        concept = "NOVEL_VALUE_SIGNAL_NOT_IN_2026_SEEDS"
        self.assertNotIn(concept, PSYCHOLOGY_DIMENSIONS)
        signal = self._signal(1, concept=concept)
        self.assertEqual(signal.psychology_dimension, concept)

    def test_only_stable_psychology_primitives_are_closed(self):
        with self.assertRaisesRegex(ValueError, "semantic_primitive"):
            self._signal(
                1,
                concept="OPEN_CONCEPT",
                primitive="SHOPPING_PLATFORM_THEME",
            )

    def test_same_named_concept_is_not_mixed_across_primitives(self):
        concept = "CERTAINTY_SEEKING"
        perception = self._signal(1, concept=concept, primitive="PERCEPTION")
        motive = self._signal(2, concept=concept, primitive="MOTIVE")
        behavior = self._signal(3, concept=concept, primitive="BEHAVIOR")

        perception_snapshot = aggregate_snapshot(
            [perception, motive, behavior],
            as_of=date(2026, 9, 20),
            geography="CN",
            actor_segment="CONSUMERS",
            psychology_dimension=concept,
            semantic_primitive="PERCEPTION",
        )
        motive_snapshot = aggregate_snapshot(
            [perception, motive, behavior],
            as_of=date(2026, 9, 20),
            geography="CN",
            actor_segment="CONSUMERS",
            psychology_dimension=concept,
            semantic_primitive="MOTIVE",
        )
        self.assertEqual(perception_snapshot.signal_count, 1)
        self.assertEqual(motive_snapshot.signal_count, 1)
        self.assertEqual(perception_snapshot.semantic_primitive, "PERCEPTION")
        self.assertEqual(motive_snapshot.semantic_primitive, "MOTIVE")

    def test_social_and_search_only_cannot_produce_high_confidence_or_population_share(self):
        concept = "NOVEL_SOCIAL_SALIENCE"
        signals = [
            self._signal(1, concept=concept, source_type="D_SOCIAL_MEDIA_LANGUAGE"),
            self._signal(2, concept=concept, source_type="D_SOCIAL_MEDIA_LANGUAGE"),
            self._signal(3, concept=concept, source_type="C_SEARCH_PLATFORM_TREND"),
            self._signal(4, concept=concept, source_type="C_SEARCH_PLATFORM_TREND"),
            self._signal(5, concept=concept, source_type="D_SOCIAL_MEDIA_LANGUAGE"),
        ]
        snapshot = aggregate_snapshot(
            signals,
            as_of=date(2026, 9, 20),
            geography="CN",
            actor_segment="CONSUMERS",
            psychology_dimension=concept,
        )
        self.assertEqual(snapshot.confidence, "LOW")
        self.assertIsNone(snapshot.representative_share)
        self.assertIsNone(snapshot.representative_sample_size)
        self.assertEqual(snapshot.behavior_evidence_refs, ())
        self.assertEqual(snapshot.money_evidence_refs, ())

    def test_multi_channel_behavior_and_money_corroboration_retains_evidence_lineage(self):
        concept = "NOVEL_CERTAINTY_PREMIUM_SIGNAL"
        signals = [
            self._signal(
                1,
                concept=concept,
                source_type="A_HARD_MONEY_BEHAVIOR",
                behavior=0.9,
                money=0.8,
            ),
            self._signal(
                2,
                concept=concept,
                source_type="A_HARD_MONEY_BEHAVIOR",
                behavior=0.8,
                money=0.8,
            ),
            self._signal(
                3,
                concept=concept,
                source_type="B_REPRESENTATIVE_RESEARCH",
                behavior=0.5,
                money=0.4,
            ),
            self._signal(
                4,
                concept=concept,
                source_type="C_SEARCH_PLATFORM_TREND",
                behavior=0.4,
                money=0.3,
            ),
            self._signal(
                5,
                concept=concept,
                source_type="D_SOCIAL_MEDIA_LANGUAGE",
                behavior=0.3,
                money=0.2,
            ),
        ]
        snapshot = aggregate_snapshot(
            signals,
            as_of=date(2026, 9, 20),
            geography="CN",
            actor_segment="CONSUMERS",
            psychology_dimension=concept,
        )
        self.assertEqual(snapshot.confidence, "HIGH")
        self.assertGreaterEqual(snapshot.behavior_corroboration, 0.35)
        self.assertGreaterEqual(snapshot.money_corroboration, 0.25)
        self.assertEqual(len(snapshot.behavior_evidence_refs), 5)
        self.assertEqual(len(snapshot.money_evidence_refs), 5)
        self.assertTrue(set(snapshot.behavior_evidence_refs).issubset(snapshot.supporting_evidence_refs))
        self.assertTrue(set(snapshot.money_evidence_refs).issubset(snapshot.supporting_evidence_refs))
        self.assertIsNone(snapshot.representative_share)

    def test_representative_share_requires_method_evidence_and_explicit_sample_size(self):
        base = dict(
            signal_id="representative-bad",
            observed_at=date(2026, 9, 10),
            source_date=date(2026, 9, 10),
            source_type="B_REPRESENTATIVE_RESEARCH",
            source_name="survey",
            geography="CN",
            actor_segment="CONSUMERS",
            psychology_dimension="OPEN_REPRESENTATIVE_TEST_CONCEPT",
            direction=0.5,
            intensity=0.5,
            representative_sample=True,
            representative_share=0.42,
            key_evidence_refs=("evidence:survey",),
        )
        with self.assertRaisesRegex(ValueError, "representative_evidence_refs"):
            PsychologySignal(**base, sample_size=1200)

        with self.assertRaisesRegex(ValueError, "sample_size"):
            PsychologySignal(
                **base,
                representative_evidence_refs=("evidence:survey",),
            )

        signal = self._signal(
            1,
            concept="OPEN_REPRESENTATIVE_TEST_CONCEPT",
            source_type="B_REPRESENTATIVE_RESEARCH",
            representative=True,
            representative_share=0.42,
            sample_size=1200,
        )
        snapshot = aggregate_snapshot(
            [signal],
            as_of=date(2026, 9, 20),
            geography="CN",
            actor_segment="CONSUMERS",
            psychology_dimension="OPEN_REPRESENTATIVE_TEST_CONCEPT",
        )
        self.assertEqual(snapshot.representative_share, 0.42)
        self.assertEqual(snapshot.representative_sample_size, 1200)
        self.assertEqual(len(snapshot.representative_evidence_refs), 1)
        self.assertTrue(
            set(snapshot.representative_evidence_refs).issubset(
                snapshot.supporting_evidence_refs
            )
        )


if __name__ == "__main__":
    unittest.main()
