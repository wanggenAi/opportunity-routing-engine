import unittest

from src.html_ingest import HtmlFetchEnvelope
from src.live_imbalance_ledger import classify_procurement_event
from src.xuzhou_procurement_results import XuzhouProcurementResultAdapter


class FakeHtmlClient:
    def __init__(self, html_by_name):
        self.html_by_name = html_by_name

    def fetch(self, url, *, request_name, params=None, headers=None):
        return HtmlFetchEnvelope(
            source_id="TEST",
            request_name=request_name,
            url=url,
            fetched_at_utc="2026-09-11T00:00:00+00:00",
            http_status=200,
            content_type="text/html; charset=utf-8",
            payload_sha256="f" * 64,
            encoding="utf-8",
            html=self.html_by_name[request_name],
        )


class UrlAwareFakeHtmlClient:
    def __init__(self, html_by_url, detail_html):
        self.html_by_url = html_by_url
        self.detail_html = detail_html
        self.urls = []

    def fetch(self, url, *, request_name, params=None, headers=None):
        self.urls.append(url)
        if request_name == "xz_ggzy.procurement_results.detail":
            html = self.detail_html
        else:
            html = self.html_by_url.get(url, "<html><body></body></html>")
        return HtmlFetchEnvelope(
            source_id="TEST",
            request_name=request_name,
            url=url,
            fetched_at_utc="2026-09-11T00:00:00+00:00",
            http_status=200,
            content_type="text/html; charset=utf-8",
            payload_sha256="e" * 64,
            encoding="utf-8",
            html=html,
        )


