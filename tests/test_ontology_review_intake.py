import json
import unittest
from dataclasses import replace
from pathlib import Path

from src.ontology_review_intake import (
    REGISTRY_EFFECT,
    SQLiteOntologyReviewDecisionStore,
    review_decision_event_from_record,
    review_item_fingerprint,
    review_items_by_id,
    review_outcome_for_decision,
    validate_review_event_against_item,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures"
QUEUE_PATH = FIXTURES / "ontology_review_queue_dry_run.json"
DECISIONS_PATH = FIXTURES / "ontology_review_decisions_dry_run.json"


class OntologyReviewIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
        cls.items = review_items_by_id(cls.queue)
        cls.item = next(iter(cls.items.values()))
        cls.records = json.loads(DECISIONS_PATH.read_text(encoding="utf-8"))
        cls.events = [review_decision_event_from_record(record) for record in cls.records]

    def test_synthetic_fixture_is_explicitly_non_production(self):
        self.assertTrue(self.queue["source_review_run_id"].startswith("SYNTHETIC_"))
        self.assertEqual(self.queue["active_ontology_changes"], 0)
        self.assertEqual(self.queue["taxonomy_promotion"], "NOT_PROMOTED")
        self.assertEqual(self.queue["business_promotion"], "NOT_PROMOTED")
        for event in self.events:
            self.assertTrue(event.review_provenance_ref.startswith("fixture://"))

    def test_decision_classes_cover_accept_reject_revise_and_defer(self):
        self.assertEqual(review_outcome_for_decision("APPROVE_NEW_CONCEPT_VERSION"), "ACCEPT")
        self.assertEqual(review_outcome_for_decision("REJECT"), "REJECT")
        self.assertEqual(review_outcome_for_decision("DEFER"), "DEFER")
        self.assertEqual(review_outcome_for_decision("REQUIRE_RENAME_REVIEW"), "REVISE")
        self.assertEqual(review_outcome_for_decision("REQUIRE_MERGE_REVIEW"), "REVISE")
        self.assertEqual(review_outcome_for_decision("REQUIRE_SPLIT_REVIEW"), "REVISE")

    def test_fixture_defer_then_accept_is_append_only_and_has_zero_registry_effect(self):
        with SQLiteOntologyReviewDecisionStore(":memory:") as store:
            store.append(self.events[0], self.item)
            store.append(self.events[1], self.item)
            store.append(self.events[1], self.item)
            snapshot = store.snapshot()

        self.assertEqual(snapshot["decision_event_count"], 2)
        self.assertEqual(snapshot["review_item_count"], 1)
        self.assertEqual(snapshot["terminal_decision_count"], 1)
        self.assertEqual(snapshot["active_ontology_changes"], 0)
        self.assertEqual(snapshot["registry_effect"], REGISTRY_EFFECT)
        self.assertEqual(snapshot["taxonomy_promotion"], "NOT_PROMOTED")
        self.assertEqual(snapshot["business_promotion"], "NOT_PROMOTED")
        self.assertEqual(snapshot["events"][1]["review_outcome"], "ACCEPT")
        self.assertEqual(
            snapshot["events"][1]["review_item_fingerprint"],
            review_item_fingerprint(self.item),
        )

    def test_validation_binds_boundary_counterexamples_and_known_evidence(self):
        event = self.events[0]
        validate_review_event_against_item(event, self.item)

        with self.assertRaisesRegex(ValueError, "reviewed_boundary"):
            validate_review_event_against_item(
                replace(event, reviewed_boundary="Different boundary"), self.item
            )
        with self.assertRaisesRegex(ValueError, "reviewed_counterexamples"):
            validate_review_event_against_item(
                replace(event, reviewed_counterexamples=("Different counterexample",)), self.item
            )
        with self.assertRaisesRegex(ValueError, "not present"):
            validate_review_event_against_item(
                replace(event, supporting_evidence_refs=("claim:not-in-queue",)), self.item
            )

    def test_accept_must_explicitly_reference_every_supporting_claim(self):
        approval = self.events[1]
        with self.assertRaisesRegex(ValueError, "every supporting claim"):
            validate_review_event_against_item(
                replace(approval, supporting_evidence_refs=("claim:synthetic:001",)), self.item
            )

    def test_strict_schema_rejects_truth_smuggling_and_unknown_fields(self):
        payload = dict(self.records[0])
        payload["payer_confirmed"] = True
        with self.assertRaisesRegex(ValueError, "truth fields"):
            review_decision_event_from_record(payload)

        payload = dict(self.records[0])
        payload["confidence"] = 0.99
        with self.assertRaisesRegex(ValueError, "unknown ontology review intake fields"):
            review_decision_event_from_record(payload)

    def test_review_provenance_and_timezone_are_required(self):
        payload = dict(self.records[0])
        payload["review_provenance_ref"] = ""
        with self.assertRaisesRegex(ValueError, "review_provenance_ref"):
            review_decision_event_from_record(payload)

        payload = dict(self.records[0])
        payload["reviewed_at"] = "2026-09-14T23:45:00"
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            review_decision_event_from_record(payload)

    def test_revision_requires_instruction_and_cannot_smuggle_concept_identity(self):
        payload = dict(self.records[0])
        payload.update(
            {
                "decision_id": "decision:synthetic-dry-run:revision",
                "decision": "REQUIRE_RENAME_REVIEW",
                "review_outcome": "REVISE",
                "revision_instruction": "Clarify the label so it names the structure rather than a channel.",
            }
        )
        revision = review_decision_event_from_record(payload)
        self.assertEqual(revision.review_outcome, "REVISE")
        validate_review_event_against_item(revision, self.item)

        missing = dict(payload)
        missing.pop("revision_instruction")
        with self.assertRaisesRegex(ValueError, "revision_instruction"):
            review_decision_event_from_record(missing)

        smuggled = dict(payload)
        smuggled["proposed_concept_id"] = "concept:not-allowed"
        with self.assertRaisesRegex(ValueError, "only allowed"):
            review_decision_event_from_record(smuggled)

    def test_terminal_decision_closes_same_review_item_and_time_cannot_move_backwards(self):
        with SQLiteOntologyReviewDecisionStore(":memory:") as store:
            store.append(self.events[0], self.item)
            earlier = replace(
                self.events[0],
                decision_id="decision:synthetic-dry-run:earlier",
                reviewed_at="2026-09-14T23:44:00+08:00",
            )
            with self.assertRaisesRegex(ValueError, "cannot move backwards"):
                store.append(earlier, self.item)

            store.append(self.events[1], self.item)
            later_defer = replace(
                self.events[0],
                decision_id="decision:synthetic-dry-run:after-terminal",
                reviewed_at="2026-09-14T23:47:00+08:00",
            )
            with self.assertRaisesRegex(ValueError, "terminal decision"):
                store.append(later_defer, self.item)

    def test_decision_id_is_immutable_and_queue_fingerprint_detects_drift(self):
        with SQLiteOntologyReviewDecisionStore(":memory:") as store:
            store.append(self.events[0], self.item)
            mutated = replace(self.events[0], rationale="Changed rationale")
            with self.assertRaisesRegex(ValueError, "different content"):
                store.append(mutated, self.item)

            changed_item = dict(self.item)
            changed_item["definition"] = self.item["definition"] + " Changed."
            with self.assertRaisesRegex(ValueError, "review item changed"):
                store.append(self.events[0], changed_item)

    def test_audited_event_projects_to_governance_decision_without_registry_mutation(self):
        governance = validate_review_event_against_item(self.events[1], self.item)
        self.assertEqual(governance.decision, "APPROVE_NEW_CONCEPT_VERSION")
        self.assertEqual(governance.review_item_id, self.item["review_item_id"])
        self.assertEqual(governance.proposed_label, "SYNTHETIC_DRY_RUN_ONLY_CONCEPT")


if __name__ == "__main__":
    unittest.main()
