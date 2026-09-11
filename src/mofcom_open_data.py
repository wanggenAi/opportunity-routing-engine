"""Free official MOFCOM open-data API adapter.

MOFCOM's current HTTPS dataset-detail pages explicitly document JSON API request
paths using plain HTTP. We do not weaken the repository-wide HTTPS JSON client for
that exception. Instead this module isolates the exact documented host/path and
marks every result as PLAINTEXT_HTTP so downstream code can require corroboration.

Truth rules:
- transport/API success != current/fresh/available data;
- API status=1 with blank `data` is still unavailable;
- API status=0 is an error, never zero-valued evidence;
- missing/blank data remains unavailable;
- raw payload is preserved before dataset-specific normalization;
- plain-HTTP MOFCOM evidence is lower-trust and must be corroborated before it can
  promote a money-flow conclusion.
"""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from src.network_ingest import FetchEnvelope


MOFCOM_HOST = "opendata.mofcom.gov.cn"
MOFCOM_PATH = "/front/data/jsonData"
MOFCOM_JSON_ENDPOINT = f"http://{MOFCOM_HOST}{MOFCOM_PATH}"


class MofcomOpenDataError(RuntimeError):
    pass


@dataclass(frozen=True)
class MofcomDatasetSpec:
    dataset_id: str
    name: str
    theme: str
    refresh_cadence: str
    enabled: bool


def _data_available(data: Any) -> bool:
    if data is None:
        return False
    if isinstance(data, str):
        return bool(data.strip())
    if isinstance(data, (list, dict, tuple, set)):
        return len(data) > 0
    return True


def load_mofcom_watchlist(path: str | Path) -> list[MofcomDatasetSpec]:
    required = {"dataset_id", "name", "theme", "refresh_cadence", "enabled"}
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or set(reader.fieldnames) != required:
            raise ValueError(
                f"MOFCOM watchlist columns mismatch; expected={sorted(required)}, "
                f"actual={sorted(reader.fieldnames or [])}"
            )
        result: list[MofcomDatasetSpec] = []
        seen: set[str] = set()
        for row in reader:
            dataset_id = row["dataset_id"].strip().upper()
            if not dataset_id or dataset_id in seen:
                raise ValueError(f"invalid/duplicate dataset_id: {dataset_id!r}")
            seen.add(dataset_id)
            flag = row["enabled"].strip().lower()
            if flag not in {"true", "false"}:
                raise ValueError("enabled must be true or false")
            result.append(
                MofcomDatasetSpec(
                    dataset_id=dataset_id,
                    name=row["name"].strip(),
                    theme=row["theme"].strip(),
                    refresh_cadence=row["refresh_cadence"].strip(),
                    enabled=flag == "true",
                )
            )
    return result


