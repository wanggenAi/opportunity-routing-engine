"""First-party Xuzhou HRSS recruitment evidence for capability demand.

This source is deliberately one-sided: an official recruitment table proves that
an institution is asking for people with explicit qualifications.  It does NOT
prove a labor shortage, an idle/surplus workforce, willingness to take delegated
work, callable availability, or an opportunity.

Truth boundaries:
- recruitment demand != labor shortage;
- graduate/jobless population != callable labor supply;
- missing requirement != no requirement;
- an advertised headcount is planned hiring demand, not completed hiring;
- no candidate/person profile is collected;
- only public, no-login, first-party Xuzhou HRSS pages/attachments are used.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timezone
from typing import Any
from urllib.parse import urlparse

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace
from src.xls_ingest import PublicXlsClient, parse_workbook_rows


SOURCE_ID = "XZ_HRSS_RECRUITMENT"
HOST = "hrss.xz.gov.cn"
LIST_URL = "https://hrss.xz.gov.cn/001/001004/list.html"
_DETAIL_RE = re.compile(r"^/001/001004/(20\d{6})/[0-9a-fA-F-]+\.html$")


_HEADER_ALIASES: dict[str, tuple[str, ...]] = {
    "employer": ("招聘单位", "单位名称", "用人单位"),
    "position": ("岗位名称", "职位名称"),
    "position_code": ("岗位代码", "职位代码"),
    "hiring_count": ("招聘人数", "招聘数量", "人数"),
    "education": ("学历", "学历要求"),
    "degree": ("学位", "学位要求"),
    "major_requirement": ("专业", "专业要求"),
    "professional_title": ("职称", "职称要求", "专业技术资格"),
    "experience_requirement": ("工作经历", "工作经验", "经历要求"),
    "qualification_requirement": ("资格条件", "资格要求", "其他条件"),
}


def _official_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname == HOST


def discover_recent_recruitment_articles(
    index_document: dict[str, Any], *, limit: int = 20
) -> list[dict[str, str]]:
    if limit <= 0 or limit > 100:
        raise ValueError("limit must be between 1 and 100")
    seen: set[str] = set()
    candidates: list[tuple[str, str, str]] = []
    for link in index_document.get("links", []):
        title = normalize_whitespace(str(link.get("text", "")))
        url = str(link.get("url", "")).strip()
        parsed = urlparse(url)
        match = _DETAIL_RE.match(parsed.path)
        if not match or not _official_url(url) or url in seen:
            continue
        if "招聘" not in title:
            continue
        seen.add(url)
        raw = match.group(1)
        publication_date = f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"
        candidates.append((publication_date, title, url))
    candidates.sort(reverse=True)
    return [
        {"publication_date_from_url": d, "title": t, "url": u}
        for d, t, u in candidates[:limit]
    ]


def discover_job_table_attachment(detail_document: dict[str, Any]) -> str | None:
    candidates: list[str] = []
    for link in detail_document.get("links", []):
        text = normalize_whitespace(str(link.get("text", "")))
        url = str(link.get("url", "")).strip()
        if not _official_url(url) or not url.lower().endswith(".xls"):
            continue
        if "岗位" in text and "表" in text:
            candidates.append(url)
    unique = list(dict.fromkeys(candidates))
    if len(unique) > 1:
        raise ValueError(f"multiple official HRSS job-table XLS attachments: {unique}")
    return unique[0] if unique else None


def _cell_text(value: Any) -> str:
    return re.sub(r"\s+", "", str(value or "")).replace("：", ":")


def _match_header(text: str, aliases: tuple[str, ...]) -> bool:
    return any(text == alias or text.endswith(alias) for alias in aliases)


def _find_header(rows: list[list[Any]]) -> tuple[int, dict[str, int]]:
    candidates: list[tuple[int, dict[str, int]]] = []
    for row_index, row in enumerate(rows[:30]):
        mapping: dict[str, int] = {}
        for col_index, cell in enumerate(row):
            text = _cell_text(cell)
            if not text:
                continue
            for field, aliases in _HEADER_ALIASES.items():
                if field in mapping:
                    continue
                if _match_header(text, aliases):
                    mapping[field] = col_index
        if {"position", "hiring_count", "major_requirement"} <= mapping.keys():
            candidates.append((row_index, mapping))
    if len(candidates) != 1:
        raise ValueError(f"expected one semantic recruitment header row, found {len(candidates)}")
    return candidates[0]


def _parse_count(value: Any) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValueError("hiring count resolved to boolean")
    try:
        number = float(str(value).replace(",", "").strip())
    except ValueError:
        return None
    if not number.is_integer():
        raise ValueError(f"hiring count is not an integer: {value!r}")
    count = int(number)
    if not 0 < count <= 10000:
        raise ValueError(f"hiring count outside sanity bounds: {count}")
    return count


def _value(row: list[Any], col: int | None) -> str | None:
    if col is None or col >= len(row):
        return None
    raw = row[col]
    if raw is None or raw == "":
        return None
    text = normalize_whitespace(str(raw))
    return text or None


def extract_capability_demand(workbook: list[dict[str, Any]]) -> dict[str, Any]:
    sheet_candidates: list[tuple[dict[str, Any], int, dict[str, int]]] = []
    for sheet in workbook:
        rows = sheet.get("rows", [])
        if not rows:
            continue
        try:
            header_row, mapping = _find_header(rows)
        except ValueError:
            continue
        sheet_candidates.append((sheet, header_row, mapping))
    if len(sheet_candidates) != 1:
        names = [str(item[0].get("sheet_name")) for item in sheet_candidates]
        raise ValueError(f"expected one structured recruitment sheet, found {len(sheet_candidates)}: {names}")

    sheet, header_row, mapping = sheet_candidates[0]
    rows = sheet["rows"]
    demand_units: list[dict[str, Any]] = []
    total_requested = 0
    for row_index, row in enumerate(rows[header_row + 1 :], start=header_row + 1):
        position = _value(row, mapping.get("position"))
        major = _value(row, mapping.get("major_requirement"))
        count = _parse_count(row[mapping["hiring_count"]] if mapping["hiring_count"] < len(row) else None)
        if not position and not major and count is None:
            continue
        if not position or count is None:
            continue
        total_requested += count
        unit = {
            "row_number_1based": row_index + 1,
            "employer": _value(row, mapping.get("employer")),
            "position": position,
            "position_code": _value(row, mapping.get("position_code")),
            "hiring_count": count,
            "education": _value(row, mapping.get("education")),
            "degree": _value(row, mapping.get("degree")),
            "major_requirement": major,
            "professional_title": _value(row, mapping.get("professional_title")),
            "experience_requirement": _value(row, mapping.get("experience_requirement")),
            "qualification_requirement": _value(row, mapping.get("qualification_requirement")),
            "evidence_state": "EXPLICIT_CAPABILITY_DEMAND",
        }
        demand_units.append(unit)

    if not demand_units:
        raise ValueError("structured HRSS job table produced no explicit demand units")
    return {
        "sheet_index": sheet.get("sheet_index"),
        "sheet_name": sheet.get("sheet_name"),
        "header_row_number_1based": header_row + 1,
        "header_mapping": mapping,
        "demand_unit_count": len(demand_units),
        "total_requested_headcount": total_requested,
        "demand_units": demand_units,
    }


def _freshness(publication_date: str) -> dict[str, Any]:
    published = date.fromisoformat(publication_date)
    age_days = (datetime.now(timezone.utc).date() - published).days
    if age_days < 0:
        status = "FUTURE_DATE_ERROR"
    elif age_days <= 180:
        status = "FRESH"
    elif age_days <= 365:
        status = "AGING"
    else:
        status = "STALE"
    return {"publication_date": publication_date, "age_days": age_days, "status": status}


class XuzhouHrssCapabilityDemandAdapter:
    def __init__(
        self,
        *,
        html_client: PublicHtmlClient | None = None,
        xls_client: PublicXlsClient | None = None,
    ) -> None:
        self.html_client = html_client or PublicHtmlClient(
            source_id=SOURCE_ID,
            allowed_hosts={HOST},
            timeout_seconds=25,
            retries=2,
            max_response_bytes=5_000_000,
        )
        self.xls_client = xls_client or PublicXlsClient(
            source_id=SOURCE_ID,
            allowed_hosts={HOST},
            timeout_seconds=25,
            retries=2,
            max_response_bytes=20_000_000,
        )

    def collect_latest_structured(self, *, scan_limit: int = 15) -> dict[str, Any]:
        index_env = self.html_client.fetch(LIST_URL, request_name="xz_hrss.recruitment.list")
        index_doc = html_to_document(index_env.html, base_url=index_env.url)
        articles = discover_recent_recruitment_articles(index_doc, limit=scan_limit)
        if not articles:
            raise ValueError("no official Xuzhou HRSS recruitment articles discovered")

        inspected: list[dict[str, Any]] = []
        for article in articles:
            detail_env = self.html_client.fetch(article["url"], request_name="xz_hrss.recruitment.detail")
            detail_doc = html_to_document(detail_env.html, base_url=detail_env.url)
            attachment_url = discover_job_table_attachment(detail_doc)
            inspected.append({"title": article["title"], "url": article["url"], "has_job_table": bool(attachment_url)})
            if not attachment_url:
                continue
            xls_env = self.xls_client.fetch(attachment_url, request_name="xz_hrss.recruitment.jobs_xls")
            workbook = parse_workbook_rows(xls_env.payload)
            observation = extract_capability_demand(workbook)
            return {
                "source_id": SOURCE_ID,
                "collected_at_utc": datetime.now(timezone.utc).isoformat(),
                "data_available": True,
                "geography": "Xuzhou",
                "evidence_kind": "PUBLIC_SECTOR_CAPABILITY_DEMAND",
                "article_title": article["title"],
                "article_url": article["url"],
                "publication_date": article["publication_date_from_url"],
                "freshness": _freshness(article["publication_date_from_url"]),
                "observation": observation,
                "inspected_articles": inspected,
                "provenance": {
                    "index": index_env.metadata(),
                    "detail": detail_env.metadata(),
                    "xls": xls_env.metadata(),
                },
                "truth_boundaries": [
                    "RECRUITMENT_DEMAND_IS_NOT_LABOR_SHORTAGE",
                    "DEMAND_IS_NOT_SURPLUS_RESOURCE",
                    "ADVERTISED_HEADCOUNT_IS_NOT_COMPLETED_HIRING",
                    "NO_CANDIDATE_PERSON_PROFILE",
                    "NO_HUMAN_CAPABILITY_UNDERUSE_INFERENCE",
                    "NO_OPPORTUNITY_INFERENCE",
                ],
            }
        raise ValueError("recent official HRSS recruitment articles contained no structured XLS job table")
