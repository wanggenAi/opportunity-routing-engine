import unittest

from src.money_flow_snapshot import (
    SnapshotFeed,
    TRUTH_BOUNDARIES,
    collect_money_flow_snapshot,
)


def _available(payload):
    return lambda: payload


class MoneyFlowSnapshotTests(unittest.TestCase):
    def test_available_and_error_are_kept_distinct(self):
        feeds = [
            SnapshotFeed(
                key="china_pbc_financial_statistics",
                geography="China",
                evidence_role="national_money_credit_liquidity",
                collect=_available(
                    {
                        "data_available": True,
                        "latest_release": {
                            "title": "2026年7月金融统计数据报告",
                            "release_date": "2026-08-14",
                            "metrics": {"m2_balance": {"value": 355.51, "unit": "trillion_cny"}},
                        },
                        "freshness": {"status": "FRESH"},
                    }
                ),
            ),
            SnapshotFeed(
                key="jiangsu_pbc_regional_social_financing",
                geography="Jiangsu",
                evidence_role="provincial_social_financing_flow",
                collect=lambda: (_ for _ in ()).throw(RuntimeError("source drift")),
            ),
        ]
        snapshot = collect_money_flow_snapshot(feeds=feeds)
        self.assertEqual(
            snapshot["feeds"]["china_pbc_financial_statistics"]["status"],
            "AVAILABLE",
        )
        failed = snapshot["feeds"]["jiangsu_pbc_regional_social_financing"]
        self.assertEqual(failed["status"], "ERROR")
        self.assertFalse(failed["data_available"])
        self.assertEqual(failed["error_type"], "RuntimeError")
        self.assertEqual(snapshot["answerability"]["jiangsu_money_flow"]["status"], "UNKNOWN")
        self.assertEqual(snapshot["answerability"]["xuzhou_financial_balance"]["status"], "UNKNOWN")

    def test_explicit_unavailable_never_becomes_available(self):
        snapshot = collect_money_flow_snapshot(
            feeds=[
                SnapshotFeed(
                    key="china_pbc_financial_statistics",
                    geography="China",
                    evidence_role="national_money_credit_liquidity",
                    collect=_available({"data_available": False, "reason": "empty payload"}),
                )
            ]
        )
        feed = snapshot["feeds"]["china_pbc_financial_statistics"]
        self.assertEqual(feed["status"], "UNAVAILABLE")
        self.assertEqual(snapshot["answerability"]["china_money_flow"]["status"], "UNKNOWN")

    def test_jiangsu_answerability_requires_all_three_live_dimensions(self):
        feeds = [
            SnapshotFeed(
                key="jiangsu_pbc_regional_social_financing",
                geography="Jiangsu",
                evidence_role="provincial_social_financing_flow",
                collect=_available({"data_available": True, "region_observation": {}}),
            ),
            SnapshotFeed(
                key="jiangsu_pbc_credit_deposit",
                geography="Jiangsu",
                evidence_role="provincial_deposit_loan_levels",
                collect=_available({"data_available": True, "observation": {"metrics": {}}}),
            ),
        ]
        snapshot = collect_money_flow_snapshot(feeds=feeds)
        self.assertEqual(snapshot["answerability"]["jiangsu_money_flow"]["status"], "PARTIAL")
        self.assertEqual(
            snapshot["answerability"]["jiangsu_money_flow"]["feeds"]["jiangsu_stats_economic_operation"],
            "NOT_RUN",
        )

    def test_xuzhou_headline_preserves_events_without_unsafe_sum(self):
        construction_payload = {
            "source_id": "XZ_GGZY",
            "discovery": {"item_count": 2},
            "event_count": 2,
            "error_count": 0,
            "amount_evidence_count": 2,
            "funding_evidence_count": 2,
            "reissue_count": 1,
            "events": [
                {"title": "A", "contract_estimate_rmb": "1000000.00", "is_reissue": False},
                {"title": "A重发", "contract_estimate_rmb": "1000000.00", "is_reissue": True},
            ],
            "aggregation_policy": "NO_SUM_WITHOUT_PROJECT_DEDUP",
        }
        procurement_payload = {
            "source_id": "XZ_GGZY",
            "discovery": {"item_count": 1},
            "event_count": 1,
            "error_count": 0,
            "events": [{"title": "purchase", "budget_rmb": "500000.00"}],
        }
        feeds = [
            SnapshotFeed(
                key="xuzhou_government_procurement",
                geography="Xuzhou",
                evidence_role="institutional_purchase_demand",
                collect=_available(procurement_payload),
            ),
            SnapshotFeed(
                key="xuzhou_construction_tenders",
                geography="Xuzhou",
                evidence_role="local_construction_capex_solicitation",
                collect=_available(construction_payload),
            ),
        ]
        snapshot = collect_money_flow_snapshot(feeds=feeds)
        xz = snapshot["headline_evidence"]["Xuzhou"]
        self.assertEqual(snapshot["answerability"]["xuzhou_institutional_spend"]["status"], "AVAILABLE")
        self.assertEqual(xz["construction_tenders"]["amount_evidence_count"], 2)
        self.assertEqual(xz["construction_tenders"]["reissue_count"], 1)
        self.assertNotIn("total_contract_estimate_rmb", xz["construction_tenders"])
        self.assertNotIn("total_budget_rmb", xz["government_procurement"])
        self.assertIn("NO_CROSS_SOURCE_SUM", snapshot["truth_boundaries"])
        self.assertIn("NO_TENDER_SUM_WITHOUT_PROJECT_DEDUP", snapshot["truth_boundaries"])

    def test_no_opportunity_promotion_exists_in_snapshot_contract(self):
        snapshot = collect_money_flow_snapshot(
            feeds=[
                SnapshotFeed(
                    key="china_pbc_financial_statistics",
                    geography="China",
                    evidence_role="national_money_credit_liquidity",
                    collect=_available({"data_available": True, "latest_release": {}, "freshness": {}}),
                )
            ]
        )
        self.assertEqual(snapshot["schema_version"], "money-flow-snapshot-v1")
        self.assertIn("NO_OPPORTUNITY_INFERENCE", TRUTH_BOUNDARIES)
        self.assertIn("NEED + SURPLUS RESOURCE + TRANSACTION BLOCKER", snapshot["interpretation_boundary"])
        self.assertNotIn("opportunities", snapshot)
        self.assertNotIn("score", snapshot)

    def test_duplicate_feed_keys_fail_closed(self):
        feed = SnapshotFeed(
            key="china_pbc_financial_statistics",
            geography="China",
            evidence_role="national_money_credit_liquidity",
            collect=_available({"data_available": True}),
        )
        with self.assertRaisesRegex(ValueError, "keys must be unique"):
            collect_money_flow_snapshot(feeds=[feed, feed])


if __name__ == "__main__":
    unittest.main()
