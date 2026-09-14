import unittest

from src.ontology_governance import OntologyConceptVersion, SQLiteOntologyRegistry


def _version(
    concept_id: str,
    version: int,
    change_kind: str,
    *,
    label: str | None = None,
    state: str = "ELIGIBLE",
) -> OntologyConceptVersion:
    return OntologyConceptVersion(
        concept_id=concept_id,
        version=version,
        primitive="FRICTION",
        preferred_label=label or concept_id.split(":")[-1].upper().replace("-", "_"),
        aliases=(),
        definition=f"Synthetic lifecycle definition for {concept_id} v{version}.",
        boundary="Synthetic lifecycle fixture only; not production ontology truth.",
        counterexamples=("Any production ontology or business claim.",),
        source_alignment_refs=(f"alignment:synthetic-lifecycle:{concept_id}:{version}",),
        supporting_claim_refs=(f"claim:synthetic-lifecycle:{concept_id}:{version}",),
        created_from_review_item_id=f"review:synthetic-lifecycle:{concept_id}:{version}",
        change_kind=change_kind,
        version_state=state,
        rationale=f"Synthetic {change_kind} lifecycle test.",
    )


class OntologyLifecycleLineageTests(unittest.TestCase):
    def test_version_one_is_valid_for_create_merge_split_only(self):
        _version("concept:synthetic-merge", 1, "MERGE")
        _version("concept:synthetic-split", 1, "SPLIT")
        with self.assertRaisesRegex(ValueError, "version 1 is only valid"):
            _version("concept:synthetic-revise", 1, "REVISE")
        with self.assertRaisesRegex(ValueError, "version 1 is only valid"):
            _version("concept:synthetic-rename", 1, "RENAME")

    def test_revise_requires_immediate_revised_from_lineage_before_activation_or_snapshot(self):
        first = _version("concept:synthetic-revise", 1, "CREATE")
        revised = _version("concept:synthetic-revise", 2, "REVISE")
        with SQLiteOntologyRegistry(":memory:") as registry:
            registry.register_version(first)
            registry.register_version(revised)
            with self.assertRaisesRegex(ValueError, "REVISE requires explicit REVISED_FROM"):
                registry.snapshot()
            with self.assertRaisesRegex(ValueError, "REVISE requires explicit REVISED_FROM"):
                registry.activate(
                    revised.concept_id,
                    revised.version,
                    activated_by="reviewer:synthetic-lifecycle",
                    activated_at="2026-09-14T23:58:00+08:00",
                    rationale="Orphan revision must not activate.",
                )

            registry.add_lineage(
                from_concept_id=revised.concept_id,
                from_version=2,
                relation="REVISED_FROM",
                to_concept_id=first.concept_id,
                to_version=1,
                rationale="Explicit synthetic revision lineage.",
            )
            registry.activate(
                revised.concept_id,
                revised.version,
                activated_by="reviewer:synthetic-lifecycle",
                activated_at="2026-09-14T23:59:00+08:00",
                rationale="Revision becomes activatable only after lineage is complete.",
            )
            self.assertEqual(registry.active_version(revised.concept_id), revised)
            self.assertEqual(registry.snapshot()["lineage_integrity"], "VALIDATED")

    def test_merge_v1_requires_two_parent_concepts(self):
        left = _version("concept:synthetic-left", 1, "CREATE")
        right = _version("concept:synthetic-right", 1, "CREATE")
        merged = _version("concept:synthetic-merged", 1, "MERGE")
        with SQLiteOntologyRegistry(":memory:") as registry:
            for spec in (left, right, merged):
                registry.register_version(spec)
            registry.add_lineage(
                from_concept_id=merged.concept_id,
                from_version=1,
                relation="MERGED_FROM",
                to_concept_id=left.concept_id,
                to_version=1,
                rationale="First synthetic merge parent.",
            )
            with self.assertRaisesRegex(ValueError, "at least two parent concepts"):
                registry.snapshot()

            registry.add_lineage(
                from_concept_id=merged.concept_id,
                from_version=1,
                relation="MERGED_FROM",
                to_concept_id=right.concept_id,
                to_version=1,
                rationale="Second synthetic merge parent.",
            )
            snapshot = registry.snapshot()
            self.assertEqual(snapshot["version_count"], 3)
            self.assertEqual(
                [edge["relation"] for edge in snapshot["lineage"]],
                ["MERGED_FROM", "MERGED_FROM"],
            )

    def test_split_v1_requires_two_child_concept_identities_from_shared_source(self):
        source = _version("concept:synthetic-source", 1, "CREATE")
        child_a = _version("concept:synthetic-child-a", 1, "SPLIT")
        child_b = _version("concept:synthetic-child-b", 1, "SPLIT")
        with SQLiteOntologyRegistry(":memory:") as registry:
            for spec in (source, child_a):
                registry.register_version(spec)
            registry.add_lineage(
                from_concept_id=child_a.concept_id,
                from_version=1,
                relation="SPLIT_FROM",
                to_concept_id=source.concept_id,
                to_version=1,
                rationale="First synthetic split child.",
            )
            with self.assertRaisesRegex(ValueError, "at least two child concept identities"):
                registry.snapshot()

            registry.register_version(child_b)
            registry.add_lineage(
                from_concept_id=child_b.concept_id,
                from_version=1,
                relation="SPLIT_FROM",
                to_concept_id=source.concept_id,
                to_version=1,
                rationale="Second synthetic split child.",
            )
            snapshot = registry.snapshot()
            self.assertEqual(snapshot["version_count"], 3)
            self.assertEqual(
                {edge["from_concept_id"] for edge in snapshot["lineage"]},
                {child_a.concept_id, child_b.concept_id},
            )

    def test_lineage_relation_direction_and_change_kind_are_fail_closed(self):
        first = _version("concept:synthetic-direction", 1, "CREATE")
        revised = _version("concept:synthetic-direction", 2, "REVISE")
        other = _version("concept:synthetic-other", 1, "CREATE")
        with SQLiteOntologyRegistry(":memory:") as registry:
            for spec in (first, revised, other):
                registry.register_version(spec)
            with self.assertRaisesRegex(ValueError, "REVISED_FROM must point"):
                registry.add_lineage(
                    from_concept_id=revised.concept_id,
                    from_version=2,
                    relation="REVISED_FROM",
                    to_concept_id=other.concept_id,
                    to_version=1,
                    rationale="Cross-concept revise must fail.",
                )
            with self.assertRaisesRegex(ValueError, "MERGED_FROM must originate"):
                registry.add_lineage(
                    from_concept_id=revised.concept_id,
                    from_version=2,
                    relation="MERGED_FROM",
                    to_concept_id=other.concept_id,
                    to_version=1,
                    rationale="Wrong change kind must fail.",
                )


if __name__ == "__main__":
    unittest.main()
