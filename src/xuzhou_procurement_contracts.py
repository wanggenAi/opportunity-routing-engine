"""First-party Xuzhou procurement contract-announcement evidence.

The Xuzhou public-resources site exposes contract announcements through its public
HTTPS full-text search service.  This adapter queries that service with an exact
``project_id`` navigation term and then *re-parses the project identity from the
returned contract body*.  A search hit is never accepted merely because the search
engine returned it.

Truth boundaries:
- contract announcement != payment / settlement;
- purchaser / Party A != payer unless a first-party source explicitly says so;
- supplier / Party B proves the named contracting supplier, not current capacity;
- title similarity, capability similarity and search-engine relevance never join a
  contract to a tender;
- only an exact project-id field match becomes contract evidence;
- zero exact matches is a valid empirical result.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from html import unescape
from typing import Any, Iterable, Mapping
from urllib.parse import urljoin

from src.network_ingest import FetchEnvelope, JsonHttpClient


XZ_GGZY_HOST = "ggzy.zwb.xz.gov.cn"
XZ_CONTRACT_CATEGORY = "003004007"
XZ_CONTRACT_LIST_URL = (
    "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004007/list.html"
)
XZ_CONTRACT_SEARCH_URL = (
    "https://ggzy.zwb.xz.gov.cn/inteligentsearchnew/rest/"
    "esinteligentsearch/getFullTextDataNew"
)

_PROJECT_ID_MODERN_RE = re.compile(
    r"三、项目编号(?:\([^)]*\))?\s*[:：]\s*(?P<value>.*?)\s*(?=四、项目名称\s*[:：])",
    re.S,
)
_PROJECT_ID_LEGACY_RE = re.compile(
    r"五、采购项目编号\s*[:：]\s*(?P<value>.*?)\s*(?=六、项目名称\s*[:：])",
    re.S,
)
_CONTRACT_ID_RE = re.compile(
    r"一、合同编号\s*[:：]\s*(?P<value>.*?)\s*(?=二、合同名称\s*[:：])",
    re.S,
)
_CONTRACT_NAME_RE = re.compile(
    r"二、合同名称\s*[:：]\s*(?P<value>.*?)\s*(?=三、项目编号)",
    re.S,
)
_PROJECT_NAME_RE = re.compile(
    r"四、项目名称\s*[:：]\s*(?P<value>.*?)\s*(?=五、合同主体)",
    re.S,
)
_LEGACY_PROJECT_NAME_RE = re.compile(
    r"六、项目名称\s*[:：]\s*(?P<value>.*?)\s*(?=七、中标供应商)",
    re.S,
)
_BUYER_RE = re.compile(
    r"采购人（甲方）\s*[:：]\s*(?P<value>.*?)\s*(?=地址\s*[:：])",
    re.S,
)
_SUPPLIER_RE = re.compile(
    r"供应商（乙方）\s*[:：]\s*(?P<value>.*?)\s*(?=地址\s*[:：])",
    re.S,
)
_LEGACY_BUYER_RE = re.compile(
    r"一、采购单位\s*[:：]\s*(?P<value>.*?)\s*(?=二、采购预算)",
    re.S,
)
_LEGACY_SUPPLIER_RE = re.compile(
    r"七、中标供应商\s*[:：]\s*(?P<value>.*?)\s*(?=八、合同金额)",
    re.S,
)
_SIGNED_DATE_RE = re.compile(
    r"(?:七|九)、合同签订日期\s*[:：]\s*(?P<value>\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}日?)"
)
_MONEY_AFTER_CONTRACT_RE = re.compile(
    r"合同金额(?:（(?P<label_unit>元|万元)）)?\s*[:：]\s*"
    r"(?P<number>[0-9][0-9,]*(?:\.\d+)?)\s*(?P<unit>亿元|万元|元)?"
)
_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class ProcurementContract:
    source_id: str
    project_id: str
    project_name: str | None
    contract_id: str | None
    contract_name: str | None
    url: str
    publication_date: str | None
    signed_date: str | None
    buyer_actor: str | None
    payer_actor: str | None
    supplier_actor: str | None
    contract_amount_rmb: str | None
    settled_amount_rmb: str | None
    contract_signed: bool
    settlement_proven: bool
    provenance: dict[str, Any]


def _plain(value: object) -> str:
    text = unescape(str(value or ""))
    text = _TAG_RE.sub(" ", text)
    return _WHITESPACE_RE.sub(" ", text).strip()


def _match_value(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    if not match:
        return None
    value = _plain(match.group("value"))
    return value or None


def _normalize_project_id(value: str | None) -> str | None:
    if not value:
        return None
    value = _plain(value).strip(" []【】")
    return value or None


def _normalize_date(value: str | None) -> str | None:
    if not value:
        return None
    parts = re.findall(r"\d+", value)
    if len(parts) < 3:
        return None
    return f"{int(parts[0]):04d}-{int(parts[1]):02d}-{int(parts[2]):02d}"


def _money_to_rmb(number: str, unit: str | None) -> str | None:
    try:
        value = Decimal(number.replace(",", ""))
    except InvalidOperation:
        return None
    multiplier = Decimal("1")
    if unit == "万元":
        multiplier = Decimal("10000")
    elif unit == "亿元":
        multiplier = Decimal("100000000")
    return format((value * multiplier).quantize(Decimal("0.01")), "f")


def parse_contract_content(content: object) -> dict[str, Any]:
    """Parse explicit fields from one official contract-announcement body.

    The parser supports both the modern JSZC template and the older Xuzhou contract
    publication template.  It deliberately does not infer payer or settlement.
    """

    text = _plain(content)
    project_id = _normalize_project_id(
        _match_value(_PROJECT_ID_MODERN_RE, text)
        or _match_value(_PROJECT_ID_LEGACY_RE, text)
    )
    project_name = (
        _match_value(_PROJECT_NAME_RE, text)
        or _match_value(_LEGACY_PROJECT_NAME_RE, text)
    )
    buyer = _match_value(_BUYER_RE, text) or _match_value(_LEGACY_BUYER_RE, text)
    supplier = (
        _match_value(_SUPPLIER_RE, text)
        or _match_value(_LEGACY_SUPPLIER_RE, text)
    )
    signed_match = _SIGNED_DATE_RE.search(text)
    signed_date = _normalize_date(
        signed_match.group("value") if signed_match else None
    )

    amount_match = _MONEY_AFTER_CONTRACT_RE.search(text)
    amount_rmb = None
    if amount_match:
        unit = amount_match.group("unit") or amount_match.group("label_unit") or "元"
        amount_rmb = _money_to_rmb(amount_match.group("number"), unit)

    return {
        "project_id": project_id,
        "project_name": project_name,
        "contract_id": _match_value(_CONTRACT_ID_RE, text),
        "contract_name": _match_value(_CONTRACT_NAME_RE, text),
        "buyer_actor": buyer,
        "payer_actor": None,
        "supplier_actor": supplier,
        "contract_amount_rmb": amount_rmb,
        "settled_amount_rmb": None,
        "signed_date": signed_date,
        "contract_signed": signed_date is not None,
        "settlement_proven": False,
    }


def _publication_date(record: Mapping[str, Any]) -> str | None:
    raw = _plain(record.get("infodate") or record.get("webdate"))
    match = re.match(r"(\d{4}-\d{2}-\d{2})", raw)
    return match.group(1) if match else None


def _record_url(record: Mapping[str, Any]) -> str | None:
    raw = _plain(record.get("linkurl"))
    if not raw:
        return None
    url = urljoin(XZ_CONTRACT_LIST_URL, raw)
    if not url.startswith(f"https://{XZ_GGZY_HOST}/"):
        return None
    return url


def _search_payload(project_id: str, *, offset: int, page_size: int) -> dict[str, Any]:
    return {
        "token": "",
        "pn": offset,
        "rn": str(page_size),
        "sdt": "",
        "edt": "",
        "wd": project_id,
        "inc_wd": "",
        "exc_wd": "",
        "fields": "title;content",
        "cnum": "002",
        "sort": '{"webdate":"0"}',
        "ssort": "title",
        "cl": 1200,
        "terminal": "",
        "condition": [
            {
                "fieldName": "categorynum",
                "isLike": True,
                "likeType": 2,
                "equal": XZ_CONTRACT_CATEGORY,
            }
        ],
        "time": None,
        "highlights": "title;content",
        "statistics": None,
        "unionCondition": None,
        "accuracy": "",
        "noParticiple": "1",
        "searchRange": None,
        "isBusiness": "1",
    }


class XuzhouProcurementContractAdapter:
    """Collect contract announcements by exact Xuzhou procurement project ID."""

    def __init__(self, client: JsonHttpClient | None = None) -> None:
        self.client = client or JsonHttpClient(
            source_id="XZ_GGZY_PROCUREMENT_CONTRACT",
            allowed_hosts={XZ_GGZY_HOST},
            timeout_seconds=30,
            retries=2,
            max_response_bytes=8_000_000,
        )

    def query_project(
        self,
        project_id: str,
        *,
        page_size: int = 20,
        max_records: int = 100,
    ) -> dict[str, Any]:
        project_id = _plain(project_id)
        if not project_id or len(project_id) > 160:
            raise ValueError("project_id must be a non-empty bounded string")
        if not isinstance(page_size, int) or page_size < 1 or page_size > 100:
            raise ValueError("page_size must be between 1 and 100")
        if not isinstance(max_records, int) or max_records < 1 or max_records > 500:
            raise ValueError("max_records must be between 1 and 500")

        offset = 0
        search_total: int | None = None
        accepted: list[dict[str, Any]] = []
        rejected: list[dict[str, Any]] = []
        query_provenance: list[dict[str, Any]] = []
        seen_urls: set[str] = set()

        while offset < max_records:
            envelope = self.client.request_json(
                "POST",
                XZ_CONTRACT_SEARCH_URL,
                request_name="xz_ggzy.procurement_contracts.search_exact_project",
                json_body=_search_payload(
                    project_id,
                    offset=offset,
                    page_size=min(page_size, max_records - offset),
                ),
                headers={"Referer": XZ_CONTRACT_LIST_URL},
            )
            query_provenance.append(envelope.metadata())
            payload = envelope.payload
            result = payload.get("result") if isinstance(payload, Mapping) else None
            if not isinstance(result, Mapping):
                raise ValueError("contract search response missing result object")
            records = result.get("records")
            if not isinstance(records, list):
                raise ValueError("contract search response missing records list")
            try:
                search_total = int(result.get("totalcount") or 0)
            except (TypeError, ValueError) as exc:
                raise ValueError("contract search response has invalid totalcount") from exc

            for record in records:
                if not isinstance(record, Mapping):
                    continue
                content = _plain(record.get("content"))
                parsed = parse_contract_content(content)
                parsed_id = parsed.get("project_id")
                url = _record_url(record)
                rejection = None
                if parsed_id is None:
                    rejection = "PROJECT_ID_UNRESOLVED"
                elif parsed_id != project_id:
                    rejection = "NO_EXACT_PROJECT_ID_MATCH"
                elif not url:
                    rejection = "FIRST_PARTY_CONTRACT_URL_UNRESOLVED"

                if rejection:
                    rejected.append(
                        {
                            "requested_project_id": project_id,
                            "parsed_project_id": parsed_id,
                            "reason": rejection,
                            "title": _plain(record.get("title")) or None,
                            "url": url,
                        }
                    )
                    continue
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                provenance = dict(envelope.metadata())
                provenance["record_content_sha256"] = hashlib.sha256(
                    content.encode("utf-8")
                ).hexdigest()
                contract = ProcurementContract(
                    source_id="XZ_GGZY_PROCUREMENT_CONTRACT",
                    project_id=project_id,
                    project_name=parsed.get("project_name"),
                    contract_id=parsed.get("contract_id"),
                    contract_name=parsed.get("contract_name"),
                    url=url,
                    publication_date=_publication_date(record),
                    signed_date=parsed.get("signed_date"),
                    buyer_actor=parsed.get("buyer_actor"),
                    payer_actor=None,
                    supplier_actor=parsed.get("supplier_actor"),
                    contract_amount_rmb=parsed.get("contract_amount_rmb"),
                    settled_amount_rmb=None,
                    contract_signed=parsed.get("contract_signed") is True,
                    settlement_proven=False,
                    provenance=provenance,
                )
                accepted.append(asdict(contract))

            offset += len(records)
            if not records or offset >= search_total:
                break
            if offset >= max_records:
                break

        total = search_total or 0
        return {
            "project_id": project_id,
            "search_total": total,
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
            "truncated": total > max_records,
            "contracts": accepted,
            "rejected_hits": rejected,
            "query_provenance": query_provenance,
        }

    def collect_projects(
        self,
        project_ids: Iterable[str],
        *,
        page_size: int = 20,
        max_records_per_project: int = 100,
    ) -> dict[str, Any]:
        ordered_ids: list[str] = []
        for value in project_ids:
            project_id = _plain(value)
            if project_id and project_id not in ordered_ids:
                ordered_ids.append(project_id)
        if not ordered_ids:
            raise ValueError("at least one project_id is required")
        if len(ordered_ids) > 100:
            raise ValueError("at most 100 project_ids may be collected per run")

        per_project = [
            self.query_project(
                project_id,
                page_size=page_size,
                max_records=max_records_per_project,
            )
            for project_id in ordered_ids
        ]
        contracts = [
            contract
            for item in per_project
            for contract in item.get("contracts", [])
        ]
        return {
            "source_id": "XZ_GGZY_PROCUREMENT_CONTRACT",
            "source_url": XZ_CONTRACT_LIST_URL,
            "search_url": XZ_CONTRACT_SEARCH_URL,
            "query_strategy": "EXACT_PROJECT_ID_SEARCH_THEN_EXACT_FIELD_REVALIDATION",
            "requested_project_ids": ordered_ids,
            "project_count": len(ordered_ids),
            "contract_count": len(contracts),
            "contracts": contracts,
            "projects": per_project,
            "truth_note": (
                "Contract announcements prove an exact-project contracting event only. "
                "Purchaser/Party A is retained as buyer, never copied into payer. "
                "No payment, settlement, current supplier availability, underuse, or "
                "orchestrator control is inferred."
            ),
        }
