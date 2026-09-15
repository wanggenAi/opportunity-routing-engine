"""Bounded public QuestMobile research-report ingestion.

Only pages publicly reachable without login are fetched. The collector discovers
report-detail links from QuestMobile's public research index, preserves exact page
provenance, and retains source-native textual findings without converting them into
market-demand, payer, transaction or opportunity truth.

Images/charts are not OCR'd here. A public report can therefore be retained with
`NO_TEXT_FINDING` when its useful evidence is image-only; that state is not zero and
is not silently promoted.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace


SOURCE_ID = "QM"
HOST = "www.questmobile.com.cn"
INDEX_URL = f"https://{HOST}/research/report-list"
_REPORT_PATH_RE = re.compile(r"^/research/report/(?P<report_id>\d+)/?$")
_DATE_RE = re.compile(r"^20\d{2}-\d{2}-\d{2}$")
_FINDING_PREFIXES = ("QuestMobile数据显示", "QuestAuto数据显示")
PARSER_VERSION = "questmobile-public-research.v1"


@dataclass(frozen=True)
class _ReportLink:
    report_id: str
    title: str
    url: str


def _official_report_link(url: str, title: str) -> _ReportLink | None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != HOST:
        return None
    match = _REPORT_PATH_RE.fullmatch(parsed.path)
    if not match:
        return None
    normalized_title = normalize_whitespace(title)
    if not normalized_title:
        return None
    canonical = f"https://{HOST}/research/report/{match.group('report_id')}/"
    return _ReportLink(match.group("report_id"), normalized_title, canonical)


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _find_title_index(lines: list[str], title: str) -> int:
    exact = [index for index, line in enumerate(lines) if normalize_whitespace(line) == title]
    if len(exact) != 1:
        raise ValueError(f"QuestMobile report title anchor must be unique: {title!r}")
    return exact[0]


def _parse_detail(link: _ReportLink, envelope: Any) -> dict[str, Any]:
    if getattr(envelope, "url", "") != link.url:
        raise ValueError("QuestMobile detail response URL diverges from canonical report URL")
    document = html_to_document(envelope.html, base_url=link.url)
    lines = [normalize_whitespace(line) for line in document["text"].splitlines() if normalize_whitespace(line)]
    title_index = _find_title_index(lines, link.title)

    header = lines[title_index + 1 : title_index + 25]
    dates = [line for line in header if _DATE_RE.fullmatch(line)]
    if len(dates) != 1:
        raise ValueError(f"QuestMobile report must expose one publication date near title: {link.url}")
    publication_date = dates[0]

    authority_lines = [line for line in header if line.startswith("来源：")]
    if authority_lines != ["来源：QuestMobile研究院"]:
        raise ValueError(f"QuestMobile report source authority drifted: {link.url}")

    category_lines = [line for line in header if line.startswith("行业：")]
    category_text = category_lines[0][len("行业：") :].strip() if category_lines else ""

    findings: list[dict[str, str]] = []
    seen: set[str] = set()
    for line in lines[title_index + 1 :]:
        if not any(prefix in line for prefix in _FINDING_PREFIXES):
            continue
        excerpt = normalize_whitespace(line)
        if excerpt in seen:
            continue
        seen.add(excerpt)
        attribution = next(prefix for prefix in _FINDING_PREFIXES if prefix in excerpt)
        findings.append(
            {
                "finding_id": f"{link.report_id}:{len(findings) + 1}",
                "attribution": attribution.removesuffix("数据显示"),
                "excerpt": excerpt,
                "excerpt_sha256": _sha256_text(excerpt),
            }
        )
        if len(findings) >= 24:
            break

    metadata = envelope.metadata()
    if metadata.get("source_id") != SOURCE_ID:
        raise ValueError("QuestMobile detail provenance source_id drifted")
    return {
        "source_id": SOURCE_ID,
        "report_id": link.report_id,
        "title": link.title,
        "publication_date": publication_date,
        "source_authority": "QuestMobile研究院",
        "category_text": category_text or None,
        "finding_evidence_state": "TEXT_FINDINGS_OBSERVED" if findings else "NO_TEXT_FINDING",
        "finding_count": len(findings),
        "findings": findings,
        "source_url": link.url,
        "provenance_sha256": metadata["payload_sha256"],
        "provenance": metadata,
    }


class QuestMobilePublicResearchCollector:
    def __init__(self, *, client: Any | None = None) -> None:
        self.client = client or PublicHtmlClient(
            source_id=SOURCE_ID,
            allowed_hosts={HOST},
            timeout_seconds=30.0,
            retries=2,
            max_response_bytes=8_000_000,
        )

    def collect(self, *, report_limit: int = 5) -> dict[str, Any]:
        if isinstance(report_limit, bool) or not isinstance(report_limit, int) or not 1 <= report_limit <= 10:
            raise ValueError("report_limit must be an integer from 1 to 10")

        index = self.client.fetch(INDEX_URL, request_name="questmobile-public-research-index")
        index_meta = index.metadata()
        if index_meta.get("source_id") != SOURCE_ID:
            raise ValueError("QuestMobile index provenance source_id drifted")
        document = html_to_document(index.html, base_url=INDEX_URL)

        links: list[_ReportLink] = []
        seen_urls: set[str] = set()
        for raw in document["links"]:
            link = _official_report_link(str(raw.get("url") or ""), str(raw.get("text") or ""))
            if link is None or link.url in seen_urls:
                continue
            seen_urls.add(link.url)
            links.append(link)
            if len(links) >= report_limit:
                break
        if not links:
            raise ValueError("QuestMobile public research index exposed no governed report links")

        reports: list[dict[str, Any]] = []
        for link in links:
            detail = self.client.fetch(
                link.url,
                request_name=f"questmobile-public-research-{link.report_id}",
            )
            reports.append(_parse_detail(link, detail))

        total_findings = sum(report["finding_count"] for report in reports)
        if total_findings <= 0:
            raise ValueError("QuestMobile latest public reports exposed no textual research findings")

        return {
            "schema_version": PARSER_VERSION,
            "source_id": SOURCE_ID,
            "data_available": True,
            "collection_scope": "LATEST_PUBLIC_RESEARCH_REPORTS_ONLY",
            "report_limit": report_limit,
            "report_count": len(reports),
            "text_finding_count": total_findings,
            "reports": reports,
            "provenance": {"index": index_meta},
            "truth_boundaries": [
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
            ],
        }


GOVERNING_INVARIANTS = (
    "ONLY_PUBLIC_QUESTMOBILE_REPORT_PAGES_MAY_BE_FETCHED",
    "REPORT_ID_TITLE_DATE_AUTHORITY_AND_PAGE_HASH_MUST_REMAIN_BOUND",
    "SOURCE_NATIVE_TEXT_FINDINGS_NE_PARSED_MARKET_TRUTH",
    "IMAGE_ONLY_EVIDENCE_REMAINS_UNEXTRACTED_WITHOUT_OCR",
    "RESEARCH_NE_CURRENT_LOCAL_REALITY",
    "UNKNOWN_NE_PASS",
)
