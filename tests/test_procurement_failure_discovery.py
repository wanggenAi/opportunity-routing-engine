import unittest

from src.html_ingest import HtmlFetchEnvelope
from src.xuzhou_procurement_failures import XuzhouProcurementFailureAdapter
from src.xuzhou_procurement_results import XZ_PROCUREMENT_RESULT_LIST


class UrlAwareFakeHtmlClient:
    def __init__(self, html_by_url):
        self.html_by_url = html_by_url
        self.urls = []

    def fetch(self, url, *, request_name, params=None, headers=None):
        self.urls.append((url, request_name))
        html = self.html_by_url.get(url, "<html><body></body></html>")
        return HtmlFetchEnvelope(
            source_id="TEST",
            request_name=request_name,
            url=url,
            fetched_at_utc="2026-09-14T00:00:00+00:00",
            http_status=200,
            content_type="text/html; charset=utf-8",
            payload_sha256="b" * 64,
            encoding="utf-8",
            html=html,
        )


class ProcurementFailureDiscoveryTests(unittest.TestCase):
    def test_result_index_discovers_failed_package_without_award_url(self):
        relevant_url = (
            "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260908/"
            "f5ef822d-2b05-48e5-b627-9dec404494f0.html"
        )
        irrelevant_url = (
            "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260908/"
            "11111111-1111-1111-1111-111111111111.html"
        )
        list_html = f"""<html><body>
        <a href='{relevant_url}'>
          徐州市水务局2026年度市直管雨、污水管渠维修养护市场化项目中标结果公告采购包2
        </a>
        <a href='{irrelevant_url}'>某医院医疗设备采购中标结果公告采购包1</a>
        </body></html>"""
        failure_html = """<html><head><title>中标结果公告</title></head><body>
        <h1>徐州市水务局2026年度市直管雨、污水管渠维修养护市场化项目中标结果公告采购包2</h1>
        <p>信息发布时间：2026-09-08</p>
        <p>一、项目编号：JSZC-320300-XZTY-G2026-0001</p>
        <p>二、项目名称：2026年度市直管雨、污水管渠维修养护市场化项目</p>
        <p>采购包2 此采购包已作废</p>
        <p>采购人信息</p><p>单位名称：徐州市水务局</p>
        </body></html>"""
        client = UrlAwareFakeHtmlClient(
            {
                XZ_PROCUREMENT_RESULT_LIST: list_html,
                relevant_url: failure_html,
            }
        )
        result = XuzhouProcurementFailureAdapter(client=client).collect_from_result_payloads(
            [],
            discover_pages=1,
            max_discovered_items=10,
        )

        self.assertEqual(result["known_result_url_count"], 0)
        self.assertEqual(result["discovered_result_url_count"], 1)
        self.assertEqual(result["result_url_count"], 1)
        self.assertEqual(result["failed_package_count"], 1)
        self.assertEqual(result["failures"][0]["package_name"], "采购包2")
        self.assertEqual(
            result["failures"][0]["candidate_source"],
            "RESULT_INDEX_DISCOVERY",
        )
        self.assertEqual(result["result_index_discovery"]["raw_item_count"], 2)
        self.assertNotIn(
            (irrelevant_url, "xz_ggzy.procurement_failures.detail"),
            client.urls,
        )

    def test_known_and_discovered_urls_are_deduplicated_before_detail_fetch(self):
        relevant_url = (
            "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260908/"
            "f5ef822d-2b05-48e5-b627-9dec404494f0.html"
        )
        list_html = f"""<html><body>
        <a href='{relevant_url}'>
          徐州市水务局2026年度市直管雨、污水管渠维修养护市场化项目中标结果公告采购包2
        </a>
        </body></html>"""
        failure_html = """<html><body>
        <p>信息发布时间：2026-09-08</p>
        <p>项目编号：JSZC-320300-XZTY-G2026-0001</p>
        <p>项目名称：2026年度市直管雨、污水管渠维修养护市场化项目</p>
        <p>采购包2 此采购包已作废</p>
        <p>采购人信息 单位名称：徐州市水务局</p>
        </body></html>"""
        client = UrlAwareFakeHtmlClient(
            {
                XZ_PROCUREMENT_RESULT_LIST: list_html,
                relevant_url: failure_html,
            }
        )
        payloads = [{"awards": [{"url": relevant_url, "title": "已知结果入口"}]}]
        result = XuzhouProcurementFailureAdapter(client=client).collect_from_result_payloads(
            payloads,
            discover_pages=1,
            max_discovered_items=10,
        )

        self.assertEqual(result["known_result_url_count"], 1)
        self.assertEqual(result["discovered_result_url_count"], 0)
        self.assertEqual(result["result_url_count"], 1)
        detail_fetches = [
            item for item in client.urls if item[1] == "xz_ggzy.procurement_failures.detail"
        ]
        self.assertEqual(len(detail_fetches), 1)

    def test_discovery_limits_fail_closed(self):
        adapter = XuzhouProcurementFailureAdapter(client=UrlAwareFakeHtmlClient({}))
        with self.assertRaises(ValueError):
            adapter.collect_from_result_payloads([], discover_pages=-1)
        with self.assertRaises(ValueError):
            adapter.collect_from_result_payloads([], discover_pages=21)
        with self.assertRaises(ValueError):
            adapter.collect_from_result_payloads([], max_discovered_items=0)


if __name__ == "__main__":
    unittest.main()