class XuzhouProcurementResultTests(unittest.TestCase):
    def _list_html(self):
        return """<html><body>
        <a href='/jyxx/003004/003004006/20260909/5acf2119-a427-4fd4-bb0b-8e947e811c93.html'>
        [新]徐州市水务局2026年度市管雨污水泵站设施维修养护市场化中标结果公告采购包2
        </a>
        </body></html>"""

    def _detail_html(self):
        return """<html><head><title>中标结果公告</title></head><body>
        <h1>徐州市水务局2026年度市管雨污水泵站设施维修养护市场化中标结果公告采购包2</h1>
        <p>信息发布时间：2026-09-09</p>
        <p>一、项目编号：JSZC-320300-XZTY-G2026-0002</p>
        <p>二、项目名称：2026年度市管雨污水泵站设施维修养护市场化、市直管截污闸门维修养护</p>
        <h2>三、中标（成交）信息</h2>
        <p>采购包2</p>
        <table>
          <tr><th>序号</th><th>供应商名称</th><th>社会信用代码</th><th>供应商地址</th><th>评审总得分</th><th>中标/成交金额</th></tr>
          <tr><td>1</td><td>江苏山祥建设工程有限公司</td><td>91320312302101990G</td><td>徐州高新技术产业开发区珠江东路11号</td><td>81.84</td><td>1186000元</td></tr>
        </table>
        <h2>四、主要标的信息</h2>
        <p>服务类</p><p>名称：2026年度市管雨污水泵站设施维修养护市场化采购包2</p>
        <h2>九、凡对本次公告内容提出询问，请按以下方式联系。</h2>
        <p>1.采购人信息</p>
        <p>单位名称：徐州市水务局</p>
        </body></html>"""

    def test_discovers_result_page_and_extracts_proven_supplier(self):
        adapter = XuzhouProcurementResultAdapter(
            client=FakeHtmlClient(
                {
                    "xz_ggzy.procurement_results.list": self._list_html(),
                    "xz_ggzy.procurement_results.detail": self._detail_html(),
                }
            )
        )
        discovery = adapter.discover_recent(limit=5)
        self.assertEqual(discovery["item_count"], 1)
        self.assertEqual(discovery["items"][0]["publication_date"], "2026-09-09")
        awards = adapter.fetch_awards(
            discovery["items"][0]["url"],
            fallback_title=discovery["items"][0]["title"],
        )
        self.assertEqual(len(awards), 1)
        award = awards[0]
        self.assertEqual(award.supplier_name, "江苏山祥建设工程有限公司")
        self.assertEqual(award.supplier_credit_code, "91320312302101990G")
        self.assertEqual(award.award_amount_rmb, "1186000.00")
        self.assertEqual(award.project_id, "JSZC-320300-XZTY-G2026-0002")
        self.assertEqual(award.buyer_actor, "徐州市水务局")
        self.assertEqual(award.package_name, "采购包2")

    def test_structured_metadata_restores_result_project_identity(self):
        detail = """<html><head><title>中标结果公告</title></head><body>
        <script type='text/html'>
          <span class='outer'>
            <span title='项目名称'>2026年度市管雨污水泵站设施维修养护市场化、市直管截污闸门维修养护</span>
            <span title='项目编号'>JSZC-320300-XZTY-G2026-0002</span>
          </span>
          <span class='outer'><span title='采购人单位名称'>徐州市水务局</span></span>
        </script>
        <p>采购包2</p>
        <table>
          <tr><th>序号</th><th>供应商名称</th><th>社会信用代码</th><th>供应商地址</th><th>中标/成交金额</th></tr>
          <tr><td>1</td><td>江苏山祥建设工程有限公司</td><td>91320312302101990G</td><td>徐州市</td><td>1186000元</td></tr>
        </table>
        </body></html>"""
        adapter = XuzhouProcurementResultAdapter(
            client=FakeHtmlClient({"xz_ggzy.procurement_results.detail": detail})
        )
        awards = adapter.fetch_awards(
            "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260909/5acf2119-a427-4fd4-bb0b-8e947e811c93.html",
            fallback_title="徐州市水务局2026年度市管雨污水泵站设施维修养护市场化中标结果公告采购包2",
        )
        self.assertEqual(len(awards), 1)
        award = awards[0]
        self.assertEqual(award.project_id, "JSZC-320300-XZTY-G2026-0002")
        self.assertEqual(
            award.project_name,
            "2026年度市管雨污水泵站设施维修养护市场化、市直管截污闸门维修养护",
        )
        self.assertEqual(award.buyer_actor, "徐州市水务局")
        self.assertEqual(award.supplier_name, "江苏山祥建设工程有限公司")
        self.assertEqual(award.award_amount_rmb, "1186000.00")

    def test_package_specific_url_rejects_other_package_supplier_rows(self):
        detail = """<html><head><title>结果公告</title></head><body>
        <h1>徐州市水务局2026年度市直管雨、污水管渠维修养护市场化项目中标结果公告采购包1</h1>
        <p>信息发布时间：2026-09-08</p>
        <p>采购包1</p>
        <table>
          <tr><th>序号</th><th>供应商名称</th><th>社会信用代码</th><th>供应商地址</th><th>中标/成交金额</th></tr>
          <tr><td>1</td><td>徐州城建排水有限公司</td><td>913203007500392629</td><td>徐州市</td><td>9297658元</td></tr>
        </table>
        <p>采购包3</p>
        <table>
          <tr><th>序号</th><th>供应商名称</th><th>社会信用代码</th><th>供应商地址</th><th>中标/成交金额</th></tr>
          <tr><td>1</td><td>上海启呈信息科技有限公司</td><td>91310116MA1J93N0X1</td><td>上海市</td><td>973000元</td></tr>
        </table>
        </body></html>"""
        adapter = XuzhouProcurementResultAdapter(
            client=FakeHtmlClient({"xz_ggzy.procurement_results.detail": detail})
        )
        awards = adapter.fetch_awards(
            "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260908/72ac9497-8358-4333-a585-faf0c5ae26a2.html"
        )
        self.assertEqual(len(awards), 1)
        self.assertEqual(awards[0].package_name, "采购包1")
        self.assertEqual(awards[0].supplier_name, "徐州城建排水有限公司")
        self.assertNotEqual(awards[0].supplier_name, "上海启呈信息科技有限公司")

    def test_package_specific_page_can_bind_an_unlabeled_single_table(self):
        detail = """<html><body>
        <h1>某维修项目中标结果公告采购包1</h1>
        <table>
          <tr><th>供应商名称</th><th>社会信用代码</th><th>金额</th></tr>
          <tr><td>某供应商</td><td>91320312302101990G</td><td>10000元</td></tr>
        </table>
        </body></html>"""
        adapter = XuzhouProcurementResultAdapter(
            client=FakeHtmlClient({"xz_ggzy.procurement_results.detail": detail})
        )
        awards = adapter.fetch_awards(
            "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260909/11111111-1111-1111-1111-111111111111.html"
        )
        self.assertEqual(len(awards), 1)
        self.assertEqual(awards[0].package_name, "采购包1")
        self.assertEqual(awards[0].supplier_name, "某供应商")

    def test_failed_package_without_supplier_row_is_not_provider_evidence(self):
        detail = """<html><body>
        <h1>某项目中标结果公告采购包1</h1>
        <p>信息发布时间：2026-09-09</p>
        <p>一、项目编号：P-VOID</p>
        <p>二、项目名称：某项目</p>
        <p>采购包1 此采购包已作废</p>
        </body></html>"""
        adapter = XuzhouProcurementResultAdapter(
            client=FakeHtmlClient({"xz_ggzy.procurement_results.detail": detail})
        )
        awards = adapter.fetch_awards(
            "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260909/00d7b76b-b26d-47f1-bc2e-00c7a8f7cb0d.html"
        )
        self.assertEqual(awards, [])

    def test_history_scans_numbered_pages_and_filters_before_detail_fetch(self):
        base = "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/list.html"
        irrelevant = """<html><body>
        <a href='/jyxx/003004/003004006/20260911/11111111-1111-1111-1111-111111111111.html'>
        某医院血液透析设备中标结果公告采购包1
        </a></body></html>"""
        matching = self._list_html()
        client = UrlAwareFakeHtmlClient(
            {
                base: irrelevant,
                "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/2.html": matching,
                "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/3.html": "<html><body></body></html>",
            },
            self._detail_html(),
        )
        adapter = XuzhouProcurementResultAdapter(client=client)
        payload = adapter.collect_history_awards(
            pages=5,
            item_filter=lambda item: classify_procurement_event(item).capability_key is not None,
            max_items=10,
            max_details=10,
        )
        self.assertEqual(payload["discovery"]["scanned_pages"], 3)
        self.assertEqual(payload["discovery"]["raw_item_count"], 2)
        self.assertEqual(payload["discovery"]["item_count"], 1)
        self.assertEqual(payload["detail_fetch_count"], 1)
        self.assertEqual(payload["award_count"], 1)
        self.assertTrue(any(url.endswith("/2.html") for url in client.urls))
        detail_urls = [url for url in client.urls if "/20260909/" in url]
        self.assertEqual(len(detail_urls), 1)

    def test_history_limits_are_fail_closed(self):
        adapter = XuzhouProcurementResultAdapter(client=FakeHtmlClient({}))
        with self.assertRaises(ValueError):
            adapter.discover_history(pages=0)
        with self.assertRaises(ValueError):
            adapter.discover_history(pages=51)
        with self.assertRaises(ValueError):
            adapter.discover_history(max_items=0)


if __name__ == "__main__":
    unittest.main()
