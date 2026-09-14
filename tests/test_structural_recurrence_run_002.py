import json
import unittest
from pathlib import Path

from src.emergent_taxonomy import ReviewedConceptAlignment, assess_reviewed_alignment
from src.observed_patterns import summarize_observed_patterns
from src.research_control_plane import (
    assess_research_coverage,
    build_research_plan,
    evidence_from_dict,
    mission_from_dict,
)
from src.research_observation_bridge import build_reviewed_research_observations


PARENT = Path("data/research_runs/BROAD_DISCOVERY_RUN_001_2026-09-14")
RUN = Path("data/research_runs/STRUCTURAL_RECURRENCE_RUN_002_2026-09-14")
MISSION = Path("data/research_missions/china_primary_broad_discovery.json")


def _obj(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _alignment(raw: dict) -> ReviewedConceptAlignment:
    return ReviewedConceptAlignment(
        alignment_id=raw["alignment_id"],
        candidate_concept=raw["candidate_concept"],
        primitive=raw["primitive"],
        definition=raw["definition"],
        boundary=raw["boundary"],
        counterexamples=tuple(raw["counterexamples"]),
        supporting_claim_refs=tuple(raw["supporting_claim_refs"]),
        alignment_rationale=raw["alignment_rationale"],
    )


class StructuralRecurrenceRun002Tests(unittest.TestCase):
    def _envelopes(self):
        parent = build_reviewed_research_observations(
            _obj(PARENT / "evidence.json"), _obj(PARENT / "reviewed_observations.json")
        )
        current = build_reviewed_research_observations(
            _obj(RUN / "evidence.json"), _obj(RUN / "reviewed_observations.json")
        )
        return parent, current, parent + current

    def test_targeted_evidence_uses_dynamic_plan_but_is_not_broad_coverage(self):
        mission = mission_from_dict(_obj(MISSION))
        terms = _obj(PARENT / "dynamic_terms.json")["dynamic_terms"]
        plan = build_research_plan(mission, dynamic_terms=terms)
        evidence_payload = _obj(RUN / "evidence.json")
        records = [evidence_from_dict(item) for item in evidence_payload["evidence"]]
        plan_ids = {item["query_id"] for item in plan["queries"]}
        self.assertTrue({item.query_id for item in records}.issubset(plan_ids))
        coverage = assess_research_coverage(mission, plan, records)
        self.assertEqual(coverage.state, "PARTIAL_DISCOVERY")
        self.assertFalse(coverage.broad_discovery_use_authorized)
        self.assertTrue(any(value.startswith("MISSING_RESEARCH_LANES:") for value in coverage.blockers))

    def test_idle_asset_alignment_is_ready_for_taxonomy_review_not_promotion(self):
        _, _, envelopes = self._envelopes()
        raw = _obj(RUN / "concept_alignments.json")["alignments"][0]
        assessment = assess_reviewed_alignment(_alignment(raw), envelopes)
        self.assertEqual(assessment.candidate_concept, "IDLE_ASSET_SCENARIO_REPURPOSING")
        self.assertEqual(assessment.state, "PROMOTION_REVIEW_READY")
        self.assertGreaterEqual(assessment.observation_count, 4)
        self.assertGreaterEqual(assessment.source_count, 2)
        self.assertGreaterEqual(assessment.actor_count, 2)
        self.assertGreaterEqual(assessment.period_count, 2)
        self.assertEqual(assessment.taxonomy_promotion, "NOT_PROMOTED")
        self.assertEqual(assessment.business_promotion, "NOT_PROMOTED")
        self.assertIn("IDLE_SPACE_SCENARIO_REPURPOSING", assessment.source_concepts)
        self.assertIn("DIVERSE_IDLE_ASSET_FUNCTIONAL_RESHAPING_AND_SCENE_REDESIGN", assessment.source_concepts)
        self.assertGreater(assessment.epistemic_counts.get("REPORTED", 0), 0)

    def test_ai_human_escalation_alignment_stays_candidate(self):
        _, _, envelopes = self._envelopes()
        raw = _obj(RUN / "concept_alignments.json")["alignments"][1]
        assessment = assess_reviewed_alignment(_alignment(raw), envelopes)
        self.assertEqual(assessment.candidate_concept, "AI_HUMAN_ESCALATION_FRICTION")
        self.assertEqual(assessment.state, "CANDIDATE")
        self.assertIn("INSUFFICIENT_OBSERVATION_COUNT", assessment.reasons)
        self.assertIn("INSUFFICIENT_ACTOR_DIVERSITY", assessment.reasons)
        self.assertEqual(assessment.taxonomy_promotion, "NOT_PROMOTED")
        self.assertEqual(assessment.business_promotion, "NOT_PROMOTED")

    def test_alignment_does_not_rewrite_exact_source_concepts_or_create_pattern(self):
        _, _, envelopes = self._envelopes()
        exact = summarize_observed_patterns(
            envelopes, research_scope_state="BROAD_DISCOVERY_READY"
        )
        self.assertEqual(exact["observed_pattern_count"], 0)
        self.assertEqual(exact["business_promotion"], "NOT_PROMOTED")
        concepts = {
            claim.concept
            for envelope in envelopes
            for claim in envelope.claims
        }
        self.assertNotIn("IDLE_ASSET_SCENARIO_REPURPOSING", concepts)
        self.assertNotIn("AI_HUMAN_ESCALATION_FRICTION", concepts)

    def test_alignment_rejects_unknown_or_cross_primitive_claim(self):
        _, _, envelopes = self._envelopes()
        raw = _obj(RUN / "concept_alignments.json")["alignments"][0]
        unknown = dict(raw)
        unknown["supporting_claim_refs"] = list(raw["supporting_claim_refs"]) + ["missing::claim::ref"]
        with self.assertRaisesRegex(ValueError, "unknown claims"):
            assess_reviewed_alignment(_alignment(unknown), envelopes)

        cross = dict(raw)
        cross["supporting_claim_refs"] = [
            "JIANGSU_URBAN_RENEWAL_POLICY::sr002-obs-js-idle-asset-policy-20260521::repurposing-policy"
        ]
        with self.assertRaisesRegex(ValueError, "primitive mismatch"):
            assess_reviewed_alignment(_alignment(cross), envelopes)


if __name__ == "__main__":
    unittest.main()
