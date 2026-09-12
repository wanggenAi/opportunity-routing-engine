import unittest

from src.procurement_lifecycle import (
    build_procurement_lifecycle,
    integrate_procurement_lifecycle,
)


class ProcurementLifecycleTests(unittest.TestCase):
    def _tender(self, project_id="JSZC-320300-TEST-G2026-0001"):
        return {
            "source_id": "XZ_GGZY",
            "project_id": project_id,
            "project_name": "测试维修养护项目",
            "title": "测试维修养护项目公开招标公告",
            "url": f"https://example.invalid/tender/{project_id}",
            "publication_date": "2026-09-01",
            "budget_rmb": "1000000.00",
            "provenance": {"payload_sha256": "tender-sha"},
        }

    def _result(self, project_id="JSZC-320300-TEST-G2026-0001"):
        return {
            "source_id": "XZ_GGZY_PROCUREMENT_RESULT",
            "project_id": project_id,
            "project_name": "测试维修养护项目",
            "title": "测试维修养护项目中标结果公告",
            "url": f"https://example.invalid/result/{project_id}",
            "publication_date": "2026-09-20",
            "buyer_actor": "徐州市测试采购单位",
            "supplier_name": "徐州测试服务有限公司",
            "supplier_credit_code": "91320300TEST000001",
            "award_amount_rmb": "900000.00",
            "package_name": "采购包1",
            "provenance": {"payload_sha256": "result-sha"},
        }

    def _contract(
        self,
        project_id="JSZC-320300-TEST-G2026-0001",
        *,
        settlement=False,
        payer="徐州市测试付款单位",
    ):
        return {
            "source_id": "JS_GOV_PROCUREMENT_CONTRACT",
            "project_id": project_id,
            "project_name": "测试维修养护项目",
            "url": f"https://example.invalid/contract/{project_id}",
            "buyer_actor": "徐州市测试采购单位",
            "payer_actor": payer,
            "supplier_actor": "徐州测试服务有限公司",
            "contract_amount_rmb": "900000.00",
            "settled_amount_rmb": "900000.00" if settlement else None,
            "contract_signed": True,
            "settlement_proven": settlement,
            "provenance": {"payload_sha256": "contract-sha"},
        }

    def test_tender_only_is_observed_not_paid(self):
        lifecycle = build_procurement_lifecycle({"events": [self._tender()]})
        record = lifecycle["records"][0]
        self.assertEqual(record["lifecycle_stage"], "TENDER_ONLY")
        self.assertFalse(record["promotion_allowed"])
        self.assertEqual(record["promotion_reason"], "TENDER_ONLY_BUDGET_IS_NOT_PAYMENT")

    def test_exact_result_is_result_found_but_not_paid(self):
        lifecycle = build_procurement_lifecycle(
            {"events": [self._tender()]},
            [{"awards": [self._result()]}],
        )
        record = lifecycle["records"][0]
        self.assertEqual(record["lifecycle_stage"], "RESULT_FOUND")
        self.assertEqual(record["buyer_actor"], "徐州市测试采购单位")
        self.assertIsNone(record["payer_actor"])
        self.assertFalse(record["promotion_allowed"])
        self.assertEqual(record["promotion_reason"], "AWARD_RESULT_IS_NOT_SETTLEMENT")

    def test_same_title_different_project_id_never_links(self):
        other = self._result("JSZC-320300-TEST-G2026-9999")
        lifecycle = build_procurement_lifecycle(
            {"events": [self._tender()]},
            [{"awards": [other]}],
        )
        record = lifecycle["records"][0]
        self.assertEqual(record["lifecycle_stage"], "TENDER_ONLY")
        self.assertEqual(record["result_evidence"], [])
        self.assertTrue(
            any(
                item.get("reason") == "NO_EXACT_TENDER_PROJECT_ID_MATCH"
                for item in lifecycle["unlinked_evidence"]
            )
        )

    def test_signed_contract_without_settlement_is_not_paid(self):
        lifecycle = build_procurement_lifecycle(
            {"events": [self._tender()]},
            [{"awards": [self._result()]}],
            [{"contracts": [self._contract(settlement=False)]}],
        )
        record = lifecycle["records"][0]
        self.assertEqual(record["lifecycle_stage"], "CONTRACT_FOUND")
        self.assertFalse(record["promotion_allowed"])
        self.assertEqual(record["promotion_reason"], "SIGNED_CONTRACT_IS_NOT_SETTLEMENT")

    def test_settlement_requires_explicit_payer(self):
        lifecycle = build_procurement_lifecycle(
            {"events": [self._tender()]},
            [{"awards": [self._result()]}],
            [{"contracts": [self._contract(settlement=True, payer=None)]}],
        )
        record = lifecycle["records"][0]
        self.assertEqual(record["lifecycle_stage"], "SETTLEMENT_PROVEN")
        self.assertFalse(record["promotion_allowed"])
        self.assertEqual(record["promotion_reason"], "SETTLEMENT_PAYER_UNRESOLVED")

    def test_exact_settlement_can_promote_matching_need_only(self):
        lifecycle = build_procurement_lifecycle(
            {"events": [self._tender()]},
            [{"awards": [self._result()]}],
            [{"contracts": [self._contract(settlement=True)]}],
        )
        record = lifecycle["records"][0]
        self.assertTrue(record["promotion_allowed"])
        self.assertEqual(
            record["promotion_reason"],
            "EXACT_PROJECT_FIRST_PARTY_SETTLEMENT_WITH_EXPLICIT_PAYER",
        )

        ledger = {
            "geography": "Xuzhou",
            "source_input_counts": {},
            "signal_counts": {
                "needs": 1,
                "resources": 1,
                "blockers": 1,
                "unbound_evidence": 0,
            },
            "status_counts": {"PAIR_HYPOTHESIS": 1},
            "blocking_reason_counts": {},
            "route_testable_count": 0,
            "signals": {
                "needs": [
                    {
                        "signal_id": "LIVE_NEED::XZ_GGZY::JSZC-320300-TEST-G2026-0001",
                        "capability_key": "TEST_MAINTENANCE",
                        "geography": "Xuzhou",
                        "need_actor": "UNRESOLVED_PUBLIC_PROCUREMENT_BUYER",
                        "payer": None,
                        "evidence_state": "OBSERVED",
                        "paid_event_count": 0,
                        "total_observed_spend_rmb": None,
                        "observation_period": "2026-09-01",
                        "source_ids": ["XZ_GGZY", self._tender()["url"]],
                        "notes": "budget is not payment",
                    }
                ],
                "resources": [
                    {
                        "signal_id": "resource-1",
                        "capability_key": "TEST_MAINTENANCE",
                        "geography": "Xuzhou",
                        "provider_actor": "徐州测试服务有限公司",
                        "resource_state": "DISCOVERED",
                        "underuse_evidence_state": "OBSERVED",
                        "available_units": "1",
                        "observation_period": "2026-09",
                        "source_ids": ["provider-source"],
                        "notes": "",
                    }
                ],
                "blockers": [
                    {
                        "signal_id": "blocker-1",
                        "capability_key": "TEST_MAINTENANCE",
                        "geography": "Xuzhou",
                        "blocker_type": "COORDINATION_GAP",
                        "evidence_state": "OBSERVED",
                        "description": "observed coordination failure",
                        "source_ids": ["blocker-source"],
                    }
                ],
            },
            "records": [],
            "route_testable_records": [],
            "unbound_evidence": [],
            "truth_notes": [],
        }
        updated = integrate_procurement_lifecycle(ledger, lifecycle)
        need = updated["signals"]["needs"][0]
        self.assertEqual(need["evidence_state"], "PAID")
        self.assertEqual(need["payer"], "徐州市测试付款单位")
        self.assertEqual(need["total_observed_spend_rmb"], "900000.00")
        self.assertEqual(updated["route_testable_count"], 1)
        self.assertEqual(updated["records"][0]["status"], "ROUTE_TESTABLE")

    def test_result_buyer_is_not_copied_into_payer_during_integration(self):
        lifecycle = build_procurement_lifecycle(
            {"events": [self._tender()]},
            [{"awards": [self._result()]}],
        )
        ledger = {
            "geography": "Xuzhou",
            "signals": {
                "needs": [
                    {
                        "signal_id": "LIVE_NEED::XZ_GGZY::JSZC-320300-TEST-G2026-0001",
                        "capability_key": "TEST_MAINTENANCE",
                        "geography": "Xuzhou",
                        "need_actor": "UNRESOLVED_PUBLIC_PROCUREMENT_BUYER",
                        "payer": None,
                        "evidence_state": "OBSERVED",
                        "paid_event_count": 0,
                        "source_ids": ["source"],
                        "notes": "",
                    }
                ],
                "resources": [],
                "blockers": [],
            },
            "truth_notes": [],
        }
        updated = integrate_procurement_lifecycle(ledger, lifecycle)
        need = updated["signals"]["needs"][0]
        self.assertEqual(need["evidence_state"], "OBSERVED")
        self.assertIsNone(need["payer"])


if __name__ == "__main__":
    unittest.main()
