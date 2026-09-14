#!/usr/bin/env python3
"""Collect source-explicit failed-package evidence from Xuzhou result pages."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.network_ingest import NetworkIngestError, write_json_atomic
from src.xuzhou_procurement_failures import XuzhouProcurementFailureAdapter


def _read_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Extract explicit failed procurement packages from known result URLs and "
            "a bounded official result-index scan"
        )
    )
    parser.add_argument(
        "--result-json",
        action="append",
        default=[],
        help="Procurement award/result JSON; may be supplied multiple times",
    )
    parser.add_argument(
        "--discover-pages",
        type=int,
        default=3,
        help="Bounded number of official result-list pages to scan; 0 disables discovery",
    )
    parser.add_argument(
        "--max-discovered-items",
        type=int,
        default=60,
        help="Maximum exact-capability result-list items admitted for detail fetch",
    )
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    try:
        payloads = [_read_json(path) for path in args.result_json]
        result = XuzhouProcurementFailureAdapter().collect_from_result_payloads(
            payloads,
            discover_pages=args.discover_pages,
            max_discovered_items=args.max_discovered_items,
        )
        write_json_atomic(args.output, result)
        print(f"wrote {args.output}")
        print(
            json.dumps(
                {
                    "result_url_count": result["result_url_count"],
                    "known_result_url_count": result["known_result_url_count"],
                    "discovered_result_url_count": result["discovered_result_url_count"],
                    "failed_package_count": result["failed_package_count"],
                    "error_count": result["error_count"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except (NetworkIngestError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"procurement failure collection failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
