#!/usr/bin/env python3
"""Collect the configured macro watchlist from live public sources."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.macro_watchlist import collect_nbs_watchlist, load_macro_watchlist
from src.nbs_adapter import NBSAdapter
from src.network_ingest import NetworkIngestError, write_json_atomic


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect configured macro watchlist")
    parser.add_argument(
        "--watchlist",
        default="data/nbs_macro_watchlist.csv",
        help="watchlist CSV",
    )
    parser.add_argument("--output", default=None)
    parser.add_argument(
        "--require-any-available",
        action="store_true",
        help="exit non-zero if no configured signal has a populated value",
    )
    args = parser.parse_args()

    try:
        items = load_macro_watchlist(args.watchlist)
        payload = collect_nbs_watchlist(NBSAdapter(), items)
    except (NetworkIngestError, ValueError) as exc:
        print(f"watchlist collection failed: {exc}", file=sys.stderr)
        return 2

    if args.output:
        write_json_atomic(args.output, payload)
        print(f"wrote {args.output}")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))

    if args.require_any_available and payload["available_signal_count"] == 0:
        print("no populated watchlist values available", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
