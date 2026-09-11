"""Xuzhou macro releases via the Jiangsu provincial-government official mirror.

Direct Xuzhou-government statistics pages are not promoted here unless a stable
machine-discoverable route is proven. Instead this adapter uses the Jiangsu
provincial-government `地方动态` column and accepts an article only when:

1. the article is on the official Jiangsu government host;
2. the title is clearly about Xuzhou economic operation / GDP;
3. the detail page explicitly identifies `徐州市政府办公室` as the source.

This is therefore an official mirror, not a claim that `jiangsu.gov.cn` is the
original Xuzhou statistics host.

Truth rules:
- mirror attribution is retained explicitly;
- missing metrics are omitted, never filled with zero;
- a relative statement such as "investment decline narrowed" is not converted
  into an investment growth rate;
- search engines are not part of production discovery.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any
from urllib.parse import urlparse

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace


SOURCE_ID = "JS_GOV_XZ_MIRROR"
HOST = "www.jiangsu.gov.cn"
COLUMN_ID = "33718"
COLUMN_URL = f"https://{HOST}/col/col{COLUMN_ID}/index.html"
PAGE_URL = f"https://{HOST}/col/col{COLUMN_ID}/index.html?pageNum={{page}}&uid=212860"
ARTICLE_RE = re.compile(
    rf"^https://{re.escape(HOST)}/art/(20\d{{2}})/(\d{{1,2}})/(\d{{1,2}})/art_{COLUMN_ID}_(\d+)\.html(?:\?.*)?$"
)
SOURCE_MARKER_RE = re.compile(r"来源[：:\s]*徐州市政府办公室")
ECONOMIC_TITLE_MARKERS = ("经济运行", "GDP", "经济半年报", "经济“半年报”", "经济一季报", "经济三季报")


def _decimal(value: str) -> str:
    return format(Decimal(value), "f")


def _signed_percent(pattern: str, text: str) -> tuple[str, str] | None:
    match = re.search(pattern, text, flags=re.S)
    if not match:
        return None
    direction = match.group(1)
    raw = Decimal(match.group(2))
    if direction in {"下降", "下跌"} and raw > 0:
        raw = -raw
    return format(raw, "f"), normalize_whitespace(match.group(0))


def _positive_percent(pattern: str, text: str) -> tuple[str, str] | None:
    match = re.search(pattern, text, flags=re.S)
    if not match:
        return None
    return _decimal(match.group(1)), normalize_whitespace(match.group(0))


def _article_date(url: str) -> str | None:
    match = ARTICLE_RE.match(url)
    if not match:
        return None
    year, month, day, _ = match.groups()
    return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"


def _is_economic_candidate(title: str) -> bool:
    clean = normalize_whitespace(title)
    return "徐州" in clean and any(marker in clean for marker in ECONOMIC_TITLE_MARKERS)


def extract_xuzhou_macro_metrics(*, text: str, source_url: str, publication_date: str | None) -> list[dict[str, Any]]:
    """Extract only explicit metrics from an official-mirror Xuzhou release."""
    metrics: list[dict[str, Any]] = []

    def add(signal_id: str, value: str, unit: str, kind: str, matched_text: str) -> None:
        metrics.append(
            {
                "signal_id": signal_id,
                "source_id": SOURCE_ID,
                "geography": "Xuzhou",
                "period": publication_date,
                "metric_kind": kind,
                "unit": unit,
                "value": value,
                "source_url": source_url,
                "matched_text": matched_text,
            }
        )

    gdp = re.search(
        r"(?:实现)?地区生产总值\s*([0-9]+(?:\.[0-9]+)?)亿元[^。；;]{0,80}?同比(增长|下降)([0-9]+(?:\.[0-9]+)?)%",
        text,
        flags=re.S,
    )
    if gdp:
        add("XZ_GDP", _decimal(gdp.group(1)), "100m_cny", "absolute", normalize_whitespace(gdp.group(0)))
        yoy = Decimal(gdp.group(3))
        if gdp.group(2) == "下降" and yoy > 0:
            yoy = -yoy
        add("XZ_GDP_YOY", format(yoy, "f"), "%", "yoy_growth", normalize_whitespace(gdp.group(0)))

    specs = [
        ("XZ_PRIMARY_YOY", r"第一产业增加值[^。；;]{0,40}?(增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
        ("XZ_SECONDARY_YOY", r"第二产业增加值[^。；;]{0,40}?(增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
        ("XZ_TERTIARY_YOY", r"第三产业增加值[^。；;]{0,40}?(增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
        ("XZ_INDUSTRIAL_VALUE_ADDED_YOY", r"规模以上工业增加值[^。；;]{0,40}?同比?(增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
        ("XZ_SERVICE_REVENUE_YOY", r"规模以上服务业营业收入[^。；;]{0,40}?同比?(增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
        ("XZ_RETAIL_YOY", r"社会消费品零售总额[^。；;]{0,40}?同比?(增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
        ("XZ_INCOME_YOY", r"全市全体居民人均可支配收入[^。；;]{0,40}?同比?(增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
        ("XZ_URBAN_INCOME_YOY", r"城镇居民人均可支配收入[^。；;]{0,40}?同比?(增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
        ("XZ_RURAL_INCOME_YOY", r"农村居民人均可支配收入[^。；;]{0,40}?同比?(增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
        ("XZ_CPI_YOY", r"居民消费价格指数CPI[^。；;]{0,40}?(上涨|增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
        ("XZ_INFO_SOFTWARE_YOY", r"信息传输、软件和信息技术服务业增加值[^。；;]{0,40}?同比?(增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
        ("XZ_RENTAL_BUSINESS_YOY", r"租赁和商务服务业增加值[^。；;]{0,40}?同比?(增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
        ("XZ_FINANCE_YOY", r"金融业增加值[^。；;]{0,40}?同比?(增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
        ("XZ_ONLINE_GOODS_RETAIL_YOY", r"(?:线上单位|限额以上单位)[^。；;]{0,50}?公共网络[^。；;]{0,50}?商品零售额[^。；;]{0,40}?同比?(增长|下降)([0-9]+(?:\.[0-9]+)?)%"),
    ]
    for signal_id, pattern in specs:
        parsed = _signed_percent(pattern, text)
        if parsed:
            value, matched = parsed
            add(signal_id, value, "%", "yoy_growth", matched)

    narrowing = _positive_percent(
        r"固定资产投资降幅较[^。；;]{0,20}?收窄([0-9]+(?:\.[0-9]+)?)个百分点",
        text,
    )
    if narrowing:
        value, matched = narrowing
        add("XZ_FIXED_INVESTMENT_DECLINE_NARROWING", value, "percentage_point", "momentum_change", matched)

    structure = re.search(
        r"三次产业结构比例[^0-9]{0,20}?([0-9]+(?:\.[0-9]+)?):([0-9]+(?:\.[0-9]+)?):([0-9]+(?:\.[0-9]+)?)",
        text,
    )
    if structure:
        matched = normalize_whitespace(structure.group(0))
        for signal_id, raw in zip(
            ("XZ_PRIMARY_SHARE", "XZ_SECONDARY_SHARE", "XZ_TERTIARY_SHARE"),
            structure.groups(),
        ):
            add(signal_id, _decimal(raw), "%", "structure_share", matched)

    return metrics


class XuzhouMacroMirrorAdapter:
    def __init__(self, client: PublicHtmlClient | None = None) -> None:
        self.client = client or PublicHtmlClient(
            source_id=SOURCE_ID,
            allowed_hosts={HOST},
            timeout_seconds=30,
            retries=2,
            max_response_bytes=5_000_000,
        )

    def discover_latest(self, *, max_pages: int = 35) -> dict[str, Any]:
        if max_pages <= 0 or max_pages > 60:
            raise ValueError("max_pages must be between 1 and 60")
        seen: set[str] = set()
        page_diagnostics: list[dict[str, Any]] = []
        for page in range(1, max_pages + 1):
            url = COLUMN_URL if page == 1 else PAGE_URL.format(page=page)
            env = self.client.fetch(url, request_name=f"js-gov.local-dynamics.page-{page}")
            doc = html_to_document(env.html, base_url=url)
            article_count = 0
            candidates: list[dict[str, str]] = []
            for link in doc["links"]:
                link_url = str(link.get("url", "")).strip()
                title = normalize_whitespace(str(link.get("text", "")))
                if not ARTICLE_RE.match(link_url):
                    continue
                article_count += 1
                if link_url in seen:
                    continue
                seen.add(link_url)
                if _is_economic_candidate(title):
                    candidates.append(
                        {
                            "title": title,
                            "url": link_url,
                            "publication_date": _article_date(link_url) or "",
                        }
                    )
            page_diagnostics.append(
                {
                    "page": page,
                    "url": env.url,
                    "link_count": len(doc["links"]),
                    "article_link_count": article_count,
                    "candidate_count": len(candidates),
                    "payload_sha256": env.metadata()["payload_sha256"],
                }
            )
            for candidate in candidates:
                try:
                    detail = self.fetch_release(candidate["url"], fallback_title=candidate["title"])
                except ValueError:
                    continue
                return {
                    "source_id": SOURCE_ID,
                    "candidate": candidate,
                    "release": detail,
                    "pages_scanned": page,
                    "page_diagnostics": page_diagnostics,
                }
        raise ValueError(
            "no verified Xuzhou economic release found in bounded Jiangsu-government column scan; "
            f"pages_scanned={max_pages}; diagnostics={page_diagnostics[-3:]}"
        )

    def fetch_release(self, url: str, *, fallback_title: str | None = None) -> dict[str, Any]:
        parsed = urlparse(url)
        if parsed.scheme != "https" or (parsed.hostname or "").lower() != HOST or not ARTICLE_RE.match(url):
            raise ValueError("URL is not an official Jiangsu-government local-dynamics article")
        env = self.client.fetch(url, request_name="js-gov.xuzhou-macro.detail")
        doc = html_to_document(env.html, base_url=url)
        text = doc["text"]
        if not SOURCE_MARKER_RE.search(text):
            raise ValueError("mirror article does not explicitly identify 徐州市政府办公室 as source")
        title = fallback_title or doc["title"]
        if not _is_economic_candidate(title):
            raise ValueError("mirror article is not a Xuzhou economic-release candidate")
        publication_date = _article_date(url)
        metrics = extract_xuzhou_macro_metrics(
            text=text,
            source_url=env.url,
            publication_date=publication_date,
        )
        if not {item["signal_id"] for item in metrics}.issuperset({"XZ_GDP", "XZ_GDP_YOY"}):
            raise ValueError("verified Xuzhou mirror article lacks required GDP core metrics")
        return {
            "source_id": SOURCE_ID,
            "mirror_owner": "江苏省人民政府",
            "original_attribution": "徐州市政府办公室",
            "statistics_attribution": "徐州市统计局",
            "title": title,
            "url": env.url,
            "publication_date": publication_date,
            "metrics": metrics,
            "metric_count": len(metrics),
            "provenance": env.metadata(),
        }

    def collect_latest(self, *, max_pages: int = 35) -> dict[str, Any]:
        discovery = self.discover_latest(max_pages=max_pages)
        release = discovery["release"]
        pub = release.get("publication_date")
        age_days = None
        freshness = "UNKNOWN"
        if pub:
            age_days = max(0, (datetime.now(timezone.utc).date() - date.fromisoformat(pub)).days)
            freshness = "FRESH" if age_days <= 90 else "AGING" if age_days <= 180 else "STALE"
        return {
            "source_id": SOURCE_ID,
            "collected_at_utc": datetime.now(timezone.utc).isoformat(),
            "data_available": True,
            "release": release,
            "freshness": {"age_days": age_days, "status": freshness},
            "discovery": {
                "pages_scanned": discovery["pages_scanned"],
                "page_diagnostics": discovery["page_diagnostics"],
            },
            "truth_note": (
                "This is an official Jiangsu-government mirror whose detail page explicitly attributes "
                "the content to 徐州市政府办公室. It is not represented as a direct xz.gov.cn source. "
                "Only explicit metrics are parsed; relative investment-improvement language remains a momentum metric."
            ),
        }
