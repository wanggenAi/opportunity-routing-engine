#!/usr/bin/env python3
"""Collect Xuzhou procurement award/result evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.live_imbalance_ledger import classify_procurement_event
from src.network_ingest import NetworkIngestError, write_json_atomic
from src.xuzhou_procurement_results import XuzhouProcurementResultAdapter


def _canonical_capability_item(item: dict) -> bool:
    return classify_procurement_event(item).capability_key is not None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect Xuzhou procurement result notices as historical capability proof"
    )
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument(
        "--pages",
        type=int,
        default=1,
        help="Number of numbered result-list pages to scan; page 1 is list.html",
    )
    parser.add_argument(
        "--capability-only",
        action="store_true",
        help="Filter list-page titles through the canonical exact capability taxonomy before fetching details",
    )
    parser.add_argument(
        "--max-details",
        type=int,
        default=40,
        help="Maximum matching result detail pages to fetch in history mode",
    )
    parser.add_argument("--require-awards", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    try:
        adapter = XuzhouProcurementResultAdapter()
        if args.pages > 1 or args.capability_only:
            payload = adapter.collect_history_awards(
                pages=args.pages,
                item_filter=_canonical_capability_item if args.capability_only else None,
                max_items=max(args.max_details, 1),
                max_details=args.max_details,
            )
        else:
            payload = adapter.collect_recent_awards(limit=args.limit)
        if args.output:
            write_json_atomic(args.output, payload)
            print(f"wrote {args.output}")
        else:
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        if args.require_awards and payload["award_count"] == 0:
            print("no procurement award supplier evidence extracted", file=sys.stderr)
            return 3
        return 0
    except (NetworkIngestError, ValueError) as exc:
        print(f"procurement result collection failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
