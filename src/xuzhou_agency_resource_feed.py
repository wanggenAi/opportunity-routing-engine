"""Xuzhou agency property-rights feed discovered from the official Xuzhou list.

The official Xuzhou public-resource page is the discovery/attestation source. Current
rows may link to e交易 for detail enrichment; historical rows may resolve through the
Jiangsu public-resource mirror.

Truth boundaries:
- discovery proves a listing exists, not that the resource is controlled by us;
- linked detail may enrich facts but does not become government data;
- explicit 闲置/空置 text is required for OBSERVED underuse;
- repeated listing is allocation friction only;
- field parsing must never promote platform disclaimer/legal boilerplate as an owner;
- title transaction semantics take precedence over unrelated body boilerplate.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from html import unescape
from typing import Any, Iterable
from urllib.parse import urljoin, urlparse

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
EJY_HOST = "www.ejy365.com"
JS_GGZY_HOST = "jsggzy.jszwfw.gov.cn"
XZ_AGENCY_LIST = "https://ggzy.zwb.xz.gov.cn/jyxx/003010/003010002/listqtxx.html"
JS_ASSET_MIRROR_PREFIX = "https://jsggzy.jszwfw.gov.cn/jyxx/003006/003006001"

_GUID_RE = re.compile(r"BiaoDuanGuid=([0-9a-fA-F-]{36})", re.I)
_DATE_RE = re.compile(r"20\d{2}-\d{1,2}-\d{1,2}")
_GR_RE = re.compile(r"(GR20\d{2}JS\d+(?:-\d+)?)", re.I)
_EJY_URL_RE = re.compile(
    r"location\.href\s*=\s*['\"](?P<url>https://www\.ejy365\.com/info/ejy\d+)['\"]",
    re.I,
)
_TITLE_ATTR_RE = re.compile(r"\btitle=['\"](?P<title>[^'\"]+)['\"]", re.I | re.S)
_ROW_RE = re.compile(r"<tr\b[^>]*>(?P<body>.*?)</tr>", re.I | re.S)
_TD_RE = re.compile(r"<td\b[^>]*>(?P<body>.*?)</td>", re.I | re.S)

_BAD_FIELD_VALUE_MARKERS = (
    "和/或招标方",
    "相关资质进行审核",
    "项目公告以及相关信息",
    "本平台",
    "不承担审核义务",
    "法律责任",
)


@dataclass(frozen=True)
class AgencyAssetListing:
    source_id: str
    discovery_source_id: str
    external_project_url: str
    monitoring_code: str | None
    legacy_guid: str | None
    title: str
    url: str
    discovery_url: str
    publication_date: str | None
    project_id: str | None
    publisher_actor: str | None
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


def _mirror_url(publication_date: str, guid: str) -> str:
    digits = "".join(ch for ch in publication_date if ch.isdigit())
    if len(digits) != 8:
        raise ValueError("publication_date must be YYYY-MM-DD for mirror construction")
    return f"{JS_ASSET_MIRROR_PREFIX}/{digits}/{guid}.html"


def _date_near_token(html: str, token: str, title: str = "") -> str | None:
    idx = html.lower().find(token.lower())
    if idx >= 0:
        nearby = _plain_html_fragment(html[max(0, idx - 600) : idx + 1600])
        matches = _DATE_RE.findall(nearby)
        if matches:
            return matches[-1]
    if title:
        plain = _plain_html_fragment(html)
        idx = plain.find(title)
        if idx >= 0:
            matches = _DATE_RE.findall(plain[idx : idx + 600])
            if matches:
                return matches[0]
    return None


def _clean_labeled_value(value: str | None) -> str | None:
    candidate = normalize_whitespace(value or "").strip(" ：:")
    if not candidate or len(candidate) > 180:
        return None
    if any(marker in candidate for marker in _BAD_FIELD_VALUE_MARKERS):
        return None
    return candidate


def _labeled_value(text: str, labels: Iterable[str]) -> str | None:
    """Extract a real label/value field without matching prose mentioning the label.

    Colon-delimited labels may occur anywhere. Whitespace-only labels must begin a
    logical line; this prevents prose such as ``挂牌方、招标方自行负责`` from being
    interpreted as a field named ``挂牌方``.
    """

    for label in labels:
        escaped = re.escape(label)
        match = re.search(rf"{escaped}\s*[：:]\s*([^\n]{{1,220}})", text)
        if match:
            cleaned = _clean_labeled_value(match.group(1))
            if cleaned:
                return cleaned
        match = re.search(rf"(?:^|\n)\s*{escaped}\s+([^\n]{{1,220}})", text)
        if match:
            cleaned = _clean_labeled_value(match.group(1))
            if cleaned:
                return cleaned
    return None


def _preferred_listing_mode(title: str, text: str, fallback: str | None = None) -> str:
    """Prefer transaction semantics from the project title over body boilerplate."""

    title_mode = _listing_mode(title)
    if title_mode != "UNKNOWN":
        return title_mode
    fallback_mode = str(fallback or "").strip().upper()
    if fallback_mode in {"LEASE", "TRANSFER"}:
        return fallback_mode
    return _listing_mode(text[:2400])


def _extract_ejy_rows(html: str) -> list[dict[str, Any]]:
    """Parse current official rows whose real href is stored in ``onclick``."""

    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row_match in _ROW_RE.finditer(html):
        row_html = row_match.group("body")
        url_match = _EJY_URL_RE.search(row_html)
        if not url_match:
            continue
        external_url = unescape(url_match.group("url"))
        if external_url in seen:
            continue
        seen.add(external_url)

        title_match = _TITLE_ATTR_RE.search(row_html)
        title = _normalize_title(
            unescape(title_match.group("title")) if title_match else _plain_html_fragment(row_html)
        )
        cells = [_plain_html_fragment(match.group("body")) for match in _TD_RE.finditer(row_html)]
        publication_date = next((cell for cell in reversed(cells) if _DATE_RE.fullmatch(cell)), None)
        publisher_actor = next(
            (cell for cell in cells if "产权" in cell and cell not in {"e交易", title}),
            None,
        )
        gr_match = _GR_RE.search(title)
        monitoring_code = gr_match.group(1).upper() if gr_match else None
        round_number = _listing_round(title)
        items.append(
            {
                "external_project_url": external_url,
                "monitoring_code": monitoring_code,
                "legacy_guid": None,
                "title": title,
                "url": external_url,
                "publication_date": publication_date,
                "publisher_actor": publisher_actor,
                "listing_mode": _listing_mode(title),
                "listing_round": round_number,
                "relisting_observed": bool(round_number and round_number >= 2),
                "detail_source": "EJY365",
            }
        )
    return items


def _extract_legacy_guid_rows(html: str, base_url: str) -> list[dict[str, Any]]:
    """Fallback for historical rows that still expose BiaoDuanGuid links."""

    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    anchor_re = re.compile(
        r"<a\b[^>]*href=['\"](?P<href>[^'\"]*BiaoDuanGuid=[^'\"]+)['\"][^>]*>(?P<body>.*?)</a>",
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
        title = _normalize_title(_plain_html_fragment(match.group("body")))
        publication_date = _date_near_token(html, guid, title)
        round_number = _listing_round(title)
        result.append(
            {
                "external_project_url": urljoin(base_url, href),
                "monitoring_code": (_GR_RE.search(title).group(1).upper() if _GR_RE.search(title) else None),
                "legacy_guid": guid,
                "title": title,
                "url": urljoin(base_url, href),
                "publication_date": publication_date,
                "publisher_actor": None,
                "listing_mode": _listing_mode(title),
                "listing_round": round_number,
                "relisting_observed": bool(round_number and round_number >= 2),
                "detail_source": "JS_GGZY_MIRROR",
                "mirror_url": _mirror_url(publication_date, guid) if publication_date else None,
            }
        )
    return result


class XuzhouAgencyAssetFeed:
    def __init__(
        self,
        *,
        discovery_client: PublicHtmlClient | None = None,
        ejy_client: PublicHtmlClient | None = None,
        mirror_client: PublicHtmlClient | None = None,
    ) -> None:
        self.discovery_client = discovery_client or PublicHtmlClient(
            source_id="XZ_GGZY_AGENCY_LIST",
            allowed_hosts={XZ_GGZY_HOST},
            timeout_seconds=30,
            retries=2,
        )
        self.ejy_client = ejy_client or PublicHtmlClient(
            source_id="EJY365_XZ_LINKED",
            allowed_hosts={EJY_HOST},
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
        items = _extract_ejy_rows(envelope.html)
        if len(items) < limit:
            current_urls = {item["external_project_url"] for item in items}
            for legacy in _extract_legacy_guid_rows(envelope.html, XZ_AGENCY_LIST):
                if legacy["external_project_url"] in current_urls:
                    continue
                items.append(legacy)
                if len(items) >= limit:
                    break
        items = items[:limit]
        return {
            "source_id": "XZ_GGZY_AGENCY_LIST",
            "list_url": XZ_AGENCY_LIST,
            "item_count": len(items),
            "items": items,
            "provenance": envelope.metadata(),
            "truth_note": (
                "Discovery is attested by the official Xuzhou list. Current rows link to "
                "e交易 through onclick redirects; external detail remains a separate source."
            ),
        }

    def _validate_officially_discovered_external_url(self, item: dict[str, Any]) -> str:
        external_url = str(item.get("external_project_url") or "").strip()
        parsed = urlparse(external_url)
        if (
            parsed.scheme != "https"
            or parsed.hostname != EJY_HOST
            or not re.fullmatch(r"/info/ejy\d+", parsed.path)
        ):
            raise ValueError("external project URL is not a supported e交易 detail URL")
        return external_url

    def fetch_ejy_listing(self, item: dict[str, Any]) -> AgencyAssetListing:
        external_url = self._validate_officially_discovered_external_url(item)
        envelope = self.ejy_client.fetch(
            external_url,
            request_name="ejy365.xuzhou_linked_asset.detail",
        )
        doc = html_to_document(envelope.html, base_url=external_url)
        text = doc["text"]
        title = self._best_title(text, doc["title"], str(item.get("title") or ""))
        monitoring_code = str(item.get("monitoring_code") or "").strip() or None
        if monitoring_code and monitoring_code not in text and monitoring_code not in title:
            raise ValueError("e交易 detail does not match the official monitoring code")

        round_number = _listing_round(title + " " + text[:2400]) or item.get("listing_round")
        # The title is source text too; explicit 闲置 in a verified project title is valid
        # underuse evidence and must not be lost merely because body extraction is sparse.
        underuse_state, underuse_excerpt = _underuse_evidence(title + "\n" + text)
        asking_price_rmb, asking_price_raw = _asking_price(text)
        project_id = (
            _labeled_value(text, ("项目编号", "项目编码"))
            or monitoring_code
        )
        return AgencyAssetListing(
            source_id="EJY365_XZ_LINKED",
            discovery_source_id="XZ_GGZY_AGENCY_LIST",
            external_project_url=external_url,
            monitoring_code=monitoring_code,
            legacy_guid=None,
            title=title,
            url=external_url,
            discovery_url=XZ_AGENCY_LIST,
            publication_date=(
                _publication_date(text, external_url)
                or str(item.get("publication_date") or "").strip()
                or None
            ),
            project_id=project_id,
            publisher_actor=str(item.get("publisher_actor") or "").strip() or None,
            listing_mode=_preferred_listing_mode(
                title,
                text,
                str(item.get("listing_mode") or ""),
            ),
            listing_round=round_number,
            relisting_observed=bool(round_number and int(round_number) >= 2),
            listing_start=_labeled_value(text, ("报名开始时间", "挂牌起始日期")),
            listing_end=_labeled_value(text, ("报名截止时间", "挂牌截止日期")),
            resource_state="DISCOVERED",
            underuse_evidence_state=underuse_state,
            underuse_excerpt=underuse_excerpt,
            asking_price_rmb=asking_price_rmb,
            asking_price_raw=asking_price_raw,
            location=_labeled_value(text, ("标的所在地", "标的坐落", "存放地")),
            owner_actor=_labeled_value(text, ("挂牌方", "转让方名称", "出租方名称")),
            source_origin_verified=True,
            discovery_provenance=dict(item.get("discovery_provenance") or {}),
            detail_provenance=envelope.metadata(),
        )

    def fetch_legacy_mirror_listing(self, item: dict[str, Any]) -> AgencyAssetListing:
        guid = str(item.get("legacy_guid") or "").strip().lower()
        if not re.fullmatch(r"[0-9a-f-]{36}", guid):
            raise ValueError("valid legacy BiaoDuanGuid is required")
        publication_date = str(item.get("publication_date") or "").strip()
        if not publication_date:
            raise ValueError("publication_date is required for legacy mirror lookup")
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
        round_number = _listing_round(title + " " + text[:2400])
        underuse_state, underuse_excerpt = _underuse_evidence(title + "\n" + text)
        asking_price_rmb, asking_price_raw = _asking_price(text)
        monitoring_code = str(item.get("monitoring_code") or "").strip() or None
        return AgencyAssetListing(
            source_id="JS_GGZY_XZ_MIRROR",
            discovery_source_id="XZ_GGZY_AGENCY_LIST",
            external_project_url=str(item.get("external_project_url") or ""),
            monitoring_code=monitoring_code,
            legacy_guid=guid,
            title=title,
            url=mirror_url,
            discovery_url=XZ_AGENCY_LIST,
            publication_date=_publication_date(text, mirror_url) or publication_date,
            project_id=_labeled_value(text, ("项目编号", "项目编码")) or monitoring_code,
            publisher_actor=str(item.get("publisher_actor") or "").strip() or None,
            listing_mode=_preferred_listing_mode(
                title,
                text,
                str(item.get("listing_mode") or ""),
            ),
            listing_round=round_number,
            relisting_observed=bool(round_number and round_number >= 2),
            listing_start=_labeled_value(text, ("挂牌起始日期",)),
            listing_end=_labeled_value(text, ("挂牌截止日期",)),
            resource_state="DISCOVERED",
            underuse_evidence_state=underuse_state,
            underuse_excerpt=underuse_excerpt,
            asking_price_rmb=asking_price_rmb,
            asking_price_raw=asking_price_raw,
            location=_labeled_value(text, ("存放地", "标的坐落", "标的所在地")),
            owner_actor=_labeled_value(text, ("转让方名称", "出租方名称", "挂牌方")),
            source_origin_verified=True,
            discovery_provenance=dict(item.get("discovery_provenance") or {}),
            detail_provenance=envelope.metadata(),
        )

    @staticmethod
    def _best_title(text: str, html_title: str, fallback: str) -> str:
        fallback = _normalize_title(fallback or "")
        if fallback and fallback in text:
            return fallback
        for line in text.splitlines()[:60]:
            line = normalize_whitespace(line)
            if len(line) > 220:
                continue
            if any(token in line for token in ("转让", "招租", "拍租", "出租")):
                return _normalize_title(line)
        return fallback or _normalize_title(html_title)

    def collect_recent(self, *, limit: int = 20) -> dict[str, Any]:
        discovery = self.discover_recent(limit=limit)
        listings: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []
        for raw_item in discovery["items"]:
            item = dict(raw_item)
            item["discovery_provenance"] = discovery["provenance"]
            try:
                if item.get("detail_source") == "EJY365":
                    listing = self.fetch_ejy_listing(item)
                else:
                    listing = self.fetch_legacy_mirror_listing(item)
                listings.append(asdict(listing))
            except Exception as exc:
                errors.append(
                    {
                        "monitoring_code": str(item.get("monitoring_code") or ""),
                        "url": str(item.get("external_project_url") or item.get("mirror_url") or ""),
                        "error": str(exc),
                    }
                )

        return {
            "source_id": "XZ_GGZY_AGENCY_LIST+LINKED_DETAIL",
            "discovery": discovery,
            "listing_count": len(listings),
            "error_count": len(errors),
            "observed_underuse_count": sum(
                1 for item in listings if item["underuse_evidence_state"] == "OBSERVED"
            ),
            "relisting_count": sum(1 for item in listings if item["relisting_observed"]),
            "listings": listings,
            "errors": errors,
            "truth_note": (
                "The official Xuzhou page attests discovery and outbound project identity; "
                "the linked e交易 page only enriches detail. DISCOVERED != OPTIONED, and "
                "relisting != underuse."
            ),
        }
