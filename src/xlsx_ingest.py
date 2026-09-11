"""Bounded HTTPS XLSX ingestion with provenance and stdlib-only parsing.

This module exists because several Chinese official sources publish structured
statistics as XLSX attachments rather than APIs.  It deliberately avoids browser
or office automation and does not require openpyxl on the runner.

Truth rules:
- only allowlisted HTTPS hosts may be fetched;
- redirects must end on an allowlisted HTTPS host;
- HTML/challenge responses are rejected as spreadsheets;
- response bytes are hashed before semantic parsing;
- malformed/unsupported workbooks fail instead of becoming empty observations.
"""

from __future__ import annotations

import hashlib
import io
import re
import time
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

from src.network_ingest import HostNotAllowedError, NetworkIngestError, ResponseTooLargeError


class NonSpreadsheetResponseError(NetworkIngestError):
    pass


class XlsxParseError(ValueError):
    pass


@dataclass(frozen=True)
class BinaryFetchEnvelope:
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


class PublicXlsxClient:
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
            raise ValueError("invalid XLSX client bounds")
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

    def fetch(self, url: str, *, request_name: str) -> BinaryFetchEnvelope:
        self._validate_url(url)
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            request = Request(
                url,
                headers={
                    "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream;q=0.9,*/*;q=0.2",
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
                            f"XLSX response exceeded {self.max_response_bytes} bytes: {request_name}"
                        )
                    if not body.startswith(b"PK"):
                        snippet = body[:80].lstrip().lower()
                        if snippet.startswith(b"<"):
                            raise NonSpreadsheetResponseError(
                                f"HTML/challenge response rejected for {request_name}"
                            )
                        raise NonSpreadsheetResponseError(
                            f"response is not an XLSX zip container: {request_name}"
                        )
                    return BinaryFetchEnvelope(
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
        raise NetworkIngestError(f"XLSX request failed for {request_name}: {last_error}")


_CELL_REF_RE = re.compile(r"^([A-Z]+)([0-9]+)$")


def _column_index(cell_ref: str) -> int:
    match = _CELL_REF_RE.match(cell_ref.upper())
    if not match:
        raise XlsxParseError(f"invalid cell reference: {cell_ref!r}")
    value = 0
    for char in match.group(1):
        value = value * 26 + (ord(char) - ord("A") + 1)
    return value - 1


def _shared_strings(zf: zipfile.ZipFile) -> list[str]:
    try:
        raw = zf.read("xl/sharedStrings.xml")
    except KeyError:
        return []
    root = ET.fromstring(raw)
    strings: list[str] = []
    for si in root.iter():
        if si.tag.endswith("}si"):
            parts = [node.text or "" for node in si.iter() if node.tag.endswith("}t")]
            strings.append("".join(parts))
    return strings


def _first_sheet_path(zf: zipfile.ZipFile) -> str:
    try:
        workbook = ET.fromstring(zf.read("xl/workbook.xml"))
        rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    except (KeyError, ET.ParseError) as exc:
        raise XlsxParseError("workbook metadata missing or malformed") from exc

    rel_map: dict[str, str] = {}
    for rel in rels:
        rid = rel.attrib.get("Id")
        target = rel.attrib.get("Target")
        if rid and target:
            rel_map[rid] = target

    for sheet in workbook.iter():
        if not sheet.tag.endswith("}sheet"):
            continue
        rid = None
        for key, value in sheet.attrib.items():
            if key.endswith("}id"):
                rid = value
                break
        if rid and rid in rel_map:
            target = rel_map[rid]
            return urljoin("xl/", target).lstrip("/")
    raise XlsxParseError("no worksheet relationship found")


def _cell_value(cell: ET.Element, shared: list[str]) -> Any:
    cell_type = cell.attrib.get("t", "")
    if cell_type == "inlineStr":
        parts = [node.text or "" for node in cell.iter() if node.tag.endswith("}t")]
        return "".join(parts)

    value_node = next((node for node in cell if node.tag.endswith("}v")), None)
    if value_node is None or value_node.text is None:
        return None
    raw = value_node.text
    if cell_type == "s":
        try:
            return shared[int(raw)]
        except (ValueError, IndexError) as exc:
            raise XlsxParseError(f"invalid shared-string index: {raw!r}") from exc
    if cell_type in {"str", "e"}:
        return raw
    if cell_type == "b":
        return raw == "1"
    try:
        number = float(raw)
        return int(number) if number.is_integer() else number
    except ValueError:
        return raw


def parse_first_sheet_rows(payload: bytes) -> list[list[Any]]:
    """Return rectangular-ish row arrays from the first XLSX worksheet."""
    try:
        zf = zipfile.ZipFile(io.BytesIO(payload))
    except zipfile.BadZipFile as exc:
        raise XlsxParseError("invalid XLSX zip container") from exc

    with zf:
        shared = _shared_strings(zf)
        sheet_path = _first_sheet_path(zf)
        try:
            root = ET.fromstring(zf.read(sheet_path))
        except (KeyError, ET.ParseError) as exc:
            raise XlsxParseError(f"worksheet missing or malformed: {sheet_path}") from exc

        rows: list[list[Any]] = []
        for row_node in root.iter():
            if not row_node.tag.endswith("}row"):
                continue
            values: list[Any] = []
            for cell in row_node:
                if not cell.tag.endswith("}c"):
                    continue
                ref = cell.attrib.get("r")
                if not ref:
                    continue
                index = _column_index(ref)
                while len(values) <= index:
                    values.append(None)
                values[index] = _cell_value(cell, shared)
            while values and values[-1] is None:
                values.pop()
            rows.append(values)
        if not rows:
            raise XlsxParseError("worksheet contains no rows")
        return rows
