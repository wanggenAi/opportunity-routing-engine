import unittest

from src.gacc_trade_flow import GaccTradeFlowAdapter, parse_html_tables


class FakeEnvelope:
    def __init__(self, url, html):
        self.url = url
        self.html = html

    def metadata(self):
        return {
            "source_id": "CN_CUSTOMS",
            "request_name": "fake",
            "url": self.url,
            "http_status": 200,
            "content_type": "text/html; charset=utf-8",
            "payload_sha256": "a" * 64,
        }


class FakeClient:
    def __init__(self, mapping):
        self.mapping = mapping

    def fetch(self, url, *, request_name, params=None, headers=None):
        return FakeEnvelope(url, self.mapping[url])


INDEX = """
<html><body><select><option>2025</option><option selected>2026</option></select>
<table>
<tr><td>（8）Imports and Exports by Location of Importers/Exporters</td>
<td><a href='/Statics/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee.html'>Jun.</a></td>
<td><a href='/Statics/11111111-2222-3333-4444-555555555555.html'>Jul.</a></td></tr>
<tr><td>（11）Imports and Exports by Specific Areas</td>
<td><a href='/Statics/bbbbbbbb-bbbb-cccc-dddd-eeeeeeeeeeee.html'>Jun.</a></td>
<td><a href='/Statics/66666666-7777-8888-9999-aaaaaaaaaaaa.html'>Jul.</a></td></tr>
</table></body></html>
"""

TABLE8_JUL = """
<html><body><h1>（8）Imports and Exports by Location of Importers/Exporters,1-7.2026</h1>
<p>Unit:US$1,000</p><table>
<tr><th>Location of Importers/Exporters</th><th colspan='2'>Exports</th><th colspan='2'>Imports</th><th colspan='2'>Percentage Change</th></tr>
<tr><th>7</th><th>1to7</th><th>7</th><th>1to7</th><th>Exports</th><th>Imports</th></tr>
<tr><td>Jiangsu Province</td><td>60</td><td>420</td><td>40</td><td>280</td><td>4.0</td><td>1.5</td></tr>
<tr><td>Xuzhou</td><td>7</td><td>50</td><td>3</td><td>20</td><td>6.0</td><td>2.0</td></tr>
</table></body></html>
"""

TABLE11_JUL = """
<html><body><h1>（11）Imports and Exports by Specific Areas, 7.2026</h1>
<p>Unit: US$1,000</p><table>
<tr><th>Specific Areas</th><th colspan='2'>Total</th><th colspan='2'>Exports</th><th colspan='2'>Imports</th><th colspan='3'>Percentage Change</th></tr>
<tr><th>7</th><th>1to7</th><th>7</th><th>1to7</th><th>7</th><th>1to7</th><th>Total</th><th>Exports</th><th>Imports</th></tr>
<tr><td>Xuzhou CBZ</td><td>8</td><td>55</td><td>6</td><td>40</td><td>2</td><td>15</td><td>-2.0</td><td>1.0</td><td>-9.0</td></tr>
<tr><td>Xuzhou BLC</td><td>2</td><td>15</td><td>1</td><td>10</td><td>1</td><td>5</td><td>-4.0</td><td>-3.0</td><td>-6.0</td></tr>
</table></body></html>
"""

TABLE8_JUN = TABLE8_JUL.replace("1-7.2026", "1-6.2026")
TABLE11_JUN = TABLE11_JUL.replace("7.2026", "6.2026")


