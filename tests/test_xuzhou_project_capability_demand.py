import unittest

from src.xuzhou_project_capability_demand import (
    XuzhouProjectCapabilityDemandAdapter,
    extract_project_capability_requirements,
)


class FakeEnvelope:
    def __init__(self, url, html):
        self.url = url
        self.html = html

    def metadata(self):
        return {
            "source_id": "XZ_GGZY",
            "request_name": "fake",
            "url": self.url,
            "http_status": 200,
            "content_type": "text/html; charset=utf-8",
            "payload_sha256": "a" * 64,
        }


class FakeClient:
    def __init__(self, html_by_name):
        self.html_by_name = html_by_name

    def fetch(self, url, *, request_name, params=None, headers=None):
        return FakeEnvelope(url, self.html_by_name[request_name])


class XuzhouProjectCapabilityDemandTests(unittest.TestCase):
    def test_extracts_manager_and_technical_lead_without_supply_inference(self):
        text = """
        3.2项目经理资格和项目总工资格要求
        3.2.1项目经理资格要求
        项目经理具有公路工程专业二级及以上注册建造师资格；
        2023年1月1日以来至少担任过一个二级及以上等级公路路面修复养护工程项目的项目经理。
        3.2.2项目总工资格要求
        项目总工具有公路工程相关专业中级及以上技术职称；
        2023年1月1日以来至少担任过一个公路工程项目的项目总工。
        拟投入项目经理、项目总工应为投标人本单位人员，并提供社保系统打印的本单位人员缴费明细。
        3.3其他要求
        投标人不得存在失信情形。
        """
        result = extract_project_capability_requirements(text)
        by_role = {item.role: item for item in result}
        self.assertIn("PROJECT_MANAGER", by_role)
        self.assertIn("PROJECT_TECHNICAL_LEAD", by_role)
        self.assertIn("二级", by_role["PROJECT_MANAGER"].constructor_license)
        self.assertTrue(by_role["PROJECT_MANAGER"].prior_project_experience_required)
        self.assertTrue(by_role["PROJECT_MANAGER"].bidder_employee_required)
        self.assertTrue(by_role["PROJECT_MANAGER"].social_insurance_proof_required)
        self.assertIn("中级", by_role["PROJECT_TECHNICAL_LEAD"].professional_title)
        self.assertFalse(hasattr(by_role["PROJECT_MANAGER"], "availability"))
        self.assertFalse(hasattr(by_role["PROJECT_MANAGER"], "surplus"))

    def test_extracts_project_lead_testing_qualification(self):
        text = """
        3.2项目负责人条件：
        ①具有公路工程相关专业高级工程师或以上技术职称；
        ②具有《公路水运工程试验检测师证书》；
        ③2023年1月1日至今，至少担任过1个公路路面技术状况自动化检测项目的项目负责人。
        拟投入项目负责人应为投标人本单位人员，并提供社保缴费明细。
        3.3其他要求：信用等级不得低于C级。
        """
        result = extract_project_capability_requirements(text)
        self.assertEqual(len(result), 1)
        item = result[0]
        self.assertEqual(item.role, "PROJECT_LEAD")
        self.assertIn("高级工程师", item.professional_title)
        self.assertIn("试验检测师", item.testing_certificate)
        self.assertTrue(item.prior_project_experience_required)
        self.assertTrue(item.bidder_employee_required)
        self.assertTrue(item.social_insurance_proof_required)

    def test_generic_heading_without_concrete_gate_is_not_evidence(self):
        self.assertEqual(
            extract_project_capability_requirements("3.2项目经理资格要求\n详见招标文件。\n3.3其他要求"),
            [],
        )

    def test_discovery_only_accepts_exact_official_transport_notice_path(self):
        list_html = """<html><body>
        <a href='/jyxx/003002/003002001/20260910/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee.html'>[新]徐州市公路工程项目A</a>
        <a href='/jyxx/003001/003001001/20260910/bbbbbbbb-bbbb-cccc-dddd-eeeeeeeeeeee.html'>建设工程其他栏目</a>
        <a href='https://evil.example/jyxx/003002/003002001/20260911/cccccccc-bbbb-cccc-dddd-eeeeeeeeeeee.html'>伪造项目</a>
        </body></html>"""
        adapter = XuzhouProjectCapabilityDemandAdapter(
            client=FakeClient({"xz_ggzy.transport_tender.list": list_html})
        )
        result = adapter.discover_recent(limit=10)
        self.assertEqual(result["item_count"], 1)
        self.assertEqual(result["items"][0]["publication_date"], "2026-09-10")
        self.assertEqual(result["items"][0]["title"], "徐州市公路工程项目A")

    def test_collect_retains_only_events_with_explicit_capability_requirements(self):
        list_html = """<html><body>
        <a href='/jyxx/003002/003002001/20260910/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee.html'>公路项目A</a>
        <a href='/jyxx/003002/003002001/20260909/bbbbbbbb-bbbb-cccc-dddd-eeeeeeeeeeee.html'>公路项目B</a>
        </body></html>"""
        detail_a = """<html><body>
        <p>信息发布时间：2026-09-10</p>
        <p>3.2项目负责人条件：具有公路工程相关专业中级及以上技术职称；2023年1月1日以来至少担任过一个公路工程项目的项目负责人。</p>
        <p>拟投入项目负责人应为投标人本单位人员，并提供社保缴费明细。</p>
        <p>3.3其他要求</p>
        </body></html>"""
        detail_b = """<html><body><p>信息发布时间：2026-09-09</p><p>本项目无专门人员资格条款。</p></body></html>"""

        class RoutingClient:
            def fetch(self, url, *, request_name, params=None, headers=None):
                if request_name == "xz_ggzy.transport_tender.list":
                    return FakeEnvelope(url, list_html)
                html = detail_a if "aaaaaaaa" in url else detail_b
                return FakeEnvelope(url, html)

        payload = XuzhouProjectCapabilityDemandAdapter(client=RoutingClient()).collect_recent_events(limit=2)
        self.assertEqual(payload["event_count"], 1)
        self.assertGreaterEqual(payload["requirement_count"], 1)
        self.assertEqual(payload["employment_tie_event_count"], 1)
        self.assertEqual(payload["social_insurance_proof_event_count"], 1)
        self.assertIn("NO_HUMAN_CAPABILITY_UNDERUSE_INFERENCE", payload["truth_boundaries"])


if __name__ == "__main__":
    unittest.main()
