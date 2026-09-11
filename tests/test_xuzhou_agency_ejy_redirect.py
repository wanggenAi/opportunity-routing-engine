import unittest

from src.html_ingest import HtmlFetchEnvelope
from src.xuzhou_agency_resource_feed import XuzhouAgencyAssetFeed


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
            payload_sha256=("a" if "list" in request_name else "b") * 64,
            encoding="utf-8",
            html=self.html_by_name[request_name],
        )


class XuzhouAgencyEjyRedirectTests(unittest.TestCase):
    def _official_list(self):
        return """<html><body><table>
        <tr class="ewb-trade-tr">
          <td class="ewb-trade-td td-index"></td>
          <td class="ewb-trade-td"><a
            onclick="confirm('跳转')?location.href='https://www.ejy365.com/info/ejy423718':''"
            href="javascript:;"
            title="江苏徐州鼓楼区城市花园1#-109房产招租(二次挂牌)项目公告(国资监测编号GR2026JS4002661-2)">项目</a></td>
          <td class="ewb-trade-td">e交易</td>
          <td class="ewb-trade-td">徐州淮海产权服务有限公司</td>
          <td class="ewb-trade-td">2026-09-10</td>
        </tr></table></body></html>"""

    def _ejy_detail(self):
        return """<html><head><title>e交易</title></head><body>
        <h1>江苏徐州鼓楼区城市花园1#-109房产招租(二次挂牌)项目公告(国资监测编号GR2026JS4002661-2)</h1>
        <p>国资监测编号GR2026JS4002661-2</p>
        <p>挂牌价 120000.00元</p>
        <p>报名开始时间：2026-09-10 09:00:00</p>
        <p>报名截止时间：2026-09-24 17:00:00</p>
        <p>挂牌方：徐州市某国有公司</p>
        <p>房屋现状 标的状态 空置</p>
        <p>标的所在地：江苏省徐州市鼓楼区</p>
        </body></html>"""

    def test_current_official_onclick_redirect_is_discovered(self):
        feed = XuzhouAgencyAssetFeed(
            discovery_client=FakeHtmlClient(
                "XZ_GGZY_AGENCY_LIST",
                {"xz_ggzy.agency_assets.list": self._official_list()},
            ),
            ejy_client=FakeHtmlClient("EJY365_XZ_LINKED", {}),
            mirror_client=FakeHtmlClient("JS_GGZY_XZ_MIRROR", {}),
        )
        discovery = feed.discover_recent(limit=5)
        self.assertEqual(discovery["item_count"], 1)
        item = discovery["items"][0]
        self.assertEqual(item["external_project_url"], "https://www.ejy365.com/info/ejy423718")
        self.assertEqual(item["monitoring_code"], "GR2026JS4002661-2")
        self.assertEqual(item["publication_date"], "2026-09-10")
        self.assertEqual(item["publisher_actor"], "徐州淮海产权服务有限公司")
        self.assertEqual(item["listing_round"], 2)
        self.assertTrue(item["relisting_observed"])

    def test_linked_ejy_detail_enriches_but_stays_discovered(self):
        feed = XuzhouAgencyAssetFeed(
            discovery_client=FakeHtmlClient(
                "XZ_GGZY_AGENCY_LIST",
                {"xz_ggzy.agency_assets.list": self._official_list()},
            ),
            ejy_client=FakeHtmlClient(
                "EJY365_XZ_LINKED",
                {"ejy365.xuzhou_linked_asset.detail": self._ejy_detail()},
            ),
            mirror_client=FakeHtmlClient("JS_GGZY_XZ_MIRROR", {}),
        )
        result = feed.collect_recent(limit=5)
        self.assertEqual(result["listing_count"], 1)
        self.assertEqual(result["error_count"], 0)
        listing = result["listings"][0]
        self.assertEqual(listing["resource_state"], "DISCOVERED")
        self.assertEqual(listing["underuse_evidence_state"], "OBSERVED")
        self.assertIn("空置", listing["underuse_excerpt"])
        self.assertEqual(listing["asking_price_rmb"], "120000.00")
        self.assertEqual(listing["monitoring_code"], "GR2026JS4002661-2")
        self.assertTrue(listing["source_origin_verified"])

    def test_monitoring_code_mismatch_is_not_silently_joined(self):
        bad_detail = self._ejy_detail().replace("GR2026JS4002661-2", "GR2026JS4999999")
        feed = XuzhouAgencyAssetFeed(
            discovery_client=FakeHtmlClient(
                "XZ_GGZY_AGENCY_LIST",
                {"xz_ggzy.agency_assets.list": self._official_list()},
            ),
            ejy_client=FakeHtmlClient(
                "EJY365_XZ_LINKED",
                {"ejy365.xuzhou_linked_asset.detail": bad_detail},
            ),
            mirror_client=FakeHtmlClient("JS_GGZY_XZ_MIRROR", {}),
        )
        result = feed.collect_recent(limit=5)
        self.assertEqual(result["listing_count"], 0)
        self.assertEqual(result["error_count"], 1)
        self.assertIn("does not match", result["errors"][0]["error"])


if __name__ == "__main__":
    unittest.main()
