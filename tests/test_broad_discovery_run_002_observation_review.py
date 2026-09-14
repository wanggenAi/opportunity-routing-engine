import json
import unittest
from pathlib import Path

from scripts.build_broad_discovery_run_002_observation_review import (
    _alignment,
    _build_research_evidence,
    _combine_reviewed,
)
from src.emergent_taxonomy import assess_reviewed_alignment
from src.observed_patterns import summarize_observed_patterns
from src.research_observation_bridge import build_reviewed_research_observations


ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "data/research_runs/BROAD_DISCOVERY_RUN_002_2026-09-14"
MISSION = ROOT / "data/research_missions/china_primary_broad_discovery.json"


def _all_keys(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from _all_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _all_keys(nested)


class BroadDiscoveryRun002ObservationReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.research_evidence = _build_research_evidence(
            MISSION,
            RUN_DIR / "dynamic_terms.json",
            RUN_DIR / "captures.json",
        )
        cls.reviewed_payload = _combine_reviewed(RUN_DIR / "reviewed")
        cls.envelopes = build_reviewed_research_observations(
            cls.research_evidence,
            cls.reviewed_payload,
        )
        cls.alignment_payload = json.loads(
            (RUN_DIR / "concept_alignments_reviewed.json").read_text(encoding="utf-8")
        )
        cls.assessments = [
            assess_reviewed_alignment(_alignment(item), cls.envelopes)
            for item in cls.alignment_payload["alignments"]
        ]

    def test_reviewed_intake_has_exact_bounded_count_and_lineage(self):
        self.assertEqual(self.research_evidence["evidence_count"], 30)
        self.assertEqual(len(self.envelopes), 17)
        self.assertEqual(len({item.observation_id for item in self.envelopes}), 17)
        self.assertEqual(
            self.reviewed_payload["semantics"],
            "REVIEWED_SOURCE_CAPTURE_NOT_FULL_PAGE",
        )
        evidence_ids = {item["evidence_id"] for item in self.research_evidence["evidence"]}
        for item in self.reviewed_payload["records"]:
            self.assertIn(item["research_evidence_id"], evidence_ids)
            self.assertIn("NOT_FULL_PAGE", item["sampling_boundary"])

    def test_only_eldercare_reaches_promotion_review_ready(self):
        by_concept = {item.candidate_concept: item for item in self.assessments}
        self.assertEqual(len(by_concept), 6)
        ready = [item for item in self.assessments if item.state == "PROMOTION_REVIEW_READY"]
        self.assertEqual([item.candidate_concept for item in ready], ["ELDERCARE_CAPACITY_ORCHESTRATION"])
        elder = by_concept["ELDERCARE_CAPACITY_ORCHESTRATION"]
        self.assertEqual(elder.observation_count, 4)
        self.assertEqual(elder.source_count, 4)
        self.assertEqual(elder.actor_count, 4)
        self.assertGreaterEqual(elder.period_count, 2)
        self.assertEqual(elder.taxonomy_promotion, "NOT_PROMOTED")
        self.assertEqual(elder.business_promotion, "NOT_PROMOTED")

    def test_other_residual_structures_remain_candidates(self):
        expected = {
            "RETAIL_FORMAT_POLARIZATION",
            "SMALL_ENTERPRISE_OPERATING_PRESSURE",
            "HOME_SERVICE_TRUSTED_FULFILLMENT_INFRASTRUCTURE",
            "PREPAID_SERVICE_TRUST_FRICTION",
            "SERVICE_AND_VALUE_SPENDING_REALLOCATION",
        }
        actual = {item.candidate_concept for item in self.assessments if item.state == "CANDIDATE"}
        self.assertEqual(actual, expected)
        for item in self.assessments:
            if item.candidate_concept in expected:
                self.assertIn("INSUFFICIENT_OBSERVATION_COUNT", item.reasons)

    def test_semantic_alignment_does_not_manufacture_exact_observed_pattern(self):
        patterns = summarize_observed_patterns(
            self.envelopes,
            research_scope_state="BROAD_DISCOVERY_READY",
        )
        self.assertEqual(patterns["observed_pattern_count"], 0)
        self.assertGreater(patterns["unbound_pattern_count"], 0)
        self.assertEqual(patterns["business_promotion"], "NOT_PROMOTED")

    def test_procurement_award_stays_below_payment_truth(self):
        procurement = next(
            item for item in self.reviewed_payload["records"]
            if item["observation_id"] == "bd002-obs-xz-longcare-outsourcing-202512"
        )
        self.assertIn("PROCUREMENT_AWARD_NE_SETTLEMENT", procurement["unknown_fields"])
        self.assertIn("BUYER_NE_PROVEN_PAYER", procurement["unknown_fields"])
        keys = set(_all_keys(procurement))
        self.assertNotIn("payer", keys)
        self.assertNotIn("paid_need", keys)
        self.assertNotIn("settled_amount", keys)

    def test_review_layer_has_no_commercial_or_route_truth(self):
        rendered = {
            "reviewed": self.reviewed_payload,
            "assessments": [item.as_dict() for item in self.assessments],
        }
        keys = set(_all_keys(rendered))
        for forbidden in (
            "payer",
            "paid_need",
            "opportunity_score",
            "commercial_score",
            "route_testable",
            "availability_confirmed",
            "permission_allowed",
        ):
            self.assertNotIn(forbidden, keys)
        self.assertTrue(all(item.business_promotion == "NOT_PROMOTED" for item in self.assessments))
        self.assertTrue(all(item.taxonomy_promotion == "NOT_PROMOTED" for item in self.assessments))


if __name__ == "__main__":
    unittest.main()
