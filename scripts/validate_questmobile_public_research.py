#!/usr/bin/env python3
"""Fail-closed validator for public QuestMobile research evidence artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse


SOURCE_ID = "QM"
SCHEMA_VERSION = "questmobile-public-research.v1"
HOST = "www.questmobile.com.cn"
REQUIRED_BOUNDARIES = {
    "PUBLIC_REPORT_PAGE_ONLY",
    "NO_LOGIN_OR_PAID_DATABASE",
    "NO_OCR_OR_IMAGE_METRIC_EXTRACTION",
    "NO_TEXT_FINDING_NE_ZERO",
    "RESEARCH_REPORT_NE_CURRENT_LOCAL_REALITY",
    "REPORTED_SAMPLE_OR_PANEL_NE_CENSUS",
    "RESEARCH_FINDING_NE_PAID_DEMAND",
    "RESEARCH_FINDING_NE_PAYER",
    "RESEARCH_FINDING_NE_PAYMENT",
    "RESEARCH_FINDING_NE_OPPORTUNITY",
    "EXACT_EXCERPT_REQUIRED",
    "UNKNOWN_NE_PASS",
}


def _mapping(value: object, field: str) -> dict:
    if not isinstance(value, dict):
        raise SystemExit(f"{field} must be an object")
    return value


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"{field} is required")
    return value.strip()


def _sha256(value: object, field: str) -> str:
    digest = _text(value, field).lower()
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise SystemExit(f"{field} must be a SHA-256 hex digest")
    return digest


def _official_report_url(value: object, field: str, report_id: str) -> str:
    url = _text(value, field)
    parsed = urlparse(url)
    expected_path = f"/research/report/{report_id}/"
    if parsed.scheme != "https" or parsed.hostname != HOST or parsed.path != expected_path:
        raise SystemExit(f"{field} must be the canonical QuestMobile report URL")
    return url


def _official_index_url(value: object, field: str) -> str:
    url = _text(value, field)
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != HOST or parsed.path.rstrip("/") != "/research/report-list":
        raise SystemExit(f"{field} must be the public QuestMobile report index")
    return url


def _iso_date(value: object, field: str) -> str:
    text = _text(value, field)
    try:
        date.fromisoformat(text)
    except ValueError as exc:
        raise SystemExit(f"{field} must be an ISO date") from exc
    return text


def _aware_time(value: object, field: str) -> str:
    text = _text(value, field)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SystemExit(f"{field} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise SystemExit(f"{field} must be timezone-aware")
    return text


def validate(payload: dict) -> dict:
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise SystemExit("unsupported QuestMobile research schema")
    if payload.get("source_id") != SOURCE_ID:
        raise SystemExit("unexpected QuestMobile source_id")
    if payload.get("data_available") is not True:
        raise SystemExit("QuestMobile public research artifact has no available data")
    if payload.get("collection_scope") != "LATEST_PUBLIC_RESEARCH_REPORTS_ONLY":
        raise SystemExit("QuestMobile collection scope drifted")

    report_limit = payload.get("report_limit")
    if isinstance(report_limit, bool) or not isinstance(report_limit, int) or not 1 <= report_limit <= 10:
        raise SystemExit("QuestMobile report_limit is invalid")
    reports = payload.get("reports")
    if not isinstance(reports, list) or not reports:
        raise SystemExit("QuestMobile reports are required")
    report_count = payload.get("report_count")
    if isinstance(report_count, bool) or not isinstance(report_count, int) or report_count != len(reports):
        raise SystemExit("QuestMobile report_count diverges from reports")
    if report_count > report_limit:
        raise SystemExit("QuestMobile report_count exceeds report_limit")

    provenance = _mapping(payload.get("provenance"), "provenance")
    index_meta = _mapping(provenance.get("index"), "provenance.index")
    if index_meta.get("source_id") != SOURCE_ID:
        raise SystemExit("QuestMobile index provenance source_id drifted")
    _official_index_url(index_meta.get("url"), "provenance.index.url")
    _sha256(index_meta.get("payload_sha256"), "provenance.index.payload_sha256")
    _aware_time(index_meta.get("fetched_at_utc"), "provenance.index.fetched_at_utc")

    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    total_findings = 0
    no_text_finding_reports = 0
    for report_index, raw_report in enumerate(reports):
        report = _mapping(raw_report, f"reports[{report_index}]")
        if report.get("source_id") != SOURCE_ID:
            raise SystemExit("QuestMobile report source_id drifted")
        report_id = _text(report.get("report_id"), f"reports[{report_index}].report_id")
        if not report_id.isdigit():
            raise SystemExit("QuestMobile report_id must be numeric")
        if report_id in seen_ids:
            raise SystemExit(f"duplicate QuestMobile report_id: {report_id}")
        seen_ids.add(report_id)
        _text(report.get("title"), f"reports[{report_index}].title")
        _iso_date(report.get("publication_date"), f"reports[{report_index}].publication_date")
        if report.get("source_authority") != "QuestMobile研究院":
            raise SystemExit("QuestMobile source authority drifted")

        source_url = _official_report_url(
            report.get("source_url"), f"reports[{report_index}].source_url", report_id
        )
        if source_url in seen_urls:
            raise SystemExit(f"duplicate QuestMobile report URL: {source_url}")
        seen_urls.add(source_url)

        page_hash = _sha256(
            report.get("provenance_sha256"), f"reports[{report_index}].provenance_sha256"
        )
        detail_meta = _mapping(report.get("provenance"), f"reports[{report_index}].provenance")
        if detail_meta.get("source_id") != SOURCE_ID:
            raise SystemExit("QuestMobile detail provenance source_id drifted")
        if _official_report_url(
            detail_meta.get("url"), f"reports[{report_index}].provenance.url", report_id
        ) != source_url:
            raise SystemExit("QuestMobile detail provenance URL diverges from report URL")
        if _sha256(
            detail_meta.get("payload_sha256"),
            f"reports[{report_index}].provenance.payload_sha256",
        ) != page_hash:
            raise SystemExit("QuestMobile report page hash diverges from detail provenance")
        _aware_time(
            detail_meta.get("fetched_at_utc"),
            f"reports[{report_index}].provenance.fetched_at_utc",
        )

        findings = report.get("findings")
        if not isinstance(findings, list):
            raise SystemExit("QuestMobile findings must be an array")
        finding_count = report.get("finding_count")
        if isinstance(finding_count, bool) or not isinstance(finding_count, int) or finding_count != len(findings):
            raise SystemExit("QuestMobile finding_count diverges from findings")
        state = report.get("finding_evidence_state")
        if findings:
            if state != "TEXT_FINDINGS_OBSERVED":
                raise SystemExit("QuestMobile text findings require TEXT_FINDINGS_OBSERVED state")
        else:
            if state != "NO_TEXT_FINDING":
                raise SystemExit("empty QuestMobile findings require NO_TEXT_FINDING state")
            no_text_finding_reports += 1

        seen_finding_ids: set[str] = set()
        seen_excerpts: set[str] = set()
        for finding_index, raw_finding in enumerate(findings):
            finding = _mapping(raw_finding, f"reports[{report_index}].findings[{finding_index}]")
            finding_id = _text(
                finding.get("finding_id"),
                f"reports[{report_index}].findings[{finding_index}].finding_id",
            )
            if finding_id in seen_finding_ids:
                raise SystemExit("duplicate QuestMobile finding_id within report")
            seen_finding_ids.add(finding_id)
            attribution = _text(
                finding.get("attribution"),
                f"reports[{report_index}].findings[{finding_index}].attribution",
            )
            if attribution not in {"QuestMobile", "QuestAuto"}:
                raise SystemExit("unsupported QuestMobile finding attribution")
            excerpt = _text(
                finding.get("excerpt"),
                f"reports[{report_index}].findings[{finding_index}].excerpt",
            )
            if f"{attribution}数据显示" not in excerpt:
                raise SystemExit("QuestMobile finding excerpt is not bound to its attribution")
            if excerpt in seen_excerpts:
                raise SystemExit("duplicate QuestMobile finding excerpt within report")
            seen_excerpts.add(excerpt)
            expected_excerpt_hash = hashlib.sha256(excerpt.encode("utf-8")).hexdigest()
            if _sha256(
                finding.get("excerpt_sha256"),
                f"reports[{report_index}].findings[{finding_index}].excerpt_sha256",
            ) != expected_excerpt_hash:
                raise SystemExit("QuestMobile finding excerpt hash mismatch")
        total_findings += finding_count

    declared_total = payload.get("text_finding_count")
    if isinstance(declared_total, bool) or not isinstance(declared_total, int) or declared_total != total_findings:
        raise SystemExit("QuestMobile text_finding_count diverges from reports")
    if total_findings <= 0:
        raise SystemExit("QuestMobile artifact contains no textual research findings")

    boundaries = payload.get("truth_boundaries")
    if not isinstance(boundaries, list) or not all(isinstance(item, str) for item in boundaries):
        raise SystemExit("QuestMobile truth_boundaries must be an array of strings")
    missing = REQUIRED_BOUNDARIES - set(boundaries)
    if missing:
        raise SystemExit(f"QuestMobile truth boundaries missing: {sorted(missing)}")

    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True).lower()
    forbidden_tokens = (
        '"paid_need"',
        '"payer_confirmed"',
        '"payment_confirmed"',
        '"route_testable"',
        '"opportunity_confirmed"',
        '"business_promotion"',
        '"taxonomy_promotion"',
    )
    if any(token in rendered for token in forbidden_tokens):
        raise SystemExit("QuestMobile artifact leaked downstream commercial or ontology truth")

    return {
        "validated": True,
        "report_count": report_count,
        "text_finding_count": total_findings,
        "no_text_finding_report_count": no_text_finding_reports,
        "report_ids": sorted(seen_ids),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("QuestMobile artifact must contain an object")
    print(json.dumps(validate(payload), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
