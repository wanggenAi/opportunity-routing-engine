import unittest

from src.gacc_trade_corroboration import JiangsuTradeCorroborator


GOOD_HTML = """
<html><head><title>前7个月我省外贸进出口同比增长26.2%</title></head><body>
<p>据南京海关统计，今年前7个月，江苏省外贸进出口4.18万亿元，较去年同期增长26.2%。其中，出口2.71万亿元，增长22.6%；进口1.47万亿元，增长33.5%。</p>
<p>7月份，我省外贸进出口6910.4亿元，增长39.7%。其中，出口4408.8亿元，增长35.3%；进口2501.6亿元，增长48.2%。</p>
</body></html>
"""


class FakeEnvelope:
    def __init__(self, html):
        self.url = "https://jszwb.jiangsu.gov.cn/art/2026/8/14/art_71797_11816221.html"
        self.html = html

    def metadata(self):
        return {
            "source_id": "JS_GOV",
            "request_name": "fake",
            "url": self.url,
            "http_status": 200,
            "content_type": "text/html; charset=utf-8",
            "payload_sha256": "b" * 64,
        }


class FakeClient:
    def __init__(self, html=GOOD_HTML):
        self.html = html
        self.calls = 0

    def fetch(self, url, *, request_name, params=None, headers=None):
        self.calls += 1
        return FakeEnvelope(self.html)


class JiangsuTradeCorroborationTests(unittest.TestCase):
    def test_same_period_is_identity_direction_corroborated(self):
        client = FakeClient()
        result = JiangsuTradeCorroborator(client=client).corroborate({
            "period": "2026-07",
            "corroboration_required": True,
            "corroboration_status": "PENDING",
        })
        self.assertEqual(client.calls, 1)
        self.assertEqual(result["corroboration_status"], "PERIOD_IDENTITY_DIRECTION_CORROBORATED")
        self.assertEqual(result["corroboration"]["basis"], "PERIOD_IDENTITY_DIRECTION_ONLY")
        self.assertEqual(result["corroboration"]["monetary_value_comparison"], "UNAVAILABLE_CROSS_CURRENCY")
        self.assertEqual(result["corroboration"]["reported_ytd"]["total_trillion_cny"], 4.18)
        self.assertEqual(result["corroboration"]["reported_month"]["total_100m_cny"], 6910.4)

    def test_other_period_stays_pending_without_reusing_stale_corroboration(self):
        client = FakeClient()
        result = JiangsuTradeCorroborator(client=client).corroborate({"period": "2026-08"})
        self.assertEqual(client.calls, 0)
        self.assertEqual(result["corroboration_status"], "PENDING")
        self.assertEqual(result["corroboration"]["status"], "NO_SAME_PERIOD_HTTPS_CORROBORATION")

    def test_missing_nanjing_customs_attribution_fails_closed(self):
        client = FakeClient(GOOD_HTML.replace("据南京海关统计", "据公开信息"))
        with self.assertRaisesRegex(ValueError, "identity drift"):
            JiangsuTradeCorroborator(client=client).corroborate({"period": "2026-07"})

    def test_inconsistent_official_figures_fail_closed(self):
        client = FakeClient(GOOD_HTML.replace("进口1.47万亿元", "进口1.00万亿元"))
        with self.assertRaisesRegex(ValueError, "YTD trade arithmetic"):
            JiangsuTradeCorroborator(client=client).corroborate({"period": "2026-07"})


if __name__ == "__main__":
    unittest.main()
