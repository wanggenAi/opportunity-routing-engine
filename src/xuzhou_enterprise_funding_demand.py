"""Scoped direct enterprise financing-demand evidence for Xuzhou.

The collector reads the public Jiangsu Government ``地方动态`` column, follows
only the pagination chain that the official page itself exposes, and then opens
Xuzhou-titled official detail pages. Evidence is emitted only when a detail
page sourced from ``徐州市政府办公室`` contains an explicit financing-demand
amount.

This feed is intentionally *not* a citywide financing-demand total. It captures
reported program/batch evidence such as a financing campaign's surveyed demand.
SME/general-enterprise scope is never relabeled as private-enterprise scope.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from html import unescape
from typing import Any
from urllib.parse import urljoin, urlparse

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace


SOURCE_ID = "XZ_GOV_FINANCE_DEMAND"
HOST = "www.jiangsu.gov.cn"
INDEX_URL = "https://www.jiangsu.gov.cn/col/col33718/index.html"
COLUMN_ID = "33718"
UNIT_ID = "212860"

TRUTH_BOUNDARIES = [
    "DIRECT_DEMAND_EVIDENCE_IS_NEED_ONLY",
    "SCOPED_PROGRAM_IS_NOT_CITYWIDE_TOTAL",
    "SME_IS_NOT_PRIVATE_ENTERPRISE",
    "MISSING_DEMAND_IS_NOT_ZERO",
    "NO_CROSS_PROGRAM_SUM",
    "NO_CROSS_PERIOD_SUM",
    "NO_SURPLUS_RESOURCE_INFERENCE",
    "NO_OPPORTUNITY_INFERENCE",
]

_ARTICLE_RE = re.compile(
    r"<a\s+href=['\"](?P<href>/art/(?P<year>20\d{2})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/art_33718_\d+\.html)['\"][^>]*"
    r"title=['\"](?P<title>[^'\"]+)['\"][^>]*>.*?</a>\s*<span>(?P<date>20\d{2}-\d{2}-\d{2})</span>",
    flags=re.I | re.S,
)
_NEXTGROUP_RE = re.compile(
    r"<nextgroup><!\[CDATA\[<a\s+href=['\"](?P<href>[^'\"]*?/module/web/jpage/dataproxy\.jsp\?[^'\"]+)['\"]",
    flags=re.I,
)
_TOTAL_RECORD_RE = re.compile(r"totalRecord:(\d+)")
_PER_PAGE_RE = re.compile(r"perPage:(\d+)")
_DETAIL_PATH_RE = re.compile(r"^/art/(20\d{2})/(\d{1,2})/(\d{1,2})/art_33718_\d+\.html$")

_DEMAND_AMOUNT_RE = re.compile(
    r"(?:累计)?(?:摸排|梳理|发布|提出|收集|汇总|对接)?\s*融资需求"
    r"(?:为|达|共计|合计)?\s*([0-9]+(?:\.[0-9]+)?)\s*亿元"
)
_DEMAND_ENTERPRISES_RE = re.compile(r"([0-9]+)\s*家企业[^。；\n]{0,20}?融资需求")
_GRANTED_CREDIT_RE = re.compile(r"(?:已|累计)?授信\s*([0-9]+(?:\.[0-9]+)?)\s*亿元")
_BENEFICIARY_RE = re.compile(r"惠及\s*([0-9]+)\s*家企业")
_PROGRAM_RE = re.compile(r"(?:开展|实施)[“\"]([^”\"]{2,80})[”\"]融资专项行动")
_PUBLICATION_RE = re.compile(r"时间：\s*(20\d{2}-\d{2}-\d{2})")
_SOURCE_RE = re.compile(r"来源：\s*徐州市政府办公室")


def _official_detail_date(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != HOST:
        return None
    match = _DETAIL_PATH_RE.match(parsed.path)
    if not match:
        return None
    year, month, day = map(int, match.groups())
    return f"{year:04d}-{month:02d}-{day:02d}"


def parse_local_dynamics_records(html: str, *, base_url: str = INDEX_URL) -> list[dict[str, str]]:
    """Parse official column records from initial or jpage proxy HTML/XML."""
    records: list[dict[str, str]] = []
    seen: set[str] = set()
    for match in _ARTICLE_RE.finditer(html):
        url = urljoin(base_url, unescape(match.group("href")))
        url_date = _official_detail_date(url)
        listed_date = match.group("date")
        if not url_date or url_date != listed_date:
            continue
        if url in seen:
            continue
        seen.add(url)
        records.append(
            {
                "title": normalize_whitespace(unescape(match.group("title"))),
                "url": url,
                "publication_date": listed_date,
            }
        )
    return records


def discover_jpage_proxy(index_html: str, *, base_url: str = INDEX_URL) -> dict[str, Any]:
    match = _NEXTGROUP_RE.search(index_html)
    if not match:
        raise ValueError("official Jiangsu local-dynamics jpage proxy not found")
    proxy_url = urljoin(base_url, unescape(match.group("href")))
    parsed = urlparse(proxy_url)
    if parsed.scheme != "https" or parsed.hostname != HOST or parsed.path != "/module/web/jpage/dataproxy.jsp":
        raise ValueError(f"unexpected local-dynamics pagination endpoint: {proxy_url}")
    if f"columnid={COLUMN_ID}" not in parsed.query or f"unitid={UNIT_ID}" not in parsed.query:
        raise ValueError("local-dynamics pagination identity drift")

    total_matches = [int(value) for value in _TOTAL_RECORD_RE.findall(index_html)]
    per_page_matches = [int(value) for value in _PER_PAGE_RE.findall(index_html)]
    return {
        "url": proxy_url,
        "total_records": max(total_matches) if total_matches else None,
        "per_page": per_page_matches[-1] if per_page_matches else None,
    }


def _proxy_page_url(proxy_url: str, page: int) -> str:
    if page < 1:
        raise ValueError("jpage page must be >= 1")
    replaced, count = re.subn(r"([?&]page=)\d+", rf"\g<1>{page}", proxy_url, count=1)
    if count != 1:
        raise ValueError("jpage proxy URL has no page parameter")
    parsed = urlparse(replaced)
    if parsed.scheme != "https" or parsed.hostname != HOST or parsed.path != "/module/web/jpage/dataproxy.jsp":
        raise ValueError("jpage proxy escaped official allowlist")
    return replaced


def _sentence_with_match(text: str, start: int, end: int) -> str:
    left = max(text.rfind("。", 0, start), text.rfind("\n", 0, start), text.rfind("；", 0, start))
    right_candidates = [
        pos
        for pos in (text.find("。", end), text.find("\n", end), text.find("；", end))
        if pos >= 0
    ]
    right = min(right_candidates) if right_candidates else len(text)
    return normalize_whitespace(text[left + 1 : right + 1])


def _actor_scope(scope_text: str) -> tuple[str, bool]:
    if "民营企业" in scope_text or "民营经济" in scope_text:
        return "PRIVATE_ENTERPRISE", True
    if "中小微企业" in scope_text:
        return "SME_AND_MICRO", False
    if "中小企业" in scope_text or "小微企业" in scope_text:
        return "SME", False
    return "ENTERPRISE_GENERAL", False


def extract_funding_demand_event(
    *,
    title: str,
    url: str,
    html: str,
    provenance_sha256: str,
) -> dict[str, Any] | None:
    """Extract one explicit scoped financing-demand observation, if present."""
    url_date = _official_detail_date(url)
    if not url_date:
        raise ValueError(f"not an official Jiangsu local-dynamics detail URL: {url}")

    document = html_to_document(html, base_url=url)
    text = document["text"]
    if title not in text:
        raise ValueError("detail title identity drift")
    if not _SOURCE_RE.search(text):
        return None
    publication = _PUBLICATION_RE.search(text)
    if not publication or publication.group(1) != url_date:
        raise ValueError("detail publication date conflicts with official URL date")

    amount_match = _DEMAND_AMOUNT_RE.search(text)
    if not amount_match:
        return None
    demand_amount = Decimal(amount_match.group(1))
    if demand_amount <= 0:
        raise ValueError("non-positive explicit financing demand")

    sentence = _sentence_with_match(text, amount_match.start(), amount_match.end())
    # Preserve nearby program/scope language without using unrelated text elsewhere in the article.
    context_start = max(0, text.rfind("。", 0, amount_match.start() - 1) + 1)
    context = normalize_whitespace(text[context_start : min(len(text), amount_match.end() + 160)])
    scope_text = context or sentence
    actor_scope, private_explicit = _actor_scope(scope_text)

    program_match = _PROGRAM_RE.search(scope_text)
    demand_enterprises = _DEMAND_ENTERPRISES_RE.search(scope_text)
    granted = _GRANTED_CREDIT_RE.search(scope_text)
    beneficiary = _BENEFICIARY_RE.search(scope_text)

    return {
        "signal_id": "XZ_ENTERPRISE_FINANCING_DEMAND_SCOPED",
        "source_id": SOURCE_ID,
        "geography": "Xuzhou",
        "evidence_role": "DIRECT_SCOPED_ENTERPRISE_FINANCING_DEMAND",
        "publication_date": url_date,
        "title": title,
        "source_authority": "徐州市政府办公室",
        "source_url": url,
        "coverage_scope": "SCOPED_PROGRAM_OR_REPORTED_BATCH",
        "actor_scope": actor_scope,
        "private_enterprise_scope_explicit": private_explicit,
        "program_name": program_match.group(1) if program_match else None,
        "demand_amount_cny_100m": format(demand_amount, "f"),
        "demand_enterprise_count": int(demand_enterprises.group(1)) if demand_enterprises else None,
        "granted_credit_amount_cny_100m": format(Decimal(granted.group(1)), "f") if granted else None,
        "beneficiary_enterprises": int(beneficiary.group(1)) if beneficiary else None,
        "matched_text": sentence,
        "scope_context": scope_text,
        "aggregation_allowed": False,
        "provenance_sha256": provenance_sha256,
        "truth_boundaries": TRUTH_BOUNDARIES,
    }


def _freshness(publication_date: str | None) -> dict[str, Any]:
    if not publication_date:
        return {"publication_date": None, "age_days": None, "status": "UNKNOWN"}
    published = date.fromisoformat(publication_date)
    age = (datetime.now(timezone.utc).date() - published).days
    if age < 0:
        status = "FUTURE_DATE_ERROR"
    elif age <= 120:
        status = "FRESH"
    elif age <= 365:
        status = "AGING"
    else:
        status = "STALE"
    return {"publication_date": publication_date, "age_days": age, "status": status}


class XuzhouEnterpriseFundingDemandAdapter:
    def __init__(
        self,
        client: PublicHtmlClient | None = None,
        *,
        lookback_days: int = 400,
        max_pages: int = 45,
    ) -> None:
        if lookback_days <= 0 or max_pages <= 0:
            raise ValueError("lookback_days and max_pages must be positive")
        self.client = client or PublicHtmlClient(
            source_id=SOURCE_ID,
            allowed_hosts={HOST},
            timeout_seconds=25,
            retries=1,
            max_response_bytes=3_000_000,
            accepted_content_types={
                "text/html",
                "application/xhtml+xml",
                "text/plain",
                "text/xml",
                "application/xml",
            },
        )
        self.lookback_days = lookback_days
        self.max_pages = max_pages

    def collect(self) -> dict[str, Any]:
        index_env = self.client.fetch(INDEX_URL, request_name="xz_funding_demand.index")
        proxy = discover_jpage_proxy(index_env.html)
        records = parse_local_dynamics_records(index_env.html)
        if not records:
            raise ValueError("official Jiangsu local-dynamics index produced no records")

        cutoff = datetime.now(timezone.utc).date() - timedelta(days=self.lookback_days)
        seen_urls = {row["url"] for row in records}
        pages_fetched = 1
        page_provenance: list[dict[str, Any]] = [index_env.metadata()]

        oldest = min(date.fromisoformat(row["publication_date"]) for row in records)
        page = 1
        while oldest >= cutoff and page <= self.max_pages:
            page_url = _proxy_page_url(proxy["url"], page)
            env = self.client.fetch(
                page_url,
                request_name=f"xz_funding_demand.list.page_{page}",
            )
            page_provenance.append(env.metadata())
            pages_fetched += 1
            batch = parse_local_dynamics_records(env.html, base_url=INDEX_URL)
            if not batch:
                break
            added = 0
            for row in batch:
                if row["url"] not in seen_urls:
                    seen_urls.add(row["url"])
                    records.append(row)
                    added += 1
            oldest = min(
                oldest,
                *(date.fromisoformat(row["publication_date"]) for row in batch),
            )
            page += 1
            if added == 0 and page > 2:
                break

        in_window = [
            row
            for row in records
            if date.fromisoformat(row["publication_date"]) >= cutoff
        ]
        candidates = [row for row in in_window if "徐州" in row["title"]]
        events: list[dict[str, Any]] = []
        detail_provenance: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []
        for row in candidates:
            try:
                env = self.client.fetch(
                    row["url"],
                    request_name="xz_funding_demand.detail",
                )
                detail_provenance.append(env.metadata())
                event = extract_funding_demand_event(
                    title=row["title"],
                    url=env.url,
                    html=env.html,
                    provenance_sha256=env.payload_sha256,
                )
                if event:
                    events.append(event)
            except Exception as exc:
                errors.append(
                    {
                        "url": row["url"],
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    }
                )

        events.sort(
            key=lambda item: (item["publication_date"], item["source_url"]),
            reverse=True,
        )
        latest_date = events[0]["publication_date"] if events else None
        return {
            "source_id": SOURCE_ID,
            "collected_at_utc": datetime.now(timezone.utc).isoformat(),
            "data_available": bool(events),
            "geography": "Xuzhou",
            "evidence_kind": "SCOPED_DIRECT_ENTERPRISE_FINANCING_DEMAND",
            "lookback_days": self.lookback_days,
            "cutoff_date": cutoff.isoformat(),
            "discovery": {
                "column_url": INDEX_URL,
                "column_id": COLUMN_ID,
                "unit_id": UNIT_ID,
                "reported_total_records": proxy.get("total_records"),
                "reported_per_page": proxy.get("per_page"),
                "pages_fetched": pages_fetched,
                "records_in_window": len(in_window),
                "xuzhou_title_candidates": len(candidates),
            },
            "event_count": len(events),
            "error_count": len(errors),
            "events": events,
            "errors": errors,
            "latest_freshness": _freshness(latest_date),
            "provenance": {
                "list_pages": page_provenance,
                "detail_pages": detail_provenance,
            },
            "truth_boundaries": TRUTH_BOUNDARIES,
            "interpretation_boundary": (
                "Each event is an explicit financing-demand amount reported by a Jiangsu Government page sourced from "
                "the Xuzhou Government Office. Evidence is scoped to the stated program/batch and proves NEED only. "
                "It is not a Xuzhou citywide total, SME/general-enterprise language is not relabeled as private-enterprise "
                "scope, and events across programs or periods must not be summed."
            ),
        }
