import unittest

from src.pbc_observation_adapter import pbc_money_flow_observations


class PbcObservationAdapterTests(unittest.TestCase):
    def _payload(self):
        digest = "a" * 64
        return {
            "source_id": "CN_PBOC",
            "data_available": True,
            "latest_release": {
                "title": "2026年8月金融统计数据报告",
                "source_url": "https://www.pbc.gov.cn/diaochatongjisi/report/index.html",
                "release_date": "2026-09-14",
                "metric_count": 3,
                "metrics": {
                    "m2_balance": {"value": 356.81, "unit": "trillion_cny", "yoy_pct": 7.5},
                    "social_financing_flow_ytd": {"value": 23.91, "unit": "trillion_cny"},
                    "social_financing_stock": {"value": 464.8, "unit": "trillion_cny", "yoy_pct": 7.2},
                },
                "metric_evidence": {
                    "m2_balance": {
                        "value_excerpt": "广义货币（M2）余额356.81万亿元",
                        "yoy_excerpt": "广义货币（M2）余额356.81万亿元，同比增长7.5%",
                    },
                    "social_financing_flow_ytd": {
                        "value_excerpt": "社会融资规模增量累计为23.91万亿元",
                    },
                    "social_financing_stock": {
                        "value_excerpt": "社会融资规模存量为464.8万亿元",
                        "yoy_excerpt": "社会融资规模存量为464.8万亿元，同比增长7.2%",
                    },
                },
            },
            "provenance": {
                "report": {
                    "source_id": "CN_PBOC",
                    "url": "https://www.pbc.gov.cn/diaochatongjisi/report/index.html",
                    "payload_sha256": digest,
                    "fetched_at_utc": "2026-09-15T02:55:37.670084+00:00",
                }
            },
        }

    def test_report_is_one_observation_with_state_flow_and_separate_change_claims(self):
        envelope = pbc_money_flow_observations(self._payload())[0]
        self.assertEqual(envelope.source_id, "CN_PBOC")
        self.assertEqual(envelope.actor_ids, ())
        claims = {claim.concept: claim for claim in envelope.claims}
        self.assertEqual(claims["CN_PBOC_M2_BALANCE"].primitive, "STATE")
        self.assertEqual(claims["CN_PBOC_M2_BALANCE_YOY"].primitive, "CHANGE")
        self.assertEqual(claims["CN_PBOC_SOCIAL_FINANCING_STOCK"].primitive, "STATE")
        self.assertEqual(claims["CN_PBOC_SOCIAL_FINANCING_STOCK_YOY"].primitive, "CHANGE")
        self.assertEqual(claims["CN_PBOC_SOCIAL_FINANCING_FLOW_YTD"].primitive, "FLOW")
        self.assertTrue(all(claim.epistemic_status == "OBSERVED" for claim in envelope.claims))
        self.assertNotIn("PAYER", {claim.concept for claim in envelope.claims})
        self.assertNotIn("PAID_NEED", {claim.concept for claim in envelope.claims})

    def test_yoy_change_claim_uses_yoy_excerpt_not_value_excerpt(self):
        envelope = pbc_money_flow_observations(self._payload())[0]
        evidence = {item.ref_id: item for item in envelope.evidence}
        yoy_claim = next(claim for claim in envelope.claims if claim.concept == "CN_PBOC_M2_BALANCE_YOY")
        self.assertEqual(yoy_claim.evidence_refs, ("report-yoy:m2_balance",))
        self.assertIn("同比增长7.5%", evidence["report-yoy:m2_balance"].excerpt)
        self.assertEqual(evidence["report-yoy:m2_balance"].content_hash, "a" * 64)

    def test_metric_without_exact_evidence_fails_closed(self):
        payload = self._payload()
        del payload["latest_release"]["metric_evidence"]["m2_balance"]
        with self.assertRaisesRegex(ValueError, "coverage diverges"):
            pbc_money_flow_observations(payload)

    def test_yoy_without_yoy_excerpt_fails_closed(self):
        payload = self._payload()
        del payload["latest_release"]["metric_evidence"]["m2_balance"]["yoy_excerpt"]
        with self.assertRaisesRegex(ValueError, "yoy_excerpt"):
            pbc_money_flow_observations(payload)

    def test_report_url_must_match_provenance(self):
        payload = self._payload()
        payload["latest_release"]["source_url"] = "https://www.pbc.gov.cn/different/index.html"
        with self.assertRaisesRegex(ValueError, "diverges"):
            pbc_money_flow_observations(payload)

    def test_unknown_metric_fails_closed_instead_of_guessing_primitive(self):
        payload = self._payload()
        payload["latest_release"]["metrics"]["mystery_metric"] = {"value": 1, "unit": "unknown"}
        payload["latest_release"]["metric_evidence"]["mystery_metric"] = {"value_excerpt": "mystery 1"}
        payload["latest_release"]["metric_count"] = 4
        with self.assertRaisesRegex(ValueError, "unsupported PBC metric"):
            pbc_money_flow_observations(payload)


if __name__ == "__main__":
    unittest.main()
