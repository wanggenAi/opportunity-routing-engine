"""Network ingestion primitives for the continuous discovery engine.

This module deliberately does not know business meaning.  It is responsible for one
thing only: fetching public/authorized JSON evidence without silently converting
network failures, HTML challenges, stale data or malformed responses into facts.

Truth rules:
- network failure != zero;
- HTML/challenge page != JSON data;
- missing != PASS;
- provenance must travel with every payload;
- only explicitly allowed hosts may be queried by a configured client.
"""

from __future__ import annotations

import csv
import hashlib
import json
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


class NetworkIngestError(RuntimeError):
    """Base class for network-ingestion failures."""


class HostNotAllowedError(NetworkIngestError):
    pass


class NonJsonResponseError(NetworkIngestError):
    pass


class ResponseTooLargeError(NetworkIngestError):
    pass


@dataclass(frozen=True)
class FetchEnvelope:
    source_id: str
    request_name: str
    url: str
    fetched_at_utc: str
    http_status: int
    content_type: str
    payload_sha256: str
    payload: Any

    def metadata(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("payload")
        return data

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SourceRegistryEntry:
    source_id: str
    name: str
    source_tier: str
    owner: str
    base_url: str
    geography: str
    indicator_scope: str
    access_mode: str
    refresh_cadence: str
    automation_allowed: str
    status: str


Transport = Callable[[Request, float], Any]


def _default_transport(request: Request, timeout: float) -> Any:
    return urlopen(request, timeout=timeout)


class JsonHttpClient:
    """Small stdlib-only JSON client with retries and evidence provenance.

    The client is intentionally narrow.  It supports HTTPS JSON endpoints only by
    default, caps response size, rejects HTML masquerading as success, and retries
    only transient network/HTTP failures.
    """

    def __init__(
        self,
        *,
        source_id: str,
        allowed_hosts: Iterable[str],
        timeout_seconds: float = 20.0,
        retries: int = 2,
        retry_backoff_seconds: float = 0.5,
        max_response_bytes: int = 8_000_000,
        transport: Transport | None = None,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if retries < 0:
            raise ValueError("retries must be >= 0")
        if max_response_bytes <= 0:
            raise ValueError("max_response_bytes must be positive")

        normalized_hosts = {host.strip().lower() for host in allowed_hosts if host.strip()}
        if not normalized_hosts:
            raise ValueError("allowed_hosts must not be empty")

        self.source_id = source_id
        self.allowed_hosts = normalized_hosts
        self.timeout_seconds = timeout_seconds
        self.retries = retries
        self.retry_backoff_seconds = retry_backoff_seconds
        self.max_response_bytes = max_response_bytes
        self.transport = transport or _default_transport

    def _validate_url(self, url: str) -> None:
        parsed = urlparse(url)
        if parsed.scheme != "https":
            raise HostNotAllowedError("only https endpoints are allowed")
        host = (parsed.hostname or "").lower()
        if host not in self.allowed_hosts:
            raise HostNotAllowedError(f"host not allowlisted: {host!r}")

    @staticmethod
    def _content_type(response: Any) -> str:
        headers = getattr(response, "headers", None)
        if headers is None:
            return ""
        getter = getattr(headers, "get_content_type", None)
        if callable(getter):
            try:
                return str(getter())
            except Exception:
                pass
        get = getattr(headers, "get", None)
        if callable(get):
            return str(get("Content-Type", ""))
        return ""

    def _decode_json(self, response: Any, *, url: str, request_name: str) -> FetchEnvelope:
        status = int(getattr(response, "status", None) or response.getcode())
        body = response.read(self.max_response_bytes + 1)
        if len(body) > self.max_response_bytes:
            raise ResponseTooLargeError(
                f"response exceeded {self.max_response_bytes} bytes: {request_name}"
            )

        text = body.decode("utf-8-sig", errors="strict").lstrip()
        if text.startswith("<"):
            snippet = text[:160].replace("\n", " ")
            raise NonJsonResponseError(
                f"HTML/challenge response rejected for {request_name}: {snippet!r}"
            )

        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            raise NonJsonResponseError(
                f"non-JSON response rejected for {request_name}"
            ) from exc

        digest = hashlib.sha256(body).hexdigest()
        return FetchEnvelope(
            source_id=self.source_id,
            request_name=request_name,
            url=url,
            fetched_at_utc=datetime.now(timezone.utc).isoformat(),
            http_status=status,
            content_type=self._content_type(response),
            payload_sha256=digest,
            payload=payload,
        )

    def request_json(
        self,
        method: str,
        url: str,
        *,
        request_name: str,
        params: Mapping[str, Any] | None = None,
        json_body: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> FetchEnvelope:
        method = method.upper().strip()
        if method not in {"GET", "POST"}:
            raise ValueError("only GET and POST are supported")

        if params:
            query = urlencode(params, doseq=True)
            url = f"{url}{'&' if '?' in url else '?'}{query}"
        self._validate_url(url)

        request_headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "OpportunityRoutingEngine/0.1 (+public-evidence-ingest)",
        }
        if headers:
            request_headers.update(headers)

        body: bytes | None = None
        if json_body is not None:
            body = json.dumps(json_body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            request_headers.setdefault("Content-Type", "application/json;charset=UTF-8")

        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            request = Request(url, data=body, headers=request_headers, method=method)
            try:
                response = self.transport(request, self.timeout_seconds)
                try:
                    return self._decode_json(
                        response, url=url, request_name=request_name
                    )
                finally:
                    close = getattr(response, "close", None)
                    if callable(close):
                        close()
            except HTTPError as exc:
                last_error = exc
                transient = exc.code in {408, 425, 429, 500, 502, 503, 504}
                if not transient or attempt >= self.retries:
                    raise NetworkIngestError(
                        f"HTTP {exc.code} for {request_name}"
                    ) from exc
            except (URLError, TimeoutError, OSError) as exc:
                last_error = exc
                if attempt >= self.retries:
                    raise NetworkIngestError(
                        f"network failure for {request_name}: {exc}"
                    ) from exc

            if self.retry_backoff_seconds > 0:
                time.sleep(self.retry_backoff_seconds * (attempt + 1))

        raise NetworkIngestError(
            f"request failed for {request_name}: {last_error}"
        )


def load_source_registry(path: str | Path) -> dict[str, SourceRegistryEntry]:
    """Load source registry keyed by source_id, rejecting duplicate/malformed rows."""

    registry_path = Path(path)
    with registry_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {field.name for field in SourceRegistryEntry.__dataclass_fields__.values()}
        if reader.fieldnames is None or set(reader.fieldnames) != required:
            raise ValueError(
                f"source registry columns mismatch; expected={sorted(required)}, "
                f"actual={sorted(reader.fieldnames or [])}"
            )

        result: dict[str, SourceRegistryEntry] = {}
        for row in reader:
            entry = SourceRegistryEntry(**{key: row[key].strip() for key in required})
            if not entry.source_id:
                raise ValueError("source_id must not be empty")
            if entry.source_id in result:
                raise ValueError(f"duplicate source_id: {entry.source_id}")
            result[entry.source_id] = entry
        return result


def write_json_atomic(path: str | Path, payload: Any) -> None:
    """Write UTF-8 JSON atomically so interrupted collection does not corrupt state."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tmp.replace(target)
