"""Live Jiangsu macro money-flow collector from official statistics releases.

This module upgrades ``JS_STATS`` from a manually supplied release URL to a
bounded official-index discovery path.  The provincial statistics homepage
exposes the newest data-release articles; economic-operation releases live in the
stable ``art_85275`` data-publication column.

The collector preserves a strict boundary between macro evidence and opportunity
claims. Missing metrics remain absent. A negative rate is represented with a
negative value only when the matched official text explicitly says ``下降``.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any
from urllib.parse import urlparse

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace
from src.regional_adapters import JiangsuStatsReleaseAdapter, OfficialDocument


SOURCE_ID = "JS_STATS"
HOST = "tj.jiangsu.gov.cn"
INDEX_URL = "https://tj.jiangsu.gov.cn/"
_DATA_RELEASE_PATH_RE = re.compile(
    r"^/art/(20\d{2})/(\d{1,2})/(\d{1,2})/art_85275_\d+\.html$"
)


def _official_data_release(url: str) -> tuple[str, str, str] | None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != HOST:
        return None
    match = _DATA_RELEASE_PATH_RE.match(parsed.path)
    return match.groups() if match else None


def discover_latest_economic_release(index_document: dict[str, Any]) -> dict[str, str]:
    """Find newest official Jiangsu economic-operation release by URL date."""
    candidates: list[tuple[int, int, int, str, str]] = []
    for link in index_document.get("links", []):
        title = normalize_whitespace(str(link.get("text", "")))
        url = str(link.get("url", "")).strip()
        date_parts = _official_data_release(url)
        if not date_parts or "全省经济运行" not in title:
            continue
        year, month, day = map(int, date_parts)
        candidates.append((year, month, day, title, url))
    if not candidates:
        raise ValueError("no official Jiangsu economic-operation data release found")
    year, month, day, title, url = max(candidates, key=lambda item: item[:3])
    return {
        "title": title,
        "url": url,
        "publication_date_from_url": f"{year:04d}-{month:02d}-{day:02d}",
    }


def _signed_percent(match: re.Match[str]) -> Decimal:
    value = Decimal(match.group(1))
    if "下降" in match.group(0) and value > 0:
        return -value
    return value


def _metric(
    *,
    signal_id: str,
    document: OfficialDocument,
    metric_kind: str,
    unit: str,
    value: Decimal,
    matched_text: str,
) -> dict[str, Any]:
    return {
        "signal_id": signal_id,
        "source_id": document.source_id,
        "geography": "Jiangsu",
        "period": document.publication_date,
        "metric_kind": metric_kind,
        "unit": unit,
        "value": format(value, "f"),
        "source_url": document.url,
        "provenance_sha256": document.provenance["payload_sha256"],
        "matched_text": matched_text,
    }


def extract_jiangsu_money_flow_metrics(document: OfficialDocument) -> list[dict[str, Any]]:
    """Extract bounded official macro/money-flow indicators from one release."""
    text = document.text
    result: list[dict[str, Any]] = []

    percent_specs = [
        (
            "JS_INDUSTRIAL_VALUE_ADDED_YOY",
            r"规模以上工业增加值同比(?:增长|下降)([-+]?\d+(?:\.\d+)?)%",
        ),
        (
            "JS_SERVICE_REVENUE_YOY",
            r"规模以上服务业营业收入同比(?:增长|下降)([-+]?\d+(?:\.\d+)?)%",
        ),
        (
            "JS_FIXED_INVESTMENT_YOY",
            r"固定资产投资同比(?:增长|下降)([-+]?\d+(?:\.\d+)?)%",
        ),
        (
            "JS_MANUFACTURING_INVESTMENT_YOY",
            r"制造业投资(?:同比)?(?:增长|下降)([-+]?\d+(?:\.\d+)?)%",
        ),
        (
            "JS_INFRASTRUCTURE_INVESTMENT_YOY",
            r"基础设施投资(?:同比)?(?:增长|下降)([-+]?\d+(?:\.\d+)?)%",
        ),
        (
            "JS_REAL_ESTATE_INVESTMENT_YOY",
            r"房地产开发投资(?:同比)?(?:增长|下降)([-+]?\d+(?:\.\d+)?)%",
        ),
        (
            "JS_EQUIPMENT_INVESTMENT_YOY",
            r"设备工器具购置投资同比(?:增长|下降)([-+]?\d+(?:\.\d+)?)%",
        ),
        (
            "JS_RETAIL_YOY",
            r"社会消费品零售总额[^。\n]{0,40}?同比(?:增长|下降)([-+]?\d+(?:\.\d+)?)%",
        ),
        (
            "JS_RMB_DEPOSIT_YOY",
            r"人民币存款余额[^；。\n]{0,30}?同比(?:增长|下降)([-+]?\d+(?:\.\d+)?)%",
        ),
        (
            "JS_RMB_LOAN_YOY",
            r"人民币贷款余额[^；。\n]{0,30}?(?:同比)?(?:增长|下降)([-+]?\d+(?:\.\d+)?)%",
        ),
        (
            "JS_CPI_YOY",
            r"居民消费价格同比(?:上涨|增长|下降)([-+]?\d+(?:\.\d+)?)%",
        ),
    ]
    for signal_id, pattern in percent_specs:
        match = re.search(pattern, text)
        if not match:
            continue
        result.append(
            _metric(
                signal_id=signal_id,
                document=document,
                metric_kind="yoy_growth",
                unit="%",
                value=_signed_percent(match),
                matched_text=match.group(0),
            )
        )

    level_specs = [
        (
            "JS_RETAIL_LEVEL_100M_CNY",
            r"社会消费品零售总额\s*([0-9]+(?:\.\d+)?)亿元",
            "100m_cny",
        ),
        (
            "JS_RMB_DEPOSIT_LEVEL_TRILLION_CNY",
            r"人民币存款余额\s*([0-9]+(?:\.\d+)?)万亿元",
            "trillion_cny",
        ),
        (
            "JS_RMB_LOAN_LEVEL_TRILLION_CNY",
            r"人民币贷款余额\s*([0-9]+(?:\.\d+)?)万亿元",
            "trillion_cny",
        ),
    ]
    for signal_id, pattern, unit in level_specs:
        match = re.search(pattern, text)
        if not match:
            continue
        value = Decimal(match.group(1))
        if value <= 0:
            raise ValueError(f"non-positive official level for {signal_id}: {value}")
        result.append(
            _metric(
                signal_id=signal_id,
                document=document,
                metric_kind="level",
                unit=unit,
                value=value,
                matched_text=match.group(0),
            )
        )

    return result


def infer_observation_period(title: str, publication_date: str | None) -> str | None:
    if not publication_date:
        return None
    year = publication_date[:4]
    match = re.search(r"1[—-](\d{1,2})月", title)
    if match:
        month = int(match.group(1))
        return f"{year}-01..{year}-{month:02d}"
    if "上半年" in title:
        return f"{year}-H1"
    if "一季度" in title:
        return f"{year}-Q1"
    if "前三季度" in title:
        return f"{year}-Q1..Q3"
    if "全年" in title:
        return year
    return None


def _freshness(publication_date: str | None) -> dict[str, Any]:
    if not publication_date:
        return {"publication_date": None, "age_days": None, "status": "UNKNOWN"}
    published = date.fromisoformat(publication_date)
    age_days = (datetime.now(timezone.utc).date() - published).days
    if age_days < 0:
        status = "FUTURE_DATE_ERROR"
    elif age_days <= 45:
        status = "FRESH"
    elif age_days <= 90:
        status = "AGING"
    else:
        status = "STALE"
    return {
        "publication_date": publication_date,
        "age_days": age_days,
        "status": status,
    }


class JiangsuMoneyFlowAdapter:
    def __init__(self, client: PublicHtmlClient | None = None) -> None:
        self.client = client or PublicHtmlClient(
            source_id=SOURCE_ID,
            allowed_hosts={HOST},
            timeout_seconds=30,
            retries=2,
            max_response_bytes=5_000_000,
        )

    def collect(self) -> dict[str, Any]:
        index_env = self.client.fetch(INDEX_URL, request_name="js_stats.money_flow.index")
        index_doc = html_to_document(index_env.html, base_url=index_env.url)
        discovered = discover_latest_economic_release(index_doc)

        release = JiangsuStatsReleaseAdapter(client=self.client).fetch_release(discovered["url"])
        if release.publication_date != discovered["publication_date_from_url"]:
            raise ValueError(
                "Jiangsu release publication date conflicts with official URL date: "
                f"{release.publication_date!r} != {discovered['publication_date_from_url']!r}"
            )
        if "经济运行" not in release.title:
            raise ValueError(f"release semantic identity drift: {release.title!r}")

        metrics = extract_jiangsu_money_flow_metrics(release)
        if not metrics:
            raise ValueError("latest Jiangsu economic release produced no recognized metrics")

        return {
            "source_id": SOURCE_ID,
            "collected_at_utc": datetime.now(timezone.utc).isoformat(),
            "data_available": True,
            "geography": "Jiangsu",
            "release_title": release.title,
            "release_url": release.url,
            "publication_date": release.publication_date,
            "observation_period": infer_observation_period(
                release.title,
                release.publication_date,
            ),
            "freshness": _freshness(release.publication_date),
            "metric_count": len(metrics),
            "metrics": metrics,
            "provenance": {
                "index": index_env.metadata(),
                "release": release.provenance,
            },
            "truth_note": (
                "Official Jiangsu macro release evidence only. Metrics are extracted only from "
                "explicit matching text; absent indicators stay absent. Investment/finance movement "
                "does not by itself establish NEED, SURPLUS, BLOCKER or an opportunity."
            ),
        }
