#!/usr/bin/env python3
"""Live regional collection for Jiangsu macro releases and Xuzhou procurement."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict
from pathlib import Path
from urllib.request import Request, urlopen

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


def _safe_response_shape_probe(url: str) -> dict:
    """Temporary live diagnostic: compare response shape without retaining page content."""
    profiles = {
        "engine": {
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5",
            "User-Agent": "OpportunityRoutingEngine/0.1 (+public-evidence-ingest)",
        },
        "browser": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        },
    }
    result = {}
    markers = ("项目编号", "项目名称", "预算金额", "采购人信息")
    for profile, headers in profiles.items():
        request = Request(url, headers=headers, method="GET")
        with urlopen(request, timeout=30) as response:
            body = response.read(5_000_000)
            content_type = str(response.headers.get("Content-Type", ""))
        try:
            html = body.decode("utf-8")
            encoding = "utf-8"
        except UnicodeDecodeError:
            html = body.decode("gb18030")
            encoding = "gb18030"
        result[profile] = {
            "bytes": len(body),
            "content_type": content_type,
            "encoding": encoding,
            "sha256_prefix": hashlib.sha256(body).hexdigest()[:16],
            "contains": {marker: marker in html for marker in markers},
            "jszc_count": len(re.findall(r"JSZC-[0-9A-Z-]+", html)),
            "iframe_count": len(re.findall(r"<iframe\\b", html, flags=re.I)),
            "script_count": len(re.findall(r"<script\\b", html, flags=re.I)),
            "escaped_project_label": "\\u9879\\u76ee\\u7f16\\u53f7" in html.lower(),
            "iframe_srcs": re.findall(
                r"<iframe\\b[^>]*?src=[\"']([^\"']+)", html, flags=re.I
            )[:5],
        }
    return result


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
            probe_item = next(
                (
                    item
                    for item in payload.get("discovery", {}).get("items", [])
                    if "市直管雨" in str(item.get("title") or "")
                ),
                None,
            )
            if probe_item:
                payload["temporary_response_shape_probe"] = _safe_response_shape_probe(
                    probe_item["url"]
                )
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
