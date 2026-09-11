"""PBC regional social-financing XLSX adapter.

The PBC statistics interpretation index publishes regional AFRE flow tables as
official XLSX attachments. This adapter discovers the newest table from the same
fixed official index used by the national money-flow adapter, follows only the
official detail page, then parses the attachment without third-party spreadsheet
libraries.

A regional value is accepted only under an official-table semantic gate. Workbook
header text is preferred; if merged-cell layout hides that text from ordinary cell
iteration, the exact official detail-page title may provide the semantic lock.
Ambiguous source identity still fails closed.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from src.html_ingest import PublicHtmlClient, html_to_document
from src.pbc_money_flow import ALLOWED_HOSTS, INDEX_URL, SOURCE_ID
from src.xlsx_ingest import PublicXlsxClient, parse_first_sheet_rows


_REGIONAL_TITLE_RE = re.compile(r"^\d{4}年.+地区社会融资规模增量统计表$")
_RELEASE_DATE_RE = re.compile(r"文章来源[:：]?\s*(\d{4}-\d{2}-\d{2})")


def discover_latest_regional_table(index_document: dict[str, Any]) -> dict[str, str]:
    for link in index_document.get("links", []):
        title = str(link.get("text", "")).strip()
        url = str(link.get("url", "")).strip()
        if _REGIONAL_TITLE_RE.match(title) and url.startswith("https://www.pbc.gov.cn/"):
            return {"title": title, "url": url}
    raise ValueError("no PBC regional social-financing table found on official index")


def discover_xlsx_attachment(detail_document: dict[str, Any]) -> str:
    for link in detail_document.get("links", []):
        url = str(link.get("url", "")).strip()
        text = str(link.get("text", "")).strip()
        if (
            url.startswith("https://www.pbc.gov.cn/")
            and url.lower().endswith(".xlsx")
            and "地区社会融资规模增量统计表" in text
        ):
            return url
    raise ValueError("official regional social-financing XLSX attachment not found")


def _normalized_text(value: Any) -> str:
    return re.sub(r"\s+", "", str(value or ""))


def extract_region_total(
    rows: list[list[Any]],
    *,
    region: str,
    expected_table_title: str | None = None,
) -> dict[str, Any]:
    """Extract regional AFRE total while retaining source row/header evidence."""
    title_semantics = bool(
        expected_table_title and _REGIONAL_TITLE_RE.match(expected_table_title.strip())
    )

    for row_index, row in enumerate(rows):
        for col_index, cell in enumerate(row):
            label = _normalized_text(cell)
            if region not in label:
                continue

            header_start = max(0, row_index - 20)
            header_rows = rows[header_start:row_index]
            header_text = " ".join(
                _normalized_text(value)
                for header in header_rows
                for value in header
                if value is not None
            )
            header_semantics = "社会融资" in header_text and "增量" in header_text
            if not header_semantics and not title_semantics:
                raise ValueError(
                    "regional XLSX semantics not recognized from workbook headers or official detail title"
                )

            total_col = None
            total_value = None
            for candidate_col in range(col_index + 1, len(row)):
                candidate = row[candidate_col]
                if isinstance(candidate, bool):
                    continue
                if isinstance(candidate, (int, float)):
                    total_col = candidate_col
                    total_value = float(candidate)
                    break
                if isinstance(candidate, str):
                    try:
                        total_value = float(candidate.replace(",", ""))
                        total_col = candidate_col
                        break
                    except ValueError:
                        continue
            if total_col is None or total_value is None:
                raise ValueError(f"no numeric AFRE total found to the right of {region}")
            if not 0 < total_value < 100_000:
                raise ValueError(f"regional AFRE total outside sanity bounds: {total_value}")

            return {
                "region": region,
                "matched_label": str(cell),
                "row_number_1based": row_index + 1,
                "region_column_1based": col_index + 1,
                "total_column_1based": total_col + 1,
                "social_financing_flow_100m_cny": total_value,
                "social_financing_flow_trillion_cny": total_value / 10_000.0,
                "semantic_gate": (
                    "WORKBOOK_HEADER" if header_semantics else "OFFICIAL_DETAIL_TITLE_FALLBACK"
                ),
                "row_values": row,
                "header_context": header_rows,
            }
    raise ValueError(f"region not found in official PBC XLSX: {region}")


class PbcRegionalFinancingAdapter:
    def __init__(
        self,
        *,
        html_client: PublicHtmlClient | None = None,
        xlsx_client: PublicXlsxClient | None = None,
    ) -> None:
        self.html_client = html_client or PublicHtmlClient(
            source_id=SOURCE_ID,
            allowed_hosts=ALLOWED_HOSTS,
            timeout_seconds=20,
            retries=2,
            max_response_bytes=4_000_000,
        )
        self.xlsx_client = xlsx_client or PublicXlsxClient(
            source_id=SOURCE_ID,
            allowed_hosts=ALLOWED_HOSTS,
            timeout_seconds=20,
            retries=2,
            max_response_bytes=20_000_000,
        )

    def collect_region(self, *, region: str = "江苏") -> dict[str, Any]:
        index_env = self.html_client.fetch(INDEX_URL, request_name="pbc-statistics-index-regional")
        index_doc = html_to_document(index_env.html, base_url=index_env.url)
        discovered = discover_latest_regional_table(index_doc)

        detail_env = self.html_client.fetch(discovered["url"], request_name="pbc-regional-table-detail")
        detail_doc = html_to_document(detail_env.html, base_url=detail_env.url)
        attachment_url = discover_xlsx_attachment(detail_doc)
        release_match = _RELEASE_DATE_RE.search(detail_doc["text"])
        release_date = release_match.group(1) if release_match else None

        xlsx_env = self.xlsx_client.fetch(attachment_url, request_name="pbc-regional-table-xlsx")
        rows = parse_first_sheet_rows(xlsx_env.payload)
        region_result = extract_region_total(
            rows,
            region=region,
            expected_table_title=discovered["title"],
        )

        return {
            "source_id": SOURCE_ID,
            "collected_at_utc": datetime.now(timezone.utc).isoformat(),
            "data_available": True,
            "table_title": discovered["title"],
            "release_date": release_date,
            "region_observation": region_result,
            "workbook_row_count": len(rows),
            "provenance": {
                "index": index_env.metadata(),
                "detail": detail_env.metadata(),
                "xlsx": xlsx_env.metadata(),
            },
            "truth_note": (
                "The region total is extracted from the newest official PBC regional AFRE XLSX. "
                "Workbook headers are preferred for semantic confirmation; merged-cell layouts may "
                "fall back only to the exact official PBC detail-page title. The complete matched row "
                "and nearby header context are retained for audit."
            ),
        }
