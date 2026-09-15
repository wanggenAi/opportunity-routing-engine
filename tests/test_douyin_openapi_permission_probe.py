import hashlib
import unittest

from src.douyin_openapi_permission_probe import (
    FREE_QUOTA_URL,
    PAYMENT_URL,
    PERMISSION_URL,
    collect_douyin_openapi_permission_evidence,
)
from src.html_ingest import HtmlFetchEnvelope


PERMISSION_HTML = """
<html><body><table><tr><td>搜索管理</td><td>关键词视频管理</td>
<td>包含通过关键词获取抖音视频及该视频下评论，并进行回复的能力</td>
<td>video.search</td><td>特殊权限</td><td>默认关闭</td><td>管理中心申请</td></tr></table></body></html>
"""
QUOTA_HTML = """
<html><body><p>免费额度用完后，会在次日8点更新，如：视频发布及管理scope中的video.list接口每日免费额度为1000。</p></body></html>
"""
PAYMENT_HTML = """
<html><body><p>增值流量包套餐是针对开放平台提供的技术服务接口在免费配额基础上提供的付费增值服务。</p></body></html>
"""


class FakeClient:
    def __init__(self, pages):
        self.pages = pages

    def fetch(self, url, *, request_name, params=None, headers=None):
        html = self.pages[url]
        raw = html.encode("utf-8")
        return HtmlFetchEnvelope(
            source_id="DOUYIN_OPENAPI",
            request_name=request_name,
            url=url,
            fetched_at_utc="2026-09-15T00:00:00+00:00",
            http_status=200,
            content_type="text/html; charset=utf-8",
            payload_sha256=hashlib.sha256(raw).hexdigest(),
            encoding="utf-8",
            html=html,
        )


class DouyinOpenApiPermissionProbeTests(unittest.TestCase):
    def _client(self, **overrides):
        pages = {
            PERMISSION_URL: PERMISSION_HTML,
            FREE_QUOTA_URL: QUOTA_HTML,
            PAYMENT_URL: PAYMENT_HTML,
        }
        pages.update(overrides)
        return FakeClient(pages)

    def test_probe_proves_signal_fit_but_keeps_producer_blocked(self):
        result = collect_douyin_openapi_permission_evidence(client=self._client())
        self.assertEqual(result["intended_scope"], "video.search")
        self.assertEqual(
            result["signal_fit"],
            "KEYWORD_VIDEO_AND_COMMENT_DISCOVERY_SUPPORTED_BY_OFFICIAL_DOCS",
        )
        self.assertEqual(result["permission_class"], "SPECIAL_PERMISSION")
        self.assertEqual(result["permission_default_state"], "DEFAULT_OFF")
        self.assertEqual(result["permission_application_route"], "MANAGEMENT_CENTER_APPLICATION")
        self.assertFalse(result["producer_trial_allowed"])
        self.assertEqual(result["application_approval_status"], "NOT_ESTABLISHED")
        self.assertEqual(
            result["intended_scope_free_quota_amount_status"],
            "NOT_ESTABLISHED_FROM_PUBLIC_DOCS",
        )
        self.assertEqual(result["zero_incremental_fee_condition"], "NOT_ESTABLISHED")
        self.assertIn("APPLICATION_APPROVAL_NOT_ESTABLISHED", result["blockers"])
        self.assertIn("VIDEO_SEARCH_FREE_QUOTA_NOT_PUBLICLY_ESTABLISHED", result["blockers"])

    def test_each_excerpt_is_bound_to_official_document_text_and_hash(self):
        result = collect_douyin_openapi_permission_evidence(client=self._client())
        self.assertEqual(len(result["documents"]), 3)
        for document in result["documents"]:
            excerpt = document["evidence"]["excerpt"]
            self.assertIn(excerpt, document["normalized_document_text"])
            self.assertEqual(
                document["evidence"]["excerpt_sha256"],
                hashlib.sha256(excerpt.encode("utf-8")).hexdigest(),
            )
            self.assertEqual(document["page_provenance"]["source_id"], "DOUYIN_OPENAPI")
            self.assertEqual(document["page_provenance"]["url"], document["source_url"])

    def test_missing_special_permission_marker_fails_closed(self):
        broken = PERMISSION_HTML.replace("特殊权限", "")
        with self.assertRaisesRegex(ValueError, "特殊权限"):
            collect_douyin_openapi_permission_evidence(
                client=self._client(**{PERMISSION_URL: broken})
            )

    def test_missing_paid_extension_boundary_fails_closed(self):
        broken = PAYMENT_HTML.replace("付费增值服务", "普通服务")
        with self.assertRaisesRegex(ValueError, "paid extension"):
            collect_douyin_openapi_permission_evidence(
                client=self._client(**{PAYMENT_URL: broken})
            )

    def test_free_quota_for_other_scope_never_promotes_video_search_quota(self):
        result = collect_douyin_openapi_permission_evidence(client=self._client())
        self.assertEqual(result["free_quota_policy_status"], "PLATFORM_FREE_QUOTA_EXISTS")
        self.assertEqual(
            result["intended_scope_free_quota_amount_status"],
            "NOT_ESTABLISHED_FROM_PUBLIC_DOCS",
        )
        self.assertFalse(result["producer_trial_allowed"])


if __name__ == "__main__":
    unittest.main()