class GaccTradeFlowTests(unittest.TestCase):
    def _adapter(self):
        base = "http://english.customs.gov.cn"
        return GaccTradeFlowAdapter(client=FakeClient({
            f"{base}/statics/report/monthly.html": INDEX,
            f"{base}/Statics/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee.html": TABLE8_JUN,
            f"{base}/Statics/11111111-2222-3333-4444-555555555555.html": TABLE8_JUL,
            f"{base}/Statics/bbbbbbbb-bbbb-cccc-dddd-eeeeeeeeeeee.html": TABLE11_JUN,
            f"{base}/Statics/66666666-7777-8888-9999-aaaaaaaaaaaa.html": TABLE11_JUL,
        }))

    def test_table_parser_retains_same_cell_links(self):
        rows = parse_html_tables(INDEX, base_url="http://english.customs.gov.cn/statics/report/monthly.html")
        self.assertIn("Location of Importers/Exporters", rows[0][0]["text"])
        self.assertTrue(rows[0][1]["links"][0].startswith("http://english.customs.gov.cn/Statics/"))

    def test_collect_separates_city_location_from_specific_areas(self):
        payload = self._adapter().collect()
        self.assertEqual(payload["period"], "2026-07")
        self.assertEqual(payload["transport_security"], "PLAINTEXT_HTTP")
        self.assertTrue(payload["corroboration_required"])
        self.assertEqual(payload["corroboration_status"], "PENDING")
        jiangsu = payload["jiangsu_importer_exporter_location"]
        self.assertEqual(jiangsu["name"], "Jiangsu Province")
        self.assertEqual(jiangsu["total_ytd_usd_thousand"], 700.0)
        self.assertEqual(jiangsu["total_basis"], "DERIVED_EXPORT_PLUS_IMPORT")
        self.assertIsNone(jiangsu["total_yoy_percent"])
        self.assertEqual(payload["xuzhou_importer_exporter_location"]["total_ytd_usd_thousand"], 70.0)
        names = [row["name"] for row in payload["xuzhou_specific_areas"]]
        self.assertEqual(names, ["Xuzhou CBZ", "Xuzhou BLC"])
        self.assertTrue(all(row["total_basis"] == "EXPLICIT_GACC" for row in payload["xuzhou_specific_areas"]))
        self.assertIn("TABLE8_TOTAL_DERIVED_ONLY_FROM_COMPLETE_EXPORT_IMPORT", payload["truth_boundaries"])
        self.assertIn("PLAINTEXT_HTTP_REQUIRES_CORROBORATION", payload["truth_boundaries"])
        self.assertIn("SPECIFIC_AREA_IS_NOT_WHOLE_XUZHOU", payload["truth_boundaries"])
        self.assertIn("NO_CROSS_TABLE_SUM", payload["truth_boundaries"])

    def test_missing_table8_component_stays_unknown_not_zero(self):
        adapter = self._adapter()
        base = "http://english.customs.gov.cn"
        adapter.client.mapping[f"{base}/Statics/11111111-2222-3333-4444-555555555555.html"] = TABLE8_JUL.replace(
            "<tr><td>Xuzhou</td><td>7</td><td>50</td><td>3</td><td>20</td><td>6.0</td><td>2.0</td></tr>",
            "<tr><td>Xuzhou</td><td>7</td><td>50</td><td>-</td><td>20</td><td>6.0</td><td>2.0</td></tr>",
        )
        payload = adapter.collect()
        row = payload["xuzhou_importer_exporter_location"]
        self.assertIsNone(row["imports_month_usd_thousand"])
        self.assertIsNone(row["total_month_usd_thousand"])
        self.assertEqual(row["total_ytd_usd_thousand"], 70.0)

    def test_inconsistent_table11_explicit_total_row_is_rejected(self):
        adapter = self._adapter()
        base = "http://english.customs.gov.cn"
        adapter.client.mapping[f"{base}/Statics/66666666-7777-8888-9999-aaaaaaaaaaaa.html"] = TABLE11_JUL.replace(
            "<tr><td>Xuzhou CBZ</td><td>8</td><td>55</td><td>6</td><td>40</td><td>2</td><td>15</td>",
            "<tr><td>Xuzhou CBZ</td><td>99</td><td>55</td><td>6</td><td>40</td><td>2</td><td>15</td>",
        )
        payload = adapter.collect()
        self.assertEqual([row["name"] for row in payload["xuzhou_specific_areas"]], ["Xuzhou BLC"])

    def test_missing_xuzhou_is_not_silently_promoted(self):
        adapter = self._adapter()
        base = "http://english.customs.gov.cn"
        adapter.client.mapping[f"{base}/Statics/11111111-2222-3333-4444-555555555555.html"] = TABLE8_JUL.replace(
            "<tr><td>Xuzhou</td><td>7</td><td>50</td><td>3</td><td>20</td><td>6.0</td><td>2.0</td></tr>", ""
        )
        payload = adapter.collect()
        self.assertIsNone(payload["xuzhou_importer_exporter_location"])
        self.assertEqual(len(payload["xuzhou_specific_areas"]), 2)

    def test_selected_year_conflict_fails_closed(self):
        adapter = self._adapter()
        base = "http://english.customs.gov.cn"
        adapter.client.mapping[f"{base}/Statics/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee.html"] = TABLE8_JUN.replace("2026", "2025")
        adapter.client.mapping[f"{base}/Statics/11111111-2222-3333-4444-555555555555.html"] = TABLE8_JUL.replace("2026", "2025")
        adapter.client.mapping[f"{base}/Statics/bbbbbbbb-bbbb-cccc-dddd-eeeeeeeeeeee.html"] = TABLE11_JUN.replace("2026", "2025")
        adapter.client.mapping[f"{base}/Statics/66666666-7777-8888-9999-aaaaaaaaaaaa.html"] = TABLE11_JUL.replace("2026", "2025")
        with self.assertRaisesRegex(ValueError, "selected bulletin year conflicts"):
            adapter.collect()


if __name__ == "__main__":
    unittest.main()
