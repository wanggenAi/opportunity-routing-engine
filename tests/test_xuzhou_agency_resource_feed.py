import unittest

from src.html_ingest import HtmlFetchEnvelope
from src.xuzhou_agency_resource_feed import XuzhouAgencyAssetFeed


GUID = "a61e3535-95f2-4711-bfac-7ce438d7ce89"


class FakeHtmlClient:
    def __init__(self, source_id, html_by_name):
        self.source_id = source_id
        self.html_by_name = html_by_name
        self.urls = []

    def fetch(self, url, *, request_name, params=None, headers=None):
        self.urls.append(url)
        return HtmlFetchEnvelope(
            source_id=self.source_id,
            request_name=request_name,
            url=url,
            fetched_at_utc="2026-09-11T00:00:00+00:00",
            http_status=200,
            content_type="text/html; charset=utf-8",
            payload_sha256=("d" if "list" in request_name else "e") * 64,
            encoding="utf-8",
            html=self.html_by_name[request_name],
        )


class XuzhouAgencyAssetFeedTests(unittest.TestCase):
    def _list_html(self):
        return f"""<html><body><table><tr><td>
        <a href='/jyxx/tradeInfo.html?BiaoDuanGuid={GUID}'>
        江苏徐州睢宁县沙集物流园一期4#厂房招租项目公告(国资监测编号GR2026JS4000001)
        </a></td><td>e交易</td><td>徐州淮海产权服务有限公司</td><td>2026-08-20</td></tr></table></body></html>"""

    def _detail_html(self):
        return """<html><head><title>江苏省公共资源交易网</title></head><body>
        <h1>江苏徐州睢宁县沙集物流园一期4#厂房招租项目</h1>
        <p>信息发布时间：2026-08-20 08:00:00 来源：徐州市公共资源交易电子服务平台</p>
        <p>交易机构：徐州淮海产权服务有限公司</p>
        <p>项目名称 江苏徐州睢宁县沙集物流园一期4#厂房招租项目 项目编号 HHCQ2026ZL1841A</p>
        <p>挂牌起始日期 2026-08-20 挂牌截止日期 2026-09-02</p>
        <p>标的坐落 江苏徐州睢宁县沙集镇电沙路东侧、园二路南侧</p>
        <p>房屋现状 标的状态 空置 是否设置原承租人优先权 否</p>
        <p>租金底价 893792.00元/年</p>
        <p>出租方名称：江苏宁通投资发展集团有限公司</p>
        </body></html>"""

    def test_discovers_legacy_guid_and_constructs_official_mirror(self):
        discovery_client = FakeHtmlClient(
            "XZ_GGZY_AGENCY_LIST", {"xz_ggzy.agency_assets.list": self._list_html()}
        )
        feed = XuzhouAgencyAssetFeed(
            discovery_client=discovery_client,
            mirror_client=FakeHtmlClient("JS_GGZY_XZ_MIRROR", {}),
        )
        result = feed.discover_recent(limit=5)
        self.assertEqual(result["item_count"], 1)
        item = result["items"][0]
        self.assertEqual(item["legacy_guid"], GUID)
        self.assertEqual(item["publication_date"], "2026-08-20")
        self.assertEqual(item["listing_mode"], "LEASE")
        self.assertEqual(item["detail_source"], "JS_GGZY_MIRROR")
        self.assertEqual(
            item["mirror_url"],
            f"https://jsggzy.jszwfw.gov.cn/jyxx/003006/003006001/20260820/{GUID}.html",
        )

    def test_mirror_detail_promotes_only_explicit_underuse(self):
        discovery_client = FakeHtmlClient(
            "XZ_GGZY_AGENCY_LIST", {"xz_ggzy.agency_assets.list": self._list_html()}
        )
        mirror_client = FakeHtmlClient(
            "JS_GGZY_XZ_MIRROR",
            {"js_ggzy.xuzhou_asset_mirror.detail": self._detail_html()},
        )
        feed = XuzhouAgencyAssetFeed(
            discovery_client=discovery_client,
            mirror_client=mirror_client,
        )
        result = feed.collect_recent(limit=5)
        self.assertEqual(result["listing_count"], 1)
        self.assertEqual(result["error_count"], 0)
        listing = result["listings"][0]
        self.assertTrue(listing["source_origin_verified"])
        self.assertEqual(listing["resource_state"], "DISCOVERED")
        self.assertEqual(listing["underuse_evidence_state"], "OBSERVED")
        self.assertIn("空置", listing["underuse_excerpt"])
        self.assertEqual(listing["asking_price_rmb"], "893792.00")
        self.assertEqual(listing["owner_actor"], "江苏宁通投资发展集团有限公司")

    def test_non_xuzhou_mirror_is_rejected(self):
        discovery_client = FakeHtmlClient(
            "XZ_GGZY_AGENCY_LIST", {"xz_ggzy.agency_assets.list": self._list_html()}
        )
        mirror_client = FakeHtmlClient(
            "JS_GGZY_XZ_MIRROR",
            {
                "js_ggzy.xuzhou_asset_mirror.detail": """<html><body>
                <h1>其他城市资产招租</h1><p>来源：其他市交易平台</p>
                </body></html>"""
            },
        )
        feed = XuzhouAgencyAssetFeed(
            discovery_client=discovery_client,
            mirror_client=mirror_client,
        )
        result = feed.collect_recent(limit=5)
        self.assertEqual(result["listing_count"], 0)
        self.assertEqual(result["error_count"], 1)
        self.assertIn("not verified as Xuzhou-origin", result["errors"][0]["error"])


if __name__ == "__main__":
    unittest.main()
