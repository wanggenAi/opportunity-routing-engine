import io
import unittest
from email.message import Message

from src.html_ingest import NonHtmlResponseError, PublicHtmlClient, html_to_document
from src.network_ingest import HostNotAllowedError


class FakeResponse:
    def __init__(self, payload: bytes, content_type="text/html; charset=utf-8"):
        self._stream = io.BytesIO(payload)
        self.status = 200
        self.headers = Message()
        self.headers["Content-Type"] = content_type

    def read(self, size=-1):
        return self._stream.read(size)

    def getcode(self):
        return self.status

    def close(self):
        pass


class HtmlIngestTests(unittest.TestCase):
    def test_fetch_retains_hash_and_document_links(self):
        html = """<html><head><title>测试页</title></head><body>
        <script>ignore me</script><h1>数据 发布</h1>
        <a href='/a/20260910/x.html'>项目 A</a><p>2026-09-10</p>
        </body></html>""".encode("utf-8")
        client = PublicHtmlClient(
            source_id="TEST",
            allowed_hosts={"example.com"},
            retries=0,
            transport=lambda request, timeout: FakeResponse(html),
        )
        result = client.fetch("https://example.com/list", request_name="list")
        self.assertEqual(len(result.payload_sha256), 64)
        doc = html_to_document(result.html, base_url=result.url)
        self.assertEqual(doc["title"], "测试页")
        self.assertIn("数据 发布", doc["text"])
        self.assertNotIn("ignore me", doc["text"])
        self.assertEqual(doc["links"][0]["url"], "https://example.com/a/20260910/x.html")

    def test_noscript_fallback_is_retained_as_public_document_content(self):
        html = """<html><head><title>采购公告</title></head><body>
        <noscript>
          <p>项目编号：JSZC-320300-XZTY-G2026-0004</p>
          <p>项目名称：2026年度市直管雨、污水管渠维修养护市场化项目</p>
          <p>预算金额：328.300000万元</p>
        </noscript>
        <script>项目编号：SHOULD_NOT_BE_VISIBLE</script>
        </body></html>"""
        doc = html_to_document(html, base_url="https://example.com/detail")
        self.assertIn("项目编号：JSZC-320300-XZTY-G2026-0004", doc["text"])
        self.assertIn("预算金额：328.300000万元", doc["text"])
        self.assertNotIn("SHOULD_NOT_BE_VISIBLE", doc["text"])

    def test_host_allowlist_is_enforced(self):
        client = PublicHtmlClient(
            source_id="TEST",
            allowed_hosts={"example.com"},
            retries=0,
            transport=lambda *_: FakeResponse(b"<html></html>"),
        )
        with self.assertRaises(HostNotAllowedError):
            client.fetch("https://other.example/page", request_name="bad")

    def test_xml_is_rejected_by_default(self):
        client = PublicHtmlClient(
            source_id="TEST",
            allowed_hosts={"example.com"},
            retries=0,
            transport=lambda *_: FakeResponse(b"<records/>", "text/xml;charset=UTF-8"),
        )
        with self.assertRaises(NonHtmlResponseError):
            client.fetch("https://example.com/list", request_name="xml-default")

    def test_source_can_explicitly_opt_in_to_xml(self):
        client = PublicHtmlClient(
            source_id="TEST_XML",
            allowed_hosts={"example.com"},
            retries=0,
            accepted_content_types={
                "text/html",
                "application/xhtml+xml",
                "text/plain",
                "text/xml",
                "application/xml",
            },
            transport=lambda *_: FakeResponse(
                "<records><record>徐州</record></records>".encode("utf-8"),
                "text/xml;charset=UTF-8",
            ),
        )
        result = client.fetch("https://example.com/list", request_name="xml-opt-in")
        self.assertEqual(result.content_type, "text/xml;charset=UTF-8")
        self.assertIn("徐州", result.html)
        self.assertEqual(len(result.payload_sha256), 64)


if __name__ == "__main__":
    unittest.main()
