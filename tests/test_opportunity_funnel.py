import copy
import unittest

from src.opportunity_funnel import build_opportunity_funnel


class OpportunityFunnelTests(unittest.TestCase):
    def _ledger(self):
        return {
            "geography": "Xuzhou",
            "records": [
                {
                    "record_id": "PAIR::near",
                    "status": "PAIR_HYPOTHESIS",
                    "capability_key": "A",
                    "geography": "Xuzhou",
                    "need_signal_id": "need-a",
                    "resource_signal_id": "resource-a",
                    "need_evidence_state": "PAID",
                    "resource_state": "DISCOVERED",
                },
                {
                    "record_id": "PAIR::far",
                    "status": "PAIR_HYPOTHESIS",
                    "capability_key": "B",
                    "geography": "Xuzhou",
                    "need_signal_id": "need-b",
                    "resource_signal_id": "resource-b",
                    "need_evidence_state": "OBSERVED",
                    "resource_state": "DISCOVERED",
                },
                {
                    "record_id": "NEED::1",
                    "status": "NEED_ONLY",
                    "capability_key": "C",
                    "geography": "Xuzhou",
                },
            ],
        }

    def _queue(self):
        return {
            "pairs": [
                {"record_id": "PAIR::near", "missing_gate_count": 1},
                {"record_id": "PAIR::far", "missing_gate_count": 3},
            ],
            "tasks": [
                {
                    "task_id": "task-near-blocker",
                    "record_id": "PAIR::near",
                    "target_gate": "TRANSACTION_BLOCKER",
                    "priority": 40,
                },
                {
                    "task_id": "task-far-payer",
                    "record_id": "PAIR::far",
                    "target_gate": "PAYER_IDENTITY",
                    "priority": 10,
                },
                {
                    "task_id": "task-far-underuse",
                    "record_id": "PAIR::far",
                    "target_gate": "RESOURCE_UNDERUSE",
                    "priority": 30,
                },
                {
                    "task_id": "task-far-blocker",
                    "record_id": "PAIR::far",
                    "target_gate": "TRANSACTION_BLOCKER",
                    "priority": 40,
                },
            ],
        }

    def _packets(self):
        return {
            "packets": [
                {
                    "packet_id": "FIELD::task-near-blocker",
                    "record_id": "PAIR::near",
                    "target_gate": "TRANSACTION_BLOCKER",
                }
            ]
        }

    def test_focus_orders_by_evidence_distance_not_commercial_score(self):
        result = build_opportunity_funnel(self._ledger(), self._queue(), self._packets())
        self.assertEqual(
            [item["record_id"] for item in result["validation_focus"]],
            ["PAIR::near", "PAIR::far"],
        )
        self.assertEqual(
            result["ordering_basis"],
            "EVIDENCE_DISTANCE_ONLY_NOT_COMMERCIAL_RANKING",
        )
        self.assertNotIn("score", result["validation_focus"][0])
        self.assertEqual(result["batch_next_action"], "EXECUTE_PAIR_VALIDATION_FOCUS")

    def test_route_testable_switches_batch_to_transaction_test_without_promoting_anything(self):
        ledger = self._ledger()
        ledger["records"].append(
            {
                "record_id": "PAIR::ready",
                "status": "ROUTE_TESTABLE",
                "capability_key": "D",
                "geography": "Xuzhou",
            }
        )
        before = copy.deepcopy(ledger)
        result = build_opportunity_funnel(ledger, self._queue(), self._packets())
        self.assertTrue(result["transaction_test_ready"])
        self.assertEqual(result["route_testable_count"], 1)
        self.assertEqual(result["batch_next_action"], "RUN_BOUNDED_TRANSACTION_TEST")
        self.assertEqual(
            result["route_testable_records"][0]["next_action"],
            "RUN_BOUNDED_TRANSACTION_TEST",
        )
        self.assertEqual(ledger, before)

    def test_only_pair_hypotheses_enter_validation_focus(self):
        result = build_opportunity_funnel(
            self._ledger(), self._queue(), self._packets(), focus_limit=1
        )
        self.assertEqual(result["validation_focus_count"], 1)
        self.assertEqual(result["validation_focus"][0]["status"], "PAIR_HYPOTHESIS")
        need = next(item for item in result["records"] if item["status"] == "NEED_ONLY")
        self.assertEqual(need["lane"], "SUPPLY_DISCOVERY")
        self.assertEqual(need["next_action"], "DISCOVER_COMPATIBLE_RESOURCE")

    def test_missing_queue_coverage_is_surfaced_not_guessed(self):
        result = build_opportunity_funnel(self._ledger(), {}, {})
        pair = next(
            item for item in result["records"] if item["record_id"] == "PAIR::near"
        )
        self.assertIsNone(pair["missing_gate_count"])
        self.assertEqual(pair["missing_gates"], [])
        self.assertEqual(
            pair["next_action"],
            "REBUILD_VALIDATION_QUEUE_OR_REVIEW_CANONICAL_GATES",
        )

    def test_invalid_focus_limit_fails_closed(self):
        with self.assertRaises(ValueError):
            build_opportunity_funnel(self._ledger(), focus_limit=-1)


if __name__ == "__main__":
    unittest.main()
