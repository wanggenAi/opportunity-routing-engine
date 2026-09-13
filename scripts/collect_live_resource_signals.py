#!/usr/bin/env python3
"""Collect one lawful live sensor directly into the canonical signal ledger."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.live_signal_store import SQLiteSignalLedgerStore
from src.resource_underuse_adapters import PublicAssetListing, XuzhouPublicAssetAdapter
from src.xuzhou_public_asset_live_sensor import signal_from_public_asset


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--summary-output")
    args = parser.parse_args()

    payload = XuzhouPublicAssetAdapter().collect_recent(limit=args.limit)
    counts: Counter[str] = Counter()
    conversion_errors: list[dict[str, str]] = []

    with SQLiteSignalLedgerStore(args.db) as store:
        for record in payload.get("listings", []):
            try:
                listing = PublicAssetListing(**record)
                signal = signal_from_public_asset(listing)
                transition = store.ingest(signal)
                counts[transition.kind.value] += 1
            except Exception as exc:
                conversion_errors.append(
                    {
                        "url": str(record.get("url", "")),
                        "error": str(exc),
                    }
                )
        current_count = sum(1 for _ in store.iter_current())

    summary = {
        "source_id": "XZ_GGZY_PUBLIC_ASSET",
        "collected_listing_count": payload.get("listing_count", 0),
        "source_error_count": payload.get("error_count", 0),
        "converted_transition_count": sum(counts.values()),
        "transition_counts": dict(sorted(counts.items())),
        "conversion_error_count": len(conversion_errors),
        "conversion_errors": conversion_errors,
        "current_signal_count": current_count,
        "truth_note": (
            "Official listing facts enter the neutral signal ledger as advertised resource evidence; "
            "operator permission remains UNKNOWN and no low-level capability is manufactured."
        ),
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))

    if args.summary_output:
        output = Path(args.summary_output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
