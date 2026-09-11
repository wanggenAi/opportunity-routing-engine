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

from src.html_ingest import PublicHtmlClient
from src.network_ingest import NetworkIngestError, write_json_atomic
from src.regional_adapters import JiangsuStatsReleaseAdapter, XuzhouProcurementAdapter


def emit(payload, output):
    if output:
        write_json_atomic(output, payload)
        print(f"wrote {output}")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def _lexical_marker_context(html: str, marker: str) -> dict:
    index = html.find(marker)
    if index < 0:
        return {"marker": marker, "index": -1}
    lower = html.lower()
    boundaries = {
        "script_open": lower.rfind("<script", 0, index),
        "script_close": lower.rfind("</script", 0, index),
        "style_open": lower.rfind("<style", 0, index),
        "style_close": lower.rfind("</style", 0, index),
        "comment_open": html.rfind("<!--", 0, index),
        "comment_close": html.rfind("-->", 0, index),
        "tag_open": html.rfind("<", 0, index),
        "tag_close": html.rfind(">", 0, index),
    }
    next_lt = html.find("<", index)
    return {
        "marker": marker,
        "index": index,
        "boundaries": boundaries,
        "inside_script_lexically": boundaries["script_open"] > boundaries["script_close"],
        "inside_style_lexically": boundaries["style_open"] > boundaries["style_close"],
        "inside_comment_lexically": boundaries["comment_open"] > boundaries["comment_close"],
        "preceding_fragment": " ".join(html[max(0, index - 350):index].split()),
        "following_fragment": " ".join(html[index:min(len(html), index + 500)].split()),
        "next_tag_fragment": (
            " ".join(html[next_lt:min(len(html), next_lt + 250)].split())
            if next_lt >= 0 else None
        ),
    }


def _marker_context_probe(url: str) -> dict:
    envelope = PublicHtmlClient(
        source_id="XZ_GGZY_DIAGNOSTIC",
        allowed_hosts={"ggzy.zwb.xz.gov.cn"},
        timeout_seconds=30,
        retries=1,
    ).fetch(url, request_name="xz_ggzy.marker_context_probe")
    html = envelope.html
    lower = html.lower()
    return {
        "payload_sha256": envelope.payload_sha256,
        "html_chars": len(html),
        "comment_open_count": html.count("<!--"),
        "comment_close_count": html.count("-->"),
        "script_open_count": lower.count("<script"),
        "script_close_count": lower.count("</script"),
        "style_open_count": lower.count("<style"),
        "style_close_count": lower.count("</style"),
        "template_open_count": lower.count("<template"),
        "marker_contexts": [
            _lexical_marker_context(html, marker)
            for marker in ("项目编号", "JSZC-320300-XZTY-G2026-0004", "预算金额")
        ],
    }


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
            target = next(
                (
                    item for item in payload.get("discovery", {}).get("items", [])
                    if "市直管雨" in str(item.get("title") or "")
                ),
                None,
            )
            if target:
                payload["temporary_marker_context_probe"] = _marker_context_probe(target["url"])
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
