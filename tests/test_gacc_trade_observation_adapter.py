import hashlib
import json
import unittest

from src.gacc_trade_observation_adapter import gacc_trade_flow_observations


def _row_evidence(name, cells, table, payload_hash, url):
    digest = hashlib.sha256(
        json.dumps(cells, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "contract": "gacc-source-row-evidence.v1",
        "source_id": "CN_CUSTOMS",
        "table_number": table,
        "source_url": url,
        "source_payload_sha256": payload_hash,
        "row_identity": name,
        "row_cells": cells,
        "row_text": " | ".join(cells),
        "row_sha256": digest,
        "parser_contract": (
            "GACC_TABLE_8_IMPORTER_EXPORTER_LOCATION_V1"
            if table == 8
            else "GACC_TABLE_11_SPECIFIC_AREA_V1"
        ),
    }


def _payload():
    table8_hash = "8" * 64
    table11_hash = "1" * 64
    table8_url = "http://english.customs.gov.cn/Statics/11111111-2222-3333-4444-555555555555.html"
    table11_url = "http://english.customs.gov.cn/Statics/66666666-7777-8888-9999-aaaaaaaaaaaa.html"
    js_hash = "a" * 64
    boundaries = [
        "PLAINTEXT_HTTP_REQUIRES_CORROBORATION",
        "TABLE8_TOTAL_DERIVED_ONLY_FROM_COMPLETE_EXPORT_IMPORT",
        "IMPORTER_EXPORTER_LOCATION_IS_NOT_DOMESTIC_ORIGIN_DESTINATION",
        "SPECIFIC_AREA_IS_NOT_WHOLE_XUZHOU",
        "NO_CROSS_TABLE_SUM",
        "MISSING_STAYS_UNKNOWN",
        "TRADE_FLOW_IS_NOT_UNMET_NEED",
        "TRADE_FLOW_IS_NOT_SURPLUS_RESOURCE",
        "NO_TRANSACTION_BLOCKER_INFERENCE",
        "NO_OPPORTUNITY_INFERENCE",
        "ROW_EVIDENCE_REQUIRES_STABLE_REFETCH",
        "WHOLE_PAGE_HASH_NE_ROW_LEVEL_LINEAGE",
        "CORROBORATION_GATE_NE_ROW_LEVEL_VALUE_CONFIRMATION",
        "DERIVED_TOTAL_NE_SOURCE_CELL",
    ]
    jiangsu_cells = ["Jiangsu Province", "60", "420", "40", "280", "4.0", "1.5"]
    cbz_cells = ["Xuzhou CBZ", "8", "55", "6", "40", "2", "15", "-2.0", "1.0", "-9.0"]
    blc_cells = ["Xuzhou BLC", "2", "15", "1", "10", "1", "5", "-4.0", "-3.0", "-6.0"]
    return {
        "source_id": "CN_CUSTOMS",
        "evidence_kind": "CUSTOMS_TRADE_FLOW",
        "period": "2026-07",
        "unit": "USD_THOUSAND",
        "transport_security": "PLAINTEXT_HTTP",
        "corroboration_required": True,
        "corroboration_status": "PERIOD_IDENTITY_DIRECTION_CORROBORATED",
        "corroboration": {
            "source_id": "JS_GOV",
            "source_authority": "JIANGSU_GOVERNMENT_HTTPS_REPOST_CITING_NANJING_CUSTOMS",
            "period": "2026-07",
            "geography": "Jiangsu",
            "basis": "PERIOD_IDENTITY_DIRECTION_ONLY",
            "reported_currency": "CNY",
            "monetary_value_comparison": "UNAVAILABLE_CROSS_CURRENCY",
            "reported_month": {"exports_100m_cny": 1.0, "imports_100m_cny": 1.0, "total_100m_cny": 2.0},
            "reported_ytd": {"exports_trillion_cny": 1.0, "imports_trillion_cny": 1.0, "total_trillion_cny": 2.0},
            "provenance": {
                "source_id": "JS_GOV",
                "url": "https://jszwb.jiangsu.gov.cn/art/2026/8/14/art_71797_11816221.html",
                "fetched_at_utc": "2026-09-15T03:50:59+00:00",
                "payload_sha256": js_hash,
            },
        },
        "row_evidence_contract": "gacc-source-row-evidence.v1",
        "row_evidence_complete": True,
        "table_8_provenance": {
            "source_id": "CN_CUSTOMS",
            "url": table8_url,
            "fetched_at_utc": "2026-09-15T03:50:32+00:00",
            "payload_sha256": table8_hash,
        },
        "table_11_provenance": {
            "source_id": "CN_CUSTOMS",
            "url": table11_url,
            "fetched_at_utc": "2026-09-15T03:50:44+00:00",
            "payload_sha256": table11_hash,
        },
        "jiangsu_importer_exporter_location": {
            "name": "Jiangsu Province",
            "total_month_usd_thousand": 100.0,
            "total_ytd_usd_thousand": 700.0,
            "exports_month_usd_thousand": 60.0,
            "exports_ytd_usd_thousand": 420.0,
            "imports_month_usd_thousand": 40.0,
            "imports_ytd_usd_thousand": 280.0,
            "total_yoy_percent": None,
            "exports_yoy_percent": 4.0,
            "imports_yoy_percent": 1.5,
            "total_basis": "DERIVED_EXPORT_PLUS_IMPORT",
            "source_row_evidence": _row_evidence("Jiangsu Province", jiangsu_cells, 8, table8_hash, table8_url),
        },
        "xuzhou_importer_exporter_location": None,
        "xuzhou_specific_areas": [
            {
                "name": "Xuzhou CBZ",
                "total_month_usd_thousand": 8.0,
                "total_ytd_usd_thousand": 55.0,
                "exports_month_usd_thousand": 6.0,
                "exports_ytd_usd_thousand": 40.0,
                "imports_month_usd_thousand": 2.0,
                "imports_ytd_usd_thousand": 15.0,
                "total_yoy_percent": -2.0,
                "exports_yoy_percent": 1.0,
                "imports_yoy_percent": -9.0,
                "total_basis": "EXPLICIT_GACC",
                "source_row_evidence": _row_evidence("Xuzhou CBZ", cbz_cells, 11, table11_hash, table11_url),
            },
            {
                "name": "Xuzhou BLC",
                "total_month_usd_thousand": 2.0,
                "total_ytd_usd_thousand": 15.0,
                "exports_month_usd_thousand": 1.0,
                "exports_ytd_usd_thousand": 10.0,
                "imports_month_usd_thousand": 1.0,
                "imports_ytd_usd_thousand": 5.0,
                "total_yoy_percent": -4.0,
                "exports_yoy_percent": -3.0,
                "imports_yoy_percent": -6.0,
                "total_basis": "EXPLICIT_GACC",
                "source_row_evidence": _row_evidence("Xuzhou BLC", blc_cells, 11, table11_hash, table11_url),
            },
        ],
        "truth_boundaries": boundaries,
    }


class GaccTradeObservationAdapterTests(unittest.TestCase):
    def test_real_shape_emits_jiangsu_and_specific_areas_without_whole_xuzhou(self):
        envelopes = gacc_trade_flow_observations(_payload())
        self.assertEqual(len(envelopes), 3)
        self.assertTrue(all(item.source_id == "CN_CUSTOMS" for item in envelopes))
        self.assertEqual(
            [item.source_record_id for item in envelopes],
            [
                "2026-07:table8:Jiangsu Province",
                "2026-07:table11:Xuzhou CBZ",
                "2026-07:table11:Xuzhou BLC",
            ],
        )
        self.assertNotIn("2026-07:table8:Xuzhou", [item.source_record_id for item in envelopes])
        self.assertEqual(len(envelopes[0].claims), 6)
        self.assertEqual(len(envelopes[1].claims), 9)
        self.assertEqual(envelopes[0].claims[0].primitive, "FLOW")
        self.assertEqual(envelopes[0].claims[-1].primitive, "CHANGE")
        self.assertNotIn("TOTAL_MONTH", {claim.concept for claim in envelopes[0].claims})
        self.assertIn("whole_xuzhou_trade_flow", envelopes[1].unknown_fields)

    def test_claims_use_exact_gacc_row_not_https_corroboration_as_value_evidence(self):
        envelopes = gacc_trade_flow_observations(_payload())
        for envelope in envelopes:
            self.assertEqual(len(envelope.evidence), 2)
            for claim in envelope.claims:
                self.assertEqual(len(claim.evidence_refs), 1)
                self.assertTrue(claim.evidence_refs[0].startswith("gacc-row:"))
                self.assertNotIn("jiangsu-https-corroboration", claim.evidence_refs)
                self.assertEqual(claim.value["corroboration_basis"], "PERIOD_IDENTITY_DIRECTION_ONLY")
                self.assertEqual(claim.value["monetary_value_comparison"], "UNAVAILABLE_CROSS_CURRENCY")

    def test_pending_or_overclaimed_corroboration_fails_closed(self):
        pending = _payload()
        pending["corroboration_status"] = "PENDING"
        with self.assertRaisesRegex(ValueError, "requires successful"):
            gacc_trade_flow_observations(pending)

        overclaimed = _payload()
        overclaimed["corroboration"]["monetary_value_comparison"] = "CONFIRMED"
        with self.assertRaisesRegex(ValueError, "must not be treated"):
            gacc_trade_flow_observations(overclaimed)

    def test_parsed_value_must_match_exact_row_cells(self):
        data = _payload()
        data["xuzhou_specific_areas"][0]["exports_ytd_usd_thousand"] = 999.0
        with self.assertRaisesRegex(ValueError, "diverges from exact GACC row evidence"):
            gacc_trade_flow_observations(data)

    def test_tampered_row_lineage_fails_before_ingress(self):
        data = _payload()
        data["xuzhou_specific_areas"][0]["source_row_evidence"]["row_cells"][1] = "999"
        with self.assertRaises(ValueError):
            gacc_trade_flow_observations(data)

    def test_missing_whole_xuzhou_and_specific_areas_fails_without_synthesis(self):
        data = _payload()
        data["xuzhou_specific_areas"] = []
        with self.assertRaisesRegex(ValueError, "explicit Xuzhou"):
            gacc_trade_flow_observations(data)

    def test_truth_boundary_removal_fails_closed(self):
        data = _payload()
        data["truth_boundaries"].remove("SPECIFIC_AREA_IS_NOT_WHOLE_XUZHOU")
        with self.assertRaisesRegex(ValueError, "truth boundaries missing"):
            gacc_trade_flow_observations(data)


if __name__ == "__main__":
    unittest.main()
