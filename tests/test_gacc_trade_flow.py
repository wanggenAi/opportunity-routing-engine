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
<tr><th>Location</th><th>Total 7</th><th>Total 1to7</th><th>Exports 7</th><th>Exports 1to7</th><th>Imports 7</th><th>Imports 1to7</th><th>Total YoY</th><th>Export YoY</th><th>Import YoY</th></tr>
<tr><td>Jiangsu</td><td>100</td><td>700</td><td>60</td><td>420</td><td>40</td><td>280</td><td>3.0</td><td>4.0</td><td>1.5</td></tr>
<tr><td>Xuzhou</td><td>10</td><td>70</td><td>7</td><td>50</td><td>3</td><td>20</td><td>5.0</td><td>6.0</td><td>2.0</td></tr>
</table></body></html>
"""

TABLE11_JUL = """
<html><body><h1>（11）Imports and Exports by Specific Areas, 7.2026</h1>
<p>Unit: US$1,000</p><table>
<tr><th>Specific Areas</th><th>Total 7</th><th>Total 1to7</th><th>Exports 7</th><th>Exports 1to7</th><th>Imports 7</th><th>Imports 1to7</th><th>Total YoY</th><th>Export YoY</th><th>Import YoY</th></tr>
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
        self.assertEqual(payload["jiangsu_importer_exporter_location"]["total_ytd_usd_thousand"], 700.0)
        self.assertEqual(payload["xuzhou_importer_exporter_location"]["total_ytd_usd_thousand"], 70.0)
        names = [row["name"] for row in payload["xuzhou_specific_areas"]]
        self.assertEqual(names, ["Xuzhou CBZ", "Xuzhou BLC"])
        self.assertIn("PLAINTEXT_HTTP_REQUIRES_CORROBORATION", payload["truth_boundaries"])
        self.assertIn("SPECIFIC_AREA_IS_NOT_WHOLE_XUZHOU", payload["truth_boundaries"])
        self.assertIn("NO_CROSS_TABLE_SUM", payload["truth_boundaries"])

    def test_missing_xuzhou_is_not_silently_promoted(self):
        adapter = self._adapter()
        base = "http://english.customs.gov.cn"
        adapter.client.mapping[f"{base}/Statics/11111111-2222-3333-4444-555555555555.html"] = TABLE8_JUL.replace(
            "<tr><td>Xuzhou</td><td>10</td><td>70</td><td>7</td><td>50</td><td>3</td><td>20</td><td>5.0</td><td>6.0</td><td>2.0</td></tr>", ""
        )
        payload = adapter.collect()
        self.assertIsNone(payload["xuzhou_importer_exporter_location"])
        self.assertEqual(len(payload["xuzhou_specific_areas"]), 2)

    def test_inconsistent_arithmetic_row_is_rejected(self):
        adapter = self._adapter()
        base = "http://english.customs.gov.cn"
        adapter.client.mapping[f"{base}/Statics/11111111-2222-3333-4444-555555555555.html"] = TABLE8_JUL.replace(
            "<td>100</td><td>700</td><td>60</td><td>420</td><td>40</td><td>280</td>",
            "<td>999</td><td>700</td><td>60</td><td>420</td><td>40</td><td>280</td>",
        )
        with self.assertRaisesRegex(ValueError, "Jiangsu row missing"):
            adapter.collect()

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
