"""Observable capability-supply evidence from Xuzhou procurement results.

A public award/result notice is strong evidence that a named supplier has previously
produced an accepted/buyable capability for a real procurement transaction. It is
not evidence that the supplier is currently idle, available, optioned, or willing to
accept another task.

Truth boundaries:
- award/result notice -> historical capability proof;
- award amount -> completed/awarded transaction evidence for that historical project;
- supplier identity -> DISCOVERED capability provider, not controlled supply;
- no current availability or underuse is inferred;
- void/failed packages without a supplier row produce no provider evidence;
- supplier rows from a different package on the same HTML page are not attributed to
  the package-specific result URL;
- paginated history is bounded and may be pre-filtered by an exact capability rule
  before detail pages are fetched.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from html import unescape
from typing import Any, Callable, Mapping

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace


XZ_GGZY_HOST = "ggzy.zwb.xz.gov.cn"
XZ_PROCUREMENT_RESULT_LIST = (
    "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/list.html"
)

_RESULT_DETAIL_RE = re.compile(
    r"/jyxx/003004/003004006/(20\d{6})/[0-9a-fA-F-]+\.html(?:\?.*)?$"
)
_TABLE_RE = re.compile(r"<table\b[^>]*>(?P<body>.*?)</table>", re.I | re.S)
_ROW_RE = re.compile(r"<tr\b[^>]*>(?P<body>.*?)</tr>", re.I | re.S)
_CELL_RE = re.compile(r"<t[dh]\b[^>]*>(?P<body>.*?)</t[dh]>", re.I | re.S)
_CREDIT_RE = re.compile(r"\b[0-9A-Z]{18}\b")
_MONEY_RE = re.compile(r"([0-9][0-9,]*(?:\.\d+)?)\s*(亿元|万元|元)")
_PACKAGE_RE = re.compile(r"采购包\s*([一二三四五六七八九十\d]+)")


@dataclass(frozen=True)
class ProcurementAward:
    source_id: str
    title: str
    url: str
    publication_date: str | None
    project_id: str | None
    project_name: str | None
    buyer_actor: str | None
    supplier_name: str
    supplier_credit_code: str | None
    supplier_address: str | None
    award_amount_rmb: str | None
    award_amount_raw: str | None
    service_name: str | None
    provenance: dict[str, Any]
    package_name: str | None = None


def _plain(fragment: str) -> str:
    text = re.sub(r"<br\s*/?>", " ", fragment, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return normalize_whitespace(unescape(text))


def _first(pattern: str, text: str, flags: int = 0) -> str | None:
    match = re.search(pattern, text, flags)
    return normalize_whitespace(match.group(1)) if match else None


def _package_label(text: str) -> str | None:
    matches = _PACKAGE_RE.findall(normalize_whitespace(text))
    if not matches:
        return None
    return f"采购包{matches[-1]}"


def _date_from_url(url: str) -> str | None:
    match = re.search(r"/(20\d{6})/", url)
    if not match:
        return None
    raw = match.group(1)
    return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"


def _publication_date(text: str, url: str) -> str | None:
    value = _first(
        r"信息发布时间[：:\s]*([0-9]{4}[-年][0-9]{1,2}[-月][0-9]{1,2}日?)",
        text,
    )
    if value:
        parts = re.findall(r"\d+", value)
        if len(parts) >= 3:
            return f"{int(parts[0]):04d}-{int(parts[1]):02d}-{int(parts[2]):02d}"
    return _date_from_url(url)


def _money_to_rmb(raw_number: str, unit: str) -> str | None:
    try:
        value = Decimal(raw_number.replace(",", ""))
    except InvalidOperation:
        return None
    multiplier = Decimal("1")
    if unit == "万元":
        multiplier = Decimal("10000")
    elif unit == "亿元":
        multiplier = Decimal("100000000")
    return format((value * multiplier).quantize(Decimal("0.01")), "f")


def _history_page_url(list_url: str, page: int) -> str:
    """Return the site's canonical numbered history page URL.

    The live first page is ``list.html``; historical pages are siblings such as
    ``2.html``, ``3.html`` and so on.
    """

    if page < 1:
        raise ValueError("page must be >= 1")
    if page == 1:
        return list_url
    base = list_url.rsplit("/", 1)[0]
    return f"{base}/{page}.html"


def _extract_award_rows(html: str) -> list[dict[str, str | None]]:
    """Extract supplier rows while retaining their nearest explicit package label.

    Xuzhou result pages can expose multiple procurement packages in one HTML body,
    even when the detail URL/title is package-specific. Losing that package boundary
    can incorrectly attribute another package's supplier to the title capability.
    """

    result: list[dict[str, str | None]] = []
    seen: set[tuple[str | None, str, str | None, str | None]] = set()
    for table_match in _TABLE_RE.finditer(html):
        # The package marker is normally rendered immediately before its result table.
        # Use a bounded preceding window and the nearest marker; if none is present we
        # retain UNKNOWN here and let a package-specific detail URL fail closed below.
        context_start = max(0, table_match.start() - 6000)
        package_name = _package_label(_plain(html[context_start : table_match.start()]))
        table_html = table_match.group("body")
        for row_match in _ROW_RE.finditer(table_html):
            cells = [
                _plain(match.group("body"))
                for match in _CELL_RE.finditer(row_match.group("body"))
            ]
            if len(cells) < 3:
                continue
            credit_index = next(
                (index for index, cell in enumerate(cells) if _CREDIT_RE.search(cell)),
                None,
            )
            if credit_index is None or credit_index < 1:
                continue
            supplier = cells[credit_index - 1].strip()
            if not supplier or supplier in {"供应商名称", "供应商"}:
                continue
            credit_codes = _CREDIT_RE.findall(cells[credit_index])
            credit_code = "、".join(credit_codes) if credit_codes else None
            address = (
                cells[credit_index + 1].strip()
                if credit_index + 1 < len(cells)
                else None
            )

            amount_raw = None
            amount_rmb = None
            for cell in reversed(cells[credit_index + 1 :]):
                match = _MONEY_RE.search(cell)
                if not match:
                    continue
                amount_raw = normalize_whitespace(match.group(0))
                amount_rmb = _money_to_rmb(match.group(1), match.group(2))
                break

            identity = (package_name, supplier, credit_code, amount_raw)
            if identity in seen:
                continue
            seen.add(identity)
            result.append(
                {
                    "package_name": package_name,
                    "supplier_name": supplier,
                    "supplier_credit_code": credit_code,
                    "supplier_address": address or None,
                    "award_amount_rmb": amount_rmb,
                    "award_amount_raw": amount_raw,
                }
            )
    return result


class XuzhouProcurementResultAdapter:
    """Discover result notices and normalize proven supplier capability events."""

    DETAIL_RE = _RESULT_DETAIL_RE

    def __init__(self, client: PublicHtmlClient | None = None) -> None:
        self.client = client or PublicHtmlClient(
            source_id="XZ_GGZY_PROCUREMENT_RESULT",
            allowed_hosts={XZ_GGZY_HOST},
            timeout_seconds=30,
            retries=2,
        )

    def discover_recent(
        self,
        *,
        list_url: str = XZ_PROCUREMENT_RESULT_LIST,
        limit: int = 30,
    ) -> dict[str, Any]:
        if limit <= 0 or limit > 200:
            raise ValueError("limit must be between 1 and 200")
        envelope = self.client.fetch(
            list_url,
            request_name="xz_ggzy.procurement_results.list",
        )
        doc = html_to_document(envelope.html, base_url=list_url)
        items: list[dict[str, Any]] = []
        seen: set[str] = set()
        for link in doc["links"]:
            url = link["url"]
            match = self.DETAIL_RE.search(url)
            if not match or url in seen:
                continue
            seen.add(url)
            raw_date = match.group(1)
            items.append(
                {
                    "title": re.sub(r"^\[?新\]?", "", link["text"]).strip(),
                    "url": url,
                    "publication_date": f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}",
                }
            )
            if len(items) >= limit:
                break
        return {
            "source_id": "XZ_GGZY_PROCUREMENT_RESULT",
            "list_url": list_url,
            "item_count": len(items),
            "items": items,
            "provenance": envelope.metadata(),
        }

    def discover_history(
        self,
        *,
        pages: int = 5,
        list_url: str = XZ_PROCUREMENT_RESULT_LIST,
        item_filter: Callable[[Mapping[str, Any]], bool] | None = None,
        max_items: int = 100,
    ) -> dict[str, Any]:
        """Boundedly scan numbered result pages and keep only relevant titles.

        Filtering occurs on list-page metadata before any detail page is fetched.
        This is important because the public result archive is very large; the engine
        should backfill evidence for known canonical capabilities rather than scrape
        the entire archive.
        """

        if not isinstance(pages, int) or pages < 1 or pages > 50:
            raise ValueError("pages must be between 1 and 50")
        if not isinstance(max_items, int) or max_items < 1 or max_items > 500:
            raise ValueError("max_items must be between 1 and 500")

        selected: list[dict[str, Any]] = []
        seen: set[str] = set()
        page_summaries: list[dict[str, Any]] = []
        raw_item_count = 0

        for page in range(1, pages + 1):
            page_url = _history_page_url(list_url, page)
            discovery = self.discover_recent(list_url=page_url, limit=200)
            page_items = list(discovery["items"])
            raw_item_count += len(page_items)
            selected_on_page = 0
            for item in page_items:
                url = str(item.get("url") or "")
                if not url or url in seen:
                    continue
                seen.add(url)
                if item_filter is not None and not item_filter(item):
                    continue
                selected.append(item)
                selected_on_page += 1
                if len(selected) >= max_items:
                    break
            page_summaries.append(
                {
                    "page": page,
                    "url": page_url,
                    "raw_item_count": len(page_items),
                    "selected_item_count": selected_on_page,
                    "provenance": discovery["provenance"],
                }
            )
            if len(selected) >= max_items:
                break
            if not page_items:
                break

        return {
            "source_id": "XZ_GGZY_PROCUREMENT_RESULT",
            "list_url": list_url,
            "requested_pages": pages,
            "scanned_pages": len(page_summaries),
            "raw_item_count": raw_item_count,
            "item_count": len(selected),
            "items": selected,
            "pages": page_summaries,
            "filter_applied": item_filter is not None,
        }

    def fetch_awards(
        self,
        url: str,
        *,
        fallback_title: str | None = None,
    ) -> list[ProcurementAward]:
        if not self.DETAIL_RE.search(url):
            raise ValueError("URL is not a Xuzhou government-procurement result notice")
        envelope = self.client.fetch(
            url,
            request_name="xz_ggzy.procurement_results.detail",
        )
        doc = html_to_document(envelope.html, base_url=url)
        text = doc["text"]
        title = self._best_title(text, doc["title"], fallback_title)
        rows = _extract_award_rows(envelope.html)

        title_package = _package_label(title)
        if title_package:
            # A package-specific result URL is authoritative only for its own package.
            # Rows whose package cannot be resolved are withheld rather than guessed.
            rows = [row for row in rows if row.get("package_name") == title_package]
        if not rows:
            return []

        project_id = _first(r"项目编号[：:\s]*([^\n]+)", text)
        project_name = _first(r"项目名称[：:\s]*([^\n]+)", text)
        buyer_actor = _first(
            r"采购人信息[\s\S]{0,600}?单位名称[：:\s]*([^\n]+)",
            text,
        )
        service_name = _first(
            r"主要标的信息[\s\S]{0,1200}?名称[：:\s]*([^\n]+)",
            text,
        )
        publication_date = _publication_date(text, url)
        return [
            ProcurementAward(
                source_id="XZ_GGZY_PROCUREMENT_RESULT",
                title=title,
                url=url,
                publication_date=publication_date,
                project_id=project_id,
                project_name=project_name,
                buyer_actor=buyer_actor,
                supplier_name=str(row["supplier_name"]),
                supplier_credit_code=row["supplier_credit_code"],
                supplier_address=row["supplier_address"],
                award_amount_rmb=row["award_amount_rmb"],
                award_amount_raw=row["award_amount_raw"],
                service_name=service_name,
                provenance=envelope.metadata(),
                package_name=row.get("package_name"),
            )
            for row in rows
        ]

    @staticmethod
    def _best_title(text: str, html_title: str, fallback: str | None) -> str:
        for line in text.splitlines()[:35]:
            line = normalize_whitespace(line)
            if len(line) <= 200 and any(
                marker in line
                for marker in ("中标结果公告", "中标公告", "成交结果公告", "成交公告")
            ):
                return line
        return fallback or html_title

    def _collect_from_discovery(
        self,
        discovery: Mapping[str, Any],
        *,
        max_details: int | None = None,
    ) -> dict[str, Any]:
        items = list(discovery.get("items", []) or [])
        if max_details is not None:
            if not isinstance(max_details, int) or max_details < 1 or max_details > 200:
                raise ValueError("max_details must be between 1 and 200")
            items = items[:max_details]

        awards: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []
        no_supplier_result_count = 0
        for item in items:
            try:
                parsed = self.fetch_awards(item["url"], fallback_title=item["title"])
                if not parsed:
                    no_supplier_result_count += 1
                awards.extend(asdict(award) for award in parsed)
            except Exception as exc:
                errors.append({"url": str(item.get("url") or ""), "error": str(exc)})
        return {
            "source_id": "XZ_GGZY_PROCUREMENT_RESULT",
            "discovery": dict(discovery),
            "detail_fetch_count": len(items),
            "award_count": len(awards),
            "no_supplier_result_count": no_supplier_result_count,
            "error_count": len(errors),
            "awards": awards,
            "errors": errors,
            "truth_note": (
                "Award notices prove historical supplier capability and transaction evidence only; "
                "package-specific URLs admit only supplier rows bound to that package; "
                "awards do not prove current provider availability, underuse, or orchestrator control."
            ),
        }

    def collect_recent_awards(self, *, limit: int = 20) -> dict[str, Any]:
        return self._collect_from_discovery(self.discover_recent(limit=limit))

    def collect_history_awards(
        self,
        *,
        pages: int = 5,
        item_filter: Callable[[Mapping[str, Any]], bool] | None = None,
        max_items: int = 100,
        max_details: int = 40,
    ) -> dict[str, Any]:
        discovery = self.discover_history(
            pages=pages,
            item_filter=item_filter,
            max_items=max_items,
        )
        return self._collect_from_discovery(discovery, max_details=max_details)
