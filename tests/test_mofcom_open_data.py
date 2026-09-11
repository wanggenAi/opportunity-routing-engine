import tempfile
import unittest
from pathlib import Path

from src.mofcom_open_data import (
    MofcomDatasetSpec,
    MofcomOpenDataAdapter,
    MofcomOpenDataError,
    load_mofcom_watchlist,
)
from src.network_ingest import FetchEnvelope


class FakeJsonClient:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def request_json(self, method, url, *, request_name, params=None, json_body=None, headers=None):
        self.calls.append((method, url, request_name, params))
        return FetchEnvelope(
            source_id="CN_MOFCOM_OPEN_DATA",
            request_name=request_name,
            url=f"{url}?id={params['id']}",
            fetched_at_utc="2026-09-11T00:00:00+00:00",
            http_status=200,
            content_type="application/json",
            payload_sha256="a" * 64,
            payload=self.payload,
        )


class MofcomOpenDataTests(unittest.TestCase):
    def setUp(self):
        self.spec = MofcomDatasetSpec(
            dataset_id="BC88824FFB8D4C862826F5513E099446",
            name="社会融资规模增量统计",
            theme="money_credit",
            refresh_cadence="IRREGULAR",
            enabled=True,
        )

    def test_success_preserves_raw_data_and_provenance(self):
        client = FakeJsonClient({"status": 1, "msg": "ok", "data": [{"period": "2026-04", "value": 1}]})
        result = MofcomOpenDataAdapter(client=client).fetch_dataset(self.spec)
        self.assertEqual(result["api_status"], 1)
        self.assertEqual(result["top_level_item_count"], 1)
        self.assertEqual(result["data"][0]["period"], "2026-04")
        self.assertEqual(result["provenance"]["payload_sha256"], "a" * 64)
        self.assertEqual(client.calls[0][3]["id"], self.spec.dataset_id)

    def test_status_zero_is_error_not_zero_evidence(self):
        client = FakeJsonClient({"status": 0, "msg": "unavailable", "data": None})
        with self.assertRaises(MofcomOpenDataError):
            MofcomOpenDataAdapter(client=client).fetch_dataset(self.spec)

    def test_success_without_data_is_rejected(self):
        client = FakeJsonClient({"status": 1, "msg": "ok"})
        with self.assertRaises(MofcomOpenDataError):
            MofcomOpenDataAdapter(client=client).fetch_dataset(self.spec)

    def test_watchlist_loader_is_strict(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "watchlist.csv"
            path.write_text(
                "dataset_id,name,theme,refresh_cadence,enabled\n"
                "ABC123,Demo,money,MONTHLY,true\n",
                encoding="utf-8",
            )
            items = load_mofcom_watchlist(path)
        self.assertEqual(len(items), 1)
        self.assertTrue(items[0].enabled)
        self.assertEqual(items[0].dataset_id, "ABC123")


if __name__ == "__main__":
    unittest.main()
