import unittest

from src.structure_validation_planning import (
    build_structure_field_packets,
    build_structure_validation_queue,
    normalize_structure_validation_profile,
)


class StructureValidationPlanningTests(unittest.TestCase):
    def _artifact(self, *, concept="GENERIC_RECURRING_STRUCTURE"):
        return {
            "candidate_id": "STRUCTURE-GENERIC-001",
            "candidate_concept": concept,
            "commercial_structure_state": "STRUCTURE_VALIDATION_READY",
            "missing_dimensions": ["COMPOUNDING"],
            "business_promotion": "NOT_PROMOTED",
        }

    def test_ready_structure_yields_three_bounded_domain_neutral_tasks(self):
        queue = build_structure_validation_queue(self._artifact())
        self.assertEqual(queue["task_count"], 3)
        self.assertEqual(
            {task["target_gate"] for task in queue["tasks"]},
            {"LOCAL_CASE_PANEL", "LOCAL_PAID_MANDATE", "COMPOUNDING"},
        )
        panel = next(task for task in queue["tasks"] if task["target_gate"] == "LOCAL_CASE_PANEL")
        required = panel["capture_contract"]["required_fields"]
        self.assertIn("focal_actor", required)
        self.assertIn("recurring_event_type", required)
        self.assertIn("transformation_or_routing_steps", required)
        self.assertNotIn("asset_identity", required)
        self.assertNotIn("underuse_evidence", required)
        compounding = next(task for task in queue["tasks"] if task["target_gate"] == "COMPOUNDING")
        self.assertEqual(compounding["task_role"], "CORE_MISSING_DIMENSION")
        self.assertEqual(compounding["capture_contract"]["min_later_cases"], 2)
        self.assertIn("reused_routing_refs", compounding["capture_contract"]["required_reuse_fields"])
        self.assertIn("cycle_days", compounding["capture_contract"]["predeclared_metrics"])
        self.assertEqual(queue["business_promotion"], "NOT_PROMOTED")

    def test_reviewed_profile_can_customize_case_and_metrics_without_changing_truth(self):
        profile = {
            "profile_id": "TEST_PROCESS_PROFILE",
            "candidate_concept": "GENERIC_RECURRING_STRUCTURE",
            "geography_scope": ["CN-JS-XUZHOU"],
            "case_unit": "DEIDENTIFIED_PROCESS_EPISODE",
            "local_case_required_fields": ["case_id", "focal_actor", "cycle_days", "source_refs"],
            "local_paid_required_fields": ["mandate_id", "payer_actor", "settlement_state", "source_refs"],
            "compounding_reuse_fields": ["reused_rule_refs", "reused_prior_outcome_refs"],
            "compounding_metrics": ["cycle_days", "acceptance_state"],
            "privacy_constraints": ["NO_PERSONAL_DATA"],
            "prohibited_fields": ["person_name"],
        }
        queue = build_structure_validation_queue(self._artifact(), profile=profile)
        self.assertEqual(queue["validation_profile"]["profile_id"], "TEST_PROCESS_PROFILE")
        self.assertEqual(queue["validation_profile"]["case_unit"], "DEIDENTIFIED_PROCESS_EPISODE")
        self.assertEqual(queue["validation_profile"]["privacy_constraints"], ["NO_PERSONAL_DATA"])
        self.assertEqual(queue["business_promotion"], "NOT_PROMOTED")
        packets = build_structure_field_packets(queue)
        self.assertEqual(packets["validation_profile_id"], "TEST_PROCESS_PROFILE")
        self.assertTrue(all("NO_PERSONAL_DATA" in packet["privacy_constraints"] for packet in packets["packets"]))

    def test_profile_concept_mismatch_and_prohibited_required_overlap_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "candidate_concept"):
            normalize_structure_validation_profile(
                {"profile_id": "x", "candidate_concept": "OTHER"},
                candidate_concept="GENERIC_RECURRING_STRUCTURE",
            )
        with self.assertRaisesRegex(ValueError, "prohibited fields"):
            normalize_structure_validation_profile(
                {
                    "profile_id": "x",
                    "local_case_required_fields": ["case_id", "secret_field"],
                    "prohibited_fields": ["secret_field"],
                },
                candidate_concept="GENERIC_RECURRING_STRUCTURE",
            )

    def test_paid_mandate_requires_settlement_payment_and_rejects_contract_as_substitute(self):
        queue = build_structure_validation_queue(self._artifact())
        task = next(task for task in queue["tasks"] if task["target_gate"] == "LOCAL_PAID_MANDATE")
        self.assertIn("signed contract without settlement/payment", task["fail_condition"])
        self.assertIn("signed contract != settlement", task["forbidden_inference"])
        self.assertEqual(task["state_effect"], "LOCAL_CORROBORATION_ONLY_NOT_GLOBAL_GATE_PROMOTION")

    def test_compounding_requires_reused_artifacts_time_order_and_outcome_metrics(self):
        queue = build_structure_validation_queue(self._artifact())
        task = next(task for task in queue["tasks"] if task["target_gate"] == "COMPOUNDING")
        capture = task["capture_contract"]
        self.assertIn("reused_template_refs", capture["required_reuse_fields"])
        self.assertIn("reused_prior_outcome_refs", capture["required_reuse_fields"])
        self.assertIn("cycle_days", capture["predeclared_metrics"])
        self.assertIn("acceptance_state", capture["predeclared_metrics"])
        self.assertIn("one-time efficiency gain", task["forbidden_inference"])
        self.assertIn("TIME_ORDERED", capture["comparison_policy"])

    def test_field_packets_remain_execution_plans_not_evidence(self):
        queue = build_structure_validation_queue(self._artifact())
        packets = build_structure_field_packets(queue)
        self.assertEqual(packets["packet_count"], 3)
        self.assertEqual(packets["business_promotion"], "NOT_PROMOTED")
        for packet in packets["packets"]:
            self.assertTrue(packet["questions"])
            self.assertIsNotNone(packet["capture_contract"])
            self.assertNotIn("evidence_state", packet)
            self.assertNotIn("opportunity_score", packet)

    def test_non_ready_or_extra_missing_dimension_fails_closed(self):
        artifact = self._artifact()
        artifact["commercial_structure_state"] = "STRUCTURE_HYPOTHESIS"
        with self.assertRaisesRegex(ValueError, "STRUCTURE_VALIDATION_READY"):
            build_structure_validation_queue(artifact)

        artifact = self._artifact()
        artifact["missing_dimensions"] = ["COMPOUNDING", "REPEAT_MONETIZATION"]
        with self.assertRaisesRegex(ValueError, "single remaining COMPOUNDING"):
            build_structure_validation_queue(artifact)


if __name__ == "__main__":
    unittest.main()
