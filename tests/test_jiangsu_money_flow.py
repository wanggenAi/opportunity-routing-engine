import unittest

from src.html_ingest import HtmlFetchEnvelope, html_to_document
from src.jiangsu_money_flow import (
    JiangsuMoneyFlowAdapter,
    discover_latest_economic_release,
    extract_jiangsu_money_flow_metrics,
)
from src.regional_adapters import OfficialDocument


class FakeHtmlClient:
    def __init__(self, html_by_name):
        self.html_by_name = html_by_name

    def fetch(self, url, *, request_name, params=None, headers=None):
        return HtmlFetchEnvelope(
            source_id="JS_STATS",
            request_name=request_name,
            url=url,
            fetched_at_utc="2026-09-11T00:00:00+00:00",
            http_status=200,
            content_type="text/html; charset=utf-8",
            payload_sha256=("a" if "index" in request_name else "b") * 64,
            encoding="utf-8",
            html=self.html_by_name[request_name],
        )


def _release_html():
    return """<html><head><title>江苏省统计局 数据发布</title></head><body>
    <h1>1—7月全省经济运行简况</h1>
    <p>2026-08-24 18:00 来源：国民经济综合统计处</p>
    <p>一、工业。1—7月，全省规模以上工业增加值同比增长6.6%。</p>
    <p>二、服务业。1—6月，全省规模以上服务业营业收入同比增长7.6%。</p>
    <p>三、固定资产投资。1—7月，全省固定资产投资同比下降9.5%。从主要领域看，制造业投资下降0.1%，基础设施投资下降6.8%，房地产开发投资下降23.9%；设备购置投资保持快增，1—7月全省设备工器具购置投资同比增长15.8%。</p>
    <p>四、消费市场。1—7月，全省社会消费品零售总额27744.3亿元，同比增长1.1%。</p>
    <p>五、金融。7月末，全省金融机构人民币存款余额29万亿元，同比增长8%；人民币贷款余额30.3万亿元，同比增长8.7%。</p>
    <p>六、居民消费价格。1—7月，全省居民消费价格同比上涨1.1%。</p>
    </body></html>"""


class JiangsuMoneyFlowTests(unittest.TestCase):
    def test_discovery_uses_data_release_column_and_newest_url_date(self):
        html = """<html><body>
        <a href='/art/2026/7/22/art_85275_11810001.html'>上半年全省经济运行总体平稳、稳中有进</a>
        <a href='/art/2026/8/24/art_85275_11819992.html'>1—7月全省经济运行简况</a>
        <a href='/art/2026/9/10/art_85272_11829999.html'>全省经济运行新闻解读</a>
        <a href='https://evil.example/art/2099/1/1/art_85275_999.html'>1—12月全省经济运行简况</a>
        </body></html>"""
        doc = html_to_document(html, base_url="https://tj.jiangsu.gov.cn/")
        result = discover_latest_economic_release(doc)
        self.assertEqual(result["publication_date_from_url"], "2026-08-24")
        self.assertEqual(result["title"], "1—7月全省经济运行简况")

    def test_discovery_fails_closed_without_matching_official_release(self):
        doc = {
            "links": [
                {
                    "text": "1—7月全省经济运行简况",
                    "url": "https://tj.jiangsu.gov.cn/art/2026/8/24/art_99999_1.html",
                }
            ]
        }
        with self.assertRaises(ValueError):
            discover_latest_economic_release(doc)

    def test_extracts_levels_and_signed_investment_growth(self):
        document = OfficialDocument(
            source_id="JS_STATS",
            title="1—7月全省经济运行简况",
            url="https://tj.jiangsu.gov.cn/art/2026/8/24/art_85275_11819992.html",
            publication_date="2026-08-24",
            text=html_to_document(
                _release_html(),
                base_url="https://tj.jiangsu.gov.cn/art/2026/8/24/art_85275_11819992.html",
            )["text"],
            provenance={"payload_sha256": "b" * 64},
        )
        metrics = {
            item["signal_id"]: item
            for item in extract_jiangsu_money_flow_metrics(document)
        }
        self.assertEqual(metrics["JS_FIXED_INVESTMENT_YOY"]["value"], "-9.5")
        self.assertEqual(metrics["JS_MANUFACTURING_INVESTMENT_YOY"]["value"], "-0.1")
        self.assertEqual(metrics["JS_INFRASTRUCTURE_INVESTMENT_YOY"]["value"], "-6.8")
        self.assertEqual(metrics["JS_REAL_ESTATE_INVESTMENT_YOY"]["value"], "-23.9")
        self.assertEqual(metrics["JS_EQUIPMENT_INVESTMENT_YOY"]["value"], "15.8")
        self.assertEqual(metrics["JS_RETAIL_LEVEL_100M_CNY"]["value"], "27744.3")
        self.assertEqual(metrics["JS_RETAIL_YOY"]["value"], "1.1")
        self.assertEqual(metrics["JS_RMB_DEPOSIT_LEVEL_TRILLION_CNY"]["value"], "29")
        self.assertEqual(metrics["JS_RMB_DEPOSIT_YOY"]["value"], "8")
        self.assertEqual(metrics["JS_RMB_LOAN_LEVEL_TRILLION_CNY"]["value"], "30.3")
        self.assertEqual(metrics["JS_RMB_LOAN_YOY"]["value"], "8.7")

    def test_collect_preserves_index_and_release_provenance(self):
        index_html = """<html><body>
        <a href='/art/2026/8/24/art_85275_11819992.html'>1—7月全省经济运行简况</a>
        </body></html>"""
        adapter = JiangsuMoneyFlowAdapter(
            client=FakeHtmlClient(
                {
                    "js_stats.money_flow.index": index_html,
                    "js_stats.release": _release_html(),
                }
            )
        )
        payload = adapter.collect()
        self.assertTrue(payload["data_available"])
        self.assertEqual(payload["observation_period"], "2026-01..2026-07")
        self.assertEqual(payload["publication_date"], "2026-08-24")
        self.assertEqual(payload["provenance"]["index"]["payload_sha256"], "a" * 64)
        self.assertEqual(payload["provenance"]["release"]["payload_sha256"], "b" * 64)
        self.assertGreaterEqual(payload["metric_count"], 10)

    def test_collect_rejects_release_date_identity_conflict(self):
        index_html = """<html><body>
        <a href='/art/2026/8/24/art_85275_11819992.html'>1—7月全省经济运行简况</a>
        </body></html>"""
        bad_release = _release_html().replace("2026-08-24", "2026-08-23")
        adapter = JiangsuMoneyFlowAdapter(
            client=FakeHtmlClient(
                {
                    "js_stats.money_flow.index": index_html,
                    "js_stats.release": bad_release,
                }
            )
        )
        with self.assertRaisesRegex(ValueError, "publication date conflicts"):
            adapter.collect()


if __name__ == "__main__":
    unittest.main()
