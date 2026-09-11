import unittest

from src.html_ingest import HtmlFetchEnvelope
from src.xuzhou_construction_capex import XuzhouConstructionTenderAdapter


class FakeHtmlClient:
    def __init__(self, html_by_name):
        self.html_by_name = html_by_name

    def fetch(self, url, *, request_name, params=None, headers=None):
        return HtmlFetchEnvelope(
            source_id="XZ_GGZY",
            request_name=request_name,
            url=url,
            fetched_at_utc="2026-09-11T00:00:00+00:00",
            http_status=200,
            content_type="text/html; charset=utf-8",
            payload_sha256=("a" if request_name.endswith("list") else "b") * 64,
            encoding="utf-8",
            html=self.html_by_name[request_name],
        )


class XuzhouConstructionCapexTests(unittest.TestCase):
    def test_discovers_only_official_construction_notice_urls(self):
        html = """<html><body>
        <a href='/jyxx/003001/003001001/20260907/94ae268d-66f0-476d-ba60-650a0a1812a8.html'>[新]水务材料采购（三次公告）</a>
        <a href='/jyxx/003004/003004002/20260907/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee.html'>政府采购公告</a>
        <a href='https://evil.example/jyxx/003001/003001001/20990101/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee.html'>未来假公告</a>
        </body></html>"""
        adapter = XuzhouConstructionTenderAdapter(
            client=FakeHtmlClient({"xz_ggzy.construction.list": html})
        )
        result = adapter.discover_recent(limit=10)
        self.assertEqual(result["item_count"], 1)
        self.assertEqual(result["items"][0]["publication_date"], "2026-09-07")
        self.assertEqual(result["items"][0]["title"], "水务材料采购（三次公告）")
        self.assertEqual(result["provenance"]["payload_sha256"], "a" * 64)

    def test_parses_explicit_unit_contract_estimate_and_self_funding(self):
        url = "https://ggzy.zwb.xz.gov.cn/jyxx/003001/003001001/20260907/94ae268d-66f0-476d-ba60-650a0a1812a8.html"
        html = """<html><head><title>水务材料</title></head><body>
        <h1>徐州经济技术开发区水务有限公司材料采购（三次公告）</h1>
        <p>信息发布时间：2026-09-07</p>
        <p>项目业主为 徐州经济技术开发区水务有限公司，招标人为 徐州经济技术开发区水务有限公司，建设资金来自 自筹，项目出资比例为100%。</p>
        <p>2.1.2 合同估算价：246.58万元；</p>
        <p>建设地点：徐州经济技术开发区工程项目现场指定位置。</p>
        </body></html>"""
        adapter = XuzhouConstructionTenderAdapter(
            client=FakeHtmlClient({"xz_ggzy.construction.detail": html})
        )
        event = adapter.fetch_event(url, fallback_title="水务材料采购（三次公告）")
        self.assertEqual(event.contract_estimate_rmb, "2465800.00")
        self.assertEqual(event.estimate_basis, "EXPLICIT_UNIT")
        self.assertEqual(event.funding_source, "自筹")
        self.assertEqual(event.project_owner, "徐州经济技术开发区水务有限公司")
        self.assertEqual(event.tenderer, "徐州经济技术开发区水务有限公司")
        self.assertTrue(event.is_reissue)
        self.assertEqual(event.evidence_state, "AMOUNT_AND_FUNDING_SOURCE")

    def test_parses_header_unit_wan_contract_estimate_and_fiscal_funding(self):
        url = "https://ggzy.zwb.xz.gov.cn/jyxx/003001/003001001/20260904/1490c31c-5883-40a3-821e-64790db32f72.html"
        html = """<html><head><title>危旧房改造</title></head><body>
        <h1>徐州市泉山区C级危旧房改造工程</h1>
        <p>信息发布时间：2026-09-04</p>
        <p>项目业主为徐州市泉山区人民政府段庄街道办事处，招标人为徐州市泉山区人民政府段庄街道办事处，建设资金来自区级财政统筹，已落实。</p>
        <p>2.2 建设地点：徐州市泉山区永安、段庄、和平、奎山街道。</p>
        <p>2.6 工程合同估算价（万元）：约10810.72</p>
        </body></html>"""
        adapter = XuzhouConstructionTenderAdapter(
            client=FakeHtmlClient({"xz_ggzy.construction.detail": html})
        )
        event = adapter.fetch_event(url, fallback_title="徐州市泉山区C级危旧房改造工程")
        self.assertEqual(event.contract_estimate_rmb, "108107200.00")
        self.assertEqual(event.estimate_basis, "HEADER_UNIT_WAN_CNY")
        self.assertEqual(event.funding_source, "区级财政统筹")
        self.assertEqual(event.location, "徐州市泉山区永安、段庄、和平、奎山街道")
        self.assertFalse(event.is_reissue)

    def test_project_total_is_not_substituted_for_tender_contract_estimate(self):
        url = "https://ggzy.zwb.xz.gov.cn/jyxx/003001/003001001/20260824/d7f9a5e4-2835-4efa-a7da-f31e5b1f0ff8.html"
        html = """<html><body>
        <p>信息发布时间：2026-08-24</p>
        <p>项目业主为某中心，招标人为某中心，建设资金来自财政资金，已落实。</p>
        <p>项目总投资约2200万元，勘察设计费约55.98万元。</p>
        </body></html>"""
        adapter = XuzhouConstructionTenderAdapter(
            client=FakeHtmlClient({"xz_ggzy.construction.detail": html})
        )
        event = adapter.fetch_event(url, fallback_title="某道路工程勘察设计")
        self.assertIsNone(event.contract_estimate_rmb)
        self.assertIsNone(event.contract_estimate_raw)
        self.assertIsNone(event.estimate_basis)
        self.assertEqual(event.evidence_state, "FUNDING_SOURCE_ONLY")

    def test_publication_date_conflict_fails_closed(self):
        url = "https://ggzy.zwb.xz.gov.cn/jyxx/003001/003001001/20260904/1490c31c-5883-40a3-821e-64790db32f72.html"
        html = "<html><body><p>信息发布时间：2026-09-03</p></body></html>"
        adapter = XuzhouConstructionTenderAdapter(
            client=FakeHtmlClient({"xz_ggzy.construction.detail": html})
        )
        with self.assertRaisesRegex(ValueError, "publication date conflicts"):
            adapter.fetch_event(url, fallback_title="date drift")

    def test_batch_keeps_per_item_errors_without_erasing_valid_events(self):
        list_html = """<html><body>
        <a href='/jyxx/003001/003001001/20260904/1490c31c-5883-40a3-821e-64790db32f72.html'>危旧房改造工程</a>
        </body></html>"""
        detail_html = """<html><body>
        <p>信息发布时间：2026-09-04</p>
        <p>建设资金来自区级财政统筹，已落实。</p>
        <p>工程合同估算价（万元）：约10810.72</p>
        </body></html>"""
        adapter = XuzhouConstructionTenderAdapter(
            client=FakeHtmlClient(
                {
                    "xz_ggzy.construction.list": list_html,
                    "xz_ggzy.construction.detail": detail_html,
                }
            )
        )
        payload = adapter.collect_recent_events(limit=5)
        self.assertEqual(payload["event_count"], 1)
        self.assertEqual(payload["error_count"], 0)
        self.assertEqual(payload["amount_evidence_count"], 1)
        self.assertIn("NO_SUM_WITHOUT_PROJECT_DEDUP", payload["aggregation_policy"])


if __name__ == "__main__":
    unittest.main()
