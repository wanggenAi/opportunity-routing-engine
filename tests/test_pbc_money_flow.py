import unittest
from datetime import date

from src.pbc_money_flow import (
    _freshness,
    discover_latest_financial_report,
    parse_financial_report,
)


class PbcMoneyFlowTests(unittest.TestCase):
    def test_discovers_first_financial_report_from_official_index_order(self):
        doc = {
            "links": [
                {"text": "2026年上半年地区社会融资规模增量统计表", "url": "https://www.pbc.gov.cn/a"},
                {"text": "2026年上半年金融统计数据报告", "url": "https://www.pbc.gov.cn/b"},
                {"text": "2026年5月金融统计数据报告", "url": "https://www.pbc.gov.cn/c"},
            ]
        }
        result = discover_latest_financial_report(doc)
        self.assertEqual(result["title"], "2026年上半年金融统计数据报告")
        self.assertEqual(result["url"], "https://www.pbc.gov.cn/b")

    def test_rejects_non_pbc_report_link(self):
        doc = {
            "links": [
                {"text": "2026年上半年金融统计数据报告", "url": "https://example.com/report"}
            ]
        }
        with self.assertRaises(ValueError):
            discover_latest_financial_report(doc)

    def test_parses_current_report_without_zero_filling(self):
        text = """
        文章来源： 2026-07-15 15:00:09
        社会融资规模存量同比增长7.4% 初步统计，2026年6月末社会融资规模存量为462.06万亿元，同比增长7.4%。
        上半年社会融资规模增量累计为20.84万亿元。
        广义货币增长8% 6月末，广义货币(M2)余额356.71万亿元,同比增长8%。
        狭义货币(M1)余额118.48万亿元,同比增长4%。
        流通中货币(M0)余额14.74万亿元,同比增长11.8%。
        上半年人民币存款增加17.76万亿元。
        上半年人民币贷款增加10.72万亿元。
        6月份同业拆借月加权平均利率为1.41%，质押式债券回购月加权平均利率为1.43%。
        6月末，国家外汇储备余额3.42万亿美元。6月末，人民币汇率为1美元兑6.8109元人民币。
        """
        parsed = parse_financial_report(
            title="2026年上半年金融统计数据报告",
            text=text,
            source_url="https://www.pbc.gov.cn/report",
        )
        self.assertEqual(parsed["release_date"], "2026-07-15")
        self.assertEqual(parsed["metrics"]["social_financing_stock"]["value"], 462.06)
        self.assertEqual(parsed["metrics"]["social_financing_stock"]["yoy_pct"], 7.4)
        self.assertEqual(parsed["metrics"]["m2_balance"]["yoy_pct"], 8.0)
        self.assertEqual(parsed["metrics"]["usd_cny_reference"]["value"], 6.8109)
        self.assertNotIn("nonexistent_metric", parsed["metrics"])

    def test_parses_full_width_parentheses_and_spacing(self):
        text = """
        文章来源： 2026-07-15 15:00:09
        社会融资规模存量为462.06万亿元，同比增长7.4%。
        社会融资规模增量累计为20.84万亿元。
        广义货币（ M2 ）余额356.71万亿元，同比 增长8%。
        狭义货币（M1）余额118.48万亿元,同比增长4%。
        流通中货币（M0）余额14.74万亿元,同比增长11.8%。
        """.replace("同比 增长", "同比增长")
        parsed = parse_financial_report(
            title="2026年上半年金融统计数据报告",
            text=text,
            source_url="https://www.pbc.gov.cn/report",
        )
        self.assertEqual(parsed["metrics"]["m2_balance"]["value"], 356.71)
        self.assertEqual(parsed["metrics"]["m1_balance"]["value"], 118.48)
        self.assertEqual(parsed["metrics"]["m0_balance"]["value"], 14.74)

    def test_negative_yoy_preserves_sign(self):
        text = """
        文章来源： 2026-07-15 15:00:09
        社会融资规模存量为462.06万亿元，同比增长7.4%。
        社会融资规模增量累计为20.84万亿元。
        广义货币(M2)余额356.71万亿元,同比增长8%。
        狭义货币(M1)余额118.48万亿元,同比下降4%。
        流通中货币(M0)余额14.74万亿元,同比增长11.8%。
        """
        parsed = parse_financial_report(
            title="2026年上半年金融统计数据报告",
            text=text,
            source_url="https://www.pbc.gov.cn/report",
        )
        self.assertEqual(parsed["metrics"]["m1_balance"]["yoy_pct"], -4.0)

    def test_core_metrics_are_required(self):
        with self.assertRaises(ValueError):
            parse_financial_report(
                title="2026年上半年金融统计数据报告",
                text="文章来源： 2026-07-15 15:00:09 广义货币(M2)余额356.71万亿元,同比增长8%。",
                source_url="https://www.pbc.gov.cn/report",
            )

    def test_freshness_states(self):
        self.assertEqual(_freshness("2026-07-15", today=date(2026, 9, 11))["status"], "FRESH")
        self.assertEqual(_freshness("2026-05-01", today=date(2026, 9, 11))["status"], "STALE")
        self.assertEqual(_freshness(None, today=date(2026, 9, 11))["status"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
