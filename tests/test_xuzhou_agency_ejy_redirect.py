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

    def _feed(self, detail_html=None):
        return XuzhouAgencyAssetFeed(
            discovery_client=FakeHtmlClient(
                "XZ_GGZY_AGENCY_LIST",
                {"xz_ggzy.agency_assets.list": self._official_list()},
            ),
            ejy_client=FakeHtmlClient(
                "EJY365_XZ_LINKED",
                {} if detail_html is None else {"ejy365.xuzhou_linked_asset.detail": detail_html},
            ),
            mirror_client=FakeHtmlClient("JS_GGZY_XZ_MIRROR", {}),
        )

    def test_current_official_onclick_redirect_is_discovered(self):
        discovery = self._feed().discover_recent(limit=5)
        self.assertEqual(discovery["item_count"], 1)
        item = discovery["items"][0]
        self.assertEqual(item["external_project_url"], "https://www.ejy365.com/info/ejy423718")
        self.assertEqual(item["monitoring_code"], "GR2026JS4002661-2")
        self.assertEqual(item["publication_date"], "2026-09-10")
        self.assertEqual(item["publisher_actor"], "徐州淮海产权服务有限公司")
        self.assertEqual(item["listing_round"], 2)
        self.assertTrue(item["relisting_observed"])

    def test_linked_ejy_detail_enriches_but_stays_discovered(self):
        result = self._feed(self._ejy_detail()).collect_recent(limit=5)
        self.assertEqual(result["listing_count"], 1)
        self.assertEqual(result["error_count"], 0)
        listing = result["listings"][0]
        self.assertEqual(listing["resource_state"], "DISCOVERED")
        self.assertEqual(listing["underuse_evidence_state"], "OBSERVED")
        self.assertIn("空置", listing["underuse_excerpt"])
        self.assertEqual(listing["asking_price_rmb"], "120000.00")
        self.assertEqual(listing["monitoring_code"], "GR2026JS4002661-2")
        self.assertEqual(listing["owner_actor"], "徐州市某国有公司")
        self.assertEqual(listing["location"], "江苏省徐州市鼓楼区")
        self.assertEqual(listing["listing_mode"], "LEASE")
        self.assertTrue(listing["source_origin_verified"])

    def test_disclaimer_mention_does_not_override_real_owner_field(self):
        detail = self._ejy_detail().replace(
            "<p>挂牌方：徐州市某国有公司</p>",
            """<p>本平台不对挂牌方和/或招标方的相关资质进行审核。项目公告以及相关信息均由挂牌方、招标方自行负责发布，并承担相应法律责任。</p>
            <p>挂牌方：徐州市真实产权方有限公司</p>""",
        )
        result = self._feed(detail).collect_recent(limit=5)
        self.assertEqual(result["error_count"], 0)
        self.assertEqual(result["listings"][0]["owner_actor"], "徐州市真实产权方有限公司")

    def test_transfer_title_wins_over_unrelated_lease_boilerplate_and_idle_title_is_observed(self):
        list_html = self._official_list().replace(
            "江苏徐州鼓楼区城市花园1#-109房产招租(二次挂牌)项目公告(国资监测编号GR2026JS4002661-2)",
            "一批观光电瓶车、空调、音响等闲置资产整体转让项目(八次挂牌)公告(国资监测编号GR2026JS4002661-2)",
        )
        detail = """<html><head><title>e交易</title></head><body>
        <h1>一批观光电瓶车、空调、音响等闲置资产整体转让项目(八次挂牌)公告(国资监测编号GR2026JS4002661-2)</h1>
        <p>国资监测编号GR2026JS4002661-2</p>
        <p>平台说明：其他招租、出租项目规则以各自公告为准。</p>
        <p>转让方名称：徐州市某资产经营有限公司</p>
        <p>挂牌价 41200.00元</p>
        </body></html>"""
        feed = XuzhouAgencyAssetFeed(
            discovery_client=FakeHtmlClient(
                "XZ_GGZY_AGENCY_LIST",
                {"xz_ggzy.agency_assets.list": list_html},
            ),
            ejy_client=FakeHtmlClient(
                "EJY365_XZ_LINKED",
                {"ejy365.xuzhou_linked_asset.detail": detail},
            ),
            mirror_client=FakeHtmlClient("JS_GGZY_XZ_MIRROR", {}),
        )
        result = feed.collect_recent(limit=5)
        self.assertEqual(result["error_count"], 0)
        listing = result["listings"][0]
        self.assertEqual(listing["listing_mode"], "TRANSFER")
        self.assertEqual(listing["owner_actor"], "徐州市某资产经营有限公司")
        self.assertEqual(listing["underuse_evidence_state"], "OBSERVED")
        self.assertIn("闲置", listing["underuse_excerpt"])

    def test_monitoring_code_mismatch_is_not_silently_joined(self):
        bad_detail = self._ejy_detail().replace("GR2026JS4002661-2", "GR2026JS4999999")
        result = self._feed(bad_detail).collect_recent(limit=5)
        self.assertEqual(result["listing_count"], 0)
        self.assertEqual(result["error_count"], 1)
        self.assertIn("does not match", result["errors"][0]["error"])


if __name__ == "__main__":
    unittest.main()
