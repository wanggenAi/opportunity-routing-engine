"""PBC Jiangsu monthly credit/deposit money-flow adapter.

The Jiangsu branch of the People's Bank of China publishes a public monthly
``江苏省金融机构信贷收支表`` index.  Each release links to an official legacy
``.xls`` workbook.  This adapter discovers the newest release, preserves
provenance, selects the RMB credit sheet semantically, and extracts a bounded set
of core deposit/loan levels without turning missing cells into zero.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timezone
from typing import Any
from urllib.parse import urlparse

from src.html_ingest import PublicHtmlClient, html_to_document
from src.xls_ingest import PublicXlsClient, parse_workbook_rows


SOURCE_ID = "CN_PBOC_JS"
INDEX_URL = "https://nanjing.pbc.gov.cn/nanjing/117532/index.html"
ALLOWED_HOSTS = {"nanjing.pbc.gov.cn"}
_TABLE_RE = re.compile(r"^(\d{4})年(\d{1,2})月江苏省金融机构信贷收支表$")
_RELEASE_DATE_RE = re.compile(r"文章来源[:：]?\s*(\d{4}-\d{2}-\d{2})")

_REQUIRED_METRICS = {
    "total_deposits_100m_cny": "各项存款",
    "household_deposits_100m_cny": "住户存款",
    "nonfinancial_enterprise_deposits_100m_cny": "非金融企业存款",
    "total_loans_100m_cny": "各项贷款",
}
_OPTIONAL_METRICS = {
    "household_loans_100m_cny": "住户贷款",
    "enterprise_institution_loans_100m_cny": "企（事）业单位贷款",
}


def _official_branch_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname == "nanjing.pbc.gov.cn"


def discover_latest_credit_table(index_document: dict[str, Any]) -> dict[str, str]:
    candidates: list[tuple[int, int, str, str]] = []
    for link in index_document.get("links", []):
        title = str(link.get("text", "")).strip()
        url = str(link.get("url", "")).strip()
        match = _TABLE_RE.match(title)
        if not match or not _official_branch_url(url):
            continue
        candidates.append((int(match.group(1)), int(match.group(2)), title, url))
    if not candidates:
        raise ValueError("no official PBC Jiangsu monthly credit table found")
    year, month, title, url = max(candidates, key=lambda item: (item[0], item[1]))
    return {
        "title": title,
        "url": url,
        "observation_period": f"{year:04d}-{month:02d}",
        "period_key": f"{year:04d}.{month:02d}",
    }


def discover_xls_attachment(detail_document: dict[str, Any], *, expected_title: str) -> str:
    exact_text = f"{expected_title}.xls"
    candidates: list[str] = []
    for link in detail_document.get("links", []):
        url = str(link.get("url", "")).strip()
        text = str(link.get("text", "")).strip()
        if not _official_branch_url(url) or not url.lower().endswith(".xls"):
            continue
        if text == exact_text:
            return url
        if "江苏省金融机构信贷收支表" in text:
            candidates.append(url)
    if len(candidates) == 1:
        return candidates[0]
    raise ValueError("official Jiangsu credit XLS attachment missing or ambiguous")


def _normalized_text(value: Any) -> str:
    return re.sub(r"\s+", "", str(value or "")).replace("：", ":")


def _period_forms(period_key: str) -> set[str]:
    match = re.fullmatch(r"(\d{4})\.(\d{2})", period_key)
    if not match:
        raise ValueError(f"invalid period key: {period_key}")
    year = match.group(1)
    month = int(match.group(2))
    return {
        f"{year}.{month:02d}",
        f"{year}.{month}",
        f"{year}-{month:02d}",
        f"{year}年{month}月",
        f"{year}年{month:02d}月",
    }


def _is_rmb_credit_sheet(sheet: dict[str, Any]) -> bool:
    name = _normalized_text(sheet.get("sheet_name"))
    rows = sheet.get("rows", [])
    text = "".join(
        _normalized_text(cell)
        for row in rows[:30]
        for cell in row
        if cell is not None
    )
    if "本外币" in name or "本外币信贷收支表" in text:
        return False
    return (
        ("人民币" in name and "信贷" in name)
        or "金融机构人民币信贷收支表" in text
        or "人民币信贷收支表" in text
    )


def _find_value_column(rows: list[list[Any]], *, period_key: str) -> tuple[int, int, str]:
    forms = _period_forms(period_key)
    matches: list[tuple[int, int]] = []
    for row_index, row in enumerate(rows[:40]):
        for col_index, cell in enumerate(row):
            if _normalized_text(cell) in forms:
                matches.append((row_index, col_index))
    columns = {col for _, col in matches}
    if len(columns) == 1:
        row_index, col_index = matches[0]
        return row_index, col_index, "EXPLICIT_PERIOD_HEADER"
    if len(columns) > 1:
        raise ValueError(f"period header appears in multiple columns: {sorted(columns)}")

    current_balance: list[tuple[int, int]] = []
    for row_index, row in enumerate(rows[:40]):
        for col_index, cell in enumerate(row):
            text = _normalized_text(cell)
            if text in {"本期余额", "期末余额"}:
                current_balance.append((row_index, col_index))
    balance_columns = {col for _, col in current_balance}
    if len(balance_columns) == 1:
        row_index, col_index = current_balance[0]
        return row_index, col_index, "TITLE_PERIOD_CURRENT_BALANCE"
    raise ValueError("cannot identify unique current-period value column in RMB credit sheet")


def _find_metric(
    rows: list[list[Any]],
    *,
    label_token: str,
    value_col: int,
) -> tuple[float, dict[str, Any]] | None:
    matches: list[tuple[int, list[Any]]] = []
    for row_index, row in enumerate(rows):
        if not row:
            continue
        label_cells = row[: min(4, len(row))]
        label_text = "".join(_normalized_text(cell) for cell in label_cells if cell is not None)
        if label_token in label_text:
            matches.append((row_index, row))
    if not matches:
        return None
    if len(matches) != 1:
        raise ValueError(f"metric label is ambiguous for {label_token!r}: {len(matches)} rows")
    row_index, row = matches[0]
    if value_col >= len(row):
        raise ValueError(f"metric {label_token!r} has no cell at value column {value_col + 1}")
    raw = row[value_col]
    if raw is None or raw == "":
        return None
    if isinstance(raw, bool):
        raise ValueError(f"metric {label_token!r} resolved to boolean")
    try:
        value = float(str(raw).replace(",", ""))
    except ValueError as exc:
        raise ValueError(f"metric {label_token!r} is not numeric: {raw!r}") from exc
    if not 0 < value < 1_000_000:
        raise ValueError(f"metric {label_token!r} outside broad sanity bounds: {value}")
    return value, {
        "label_token": label_token,
        "row_number_1based": row_index + 1,
        "value_column_1based": value_col + 1,
        "raw_value": raw,
        "row_values": row,
    }


def extract_jiangsu_credit_metrics(
    workbook: list[dict[str, Any]],
    *,
    period_key: str,
) -> dict[str, Any]:
    candidates = [sheet for sheet in workbook if _is_rmb_credit_sheet(sheet)]
    if len(candidates) != 1:
        names = [str(sheet.get("sheet_name")) for sheet in candidates]
        raise ValueError(f"expected one RMB credit sheet, found {len(candidates)}: {names}")

    sheet = candidates[0]
    rows = sheet.get("rows", [])
    if not rows:
        raise ValueError("RMB credit sheet contains no rows")
    header_text = "".join(
        _normalized_text(cell)
        for row in rows[:40]
        for cell in row
        if cell is not None
    )
    if "单位:亿元" not in header_text and "单位:亿元人民币" not in header_text:
        raise ValueError("RMB credit sheet unit is not explicitly 亿元")

    header_row, value_col, period_gate = _find_value_column(rows, period_key=period_key)
    metrics: dict[str, float | None] = {}
    evidence: dict[str, Any] = {}
    missing: list[str] = []

    for output_name, label in _REQUIRED_METRICS.items():
        found = _find_metric(rows, label_token=label, value_col=value_col)
        if found is None:
            missing.append(output_name)
            metrics[output_name] = None
            continue
        value, row_evidence = found
        metrics[output_name] = value
        evidence[output_name] = row_evidence

    if missing:
        raise ValueError(f"required Jiangsu credit metrics missing: {missing}")

    for output_name, label in _OPTIONAL_METRICS.items():
        found = _find_metric(rows, label_token=label, value_col=value_col)
        if found is None:
            metrics[output_name] = None
            continue
        value, row_evidence = found
        metrics[output_name] = value
        evidence[output_name] = row_evidence

    total_deposits = float(metrics["total_deposits_100m_cny"] or 0)
    total_loans = float(metrics["total_loans_100m_cny"] or 0)
    metrics["total_deposits_trillion_cny"] = total_deposits / 10_000.0
    metrics["total_loans_trillion_cny"] = total_loans / 10_000.0

    header_start = max(0, header_row - 8)
    header_end = min(len(rows), header_row + 3)
    return {
        "sheet_index": sheet.get("sheet_index"),
        "sheet_name": sheet.get("sheet_name"),
        "period_key": period_key,
        "period_gate": period_gate,
        "header_row_number_1based": header_row + 1,
        "value_column_1based": value_col + 1,
        "unit": "100m_cny",
        "metrics": metrics,
        "metric_evidence": evidence,
        "header_context": rows[header_start:header_end],
    }


def _freshness(release_date: str | None) -> dict[str, Any]:
    if not release_date:
        return {"release_date": None, "age_days": None, "status": "UNKNOWN"}
    published = date.fromisoformat(release_date)
    today = datetime.now(timezone.utc).date()
    age_days = (today - published).days
    if age_days < 0:
        status = "FUTURE_DATE_ERROR"
    elif age_days <= 45:
        status = "FRESH"
    elif age_days <= 90:
        status = "AGING"
    else:
        status = "STALE"
    return {"release_date": release_date, "age_days": age_days, "status": status}


class PbcJiangsuCreditAdapter:
    def __init__(
        self,
        *,
        html_client: PublicHtmlClient | None = None,
        xls_client: PublicXlsClient | None = None,
    ) -> None:
        self.html_client = html_client or PublicHtmlClient(
            source_id=SOURCE_ID,
            allowed_hosts=ALLOWED_HOSTS,
            timeout_seconds=20,
            retries=2,
            max_response_bytes=4_000_000,
        )
        self.xls_client = xls_client or PublicXlsClient(
            source_id=SOURCE_ID,
            allowed_hosts=ALLOWED_HOSTS,
            timeout_seconds=20,
            retries=2,
            max_response_bytes=20_000_000,
        )

    def collect(self) -> dict[str, Any]:
        index_env = self.html_client.fetch(INDEX_URL, request_name="pbc-js-financial-data-index")
        index_doc = html_to_document(index_env.html, base_url=index_env.url)
        discovered = discover_latest_credit_table(index_doc)

        detail_env = self.html_client.fetch(discovered["url"], request_name="pbc-js-credit-detail")
        detail_doc = html_to_document(detail_env.html, base_url=detail_env.url)
        release_match = _RELEASE_DATE_RE.search(detail_doc["text"])
        release_date = release_match.group(1) if release_match else None
        attachment_url = discover_xls_attachment(
            detail_doc,
            expected_title=discovered["title"],
        )

        xls_env = self.xls_client.fetch(attachment_url, request_name="pbc-js-credit-xls")
        workbook = parse_workbook_rows(xls_env.payload)
        observation = extract_jiangsu_credit_metrics(
            workbook,
            period_key=discovered["period_key"],
        )

        return {
            "source_id": SOURCE_ID,
            "collected_at_utc": datetime.now(timezone.utc).isoformat(),
            "data_available": True,
            "geography": "Jiangsu",
            "table_title": discovered["title"],
            "observation_period": discovered["observation_period"],
            "release_date": release_date,
            "freshness": _freshness(release_date),
            "observation": observation,
            "workbook_sheets": [
                {
                    "sheet_index": sheet.get("sheet_index"),
                    "sheet_name": sheet.get("sheet_name"),
                    "row_count": sheet.get("row_count"),
                    "column_count": sheet.get("column_count"),
                }
                for sheet in workbook
            ],
            "provenance": {
                "index": index_env.metadata(),
                "detail": detail_env.metadata(),
                "xls": xls_env.metadata(),
            },
            "truth_note": (
                "Values come from the newest public monthly PBC Jiangsu credit/deposit XLS. "
                "The RMB sheet, unit, period column and required row labels are all validated "
                "semantically. Missing or ambiguous cells fail closed and are never converted to zero."
            ),
        }
