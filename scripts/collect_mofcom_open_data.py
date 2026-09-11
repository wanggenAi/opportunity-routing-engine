#!/usr/bin/env python3
"""Collect enabled free official MOFCOM API datasets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.mofcom_open_data import MofcomOpenDataAdapter, load_mofcom_watchlist
from src.network_ingest import write_json_atomic


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--watchlist", default="data/mofcom_api_watchlist.csv")
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--require-available-data",
        action="store_true",
        help="fail when official API responses contain no non-blank dataset payload",
    )
    args = parser.parse_args()

    specs = load_mofcom_watchlist(args.watchlist)
    payload = MofcomOpenDataAdapter().collect_watchlist(specs)
    write_json_atomic(args.output, payload)
    print(f"wrote {args.output}")
    print(
        "enabled=", payload["enabled_dataset_count"],
        "responses=", payload["response_count"],
        "available=", payload["available_count"],
        "unavailable=", payload["unavailable_count"],
        "errors=", payload["error_count"],
    )
    for item in payload["datasets"]:
        print(
            "DATASET",
            item["dataset"]["dataset_id"],
            item["dataset"]["name"],
            "available=", item["data_available"],
            "type=", item["data_type"],
            "items=", item["top_level_item_count"],
            "transport=", item["transport_security"],
        )
    for error in payload["errors"]:
        print(
            "ERROR",
            error.get("dataset_id", ""),
            error.get("name", ""),
            error.get("error", ""),
        )
    if args.require_available_data and payload["available_count"] < 1:
        raise SystemExit("no MOFCOM API dataset returned non-blank data")


if __name__ == "__main__":
    main()
