"""Free official MOFCOM open-data API adapter.

The Ministry of Commerce public-service open-data platform publishes dataset detail
pages that explicitly expose JSON API request paths.  This adapter keeps the first
integration deliberately generic: transport/provenance are normalized, but dataset
business semantics remain in the watchlist and are not guessed from arbitrary JSON.

Truth rules:
- HTTP/API success != current/fresh data;
- API status=0 is an error, never zero-valued evidence;
- missing data remains unavailable;
- raw payload is preserved for later schema-specific normalization;
- only the official open-data host is allowlisted.
"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from src.network_ingest import JsonHttpClient


MOFCOM_HOST = "opendata.mofcom.gov.cn"
MOFCOM_JSON_ENDPOINT = "https://opendata.mofcom.gov.cn/front/data/jsonData"


class MofcomOpenDataError(RuntimeError):
    pass


@dataclass(frozen=True)
class MofcomDatasetSpec:
    dataset_id: str
    name: str
    theme: str
    refresh_cadence: str
    enabled: bool



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


class MofcomOpenDataAdapter:
    def __init__(self, client: JsonHttpClient | None = None) -> None:
        self.client = client or JsonHttpClient(
            source_id="CN_MOFCOM_OPEN_DATA",
            allowed_hosts={MOFCOM_HOST},
            timeout_seconds=30,
            retries=2,
        )

    def fetch_dataset(self, spec: MofcomDatasetSpec) -> dict[str, Any]:
        envelope = self.client.request_json(
            "GET",
            MOFCOM_JSON_ENDPOINT,
            request_name=f"mofcom.open_data.{spec.dataset_id}",
            params={"id": spec.dataset_id},
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
            raise MofcomOpenDataError("MOFCOM API success response has no data")

        data = payload["data"]
        if isinstance(data, (list, dict)):
            item_count = len(data)
        else:
            item_count = 1
        return {
            "source_id": "CN_MOFCOM_OPEN_DATA",
            "dataset": asdict(spec),
            "api_status": status,
            "message": str(payload.get("msg") or ""),
            "data_type": type(data).__name__,
            "top_level_item_count": item_count,
            "data": data,
            "provenance": envelope.metadata(),
            "truth_note": (
                "API transport success proves only that the official endpoint returned data; "
                "freshness and dataset-specific semantics require separate validation."
            ),
        }

    def collect_watchlist(self, specs: list[MofcomDatasetSpec]) -> dict[str, Any]:
        results: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []
        enabled = [spec for spec in specs if spec.enabled]
        for spec in enabled:
            try:
                results.append(self.fetch_dataset(spec))
            except Exception as exc:
                errors.append(
                    {"dataset_id": spec.dataset_id, "name": spec.name, "error": str(exc)}
                )
        return {
            "source_id": "CN_MOFCOM_OPEN_DATA",
            "enabled_dataset_count": len(enabled),
            "success_count": len(results),
            "error_count": len(errors),
            "datasets": results,
            "errors": errors,
        }
