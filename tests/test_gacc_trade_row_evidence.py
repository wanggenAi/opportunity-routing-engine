import unittest

from src.gacc_trade_row_evidence import (
    ROW_EVIDENCE_CONTRACT,
    enrich_gacc_trade_row_evidence,
    validate_gacc_trade_row_evidence,
)


TABLE8_URL = "http://english.customs.gov.cn/Statics/11111111-2222-3333-4444-555555555555.html"
TABLE11_URL = "http://english.customs.gov.cn/Statics/66666666-7777-8888-9999-aaaaaaaaaaaa.html"

TABLE8 = """
<html><body><table>
<tr><th>Location</th><th>Exp M</th><th>Exp YTD</th><th>Imp M</th><th>Imp YTD</th><th>Exp YoY</th><th>Imp YoY</th></tr>
<tr><td>Jiangsu Province</td><td>60</td><td>420</td><td>40</td><td>280</td><td>4.0</td><td>1.5</td></tr>
<tr><td>Xuzhou</td><td>7</td><td>50</td><td>3</td><td>20</td><td>6.0</td><td>2.0</td></tr>
</table></body></html>
"""

TABLE11 = """
<html><body><table>
<tr><th>Specific Area</th><th>Total M</th><th>Total YTD</th><th>Exp M</th><th>Exp YTD</th><th>Imp M</th><th>Imp YTD</th><th>Total YoY</th><th>Exp YoY</th><th>Imp YoY</th></tr>
<tr><td>Xuzhou CBZ</td><td>8</td><td>55</td><td>6</td><td>40</td><td>2</td><td>15</td><td>-2.0</td><td>1.0</td><td>-9.0</td></tr>
</table></body></html>
"""


class FakeEnvelope:
    def __init__(self, url, html, sha):
        self.url = url
        self.html = html
        self._sha = sha

    def metadata(self):
        return {
            "source_id": "CN_CUSTOMS",
            "request_name": "fake.row.evidence",
            "url": self.url,
            "http_status": 200,
            "content_type": "text/html; charset=utf-8",
            "payload_sha256": self._sha,
        }


class FakeClient:
    def __init__(self, mapping, hashes):
        self.mapping = dict(mapping)
        self.hashes = dict(hashes)

    def fetch(self, url, *, request_name, params=None, headers=None):
        return FakeEnvelope(url, self.mapping[url], self.hashes[url])


def payload():
    return {
        "source_id": "CN_CUSTOMS",
        "transport_security": "PLAINTEXT_HTTP",
        "corroboration_required": True,
        "jiangsu_importer_exporter_location": {
            "name": "Jiangsu Province",
            "total_ytd_usd_thousand": 700.0,
        },
        "xuzhou_importer_exporter_location": {
            "name": "Xuzhou",
            "total_ytd_usd_thousand": 70.0,
        },
        "xuzhou_specific_areas": [
            {
                "name": "Xuzhou CBZ",
                "total_ytd_usd_thousand": 55.0,
            }
        ],
        "table_8_provenance": {
            "source_id": "CN_CUSTOMS",
            "url": TABLE8_URL,
            "payload_sha256": "8" * 64,
        },
        "table_11_provenance": {
            "source_id": "CN_CUSTOMS",
            "url": TABLE11_URL,
            "payload_sha256": "1" * 64,
        },
        "truth_boundaries": [],
    }


def client():
    return FakeClient(
        {TABLE8_URL: TABLE8, TABLE11_URL: TABLE11},
        {TABLE8_URL: "8" * 64, TABLE11_URL: "1" * 64},
    )


class GaccTradeRowEvidenceTests(unittest.TestCase):
    def test_enrichment_binds_every_serialized_row_to_exact_source_cells(self):
        enriched = enrich_gacc_trade_row_evidence(payload(), client=client())
        self.assertEqual(enriched["row_evidence_contract"], ROW_EVIDENCE_CONTRACT)
        self.assertTrue(enriched["row_evidence_complete"])

        jiangsu = enriched["jiangsu_importer_exporter_location"]["source_row_evidence"]
        xuzhou = enriched["xuzhou_importer_exporter_location"]["source_row_evidence"]
        area = enriched["xuzhou_specific_areas"][0]["source_row_evidence"]
        self.assertEqual(jiangsu["table_number"], 8)
        self.assertEqual(xuzhou["table_number"], 8)
        self.assertEqual(area["table_number"], 11)
        self.assertEqual(jiangsu["row_cells"], ["Jiangsu Province", "60", "420", "40", "280", "4.0", "1.5"])
        self.assertEqual(area["row_cells"][0], "Xuzhou CBZ")
        self.assertEqual(jiangsu["source_payload_sha256"], "8" * 64)
        self.assertEqual(area["source_payload_sha256"], "1" * 64)
        self.assertEqual(len(jiangsu["row_sha256"]), 64)
        self.assertIn("WHOLE_PAGE_HASH_NE_ROW_LEVEL_LINEAGE", enriched["truth_boundaries"])
        self.assertIn("CORROBORATION_GATE_NE_ROW_LEVEL_VALUE_CONFIRMATION", enriched["truth_boundaries"])
        validate_gacc_trade_row_evidence(enriched)

    def test_whole_page_hash_without_row_evidence_is_not_enough(self):
        with self.assertRaisesRegex(ValueError, "row evidence contract"):
            validate_gacc_trade_row_evidence(payload())

    def test_payload_change_between_parse_and_evidence_refetch_fails_closed(self):
        bad = client()
        bad.hashes[TABLE8_URL] = "f" * 64
        with self.assertRaisesRegex(ValueError, "changed between parse and row-evidence refetch"):
            enrich_gacc_trade_row_evidence(payload(), client=bad)

    def test_missing_or_ambiguous_exact_row_identity_fails_closed(self):
        missing = client()
        missing.mapping[TABLE11_URL] = TABLE11.replace("Xuzhou CBZ", "Other CBZ")
        with self.assertRaisesRegex(ValueError, "matched 0 rows"):
            enrich_gacc_trade_row_evidence(payload(), client=missing)

        duplicate = client()
        duplicate.mapping[TABLE11_URL] = TABLE11.replace(
            "</table>",
            "<tr><td>Xuzhou CBZ</td><td>8</td><td>55</td><td>6</td><td>40</td><td>2</td><td>15</td><td>-2.0</td><td>1.0</td><td>-9.0</td></tr></table>",
        )
        with self.assertRaisesRegex(ValueError, "matched 2 rows"):
            enrich_gacc_trade_row_evidence(payload(), client=duplicate)

    def test_mutated_bound_cells_fail_validation(self):
        enriched = enrich_gacc_trade_row_evidence(payload(), client=client())
        enriched["xuzhou_specific_areas"][0]["source_row_evidence"]["row_cells"][1] = "999"
        with self.assertRaisesRegex(ValueError, "text does not match cells|hash does not match cells"):
            validate_gacc_trade_row_evidence(enriched)

    def test_null_whole_city_row_does_not_get_synthesized(self):
        source = payload()
        source["xuzhou_importer_exporter_location"] = None
        enriched = enrich_gacc_trade_row_evidence(source, client=client())
        self.assertIsNone(enriched["xuzhou_importer_exporter_location"])
        self.assertEqual(enriched["xuzhou_specific_areas"][0]["name"], "Xuzhou CBZ")
        validate_gacc_trade_row_evidence(enriched)


if __name__ == "__main__":
    unittest.main()
