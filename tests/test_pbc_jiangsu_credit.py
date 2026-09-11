import io
import unittest

from src.network_ingest import HostNotAllowedError
from src.pbc_jiangsu_credit import (
    discover_latest_credit_table,
    discover_xls_attachment,
    extract_jiangsu_credit_metrics,
)
from src.xls_ingest import NonXlsResponseError, PublicXlsClient, XlsParseError, parse_workbook_rows


class _Headers:
    def __init__(self, values=None):
        self.values = values or {}

    def get(self, name, default=""):
        return self.values.get(name, default)


class _Response:
    def __init__(self, body, *, url="https://nanjing.pbc.gov.cn/file.xls", content_type="application/vnd.ms-excel"):
        self.body = body
        self.url = url
        self.status = 200
        self.headers = _Headers({"Content-Type": content_type})

    def read(self, _limit):
        return self.body

    def getcode(self):
        return self.status

    def geturl(self):
        return self.url

    def close(self):
        pass


def _rmb_sheet():
    return {
        "sheet_index": 0,
        "sheet_name": "人民币信贷",
        "row_count": 10,
        "column_count": 4,
        "rows": [
            ["2026年7月江苏省金融机构人民币信贷收支表"],
            ["单位：亿元"],
            ["项目 Item", "2026.06", "2026.07", "2026.08"],
            ["一、各项存款 Total Deposits", 285000, 291300, None],
            ["1.住户存款 Household Deposits", 150000, 152000, None],
            ["2.非金融企业存款 Non-financial Enterprise Deposits", 80000, 81000, None],
            ["资金运用方项目"],
            ["一、各项贷款 Total Loans", 298000, 302800, None],
            ["1.住户贷款 Household Loans", 60000, 61000, None],
            ["2.企（事）业单位贷款 Enterprise and Institution Loans", 230000, 235000, None],
        ],
    }


