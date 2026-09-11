"""Xuzhou agency property-rights feed backed by the official Jiangsu mirror.

The Xuzhou public-resource platform exposes a separate list for notices imported from
legally established property-rights agencies (notably e交易 / 徐州淮海产权服务有限公司).
Those rows can carry a BiaoDuanGuid.  The same GUID/date is mirrored as a static
official Jiangsu public-resource page, which is substantially easier to preserve and
parse than a JavaScript-heavy transaction detail page.

Truth boundaries:
- list row + GUID proves only that a resource listing exists;
- mirror detail must identify Xuzhou as the source before it is treated as Xuzhou evidence;
- explicit 闲置/空置 text is required for OBSERVED underuse;
- repeated listing is allocation friction only;
- no CapabilityUnit or blocker type is inferred from free-form titles.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from html import unescape
from typing import Any
from urllib.parse import urljoin

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace
from src.resource_underuse_adapters import (
    _asking_price,
    _first,
    _listing_mode,
    _listing_round,
    _normalize_title,
    _publication_date,
    _underuse_evidence,
)


XZ_GGZY_HOST = "ggzy.zwb.xz.gov.cn"
JS_GGZY_HOST = "jsggzy.jszwfw.gov.cn"
XZ_AGENCY_LIST = "https://ggzy.zwb.xz.gov.cn/jyxx/003010/003010002/listqtxx.html"
JS_ASSET_MIRROR_PREFIX = "https://jsggzy.jszwfw.gov.cn/jyxx/003006/003006001"
_GUID_RE = re.compile(r"BiaoDuanGuid=([0-9a-fA-F-]{36})", re.I)
_DATE_RE = re.compile(r"20\d{2}-\d{1,2}-\d{1,2}")


@dataclass(frozen=True)
class AgencyAssetListing:
    source_id: str
    discovery_source_id: str
    guid: str
    title: str
    url: str
    discovery_url: str
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
    source_origin_verified: bool
    discovery_provenance: dict[str, Any]
    detail_provenance: dict[str, Any]


def _plain_html_fragment(fragment: str) -> str:
    return normalize_whitespace(unescape(re.sub(r"<[^>]+>", " ", fragment)))


def _date_near_guid(html: str, guid: str, title: str = "") -> str | None:
    idx = html.lower().find(guid.lower())
    if idx >= 0:
        nearby = _plain_html_fragment(html[max(0, idx - 500) : idx + 1400])
        matches = _DATE_RE.findall(nearby)
        if matches:
            return matches[-1]
    if title:
        plain = _plain_html_fragment(html)
        idx = plain.find(title)
        if idx >= 0:
            matches = _DATE_RE.findall(plain[idx : idx + 500])
            if matches:
                return matches[0]
    return None


def _mirror_url(publication_date: str, guid: str) -> str:
    digits = "".join(ch for ch in publication_date if ch.isdigit())
    if len(digits) != 8:
        raise ValueError("publication_date must be YYYY-MM-DD for mirror construction")
    return f"{JS_ASSET_MIRROR_PREFIX}/{digits}/{guid}.html"


def _extract_guid_links(html: str, base_url: str) -> list[tuple[str, str, str]]:
    """Return `(guid, url, anchor_text)` even when the generic parser misses an anchor."""

    result: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    anchor_re = re.compile(
        r"<a\b[^>]*href=[\"'](?P<href>[^\"']*BiaoDuanGuid=[^\"']+)[\"'][^>]*>(?P<body>.*?)</a>",
        re.I | re.S,
    )
    for match in anchor_re.finditer(html):
        href = unescape(match.group("href"))
        guid_match = _GUID_RE.search(href)
        if not guid_match:
            continue
        guid = guid_match.group(1).lower()
        if guid in seen:
            continue
        seen.add(guid)
        result.append((guid, urljoin(base_url, href), _plain_html_fragment(match.group("body"))))
    return result


class XuzhouAgencyAssetFeed:
    def __init__(
        self,
        *,
        discovery_client: PublicHtmlClient | None = None,
        mirror_client: PublicHtmlClient | None = None,
    ) -> None:
        self.discovery_client = discovery_client or PublicHtmlClient(
            source_id="XZ_GGZY_AGENCY_LIST",
            allowed_hosts={XZ_GGZY_HOST},
            timeout_seconds=30,
            retries=2,
        )
        self.mirror_client = mirror_client or PublicHtmlClient(
            source_id="JS_GGZY_XZ_MIRROR",
            allowed_hosts={JS_GGZY_HOST},
            timeout_seconds=30,
            retries=2,
        )

    def discover_recent(self, *, limit: int = 30) -> dict[str, Any]:
        if limit <= 0 or limit > 200:
            raise ValueError("limit must be between 1 and 200")
        envelope = self.discovery_client.fetch(
            XZ_AGENCY_LIST,
            request_name="xz_ggzy.agency_assets.list",
        )
        doc = html_to_document(envelope.html, base_url=XZ_AGENCY_LIST)
        candidates: list[tuple[str, str, str]] = []
        seen: set[str] = set()

        for link in doc["links"]:
            guid_match = _GUID_RE.search(link["url"])
            if not guid_match:
                continue
            guid = guid_match.group(1).lower()
            if guid in seen:
                continue
            seen.add(guid)
            candidates.append((guid, link["url"], link["text"]))

        for guid, url, text in _extract_guid_links(envelope.html, XZ_AGENCY_LIST):
            if guid in seen:
                continue
            seen.add(guid)
            candidates.append((guid, url, text))

        items: list[dict[str, Any]] = []
        for guid, url, raw_title in candidates:
            title = _normalize_title(raw_title)
            publication_date = _date_near_guid(envelope.html, guid, title)
            round_number = _listing_round(title)
            items.append(
                {
                    "guid": guid,
                    "title": title,
                    "url": url,
                    "publication_date": publication_date,
                    "listing_mode": _listing_mode(title),
                    "listing_round": round_number,
                    "relisting_observed": bool(round_number and round_number >= 2),
                    "mirror_url": (
                        _mirror_url(publication_date, guid) if publication_date else None
                    ),
                }
            )
            if len(items) >= limit:
                break

        return {
            "source_id": "XZ_GGZY_AGENCY_LIST",
            "list_url": XZ_AGENCY_LIST,
            "item_count": len(items),
            "items": items,
            "provenance": envelope.metadata(),
        }

    def fetch_mirror_listing(self, item: dict[str, Any]) -> AgencyAssetListing:
        guid = str(item.get("guid") or "").strip().lower()
        if not _GUID_RE.fullmatch(f"BiaoDuanGuid={guid}"):
            raise ValueError("valid BiaoDuanGuid is required")
        publication_date = str(item.get("publication_date") or "").strip()
        if not publication_date:
            raise ValueError("publication_date is required for official mirror lookup")
        mirror_url = str(item.get("mirror_url") or _mirror_url(publication_date, guid))
        envelope = self.mirror_client.fetch(
            mirror_url,
            request_name="js_ggzy.xuzhou_asset_mirror.detail",
        )
        doc = html_to_document(envelope.html, base_url=mirror_url)
        text = doc["text"]
        source_origin_verified = bool(
            re.search(r"来源[：:\s]*徐州市公共资源交易", text)
            or "徐州淮海产权服务有限公司" in text
        )
        if not source_origin_verified:
            raise ValueError("official mirror detail is not verified as Xuzhou-origin evidence")

        title = self._best_title(text, doc["title"], str(item.get("title") or ""))
        round_number = _listing_round(title + " " + text[:1600])
        underuse_state, underuse_excerpt = _underuse_evidence(text)
        asking_price_rmb, asking_price_raw = _asking_price(text)
        return AgencyAssetListing(
            source_id="JS_GGZY_XZ_MIRROR",
            discovery_source_id="XZ_GGZY_AGENCY_LIST",
            guid=guid,
            title=title,
            url=mirror_url,
            discovery_url=str(item.get("url") or XZ_AGENCY_LIST),
            publication_date=_publication_date(text, mirror_url) or publication_date,
            project_id=_first(r"项目编号[：:\s]*([^\n]+)", text),
            listing_mode=_listing_mode(title + " " + text[:1600]),
            listing_round=round_number,
            relisting_observed=bool(round_number and round_number >= 2),
            listing_start=_first(
                r"挂牌起始日期[：:\s]*([0-9]{4}[-年][0-9]{1,2}[-月][0-9]{1,2}日?)",
                text,
            ),
            listing_end=_first(
                r"挂牌截止日期[：:\s]*([0-9]{4}[-年][0-9]{1,2}[-月][0-9]{1,2}日?)",
                text,
            ),
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
            source_origin_verified=True,
            discovery_provenance=dict(item.get("discovery_provenance") or {}),
            detail_provenance=envelope.metadata(),
        )

    @staticmethod
    def _best_title(text: str, html_title: str, fallback: str) -> str:
        for line in text.splitlines()[:45]:
            line = normalize_whitespace(line)
            if len(line) > 200:
                continue
            if any(token in line for token in ("转让", "招租", "拍租", "出租")):
                return _normalize_title(line)
        return _normalize_title(fallback or html_title)

    def collect_recent(self, *, limit: int = 20) -> dict[str, Any]:
        discovery = self.discover_recent(limit=limit)
        listings: list[dict[str, Any]] = []
        skipped: list[dict[str, str]] = []
        errors: list[dict[str, str]] = []
        for raw_item in discovery["items"]:
            item = dict(raw_item)
            item["discovery_provenance"] = discovery["provenance"]
            if not item.get("publication_date"):
                skipped.append(
                    {"guid": item["guid"], "reason": "publication_date unavailable"}
                )
                continue
            try:
                listings.append(asdict(self.fetch_mirror_listing(item)))
            except Exception as exc:
                errors.append(
                    {"guid": item["guid"], "url": str(item.get("mirror_url") or ""), "error": str(exc)}
                )

        return {
            "source_id": "XZ_GGZY_AGENCY_LIST+JS_GGZY_XZ_MIRROR",
            "discovery": discovery,
            "listing_count": len(listings),
            "skipped_count": len(skipped),
            "error_count": len(errors),
            "observed_underuse_count": sum(
                1 for item in listings if item["underuse_evidence_state"] == "OBSERVED"
            ),
            "relisting_count": sum(
                1 for item in listings if item["relisting_observed"]
            ),
            "listings": listings,
            "skipped": skipped,
            "errors": errors,
            "truth_note": (
                "Xuzhou list discovers the event; Jiangsu static mirror supplies detail. "
                "Only verified Xuzhou-origin mirror text is promoted."
            ),
        }
