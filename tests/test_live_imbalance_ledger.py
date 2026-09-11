import unittest

from src.live_imbalance_ledger import (
    build_live_imbalance_ledger,
    classify_procurement_event,
    classify_resource_listing,
)
from src.resource_imbalance import BlockerSignal


class LiveImbalanceLedgerTests(unittest.TestCase):
    def _factory_need(self):
        return {
            "source_id": "XZ_GGZY",
            "title": "某产业园厂房租赁服务采购公告",
            "project_id": "P-001",
            "project_name": "产业园厂房租赁服务",
            "url": "https://ggzy.example.test/need-1",
            "publication_date": "2026-09-11",
            "budget_rmb": "1000000.00",
        }

    def _factory_resource(self):
        return {
            "source_id": "XZ_GGZY",
            "title": "某产业园5号厂房招租",
            "project_id": "R-001",
            "url": "https://ggzy.example.test/resource-1",
            "publication_date": "2026-09-11",
            "listing_mode": "LEASE",
            "listing_round": 2,
            "relisting_observed": True,
            "resource_state": "DISCOVERED",
            "underuse_evidence_state": "OBSERVED",
            "underuse_excerpt": "房屋现状：空置",
            "asking_price_rmb": "500000.00",
            "owner_actor": "徐州某产业发展有限公司",
            "location": "徐州市某产业园",
        }

    def test_exact_factory_pair_stays_hypothesis_without_paid_payer_or_blocker(self):
        ledger = build_live_imbalance_ledger(
            {"events": [self._factory_need()]},
            [{"listings": [self._factory_resource()]}],
        )
        self.assertEqual(ledger["status_counts"], {"PAIR_HYPOTHESIS": 1})
        self.assertEqual(ledger["route_testable_count"], 0)
        self.assertEqual(ledger["signal_counts"]["unbound_evidence"], 0)
        record = ledger["records"][0]
        self.assertEqual(record["capability_key"], "INDUSTRIAL_SPACE_LEASE")
        self.assertEqual(record["need_evidence_state"], "OBSERVED")
        self.assertEqual(record["underuse_evidence_state"], "OBSERVED")
        self.assertIn("need side lacks direct paid evidence", record["reasons"])
        self.assertIn("payer is not identified", record["reasons"])
        self.assertIn("transaction blocker is not identified", record["reasons"])

    def test_observed_blocker_does_not_override_unpaid_unresolved_need(self):
        blocker = BlockerSignal(
            signal_id="blocker-1",
            capability_key="INDUSTRIAL_SPACE_LEASE",
            geography="Xuzhou",
            blocker_type="INFORMATION_GAP",
            evidence_state="OBSERVED",
            description="verified counterparties report incompatible availability information",
            source_ids=("field-evidence-1",),
        )
        ledger = build_live_imbalance_ledger(
            {"events": [self._factory_need()]},
            [{"listings": [self._factory_resource()]}],
            [blocker],
        )
        self.assertEqual(ledger["status_counts"], {"PAIR_HYPOTHESIS": 1})
        record = ledger["records"][0]
        self.assertEqual(record["blocker_signal_id"], "blocker-1")
        self.assertEqual(record["blocker_evidence_state"], "OBSERVED")
        self.assertIn("need side lacks direct paid evidence", record["reasons"])
        self.assertIn("payer is not identified", record["reasons"])
        self.assertNotIn("transaction blocker is not observed", record["reasons"])

    def test_unclassified_evidence_is_retained_not_guessed(self):
        need = {
            "source_id": "XZ_GGZY",
            "title": "综合服务采购公告",
            "project_id": "P-unknown",
            "url": "https://ggzy.example.test/unknown-need",
            "publication_date": "2026-09-11",
            "budget_rmb": "500000.00",
        }
        resource = self._factory_resource() | {
            "title": "一批资产公开招租",
            "location": "徐州市",
        }
        ledger = build_live_imbalance_ledger(
            {"events": [need]},
            [{"listings": [resource]}],
        )
        self.assertEqual(ledger["records"], [])
        self.assertEqual(ledger["signal_counts"]["unbound_evidence"], 2)
        reasons = {item["reason"] for item in ledger["unbound_evidence"]}
        self.assertEqual(reasons, {"NO_EXACT_CAPABILITY_RULE"})

    def test_ambiguous_capability_text_is_not_silently_bound(self):
        event = self._factory_need() | {
            "title": "厂房租赁及办公用房租赁服务采购公告",
            "project_name": "厂房租赁及办公用房租赁服务",
        }
        result = classify_procurement_event(event)
        self.assertIsNone(result.capability_key)
        self.assertEqual(result.reason, "AMBIGUOUS_EXACT_CAPABILITY_RULE")

    def test_resource_mode_is_part_of_classification_contract(self):
        listing = self._factory_resource() | {"listing_mode": "TRANSFER"}
        result = classify_resource_listing(listing)
        self.assertIsNone(result.capability_key)
        self.assertEqual(result.reason, "NO_EXACT_CAPABILITY_RULE")

    def test_resource_owner_is_required_before_resource_signal_promotion(self):
        listing = self._factory_resource() | {"owner_actor": None}
        ledger = build_live_imbalance_ledger({}, [{"listings": [listing]}])
        self.assertEqual(ledger["records"], [])
        self.assertEqual(
            ledger["unbound_evidence"][0]["reason"],
            "RESOURCE_OWNER_UNRESOLVED_OR_INVALID",
        )

    def test_platform_disclaimer_is_not_accepted_as_resource_owner(self):
        listing = self._factory_resource() | {
            "owner_actor": "和/或招标方的相关资质进行审核。本平台不承担审核义务与法律责任。"
        }
        ledger = build_live_imbalance_ledger({}, [{"listings": [listing]}])
        self.assertEqual(ledger["signal_counts"]["resources"], 0)
        self.assertEqual(
            ledger["unbound_evidence"][0]["reason"],
            "RESOURCE_OWNER_UNRESOLVED_OR_INVALID",
        )

    def test_current_xuzhou_procurement_titles_create_auditable_need_only_signals(self):
        titles = {
            "徐州市水务局2026年度市管雨污水泵站设施维修养护市场化项目公开招标公告": "WATER_PUMP_STATION_MAINTENANCE",
            "徐州市财政效能中心徐州市数智化财政业务平台-财政信息化服务公开招标公告": "FINANCE_DIGITAL_IT_SERVICE",
            "沛县自然资源和规划局2026年度一体化调查监测项目竞争性磋商公告": "SURVEY_MONITORING_SERVICE",
            "徐州市南水北调工程管理中心2026年市级水利工程养护竞争性磋商采购公告": "WATER_ENGINEERING_MAINTENANCE",
            "江苏徐淮地区徐州农业科学研究所三地日光温室建设项目采购公告": "AGRICULTURAL_FACILITY_CONSTRUCTION",
            "徐州市中心医院全自动内窥镜清洗消毒机采购公开招标公告": "MEDICAL_CLEANING_EQUIPMENT_SUPPLY",
        }
        events = []
        for i, title in enumerate(titles, start=1):
            result = classify_procurement_event({"title": title})
            self.assertEqual(result.capability_key, titles[title])
            events.append(
                {
                    "source_id": "XZ_GGZY",
                    "title": title,
                    "url": f"https://ggzy.example.test/{i}",
                    "publication_date": "2026-09-11",
                }
            )
        ledger = build_live_imbalance_ledger({"events": events})
        self.assertEqual(ledger["signal_counts"]["needs"], len(events))
        self.assertEqual(ledger["status_counts"], {"NEED_ONLY": len(events)})
        self.assertEqual(ledger["route_testable_count"], 0)

    def test_commercial_space_classification_remains_mode_gated(self):
        listing = self._factory_resource() | {
            "title": "江苏徐州睢宁县八里商业城A7-10招租项目公告",
            "listing_mode": "LEASE",
        }
        result = classify_resource_listing(listing)
        self.assertEqual(result.capability_key, "COMMERCIAL_SPACE_LEASE")
        transfer = classify_resource_listing(listing | {"listing_mode": "TRANSFER"})
        self.assertIsNone(transfer.capability_key)

    def test_historical_procurement_award_creates_pair_but_not_route_testable(self):
        live_need = {
            "source_id": "XZ_GGZY",
            "title": "徐州市水务局2026年度市管雨污水泵站设施维修养护市场化项目公开招标公告",
            "project_id": "OPEN-2026-01",
            "project_name": "2026年度市管雨污水泵站设施维修养护市场化",
            "url": "https://ggzy.example.test/open-pump",
            "publication_date": "2026-09-10",
            "budget_rmb": "1883300.00",
        }
        historical_award = {
            "source_id": "XZ_GGZY_PROCUREMENT_RESULT",
            "title": "徐州市水务局2026年度市管雨污水泵站设施维修养护市场化中标结果公告采购包2",
            "project_id": "OLD-2026-01",
            "project_name": "2026年度市管雨污水泵站设施维修养护市场化、市直管截污闸门维修养护",
            "url": "https://ggzy.example.test/result-pump",
            "publication_date": "2026-09-09",
            "buyer_actor": "徐州市水务局",
            "supplier_name": "江苏山祥建设工程有限公司",
            "supplier_credit_code": "91320312302101990G",
            "award_amount_rmb": "1186000.00",
        }
        ledger = build_live_imbalance_ledger(
            {"events": [live_need]},
            provider_payloads=[{"awards": [historical_award]}],
        )
        self.assertEqual(ledger["source_input_counts"]["provider_awards"], 1)
        self.assertEqual(ledger["status_counts"], {"PAIR_HYPOTHESIS": 1})
        self.assertEqual(ledger["route_testable_count"], 0)
        record = ledger["records"][0]
        self.assertEqual(record["capability_key"], "WATER_PUMP_STATION_MAINTENANCE")
        self.assertEqual(record["resource_state"], "DISCOVERED")
        self.assertEqual(record["underuse_evidence_state"], "UNKNOWN")
        self.assertIn("need side lacks direct paid evidence", record["reasons"])
        self.assertIn("payer is not identified", record["reasons"])
        self.assertIn("resource underuse is not observed", record["reasons"])
        self.assertIn("transaction blocker is not identified", record["reasons"])
        resource = ledger["signals"]["resources"][0]
        self.assertEqual(resource["provider_actor"], "江苏山祥建设工程有限公司")
        self.assertIn("historical public procurement award", resource["notes"])


if __name__ == "__main__":
    unittest.main()
