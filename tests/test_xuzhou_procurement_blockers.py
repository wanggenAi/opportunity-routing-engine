import unittest

from src.html_ingest import HtmlFetchEnvelope
from src.xuzhou_procurement_blockers import (
    XuzhouProcurementBlockerAdapter,
    extract_explicit_constraints,
)


class _FakeClient:
    def __init__(self, html: str):
        self.html = html

    def fetch(self, url: str, *, request_name: str):
        return HtmlFetchEnvelope(
            source_id="XZ_GGZY_PROCUREMENT_BLOCKER",
            request_name=request_name,
            url=url,
            fetched_at_utc="2026-09-12T00:00:00+00:00",
            http_status=200,
            content_type="text/html; charset=utf-8",
            payload_sha256="a" * 64,
            encoding="utf-8",
            html=self.html,
        )


class XuzhouProcurementBlockerTests(unittest.TestCase):
    def test_specific_qualification_is_observed_capability_constraint(self):
        text = """
二、申请人的资格要求：
（三）本项目的特定资格要求：
投标人具备市政公用工程施工总承包贰级（含）及以上资质（须提供资质证书）。
三、获取招标文件
"""
        result = extract_explicit_constraints(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "CAPABILITY_GAP")
        self.assertEqual(result[0][1], "EXPLICIT_SPECIFIC_QUALIFICATION_REQUIREMENT")
        self.assertIn("市政公用工程施工总承包贰级", result[0][2])

    def test_no_specific_requirement_does_not_manufacture_blocker(self):
        text = """
（三）本项目的特定资格要求：无
三、获取招标文件
"""
        self.assertEqual(extract_explicit_constraints(text), [])

    def test_no_subcontract_rule_is_observed_coordination_constraint(self):
        text = "成交后不得转包或分包，但电气设备的预防性试验可以委托第三方完成。"
        result = extract_explicit_constraints(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "COORDINATION_GAP")
        self.assertEqual(result[0][1], "EXPLICIT_NO_SUBCONTRACT_OR_TRANSFER_RULE")
        self.assertIn("不得转包或分包", result[0][2])

    def test_generic_qualification_section_is_not_enough(self):
        text = "申请人的资格要求：满足政府采购法第二十二条规定。"
        self.assertEqual(extract_explicit_constraints(text), [])

    def test_embedded_article_markup_uses_same_response_fallback(self):
        # Current Xuzhou pages can expose canonical spans/article HTML inside a
        # script/template payload. html_to_document intentionally skips script text;
        # the blocker adapter must recover only explicit approved markers from the
        # same first-party response, without executing JavaScript or relaxing identity.
        project_id = "JSZC-320300-XZTY-G2026-0004"
        url = (
            "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004002/20260910/"
            "fa34bda1-6f69-4512-b5dc-731bf34418ef.html"
        )
        html = f"""
<html><body>
<script type="text/template">
<div><span title="项目编号">{project_id}</span></div>
<div><span title="项目名称">2026年度市直管雨、污水管渠维修养护市场化项目</span></div>
<div>二、申请人的资格要求：</div>
<div>（三）本项目的特定资格要求：</div>
<div>投标人具备市政公用工程施工总承包贰级（含）及以上资质。</div>
<div>三、获取招标文件</div>
<div>成交后不得转包或分包。</div>
</script>
</body></html>
"""
        payload = {
            "events": [
                {
                    "source_id": "XZ_GGZY",
                    "project_id": project_id,
                    "project_name": "2026年度市直管雨、污水管渠维修养护市场化项目",
                    "title": "徐州市水务局2026年度市直管雨、污水管渠维修养护市场化项目公开招标公告",
                    "url": url,
                }
            ]
        }
        result = XuzhouProcurementBlockerAdapter(client=_FakeClient(html)).collect(payload)
        self.assertEqual(result["queried_event_count"], 1)
        self.assertEqual(result["rejected"], [])
        self.assertEqual(result["blocker_count"], 2)
        self.assertEqual(
            {item["blocker_type"] for item in result["blockers"]},
            {"CAPABILITY_GAP", "COORDINATION_GAP"},
        )
        self.assertTrue(
            all(
                item["extraction_path"] == "RAW_HTML_PLAIN_FALLBACK"
                for item in result["blockers"]
            )
        )
        self.assertTrue(
            all(item["project_id"] == project_id for item in result["blockers"])
        )


if __name__ == "__main__":
    unittest.main()
