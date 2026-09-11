"""Bounded HTTPS ingestion for legacy BIFF/OLE .xls workbooks.

Some official Chinese statistical sources still publish Excel 97-2003 files.  A
correct BIFF parser is not reasonable to reimplement with the Python standard
library, so parsing is intentionally delegated to the small, pinned ``xlrd``
optional dependency used only by workflows that ingest legacy XLS.

Truth rules:
- only allowlisted HTTPS hosts may be fetched;
- redirects must end on an allowlisted HTTPS host;
- HTML/challenge responses are rejected;
- response bytes are hashed before semantic parsing;
- malformed/unsupported workbooks fail instead of becoming empty observations;
- workbook dimensions are bounded before rows are materialized.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from src.network_ingest import HostNotAllowedError, NetworkIngestError, ResponseTooLargeError


class NonXlsResponseError(NetworkIngestError):
    pass


class XlsParseError(ValueError):
    pass


_OLE_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"


@dataclass(frozen=True)
class XlsFetchEnvelope:
    source_id: str
    request_name: str
    url: str
    fetched_at_utc: str
    http_status: int
    content_type: str
    payload_sha256: str
    size_bytes: int
    payload: bytes

    def metadata(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("payload")
        return data


Transport = Callable[[Request, float], Any]


def _default_transport(request: Request, timeout: float) -> Any:
    return urlopen(request, timeout=timeout)


def _header(response: Any, name: str) -> str:
    headers = getattr(response, "headers", None)
    if headers is None:
        return ""
    getter = getattr(headers, "get", None)
    return str(getter(name, "")) if callable(getter) else ""


class PublicXlsClient:
    def __init__(
        self,
        *,
        source_id: str,
        allowed_hosts: Iterable[str],
        timeout_seconds: float = 20.0,
        retries: int = 2,
        retry_backoff_seconds: float = 0.5,
        max_response_bytes: int = 20_000_000,
        transport: Transport | None = None,
    ) -> None:
        self.source_id = source_id
        self.allowed_hosts = {host.strip().lower() for host in allowed_hosts if host.strip()}
        if not self.allowed_hosts:
            raise ValueError("allowed_hosts must not be empty")
        if timeout_seconds <= 0 or retries < 0 or max_response_bytes <= 0:
            raise ValueError("invalid XLS client bounds")
        self.timeout_seconds = timeout_seconds
        self.retries = retries
        self.retry_backoff_seconds = retry_backoff_seconds
        self.max_response_bytes = max_response_bytes
        self.transport = transport or _default_transport

    def _validate_url(self, url: str) -> None:
        parsed = urlparse(url)
        if parsed.scheme != "https":
            raise HostNotAllowedError("only https endpoints are allowed")
        if (parsed.hostname or "").lower() not in self.allowed_hosts:
            raise HostNotAllowedError(f"host not allowlisted: {parsed.hostname!r}")

    def fetch(self, url: str, *, request_name: str) -> XlsFetchEnvelope:
        self._validate_url(url)
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            request = Request(
                url,
                headers={
                    "Accept": "application/vnd.ms-excel,application/octet-stream;q=0.9,*/*;q=0.2",
                    "User-Agent": "OpportunityRoutingEngine/0.1 (+public-evidence-ingest)",
                },
                method="GET",
            )
            try:
                response = self.transport(request, self.timeout_seconds)
                try:
                    final_url = str(getattr(response, "url", None) or response.geturl())
                    self._validate_url(final_url)
                    status = int(getattr(response, "status", None) or response.getcode())
                    body = response.read(self.max_response_bytes + 1)
                    if len(body) > self.max_response_bytes:
                        raise ResponseTooLargeError(
                            f"XLS response exceeded {self.max_response_bytes} bytes: {request_name}"
                        )
                    snippet = body[:80].lstrip().lower()
                    if snippet.startswith((b"<html", b"<!doctype", b"<?xml")):
                        raise NonXlsResponseError(
                            f"HTML/XML challenge response rejected for {request_name}"
                        )
                    if not body.startswith(_OLE_MAGIC):
                        raise NonXlsResponseError(
                            f"response is not an OLE2 XLS container: {request_name}"
                        )
                    return XlsFetchEnvelope(
                        source_id=self.source_id,
                        request_name=request_name,
                        url=final_url,
                        fetched_at_utc=datetime.now(timezone.utc).isoformat(),
                        http_status=status,
                        content_type=_header(response, "Content-Type"),
                        payload_sha256=hashlib.sha256(body).hexdigest(),
                        size_bytes=len(body),
                        payload=body,
                    )
                finally:
                    close = getattr(response, "close", None)
                    if callable(close):
                        close()
            except HTTPError as exc:
                last_error = exc
                transient = exc.code in {408, 425, 429, 500, 502, 503, 504}
                if not transient or attempt >= self.retries:
                    raise NetworkIngestError(f"HTTP {exc.code} for {request_name}") from exc
            except (URLError, TimeoutError, OSError) as exc:
                last_error = exc
                if attempt >= self.retries:
                    raise NetworkIngestError(
                        f"network failure for {request_name}: {exc}"
                    ) from exc
            if self.retry_backoff_seconds > 0:
                time.sleep(self.retry_backoff_seconds * (attempt + 1))
        raise NetworkIngestError(f"XLS request failed for {request_name}: {last_error}")


def _clean_cell(value: Any) -> Any:
    if value == "":
        return None
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def parse_workbook_rows(
    payload: bytes,
    *,
    max_sheets: int = 16,
    max_rows_per_sheet: int = 2_000,
    max_cols_per_sheet: int = 256,
) -> list[dict[str, Any]]:
    """Parse all bounded sheets from an OLE2 XLS workbook using optional xlrd."""
    if not payload.startswith(_OLE_MAGIC):
        raise XlsParseError("invalid OLE2 XLS signature")
    if max_sheets <= 0 or max_rows_per_sheet <= 0 or max_cols_per_sheet <= 0:
        raise ValueError("workbook bounds must be positive")

    try:
        import xlrd  # type: ignore
    except ImportError as exc:  # pragma: no cover - exercised by live workflow with dependency installed
        raise XlsParseError(
            "legacy XLS parsing requires optional dependency xlrd==2.0.2"
        ) from exc

    try:
        workbook = xlrd.open_workbook(file_contents=payload, on_demand=True)
    except Exception as exc:
        raise XlsParseError(f"unable to open XLS workbook: {exc}") from exc

    sheet_names = list(workbook.sheet_names())
    if not sheet_names:
        raise XlsParseError("XLS workbook contains no sheets")
    if len(sheet_names) > max_sheets:
        raise XlsParseError(
            f"XLS workbook has too many sheets: {len(sheet_names)} > {max_sheets}"
        )

    parsed: list[dict[str, Any]] = []
    for sheet_index, sheet_name in enumerate(sheet_names):
        sheet = workbook.sheet_by_index(sheet_index)
        if sheet.nrows > max_rows_per_sheet:
            raise XlsParseError(
                f"XLS sheet {sheet_name!r} has too many rows: {sheet.nrows}"
            )
        if sheet.ncols > max_cols_per_sheet:
            raise XlsParseError(
                f"XLS sheet {sheet_name!r} has too many columns: {sheet.ncols}"
            )
        rows = [
            [_clean_cell(value) for value in sheet.row_values(row_index)]
            for row_index in range(sheet.nrows)
        ]
        parsed.append(
            {
                "sheet_index": sheet_index,
                "sheet_name": str(sheet_name),
                "row_count": sheet.nrows,
                "column_count": sheet.ncols,
                "rows": rows,
            }
        )
    release_resources = getattr(workbook, "release_resources", None)
    if callable(release_resources):
        release_resources()
    return parsed
