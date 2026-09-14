import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from src.live_observation_adapters import (
    jiangsu_money_flow_observations,
    xuzhou_procurement_observations,
    xuzhou_resource_underuse_observations,
)
from src.live_observation_pipeline import ingest_live_observations, summarize_live_store
from src.observation_store import SQLiteObservationStore


class LiveObservationAdapterTests(unittest.TestCase):
    def _jiangsu(self):
        source_hash = "a" * 64
        url = "https://tj.jiangsu.gov.cn/art/2026/8/24/example.html"
        return {
            "source_id": "JS_STATS",
            "data_available": True,
            "geography": "Jiangsu",
            "observation_period": "2026-01..2026-07",
            "publication_date": "2026-08-24",
            "release_url": url,
            "metrics": [
                {
                    "source_id": "JS_STATS",
                    "signal_id": "JS_RETAIL_YOY",
                    "metric_kind": "yoy_growth",
                    "value": "1.1",
                    "unit": "%",
                    "matched_text": "社会消费品零售总额同比增长1.1%",
                    "publication_date": "2026-08-24",
                    "observation_period": None,
                    "source_url": url,
                    "provenance_sha256": source_hash,
                },
                {
                    "source_id": "JS_STATS",
                    "signal_id": "JS_RMB_DEPOSIT_LEVEL_TRILLION_CNY",
                    "metric_kind": "level",
                    "value": "29",
                    "unit": "trillion_cny",
                    "matched_text": "人民币存款余额29万亿元",
                    "publication_date": "2026-08-24",
                    "observation_period": None,
                    "source_url": url,
                    "provenance_sha256": source_hash,
                },
            ],
            "provenance": {
                "release": {
                    "url": url,
                    "payload_sha256": source_hash,
                    "fetched_at_utc": "2026-09-13T09:41:53+00:00",
                }
            },
        }

    def _procurement(self):
        return {
            "source_id": "XZ_GGZY",
            "error_count": 0,
            "events": [
                {
                    "source_id": "XZ_GGZY",
                    "project_id": "JSZC-TEST-001",
                    "project_name": "测试采购项目",
                    "title": "测试采购项目公开招标公告",
                    "url": "https://ggzy.zwb.xz.gov.cn/example.html",
                    "publication_date": "2026-09-11",
                    "budget_raw": "预算金额：100.00万元",
                    "budget_rmb": "1000000.00",
                    "deadline": "2026-10-09 09:30",
                    "joint_venture_allowed": "否",
                    "procurement_method": None,
                    "contract_term": None,
                    "provenance": {
                        "url": "https://ggzy.zwb.xz.gov.cn/example.html",
                        "payload_sha256": "b" * 64,
                        "fetched_at_utc": "2026-09-13T06:45:20+00:00",
                    },
                }
            ],
        }

    def _linked_asset(self, *, underuse="OBSERVED", relisting=True):
        return {
            "error_count": 0,
            "listings": [
                {
                    "source_id": "EJY365_XZ_LINKED",
                    "url": "https://www.ejy365.com/info/example",
                    "title": "某房产二次挂牌招租项目公告",
                    "project_id": "HHCQ2026TEST",
                    "monitoring_code": "GR2026TEST-2",
                    "publication_date": "2026-09-11",
                    "listing_mode": "LEASE",
                    "listing_round": 2 if relisting else None,
                    "relisting_observed": relisting,
                    "resource_state": "DISCOVERED",
                    "underuse_evidence_state": underuse,
                    "underuse_excerpt": "标的状态 空置" if underuse == "OBSERVED" else None,
                    "asking_price_rmb": "15260.00",
                    "asking_price_raw": "挂牌价 15,260 元",
                    "location": "江苏",
                    "owner_actor": "睢宁润盈资产经营有限公司",
                    "publisher_actor": "徐州淮海产权服务有限公司",
                    "source_origin_verified": True,
                    "detail_provenance": {
                        "url": "https://www.ejy365.com/info/example",
                        "payload_sha256": "c" * 64,
                        "fetched_at_utc": "2026-09-13T07:26:50+00:00",
                    },
                    "discovery_provenance": {
                        "url": "https://ggzy.zwb.xz.gov.cn/jyxx/003010/list.html",
                        "payload_sha256": "d" * 64,
                        "fetched_at_utc": "2026-09-13T07:26:47+00:00",
                    },
                }
            ],
        }

    def test_jiangsu_macro_is_actorless_and_preserves_metric_semantics(self):
        envelope = jiangsu_money_flow_observations(self._jiangsu())[0]
        self.assertEqual(envelope.actor_ids, ())
        claims = {claim.concept: claim for claim in envelope.claims}
        self.assertEqual(claims["JS_RETAIL_YOY"].primitive, "CHANGE")
        self.assertEqual(claims["JS_RMB_DEPOSIT_LEVEL_TRILLION_CNY"].primitive, "STATE")
        self.assertTrue(all(c.epistemic_status == "OBSERVED" for c in envelope.claims))

    def test_procurement_budget_is_declared_flow_not_payment(self):
        envelope = xuzhou_procurement_observations(self._procurement())[0]
        claims = {claim.concept: claim for claim in envelope.claims}
        self.assertIn("DECLARED_PROCUREMENT_BUDGET", claims)
        self.assertEqual(claims["DECLARED_PROCUREMENT_BUDGET"].value["payment_status"], "NOT_ESTABLISHED")
        self.assertNotIn("PAID_NEED", claims)
        self.assertNotIn("PAYER_CONFIRMED", claims)
        self.assertEqual(envelope.actor_ids, ())

    def test_linked_asset_preserves_owner_and_underuse_without_availability(self):
        envelope = xuzhou_resource_underuse_observations(self._linked_asset())[0]
        concepts = {claim.concept for claim in envelope.claims}
        self.assertIn("PUBLICLY_LISTED_ASSET_OR_RIGHT", concepts)
        self.assertIn("EXPLICIT_RESOURCE_UNDERUSE_OR_VACANCY", concepts)
        self.assertIn("PUBLIC_LISTING_REPEATED", concepts)
        self.assertNotIn("CURRENT_AVAILABILITY_CONFIRMED", concepts)
        self.assertEqual(len(envelope.actor_ids), 1)
        listed = next(c for c in envelope.claims if c.concept == "PUBLICLY_LISTED_ASSET_OR_RIGHT")
        self.assertEqual(listed.value["owner_actor_as_named"], "睢宁润盈资产经营有限公司")
        self.assertEqual(listed.value["publisher_actor_as_named"], "徐州淮海产权服务有限公司")
        self.assertNotEqual(envelope.actor_ids[0], "徐州淮海产权服务有限公司")

    def test_relisting_does_not_manufacture_underuse(self):
        envelope = xuzhou_resource_underuse_observations(self._linked_asset(underuse="UNKNOWN", relisting=True))[0]
        concepts = {claim.concept for claim in envelope.claims}
        self.assertIn("PUBLIC_LISTING_REPEATED", concepts)
        self.assertNotIn("EXPLICIT_RESOURCE_UNDERUSE_OR_VACANCY", concepts)

    def test_linked_asset_requires_verified_official_discovery_origin(self):
        payload = self._linked_asset()
        payload["listings"][0]["source_origin_verified"] = False
        with self.assertRaisesRegex(ValueError, "verified Xuzhou source origin"):
            xuzhou_resource_underuse_observations(payload)

    def test_observed_underuse_requires_excerpt(self):
        payload = self._linked_asset()
        payload["listings"][0]["underuse_excerpt"] = None
        with self.assertRaisesRegex(ValueError, "requires explicit evidence excerpt"):
            xuzhou_resource_underuse_observations(payload)


