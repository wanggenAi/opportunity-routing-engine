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
        self.assertEqual(snapshot["answerability"]["xuzhou_enterprise_funding_demand"]["status"], "UNKNOWN")

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

    def test_customs_scope_keeps_jiangsu_xuzhou_area_and_city_distinct(self):
        customs_payload = {
            "source_id": "CN_CUSTOMS",
            "period": "2026-07",
            "unit": "USD_THOUSAND",
            "transport_security": "PLAINTEXT_HTTP",
            "corroboration_status": "PERIOD_IDENTITY_DIRECTION_CORROBORATED",
            "corroboration": {
                "source_id": "JS_GOV",
                "period": "2026-07",
                "basis": "PERIOD_IDENTITY_DIRECTION_ONLY",
                "monetary_value_comparison": "UNAVAILABLE_CROSS_CURRENCY",
            },
            "jiangsu_importer_exporter_location": {
                "name": "Jiangsu Province",
                "total_ytd_usd_thousand": 604348420.0,
                "total_basis": "DERIVED_EXPORT_PLUS_IMPORT",
            },
            "xuzhou_importer_exporter_location": None,
            "xuzhou_specific_areas": [
                {"name": "Xuzhou CBZ", "total_ytd_usd_thousand": 497299.0},
                {"name": "Xuzhou BLC", "total_ytd_usd_thousand": 37848.0},
            ],
        }
        snapshot = collect_money_flow_snapshot(
            feeds=[
                SnapshotFeed(
                    key="jiangsu_customs_trade_flow",
                    geography="Jiangsu/XuzhouSpecificAreas",
                    evidence_role="provincial_trade_flow_and_specific_area_customs_activity",
                    collect=_available(customs_payload),
                )
            ]
        )
        answerability = snapshot["answerability"]
        self.assertEqual(answerability["jiangsu_trade_flow"]["status"], "AVAILABLE")
        self.assertEqual(answerability["xuzhou_specific_area_trade"]["status"], "PARTIAL")
        self.assertEqual(answerability["xuzhou_city_trade_flow"]["status"], "UNKNOWN")

        js = snapshot["headline_evidence"]["Jiangsu"]["customs_trade_flow"]
        self.assertEqual(js["corroboration_status"], "PERIOD_IDENTITY_DIRECTION_CORROBORATED")
        self.assertEqual(
            js["corroboration"]["monetary_value_comparison"],
            "UNAVAILABLE_CROSS_CURRENCY",
        )
        xz = snapshot["headline_evidence"]["Xuzhou"]["customs_specific_areas"]
        self.assertEqual(xz["scope"], "SPECIFIC_AREAS_ONLY")
        self.assertEqual(xz["specific_area_value_corroboration"], "NOT_ESTABLISHED")
        self.assertIsNone(xz["city_location_row"])
        self.assertEqual([row["name"] for row in xz["areas"]], ["Xuzhou CBZ", "Xuzhou BLC"])
        self.assertNotIn("xuzhou_trade_total", xz)
        self.assertNotIn("specific_area_total", xz)
        for boundary in (
            "CUSTOMS_PLAINTEXT_HTTP_REQUIRES_CORROBORATION",
            "CUSTOMS_CROSS_CURRENCY_VALUES_NOT_DIRECTLY_COMPARABLE",
            "XUZHOU_SPECIFIC_AREA_TRADE_IS_NOT_CITY_TOTAL",
            "PROVINCE_CORROBORATION_DOES_NOT_CORROBORATE_XUZHOU_SPECIFIC_AREA_VALUES",
        ):
            self.assertIn(boundary, snapshot["truth_boundaries"])

    def test_pending_customs_corroboration_cannot_make_jiangsu_trade_available(self):
        customs_payload = {
            "source_id": "CN_CUSTOMS",
            "period": "2026-08",
            "unit": "USD_THOUSAND",
            "transport_security": "PLAINTEXT_HTTP",
            "corroboration_status": "PENDING",
            "corroboration": {
                "status": "NO_SAME_PERIOD_HTTPS_CORROBORATION",
                "known_corroboration_period": "2026-07",
            },
            "jiangsu_importer_exporter_location": {
                "name": "Jiangsu Province",
                "total_ytd_usd_thousand": 700000000.0,
            },
            "xuzhou_importer_exporter_location": None,
            "xuzhou_specific_areas": [{"name": "Xuzhou CBZ", "total_ytd_usd_thousand": 510000.0}],
        }
        snapshot = collect_money_flow_snapshot(
            feeds=[
                SnapshotFeed(
                    key="jiangsu_customs_trade_flow",
                    geography="Jiangsu/XuzhouSpecificAreas",
                    evidence_role="provincial_trade_flow_and_specific_area_customs_activity",
                    collect=_available(customs_payload),
                )
            ]
        )
        self.assertEqual(snapshot["answerability"]["jiangsu_trade_flow"]["status"], "PARTIAL")
        self.assertEqual(snapshot["answerability"]["xuzhou_specific_area_trade"]["status"], "PARTIAL")
        self.assertEqual(snapshot["answerability"]["xuzhou_city_trade_flow"]["status"], "UNKNOWN")

    def test_scoped_sme_funding_demand_is_partial_but_not_private(self):
        payload = {
            "source_id": "XZ_GOV_FINANCE_DEMAND",
            "data_available": True,
            "evidence_kind": "SCOPED_DIRECT_ENTERPRISE_FINANCING_DEMAND",
            "event_count": 1,
            "error_count": 0,
            "latest_freshness": {"publication_date": "2025-12-15", "status": "AGING"},
            "events": [
                {
                    "actor_scope": "SME_AND_MICRO",
                    "private_enterprise_scope_explicit": False,
                    "coverage_scope": "SCOPED_PROGRAM_OR_REPORTED_BATCH",
                    "program_name": "银企同心 产融共进",
                    "demand_amount_cny_100m": "13.6",
                    "aggregation_allowed": False,
                }
            ],
        }
        snapshot = collect_money_flow_snapshot(
            feeds=[
                SnapshotFeed(
                    key="xuzhou_scoped_enterprise_funding_demand",
                    geography="Xuzhou",
                    evidence_role="scoped_direct_enterprise_financing_demand",
                    collect=_available(payload),
                )
            ]
        )
        answerability = snapshot["answerability"]
        self.assertEqual(answerability["xuzhou_enterprise_funding_demand"]["status"], "PARTIAL")
        self.assertEqual(answerability["xuzhou_private_enterprise_funding_demand"]["status"], "UNKNOWN")
        headline = snapshot["headline_evidence"]["Xuzhou"]["enterprise_financing_demand"]
        self.assertEqual(headline["events"][0]["demand_amount_cny_100m"], "13.6")
        self.assertEqual(headline["aggregation_policy"], "NO_CROSS_PROGRAM_OR_PERIOD_SUM")
        self.assertNotIn("total_demand_amount_cny_100m", headline)
        for boundary in (
            "SCOPED_ENTERPRISE_FUNDING_DEMAND_IS_NOT_CITYWIDE_TOTAL",
            "SME_IS_NOT_PRIVATE_ENTERPRISE",
            "NO_CROSS_PROGRAM_FINANCING_DEMAND_SUM",
            "DIRECT_FUNDING_DEMAND_EVIDENCE_PROVES_NEED_ONLY",
        ):
            self.assertIn(boundary, snapshot["truth_boundaries"])

    def test_explicit_private_scoped_event_is_still_partial_not_citywide(self):
        payload = {
            "source_id": "XZ_GOV_FINANCE_DEMAND",
            "data_available": True,
            "evidence_kind": "SCOPED_DIRECT_ENTERPRISE_FINANCING_DEMAND",
            "event_count": 1,
            "error_count": 0,
            "events": [
                {
                    "actor_scope": "PRIVATE_ENTERPRISE",
                    "private_enterprise_scope_explicit": True,
                    "coverage_scope": "SCOPED_PROGRAM_OR_REPORTED_BATCH",
                    "demand_amount_cny_100m": "2.0",
                    "aggregation_allowed": False,
                }
            ],
        }
        snapshot = collect_money_flow_snapshot(
            feeds=[
                SnapshotFeed(
                    key="xuzhou_scoped_enterprise_funding_demand",
                    geography="Xuzhou",
                    evidence_role="scoped_direct_enterprise_financing_demand",
                    collect=_available(payload),
                )
            ]
        )
        self.assertEqual(snapshot["answerability"]["xuzhou_enterprise_funding_demand"]["status"], "PARTIAL")
        self.assertEqual(snapshot["answerability"]["xuzhou_private_enterprise_funding_demand"]["status"], "PARTIAL")
        self.assertNotEqual(snapshot["answerability"]["xuzhou_private_enterprise_funding_demand"]["status"], "AVAILABLE")

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
        self.assertEqual(snapshot["schema_version"], "money-flow-snapshot-v3")
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
