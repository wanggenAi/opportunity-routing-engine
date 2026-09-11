#!/usr/bin/env python3
"""Collect enabled free official MOFCOM API datasets."""

from __future__ import annotations

import argparse
import json
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
    parser.add_argument("--require-success", action="store_true")
    args = parser.parse_args()

    specs = load_mofcom_watchlist(args.watchlist)
    payload = MofcomOpenDataAdapter().collect_watchlist(specs)
    write_json_atomic(args.output, payload)
    print(f"wrote {args.output}")
    print(
        "enabled=", payload["enabled_dataset_count"],
        "success=", payload["success_count"],
        "errors=", payload["error_count"],
    )
    if args.require_success and payload["success_count"] < 1:
        raise SystemExit("no MOFCOM API dataset collected successfully")


if __name__ == "__main__":
    main()
