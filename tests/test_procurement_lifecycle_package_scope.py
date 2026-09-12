import unittest

from src.procurement_lifecycle import build_procurement_lifecycle


class ProcurementLifecyclePackageScopeTests(unittest.TestCase):
    PROJECT_ID = "JSZC-320300-WYKJ-G2026-0034"

    def _tender(self, *, budget_raw=None):
        return {
            "source_id": "XZ_GGZY",
            "project_id": self.PROJECT_ID,
            "project_name": "徐州市数智化财政业务平台-财政信息化服务",
            "title": "财政信息化服务公开招标公告",
            "url": "https://example.invalid/tender/0034",
            "publication_date": "2026-09-10",
            "budget_rmb": "1259500.00",
            "budget_raw": budget_raw,
            "provenance": {"payload_sha256": "tender-sha"},
        }

    def _settlement(self, *, package_name=None, amount="389500.00"):
        return {
            "source_id": "FIRST_PARTY_SETTLEMENT",
            "project_id": self.PROJECT_ID,
            "project_name": "徐州市数智化财政业务平台-财政信息化服务",
            "url": "https://example.invalid/settlement/0034",
            "publication_date": "2026-11-20",
            "buyer_actor": "徐州市财政效能中心",
            "payer_actor": "徐州市财政效能中心",
            "supplier_actor": "南京测试信息工程有限公司",
            "package_name": package_name,
            "contract_amount_rmb": amount,
            "settled_amount_rmb": amount,
            "contract_signed": True,
            "settlement_proven": True,
            "provenance": {"payload_sha256": "settlement-sha"},
        }

    def _multi_package_tender(self):
        return self._tender(
            budget_raw=(
                "预算金额：125.950000万元（采购包1：87.000000万元；"
                "采购包2：38.950000万元）"
            )
        )

    def test_package_specific_settlement_cannot_promote_multi_package_project_need(self):
        lifecycle = build_procurement_lifecycle(
            {"events": [self._multi_package_tender()]},
            contract_payloads=[{"contracts": [self._settlement(package_name="采购包2")]}],
        )
        record = lifecycle["records"][0]
        self.assertEqual(record["lifecycle_stage"], "SETTLEMENT_PROVEN")
        self.assertEqual(record["tender_package_names"], ["采购包1", "采购包2"])
        self.assertEqual(record["settlement_package_names"], ["采购包2"])
        self.assertEqual(record["package_scope"], "MULTI_PACKAGE_PROJECT")
        self.assertFalse(record["promotion_allowed"])
        self.assertEqual(
            record["promotion_reason"],
            "PACKAGE_SCOPED_SETTLEMENT_CANNOT_PROMOTE_PROJECT_LEVEL_NEED",
        )
        self.assertIn("PACKAGE_SCOPE", record["unresolved_fields"])

    def test_missing_settlement_package_scope_cannot_promote_multi_package_project_need(self):
        lifecycle = build_procurement_lifecycle(
            {"events": [self._multi_package_tender()]},
            contract_payloads=[{"contracts": [self._settlement(package_name=None, amount="1259500.00")]}],
        )
        record = lifecycle["records"][0]
        self.assertEqual(record["package_scope"], "MULTI_PACKAGE_PROJECT")
        self.assertEqual(record["settlement_package_names"], [])
        self.assertFalse(record["promotion_allowed"])
        self.assertEqual(
            record["promotion_reason"],
            "PACKAGE_SCOPED_SETTLEMENT_CANNOT_PROMOTE_PROJECT_LEVEL_NEED",
        )
        self.assertIn("PACKAGE_SCOPE", record["unresolved_fields"])

    def test_explicit_whole_project_settlement_can_promote_multi_package_project_need(self):
        lifecycle = build_procurement_lifecycle(
            {"events": [self._multi_package_tender()]},
            contract_payloads=[
                {"contracts": [self._settlement(package_name="项目整体", amount="1259500.00")]}
            ],
        )
        record = lifecycle["records"][0]
        self.assertEqual(record["package_scope"], "MULTI_PACKAGE_PROJECT")
        self.assertEqual(record["settlement_package_names"], ["项目整体"])
        self.assertTrue(record["promotion_allowed"])
        self.assertEqual(
            record["promotion_reason"],
            "EXACT_PROJECT_FIRST_PARTY_SETTLEMENT_WITH_EXPLICIT_PAYER",
        )

    def test_unique_single_package_settlement_can_promote_project_need(self):
        tender = self._tender(
            budget_raw="预算金额：38.950000万元（采购包1：38.950000万元）"
        )
        lifecycle = build_procurement_lifecycle(
            {"events": [tender]},
            contract_payloads=[{"contracts": [self._settlement(package_name="采购包1")]}],
        )
        record = lifecycle["records"][0]
        self.assertEqual(record["tender_package_names"], ["采购包1"])
        self.assertEqual(record["package_scope"], "SINGLE_PACKAGE_OR_UNSPECIFIED")
        self.assertTrue(record["promotion_allowed"])

    def test_explicit_package_names_field_is_preferred_for_scope_detection(self):
        tender = self._tender(budget_raw="预算金额：125.95万元")
        tender["package_names"] = ["采购包1", "采购包2"]
        lifecycle = build_procurement_lifecycle(
            {"events": [tender]},
            contract_payloads=[{"contracts": [self._settlement(package_name="采购包1")]}],
        )
        record = lifecycle["records"][0]
        self.assertEqual(record["tender_package_names"], ["采购包1", "采购包2"])
        self.assertFalse(record["promotion_allowed"])


if __name__ == "__main__":
    unittest.main()
