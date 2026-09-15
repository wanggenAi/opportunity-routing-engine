import unittest

from src.official_macro_observation_adapters import (
    nbs_macro_watchlist_observations,
    pbc_jiangsu_credit_observations,
)


class NbsMacroObservationAdapterTests(unittest.TestCase):
    def _payload(self):
        digest = "a" * 64
        request = {
            "content_type": "application/json",
            "fetched_at_utc": "2026-09-14T06:26:45.493744+00:00",
            "http_status": 200,
            "payload_sha256": digest,
            "request_name": "nbs.values.monthData.synthetic",
            "source_id": "CN_NBS",
            "url": "https://data.stats.gov.cn/dg/website/publicrelease/web/external/stream/esData",
        }
        return {
            "source_id": "CN_NBS",
            "active_signal_count": 2,
            "available_signal_count": 2,
            "unavailable_signal_count": 0,
            "groups": [{"request": request}],
            "signals": [
                {
                    "actual_label": "社会消费品零售总额当期值 (亿元)",
                    "actual_unit": "亿元",
                    "configured_label": "社会消费品零售总额当期值 (亿元)",
                    "configured_unit": "亿元",
                    "fetched_at_utc": request["fetched_at_utc"],
                    "frequency": "month",
                    "geography": "China",
                    "identity_status": "MATCH",
                    "latest_advertised_period": "202608MM",
                    "latest_populated_period": "202607MM",
                    "metric_kind": "level",
                    "period_lag": 1,
                    "request_sha256": digest,
                    "selected_record": {
                        "area_code": "000000000000",
                        "area_name": "国家",
                        "cid": "synthetic",
                        "frequency": "month",
                        "indicator_id": "retail-current",
                        "indicator_label": "社会消费品零售总额当期值 (亿元)",
                        "page": "monthData",
                        "period_code": "202607MM",
                        "period_name": "2026年7月",
                        "source_id": "CN_NBS",
                        "unit": "亿元",
                        "value": "39022.3",
                        "value_present": True,
                    },
                    "signal_id": "CN_RETAIL_CURRENT",
                    "source_id": "CN_NBS",
                    "status": "AVAILABLE",
                    "value": "39022.3",
                },
                {
                    "actual_label": "社会消费品零售总额同比增长 (%)",
                    "actual_unit": "%",
                    "configured_label": "社会消费品零售总额同比增长 (%)",
                    "configured_unit": "%",
                    "fetched_at_utc": request["fetched_at_utc"],
                    "frequency": "month",
                    "geography": "China",
                    "identity_status": "MATCH",
                    "latest_advertised_period": "202608MM",
                    "latest_populated_period": "202607MM",
                    "metric_kind": "yoy_growth",
                    "period_lag": 1,
                    "request_sha256": digest,
                    "selected_record": {
                        "area_code": "000000000000",
                        "area_name": "国家",
                        "cid": "synthetic",
                        "frequency": "month",
                        "indicator_id": "retail-yoy",
                        "indicator_label": "社会消费品零售总额同比增长 (%)",
                        "page": "monthData",
                        "period_code": "202607MM",
                        "period_name": "2026年7月",
                        "source_id": "CN_NBS",
                        "unit": "%",
                        "value": "0.6",
                        "value_present": True,
                    },
                    "signal_id": "CN_RETAIL_YOY",
                    "source_id": "CN_NBS",
                    "status": "AVAILABLE",
                    "value": "0.6",
                },
            ],
        }

    def test_level_and_growth_keep_distinct_primitives(self):
        envelopes = nbs_macro_watchlist_observations(self._payload())
        claims = {item.claims[0].concept: item.claims[0] for item in envelopes}
        self.assertEqual(claims["CN_RETAIL_CURRENT"].primitive, "STATE")
        self.assertEqual(claims["CN_RETAIL_YOY"].primitive, "CHANGE")
        self.assertTrue(all(item.actor_ids == () for item in envelopes))
        self.assertTrue(all(item.claims[0].epistemic_status == "OBSERVED" for item in envelopes))

    def test_request_hash_must_bind_to_governed_request(self):
        payload = self._payload()
        payload["signals"][0]["request_sha256"] = "b" * 64
        with self.assertRaisesRegex(ValueError, "request provenance is missing"):
            nbs_macro_watchlist_observations(payload)

    def test_identity_mismatch_fails_closed(self):
        payload = self._payload()
        payload["signals"][0]["identity_status"] = "MISMATCH"
        with self.assertRaisesRegex(ValueError, "exact identity"):
            nbs_macro_watchlist_observations(payload)

    def test_available_count_must_match_source_artifact(self):
        payload = self._payload()
        payload["available_signal_count"] = 1
        with self.assertRaisesRegex(ValueError, "diverges"):
            nbs_macro_watchlist_observations(payload)


