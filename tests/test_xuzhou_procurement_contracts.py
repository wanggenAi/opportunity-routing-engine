import unittest

from src.network_ingest import FetchEnvelope
from src.xuzhou_procurement_contracts import (
    XuzhouProcurementContractAdapter,
    parse_contract_content,
)


MODERN_CONTENT = (
    "测试维修养护项目采购包1合同"
    "一、合同编号：JSZC-320300-TEST-G2026-0001001"
    "二、合同名称：测试维修养护项目采购包1合同"
    "三、项目编号(或招标编号、政府采购计划编号、采购计划备案号等、如有) : "
    "JSZC-320300-TEST-G2026-0001"
    "四、项目名称：测试维修养护项目"
    "五、合同主体"
    "采购人（甲方）：徐州市测试采购单位"
    "地址：徐州市测试路1号联系方式：12345678"
    "供应商（乙方）: 徐州测试服务有限公司"
    "地址：徐州市服务路2号联系方式：87654321"
    "六、合同主要信息"
    "主要标的信息：维修养护服务"
    "合同金额：90万元"
    "履约期限、地点等简要信息：一年"
    "七、合同签订日期：2026-09-20"
    "八、合同公告日期：2026-09-21"
)

LEGACY_CONTENT = (
    "一、采购单位：徐州经济技术开发区水务处"
    "二、采购预算（元）：6753300.00"
    "三、编号：legacy-ref"
    "四、合同名称：2021年市政排水设施养护项目采购合同公示"
    "五、采购项目编号：徐采公（2021）JSSW（Q）001"
    "六、项目名称：徐州经济技术开发区2021年市政排水设施养护项目"
    "七、中标供应商：江苏嘉利物业管理有限公司"
    "八、合同金额（元）：6680000.00"
    "九、合同签订日期：2021-04-15"
    "十、合同公告日期：2021-05-10"
)


class FakeClient:
    def __init__(self, payloads):
        self.payloads = list(payloads)
        self.calls = []

    def request_json(self, method, url, *, request_name, params=None, json_body=None, headers=None):
        self.calls.append(
            {
                "method": method,
                "url": url,
                "request_name": request_name,
                "params": params,
                "json_body": json_body,
                "headers": headers,
            }
        )
        payload = self.payloads.pop(0)
        return FetchEnvelope(
            source_id="XZ_GGZY_PROCUREMENT_CONTRACT",
            request_name=request_name,
            url=url,
            fetched_at_utc="2026-09-12T00:00:00+00:00",
            http_status=200,
            content_type="application/json;charset=UTF-8",
            payload_sha256="search-sha",
            payload=payload,
        )


def _search_payload(records):
    return {"result": {"totalcount": len(records), "records": records}}


def _record(content, *, url="/jyxx/003004/003004007//contract-guid.html"):
    return {
        "title": "测试维修养护项目采购包1合同",
        "content": content,
        "linkurl": url,
        "infodate": "2026-09-21 10:20:30",
        "categorynum": "003004007",
    }


class XuzhouProcurementContractTests(unittest.TestCase):
    def test_modern_contract_fields_are_explicit_and_buyer_is_not_payer(self):
        parsed = parse_contract_content(MODERN_CONTENT)
        self.assertEqual(parsed["project_id"], "JSZC-320300-TEST-G2026-0001")
        self.assertEqual(parsed["project_name"], "测试维修养护项目")
        self.assertEqual(parsed["contract_id"], "JSZC-320300-TEST-G2026-0001001")
        self.assertEqual(parsed["buyer_actor"], "徐州市测试采购单位")
        self.assertEqual(parsed["supplier_actor"], "徐州测试服务有限公司")
        self.assertEqual(parsed["contract_amount_rmb"], "900000.00")
        self.assertEqual(parsed["signed_date"], "2026-09-20")
        self.assertTrue(parsed["contract_signed"])
        self.assertIsNone(parsed["payer_actor"])
        self.assertIsNone(parsed["settled_amount_rmb"])
        self.assertFalse(parsed["settlement_proven"])

    def test_legacy_contract_template_is_parsed_without_payment_inference(self):
        parsed = parse_contract_content(LEGACY_CONTENT)
        self.assertEqual(parsed["project_id"], "徐采公（2021）JSSW（Q）001")
        self.assertEqual(parsed["buyer_actor"], "徐州经济技术开发区水务处")
        self.assertEqual(parsed["supplier_actor"], "江苏嘉利物业管理有限公司")
        self.assertEqual(parsed["contract_amount_rmb"], "6680000.00")
        self.assertEqual(parsed["signed_date"], "2021-04-15")
        self.assertIsNone(parsed["payer_actor"])
        self.assertFalse(parsed["settlement_proven"])

    def test_exact_project_hit_becomes_contract_evidence_only(self):
        client = FakeClient([_search_payload([_record(MODERN_CONTENT)])])
        adapter = XuzhouProcurementContractAdapter(client=client)
        payload = adapter.collect_projects(["JSZC-320300-TEST-G2026-0001"])
        self.assertEqual(payload["contract_count"], 1)
        contract = payload["contracts"][0]
        self.assertEqual(contract["project_id"], "JSZC-320300-TEST-G2026-0001")
        self.assertTrue(contract["contract_signed"])
        self.assertFalse(contract["settlement_proven"])
        self.assertIsNone(contract["payer_actor"])
        self.assertEqual(contract["provenance"]["payload_sha256"], "search-sha")
        self.assertTrue(contract["url"].startswith("https://ggzy.zwb.xz.gov.cn/"))
        self.assertEqual(client.calls[0]["method"], "POST")
        self.assertEqual(
            client.calls[0]["json_body"]["condition"][0]["equal"],
            "003004007",
        )
        self.assertEqual(client.calls[0]["json_body"]["noParticiple"], "1")

    def test_search_relevance_cannot_override_project_identity(self):
        client = FakeClient([_search_payload([_record(MODERN_CONTENT)])])
        adapter = XuzhouProcurementContractAdapter(client=client)
        payload = adapter.collect_projects(["JSZC-320300-OTHER-G2026-9999"])
        self.assertEqual(payload["contract_count"], 0)
        project = payload["projects"][0]
        self.assertEqual(project["rejected_count"], 1)
        self.assertEqual(
            project["rejected_hits"][0]["reason"],
            "NO_EXACT_PROJECT_ID_MATCH",
        )

    def test_zero_exact_contracts_is_valid_empirical_result(self):
        client = FakeClient([_search_payload([])])
        adapter = XuzhouProcurementContractAdapter(client=client)
        payload = adapter.collect_projects(["JSZC-320300-TEST-G2026-0001"])
        self.assertEqual(payload["contract_count"], 0)
        self.assertEqual(payload["projects"][0]["search_total"], 0)
        self.assertFalse(payload["projects"][0]["truncated"])

    def test_non_first_party_link_is_rejected(self):
        client = FakeClient(
            [_search_payload([_record(MODERN_CONTENT, url="https://example.com/x")])]
        )
        adapter = XuzhouProcurementContractAdapter(client=client)
        payload = adapter.collect_projects(["JSZC-320300-TEST-G2026-0001"])
        self.assertEqual(payload["contract_count"], 0)
        self.assertEqual(
            payload["projects"][0]["rejected_hits"][0]["reason"],
            "FIRST_PARTY_CONTRACT_URL_UNRESOLVED",
        )


if __name__ == "__main__":
    unittest.main()
