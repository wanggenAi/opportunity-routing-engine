import unittest

from src.html_ingest import HtmlFetchEnvelope
from src.resource_underuse_adapters import XuzhouPublicAssetAdapter


class FakeHtmlClient:
    def __init__(self, html_by_name):
        self.html_by_name = html_by_name

    def fetch(self, url, *, request_name, params=None, headers=None):
        return HtmlFetchEnvelope(
            source_id="TEST",
            request_name=request_name,
            url=url,
            fetched_at_utc="2026-09-11T00:00:00+00:00",
            http_status=200,
            content_type="text/html; charset=utf-8",
            payload_sha256="c" * 64,
            encoding="utf-8",
            html=self.html_by_name[request_name],
        )


class XuzhouPublicAssetAdapterTests(unittest.TestCase):
    def test_discovery_preserves_relisting_as_friction_not_underuse(self):
        list_html = """<html><body>
        <a href='/jyxx/003005/003005003/20260804/4f3b4f2e-96b7-425d-8836-dff05d574acd.html'>
        [新][江苏省·徐州市·徐州市]〖交易公告〗一辆海格牌大型普通客车转让项目（第三次）拍卖公告[正在报名]
        </a>
        </body></html>"""
        adapter = XuzhouPublicAssetAdapter(
            client=FakeHtmlClient({"xz_ggzy.property_rights.list": list_html})
        )
        result = adapter.discover_recent(limit=5)
        self.assertEqual(result["item_count"], 1)
        item = result["items"][0]
        self.assertEqual(item["publication_date"], "2026-08-04")
        self.assertEqual(item["listing_mode"], "TRANSFER")
        self.assertEqual(item["listing_round"], 3)
        self.assertTrue(item["relisting_observed"])
        self.assertNotIn("underuse_evidence_state", item)

    def test_detail_explicit_idle_becomes_observed_underuse(self):
        detail_html = """<html><head><title>产权交易</title></head><body>
        <h1>一批原材料、机器设备、电子设备整体转让项目(三次挂牌)</h1>
        <p>信息发布时间：2026-03-09 08:00:00</p>
        <p>项目编号：HHCQ2026ZC0033C</p>
        <p>挂牌起始日期：2026-03-09</p>
        <p>挂牌截止日期：2026-03-13</p>
        <p>存放地：徐州市青年路公园巷1号、2号</p>
        <p>标的现状：标的资产处于闲置状态。</p>
        <p>转让底价（元）：90870.06元</p>
        <p>转让方名称：徐州凤凰新华数码印务有限公司</p>
        </body></html>"""
        url = "https://ggzy.zwb.xz.gov.cn/jyxx/003005/003005003/20260309/43e2d63b-3284-442c-b89f-7458d7083c06.html"
        adapter = XuzhouPublicAssetAdapter(
            client=FakeHtmlClient({"xz_ggzy.property_rights.detail": detail_html})
        )
        listing = adapter.fetch_listing(url)
        self.assertEqual(listing.publication_date, "2026-03-09")
        self.assertEqual(listing.project_id, "HHCQ2026ZC0033C")
        self.assertEqual(listing.listing_round, 3)
        self.assertTrue(listing.relisting_observed)
        self.assertEqual(listing.resource_state, "DISCOVERED")
        self.assertEqual(listing.underuse_evidence_state, "OBSERVED")
        self.assertIn("闲置状态", listing.underuse_excerpt)
        self.assertEqual(listing.asking_price_rmb, "90870.06")
        self.assertEqual(listing.location, "徐州市青年路公园巷1号、2号")
        self.assertEqual(listing.owner_actor, "徐州凤凰新华数码印务有限公司")

    def test_vacant_lease_is_observed_underuse(self):
        detail_html = """<html><body>
        <h1>江苏徐州泉山区吉祥佳苑2#1-109招租项目</h1>
        <p>信息发布时间：2026-07-13</p>
        <p>项目编号：HHCQ2026ZL1493A</p>
        <p>标的坐落：徐州市泉山区二环西路吉祥佳苑</p>
        <p>房屋现状 标的状态：空置 是否设置原承租人优先权：否</p>
        <p>租金底价：31872.12元/年</p>
        <p>出租方名称：徐州新田投资发展有限责任公司</p>
        </body></html>"""
        url = "https://ggzy.zwb.xz.gov.cn/jyxx/003005/003005003/20260713/3a1c6916-de0e-491d-b015-8663acc5066f.html"
        adapter = XuzhouPublicAssetAdapter(
            client=FakeHtmlClient({"xz_ggzy.property_rights.detail": detail_html})
        )
        listing = adapter.fetch_listing(url)
        self.assertEqual(listing.listing_mode, "LEASE")
        self.assertEqual(listing.underuse_evidence_state, "OBSERVED")
        self.assertEqual(listing.asking_price_rmb, "31872.12")

    def test_listing_without_idle_language_stays_unknown_underuse(self):
        detail_html = """<html><body>
        <h1>一批大型游乐设备整体转让项目</h1>
        <p>信息发布时间：2026-06-22</p>
        <p>项目编号：HHCQ2026ZC0243A</p>
        <p>存放地：江苏徐州泉山区彭祖园</p>
        <p>标的现状：标的资产主要包含旋转木马及观光列车，以现场为准。</p>
        <p>转让底价：100000元</p>
        </body></html>"""
        url = "https://ggzy.zwb.xz.gov.cn/jyxx/003005/003005003/20260622/79c7a21b-1bfb-4f02-83c5-a48d1bb3e146.html"
        adapter = XuzhouPublicAssetAdapter(
            client=FakeHtmlClient({"xz_ggzy.property_rights.detail": detail_html})
        )
        listing = adapter.fetch_listing(url)
        self.assertEqual(listing.resource_state, "DISCOVERED")
        self.assertEqual(listing.underuse_evidence_state, "UNKNOWN")
        self.assertIsNone(listing.underuse_excerpt)
        self.assertFalse(listing.relisting_observed)


if __name__ == "__main__":
    unittest.main()
