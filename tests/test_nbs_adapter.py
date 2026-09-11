import unittest

from src.nbs_adapter import NBSAdapter, normalize_period_token, normalize_periods
from src.network_ingest import FetchEnvelope


class FakeClient:
    def __init__(self):
        self.calls = []

    def request_json(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        name = kwargs["request_name"]
        if name.startswith("nbs.root"):
            payload = {"data": [{"_id": "root-1", "name": "月度数据", "isLeaf": False}]}
        elif name.startswith("nbs.tree"):
            payload = {"data": [{"_id": "cid-1", "name": "居民消费价格指数", "isLeaf": True}]}
        elif name.startswith("nbs.indicators"):
            payload = {
                "data": {
                    "list": [
                        {
                            "_id": "ind-1",
                            "i_showname": "居民消费价格指数(上年同月=100)",
                            "du_name": "指数",
                            "catalogid": "cid-1",
                        }
                    ]
                }
            }
        elif name.startswith("nbs.dates"):
            payload = {"data": ["202608MM"]}
        elif name.startswith("nbs.values"):
            payload = {
                "data": [
                    {
                        "code": "202608MM",
                        "values": [
                            {
                                "_id": "ind-1",
                                "i_showname": "居民消费价格指数(上年同月=100)",
                                "du_name": "指数",
                                "area": "全国",
                                "areaCode": "000000000000",
                                "value": "101.2",
                            }
                        ],
                    }
                ]
            }
        else:
            raise AssertionError(name)
        return FetchEnvelope(
            source_id="CN_NBS",
            request_name=name,
            url=url,
            fetched_at_utc="2026-09-11T00:00:00+00:00",
            http_status=200,
            content_type="application/json",
            payload_sha256="0" * 64,
            payload=payload,
        )


class NBSAdapterTests(unittest.TestCase):
    def test_period_normalization(self):
        self.assertEqual(normalize_period_token("202608", "month"), "202608MM")
        self.assertEqual(normalize_period_token("2026Q2", "quarter"), "202602SS")
        self.assertEqual(normalize_period_token("2026", "year"), "2026YY")
        self.assertEqual(normalize_periods(["202601-202608"], "month"), ["202601MM-202608MM"])

    def test_probe_reads_root_and_children(self):
        adapter = NBSAdapter(client=FakeClient())
        result = adapter.probe(["monthData"])
        self.assertEqual(result["pages"]["monthData"]["root"]["id"], "root-1")
        self.assertEqual(result["pages"]["monthData"]["children"][0]["id"], "cid-1")

    def test_indicator_normalization(self):
        adapter = NBSAdapter(client=FakeClient())
        indicators = adapter.indicators("monthData", cid="cid-1")
        self.assertEqual(indicators[0]["indicator_id"], "ind-1")
        self.assertEqual(indicators[0]["unit"], "指数")

    def test_fetch_values_flattens_records_and_sends_current_payload_shape(self):
        client = FakeClient()
        adapter = NBSAdapter(client=client)
        result = adapter.fetch_values(
            "monthData",
            cid="cid-1",
            indicator_ids=["ind-1"],
            periods=["202608"],
        )
        self.assertEqual(result["row_count"], 1)
        self.assertEqual(result["records"][0]["value"], "101.2")
        method, _, kwargs = client.calls[-1]
        self.assertEqual(method, "POST")
        self.assertEqual(kwargs["json_body"]["dts"], ["202608MM"])
        self.assertEqual(kwargs["json_body"]["rootId"], "root-1")

    def test_bounded_catalog_discovery(self):
        adapter = NBSAdapter(client=FakeClient())
        matches = adapter.discover_catalogs(
            "monthData",
            keywords=["居民消费价格"],
            max_nodes=10,
        )
        self.assertEqual(matches["居民消费价格"][0]["cid"], "cid-1")


if __name__ == "__main__":
    unittest.main()
