#!/usr/bin/env python3
"""Live regional collection for Jiangsu macro releases and Xuzhou procurement."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.network_ingest import NetworkIngestError, write_json_atomic
from src.regional_adapters import JiangsuStatsReleaseAdapter, XuzhouProcurementAdapter


def emit(payload, output):
    if output:
        write_json_atomic(output, payload)
        print(f"wrote {output}")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser():
    parser = argparse.ArgumentParser(description="Collect regional public discovery evidence")
    sub = parser.add_subparsers(dest="command", required=True)

    js = sub.add_parser("jiangsu-release")
    js.add_argument("--url", required=True)
    js.add_argument("--output")

    xz_list = sub.add_parser("xuzhou-procurement-list")
    xz_list.add_argument("--limit", type=int, default=30)
    xz_list.add_argument("--output")

    xz_events = sub.add_parser("xuzhou-procurement-events")
    xz_events.add_argument("--limit", type=int, default=10)
    xz_events.add_argument("--require-events", action="store_true")
    xz_events.add_argument("--output")

    xz_detail = sub.add_parser("xuzhou-procurement-detail")
    xz_detail.add_argument("--url", required=True)
    xz_detail.add_argument("--output")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "jiangsu-release":
            adapter = JiangsuStatsReleaseAdapter()
            doc = adapter.fetch_release(args.url)
            payload = {
                "document": asdict(doc),
                "money_flow_metrics": adapter.extract_money_flow_metrics(doc),
            }
        elif args.command == "xuzhou-procurement-list":
            payload = XuzhouProcurementAdapter().discover_recent(limit=args.limit)
        elif args.command == "xuzhou-procurement-events":
            payload = XuzhouProcurementAdapter().collect_recent_events(limit=args.limit)
            if args.require_events and payload["event_count"] == 0:
                emit(payload, args.output)
                print("no procurement events extracted", file=sys.stderr)
                return 3
        else:
            payload = asdict(XuzhouProcurementAdapter().fetch_event(args.url))
        emit(payload, args.output)
        return 0
    except (NetworkIngestError, ValueError) as exc:
        print(f"regional collection failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