class MofcomOfficialHttpClient:
    """Exact-host/path client for the plain-HTTP endpoint documented by MOFCOM."""

    def __init__(self, *, timeout_seconds: float = 30.0, max_response_bytes: int = 8_000_000) -> None:
        self.timeout_seconds = timeout_seconds
        self.max_response_bytes = max_response_bytes

    def request_dataset(self, dataset_id: str, *, request_name: str) -> FetchEnvelope:
        query = urlencode({"id": dataset_id})
        requested_url = f"{MOFCOM_JSON_ENDPOINT}?{query}"
        parsed = urlparse(requested_url)
        if parsed.scheme != "http" or parsed.hostname != MOFCOM_HOST or parsed.path != MOFCOM_PATH:
            raise MofcomOpenDataError("MOFCOM HTTP client only permits the documented exact endpoint")
        request = Request(
            requested_url,
            headers={
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "OpportunityRoutingEngine/0.1 (+public-evidence-ingest)",
            },
            method="GET",
        )
        try:
            response = urlopen(request, timeout=self.timeout_seconds)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise MofcomOpenDataError(f"MOFCOM documented HTTP endpoint failed: {exc}") from exc
        try:
            final_url = str(getattr(response, "geturl", lambda: requested_url)())
            final = urlparse(final_url)
            if final.hostname != MOFCOM_HOST or final.path != MOFCOM_PATH or final.scheme not in {"http", "https"}:
                raise MofcomOpenDataError(f"unexpected MOFCOM redirect target: {final_url}")
            body = response.read(self.max_response_bytes + 1)
            if len(body) > self.max_response_bytes:
                raise MofcomOpenDataError("MOFCOM response exceeded size limit")
            try:
                text = body.decode("utf-8-sig")
            except UnicodeDecodeError:
                text = body.decode("gb18030")
            if text.lstrip().startswith("<"):
                raise MofcomOpenDataError("MOFCOM API returned HTML instead of JSON")
            try:
                payload = json.loads(text)
            except json.JSONDecodeError as exc:
                raise MofcomOpenDataError("MOFCOM API returned malformed JSON") from exc
            headers = getattr(response, "headers", None)
            content_type = str(headers.get("Content-Type", "")) if headers is not None else ""
            status = int(getattr(response, "status", None) or response.getcode())
            return FetchEnvelope(
                source_id="CN_MOFCOM_OPEN_DATA",
                request_name=request_name,
                url=final_url,
                fetched_at_utc=datetime.now(timezone.utc).isoformat(),
                http_status=status,
                content_type=content_type,
                payload_sha256=hashlib.sha256(body).hexdigest(),
                payload=payload,
            )
        finally:
            close = getattr(response, "close", None)
            if callable(close):
                close()


class MofcomOpenDataAdapter:
    def __init__(self, client: Any | None = None) -> None:
        self.client = client or MofcomOfficialHttpClient()

    def fetch_dataset(self, spec: MofcomDatasetSpec) -> dict[str, Any]:
        envelope = self.client.request_dataset(
            spec.dataset_id,
            request_name=f"mofcom.open_data.{spec.dataset_id}",
        )
        payload = envelope.payload
        if not isinstance(payload, Mapping):
            raise MofcomOpenDataError("MOFCOM API payload must be a JSON object")
        try:
            status = int(payload.get("status", 0))
        except (TypeError, ValueError) as exc:
            raise MofcomOpenDataError("MOFCOM API status is malformed") from exc
        if status != 1:
            raise MofcomOpenDataError(
                f"MOFCOM API returned status={status}: {payload.get('msg', '')}"
            )
        if "data" not in payload or payload.get("data") is None:
            raise MofcomOpenDataError("MOFCOM API success response has no data field")

        data = payload["data"]
        available = _data_available(data)
        item_count = len(data) if isinstance(data, (list, dict, str)) else 1
        final_scheme = urlparse(envelope.url).scheme
        return {
            "source_id": "CN_MOFCOM_OPEN_DATA",
            "dataset": asdict(spec),
            "api_status": status,
            "message": str(payload.get("msg") or ""),
            "data_type": type(data).__name__,
            "top_level_item_count": item_count,
            "data_available": available,
            "data": data,
            "transport_security": "HTTPS" if final_scheme == "https" else "PLAINTEXT_HTTP",
            "corroboration_required": final_scheme != "https",
            "provenance": envelope.metadata(),
            "truth_note": (
                "Transport/API success is recorded separately from data availability. "
                "Blank data remains unavailable; plain-HTTP evidence also requires corroboration."
            ),
        }

    def collect_watchlist(self, specs: list[MofcomDatasetSpec]) -> dict[str, Any]:
        responses: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []
        enabled = [spec for spec in specs if spec.enabled]
        for spec in enabled:
            try:
                responses.append(self.fetch_dataset(spec))
            except Exception as exc:
                errors.append({"dataset_id": spec.dataset_id, "name": spec.name, "error": str(exc)})
        available_count = sum(1 for item in responses if item["data_available"])
        return {
            "source_id": "CN_MOFCOM_OPEN_DATA",
            "enabled_dataset_count": len(enabled),
            "response_count": len(responses),
            "available_count": available_count,
            "unavailable_count": len(responses) - available_count,
            "error_count": len(errors),
            "datasets": responses,
            "errors": errors,
        }
