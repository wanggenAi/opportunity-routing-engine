"""Public adapters for observable resource-underuse evidence.

V1 starts with Xuzhou public property-rights listings because they can expose
stronger facts than generic market-presence data:
- an asset/resource is publicly offered for transfer or lease;
- some notices explicitly state the asset is idle/vacant;
- repeated listings are observable allocation/transaction friction.

Important separation:
- a listing proves DISCOVERED market availability, not orchestrator control;
- `闲置`/`空置` in the source can support OBSERVED underuse;
- repeated listing supports observed allocation friction, not by itself underuse;
- neither fact proves a profitable orchestration route.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace


XZ_GGZY_HOST = "ggzy.zwb.xz.gov.cn"
XZ_PROPERTY_RIGHTS_LIST = (
    "https://ggzy.zwb.xz.gov.cn/jyxx/003005/003005003/list.html"
)

_CHINESE_NUMERAL = {
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}


@dataclass(frozen=True)
class PublicAssetListing:
    source_id: str
    title: str
    url: str
    publication_date: str | None
    project_id: str | None
    listing_mode: str
    listing_round: int | None
    relisting_observed: bool
    listing_start: str | None
    listing_end: str | None
    resource_state: str
    underuse_evidence_state: str
    underuse_excerpt: str | None
    asking_price_rmb: str | None
    asking_price_raw: str | None
    location: str | None
    owner_actor: str | None
    provenance: dict[str, Any]


def _first(pattern: str, text: str, flags: int = 0) -> str | None:
    match = re.search(pattern, text, flags)
    return normalize_whitespace(match.group(1)) if match else None


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
        digits = re.findall(r"\d+", value)
        if len(digits) >= 3:
            return f"{int(digits[0]):04d}-{int(digits[1]):02d}-{int(digits[2]):02d}"
    return _date_from_url(url)


def _normalize_title(raw: str) -> str:
    text = normalize_whitespace(raw)
    text = re.sub(r"^\[?新\]?", "", text).strip()
    text = re.sub(r"^\[江苏省[^\]]*\]", "", text).strip()
    text = re.sub(r"^〖交易公告〗", "", text).strip()
    text = re.sub(r"\[(?:正在报名|报名结束)\]$", "", text).strip()
    return text


def _listing_round(text: str) -> int | None:
    patterns = (
        r"[（(]第?([一二两三四五六七八九十\d]+)次[）)]",
        r"第([一二两三四五六七八九十\d]+)次(?:挂牌|拍卖|招租|拍租|转让)",
        r"[（(]([一二两三四五六七八九十\d]+)次挂牌[）)]",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if not match:
            continue
        token = match.group(1)
        if token.isdigit():
            return int(token)
        if token in _CHINESE_NUMERAL:
            return _CHINESE_NUMERAL[token]
    return None


def _listing_mode(text: str) -> str:
    if any(token in text for token in ("招租", "拍租", "租赁权", "出租")):
        return "LEASE"
    if any(token in text for token in ("转让", "拍卖", "出售")):
        return "TRANSFER"
    return "UNKNOWN"


def _money_to_rmb(raw_number: str | None, unit: str | None) -> str | None:
    if not raw_number:
        return None
    try:
        value = Decimal(raw_number.replace(",", ""))
    except InvalidOperation:
        return None
    multiplier = Decimal("1")
    unit = unit or "元"
    if "亿元" in unit:
        multiplier = Decimal("100000000")
    elif "万元" in unit:
        multiplier = Decimal("10000")
    return format((value * multiplier).quantize(Decimal("0.01")), "f")


def _asking_price(text: str) -> tuple[str | None, str | None]:
    patterns = (
        r"(?:转让底价|租金底价|挂牌价格|挂牌价|起拍价|拍租底价|年租金底价)[^\d]{0,30}([0-9][0-9,]*(?:\.\d+)?)\s*(亿元|万元|元)",
        r"(?:转让底价|租金底价|挂牌价格|挂牌价|起拍价|拍租底价|年租金底价)[^\d]{0,30}([0-9][0-9,]*(?:\.\d+)?)\s*(元/年|万元/年)",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if not match:
            continue
        number, unit = match.groups()
        normalized_unit = unit.replace("/年", "")
        return _money_to_rmb(number, normalized_unit), normalize_whitespace(match.group(0))
    return None, None


def _underuse_evidence(text: str) -> tuple[str, str | None]:
    patterns = (
        r"标的资产[^。\n]{0,80}(?:处于)?闲置状态",
        r"标的状态[：:\s]*空置",
        r"房屋现状[^。\n]{0,80}空置",
        r"目前[^。\n]{0,80}(?:闲置|空置)",
        # Explicit source wording such as "闲置资产整体转让" is itself a direct
        # state assertion. Keep this bounded to concrete asset nouns so generic
        # narrative mentions of "闲置" do not become observed underuse.
        r"闲置(?:资产|房产|房屋|厂房|设备|土地|场地|商铺|门面|办公用房|用房)",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return "OBSERVED", normalize_whitespace(match.group(0))
    return "UNKNOWN", None


class XuzhouPublicAssetAdapter:
    """Discover and normalize bounded Xuzhou property-rights listings."""

    DETAIL_RE = re.compile(
        r"/jyxx/003005/003005003/(20\d{6})/[0-9a-fA-F-]+\.html(?:\?.*)?$"
    )

    def __init__(self, client: PublicHtmlClient | None = None) -> None:
        self.client = client or PublicHtmlClient(
            source_id="XZ_GGZY",
            allowed_hosts={XZ_GGZY_HOST},
            timeout_seconds=30,
            retries=2,
        )

    def discover_recent(
        self,
        *,
        list_url: str = XZ_PROPERTY_RIGHTS_LIST,
        limit: int = 30,
    ) -> dict[str, Any]:
        if limit <= 0 or limit > 200:
            raise ValueError("limit must be between 1 and 200")
        envelope = self.client.fetch(
            list_url,
            request_name="xz_ggzy.property_rights.list",
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
            title = _normalize_title(link["text"])
            round_number = _listing_round(title)
            items.append(
                {
                    "title": title,
                    "url": url,
                    "publication_date": f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}",
                    "listing_mode": _listing_mode(title),
                    "listing_round": round_number,
                    "relisting_observed": bool(round_number and round_number >= 2),
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

    def fetch_listing(
        self,
        url: str,
        *,
        fallback_title: str | None = None,
    ) -> PublicAssetListing:
        if not self.DETAIL_RE.search(url):
            raise ValueError("URL is not a Xuzhou property-rights listing")
        envelope = self.client.fetch(
            url,
            request_name="xz_ggzy.property_rights.detail",
        )
        doc = html_to_document(envelope.html, base_url=url)
        text = doc["text"]
        title = self._best_title(text, doc["title"], fallback_title)
        round_number = _listing_round(title + " " + text[:1200])
        underuse_state, underuse_excerpt = _underuse_evidence(text)
        asking_price_rmb, asking_price_raw = _asking_price(text)
        return PublicAssetListing(
            source_id="XZ_GGZY",
            title=title,
            url=url,
            publication_date=_publication_date(text, url),
            project_id=_first(r"项目编号[：:\s]*([^\n]+)", text),
            listing_mode=_listing_mode(title + " " + text[:1200]),
            listing_round=round_number,
            relisting_observed=bool(round_number and round_number >= 2),
            listing_start=_first(r"挂牌起始日期[：:\s]*([0-9]{4}[-年][0-9]{1,2}[-月][0-9]{1,2}日?)", text),
            listing_end=_first(r"挂牌截止日期[：:\s]*([0-9]{4}[-年][0-9]{1,2}[-月][0-9]{1,2}日?)", text),
            resource_state="DISCOVERED",
            underuse_evidence_state=underuse_state,
            underuse_excerpt=underuse_excerpt,
            asking_price_rmb=asking_price_rmb,
            asking_price_raw=asking_price_raw,
            location=(
                _first(r"存放地[：:\s]*([^\n]+)", text)
                or _first(r"标的坐落[：:\s]*([^\n]+)", text)
            ),
            owner_actor=(
                _first(r"转让方名称[：:\s]*([^\n]+)", text)
                or _first(r"出租方名称[：:\s]*([^\n]+)", text)
            ),
            provenance=envelope.metadata(),
        )

    @staticmethod
    def _best_title(text: str, html_title: str, fallback: str | None) -> str:
        for line in text.splitlines()[:40]:
            line = normalize_whitespace(line)
            if len(line) > 180:
                continue
            if any(token in line for token in ("转让", "招租", "拍租", "拍卖")):
                return _normalize_title(line)
        return _normalize_title(fallback or html_title)

    def collect_recent(self, *, limit: int = 20) -> dict[str, Any]:
        discovery = self.discover_recent(limit=limit)
        listings: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []
        for item in discovery["items"]:
            try:
                listing = self.fetch_listing(
                    item["url"],
                    fallback_title=item["title"],
                )
                listings.append(asdict(listing))
            except Exception as exc:  # one bad detail must not erase the batch
                errors.append({"url": item["url"], "error": str(exc)})

        observed_underuse = sum(
            1
            for item in listings
            if item["underuse_evidence_state"] == "OBSERVED"
        )
        relistings = sum(1 for item in listings if item["relisting_observed"])
        return {
            "source_id": "XZ_GGZY",
            "discovery": discovery,
            "listing_count": len(listings),
            "error_count": len(errors),
            "observed_underuse_count": observed_underuse,
            "relisting_count": relistings,
            "listings": listings,
            "errors": errors,
            "truth_note": (
                "Explicit idle/vacant text supports observed underuse; relisting supports "
                "allocation friction only. Neither proves a profitable route."
            ),
        }
