import unittest

from src.validation_queue import build_pair_validation_queue


class ValidationQueueTests(unittest.TestCase):
    def _ledger(self):
        return {
            "geography": "Xuzhou",
            "signals": {
                "needs": [
                    {
                        "signal_id": "need-1",
                        "need_actor": "UNRESOLVED_PUBLIC_PROCUREMENT_BUYER",
                    }
                ],
                "resources": [
                    {
                        "signal_id": "resource-1",
                        "provider_actor": "江苏某建设有限公司",
                    }
                ],
            },
            "records": [
                {
                    "record_id": "PAIR::need-1::resource-1",
                    "capability_key": "WATER_PUMP_STATION_MAINTENANCE",
                    "geography": "Xuzhou",
                    "status": "PAIR_HYPOTHESIS",
                    "need_signal_id": "need-1",
                    "resource_signal_id": "resource-1",
                    "payer": None,
                    "need_evidence_state": "OBSERVED",
                    "resource_state": "DISCOVERED",
                    "underuse_evidence_state": "UNKNOWN",
                    "blocker_evidence_state": None,
                },
                {
                    "record_id": "NEED::need-2",
                    "capability_key": "OTHER",
                    "geography": "Xuzhou",
                    "status": "NEED_ONLY",
                    "need_signal_id": "need-2",
                    "resource_signal_id": None,
                    "payer": None,
                    "need_evidence_state": "OBSERVED",
                    "resource_state": None,
                    "underuse_evidence_state": None,
                    "blocker_evidence_state": None,
                },
            ],
        }

    def test_pair_hypothesis_yields_four_missing_gate_tasks(self):
        queue = build_pair_validation_queue(self._ledger())
        self.assertEqual(queue["pair_hypothesis_count"], 1)
        self.assertEqual(queue["queued_pair_count"], 1)
        self.assertEqual(queue["task_count"], 4)
        self.assertEqual(
            queue["target_counts"],
            {
                "PAID_NEED": 1,
                "PAYER_IDENTITY": 1,
                "RESOURCE_UNDERUSE": 1,
                "TRANSACTION_BLOCKER": 1,
            },
        )
        self.assertEqual(
            [task["target_gate"] for task in queue["tasks"]],
            [
                "PAYER_IDENTITY",
                "PAID_NEED",
                "RESOURCE_UNDERUSE",
                "TRANSACTION_BLOCKER",
            ],
        )
        pair = queue["pairs"][0]
        self.assertEqual(pair["provider_actor"], "江苏某建设有限公司")
        self.assertEqual(pair["missing_gate_count"], 4)
        self.assertTrue(
            all(task["state_effect"] == "NONE_UNTIL_NEW_EVIDENCE_IS_INGESTED" for task in queue["tasks"])
        )

    def test_satisfied_gates_do_not_generate_tasks(self):
        ledger = self._ledger()
        record = ledger["records"][0]
        record.update(
            {
                "payer": "徐州市某采购单位",
                "need_evidence_state": "PAID",
                "underuse_evidence_state": "OBSERVED",
                "blocker_evidence_state": "OBSERVED",
            }
        )
        queue = build_pair_validation_queue(ledger)
        self.assertEqual(queue["task_count"], 0)
        self.assertEqual(queue["pairs"][0]["missing_gate_count"], 0)

    def test_route_testable_and_one_sided_records_are_not_queued(self):
        ledger = self._ledger()
        ledger["records"][0]["status"] = "ROUTE_TESTABLE"
        queue = build_pair_validation_queue(ledger)
        self.assertEqual(queue["pair_hypothesis_count"], 0)
        self.assertEqual(queue["pairs"], [])
        self.assertEqual(queue["tasks"], [])

    def test_claimed_underuse_and_blocker_still_require_observed_evidence(self):
        ledger = self._ledger()
        record = ledger["records"][0]
        record["payer"] = "某付款方"
        record["need_evidence_state"] = "PAID"
        record["underuse_evidence_state"] = "CLAIMED"
        record["blocker_evidence_state"] = "CLAIMED"
        queue = build_pair_validation_queue(ledger)
        self.assertEqual(
            [task["target_gate"] for task in queue["tasks"]],
            ["RESOURCE_UNDERUSE", "TRANSACTION_BLOCKER"],
        )
        for task in queue["tasks"]:
            self.assertIn("!=", task["forbidden_inference"])


if __name__ == "__main__":
    unittest.main()