class LiveObservationPersistenceTests(unittest.TestCase):
    def _envelope(self):
        fixture = LiveObservationAdapterTests(methodName="runTest")
        return jiangsu_money_flow_observations(fixture._jiangsu())[0]

    def test_refetch_of_unchanged_source_does_not_inflate_history(self):
        first = self._envelope()
        later = replace(first, observed_at="2026-09-14T09:41:53+00:00", retrieved_at="2026-09-14T09:41:53+00:00")
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteObservationStore(Path(tmp) / "live.db") as store:
                first_counts = ingest_live_observations(store, [first])
                second_counts = ingest_live_observations(store, [later])
                self.assertEqual(first_counts["FIRST_SEEN"], 1)
                self.assertEqual(second_counts["UNCHANGED_SOURCE_CONTENT"], 1)
                self.assertEqual(len(store.history(first.source_id, first.observation_id)), 1)

    def test_parser_change_is_preserved_as_revision(self):
        first = self._envelope()
        later = replace(
            first,
            retrieved_at="2026-09-14T09:41:53+00:00",
            observed_at="2026-09-14T09:41:53+00:00",
            parser_version="live-observation-adapters.v2",
        )
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteObservationStore(Path(tmp) / "live.db") as store:
                ingest_live_observations(store, [first])
                counts = ingest_live_observations(store, [later])
                self.assertEqual(counts["REVISION"], 1)
                self.assertEqual(len(store.history(first.source_id, first.observation_id)), 2)

    def test_summary_remains_observation_only(self):
        envelope = self._envelope()
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteObservationStore(Path(tmp) / "live.db") as store:
                counts = ingest_live_observations(store, [envelope])
                summary = summarize_live_store(
                    store,
                    input_observation_count=1,
                    transition_counts=counts,
                    upstream_manifest={"jiangsu_run_id": 123},
                )
        self.assertFalse(summary["fixture_only"])
        self.assertEqual(summary["current_observation_count"], 1)
        self.assertEqual(summary["epistemic_counts"], {"OBSERVED": 2})
        self.assertIn("DECLARED_PROCUREMENT_BUDGET_NE_PAYMENT", summary["truth_boundaries"])
        self.assertNotIn("OPPORTUNITY_CONFIRMED", summary["concepts"])


if __name__ == "__main__":
    unittest.main()
