import io
import unittest
from email.message import Message

from src.html_ingest import PublicHtmlClient, html_to_document
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

    def test_host_allowlist_is_enforced(self):
        client = PublicHtmlClient(
            source_id="TEST",
            allowed_hosts={"example.com"},
            retries=0,
            transport=lambda *_: FakeResponse(b"<html></html>"),
        )
        with self.assertRaises(HostNotAllowedError):
            client.fetch("https://other.example/page", request_name="bad")


if __name__ == "__main__":
    unittest.main()