class PbcJiangsuCreditTests(unittest.TestCase):
    def test_discovers_latest_month_by_period_not_link_order(self):
        doc = {
            "links": [
                {
                    "text": "2026年6月江苏省金融机构信贷收支表",
                    "url": "https://nanjing.pbc.gov.cn/nanjing/june/index.html",
                },
                {
                    "text": "2025年12月江苏省金融机构信贷收支表",
                    "url": "https://nanjing.pbc.gov.cn/nanjing/dec/index.html",
                },
                {
                    "text": "2026年7月江苏省金融机构信贷收支表",
                    "url": "https://nanjing.pbc.gov.cn/nanjing/july/index.html",
                },
            ]
        }
        result = discover_latest_credit_table(doc)
        self.assertEqual(result["observation_period"], "2026-07")
        self.assertEqual(result["period_key"], "2026.07")
        self.assertIn("7月", result["title"])

    def test_latest_discovery_rejects_non_official_host(self):
        with self.assertRaises(ValueError):
            discover_latest_credit_table(
                {
                    "links": [
                        {
                            "text": "2099年12月江苏省金融机构信贷收支表",
                            "url": "https://evil.example/latest",
                        }
                    ]
                }
            )

    def test_discovers_exact_official_xls_attachment(self):
        title = "2026年7月江苏省金融机构信贷收支表"
        doc = {
            "links": [
                {
                    "text": f"{title}.xls",
                    "url": "https://nanjing.pbc.gov.cn/nanjing/file.xls",
                }
            ]
        }
        self.assertEqual(
            discover_xls_attachment(doc, expected_title=title),
            "https://nanjing.pbc.gov.cn/nanjing/file.xls",
        )

    def test_attachment_rejects_off_domain(self):
        title = "2026年7月江苏省金融机构信贷收支表"
        with self.assertRaises(ValueError):
            discover_xls_attachment(
                {
                    "links": [
                        {
                            "text": f"{title}.xls",
                            "url": "https://evil.example/file.xls",
                        }
                    ]
                },
                expected_title=title,
            )

    def test_extracts_required_jiangsu_credit_metrics_from_period_column(self):
        result = extract_jiangsu_credit_metrics([_rmb_sheet()], period_key="2026.07")
        metrics = result["metrics"]
        self.assertEqual(result["period_gate"], "EXPLICIT_PERIOD_HEADER")
        self.assertEqual(result["value_column_1based"], 3)
        self.assertEqual(metrics["total_deposits_100m_cny"], 291300.0)
        self.assertEqual(metrics["household_deposits_100m_cny"], 152000.0)
        self.assertEqual(metrics["nonfinancial_enterprise_deposits_100m_cny"], 81000.0)
        self.assertEqual(metrics["total_loans_100m_cny"], 302800.0)
        self.assertEqual(metrics["household_loans_100m_cny"], 61000.0)
        self.assertEqual(metrics["enterprise_institution_loans_100m_cny"], 235000.0)
        self.assertAlmostEqual(metrics["total_deposits_trillion_cny"], 29.13)
        self.assertAlmostEqual(metrics["total_loans_trillion_cny"], 30.28)

    def test_missing_required_metric_fails_closed(self):
        sheet = _rmb_sheet()
        sheet["rows"] = [row for row in sheet["rows"] if "非金融企业存款" not in str(row[0])]
        with self.assertRaisesRegex(ValueError, "required Jiangsu credit metrics missing"):
            extract_jiangsu_credit_metrics([sheet], period_key="2026.07")

    def test_duplicate_metric_label_fails_closed(self):
        sheet = _rmb_sheet()
        sheet["rows"].append(["各项贷款 duplicate", 1, 2, 3])
        with self.assertRaisesRegex(ValueError, "metric label is ambiguous"):
            extract_jiangsu_credit_metrics([sheet], period_key="2026.07")

    def test_missing_unit_fails_closed(self):
        sheet = _rmb_sheet()
        sheet["rows"][1] = ["金额"]
        with self.assertRaisesRegex(ValueError, "unit is not explicitly"):
            extract_jiangsu_credit_metrics([sheet], period_key="2026.07")

    def test_foreign_currency_sheet_is_not_accepted_as_rmb_sheet(self):
        sheet = _rmb_sheet()
        sheet["sheet_name"] = "本外币信贷"
        sheet["rows"][0] = ["江苏省金融机构本外币信贷收支表"]
        with self.assertRaisesRegex(ValueError, "expected one RMB credit sheet"):
            extract_jiangsu_credit_metrics([sheet], period_key="2026.07")

    def test_public_xls_client_hashes_valid_ole_payload(self):
        payload = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"fake-biff-test-payload"
        client = PublicXlsClient(
            source_id="TEST",
            allowed_hosts={"nanjing.pbc.gov.cn"},
            retries=0,
            transport=lambda _request, _timeout: _Response(payload),
        )
        envelope = client.fetch("https://nanjing.pbc.gov.cn/file.xls", request_name="test")
        self.assertEqual(envelope.payload, payload)
        self.assertEqual(envelope.size_bytes, len(payload))
        self.assertEqual(len(envelope.payload_sha256), 64)

    def test_public_xls_client_rejects_html_and_off_domain(self):
        html_client = PublicXlsClient(
            source_id="TEST",
            allowed_hosts={"nanjing.pbc.gov.cn"},
            retries=0,
            transport=lambda _request, _timeout: _Response(b"<html>challenge</html>", content_type="text/html"),
        )
        with self.assertRaises(NonXlsResponseError):
            html_client.fetch("https://nanjing.pbc.gov.cn/file.xls", request_name="test")
        with self.assertRaises(HostNotAllowedError):
            html_client.fetch("https://evil.example/file.xls", request_name="test")

    def test_parser_rejects_non_ole_before_optional_dependency(self):
        with self.assertRaises(XlsParseError):
            parse_workbook_rows(b"not-an-xls")


if __name__ == "__main__":
    unittest.main()
