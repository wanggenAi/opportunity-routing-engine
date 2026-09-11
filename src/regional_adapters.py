"""Regional public-data adapters for Jiangsu and Xuzhou.

These adapters deliberately separate evidence acquisition from commercial inference:
- Jiangsu statistics releases are official macro/provincial evidence documents.
- Xuzhou procurement notices are institutional money-flow / task-demand events.

Neither source by itself proves a private-market business opportunity.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from decimal import Decimal, InvalidOperation
from typing import Any, Iterable
from urllib.parse import urlparse

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace


JS_STATS_HOST = "tj.jiangsu.gov.cn"
XZ_GGZY_HOST = "ggzy.zwb.xz.gov.cn"
XZ_PROCUREMENT_LIST = "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004002/list.html"


@dataclass(frozen=True)
class OfficialDocument:
    source_id: str
    title: str
    url: str
    publication_date: str | None
    text: str
    provenance: dict[str, Any]


@dataclass(frozen=True)
class ProcurementEvent:
    source_id: str
    title: str
    url: str
    publication_date: str | None
    project_id: str | None
    project_name: str | None
    procurement_method: str | None
    budget_rmb: str | None
    budget_raw: str | None
    deadline: str | None
    contract_term: str | None
    joint_venture_allowed: str | None
    provenance: dict[str, Any]


def _first(pattern: str, text: str, flags: int = 0) -> str | None:
    match = re.search(pattern, text, flags)
    return normalize_whitespace(match.group(1)) if match else None


def _publication_date(text: str, url: str = "") -> str | None:
    for pattern in (
        r"信息发布时间[：:\s]*([0-9]{4}[-年][0-9]{1,2}[-月][0-9]{1,2}日?)",
        r"([0-9]{4}-[0-9]{2}-[0-9]{2})\s+(?:来源|发布|$)",
        r"([0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日)",
    ):
        value = _first(pattern, text)
        if value:
            digits = re.findall(r"\d+", value)
            if len(digits) >= 3:
                return f"{int(digits[0]):04d}-{int(digits[1]):02d}-{int(digits[2]):02d}"
    match = re.search(r"/(20\d{6})/", url)
    if match:
        raw = match.group(1)
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"
    return None


def _money_to_rmb(raw_number: str | None, unit: str | None) -> str | None:
    if not raw_number:
        return None
    try:
        value = Decimal(raw_number.replace(",", ""))
    except InvalidOperation:
        return None
    unit = unit or "元"
    multiplier = Decimal("1")
    if "亿元" in unit:
        multiplier = Decimal("100000000")
    elif "万元" in unit:
        multiplier = Decimal("10000")
    result = value * multiplier
    return format(result.quantize(Decimal("0.01")), "f")


class JiangsuStatsReleaseAdapter:
    """Fetch and normalize one official Jiangsu statistics release."""

    def __init__(self, client: PublicHtmlClient | None = None) -> None:
        self.client = client or PublicHtmlClient(
            source_id="JS_STATS",
            allowed_hosts={JS_STATS_HOST},
            timeout_seconds=30,
            retries=2,
        )

    def fetch_release(self, url: str) -> OfficialDocument:
        if (urlparse(url).hostname or "").lower() != JS_STATS_HOST:
            raise ValueError("JiangsuStatsReleaseAdapter only accepts tj.jiangsu.gov.cn")
        envelope = self.client.fetch(url, request_name="js_stats.release")
        doc = html_to_document(envelope.html, base_url=url)
        text = doc["text"]
        title = self._best_title(doc["title"], text)
        return OfficialDocument(
            source_id="JS_STATS",
            title=title,
            url=url,
            publication_date=_publication_date(text, url),
            text=text,
            provenance=envelope.metadata(),
        )

    @staticmethod
    def _best_title(html_title: str, text: str) -> str:
        for line in text.splitlines()[:30]:
            if "经济运行" in line and len(line) <= 80:
                return line
        return html_title

    @staticmethod
    def extract_money_flow_metrics(document: OfficialDocument) -> list[dict[str, Any]]:
        """Extract a bounded set of stable provincial macro metrics.

        Patterns are intentionally explicit. Unmatched prose remains source evidence
        rather than being guessed into a metric.
        """

        text = document.text
        specs = [
            ("JS_INDUSTRIAL_VALUE_ADDED_YOY", r"规模以上工业增加值同比(?:增长|下降)([-+]?\d+(?:\.\d+)?)%", "yoy_growth"),
            ("JS_SERVICE_REVENUE_YOY", r"规模以上服务业营业收入同比(?:增长|下降)([-+]?\d+(?:\.\d+)?)%", "yoy_growth"),
            ("JS_FIXED_INVESTMENT_YOY", r"固定资产投资同比(?:增长|下降)([-+]?\d+(?:\.\d+)?)%", "yoy_growth"),
            ("JS_EQUIPMENT_INVESTMENT_YOY", r"设备工器具购置投资同比(?:增长|下降)([-+]?\d+(?:\.\d+)?)%", "yoy_growth"),
            ("JS_RETAIL_YOY", r"社会消费品零售总额(?:同比)?(?:增长|下降)([-+]?\d+(?:\.\d+)?)%", "yoy_growth"),
            ("JS_CPI_YOY", r"居民消费价格(?:同比)?(?:上涨|增长|下降)([-+]?\d+(?:\.\d+)?)%", "yoy_growth"),
        ]
        result: list[dict[str, Any]] = []
        for signal_id, pattern, metric_kind in specs:
            match = re.search(pattern, text)
            if not match:
                continue
            value = Decimal(match.group(1))
            local = match.group(0)
            if "下降" in local and value > 0:
                value = -value
            result.append(
                {
                    "signal_id": signal_id,
                    "source_id": document.source_id,
                    "geography": "Jiangsu",
                    "period": document.publication_date,
                    "metric_kind": metric_kind,
                    "unit": "%",
                    "value": format(value, "f"),
                    "source_url": document.url,
                    "provenance_sha256": document.provenance["payload_sha256"],
                    "matched_text": local,
                }
            )
        return result


class XuzhouProcurementAdapter:
    """Discover and parse bounded Xuzhou government-procurement notices."""

    DETAIL_RE = re.compile(
        r"/jyxx/003004/003004002/(20\d{6})/[0-9a-fA-F-]+\.html(?:\?.*)?$"
    )

    def __init__(self, client: PublicHtmlClient | None = None) -> None:
        self.client = client or PublicHtmlClient(
            source_id="XZ_GGZY",
            allowed_hosts={XZ_GGZY_HOST},
            timeout_seconds=30,
            retries=2,
        )

    def discover_recent(self, *, list_url: str = XZ_PROCUREMENT_LIST, limit: int = 30) -> dict[str, Any]:
        if limit <= 0 or limit > 200:
            raise ValueError("limit must be between 1 and 200")
        envelope = self.client.fetch(list_url, request_name="xz_ggzy.procurement.list")
        doc = html_to_document(envelope.html, base_url=list_url)
        seen: set[str] = set()
        items: list[dict[str, Any]] = []
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
            "source_id": "XZ_GGZY",
            "list_url": list_url,
            "item_count": len(items),
            "items": items,
            "provenance": envelope.metadata(),
        }

    def fetch_event(self, url: str, *, fallback_title: str | None = None) -> ProcurementEvent:
        if not self.DETAIL_RE.search(url):
            raise ValueError("URL is not a Xuzhou government-procurement purchase notice")
        envelope = self.client.fetch(url, request_name="xz_ggzy.procurement.detail")
        doc = html_to_document(envelope.html, base_url=url)
        text = doc["text"]
        title = self._best_title(text, doc["title"], fallback_title)
        budget_match = re.search(
            r"预算金额[：:\s]*([0-9][0-9,]*(?:\.\d+)?)\s*(亿元|万元|元)", text
        )
        budget_number = budget_match.group(1) if budget_match else None
        budget_unit = budget_match.group(2) if budget_match else None
        budget_raw = budget_match.group(0) if budget_match else None
        return ProcurementEvent(
            source_id="XZ_GGZY",
            title=title,
            url=url,
            publication_date=_publication_date(text, url),
            project_id=_first(r"项目编号[：:\s]*([^\n]+)", text),
            project_name=_first(r"项目名称[：:\s]*([^\n]+)", text),
            procurement_method=_first(r"采购方式[：:\s]*([^\n]+)", text),
            budget_rmb=_money_to_rmb(budget_number, budget_unit),
            budget_raw=budget_raw,
            deadline=_first(
                r"(?:提交响应文件|提交投标文件|响应文件提交)[^\n]*?截止时间[：:\s]*([^\n]+)",
                text,
            ) or _first(r"截止时间[：:\s]*([^\n]+)", text),
            contract_term=_first(r"合同履行期限[：:\s]*([^\n]+)", text),
            joint_venture_allowed=_first(r"本项目[^\n]{0,20}接受联合体[：:\s]*([^\n]+)", text),
            provenance=envelope.metadata(),
        )

    @staticmethod
    def _best_title(text: str, html_title: str, fallback: str | None) -> str:
        for line in text.splitlines()[:30]:
            if any(marker in line for marker in ("采购公告", "招标公告", "磋商公告")) and len(line) <= 160:
                return line
        return fallback or html_title

    def collect_recent_events(self, *, limit: int = 10) -> dict[str, Any]:
        discovery = self.discover_recent(limit=limit)
        events: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []
        for item in discovery["items"]:
            try:
                event = self.fetch_event(item["url"], fallback_title=item["title"])
                events.append(asdict(event))
            except Exception as exc:  # per-item evidence failure must not erase the batch
                errors.append({"url": item["url"], "error": str(exc)})
        return {
            "source_id": "XZ_GGZY",
            "discovery": discovery,
            "event_count": len(events),
            "error_count": len(errors),
            "events": events,
            "errors": errors,
        }
