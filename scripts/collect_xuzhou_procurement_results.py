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

from src.network_ingest import NetworkIngestError, write_json_atomic
from src.xuzhou_procurement_results import XuzhouProcurementResultAdapter


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect Xuzhou procurement result notices as historical capability proof"
    )
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--require-awards", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    try:
        payload = XuzhouProcurementResultAdapter().collect_recent_awards(limit=args.limit)
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
