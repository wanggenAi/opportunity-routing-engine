"""Official GACC monthly trade-flow evidence for Jiangsu and Xuzhou.

GACC's English Monthly Bulletin is currently reachable by GitHub-hosted runners over
plain HTTP, while its HTTPS certificate chain fails standard verification. We do
not weaken TLS verification repository-wide. Instead, exactly like the isolated
MOFCOM official-HTTP exception, this module permits only the documented GACC host
and monthly/detail paths, records plaintext transport explicitly, and requires
independent corroboration before downstream conclusions may rely on the data.

Truth boundaries:
- plaintext official HTTP is lower-trust and requires corroboration;
- importer/exporter-location trade != domestic origin/destination trade;
- a specific customs area != the whole Xuzhou economy;
- specific-area rows are not summed into city/province totals here;
- trade flow != unmet need, surplus resource, transaction blocker, or opportunity;
- missing/blank values stay unknown and are never zero-filled.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from src.html_ingest import HtmlFetchEnvelope, normalize_whitespace


SOURCE_ID = "CN_CUSTOMS"
HOST = "english.customs.gov.cn"
MONTHLY_PATH = "/statics/report/monthly.html"
MONTHLY_URL = f"http://{HOST}{MONTHLY_PATH}"
_DETAIL_PATH_RE = re.compile(r"^/statics/[0-9a-f-]+\.html$", re.IGNORECASE)
_PERIOD_RE = re.compile(r"(?:1\s*(?:to|[-—–])\s*)?(\d{1,2})\s*[.]\s*(20\d{2})", re.IGNORECASE)
_NUMBER_RE = re.compile(r"^-?\d[\d,]*(?:\.\d+)?$")


class GaccOfficialHttpError(RuntimeError):
    pass


class GaccOfficialHttpClient:
    """Exact-host/path client for GACC's public plaintext monthly bulletin.

    This is intentionally isolated rather than weakening ``PublicHtmlClient``'s
    HTTPS-only invariant. Redirects to another host/scheme/path are rejected.
    """

    def __init__(self, *, timeout_seconds: float = 30.0, max_response_bytes: int = 8_000_000) -> None:
        if timeout_seconds <= 0 or max_response_bytes <= 0:
            raise ValueError("invalid GACC HTTP client bounds")
        self.timeout_seconds = timeout_seconds
        self.max_response_bytes = max_response_bytes

    @staticmethod
    def _allowed(url: str) -> bool:
        parsed = urlparse(url)
        if parsed.scheme != "http" or parsed.hostname != HOST:
            return False
        return parsed.path == MONTHLY_PATH or bool(_DETAIL_PATH_RE.match(parsed.path))

    def fetch(self, url: str, *, request_name: str, params=None, headers=None) -> HtmlFetchEnvelope:
        if params:
            raise GaccOfficialHttpError("GACC monthly bulletin client does not accept query parameters")
        if not self._allowed(url):
            raise GaccOfficialHttpError(f"GACC HTTP client rejected URL: {url}")
        request_headers = {
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5",
            "User-Agent": "OpportunityRoutingEngine/0.1 (+public-evidence-ingest)",
        }
        if headers:
            request_headers.update(headers)
        request = Request(url, headers=request_headers, method="GET")
        try:
            response = urlopen(request, timeout=self.timeout_seconds)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise GaccOfficialHttpError(f"GACC official HTTP request failed for {request_name}: {exc}") from exc
        try:
            final_url = str(getattr(response, "geturl", lambda: url)())
            if not self._allowed(final_url):
                raise GaccOfficialHttpError(f"unexpected GACC redirect target: {final_url}")
            body = response.read(self.max_response_bytes + 1)
            if len(body) > self.max_response_bytes:
                raise GaccOfficialHttpError("GACC response exceeded size limit")
            headers_obj = getattr(response, "headers", None)
            content_type = str(headers_obj.get("Content-Type", "")) if headers_obj is not None else ""
            lowered = content_type.lower()
            if lowered and not any(x in lowered for x in ("text/html", "application/xhtml+xml", "text/plain")):
                raise GaccOfficialHttpError(f"unexpected GACC content type: {content_type}")
            charset = None
            if headers_obj is not None:
                get_charset = getattr(headers_obj, "get_content_charset", None)
                if callable(get_charset):
                    charset = get_charset()
            candidates = [charset] if charset else []
            candidates.extend(["utf-8", "gb18030"])
            html = None
            used_encoding = None
            for encoding in candidates:
                if not encoding:
                    continue
                try:
                    html = body.decode(encoding, errors="strict")
                    used_encoding = encoding
                    break
                except (LookupError, UnicodeDecodeError):
                    continue
            if html is None or used_encoding is None:
                raise GaccOfficialHttpError("unable to decode GACC HTML")
            status = int(getattr(response, "status", None) or response.getcode())
            return HtmlFetchEnvelope(
                source_id=SOURCE_ID,
                request_name=request_name,
                url=final_url,
                fetched_at_utc=datetime.now(timezone.utc).isoformat(),
                http_status=status,
                content_type=content_type,
                payload_sha256=hashlib.sha256(body).hexdigest(),
                encoding=used_encoding,
                html=html,
            )
        finally:
            close = getattr(response, "close", None)
            if callable(close):
                close()


class _TableParser(HTMLParser):
    """Small table parser retaining cell text and same-cell links."""

    def __init__(self, *, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.rows: list[list[dict[str, Any]]] = []
        self._row: list[dict[str, Any]] | None = None
        self._cell: dict[str, Any] | None = None
        self._cell_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag == "tr":
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._cell = {"parts": [], "links": []}
            self._cell_depth = 1
        elif self._cell is not None:
            self._cell_depth += 1
            if tag == "a":
                href = dict(attrs).get("href")
                if href and not href.lower().startswith(("javascript:", "mailto:", "#")):
                    self._cell["links"].append(urljoin(self.base_url, href))

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._cell is not None:
            if tag in {"td", "th"} and self._cell_depth == 1:
                self._row.append(
                    {
                        "text": normalize_whitespace(" ".join(self._cell["parts"])),
                        "links": list(dict.fromkeys(self._cell["links"])),
                    }
                )
                self._cell = None
                self._cell_depth = 0
                return
            self._cell_depth = max(1, self._cell_depth - 1)
        if tag == "tr" and self._row is not None:
            if any(cell["text"] or cell["links"] for cell in self._row):
                self.rows.append(self._row)
            self._row = None

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            text = normalize_whitespace(data)
            if text:
                self._cell["parts"].append(text)


def parse_html_tables(html: str, *, base_url: str) -> list[list[dict[str, Any]]]:
    parser = _TableParser(base_url=base_url)
    parser.feed(html)
    return parser.rows


def _official_detail_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "http" and parsed.hostname == HOST and bool(_DETAIL_PATH_RE.match(parsed.path))


def _selected_year(html: str) -> int | None:
    patterns = (
        r"<option[^>]*selected[^>]*>\s*(20\d{2})\s*</option>",
        r"<option[^>]*value=['\"]?(20\d{2})['\"]?[^>]*selected[^>]*>",
    )
    for pattern in patterns:
        match = re.search(pattern, html, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
    years = [int(x) for x in re.findall(r"<option[^>]*>\s*(20\d{2})\s*</option>", html, flags=re.IGNORECASE)]
    return max(years) if years else None


def _period_from_text(text: str) -> tuple[int, int] | None:
    matches = list(_PERIOD_RE.finditer(text))
    if not matches:
        return None
    month, year = matches[-1].groups()
    month_i = int(month)
    if not 1 <= month_i <= 12:
        return None
    return int(year), month_i


def _number(value: str) -> float | None:
    value = normalize_whitespace(value).replace("−", "-")
    if value in {"", "-", "--", "…", "..."}:
        return None
    value = value.replace("%", "")
    if not _NUMBER_RE.match(value):
        return None
    return float(value.replace(",", ""))


@dataclass(frozen=True)
class TradeRow:
    name: str
    total_month_usd_thousand: float | None
    total_ytd_usd_thousand: float | None
    exports_month_usd_thousand: float | None
    exports_ytd_usd_thousand: float | None
    imports_month_usd_thousand: float | None
    imports_ytd_usd_thousand: float | None
    total_yoy_percent: float | None
    exports_yoy_percent: float | None
    imports_yoy_percent: float | None


def _trade_row(cells: list[dict[str, Any]]) -> TradeRow | None:
    if len(cells) < 7:
        return None
    name = normalize_whitespace(cells[0]["text"])
    if not name:
        return None
    values = [_number(cell["text"]) for cell in cells[1:]]
    if sum(v is not None for v in values[:6]) < 4:
        return None
    padded = values + [None] * 9
    return TradeRow(
        name=name,
        total_month_usd_thousand=padded[0],
        total_ytd_usd_thousand=padded[1],
        exports_month_usd_thousand=padded[2],
        exports_ytd_usd_thousand=padded[3],
        imports_month_usd_thousand=padded[4],
        imports_ytd_usd_thousand=padded[5],
        total_yoy_percent=padded[6],
        exports_yoy_percent=padded[7],
        imports_yoy_percent=padded[8],
    )


def _row_consistent(row: TradeRow) -> bool:
    checks = (
        (row.total_month_usd_thousand, row.exports_month_usd_thousand, row.imports_month_usd_thousand),
        (row.total_ytd_usd_thousand, row.exports_ytd_usd_thousand, row.imports_ytd_usd_thousand),
    )
    for total, exports, imports in checks:
        if total is None or exports is None or imports is None:
            continue
        tolerance = max(2.0, abs(total) * 0.00002)
        if abs(total - exports - imports) > tolerance:
            return False
    return True


class GaccTradeFlowAdapter:
    def __init__(self, client: Any | None = None) -> None:
        self.client = client or GaccOfficialHttpClient()

    def _discover_row(self, rows: list[list[dict[str, Any]]], needle: str) -> list[str]:
        for row in rows:
            if not row:
                continue
            row_text = " ".join(cell["text"] for cell in row)
            if needle.lower() not in row_text.lower():
                continue
            links: list[str] = []
            for cell in row:
                for url in cell["links"]:
                    if _official_detail_url(url):
                        links.append(url)
            if links:
                return list(dict.fromkeys(links))
        return []

    def discover_latest(self) -> dict[str, Any]:
        env = self.client.fetch(MONTHLY_URL, request_name="gacc.monthly.index")
        rows = parse_html_tables(env.html, base_url=env.url)
        selected_year = _selected_year(env.html)
        location_links = self._discover_row(rows, "Location of Importers/Exporters")
        area_links = self._discover_row(rows, "Imports and Exports by Specific Areas")
        if not location_links or not area_links:
            raise ValueError("GACC monthly bulletin did not expose table 8/11 official detail links")
        return {
            "source_id": SOURCE_ID,
            "index_url": env.url,
            "selected_year": selected_year,
            "location_links": location_links,
            "specific_area_links": area_links,
            "transport_security": "PLAINTEXT_HTTP",
            "corroboration_required": True,
            "provenance": env.metadata(),
        }

    def _fetch_latest_valid(self, links: list[str], *, table_number: int) -> dict[str, Any]:
        best: dict[str, Any] | None = None
        for url in reversed(links):
            env = self.client.fetch(url, request_name=f"gacc.monthly.table_{table_number}")
            text = normalize_whitespace(re.sub(r"<[^>]+>", " ", env.html))
            period = _period_from_text(text)
            if period is None:
                continue
            if f"({table_number})" not in text and f"（{table_number}）" not in text:
                continue
            candidate = {
                "url": env.url,
                "period_year": period[0],
                "period_month": period[1],
                "html": env.html,
                "provenance": env.metadata(),
            }
            if best is None or (candidate["period_year"], candidate["period_month"]) > (
                best["period_year"], best["period_month"]
            ):
                best = candidate
        if best is None:
            raise ValueError(f"no valid GACC table {table_number} detail publication found")
        return best

    def _rows_from_detail(self, detail: dict[str, Any]) -> list[TradeRow]:
        html = detail["html"]
        text = normalize_whitespace(re.sub(r"<[^>]+>", " ", html))
        if not re.search(r"Unit\s*:\s*US\$\s*1,?000", text, flags=re.IGNORECASE):
            raise ValueError("GACC trade table unit is not explicit US$1,000")
        parsed: list[TradeRow] = []
        for cells in parse_html_tables(html, base_url=detail["url"]):
            row = _trade_row(cells)
            if row is not None and _row_consistent(row):
                parsed.append(row)
        return parsed

    def collect(self) -> dict[str, Any]:
        discovery = self.discover_latest()
        location = self._fetch_latest_valid(discovery["location_links"], table_number=8)
        areas = self._fetch_latest_valid(discovery["specific_area_links"], table_number=11)
        if (location["period_year"], location["period_month"]) != (areas["period_year"], areas["period_month"]):
            raise ValueError("GACC table 8 and table 11 periods do not match")
        if discovery["selected_year"] is not None and location["period_year"] != discovery["selected_year"]:
            raise ValueError("GACC selected bulletin year conflicts with discovered detail year")

        location_rows = self._rows_from_detail(location)
        area_rows = self._rows_from_detail(areas)
        jiangsu = next((row for row in location_rows if row.name.strip().lower() == "jiangsu"), None)
        xuzhou_location = next((row for row in location_rows if row.name.strip().lower() == "xuzhou"), None)
        xuzhou_areas = [row for row in area_rows if "xuzhou" in row.name.lower()]
        if jiangsu is None:
            raise ValueError("Jiangsu row missing from GACC importer/exporter-location table")
        if not xuzhou_areas and xuzhou_location is None:
            raise ValueError("no explicit Xuzhou row found in current GACC location/specific-area tables")

        return {
            "source_id": SOURCE_ID,
            "evidence_kind": "CUSTOMS_TRADE_FLOW",
            "period": f"{location['period_year']:04d}-{location['period_month']:02d}",
            "unit": "USD_THOUSAND",
            "transport_security": "PLAINTEXT_HTTP",
            "corroboration_required": True,
            "corroboration_status": "PENDING",
            "jiangsu_importer_exporter_location": asdict(jiangsu),
            "xuzhou_importer_exporter_location": asdict(xuzhou_location) if xuzhou_location else None,
            "xuzhou_specific_areas": [asdict(row) for row in xuzhou_areas],
            "discovery": discovery,
            "table_8_provenance": location["provenance"],
            "table_11_provenance": areas["provenance"],
            "truth_boundaries": [
                "PLAINTEXT_HTTP_REQUIRES_CORROBORATION",
                "IMPORTER_EXPORTER_LOCATION_IS_NOT_DOMESTIC_ORIGIN_DESTINATION",
                "SPECIFIC_AREA_IS_NOT_WHOLE_XUZHOU",
                "NO_CROSS_TABLE_SUM",
                "MISSING_STAYS_UNKNOWN",
                "TRADE_FLOW_IS_NOT_UNMET_NEED",
                "TRADE_FLOW_IS_NOT_SURPLUS_RESOURCE",
                "NO_TRANSACTION_BLOCKER_INFERENCE",
                "NO_OPPORTUNITY_INFERENCE",
            ],
        }
