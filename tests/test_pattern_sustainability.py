import unittest

from src.pattern_sustainability import (
    assess_pattern_sustainability,
    summarize_pattern_sustainability,
)


class PatternSustainabilityTests(unittest.TestCase):
    def _pattern(self, **overrides):
        value = {
            "pattern_id": "pattern-1",
            "state": "OBSERVED_PATTERN",
            "primitive": "RESOURCE",
            "concept": "PUBLICLY_LISTED_ASSET_OR_RIGHT",
            "geography": "CN-JS-XZ",
            "observation_count": 6,
            "actor_count": 3,
            "source_count": 2,
            "period_count": 2,
            "supporting_observation_refs": ["A::1", "A::2", "B::3", "B::4", "B::5", "B::6"],
            "supporting_actor_ids": ["actor-a", "actor-b", "actor-c"],
            "supporting_periods": ["2026-09-13", "2026-09-14"],
            "evidence_cautions": [],
            "business_promotion": "NOT_PROMOTED",
        }
        value.update(overrides)
        return value

    def test_observed_recurrence_does_not_self_promote_to_business(self):
        assessment = assess_pattern_sustainability(self._pattern())
        self.assertEqual(assessment.core_business_state, "PATTERN_ONLY")
        self.assertEqual(assessment.business_promotion, "NOT_PROMOTED")
        self.assertEqual(assessment.axes["RECURRENCE"].state, "EVIDENCED")
        self.assertEqual(assessment.axes["POPULATION"].state, "EVIDENCED")
        self.assertEqual(assessment.axes["STANDARDIZABILITY"].state, "UNKNOWN")
        self.assertEqual(assessment.axes["REPEAT_MONETIZATION"].state, "UNKNOWN")
        self.assertEqual(assessment.axes["COMPOUNDING"].state, "UNKNOWN")
        self.assertEqual(assessment.regenerating_event_flow.state, "UNKNOWN")
        self.assertEqual(assessment.complementary_actor_structure.state, "UNKNOWN")

    def test_missing_core_gates_match_sustainable_business_requirements(self):
        assessment = assess_pattern_sustainability(self._pattern())
        self.assertEqual(
            set(assessment.missing_core_gates),
            {
                "STANDARDIZABILITY",
                "REPEAT_MONETIZATION",
                "COMPOUNDING",
                "REGENERATING_EVENT_FLOW",
                "COMPLEMENTARY_ACTOR_STRUCTURE",
            },
        )
        task_types = {task["task_type"] for task in assessment.validation_tasks}
        self.assertIn("ESTABLISH_REUSABLE_TRANSFORMATION_MECHANISM", task_types)
        self.assertIn("ESTABLISH_REPEAT_MONETIZATION", task_types)
        self.assertIn("ESTABLISH_COMPOUNDING_MECHANISM", task_types)

    def test_calibration_assessment_can_suppress_operator_tasks(self):
        assessment = assess_pattern_sustainability(
            self._pattern(),
            allow_validation_tasks=False,
        )
        self.assertEqual(assessment.validation_tasks, ())
        self.assertEqual(assessment.core_business_state, "PATTERN_ONLY")
        self.assertEqual(assessment.axes["STANDARDIZABILITY"].state, "UNKNOWN")

    def test_unbound_pattern_cannot_enter_sustainability_gate(self):
        with self.assertRaisesRegex(ValueError, "only OBSERVED_PATTERN"):
            assess_pattern_sustainability(self._pattern(state="UNBOUND"))

    def test_source_pattern_business_boundary_is_enforced(self):
        with self.assertRaisesRegex(ValueError, "business-promotion boundary"):
            assess_pattern_sustainability(self._pattern(business_promotion="PROMOTED"))

    def test_single_source_caution_is_preserved_not_hidden(self):
        assessment = assess_pattern_sustainability(
            self._pattern(source_count=1, evidence_cautions=["SINGLE_SOURCE_ONLY"])
        )
        self.assertEqual(assessment.evidence_cautions, ("SINGLE_SOURCE_ONLY",))
        self.assertEqual(assessment.axes["RECURRENCE"].state, "EVIDENCED")
        self.assertEqual(assessment.axes["STANDARDIZABILITY"].state, "UNKNOWN")

    def test_calibration_summary_assesses_patterns_but_creates_no_execution_backlog(self):
        source = {
            "business_promotion": "NOT_PROMOTED",
            "research_scope_state": "CALIBRATION_ONLY",
            "source_observation_run_id": 99,
            "observed_pattern_count": 1,
            "patterns": [
                self._pattern(),
                self._pattern(
                    pattern_id="pattern-2",
                    state="UNBOUND",
                    concept="DECLARED_PROCUREMENT_BUDGET",
                ),
            ],
        }
        result = summarize_pattern_sustainability(source, source_pattern_run_id=123)
        self.assertEqual(result["source_pattern_run_id"], 123)
        self.assertEqual(result["source_observation_run_id"], 99)
        self.assertEqual(result["source_research_scope_state"], "CALIBRATION_ONLY")
        self.assertFalse(result["validation_execution_authorized"])
        self.assertEqual(result["assessment_count"], 1)
        self.assertEqual(result["validation_task_count"], 0)
        self.assertEqual(result["core_business_candidate_count"], 0)
        self.assertEqual(result["business_promotion"], "NOT_PROMOTED")
        self.assertEqual(result["assessments"][0]["pattern_id"], "pattern-1")
        self.assertEqual(result["assessments"][0]["validation_tasks"], [])

    def test_broad_research_scope_can_create_validation_tasks_but_not_core_candidate(self):
        source = {
            "business_promotion": "NOT_PROMOTED",
            "research_scope_state": "BROAD_DISCOVERY_READY",
            "source_observation_run_id": 99,
            "observed_pattern_count": 1,
            "patterns": [self._pattern()],
        }
        result = summarize_pattern_sustainability(source)
        self.assertTrue(result["validation_execution_authorized"])
        self.assertEqual(result["validation_task_count"], 5)
        self.assertEqual(result["core_business_candidate_count"], 0)
        self.assertEqual(result["business_promotion"], "NOT_PROMOTED")


if __name__ == "__main__":
    unittest.main()
