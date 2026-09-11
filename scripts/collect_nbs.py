#!/usr/bin/env python3
"""Live collection CLI for the NBS adapter.

Examples:
  python scripts/collect_nbs.py probe --output .local/nbs_probe.json
  python scripts/collect_nbs.py discover --page monthData --keyword 居民消费价格
  python scripts/collect_nbs.py values --page monthData --cid <cid> --indicator-id <id> --period 202608
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.nbs_adapter import NBSAdapter
from src.network_ingest import NetworkIngestError, write_json_atomic


def _emit(payload: object, output: str | None) -> None:
    if output:
        write_json_atomic(output, payload)
        print(f"wrote {output}")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect public NBS discovery data")
    sub = parser.add_subparsers(dest="command", required=True)

    probe = sub.add_parser("probe", help="verify current NBS catalog connectivity")
    probe.add_argument(
        "--page",
        action="append",
        dest="pages",
        default=None,
        help="NBS page name; repeatable",
    )
    probe.add_argument("--output")

    discover = sub.add_parser("discover", help="bounded keyword search of NBS catalog tree")
    discover.add_argument("--page", default="monthData")
    discover.add_argument("--keyword", action="append", required=True)
    discover.add_argument("--max-depth", type=int, default=8)
    discover.add_argument("--max-nodes", type=int, default=400)
    discover.add_argument("--limit-per-keyword", type=int, default=5)
    discover.add_argument("--output")

    values = sub.add_parser("values", help="fetch values using pinned catalog/indicator IDs")
    values.add_argument("--page", required=True)
    values.add_argument("--cid", required=True)
    values.add_argument("--indicator-id", action="append", required=True)
    values.add_argument("--period", action="append", default=None)
    values.add_argument("--output")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    adapter = NBSAdapter()
    try:
        if args.command == "probe":
            pages = args.pages or ["monthData", "quarterData", "yearData", "fsMonthData"]
            payload = adapter.probe(pages)
        elif args.command == "discover":
            payload = {
                "source_id": "CN_NBS",
                "page": args.page,
                "keywords": args.keyword,
                "matches": adapter.discover_catalogs(
                    args.page,
                    keywords=args.keyword,
                    max_depth=args.max_depth,
                    max_nodes=args.max_nodes,
                    limit_per_keyword=args.limit_per_keyword,
                ),
            }
        else:
            payload = adapter.fetch_values(
                args.page,
                cid=args.cid,
                indicator_ids=args.indicator_id,
                periods=args.period,
            )
        _emit(payload, args.output)
        return 0
    except (NetworkIngestError, ValueError) as exc:
        print(f"collection failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
