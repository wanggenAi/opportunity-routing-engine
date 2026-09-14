import unittest

from src.html_ingest import HtmlFetchEnvelope
from src.procurement_rebid import build_procurement_rebid_signals
from src.xuzhou_procurement_failures import (
    XuzhouProcurementFailureAdapter,
    extract_explicit_void_packages,
)


class FakeHtmlClient:
    def __init__(self, html):
        self.html = html

    def fetch(self, url, *, request_name, params=None, headers=None):
        return HtmlFetchEnvelope(
            source_id="TEST",
            request_name=request_name,
            url=url,
            fetched_at_utc="2026-09-14T00:00:00+00:00",
            http_status=200,
            content_type="text/html; charset=utf-8",
            payload_sha256="a" * 64,
            encoding="utf-8",
            html=self.html,
        )


class ProcurementFailureTests(unittest.TestCase):
    def test_extracts_only_package_segment_with_explicit_void_marker(self):
        text = (
            "采购包1 供应商名称 某公司 913203000000000000 中标金额100元 "
            "采购包2 有效投标人不足三家，此采购包已作废。 "
            "采购包3 供应商名称 另一公司 913203000000000001 中标金额200元"
        )
        self.assertEqual(
            extract_explicit_void_packages(text),
            [("采购包2", "采购包2 有效投标人不足三家,此采购包已作废")],
        )

    def test_fetch_failure_preserves_exact_project_and_buyer_identity(self):
        html = """<html><head><title>结果公告</title></head><body>
        <h1>徐州市水务局2026年度市直管雨、污水管渠维修养护市场化项目中标结果公告采购包2</h1>
        <p>信息发布时间：2026-09-08</p>
        <p>一、项目编号：JSZC-320300-XZTY-G2026-0001</p>
        <p>二、项目名称：2026年度市直管雨、污水管渠维修养护市场化项目</p>
        <p>采购包1</p><table><tr><td>供应商</td></tr></table>
        <p>采购包2</p><p>此采购包已作废</p>
        <p>采购包3</p><table><tr><td>供应商</td></tr></table>
        <h2>九、凡对本次公告内容提出询问，请按以下方式联系。</h2>
        <p>1.采购人信息</p><p>单位名称：徐州市水务局</p>
        </body></html>"""
        adapter = XuzhouProcurementFailureAdapter(client=FakeHtmlClient(html))
        failures = adapter.fetch_failures(
            "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260908/f5ef822d-2b05-48e5-b627-9dec404494f0.html"
        )
        self.assertEqual(len(failures), 1)
        failure = failures[0]
        self.assertEqual(failure.project_id, "JSZC-320300-XZTY-G2026-0001")
        self.assertEqual(failure.buyer_actor, "徐州市水务局")
        self.assertEqual(failure.package_name, "采购包2")
        self.assertEqual(failure.outcome_state, "EXPLICIT_PACKAGE_VOID")

    def test_missing_or_unawarded_supplier_does_not_itself_create_failure(self):
        text = "采购包1 暂无供应商信息 采购包2 中标公告"
        self.assertEqual(extract_explicit_void_packages(text), [])

    def test_collect_deduplicates_same_failed_package_seen_on_sibling_result_urls(self):
        html = """<html><body>
        <p>信息发布时间：2026-09-08</p>
        <p>项目编号：P-1</p><p>项目名称：2026年度市直管雨、污水管渠维修养护市场化项目</p>
        <p>采购包2 此采购包已作废</p>
        <p>采购人信息 单位名称：徐州市水务局</p>
        </body></html>"""
        adapter = XuzhouProcurementFailureAdapter(client=FakeHtmlClient(html))
        payload = adapter.collect_from_result_payloads(
            [
                {
                    "awards": [
                        {
                            "url": "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260908/11111111-1111-1111-1111-111111111111.html",
                            "title": "结果公告采购包1",
                        },
                        {
                            "url": "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260908/22222222-2222-2222-2222-222222222222.html",
                            "title": "结果公告采购包3",
                        },
                    ]
                }
            ]
        )
        self.assertEqual(payload["result_url_count"], 2)
        self.assertEqual(payload["failed_package_count"], 1)


