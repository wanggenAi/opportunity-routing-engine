"""Bounded public-doc probe for Douyin OpenAPI permission feasibility.

This producer does not call Douyin APIs and never uses credentials. It fetches only
public official documentation from ``open.douyin.com`` to determine whether the
currently registered ``DOUYIN_OPENAPI`` path is safe to advance from permission
validation into an automated producer trial.

The conclusion is intentionally fail-closed: a relevant official scope may exist
without being granted to our application, and a platform may publish free quota
without publicly establishing the free quota for the exact scope we need.
"""

from __future__ import annotations

import hashlib
from typing import Any

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace


SOURCE_ID = "DOUYIN_OPENAPI"
HOST = "open.douyin.com"
PERMISSION_URL = (
    "https://open.douyin.com/platform/resource/docs/accession-guide/type-and-permission"
)
FREE_QUOTA_URL = (
    "https://open.douyin.com/platform/resource/docs/common-question/free-quota-common-question"
)
PAYMENT_URL = (
    "https://open.douyin.com/platform/resource/docs/common-question/payment-common-question/"
)


def _flat(text: str) -> str:
    return normalize_whitespace(text)


def _window(text: str, anchor: str, *, radius: int = 900) -> str:
    flat = _flat(text)
    index = flat.find(anchor)
    if index < 0:
        raise ValueError(f"official documentation missing anchor: {anchor}")
    start = max(0, index - radius)
    end = min(len(flat), index + len(anchor) + radius)
    return flat[start:end].strip()


def _excerpt_record(text: str, anchor: str) -> dict[str, str]:
    excerpt = _window(text, anchor)
    return {
        "anchor": anchor,
        "excerpt": excerpt,
        "excerpt_sha256": hashlib.sha256(excerpt.encode("utf-8")).hexdigest(),
    }


def _fetch_document(client: PublicHtmlClient, url: str, request_name: str) -> tuple[dict[str, Any], dict[str, Any]]:
    envelope = client.fetch(url, request_name=request_name)
    document = html_to_document(envelope.html, base_url=envelope.url)
    text = document.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"official documentation produced no public text: {request_name}")
    return envelope.metadata(), document


def collect_douyin_openapi_permission_evidence(
    *, client: PublicHtmlClient | None = None,
) -> dict[str, Any]:
    client = client or PublicHtmlClient(
        source_id=SOURCE_ID,
        allowed_hosts={HOST},
        timeout_seconds=20.0,
        retries=2,
        max_response_bytes=4_000_000,
    )

    permission_meta, permission_doc = _fetch_document(
        client, PERMISSION_URL, "douyin-openapi-permission-overview"
    )
    quota_meta, quota_doc = _fetch_document(
        client, FREE_QUOTA_URL, "douyin-openapi-free-quota-faq"
    )
    payment_meta, payment_doc = _fetch_document(
        client, PAYMENT_URL, "douyin-openapi-payment-faq"
    )

    permission_text = _flat(str(permission_doc["text"]))
    quota_text = _flat(str(quota_doc["text"]))
    payment_text = _flat(str(payment_doc["text"]))

    permission_markers = (
        "关键词视频管理",
        "video.search",
        "特殊权限",
        "默认关闭",
        "管理中心申请",
    )
    for marker in permission_markers:
        if marker not in permission_text:
            raise ValueError(f"permission overview no longer proves required marker: {marker}")
    if "通过关键词获取抖音视频" not in permission_text or "评论" not in permission_text:
        raise ValueError("permission overview no longer proves keyword-video/comment signal fit")

    for marker in ("免费额度用完后", "次日8点更新", "video.list", "1000"):
        if marker not in quota_text:
            raise ValueError(f"free-quota FAQ no longer proves required marker: {marker}")

    if "免费配额基础上" not in payment_text or "付费增值服务" not in payment_text:
        raise ValueError("payment FAQ no longer proves paid extension after free quota")

    documents = [
        {
            "document_role": "PERMISSION_OVERVIEW",
            "source_url": PERMISSION_URL,
            "page_provenance": permission_meta,
            "normalized_document_text": permission_text,
            "evidence": _excerpt_record(permission_text, "关键词视频管理"),
        },
        {
            "document_role": "FREE_QUOTA_POLICY",
            "source_url": FREE_QUOTA_URL,
            "page_provenance": quota_meta,
            "normalized_document_text": quota_text,
            "evidence": _excerpt_record(quota_text, "免费额度用完后"),
        },
        {
            "document_role": "PAID_EXTENSION_POLICY",
            "source_url": PAYMENT_URL,
            "page_provenance": payment_meta,
            "normalized_document_text": payment_text,
            "evidence": _excerpt_record(payment_text, "增值流量包套餐"),
        },
    ]

    return {
        "schema_version": "douyin-openapi-permission-probe.v1",
        "source_id": SOURCE_ID,
        "intended_scope": "video.search",
        "signal_fit": "KEYWORD_VIDEO_AND_COMMENT_DISCOVERY_SUPPORTED_BY_OFFICIAL_DOCS",
        "permission_class": "SPECIAL_PERMISSION",
        "permission_default_state": "DEFAULT_OFF",
        "permission_application_route": "MANAGEMENT_CENTER_APPLICATION",
        "application_approval_status": "NOT_ESTABLISHED",
        "free_quota_policy_status": "PLATFORM_FREE_QUOTA_EXISTS",
        "intended_scope_free_quota_amount_status": "NOT_ESTABLISHED_FROM_PUBLIC_DOCS",
        "paid_extension_status": "PAID_EXTENSION_EXISTS_AFTER_FREE_QUOTA",
        "zero_incremental_fee_condition": "NOT_ESTABLISHED",
        "producer_trial_allowed": False,
        "blockers": [
            "VIDEO_SEARCH_SPECIAL_PERMISSION_DEFAULT_OFF",
            "APPLICATION_APPROVAL_NOT_ESTABLISHED",
            "VIDEO_SEARCH_FREE_QUOTA_NOT_PUBLICLY_ESTABLISHED",
            "ZERO_INCREMENTAL_FEE_CONDITION_NOT_ESTABLISHED",
        ],
        "documents": documents,
        "truth_boundaries": [
            "OFFICIAL_SCOPE_EXISTS_NE_SCOPE_GRANTED",
            "DEFAULT_OFF_NE_PERMISSION_GRANTED",
            "FREE_QUOTA_EXISTS_NE_TARGET_SCOPE_FREE_QUOTA_PROVEN",
            "FREE_QUOTA_NE_ZERO_INCREMENTAL_COST_GUARANTEE",
            "PAID_EXTENSION_EXISTS_NE_PERMISSION_TO_BUY",
            "KEYWORD_VIDEO_DISCOVERY_NE_MARKET_DEMAND",
            "COMMENTS_NE_PAID_NEED",
            "PERMISSION_EVIDENCE_NE_SOURCE_ACTIVATION",
            "UNKNOWN_NE_PASS",
        ],
    }
