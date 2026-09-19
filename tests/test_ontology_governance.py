import unittest
from dataclasses import replace

from src.ontology_governance import (
    OntologyConceptVersion,
    OntologyReviewDecision,
    SQLiteOntologyRegistry,
    approved_new_concept_version,
    build_ontology_review_queue,
    review_decision_from_dict,
)


def _ready(alignment_id: str, concept: str, primitive: str):
    return {
        "state": "PROMOTION_REVIEW_READY",
        "alignment_id": alignment_id,
        "candidate_concept": concept,
        "primitive": primitive,
        "definition": "Synthetic concept used only to test ontology governance.",
        "boundary": "Does not imply demand, payer, business or active taxonomy.",
        "counterexamples": ["Synthetic counterexample."],
        "supporting_claim_refs": [f"claim::{alignment_id}::1", f"claim::{alignment_id}::2"],
        "supporting_observation_refs": [f"obs::{alignment_id}::1", f"obs::{alignment_id}::2"],
        "supporting_source_ids": [f"source::{alignment_id}::1", f"source::{alignment_id}::2"],
        "supporting_actor_ids": [f"actor::{alignment_id}::1", f"actor::{alignment_id}::2"],
        "supporting_periods": ["2026-09-18", "2026-09-19"],
        "observation_count": 2,
        "source_count": 2,
        "actor_count": 2,
        "period_count": 2,
        "epistemic_counts": {"OBSERVED": 2},
        "taxonomy_promotion": "NOT_PROMOTED",
        "business_promotion": "NOT_PROMOTED",
    }


class OntologyGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review_summary = {
            "schema_version": "broad-discovery-observation-review.v1",
            "run_id": "SYNTHETIC_GOVERNANCE_FIXTURE",
            "taxonomy_promotion": "NOT_PROMOTED",
            "business_promotion": "NOT_PROMOTED",
            "assessments": [
                _ready("a", "SYNTHETIC_COORDINATION_PATTERN_A", "BEHAVIOR"),
                _ready("b", "SYNTHETIC_COORDINATION_PATTERN_B", "FRICTION"),
                {"state": "CANDIDATE"},
                {"state": "CANDIDATE"},
                {"state": "CANDIDATE"},
            ],
        }
        cls.queue = build_ontology_review_queue(cls.review_summary)

    def test_queue_contains_only_review_ready_concepts_and_promotes_nothing(self):
        self.assertEqual(self.queue["queue_kind"], "ONTOLOGY_PROMOTION_REVIEW")
        self.assertEqual(self.queue["review_ready_count"], 2)
        self.assertEqual(self.queue["candidate_not_queued_count"], 3)
        self.assertEqual(self.queue["residual_not_queued_count"], 0)
        self.assertEqual(self.queue["active_ontology_changes"], 0)
        self.assertEqual(self.queue["taxonomy_promotion"], "NOT_PROMOTED")
        self.assertEqual(self.queue["business_promotion"], "NOT_PROMOTED")
        self.assertEqual(
            {item["candidate_concept"] for item in self.queue["items"]},
            {"SYNTHETIC_COORDINATION_PATTERN_A", "SYNTHETIC_COORDINATION_PATTERN_B"},
        )
        for item in self.queue["items"]:
            self.assertEqual(item["review_state"], "AWAITING_EXPLICIT_REVIEW")
            self.assertEqual(item["registry_effect"], "NONE_UNTIL_EXPLICIT_REVIEW_DECISION_AND_SEPARATE_ACTIVATION")
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
        slug = item["candidate_concept"].lower().replace("_", "-")
        return OntologyReviewDecision(
            review_item_id=item["review_item_id"],
            decision="APPROVE_NEW_CONCEPT_VERSION",
            reviewer_id="reviewer:ontology-governance-test",
            reviewed_at="2026-09-19T21:00:00+08:00",
            rationale="Synthetic explicit governance approval; not a business decision.",
            proposed_concept_id=f"concept:{slug}",
            proposed_label=item["candidate_concept"],
        )

    def test_explicit_approval_creates_inactive_version_and_activation_is_separate(self):
        item = next(item for item in self.queue["items"] if item["candidate_concept"] == "SYNTHETIC_COORDINATION_PATTERN_A")
        spec = approved_new_concept_version(item, self._approval(item))
        self.assertEqual(spec.version, 1)
        self.assertEqual(spec.change_kind, "CREATE")
        self.assertEqual(spec.version_state, "ELIGIBLE")
        with SQLiteOntologyRegistry(":memory:") as registry:
            registry.register_version(spec)
            self.assertEqual(registry.snapshot()["active_concept_count"], 0)
            registry.activate(spec.concept_id, 1, activated_by="reviewer:test", activated_at="2026-09-19T21:05:00+08:00", rationale="Synthetic activation.")
            self.assertEqual(registry.active_version(spec.concept_id), spec)

    def test_version_content_is_append_only_and_numbers_are_contiguous(self):
        item = self.queue["items"][0]
        first = approved_new_concept_version(item, self._approval(item))
        with SQLiteOntologyRegistry(":memory:") as registry:
            registry.register_version(first)
            registry.register_version(first)
            with self.assertRaisesRegex(ValueError, "different content"):
                registry.register_version(replace(first, definition=first.definition + " changed"))
            skipped = OntologyConceptVersion(
                concept_id=first.concept_id, version=3, primitive=first.primitive,
                preferred_label=first.preferred_label, aliases=(), definition=first.definition,
                boundary=first.boundary, counterexamples=first.counterexamples,
                source_alignment_refs=first.source_alignment_refs, supporting_claim_refs=first.supporting_claim_refs,
                created_from_review_item_id=first.created_from_review_item_id, change_kind="REVISE",
                version_state="ELIGIBLE", rationale="Synthetic skipped version."
            )
            with self.assertRaisesRegex(ValueError, "contiguous"):
                registry.register_version(skipped)

    def test_rename_and_deprecation_preserve_history(self):
        item = self.queue["items"][0]
        first = approved_new_concept_version(item, self._approval(item))
        renamed = replace(first, version=2, preferred_label="SYNTHETIC_COORDINATION_PATTERN_A_RENAMED",
                          aliases=(first.preferred_label,), change_kind="RENAME", rationale="Synthetic rename.")
        deprecated = replace(renamed, version=3, change_kind="DEPRECATE", version_state="DEPRECATED",
                             rationale="Synthetic deprecation.")
        with SQLiteOntologyRegistry(":memory:") as registry:
            registry.register_version(first)
            registry.register_version(renamed)
            registry.activate(renamed.concept_id, 2, activated_by="reviewer:test", activated_at="2026-09-19T21:10:00+08:00", rationale="Activate rename.")
            with self.assertRaisesRegex(ValueError, "explicitly deactivated"):
                registry.register_version(deprecated)
            registry.deactivate(renamed.concept_id)
            registry.register_version(deprecated)
            with self.assertRaisesRegex(ValueError, "deprecated ontology version"):
                registry.activate(deprecated.concept_id, 3, activated_by="reviewer:test", activated_at="2026-09-19T21:20:00+08:00", rationale="Must fail.")
            self.assertEqual([spec.version for spec in registry.versions(first.concept_id)], [1, 2, 3])

    def test_review_decision_schema_rejects_truth_smuggling_and_nonapproval_identity(self):
        item = self.queue["items"][0]
        with self.assertRaisesRegex(ValueError, "unknown ontology review decision fields"):
            review_decision_from_dict({
                "review_item_id": item["review_item_id"], "decision": "DEFER",
                "reviewer_id": "reviewer:test", "reviewed_at": "2026-09-19T21:00:00+08:00",
                "rationale": "Need more evidence.", "route_testable": True,
            })
        with self.assertRaisesRegex(ValueError, "only allowed"):
            review_decision_from_dict({
                "review_item_id": item["review_item_id"], "decision": "DEFER",
                "reviewer_id": "reviewer:test", "reviewed_at": "2026-09-19T21:00:00+08:00",
                "rationale": "Need more evidence.", "proposed_concept_id": "concept:should-not-exist",
            })


if __name__ == "__main__":
    unittest.main()
