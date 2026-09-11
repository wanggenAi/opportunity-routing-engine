import io
import json
import unittest
from email.message import Message
from pathlib import Path
from tempfile import TemporaryDirectory

from src.network_ingest import (
    HostNotAllowedError,
    JsonHttpClient,
    NonJsonResponseError,
    load_source_registry,
    write_json_atomic,
)


class FakeResponse:
    def __init__(self, payload: bytes, status: int = 200, content_type: str = "application/json"):
        self._stream = io.BytesIO(payload)
        self.status = status
        self.headers = Message()
        self.headers["Content-Type"] = content_type

    def read(self, size=-1):
        return self._stream.read(size)

    def getcode(self):
        return self.status

    def close(self):
        pass


class NetworkIngestTests(unittest.TestCase):
    def test_json_fetch_preserves_provenance(self):
        captured = {}

        def transport(request, timeout):
            captured["url"] = request.full_url
            captured["timeout"] = timeout
            return FakeResponse(json.dumps({"ok": True}).encode())

        client = JsonHttpClient(
            source_id="TEST",
            allowed_hosts={"example.com"},
            transport=transport,
            retries=0,
        )
        result = client.request_json(
            "GET",
            "https://example.com/api",
            request_name="demo",
            params={"q": "徐州"},
        )
        self.assertEqual(result.payload, {"ok": True})
        self.assertEqual(result.source_id, "TEST")
        self.assertEqual(result.request_name, "demo")
        self.assertEqual(len(result.payload_sha256), 64)
        self.assertIn("q=", captured["url"])

    def test_rejects_non_allowlisted_host(self):
        client = JsonHttpClient(
            source_id="TEST",
            allowed_hosts={"example.com"},
            transport=lambda *_: FakeResponse(b"{}"),
        )
        with self.assertRaises(HostNotAllowedError):
            client.request_json(
                "GET",
                "https://evil.example/api",
                request_name="bad",
            )

    def test_rejects_html_challenge_even_with_200(self):
        client = JsonHttpClient(
            source_id="TEST",
            allowed_hosts={"example.com"},
            transport=lambda *_: FakeResponse(
                b"<html>Please enable JavaScript</html>",
                content_type="text/html",
            ),
            retries=0,
        )
        with self.assertRaises(NonJsonResponseError):
            client.request_json(
                "GET", "https://example.com/api", request_name="challenge"
            )

    def test_registry_schema_is_strict(self):
        with TemporaryDirectory() as temp:
            path = Path(temp) / "registry.csv"
            path.write_text(
                "source_id,name,source_tier,owner,base_url,geography,indicator_scope,access_mode,refresh_cadence,automation_allowed,status\n"
                "A,Alpha,A,Owner,https://example.com,China,GDP,JSON,MONTHLY,YES,ACTIVE\n",
                encoding="utf-8",
            )
            registry = load_source_registry(path)
            self.assertEqual(registry["A"].owner, "Owner")

    def test_atomic_json_write(self):
        with TemporaryDirectory() as temp:
            path = Path(temp) / "nested" / "sample.json"
            write_json_atomic(path, {"x": 1})
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {"x": 1})


if __name__ == "__main__":
    unittest.main()
