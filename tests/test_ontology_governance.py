import json
import unittest
from dataclasses import replace
from pathlib import Path

from scripts.build_broad_discovery_observation_review import build_observation_review
from src.ontology_governance import (
    OntologyConceptVersion,
    OntologyReviewDecision,
    SQLiteOntologyRegistry,
    approved_new_concept_version,
    build_ontology_review_queue,
    review_decision_from_dict,
)


ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "data/research_runs/BROAD_DISCOVERY_RUN_003_2026-09-14"
MISSION = ROOT / "data/research_missions/china_primary_broad_discovery.json"


class OntologyGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review_summary, _ = build_observation_review(
            mission_path=MISSION,
            dynamic_terms_path=RUN_DIR / "dynamic_terms.json",
            captures_path=RUN_DIR / "captures.json",
            reviewed_dir=RUN_DIR / "reviewed",
            alignments_path=RUN_DIR / "concept_alignments_reviewed.json",
        )
        cls.queue = build_ontology_review_queue(cls.review_summary)

    def test_run003_queue_contains_only_review_ready_concepts_and_promotes_nothing(self):
        self.assertEqual(self.queue["queue_kind"], "ONTOLOGY_PROMOTION_REVIEW")
        self.assertEqual(self.queue["review_ready_count"], 2)
        self.assertEqual(self.queue["candidate_not_queued_count"], 3)
        self.assertEqual(self.queue["residual_not_queued_count"], 0)
        self.assertEqual(self.queue["active_ontology_changes"], 0)
        self.assertEqual(self.queue["taxonomy_promotion"], "NOT_PROMOTED")
        self.assertEqual(self.queue["business_promotion"], "NOT_PROMOTED")
        self.assertEqual(
            {item["candidate_concept"] for item in self.queue["items"]},
            {
                "SKILL_TO_WORK_MATCHING_INFRASTRUCTURE",
                "PLATFORM_TRUST_AND_GOVERNANCE_INFRASTRUCTURE",
            },
        )
        for item in self.queue["items"]:
            self.assertEqual(item["review_state"], "AWAITING_EXPLICIT_REVIEW")
            self.assertEqual(
                item["registry_effect"],
                "NONE_UNTIL_EXPLICIT_REVIEW_DECISION_AND_SEPARATE_ACTIVATION",
            )
            self.assertEqual(item["taxonomy_promotion"], "NOT_PROMOTED")
            self.assertEqual(item["business_promotion"], "NOT_PROMOTED")

    def test_queue_fails_closed_if_upstream_claims_taxonomy_or_business_promotion(self):
        promoted = dict(self.review_summary)
        promoted["taxonomy_promotion"] = "PROMOTED"
        with self.assertRaisesRegex(ValueError, "non-promoted taxonomy"):
            build_ontology_review_queue(promoted)

        promoted = dict(self.review_summary)
        promoted["business_promotion"] = "PROMOTED"
        with self.assertRaisesRegex(ValueError, "promoted business truth"):
            build_ontology_review_queue(promoted)

    def _approval(self, item):
        return OntologyReviewDecision(
            review_item_id=item["review_item_id"],
            decision="APPROVE_NEW_CONCEPT_VERSION",
            reviewer_id="reviewer:ontology-governance-test",
            reviewed_at="2026-09-14T21:00:00+08:00",
            rationale="Test explicit governance approval; not a business decision.",
            proposed_concept_id="concept:skill-to-work-matching-infrastructure",
            proposed_label="SKILL_TO_WORK_MATCHING_INFRASTRUCTURE",
        )

    def test_explicit_approval_creates_inactive_version_and_activation_is_separate(self):
        item = next(
            item for item in self.queue["items"]
            if item["candidate_concept"] == "SKILL_TO_WORK_MATCHING_INFRASTRUCTURE"
        )
        spec = approved_new_concept_version(item, self._approval(item))
        self.assertEqual(spec.version, 1)
        self.assertEqual(spec.change_kind, "CREATE")
        self.assertEqual(spec.version_state, "ELIGIBLE")

        with SQLiteOntologyRegistry(":memory:") as registry:
            registry.register_version(spec)
            snapshot = registry.snapshot()
            self.assertEqual(snapshot["version_count"], 1)
            self.assertEqual(snapshot["active_concept_count"], 0)
            self.assertIsNone(registry.active_version(spec.concept_id))

            registry.activate(
                spec.concept_id,
                1,
                activated_by="reviewer:ontology-governance-test",
                activated_at="2026-09-14T21:05:00+08:00",
                rationale="Separate explicit activation after version review.",
            )
            self.assertEqual(registry.active_version(spec.concept_id), spec)
            self.assertEqual(registry.snapshot()["active_concept_count"], 1)

    def test_version_content_is_append_only_and_version_numbers_are_contiguous(self):
        item = self.queue["items"][0]
        first = approved_new_concept_version(item, self._approval(item))
        with SQLiteOntologyRegistry(":memory:") as registry:
            registry.register_version(first)
            registry.register_version(first)
            changed_same_version = replace(first, definition=first.definition + " changed")
            with self.assertRaisesRegex(ValueError, "different content"):
                registry.register_version(changed_same_version)

            skipped = OntologyConceptVersion(
                concept_id=first.concept_id,
                version=3,
                primitive=first.primitive,
                preferred_label=first.preferred_label,
                aliases=(),
                definition=first.definition,
                boundary=first.boundary,
                counterexamples=first.counterexamples,
                source_alignment_refs=first.source_alignment_refs,
                supporting_claim_refs=first.supporting_claim_refs,
                created_from_review_item_id=first.created_from_review_item_id,
                change_kind="REVISE",
                version_state="ELIGIBLE",
                rationale="Attempt to skip version two.",
            )
            with self.assertRaisesRegex(ValueError, "contiguous"):
                registry.register_version(skipped)

    def test_rename_and_deprecation_preserve_history_and_lineage(self):
        item = next(
            item for item in self.queue["items"]
            if item["candidate_concept"] == "SKILL_TO_WORK_MATCHING_INFRASTRUCTURE"
        )
        first = approved_new_concept_version(item, self._approval(item))
        renamed = OntologyConceptVersion(
            concept_id=first.concept_id,
            version=2,
            primitive=first.primitive,
            preferred_label="SKILL_WORK_MATCHING_INFRASTRUCTURE",
            aliases=(first.preferred_label,),
            definition=first.definition,
            boundary=first.boundary,
            counterexamples=first.counterexamples,
            source_alignment_refs=first.source_alignment_refs,
            supporting_claim_refs=first.supporting_claim_refs,
            created_from_review_item_id=first.created_from_review_item_id,
            change_kind="RENAME",
            version_state="ELIGIBLE",
            rationale="Reviewed rename without erasing the original label.",
        )
        deprecated = OntologyConceptVersion(
            concept_id=first.concept_id,
            version=3,
            primitive=first.primitive,
            preferred_label=renamed.preferred_label,
            aliases=renamed.aliases,
            definition=renamed.definition,
            boundary=renamed.boundary,
            counterexamples=renamed.counterexamples,
            source_alignment_refs=renamed.source_alignment_refs,
            supporting_claim_refs=renamed.supporting_claim_refs,
            created_from_review_item_id=first.created_from_review_item_id,
            change_kind="DEPRECATE",
            version_state="DEPRECATED",
            rationale="Concept no longer explains current observations; preserve history.",
        )

        with SQLiteOntologyRegistry(":memory:") as registry:
            registry.register_version(first)
            registry.register_version(renamed)
            registry.add_lineage(
                from_concept_id=renamed.concept_id,
                from_version=2,
                relation="RENAMED_FROM",
                to_concept_id=first.concept_id,
                to_version=1,
                rationale="Version two retains lineage to the original label.",
            )
            registry.register_version(deprecated)
            registry.activate(
                renamed.concept_id,
                2,
                activated_by="reviewer:test",
                activated_at="2026-09-14T21:10:00+08:00",
                rationale="Activate reviewed rename.",
            )
            registry.deactivate(renamed.concept_id)
            self.assertIsNone(registry.active_version(renamed.concept_id))
            with self.assertRaisesRegex(ValueError, "deprecated ontology version"):
                registry.activate(
                    deprecated.concept_id,
                    3,
                    activated_by="reviewer:test",
                    activated_at="2026-09-14T21:20:00+08:00",
                    rationale="Should fail.",
                )
            self.assertEqual([spec.version for spec in registry.versions(first.concept_id)], [1, 2, 3])
            self.assertEqual(registry.lineage()[0]["relation"], "RENAMED_FROM")

    def test_review_decision_schema_rejects_truth_smuggling_and_nonapproval_identity(self):
        item = self.queue["items"][0]
        with self.assertRaisesRegex(ValueError, "unknown ontology review decision fields"):
            review_decision_from_dict(
                {
                    "review_item_id": item["review_item_id"],
                    "decision": "DEFER",
                    "reviewer_id": "reviewer:test",
                    "reviewed_at": "2026-09-14T21:00:00+08:00",
                    "rationale": "Need more evidence.",
                    "route_testable": True,
                }
            )

        with self.assertRaisesRegex(ValueError, "only allowed"):
            review_decision_from_dict(
                {
                    "review_item_id": item["review_item_id"],
                    "decision": "DEFER",
                    "reviewer_id": "reviewer:test",
                    "reviewed_at": "2026-09-14T21:00:00+08:00",
                    "rationale": "Need more evidence.",
                    "proposed_concept_id": "concept:should-not-exist",
                }
            )


if __name__ == "__main__":
    unittest.main()
