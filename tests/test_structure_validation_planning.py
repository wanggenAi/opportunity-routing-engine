import unittest

from src.structure_validation_planning import (
    build_structure_field_packets,
    build_structure_validation_queue,
)


class StructureValidationPlanningTests(unittest.TestCase):
    def _artifact(self):
        return {
            "candidate_id": "LV-STRUCTURE-IDLE-ASSET-REPURPOSING-001",
            "candidate_concept": "IDLE_ASSET_SCENARIO_REPURPOSING",
            "commercial_structure_state": "STRUCTURE_VALIDATION_READY",
            "missing_dimensions": ["COMPOUNDING"],
            "business_promotion": "NOT_PROMOTED",
        }

    def test_ready_structure_yields_three_bounded_tasks(self):
        queue = build_structure_validation_queue(self._artifact())
        self.assertEqual(queue["task_count"], 3)
        self.assertEqual(
            {task["target_gate"] for task in queue["tasks"]},
            {"LOCAL_CASE_PANEL", "LOCAL_PAID_MANDATE", "COMPOUNDING"},
        )
        compounding = next(task for task in queue["tasks"] if task["target_gate"] == "COMPOUNDING")
        self.assertEqual(compounding["task_role"], "CORE_MISSING_DIMENSION")
        self.assertEqual(compounding["capture_contract"]["min_later_cases"], 2)
        self.assertIn("search_minutes", compounding["capture_contract"]["predeclared_metrics"])
        self.assertEqual(queue["business_promotion"], "NOT_PROMOTED")

    def test_local_case_panel_requires_multiple_owners_and_current_cases(self):
        queue = build_structure_validation_queue(self._artifact())
        panel = next(task for task in queue["tasks"] if task["target_gate"] == "LOCAL_CASE_PANEL")
        self.assertGreaterEqual(panel["capture_contract"]["target_case_count_min"], 5)
        self.assertGreaterEqual(panel["capture_contract"]["min_independent_owners"], 3)
        self.assertIn("owner_actor", panel["capture_contract"]["required_fields"])
        self.assertIn("underuse_evidence", panel["capture_contract"]["required_fields"])

    def test_paid_mandate_rejects_budget_or_award_as_payment(self):
        queue = build_structure_validation_queue(self._artifact())
        task = next(task for task in queue["tasks"] if task["target_gate"] == "LOCAL_PAID_MANDATE")
        self.assertIn("settlement/payment proof", task["fail_condition"])
        self.assertIn("tender budget/award != payment", task["forbidden_inference"])
        self.assertEqual(task["state_effect"], "LOCAL_CORROBORATION_ONLY_NOT_GLOBAL_GATE_PROMOTION")

    def test_compounding_requires_reused_artifacts_and_outcome_metrics(self):
        queue = build_structure_validation_queue(self._artifact())
        task = next(task for task in queue["tasks"] if task["target_gate"] == "COMPOUNDING")
        capture = task["capture_contract"]
        self.assertIn("reused_template_refs", capture["required_reuse_fields"])
        self.assertIn("cycle_days", capture["predeclared_metrics"])
        self.assertIn("acceptance_state", capture["predeclared_metrics"])
        self.assertIn("database size", task["forbidden_inference"])

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
