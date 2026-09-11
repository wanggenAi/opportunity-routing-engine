import unittest

from src.html_ingest import HtmlFetchEnvelope
from src.regional_adapters import JiangsuStatsReleaseAdapter, XuzhouProcurementAdapter


class FakeHtmlClient:
    def __init__(self, html_by_name):
        self.html_by_name = html_by_name

    def fetch(self, url, *, request_name, params=None, headers=None):
        html = self.html_by_name[request_name]
        return HtmlFetchEnvelope(
            source_id="TEST",
            request_name=request_name,
            url=url,
            fetched_at_utc="2026-09-11T00:00:00+00:00",
            http_status=200,
            content_type="text/html; charset=utf-8",
            payload_sha256="b" * 64,
            encoding="utf-8",
            html=html,
        )


class JiangsuStatsTests(unittest.TestCase):
    def test_release_and_metrics(self):
        html = """<html><head><title>江苏省统计局</title></head><body>
        <h1>1—7月全省经济运行简况</h1>
        <p>2026-08-24 来源：国民经济综合统计处</p>
        <p>1—7月，全省规模以上工业增加值同比增长6.6%。</p>
        <p>1—6月，全省规模以上服务业营业收入同比增长7.6%。</p>
        <p>1—7月，全省固定资产投资同比下降9.5%。</p>
        <p>设备工器具购置投资同比增长15.8%。</p>
        </body></html>"""
        adapter = JiangsuStatsReleaseAdapter(
            client=FakeHtmlClient({"js_stats.release": html})
        )
        doc = adapter.fetch_release(
            "https://tj.jiangsu.gov.cn/art/2026/8/24/art_85275_11819992.html"
        )
        self.assertEqual(doc.publication_date, "2026-08-24")
        metrics = {m["signal_id"]: m for m in adapter.extract_money_flow_metrics(doc)}
        self.assertEqual(metrics["JS_INDUSTRIAL_VALUE_ADDED_YOY"]["value"], "6.6")
        self.assertEqual(metrics["JS_FIXED_INVESTMENT_YOY"]["value"], "-9.5")
        self.assertEqual(metrics["JS_EQUIPMENT_INVESTMENT_YOY"]["value"], "15.8")


class XuzhouProcurementTests(unittest.TestCase):
    def test_discovery_and_event_parse(self):
        list_html = """<html><body>
        <a href='/jyxx/003004/003004002/20260910/df0173c0-fd99-415a-83e4-955628ce0be4.html'>[新]草莓大棚提档升级改造项目采购公告</a>
        </body></html>"""
        detail_html = """<html><head><title>采购公告</title></head><body>
        <h1>2026年贾汪区现代农业产业园区草莓大棚提档升级改造项目采购公告</h1>
        <p>信息发布时间：2026-09-10</p>
        <p>项目编号：JSZC-320305-ZLBJ-C2026-0001</p>
        <p>项目名称：草莓大棚提档升级改造项目</p>
        <p>采购方式：竞争性磋商</p>
        <p>预算金额：379.608908万元</p>
        <p>合同履行期限：60日历天</p>
        <p>本项目（是/否）接受联合体：否</p>
        <p>响应文件提交 截止时间：2026-09-21 10:00</p>
        </body></html>"""
        client = FakeHtmlClient(
            {
                "xz_ggzy.procurement.list": list_html,
                "xz_ggzy.procurement.detail": detail_html,
            }
        )
        adapter = XuzhouProcurementAdapter(client=client)
        discovery = adapter.discover_recent(limit=5)
        self.assertEqual(discovery["item_count"], 1)
        self.assertEqual(discovery["items"][0]["publication_date"], "2026-09-10")
        event = adapter.fetch_event(discovery["items"][0]["url"])
        self.assertEqual(event.project_id, "JSZC-320305-ZLBJ-C2026-0001")
        self.assertEqual(event.procurement_method, "竞争性磋商")
        self.assertEqual(event.budget_rmb, "3796089.08")
        self.assertEqual(event.contract_term, "60日历天")

    def test_structured_titled_spans_restore_identity_when_visible_text_is_unavailable(self):
        detail_html = """<html><head><title>采购公告</title></head><body>
        <script type='text/html'>
          <span class='outer'>
            <span title='项目名称'>2026年度市直管雨、污水管渠维修养护市场化项目</span>
            <span title='项目编号'>JSZC-320300-XZTY-G2026-0004</span>
          </span>
          <span class='outer'><span title='采购方式'>公开招标</span></span>
          <span class='outer'>预算金额：<span title='预算金额'>328.300000万元</span></span>
          <span title='投标文件接收截止时间'>2026-10-08 09:30</span>
          <span class='outer'><span title='合同履行期限'>一年</span></span>
        </script>
        </body></html>"""
        adapter = XuzhouProcurementAdapter(
            client=FakeHtmlClient({"xz_ggzy.procurement.detail": detail_html})
        )
        event = adapter.fetch_event(
            "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004002/20260910/fa34bda1-6f69-4512-b5dc-731bf34418ef.html",
            fallback_title="徐州市水务局2026年度市直管雨、污水管渠维修养护市场化项目公开招标公告",
        )
        self.assertEqual(event.project_id, "JSZC-320300-XZTY-G2026-0004")
        self.assertEqual(event.project_name, "2026年度市直管雨、污水管渠维修养护市场化项目")
        self.assertEqual(event.procurement_method, "公开招标")
        self.assertEqual(event.budget_rmb, "3283000.00")
        self.assertEqual(event.budget_raw, "预算金额：328.300000万元")
        self.assertEqual(event.deadline, "2026-10-08 09:30")
        self.assertEqual(event.contract_term, "一年")

    def test_conflicting_structured_identity_fails_closed(self):
        detail_html = """<html><body><script type='text/html'>
          <span title='项目编号'>PROJECT-A</span>
          <span title='项目编号'>PROJECT-B</span>
        </script></body></html>"""
        adapter = XuzhouProcurementAdapter(
            client=FakeHtmlClient({"xz_ggzy.procurement.detail": detail_html})
        )
        event = adapter.fetch_event(
            "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004002/20260910/fa34bda1-6f69-4512-b5dc-731bf34418ef.html",
            fallback_title="采购公告",
        )
        self.assertIsNone(event.project_id)


if __name__ == "__main__":
    unittest.main()
