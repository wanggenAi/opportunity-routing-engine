"""Xuzhou public construction-tender capital-flow evidence.

The Xuzhou Public Resources Trading Center publishes a stable public list of
construction tender notices.  These notices expose project-level evidence such as
contract estimates, funding sources, owners and tenderers.  They are useful for
answering where institutional/local capital expenditure is being routed, but they
do *not* by themselves prove a commercial opportunity, unmet need or surplus
resource.

Truth boundaries:
- a tender notice is a planned/solicited spend event, not a completed payment;
- re-issued notices are marked and must not be summed as new money;
- missing amount/funding fields remain ``None``;
- project total investment is never substituted for tender contract estimate;
- only the official Xuzhou public-resources HTTPS host is accepted.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from typing import Any
from urllib.parse import urlparse

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace
from src.regional_adapters import _publication_date


SOURCE_ID = "XZ_GGZY"
HOST = "ggzy.zwb.xz.gov.cn"
LIST_URL = "https://ggzy.zwb.xz.gov.cn/jyxx/003001/003001001/list.html"
_DETAIL_RE = re.compile(
    r"^/jyxx/003001/003001001/(20\d{6})/[0-9a-fA-F-]+\.html$"
)
_REISSUE_RE = re.compile(r"(?:重发公告|再次公告|二次公告|三次公告|四次公告|重新招标)")


@dataclass(frozen=True)
class ConstructionTenderEvent:
    source_id: str
    event_kind: str
    title: str
    url: str
    publication_date: str | None
    project_owner: str | None
    tenderer: str | None
    funding_source: str | None
    contract_estimate_rmb: str | None
    contract_estimate_raw: str | None
    estimate_basis: str | None
    location: str | None
    is_reissue: bool
    evidence_state: str
    provenance: dict[str, Any]


def _official_detail_date(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != HOST:
        return None
    match = _DETAIL_RE.match(parsed.path)
    if not match:
        return None
    raw = match.group(1)
    return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"


def _first(pattern: str, text: str, flags: int = 0) -> str | None:
    match = re.search(pattern, text, flags)
    if not match:
        return None
    value = normalize_whitespace(match.group(1)).strip(" ：:，,。；;")
    return value or None


def _money_to_rmb(number: str, unit: str) -> str:
    try:
        value = Decimal(number.replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError(f"invalid contract estimate number: {number!r}") from exc
    if value <= 0:
        raise ValueError(f"contract estimate must be positive: {number!r}")
    multiplier = {
        "元": Decimal("1"),
        "万元": Decimal("10000"),
        "亿元": Decimal("100000000"),
    }[unit]
    return format((value * multiplier).quantize(Decimal("0.01")), "f")


def _extract_contract_estimate(text: str) -> tuple[str | None, str | None, str | None]:
    """Return tender-level contract estimate only; never use project total investment."""
    explicit = re.search(
        r"(?:工程)?合同估算价\s*[：:]?\s*(?:约\s*)?"
        r"([0-9][0-9,]*(?:\.\d+)?)\s*(亿元|万元|元)",
        text,
    )
    if explicit:
        raw = normalize_whitespace(explicit.group(0))
        return _money_to_rmb(explicit.group(1), explicit.group(2)), raw, "EXPLICIT_UNIT"

    implied_wan = re.search(
        r"(?:工程)?合同估算价\s*[（(]\s*万元\s*[）)]\s*[：:]?\s*"
        r"(?:约\s*)?([0-9][0-9,]*(?:\.\d+)?)",
        text,
    )
    if implied_wan:
        raw = normalize_whitespace(implied_wan.group(0))
        return _money_to_rmb(implied_wan.group(1), "万元"), raw, "HEADER_UNIT_WAN_CNY"

    return None, None, None


def _evidence_state(amount: str | None, funding: str | None) -> str:
    if amount is not None and funding is not None:
        return "AMOUNT_AND_FUNDING_SOURCE"
    if amount is not None:
        return "AMOUNT_ONLY"
    if funding is not None:
        return "FUNDING_SOURCE_ONLY"
    return "NOTICE_ONLY"


class XuzhouConstructionTenderAdapter:
    def __init__(self, client: PublicHtmlClient | None = None) -> None:
        self.client = client or PublicHtmlClient(
            source_id=SOURCE_ID,
            allowed_hosts={HOST},
            timeout_seconds=30,
            retries=2,
            max_response_bytes=5_000_000,
        )

    def discover_recent(self, *, limit: int = 20) -> dict[str, Any]:
        if limit <= 0 or limit > 100:
            raise ValueError("limit must be between 1 and 100")
        env = self.client.fetch(LIST_URL, request_name="xz_ggzy.construction.list")
        doc = html_to_document(env.html, base_url=env.url)
        items: list[dict[str, str]] = []
        seen: set[str] = set()
        for link in doc.get("links", []):
            url = str(link.get("url", "")).strip()
            publication_date = _official_detail_date(url)
            if publication_date is None or url in seen:
                continue
            seen.add(url)
            title = re.sub(r"^\[?新\]?", "", normalize_whitespace(str(link.get("text", "")))).strip()
            if not title:
                continue
            items.append(
                {
                    "title": title,
                    "url": url,
                    "publication_date": publication_date,
                }
            )
            if len(items) >= limit:
                break
        return {
            "source_id": SOURCE_ID,
            "event_kind": "CONSTRUCTION_TENDER_NOTICE",
            "list_url": LIST_URL,
            "item_count": len(items),
            "items": items,
            "provenance": env.metadata(),
        }

    def fetch_event(
        self,
        url: str,
        *,
        fallback_title: str | None = None,
    ) -> ConstructionTenderEvent:
        url_date = _official_detail_date(url)
        if url_date is None:
            raise ValueError("URL is not an official Xuzhou construction tender notice")
        env = self.client.fetch(url, request_name="xz_ggzy.construction.detail")
        doc = html_to_document(env.html, base_url=env.url)
        text = doc["text"]
        title = self._best_title(doc.get("title", ""), text, fallback_title)
        page_date = _publication_date(text, url)
        if page_date is not None and page_date != url_date:
            raise ValueError(
                f"construction notice publication date conflicts with URL: {page_date} != {url_date}"
            )

        amount, amount_raw, estimate_basis = _extract_contract_estimate(text)
        funding = _first(r"建设资金来自\s*([^，。；\n]{1,80})", text)
        owner = _first(r"项目业主为\s*([^，。；\n]{1,100})", text)
        tenderer = _first(r"招标人为\s*([^，。；\n]{1,100})", text)
        location = _first(r"建设地点\s*[：:]\s*([^。；\n]{1,120})", text)

        return ConstructionTenderEvent(
            source_id=SOURCE_ID,
            event_kind="CONSTRUCTION_TENDER_NOTICE",
            title=title,
            url=url,
            publication_date=page_date or url_date,
            project_owner=owner,
            tenderer=tenderer,
            funding_source=funding,
            contract_estimate_rmb=amount,
            contract_estimate_raw=amount_raw,
            estimate_basis=estimate_basis,
            location=location,
            is_reissue=bool(_REISSUE_RE.search(title) or _REISSUE_RE.search(text[:600])),
            evidence_state=_evidence_state(amount, funding),
            provenance=env.metadata(),
        )

    @staticmethod
    def _best_title(html_title: str, text: str, fallback: str | None) -> str:
        lines = [normalize_whitespace(line) for line in text.splitlines()[:35]]
        for line in lines:
            if not line or len(line) > 180:
                continue
            if any(token in line for token in ("招标公告", "资审公告")):
                continue
            if line in {"建设工程", "招标公告/资审公告"}:
                continue
            if fallback and fallback.replace("[新]", "") in line:
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
            except Exception as exc:
                errors.append({"url": item["url"], "error": str(exc)})

        return {
            "source_id": SOURCE_ID,
            "event_kind": "CONSTRUCTION_TENDER_NOTICE",
            "discovery": discovery,
            "event_count": len(events),
            "error_count": len(errors),
            "amount_evidence_count": sum(
                1 for event in events if event["contract_estimate_rmb"] is not None
            ),
            "funding_evidence_count": sum(
                1 for event in events if event["funding_source"] is not None
            ),
            "reissue_count": sum(1 for event in events if event["is_reissue"]),
            "events": events,
            "errors": errors,
            "aggregation_policy": (
                "NO_SUM_WITHOUT_PROJECT_DEDUP: tender estimates are event evidence only; "
                "reissues and multi-lot notices can repeat the same underlying capital project."
            ),
        }
