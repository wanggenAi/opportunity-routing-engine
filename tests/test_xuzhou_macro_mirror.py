import unittest

from src.xuzhou_macro_mirror import (
    _is_economic_candidate,
    extract_xuzhou_macro_metrics,
)


class XuzhouMacroMirrorTests(unittest.TestCase):
    def test_candidate_requires_xuzhou_and_economic_marker(self):
        self.assertTrue(_is_economic_candidate("徐州GDP达4846.9亿元 经济运行稳进提质"))
        self.assertTrue(_is_economic_candidate("徐州经济运行总体平稳"))
        self.assertFalse(_is_economic_candidate("南京经济运行稳中有进"))
        self.assertFalse(_is_economic_candidate("徐州推进养老服务体系建设"))

    def test_extracts_explicit_h1_metrics_without_inventing_investment_growth(self):
        text = """
        2026年1—6月，徐州实现地区生产总值4846.9亿元，同比增长5.2%。
        第一产业增加值同比增长2.5%，第二产业增加值同比增长3.9%，第三产业增加值同比增长6.3%，
        三次产业结构比例优化为6.9:33.9:59.2。
        全市全体居民人均可支配收入同比增长5.4%，其中城镇居民人均可支配收入同比增长4.5%，
        农村居民人均可支配收入同比增长6.8%。居民消费价格指数CPI温和上涨2.2%。
        全市规模以上工业增加值同比增长6.1%。规模以上服务业营业收入同比增长5.4%。
        全市社会消费品零售总额同比增长4.4%。
        全市固定资产投资降幅较1—5月收窄3.1个百分点。
        信息传输、软件和信息技术服务业增加值同比增长15.2%，
        租赁和商务服务业增加值同比增长15.1%，金融业增加值同比增长10.8%。
        全市线上单位通过公共网络实现商品零售额同比增长13.0%。
        """
        metrics = extract_xuzhou_macro_metrics(
            text=text,
            source_url="https://www.jiangsu.gov.cn/art/2026/7/31/art_33718_11812411.html",
            publication_date="2026-07-31",
        )
        by_id = {item["signal_id"]: item for item in metrics}
        self.assertEqual(by_id["XZ_GDP"]["value"], "4846.9")
        self.assertEqual(by_id["XZ_GDP_YOY"]["value"], "5.2")
        self.assertEqual(by_id["XZ_INDUSTRIAL_VALUE_ADDED_YOY"]["value"], "6.1")
        self.assertEqual(by_id["XZ_RETAIL_YOY"]["value"], "4.4")
        self.assertEqual(by_id["XZ_INFO_SOFTWARE_YOY"]["value"], "15.2")
        self.assertEqual(by_id["XZ_FIXED_INVESTMENT_DECLINE_NARROWING"]["value"], "3.1")
        self.assertEqual(by_id["XZ_PRIMARY_SHARE"]["value"], "6.9")
        self.assertNotIn("XZ_FIXED_INVESTMENT_YOY", by_id)

    def test_decline_keeps_negative_sign(self):
        metrics = extract_xuzhou_macro_metrics(
            text=(
                "徐州实现地区生产总值4846.9亿元，同比增长5.2%。"
                "全市社会消费品零售总额同比下降1.3%。"
            ),
            source_url="https://www.jiangsu.gov.cn/art/2026/7/31/art_33718_11812411.html",
            publication_date="2026-07-31",
        )
        by_id = {item["signal_id"]: item for item in metrics}
        self.assertEqual(by_id["XZ_RETAIL_YOY"]["value"], "-1.3")


if __name__ == "__main__":
    unittest.main()
