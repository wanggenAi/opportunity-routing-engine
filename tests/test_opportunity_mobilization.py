import unittest

from src.missing_edge_gate import ReachabilityGrade
from src.opportunity_mobilization import (
    MobilizationEvidence,
    MobilizationGrade,
    OpportunityMobilizationProfile,
    bilateral_pull,
    current_stage_mobilization_priority_allowed,
    mobilization_grade,
    mobilization_index,
    validate_mobilization,
)


class OpportunityMobilizationTests(unittest.TestCase):
    def _e(self, suffix: str) -> tuple[MobilizationEvidence, ...]:
        return (MobilizationEvidence(f"source:{suffix}", f"observed {suffix} behavior"),)

    def _profile(self, **overrides) -> OpportunityMobilizationProfile:
        payload = dict(
            candidate_id="CAND-001",
            demand_actor="SME buyer",
            supply_actor="replaceable capability providers",
            payer="SME buyer",
            operator_role="task schema + routing + acceptance + settlement",
            task_unit="one bounded paid task",
            money_flow="buyer -> orchestrator -> provider",
            missing_edge="task packaging / trust / acceptance / routing",
            demand_urgency=3,
            supply_hunger=3,
            resource_abundance=2,
            activation_ease=3,
            value_capture=2,
            repeatability=2,
            self_propulsion=2,
            operator_exit=2,
            demand_pull_evidence=self._e("demand"),
            supply_hunger_evidence=self._e("supply"),
            resource_abundance_evidence=self._e("abundance"),
            activation_evidence=self._e("activation"),
            value_capture_evidence=self._e("value"),
            repeatability_evidence=self._e("repeat"),
            self_propulsion_evidence=self._e("self"),
            operator_exit_evidence=self._e("exit"),
        )
        payload.update(overrides)
        return OpportunityMobilizationProfile(**payload)

    def test_high_mobilization_requires_bilateral_pull_and_all_core_dimensions(self):
        profile = self._profile()
        self.assertEqual(validate_mobilization(profile), [])
        self.assertTrue(bilateral_pull(profile))
        self.assertEqual(mobilization_grade(profile), MobilizationGrade.HIGH)
        self.assertGreater(mobilization_index(profile), 0)
        self.assertTrue(
            current_stage_mobilization_priority_allowed(profile, ReachabilityGrade.A)
        )

    def test_one_sided_demand_is_low_not_attractive_story(self):
        profile = self._profile(supply_hunger=1)
        self.assertFalse(bilateral_pull(profile))
        self.assertEqual(mobilization_grade(profile), MobilizationGrade.LOW)
        self.assertFalse(
            current_stage_mobilization_priority_allowed(profile, ReachabilityGrade.A)
        )

    def test_founder_hustle_does_not_count_as_self_propulsion(self):
        delivery_bound = self._profile(founder_delivery_required=True)
        sales_bound = self._profile(founder_sales_required_per_transaction=True)
        self.assertEqual(mobilization_grade(delivery_bound), MobilizationGrade.LOW)
        self.assertEqual(mobilization_grade(sales_bound), MobilizationGrade.LOW)

    def test_zero_value_capture_collapses_index_and_grade(self):
        profile = self._profile(value_capture=0, value_capture_evidence=())
        self.assertEqual(validate_mobilization(profile), [])
        self.assertEqual(mobilization_index(profile), 0.0)
        self.assertEqual(mobilization_grade(profile), MobilizationGrade.LOW)

    def test_nonzero_score_requires_evidence(self):
        profile = self._profile(supply_hunger_evidence=())
        self.assertIn("missing_evidence:supply_hunger", validate_mobilization(profile))
        self.assertEqual(mobilization_grade(profile), MobilizationGrade.UNASSESSED)
        self.assertEqual(mobilization_index(profile), 0.0)

    def test_unreachable_high_mobilization_is_not_current_stage_priority(self):
        profile = self._profile()
        self.assertEqual(mobilization_grade(profile), MobilizationGrade.HIGH)
        self.assertFalse(
            current_stage_mobilization_priority_allowed(profile, ReachabilityGrade.C)
        )


if __name__ == "__main__":
    unittest.main()
