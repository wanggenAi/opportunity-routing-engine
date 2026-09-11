"""Public HTML ingestion primitives for official publication sources.

Unlike JSON ingestion, some official regional sources expose useful evidence only as
HTML publication/list pages. This module fetches bounded public pages, retains
provenance, rejects binary responses, and converts HTML to normalized text without
pretending that text extraction is a semantic fact parser.

It does not bypass login, CAPTCHA, anti-bot controls, or access restrictions.
"""

from __future__ import annotations

import hashlib
import re
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from typing import Any, Callable, Iterable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

from src.network_ingest import HostNotAllowedError, NetworkIngestError, ResponseTooLargeError


class NonHtmlResponseError(NetworkIngestError):
    pass


@dataclass(frozen=True)
class HtmlFetchEnvelope:
    source_id: str
    request_name: str
    url: str
    fetched_at_utc: str
    http_status: int
    content_type: str
    payload_sha256: str
    encoding: str
    html: str

    def metadata(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("html")
        return data


@dataclass(frozen=True)
class LinkRecord:
    href: str
    text: str


Transport = Callable[[Request, float], Any]


def _default_transport(request: Request, timeout: float) -> Any:
    return urlopen(request, timeout=timeout)


def _header_value(response: Any, name: str) -> str:
    headers = getattr(response, "headers", None)
    if headers is None:
        return ""
    getter = getattr(headers, "get", None)
    return str(getter(name, "")) if callable(getter) else ""


def _encoding_from_headers(response: Any) -> str:
    headers = getattr(response, "headers", None)
    if headers is not None:
        getter = getattr(headers, "get_content_charset", None)
        if callable(getter):
            charset = getter()
            if charset:
                return str(charset).lower()
    return "utf-8"


_DEFAULT_ACCEPTED_CONTENT_TYPES = frozenset(
    {"text/html", "application/xhtml+xml", "text/plain"}
)


class PublicHtmlClient:
    def __init__(
        self,
        *,
        source_id: str,
        allowed_hosts: Iterable[str],
        timeout_seconds: float = 20.0,
        retries: int = 2,
        retry_backoff_seconds: float = 0.5,
        max_response_bytes: int = 10_000_000,
        accepted_content_types: Iterable[str] | None = None,
        transport: Transport | None = None,
    ) -> None:
        self.source_id = source_id
        self.allowed_hosts = {host.strip().lower() for host in allowed_hosts if host.strip()}
        if not self.allowed_hosts:
            raise ValueError("allowed_hosts must not be empty")
        if timeout_seconds <= 0 or max_response_bytes <= 0 or retries < 0:
            raise ValueError("invalid HTML client bounds")
        accepted = (
            _DEFAULT_ACCEPTED_CONTENT_TYPES
            if accepted_content_types is None
            else frozenset(
                value.strip().lower()
                for value in accepted_content_types
                if value and value.strip()
            )
        )
        if not accepted:
            raise ValueError("accepted_content_types must not be empty")
        self.accepted_content_types = accepted
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

    def fetch(
        self,
        url: str,
        *,
        request_name: str,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> HtmlFetchEnvelope:
        if params:
            query = urlencode(params, doseq=True)
            url = f"{url}{'&' if '?' in url else '?'}{query}"
        self._validate_url(url)

        request_headers = {
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5",
            "User-Agent": "OpportunityRoutingEngine/0.1 (+public-evidence-ingest)",
        }
        if headers:
            request_headers.update(headers)

        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            request = Request(url, headers=request_headers, method="GET")
            try:
                response = self.transport(request, self.timeout_seconds)
                try:
                    status = int(getattr(response, "status", None) or response.getcode())
                    body = response.read(self.max_response_bytes + 1)
                    if len(body) > self.max_response_bytes:
                        raise ResponseTooLargeError(
                            f"HTML response exceeded {self.max_response_bytes} bytes: {request_name}"
                        )
                    content_type = _header_value(response, "Content-Type")
                    media_type = content_type.split(";", 1)[0].strip().lower()
                    if media_type and media_type not in self.accepted_content_types:
                        raise NonHtmlResponseError(
                            f"unexpected content type for {request_name}: {content_type}"
                        )
                    encoding = _encoding_from_headers(response)
                    try:
                        html = body.decode(encoding, errors="strict")
                    except (LookupError, UnicodeDecodeError):
                        # Chinese government sites are commonly UTF-8 or GB18030.
                        try:
                            encoding = "utf-8"
                            html = body.decode("utf-8", errors="strict")
                        except UnicodeDecodeError:
                            encoding = "gb18030"
                            html = body.decode("gb18030", errors="strict")
                    return HtmlFetchEnvelope(
                        source_id=self.source_id,
                        request_name=request_name,
                        url=url,
                        fetched_at_utc=datetime.now(timezone.utc).isoformat(),
                        http_status=status,
                        content_type=content_type,
                        payload_sha256=hashlib.sha256(body).hexdigest(),
                        encoding=encoding,
                        html=html,
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

        raise NetworkIngestError(f"HTML request failed for {request_name}: {last_error}")


class _DocumentParser(HTMLParser):
    # ``noscript`` is intentionally retained. Some first-party government pages put
    # the authoritative article body in a noscript fallback even though the raw
    # response contains no executable script. Treating noscript as noise erased the
    # project identity and budget from those pages. Executable/non-content elements
    # remain excluded.
    SKIP_TAGS = {"script", "style", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.text_parts: list[str] = []
        self.links: list[LinkRecord] = []
        self._link_href: str | None = None
        self._link_text: list[str] = []
        self.title_parts: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag == "a":
            self._link_href = dict(attrs).get("href")
            self._link_text = []
        elif tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            if self.skip_depth:
                self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag == "a" and self._link_href:
            text = normalize_whitespace(" ".join(self._link_text))
            if text:
                self.links.append(LinkRecord(self._link_href, text))
            self._link_href = None
            self._link_text = []
        elif tag == "title":
            self._in_title = False
        elif tag in {"p", "div", "li", "tr", "td", "th", "h1", "h2", "h3", "br"}:
            self.text_parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = unescape(data)
        if self._link_href is not None:
            self._link_text.append(text)
        if self._in_title:
            self.title_parts.append(text)
        self.text_parts.append(text)


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def html_to_document(html: str, *, base_url: str) -> dict[str, Any]:
    parser = _DocumentParser()
    parser.feed(html)
    lines = [normalize_whitespace(line) for line in "".join(parser.text_parts).splitlines()]
    text = "\n".join(line for line in lines if line)
    links = [
        {"url": urljoin(base_url, record.href), "text": record.text}
        for record in parser.links
        if record.href and not record.href.lower().startswith(("javascript:", "mailto:", "#"))
    ]
    return {
        "title": normalize_whitespace(" ".join(parser.title_parts)),
        "text": text,
        "links": links,
    }
