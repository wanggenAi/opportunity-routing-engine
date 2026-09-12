import unittest

from src.field_validation_packets import build_field_validation_packets


class FieldValidationPacketTests(unittest.TestCase):
    def _ledger(self):
        return {
            "geography": "Xuzhou",
            "signals": {
                "needs": [{
                    "signal_id": "need-1",
                    "need_actor": "UNRESOLVED_PUBLIC_PROCUREMENT_BUYER",
                }],
                "resources": [{
                    "signal_id": "resource-1",
                    "provider_actor": "徐州测试服务有限公司",
                    "source_ids": ["XZ_GGZY_PROCUREMENT_RESULT", "https://example.invalid/award/1"],
                }],
            },
            "records": [{
                "record_id": "PAIR::need-1::resource-1",
                "capability_key": "TEST_CAPABILITY",
                "geography": "Xuzhou",
                "need_signal_id": "need-1",
                "resource_signal_id": "resource-1",
            }],
        }

    def _queue(self):
        return {
            "tasks": [
                {
                    "task_id": "VALIDATE::PAIR::need-1::resource-1::RESOURCE_UNDERUSE",
                    "record_id": "PAIR::need-1::resource-1",
                    "target_gate": "RESOURCE_UNDERUSE",
                    "instruction": "verify exact provider spare capacity",
                    "pass_condition": "observed capacity",
                    "fail_condition": "claim only",
                    "forbidden_inference": "capability != underuse",
                    "evidence_capture": {
                        "ingestion_flag": "--provider-capacity-json",
                        "promotion_policy": "EXACT_RESOURCE_SIGNAL_AND_IDENTITY_ONLY",
                    },
                },
                {
                    "task_id": "VALIDATE::PAIR::need-1::resource-1::TRANSACTION_BLOCKER",
                    "record_id": "PAIR::need-1::resource-1",
                    "target_gate": "TRANSACTION_BLOCKER",
                    "instruction": "observe exact route blocker",
                    "pass_condition": "observed blocker",
                    "fail_condition": "hypothesis only",
                    "forbidden_inference": "pair != blocker",
                },
                {
                    "task_id": "VALIDATE::PAIR::need-1::resource-1::PAID_NEED",
                    "record_id": "PAIR::need-1::resource-1",
                    "target_gate": "PAID_NEED",
                },
            ]
        }

    def _provider_payload(self):
        return {
            "awards": [{
                "source_id": "XZ_GGZY_PROCUREMENT_RESULT",
                "supplier_name": "徐州测试服务有限公司",
                "supplier_address": "徐州市测试路1号",
                "supplier_credit_code": "91320300TEST000001",
                "project_id": "PROJECT-1",
                "package_name": "采购包1",
                "url": "https://example.invalid/award/1",
                "award_amount_rmb": "900000.00",
            }]
        }

    def test_builds_only_real_world_field_tasks(self):
        result = build_field_validation_packets(
            self._ledger(), self._queue(), provider_payloads=[self._provider_payload()]
        )
        self.assertEqual(result["packet_count"], 2)
        self.assertEqual(
            {packet["target_gate"] for packet in result["packets"]},
            {"RESOURCE_UNDERUSE", "TRANSACTION_BLOCKER"},
        )
        self.assertTrue(all(
            packet["state_effect"] == "NONE_UNTIL_CAPTURED_EVIDENCE_IS_INGESTED_AND_CANONICAL_ENGINE_REBUILDS"
            for packet in result["packets"]
        ))

    def test_provider_metadata_requires_exact_source_backing(self):
        result = build_field_validation_packets(
            self._ledger(), self._queue(), provider_payloads=[self._provider_payload()]
        )
        packet = next(item for item in result["packets"] if item["target_gate"] == "RESOURCE_UNDERUSE")
        self.assertEqual(packet["provider_evidence"]["resolution_state"], "RESOLVED")
        self.assertEqual(packet["provider_evidence"]["supplier_address"], "徐州市测试路1号")
        self.assertIn("does not prove current spare capacity", packet["provider_evidence"]["truth_note"])

    def test_does_not_guess_provider_metadata_when_source_does_not_match(self):
        payload = self._provider_payload()
        payload["awards"][0]["url"] = "https://example.invalid/award/other"
        result = build_field_validation_packets(
            self._ledger(), self._queue(), provider_payloads=[payload]
        )
        packet = next(item for item in result["packets"] if item["target_gate"] == "RESOURCE_UNDERUSE")
        self.assertEqual(packet["provider_evidence"]["resolution_state"], "UNRESOLVED")
        self.assertNotIn("supplier_address", packet["provider_evidence"])

    def test_underuse_packet_preserves_canonical_ingestion_contract(self):
        result = build_field_validation_packets(
            self._ledger(), self._queue(), provider_payloads=[self._provider_payload()]
        )
        packet = next(item for item in result["packets"] if item["target_gate"] == "RESOURCE_UNDERUSE")
        self.assertEqual(packet["capture_contract"]["ingestion_flag"], "--provider-capacity-json")
        self.assertEqual(
            packet["capture_contract"]["promotion_policy"],
            "EXACT_RESOURCE_SIGNAL_AND_IDENTITY_ONLY",
        )
        self.assertIn("不要只回答", packet["questions"][0])


if __name__ == "__main__":
    unittest.main()
