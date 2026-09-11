#!/usr/bin/env python3
"""Collect bounded public evidence of underused resources."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.resource_underuse_adapters import XuzhouPublicAssetAdapter
from src.xuzhou_agency_resource_feed import XuzhouAgencyAssetFeed


def _write(path: str, payload: dict) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output}")


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--require-listings",
        action="store_true",
        help="fail if no listing detail can be parsed",
    )


def _summary(payload: dict) -> None:
    print(
        "listings=",
        payload["listing_count"],
        "explicit_underuse=",
        payload["observed_underuse_count"],
        "relistings=",
        payload["relisting_count"],
        "errors=",
        payload["error_count"],
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    recent = sub.add_parser(
        "xuzhou-public-assets",
        help="collect recent Xuzhou property-rights listings",
    )
    _add_common(recent)

    agency = sub.add_parser(
        "xuzhou-agency-assets",
        help="discover Xuzhou agency listings and fetch official Jiangsu mirror details",
    )
    _add_common(agency)

    args = parser.parse_args()

    if args.command == "xuzhou-public-assets":
        payload = XuzhouPublicAssetAdapter().collect_recent(limit=args.limit)
        if args.require_listings and payload["listing_count"] < 1:
            raise SystemExit("no Xuzhou public-asset listing parsed")
        _write(args.output, payload)
        _summary(payload)
        return

    if args.command == "xuzhou-agency-assets":
        payload = XuzhouAgencyAssetFeed().collect_recent(limit=args.limit)
        if args.require_listings and payload["listing_count"] < 1:
            raise SystemExit("no Xuzhou agency asset mirror listing parsed")
        _write(args.output, payload)
        _summary(payload)
        print("skipped=", payload["skipped_count"])
        return

    raise AssertionError(args.command)


if __name__ == "__main__":
    main()
