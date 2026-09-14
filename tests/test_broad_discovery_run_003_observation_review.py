import json
import unittest
from pathlib import Path

from scripts.build_broad_discovery_observation_review import (
    _alignment,
    _build_research_evidence,
    _combine_reviewed,
    build_observation_review,
)
from src.emergent_taxonomy import assess_reviewed_alignment
from src.observed_patterns import summarize_observed_patterns
from src.research_observation_bridge import build_reviewed_research_observations


ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "data/research_runs/BROAD_DISCOVERY_RUN_003_2026-09-14"
MISSION = ROOT / "data/research_missions/china_primary_broad_discovery.json"


def _all_keys(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from _all_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _all_keys(nested)


class BroadDiscoveryRun003ObservationReviewTests(unittest.TestCase):
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

    def test_reviewed_intake_is_bounded_and_has_exact_lineage(self):
        self.assertEqual(self.research_evidence["evidence_count"], 30)
        self.assertEqual(len(self.envelopes), 18)
        self.assertEqual(len({item.observation_id for item in self.envelopes}), 18)
        self.assertEqual(
            self.reviewed_payload["semantics"],
            "REVIEWED_SOURCE_CAPTURE_NOT_FULL_PAGE",
        )
        evidence_ids = {item["evidence_id"] for item in self.research_evidence["evidence"]}
        for item in self.reviewed_payload["records"]:
            self.assertIn(item["research_evidence_id"], evidence_ids)
            self.assertIn("NOT_FULL_PAGE", item["sampling_boundary"])

    def test_only_two_cross_level_structures_reach_promotion_review_ready(self):
        by_concept = {item.candidate_concept: item for item in self.assessments}
        self.assertEqual(len(by_concept), 5)
        ready = {item.candidate_concept for item in self.assessments if item.state == "PROMOTION_REVIEW_READY"}
        self.assertEqual(
            ready,
            {
                "SKILL_TO_WORK_MATCHING_INFRASTRUCTURE",
                "PLATFORM_TRUST_AND_GOVERNANCE_INFRASTRUCTURE",
            },
        )
        for concept in ready:
            assessment = by_concept[concept]
            self.assertEqual(assessment.observation_count, 4)
            self.assertEqual(assessment.source_count, 4)
            self.assertGreaterEqual(assessment.actor_count, 4)
            self.assertGreaterEqual(assessment.period_count, 4)
            self.assertEqual(assessment.taxonomy_promotion, "NOT_PROMOTED")
            self.assertEqual(assessment.business_promotion, "NOT_PROMOTED")

    def test_three_other_structures_remain_candidates(self):
        expected = {
            "CIRCULAR_RECOMMERCE_INFRASTRUCTURE",
            "PET_SERVICE_ECOSYSTEM_FORMALIZATION",
            "LOGISTICS_CAPACITY_ORCHESTRATION",
        }
        actual = {item.candidate_concept for item in self.assessments if item.state == "CANDIDATE"}
        self.assertEqual(actual, expected)
        for item in self.assessments:
            if item.candidate_concept in expected:
                self.assertEqual(item.observation_count, 3)
                self.assertIn("INSUFFICIENT_OBSERVATION_COUNT", item.reasons)

    def test_subsidy_counterevidence_does_not_support_circular_alignment(self):
        circular = next(
            item for item in self.alignment_payload["alignments"]
            if item["candidate_concept"] == "CIRCULAR_RECOMMERCE_INFRASTRUCTURE"
        )
        self.assertFalse(any("subsidy-demand-contamination" in ref for ref in circular["supporting_claim_refs"]))
        counter = next(
            item for item in self.reviewed_payload["records"]
            if item["observation_id"] == "bd003-obs-xz-subsidy-leverage-202606"
        )
        self.assertIn("FISCAL_LEVERAGE_NE_COUNTERFACTUAL_ORGANIC_DEMAND", counter["unknown_fields"])
        self.assertEqual(counter["claims"][0]["primitive"], "CONSTRAINT")

    def test_pet_and_logistics_boundaries_preserve_negative_evidence(self):
        pet = next(
            item for item in self.reviewed_payload["records"]
            if item["observation_id"] == "bd003-obs-cn-pet-service-use-2025"
        )
        self.assertEqual(pet["captured_payload"]["medical_share_direction_vs_2024"], "DOWN")
        self.assertIn("PET_MARKET_GROWTH_NE_ALL_SERVICE_GROWTH", pet["unknown_fields"])

        logistics = next(
            item for item in self.reviewed_payload["records"]
            if item["observation_id"] == "bd003-obs-cn-logistics-q2-202606"
        )
        self.assertEqual(logistics["captured_payload"]["average_vacancy_pct"], 18.5)
        self.assertEqual(logistics["captured_payload"]["net_absorption_qoq_pct"], 119.6)
        self.assertIn("MARKET_VACANCY_NE_CALLABLE_SPARE_CAPACITY", logistics["unknown_fields"])

    def test_semantic_alignment_does_not_manufacture_exact_observed_pattern(self):
        patterns = summarize_observed_patterns(
            self.envelopes,
            research_scope_state="BROAD_DISCOVERY_READY",
        )
        self.assertEqual(patterns["observed_pattern_count"], 0)
        self.assertGreater(patterns["unbound_pattern_count"], 0)
        self.assertEqual(patterns["business_promotion"], "NOT_PROMOTED")

    def test_generic_builder_renders_expected_run003_state(self):
        summary, observations = build_observation_review(
            mission_path=MISSION,
            dynamic_terms_path=RUN_DIR / "dynamic_terms.json",
            captures_path=RUN_DIR / "captures.json",
            reviewed_dir=RUN_DIR / "reviewed",
            alignments_path=RUN_DIR / "concept_alignments_reviewed.json",
        )
        self.assertEqual(summary["reviewed_observation_count"], 18)
        self.assertEqual(summary["alignment_state_counts"], {"CANDIDATE": 3, "PROMOTION_REVIEW_READY": 2})
        self.assertEqual(summary["exact_observed_pattern_count"], 0)
        self.assertEqual(summary["taxonomy_promotion"], "NOT_PROMOTED")
        self.assertEqual(summary["business_promotion"], "NOT_PROMOTED")
        self.assertEqual(observations["business_promotion"], "NOT_PROMOTED")
        self.assertIn("SUBSIDIZED_FLOW_NE_ORGANIC_DEMAND", summary["truth_boundaries"])

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
