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
            "RESOURCE_OWNER_UNRESOLVED",
        )


if __name__ == "__main__":
    unittest.main()
