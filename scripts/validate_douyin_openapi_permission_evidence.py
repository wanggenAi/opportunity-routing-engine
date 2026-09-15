#!/usr/bin/env python3
"""Fail-closed validation for Douyin OpenAPI public permission evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse


EXPECTED_ROLES = {
    "PERMISSION_OVERVIEW",
    "FREE_QUOTA_POLICY",
    "PAID_EXTENSION_POLICY",
}
EXPECTED_BLOCKERS = {
    "VIDEO_SEARCH_SPECIAL_PERMISSION_DEFAULT_OFF",
    "APPLICATION_APPROVAL_NOT_ESTABLISHED",
    "VIDEO_SEARCH_FREE_QUOTA_NOT_PUBLICLY_ESTABLISHED",
    "ZERO_INCREMENTAL_FEE_CONDITION_NOT_ESTABLISHED",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))

    if data.get("schema_version") != "douyin-openapi-permission-probe.v1":
        raise SystemExit("unsupported permission probe schema")
    if data.get("source_id") != "DOUYIN_OPENAPI":
        raise SystemExit("unexpected source id")
    if data.get("intended_scope") != "video.search":
        raise SystemExit("unexpected intended scope")
    if data.get("signal_fit") != "KEYWORD_VIDEO_AND_COMMENT_DISCOVERY_SUPPORTED_BY_OFFICIAL_DOCS":
        raise SystemExit("signal fit is not established by the expected official scope")
    if data.get("permission_class") != "SPECIAL_PERMISSION" or data.get("permission_default_state") != "DEFAULT_OFF":
        raise SystemExit("special-permission/default-off boundary is missing")
    if data.get("permission_application_route") != "MANAGEMENT_CENTER_APPLICATION":
        raise SystemExit("permission application route is not established")
    if data.get("application_approval_status") != "NOT_ESTABLISHED":
        raise SystemExit("application approval was silently promoted")
    if data.get("intended_scope_free_quota_amount_status") != "NOT_ESTABLISHED_FROM_PUBLIC_DOCS":
        raise SystemExit("video.search free quota was silently invented")
    if data.get("zero_incremental_fee_condition") != "NOT_ESTABLISHED":
        raise SystemExit("zero incremental fee was silently promoted")
    if data.get("producer_trial_allowed") is not False:
        raise SystemExit("permission evidence must not activate a producer trial")
    if set(data.get("blockers", [])) != EXPECTED_BLOCKERS:
        raise SystemExit("permission blockers diverge from fail-closed contract")

    documents = data.get("documents")
    if not isinstance(documents, list) or {x.get("document_role") for x in documents if isinstance(x, dict)} != EXPECTED_ROLES:
        raise SystemExit("official document set is incomplete")
    for document in documents:
        url = document.get("source_url")
        parsed = urlparse(str(url))
        if parsed.scheme != "https" or parsed.hostname != "open.douyin.com":
            raise SystemExit("permission evidence contains a non-official source URL")
        text = document.get("normalized_document_text")
        evidence = document.get("evidence")
        provenance = document.get("page_provenance")
        if not isinstance(text, str) or not text.strip() or not isinstance(evidence, dict) or not isinstance(provenance, dict):
            raise SystemExit("permission document evidence is incomplete")
        excerpt = evidence.get("excerpt")
        digest = evidence.get("excerpt_sha256")
        if not isinstance(excerpt, str) or excerpt not in text:
            raise SystemExit("evidence excerpt is not bound to normalized official text")
        if digest != hashlib.sha256(excerpt.encode("utf-8")).hexdigest():
            raise SystemExit("evidence excerpt hash mismatch")
        page_hash = provenance.get("payload_sha256")
        if not isinstance(page_hash, str) or len(page_hash) != 64:
            raise SystemExit("official page provenance hash is missing")
        if provenance.get("source_id") != "DOUYIN_OPENAPI":
            raise SystemExit("official page provenance source mismatch")
        if provenance.get("url") != url:
            raise SystemExit("official page provenance URL mismatch")

    permission_text = next(x["normalized_document_text"] for x in documents if x["document_role"] == "PERMISSION_OVERVIEW")
    for marker in ("关键词视频管理", "video.search", "特殊权限", "默认关闭", "管理中心申请", "通过关键词获取抖音视频"):
        if marker not in permission_text:
            raise SystemExit(f"permission marker missing: {marker}")
    quota_text = next(x["normalized_document_text"] for x in documents if x["document_role"] == "FREE_QUOTA_POLICY")
    for marker in ("免费额度用完后", "次日8点更新", "video.list", "1000"):
        if marker not in quota_text:
            raise SystemExit(f"quota marker missing: {marker}")
    payment_text = next(x["normalized_document_text"] for x in documents if x["document_role"] == "PAID_EXTENSION_POLICY")
    for marker in ("免费配额基础上", "付费增值服务"):
        if marker not in payment_text:
            raise SystemExit(f"payment marker missing: {marker}")

    forbidden_keys = {"payer", "paid_need", "opportunity", "commercial_score", "source_activated", "production_promoted"}
    def walk(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in forbidden_keys:
                    raise SystemExit(f"permission artifact leaked forbidden field: {key}")
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(data)

    print(json.dumps({"validated": True, "producer_trial_allowed": False, "blockers": sorted(EXPECTED_BLOCKERS)}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
