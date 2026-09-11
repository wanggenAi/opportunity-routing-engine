import unittest

from src.xuzhou_enterprise_funding_demand import (
    TRUTH_BOUNDARIES,
    discover_jpage_proxy,
    extract_funding_demand_event,
    parse_local_dynamics_records,
)


INDEX_HTML = """<html><body>
<div id="212860"><script type="text/xml"><datastore>
<nextgroup><![CDATA[<a href="/module/web/jpage/dataproxy.jsp?page=1&appid=1&webid=1&path=/&columnid=33718&unitid=212860&webname=江苏省人民政府&permissiontype=0"></a>]]></nextgroup>
<recordset>
<record><![CDATA[<li><a href='/art/2026/9/11/art_33718_11828204.html' title='连云港跨里海班列运输提质提速'>连云港跨里海班列运输提质提速</a><span>2026-09-11</span></li>]]></record>
<record><![CDATA[<li><a href='/art/2025/12/15/art_33718_11693505.html' title='徐州以产业集群培育赋能中小企业高质量发展'>徐州以产业集群培育赋能中小企业高质量发展</a><span>2025-12-15</span></li>]]></record>
</recordset></datastore></script></div>
<script>var param_212860={columnid:33718,unitid:'212860'}; $('#212860').jpage({totalRecord:4895,perPage:19});</script>
</body></html>"""


def funding_article(scope="中小微企业", demand="13.6"):
    return f"""<html><head><title>江苏省人民政府 地方动态</title></head><body>
    <h1>徐州以产业集群培育赋能中小企业高质量发展</h1>
    <div>时间：2025-12-15 14:18 来源：徐州市政府办公室 字号：默认 小 大</div>
    <p>针对企业发展需求，徐州强化政策精准赋能。</p>
    <p>2025年开展“银企同心 产融共进”融资专项行动，联合相关部门安排专项信贷资金1100亿元支持{scope}，截至目前，累计摸排融资需求{demand}亿元，已授信12.59亿元，惠及118家企业。</p>
    </body></html>"""


class XuzhouEnterpriseFundingDemandTests(unittest.TestCase):
    def test_parses_official_column_records_and_rejects_date_identity_drift(self):
        html = INDEX_HTML + "<a href='/art/2026/9/10/art_33718_1.html' title='徐州错误日期'>x</a><span>2026-09-09</span>"
        records = parse_local_dynamics_records(html)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[1]["publication_date"], "2025-12-15")
        self.assertTrue(records[1]["url"].startswith("https://www.jiangsu.gov.cn/art/"))

    def test_discovers_only_official_jpage_identity(self):
        proxy = discover_jpage_proxy(INDEX_HTML)
        self.assertIn("/module/web/jpage/dataproxy.jsp", proxy["url"])
        self.assertEqual(proxy["total_records"], 4895)
        self.assertEqual(proxy["per_page"], 19)

    def test_extracts_scoped_direct_need_without_relabeling_sme_private(self):
        event = extract_funding_demand_event(
            title="徐州以产业集群培育赋能中小企业高质量发展",
            url="https://www.jiangsu.gov.cn/art/2025/12/15/art_33718_11693505.html",
            html=funding_article(),
            provenance_sha256="a" * 64,
        )
        self.assertIsNotNone(event)
        self.assertEqual(event["demand_amount_cny_100m"], "13.6")
        self.assertEqual(event["granted_credit_amount_cny_100m"], "12.59")
        self.assertEqual(event["beneficiary_enterprises"], 118)
        self.assertEqual(event["program_name"], "银企同心 产融共进")
        self.assertEqual(event["actor_scope"], "SME_AND_MICRO")
        self.assertFalse(event["private_enterprise_scope_explicit"])
        self.assertFalse(event["aggregation_allowed"])
        self.assertIn("DIRECT_DEMAND_EVIDENCE_IS_NEED_ONLY", event["truth_boundaries"])
        self.assertIn("SME_IS_NOT_PRIVATE_ENTERPRISE", event["truth_boundaries"])

    def test_private_scope_requires_explicit_private_language(self):
        event = extract_funding_demand_event(
            title="徐州以产业集群培育赋能中小企业高质量发展",
            url="https://www.jiangsu.gov.cn/art/2025/12/15/art_33718_11693505.html",
            html=funding_article(scope="民营企业"),
            provenance_sha256="b" * 64,
        )
        self.assertEqual(event["actor_scope"], "PRIVATE_ENTERPRISE")
        self.assertTrue(event["private_enterprise_scope_explicit"])

    def test_policy_language_without_explicit_demand_amount_is_not_evidence(self):
        html = funding_article().replace("累计摸排融资需求13.6亿元，", "持续满足企业融资需求，")
        event = extract_funding_demand_event(
            title="徐州以产业集群培育赋能中小企业高质量发展",
            url="https://www.jiangsu.gov.cn/art/2025/12/15/art_33718_11693505.html",
            html=html,
            provenance_sha256="c" * 64,
        )
        self.assertIsNone(event)

    def test_non_xuzhou_government_office_page_is_not_promoted(self):
        html = funding_article().replace("徐州市政府办公室", "某媒体")
        event = extract_funding_demand_event(
            title="徐州以产业集群培育赋能中小企业高质量发展",
            url="https://www.jiangsu.gov.cn/art/2025/12/15/art_33718_11693505.html",
            html=html,
            provenance_sha256="d" * 64,
        )
        self.assertIsNone(event)

    def test_truth_boundaries_forbid_cross_program_sum_and_opportunity_inference(self):
        self.assertIn("NO_CROSS_PROGRAM_SUM", TRUTH_BOUNDARIES)
        self.assertIn("NO_CROSS_PERIOD_SUM", TRUTH_BOUNDARIES)
        self.assertIn("NO_SURPLUS_RESOURCE_INFERENCE", TRUTH_BOUNDARIES)
        self.assertIn("NO_OPPORTUNITY_INFERENCE", TRUTH_BOUNDARIES)


if __name__ == "__main__":
    unittest.main()
