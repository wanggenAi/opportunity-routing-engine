import hashlib
import unittest

from src.questmobile_public_research import (
    INDEX_URL,
    QuestMobilePublicResearchCollector,
)


class FakeEnvelope:
    def __init__(self, url, html, *, source_id="QM"):
        self.url = url
        self.html = html
        self.source_id = source_id

    def metadata(self):
        return {
            "source_id": self.source_id,
            "request_name": "fake",
            "url": self.url,
            "fetched_at_utc": "2026-09-15T12:00:00+00:00",
            "http_status": 200,
            "content_type": "text/html; charset=utf-8",
            "payload_sha256": hashlib.sha256(self.html.encode("utf-8")).hexdigest(),
            "encoding": "utf-8",
        }


class FakeClient:
    def __init__(self, mapping):
        self.mapping = mapping

    def fetch(self, url, *, request_name, params=None, headers=None):
        return FakeEnvelope(url, self.mapping[url])


TITLE_1 = "QuestMobile2026 中国移动互联网半年报告：结构变化测试"
TITLE_2 = "QuestAuto 2026年新能源汽车市场发展半年报：测试"
URL_1 = "https://www.questmobile.com.cn/research/report/2084487578531254273/"
URL_2 = "https://www.questmobile.com.cn/research/report/2084000000000000000/"

INDEX = f"""
<html><body>
<a href='/research/report/2084487578531254273'>{TITLE_1}</a>
<a href='/research/report/2084487578531254273/'>{TITLE_1}</a>
<a href='/research/report/2084000000000000000/'>{TITLE_2}</a>
<a href='https://evil.example/research/report/1/'>Not governed</a>
</body></html>
"""

DETAIL_1 = f"""
<html><body>
<div>热门报告</div><div>2026-07-29</div>
<h1>{TITLE_1}</h1>
<div>行业：生活服务|移动购物</div>
<div>关键词：半年报告</div>
<div>2026-08-04</div>
<div>来源：QuestMobile研究院</div>
<p>QuestMobile数据显示，截止到2026年6月，全网月活跃用户规模达到12.82亿，同比增长1.2%。</p>
<p>普通分析文字，不作为 source-native data finding。</p>
<p>QuestMobile数据显示，2026年6月，三线及以下用户比例过半。</p>
</body></html>
"""

DETAIL_2 = f"""
<html><body>
<h1>{TITLE_2}</h1>
<div>行业：汽车品牌</div>
<div>2026-07-29</div>
<div>来源：QuestMobile研究院</div>
<p>QuestAuto数据显示，新能源活跃量继续增长。</p>
</body></html>
"""


class QuestMobilePublicResearchTests(unittest.TestCase):
    def _collector(self, *, detail1=DETAIL_1, detail2=DETAIL_2):
        return QuestMobilePublicResearchCollector(
            client=FakeClient({
                INDEX_URL: INDEX,
                URL_1: detail1,
                URL_2: detail2,
            })
        )

    def test_collect_binds_public_report_metadata_and_exact_findings(self):
        payload = self._collector().collect(report_limit=2)
        self.assertEqual(payload["schema_version"], "questmobile-public-research.v1")
        self.assertEqual(payload["source_id"], "QM")
        self.assertEqual(payload["report_count"], 2)
        self.assertEqual(payload["text_finding_count"], 3)

        first = payload["reports"][0]
        self.assertEqual(first["report_id"], "2084487578531254273")
        self.assertEqual(first["publication_date"], "2026-08-04")
        self.assertEqual(first["source_authority"], "QuestMobile研究院")
        self.assertEqual(first["category_text"], "生活服务|移动购物")
        self.assertEqual(first["finding_count"], 2)
        self.assertEqual(first["finding_evidence_state"], "TEXT_FINDINGS_OBSERVED")
        for finding in first["findings"]:
            self.assertEqual(
                finding["excerpt_sha256"],
                hashlib.sha256(finding["excerpt"].encode("utf-8")).hexdigest(),
            )
        self.assertIn("RESEARCH_REPORT_NE_CURRENT_LOCAL_REALITY", payload["truth_boundaries"])
        self.assertIn("RESEARCH_FINDING_NE_PAID_DEMAND", payload["truth_boundaries"])

    def test_date_is_scoped_after_main_title_not_hot_report_navigation(self):
        payload = self._collector().collect(report_limit=1)
        self.assertEqual(payload["reports"][0]["publication_date"], "2026-08-04")

    def test_duplicate_and_foreign_report_links_do_not_expand_scope(self):
        payload = self._collector().collect(report_limit=10)
        self.assertEqual([row["source_url"] for row in payload["reports"]], [URL_1, URL_2])

    def test_questauto_source_native_findings_are_preserved_without_relabeling(self):
        payload = self._collector().collect(report_limit=2)
        finding = payload["reports"][1]["findings"][0]
        self.assertEqual(finding["attribution"], "QuestAuto")
        self.assertTrue(finding["excerpt"].startswith("QuestAuto数据显示"))

    def test_report_with_no_text_finding_remains_explicit_unknown_state(self):
        no_finding = DETAIL_2.replace(
            "<p>QuestAuto数据显示，新能源活跃量继续增长。</p>",
            "<p>数据仅存在于图片中。</p>",
        )
        payload = self._collector(detail2=no_finding).collect(report_limit=2)
        second = payload["reports"][1]
        self.assertEqual(second["finding_evidence_state"], "NO_TEXT_FINDING")
        self.assertEqual(second["finding_count"], 0)
        self.assertEqual(second["findings"], [])

    def test_title_anchor_drift_fails_closed(self):
        drifted = DETAIL_1.replace(f"<h1>{TITLE_1}</h1>", "<h1>Different title</h1>")
        with self.assertRaisesRegex(ValueError, "title anchor"):
            self._collector(detail1=drifted).collect(report_limit=1)

    def test_source_authority_drift_fails_closed(self):
        drifted = DETAIL_1.replace("来源：QuestMobile研究院", "来源：Unknown")
        with self.assertRaisesRegex(ValueError, "source authority drifted"):
            self._collector(detail1=drifted).collect(report_limit=1)

    def test_report_limit_is_bounded(self):
        for value in (0, 11, True):
            with self.assertRaisesRegex(ValueError, "report_limit"):
                self._collector().collect(report_limit=value)


if __name__ == "__main__":
    unittest.main()