class PbcJiangsuObservationAdapterTests(unittest.TestCase):
    def _payload(self):
        return {
            "source_id": "CN_PBOC_JS",
            "data_available": True,
            "geography": "Jiangsu",
            "observation_period": "2026-07",
            "release_date": "2026-08-21",
            "table_title": "2026年7月江苏省金融机构信贷收支表",
            "observation": {
                "metric_evidence": {
                    "total_deposits_100m_cny": {
                        "label_token": "各项存款",
                        "raw_value": 289693.294952456,
                        "row_number_1based": 5,
                        "row_values": ["一、各项存款", 287409.2, 289693.294952456],
                        "value_column_1based": 8,
                    },
                    "total_loans_100m_cny": {
                        "label_token": "各项贷款",
                        "raw_value": 302924.838095299,
                        "row_number_1based": 17,
                        "row_values": ["一、各项贷款", 294491.4, 302924.838095299],
                        "value_column_1based": 8,
                    },
                },
                "metrics": {
                    "total_deposits_100m_cny": 289693.294952456,
                    "total_deposits_trillion_cny": 28.969329495245603,
                    "total_loans_100m_cny": 302924.838095299,
                    "total_loans_trillion_cny": 30.2924838095299,
                },
                "period_gate": "EXPLICIT_PERIOD_HEADER",
                "period_key": "2026.07",
                "sheet_name": "(1)江苏省金融机构人民币信贷收支表",
                "unit": "100m_cny",
            },
            "provenance": {
                "xls": {
                    "content_type": "application/vnd.ms-excel",
                    "fetched_at_utc": "2026-09-14T09:52:09.177090+00:00",
                    "http_status": 200,
                    "payload_sha256": "c" * 64,
                    "request_name": "pbc-js-credit-xls",
                    "size_bytes": 68608,
                    "source_id": "CN_PBOC_JS",
                    "url": "https://nanjing.pbc.gov.cn/nanjing/117532/example.xls",
                }
            },
        }

    def test_only_evidence_backed_source_rows_become_observed_claims(self):
        envelope = pbc_jiangsu_credit_observations(self._payload())[0]
        self.assertEqual(envelope.source_id, "CN_PBOC_JS")
        self.assertEqual(len(envelope.claims), 2)
        concepts = {claim.concept for claim in envelope.claims}
        self.assertEqual(
            concepts,
            {
                "CN_PBOC_JS_TOTAL_DEPOSITS_100M_CNY",
                "CN_PBOC_JS_TOTAL_LOANS_100M_CNY",
            },
        )
        self.assertTrue(all(claim.primitive == "STATE" for claim in envelope.claims))
        self.assertNotIn("CN_PBOC_JS_TOTAL_DEPOSITS_TRILLION_CNY", concepts)
        self.assertNotIn("CN_PBOC_JS_TOTAL_LOANS_TRILLION_CNY", concepts)

    def test_metric_value_must_match_evidence_row(self):
        payload = self._payload()
        payload["observation"]["metrics"]["total_deposits_100m_cny"] = 1
        with self.assertRaisesRegex(ValueError, "diverges"):
            pbc_jiangsu_credit_observations(payload)

    def test_missing_explicit_period_gate_fails_closed(self):
        payload = self._payload()
        payload["observation"]["period_gate"] = "UNKNOWN"
        with self.assertRaisesRegex(ValueError, "period header gate"):
            pbc_jiangsu_credit_observations(payload)


if __name__ == "__main__":
    unittest.main()
