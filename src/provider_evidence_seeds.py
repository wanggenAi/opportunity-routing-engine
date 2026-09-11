"""Verify research navigation seeds against first-party procurement result evidence.

A seed is only a pointer to an official result detail page. It is never evidence by
itself. Every seed must be re-fetched from the Xuzhou public-resource host, parsed
through the normal procurement-result adapter, and reclassified through the same
exact capability taxonomy used by live demand before any supplier can enter the
Capability Graph.

Truth boundaries:
- seed URL != evidence;
- expected capability != observed capability;
- search-engine discovery != provenance;
- only the freshly fetched official detail payload may prove a supplier capability;
- historical award still does not prove current availability, underuse, or control.
"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping
from urllib.parse import urlparse

from src.live_imbalance_ledger import classify_procurement_event
from src.xuzhou_procurement_results import (
    XZ_GGZY_HOST,
    XuzhouProcurementResultAdapter,
)


@dataclass(frozen=True)
class ProcurementResultSeed:
    seed_id: str
    url: str
    expected_capability_key: str
    discovered_via: str | None = None
    note: str | None = None


def _required(name: str, value: object) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{name} is required")
    return text


def _validate_official_result_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or (parsed.hostname or "").lower() != XZ_GGZY_HOST:
        raise ValueError("seed URL must be an HTTPS Xuzhou public-resource URL")
    if not XuzhouProcurementResultAdapter.DETAIL_RE.search(url):
        raise ValueError("seed URL must be an official Xuzhou procurement result detail URL")


def load_procurement_result_seeds(path: str | Path) -> list[ProcurementResultSeed]:
    result: list[ProcurementResultSeed] = []
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required_columns = {"seed_id", "url", "expected_capability_key"}
        if not reader.fieldnames or not required_columns.issubset(set(reader.fieldnames)):
            raise ValueError("seed CSV is missing required columns")
        for row in reader:
            if not any(str(value or "").strip() for value in row.values()):
                continue
            seed_id = _required("seed_id", row.get("seed_id"))
            url = _required("url", row.get("url"))
            capability = _required(
                "expected_capability_key", row.get("expected_capability_key")
            )
            _validate_official_result_url(url)
            if seed_id in seen_ids:
                raise ValueError(f"duplicate seed_id: {seed_id}")
            if url in seen_urls:
                raise ValueError(f"duplicate seed URL: {url}")
            seen_ids.add(seed_id)
            seen_urls.add(url)
            result.append(
                ProcurementResultSeed(
                    seed_id=seed_id,
                    url=url,
                    expected_capability_key=capability,
                    discovered_via=str(row.get("discovered_via") or "").strip() or None,
                    note=str(row.get("note") or "").strip() or None,
                )
            )
    return result


def verify_procurement_result_seeds(
    seeds: Iterable[ProcurementResultSeed],
    *,
    adapter: XuzhouProcurementResultAdapter | None = None,
) -> dict[str, Any]:
    adapter = adapter or XuzhouProcurementResultAdapter()
    seed_list = list(seeds)
    awards: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    rejections: list[dict[str, Any]] = []
    verified_seed_ids: set[str] = set()
    seen_awards: set[tuple[str, str, str]] = set()

    for seed in seed_list:
        try:
            parsed_awards = adapter.fetch_awards(seed.url)
        except Exception as exc:  # one broken navigation seed must not erase the batch
            errors.append(
                {
                    "seed_id": seed.seed_id,
                    "url": seed.url,
                    "error": str(exc),
                }
            )
            continue

        if not parsed_awards:
            rejections.append(
                {
                    "seed_id": seed.seed_id,
                    "url": seed.url,
                    "expected_capability_key": seed.expected_capability_key,
                    "reason": "OFFICIAL_DETAIL_HAS_NO_SUPPLIER_AWARD",
                }
            )
            continue

        accepted_for_seed = 0
        observed_capabilities: set[str] = set()
        for award in parsed_awards:
            payload = asdict(award)
            classification = classify_procurement_event(payload)
            if classification.capability_key:
                observed_capabilities.add(classification.capability_key)
            if classification.capability_key != seed.expected_capability_key:
                continue

            identity = (
                str(payload.get("url") or ""),
                str(payload.get("supplier_credit_code") or payload.get("supplier_name") or ""),
                str(payload.get("award_amount_rmb") or ""),
            )
            if identity in seen_awards:
                continue
            seen_awards.add(identity)
            payload["navigation_seed_id"] = seed.seed_id
            payload["navigation_seed_expected_capability_key"] = seed.expected_capability_key
            payload["navigation_seed_discovered_via"] = seed.discovered_via
            awards.append(payload)
            accepted_for_seed += 1

        if accepted_for_seed:
            verified_seed_ids.add(seed.seed_id)
        else:
            rejections.append(
                {
                    "seed_id": seed.seed_id,
                    "url": seed.url,
                    "expected_capability_key": seed.expected_capability_key,
                    "observed_capability_keys": sorted(observed_capabilities),
                    "reason": "OFFICIAL_DETAIL_CAPABILITY_MISMATCH",
                }
            )

    return {
        "source_id": "XZ_GGZY_PROCUREMENT_RESULT_SEED_VERIFICATION",
        "seed_count": len(seed_list),
        "verified_seed_count": len(verified_seed_ids),
        "award_count": len(awards),
        "rejected_seed_count": len(rejections),
        "error_count": len(errors),
        "seeds": [asdict(seed) for seed in seed_list],
        "verified_seed_ids": sorted(verified_seed_ids),
        "awards": awards,
        "rejections": rejections,
        "errors": errors,
        "truth_note": (
            "Navigation seeds are not evidence. Supplier capability is admitted only after "
            "fresh first-party detail fetch, supplier-row parsing, and exact capability "
            "reclassification. Historical awards do not prove current availability or underuse."
        ),
    }