class ProcurementRebidTests(unittest.TestCase):
    def _failure_payload(self):
        return {
            "failures": [
                {
                    "source_id": "XZ_GGZY_PROCUREMENT_FAILURE",
                    "url": "https://example.test/result",
                    "publication_date": "2026-09-08",
                    "project_id": "JSZC-320300-XZTY-G2026-0001",
                    "project_name": "2026年度市直管雨、污水管渠维修养护市场化项目",
                    "buyer_actor": "徐州市水务局",
                    "package_name": "采购包2",
                    "outcome_state": "EXPLICIT_PACKAGE_VOID",
                    "title": "徐州市水务局2026年度市直管雨、污水管渠维修养护市场化项目中标结果公告采购包2",
                }
            ]
        }

    def _tender_payload(self):
        return {
            "events": [
                {
                    "source_id": "XZ_GGZY",
                    "url": "https://example.test/tender",
                    "publication_date": "2026-09-10",
                    "project_id": "JSZC-320300-XZTY-G2026-0004",
                    "project_name": "2026年度市直管雨、污水管渠维修养护市场化项目",
                    "title": "徐州市水务局2026年度市直管雨、污水管渠维修养护市场化项目公开招标公告",
                    "budget_rmb": "3283000.00",
                }
            ]
        }

    def test_builds_observed_program_rebid_without_promoting_commercial_truth(self):
        result = build_procurement_rebid_signals(
            self._tender_payload(), self._failure_payload()
        )
        self.assertEqual(result["signal_count"], 1)
        signal = result["signals"][0]
        self.assertEqual(signal["capability_key"], "DRAINAGE_NETWORK_MAINTENANCE")
        self.assertEqual(signal["actor"], "徐州市水务局")
        self.assertEqual(signal["days_after_failure"], 2)
        self.assertEqual(signal["failed_packages"], ["采购包2"])
        self.assertEqual(signal["current_budget_rmb"], "3283000.00")
        self.assertEqual(
            signal["package_mapping_state"],
            "PROGRAM_LEVEL_ONLY_EXACT_PACKAGE_MAPPING_UNRESOLVED",
        )
        for forbidden in ("payer", "paid_event_count", "commercial_score", "provider_actor"):
            self.assertNotIn(forbidden, signal)

    def test_different_buyer_does_not_match_even_with_same_project_name(self):
        tender = self._tender_payload()
        tender["events"][0]["title"] = (
            "其他采购单位2026年度市直管雨、污水管渠维修养护市场化项目公开招标公告"
        )
        result = build_procurement_rebid_signals(tender, self._failure_payload())
        self.assertEqual(result["signal_count"], 0)
        self.assertEqual(
            result["rejected"][0]["reason"],
            "BUYER_ACTOR_NOT_EXPLICIT_IN_CURRENT_TENDER_TITLE",
        )

    def test_fuzzy_project_name_is_forbidden(self):
        tender = self._tender_payload()
        tender["events"][0]["project_name"] += "（二次）"
        result = build_procurement_rebid_signals(tender, self._failure_payload())
        self.assertEqual(result["signal_count"], 0)

    def test_time_must_move_forward_within_bounded_window(self):
        tender = self._tender_payload()
        tender["events"][0]["publication_date"] = "2026-09-07"
        self.assertEqual(
            build_procurement_rebid_signals(tender, self._failure_payload())["signal_count"],
            0,
        )
        tender["events"][0]["publication_date"] = "2026-11-30"
        self.assertEqual(
            build_procurement_rebid_signals(tender, self._failure_payload())["signal_count"],
            0,
        )

    def test_invalid_window_fails_closed(self):
        with self.assertRaises(ValueError):
            build_procurement_rebid_signals(
                self._tender_payload(), self._failure_payload(), max_days_after_failure=0
            )


if __name__ == "__main__":
    unittest.main()
