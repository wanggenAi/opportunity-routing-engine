"""Official PBC money-flow release discovery and parsing.

The People's Bank of China exposes a stable public HTML index for statistical
interpretation releases. This adapter discovers the newest financial-statistics
report from that official index, fetches the report, and extracts a deliberately
small set of macro money-flow indicators while preserving source provenance.

Truth rules:
- newest visible official release != today's data;
- missing metric != zero;
- parser failure != economic observation;
- no search-engine/private endpoint is used for production discovery.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timezone
from typing import Any

from src.html_ingest import PublicHtmlClient, html_to_document


SOURCE_ID = "CN_PBOC"
INDEX_URL = "https://www.pbc.gov.cn/diaochatongjisi/116219/116225/index.html"
ALLOWED_HOSTS = {"www.pbc.gov.cn"}

_REPORT_TITLE_RE = re.compile(r"^\d{4}年.+金融统计数据报告$")
_RELEASE_DATE_RE = re.compile(r"文章来源[:：]?\s*(\d{4}-\d{2}-\d{2})")
_M2 = r"广义货币\s*[（(]\s*M2\s*[）)]"
_M1 = r"狭义货币\s*[（(]\s*M1\s*[）)]"
_M0 = r"流通中货币\s*[（(]\s*M0\s*[）)]"


def _number(pattern: str, text: str) -> float | None:
    match = re.search(pattern, text, flags=re.S)
    return float(match.group(1)) if match else None


def _signed_yoy(label: str, text: str) -> float | None:
    pattern = rf"{label}.*?同比(增长|下降)([0-9.]+)%"
    match = re.search(pattern, text, flags=re.S)
    if not match:
        return None
    value = float(match.group(2))
    return -value if match.group(1) == "下降" else value


def discover_latest_financial_report(index_document: dict[str, Any]) -> dict[str, str]:
    """Return the first financial-statistics report from the official newest-first index."""
    for link in index_document.get("links", []):
        title = str(link.get("text", "")).strip()
        url = str(link.get("url", "")).strip()
        if _REPORT_TITLE_RE.match(title) and url.startswith("https://www.pbc.gov.cn/"):
            return {"title": title, "url": url}
    raise ValueError("no PBC financial-statistics report found on official index")


def parse_financial_report(*, title: str, text: str, source_url: str) -> dict[str, Any]:
    release_match = _RELEASE_DATE_RE.search(text)
    release_date = release_match.group(1) if release_match else None

    metrics: dict[str, dict[str, Any]] = {}

    def add(key: str, value: float | None, unit: str, *, yoy: float | None = None) -> None:
        if value is None:
            return
        item: dict[str, Any] = {"value": value, "unit": unit}
        if yoy is not None:
            item["yoy_pct"] = yoy
        metrics[key] = item

    add(
        "social_financing_stock",
        _number(r"社会融资规模存量为\s*([0-9.]+)万亿元", text),
        "trillion_cny",
        yoy=_number(r"社会融资规模存量为\s*[0-9.]+万亿元.*?同比增长\s*([0-9.]+)%", text),
    )
    add(
        "social_financing_flow_ytd",
        _number(r"社会融资规模增量累计为\s*([0-9.]+)万亿元", text),
        "trillion_cny",
    )
    add(
        "m2_balance",
        _number(rf"{_M2}\s*余额为?\s*([0-9.]+)万亿元", text),
        "trillion_cny",
        yoy=_signed_yoy(_M2, text),
    )
    add(
        "m1_balance",
        _number(rf"{_M1}\s*余额为?\s*([0-9.]+)万亿元", text),
        "trillion_cny",
        yoy=_signed_yoy(_M1, text),
    )
    add(
        "m0_balance",
        _number(rf"{_M0}\s*余额为?\s*([0-9.]+)万亿元", text),
        "trillion_cny",
        yoy=_signed_yoy(_M0, text),
    )
    add(
        "rmb_deposit_flow_ytd",
        _number(r"人民币存款增加\s*([0-9.]+)万亿元", text),
        "trillion_cny",
    )
    add(
        "rmb_loan_flow_ytd",
        _number(r"人民币贷款增加\s*([0-9.]+)万亿元", text),
        "trillion_cny",
    )
    add(
        "interbank_lending_weighted_rate",
        _number(r"同业拆借月加权平均利率为\s*([0-9.]+)%", text),
        "percent",
    )
    add(
        "pledged_repo_weighted_rate",
        _number(r"质押式债券回购月加权平均利率为\s*([0-9.]+)%", text),
        "percent",
    )
    add(
        "fx_reserves",
        _number(r"国家外汇储备余额\s*([0-9.]+)万亿美元", text),
        "trillion_usd",
    )
    add(
        "usd_cny_reference",
        _number(r"人民币汇率为\s*1美元兑\s*([0-9.]+)元人民币", text),
        "cny_per_usd",
    )

    core = {"social_financing_stock", "social_financing_flow_ytd", "m2_balance", "m1_balance", "m0_balance"}
    core_present = sorted(core.intersection(metrics))
    if len(core_present) < 4:
        raise ValueError(f"PBC report core metrics incomplete: {core_present}")

    return {
        "title": title,
        "source_url": source_url,
        "release_date": release_date,
        "metrics": metrics,
        "metric_count": len(metrics),
        "core_metric_count": len(core_present),
        "core_metrics_present": core_present,
    }


def _freshness(release_date: str | None, *, today: date) -> dict[str, Any]:
    if not release_date:
        return {"age_days": None, "status": "UNKNOWN"}
    released = date.fromisoformat(release_date)
    age = max(0, (today - released).days)
    if age <= 60:
        status = "FRESH"
    elif age <= 120:
        status = "AGING"
    else:
        status = "STALE"
    return {"age_days": age, "status": status}


class PbcMoneyFlowAdapter:
    def __init__(self, *, client: PublicHtmlClient | None = None) -> None:
        self.client = client or PublicHtmlClient(
            source_id=SOURCE_ID,
            allowed_hosts=ALLOWED_HOSTS,
            timeout_seconds=20,
            retries=2,
            max_response_bytes=4_000_000,
        )

    def collect_latest(self) -> dict[str, Any]:
        index_env = self.client.fetch(INDEX_URL, request_name="pbc-statistics-index")
        index_doc = html_to_document(index_env.html, base_url=index_env.url)
        discovered = discover_latest_financial_report(index_doc)

        report_env = self.client.fetch(discovered["url"], request_name="pbc-latest-financial-report")
        report_doc = html_to_document(report_env.html, base_url=report_env.url)
        report = parse_financial_report(
            title=discovered["title"],
            text=report_doc["text"],
            source_url=report_env.url,
        )
        today = datetime.now(timezone.utc).date()
        return {
            "source_id": SOURCE_ID,
            "collected_at_utc": datetime.now(timezone.utc).isoformat(),
            "data_available": True,
            "latest_release": report,
            "freshness": _freshness(report.get("release_date"), today=today),
            "provenance": {
                "index": index_env.metadata(),
                "report": report_env.metadata(),
            },
            "truth_note": (
                "Metrics are parsed from the newest financial-statistics report visible on the "
                "official PBC statistics interpretation index. Missing fields are omitted, never zero-filled."
            ),
        }
