"""Config-driven macro watchlist collection.

The watchlist separates three notions that must never be conflated:
- configured indicator identity;
- latest period advertised by source metadata;
- latest period with a materially populated value.

This protects the Money Flow Engine from treating staged/future metadata as data.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from src.nbs_adapter import NBSAdapter, PAGE_SPECS


@dataclass(frozen=True)
class MacroWatchItem:
    signal_id: str
    source_id: str
    page: str
    cid: str
    indicator_id: str
    expected_label: str
    frequency: str
    unit: str
    geography: str
    metric_kind: str
    lookback_periods: int
    status: str

    def __post_init__(self) -> None:
        if self.source_id != "CN_NBS":
            raise ValueError(f"unsupported watchlist source: {self.source_id}")
        if self.page not in PAGE_SPECS:
            raise ValueError(f"unknown NBS page: {self.page}")
        if self.frequency != PAGE_SPECS[self.page].frequency:
            raise ValueError(
                f"frequency mismatch for {self.signal_id}: {self.frequency} != {PAGE_SPECS[self.page].frequency}"
            )
        if self.lookback_periods <= 0:
            raise ValueError("lookback_periods must be positive")


WATCHLIST_FIELDS = [
    "signal_id",
    "source_id",
    "page",
    "cid",
    "indicator_id",
    "expected_label",
    "frequency",
    "unit",
    "geography",
    "metric_kind",
    "lookback_periods",
    "status",
]


def load_macro_watchlist(path: str | Path) -> list[MacroWatchItem]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != WATCHLIST_FIELDS:
            raise ValueError(
                f"macro watchlist columns mismatch; expected={WATCHLIST_FIELDS}, actual={reader.fieldnames}"
            )
        result: list[MacroWatchItem] = []
        seen: set[str] = set()
        for row in reader:
            signal_id = row["signal_id"].strip()
            if not signal_id:
                raise ValueError("signal_id must not be empty")
            if signal_id in seen:
                raise ValueError(f"duplicate signal_id: {signal_id}")
            seen.add(signal_id)
            result.append(
                MacroWatchItem(
                    signal_id=signal_id,
                    source_id=row["source_id"].strip(),
                    page=row["page"].strip(),
                    cid=row["cid"].strip(),
                    indicator_id=row["indicator_id"].strip(),
                    expected_label=row["expected_label"].strip(),
                    frequency=row["frequency"].strip(),
                    unit=row["unit"].strip(),
                    geography=row["geography"].strip(),
                    metric_kind=row["metric_kind"].strip(),
                    lookback_periods=int(row["lookback_periods"]),
                    status=row["status"].strip(),
                )
            )
        return result


def advertised_period(dates_payload: dict[str, Any]) -> str | None:
    data = dates_payload.get("data", {}) if isinstance(dates_payload, dict) else {}
    if not isinstance(data, dict):
        return None
    value = data.get("dt_all")
    return str(value).strip() if value else None


def period_lookback(latest: str, frequency: str, count: int) -> list[str]:
    """Return newest-to-oldest normalized period codes including latest."""

    if count <= 0:
        raise ValueError("count must be positive")
    latest = latest.strip().upper()

    if frequency == "month":
        if not latest.endswith("MM") or len(latest) != 8:
            raise ValueError(f"invalid monthly period: {latest}")
        year = int(latest[:4])
        month = int(latest[4:6])
        result = []
        for _ in range(count):
            result.append(f"{year:04d}{month:02d}MM")
            month -= 1
            if month == 0:
                year -= 1
                month = 12
        return result

    if frequency == "quarter":
        if not latest.endswith("SS") or len(latest) != 8:
            raise ValueError(f"invalid quarterly period: {latest}")
        year = int(latest[:4])
        quarter = int(latest[5])
        if quarter not in {1, 2, 3, 4}:
            raise ValueError(f"invalid quarter number: {latest}")
        result = []
        for _ in range(count):
            result.append(f"{year:04d}0{quarter}SS")
            quarter -= 1
            if quarter == 0:
                year -= 1
                quarter = 4
        return result

    if frequency == "year":
        if not latest.endswith("YY") or len(latest) != 6:
            raise ValueError(f"invalid annual period: {latest}")
        year = int(latest[:4])
        return [f"{year - offset:04d}YY" for offset in range(count)]

    raise ValueError(f"unsupported frequency: {frequency}")


def _normalized_text(value: str) -> str:
    return " ".join(value.split()).strip()


def collect_nbs_watchlist(
    adapter: NBSAdapter,
    items: Iterable[MacroWatchItem],
) -> dict[str, Any]:
    """Collect latest materially populated values for active NBS watch items."""

    active = [item for item in items if item.status == "ACTIVE"]
    groups: dict[tuple[str, str], list[MacroWatchItem]] = defaultdict(list)
    for item in active:
        groups[(item.page, item.cid)].append(item)

    signals: list[dict[str, Any]] = []
    group_evidence: list[dict[str, Any]] = []

    for (page, cid), group in sorted(groups.items()):
        dates_payload = adapter.dates(page, cid=cid)
        latest_advertised = advertised_period(dates_payload)
        if latest_advertised is None:
            for item in group:
                signals.append(
                    {
                        "signal_id": item.signal_id,
                        "status": "NO_ADVERTISED_PERIOD",
                        "latest_advertised_period": None,
                        "latest_populated_period": None,
                        "value": None,
                    }
                )
            continue

        max_lookback = max(item.lookback_periods for item in group)
        candidates = period_lookback(
            latest_advertised,
            PAGE_SPECS[page].frequency,
            max_lookback,
        )
        fetched = adapter.fetch_values(
            page,
            cid=cid,
            indicator_ids=[item.indicator_id for item in group],
            periods=candidates,
        )
        group_evidence.append(
            {
                "page": page,
                "cid": cid,
                "latest_advertised_period": latest_advertised,
                "candidate_periods": candidates,
                "request": fetched["request"],
                "observed_row_count": fetched["observed_row_count"],
                "populated_row_count": fetched["populated_row_count"],
                "populated_periods": fetched["populated_periods"],
            }
        )

        by_indicator_period = {
            (record["indicator_id"], record["period_code"]): record
            for record in fetched["records"]
        }
        indicator_metadata = {
            indicator["indicator_id"]: indicator
            for indicator in adapter.indicators(page, cid=cid)
        }

        for item in group:
            metadata = indicator_metadata.get(item.indicator_id)
            identity_status = "MATCH"
            actual_label = None
            actual_unit = None
            if metadata is None:
                identity_status = "INDICATOR_NOT_FOUND"
            else:
                actual_label = metadata["label"]
                actual_unit = metadata["unit"]
                if _normalized_text(actual_label) != _normalized_text(item.expected_label):
                    identity_status = "LABEL_DRIFT"
                if item.unit and actual_unit and actual_unit != item.unit:
                    identity_status = "UNIT_DRIFT"

            item_candidates = candidates[: item.lookback_periods]
            selected = next(
                (
                    by_indicator_period.get((item.indicator_id, period))
                    for period in item_candidates
                    if by_indicator_period.get((item.indicator_id, period), {}).get(
                        "value_present"
                    )
                ),
                None,
            )
            availability = "AVAILABLE" if selected else "STAGED_OR_UNAVAILABLE"
            if identity_status != "MATCH":
                availability = identity_status

            signals.append(
                {
                    "signal_id": item.signal_id,
                    "source_id": item.source_id,
                    "geography": item.geography,
                    "metric_kind": item.metric_kind,
                    "frequency": item.frequency,
                    "configured_label": item.expected_label,
                    "actual_label": actual_label,
                    "configured_unit": item.unit,
                    "actual_unit": actual_unit,
                    "identity_status": identity_status,
                    "status": availability,
                    "latest_advertised_period": latest_advertised,
                    "latest_populated_period": selected["period_code"] if selected else None,
                    "period_lag": (
                        item_candidates.index(selected["period_code"])
                        if selected and selected["period_code"] in item_candidates
                        else None
                    ),
                    "value": selected["value"] if selected else None,
                    "selected_record": selected,
                    "request_sha256": fetched["request"]["payload_sha256"],
                    "fetched_at_utc": fetched["request"]["fetched_at_utc"],
                }
            )

    return {
        "source_id": "CN_NBS",
        "active_signal_count": len(active),
        "available_signal_count": sum(1 for item in signals if item["status"] == "AVAILABLE"),
        "unavailable_signal_count": sum(1 for item in signals if item["status"] != "AVAILABLE"),
        "signals": signals,
        "groups": group_evidence,
    }
