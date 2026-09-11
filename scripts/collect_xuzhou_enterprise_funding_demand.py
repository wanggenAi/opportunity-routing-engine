#!/usr/bin/env python3
"""Collect scoped direct Xuzhou enterprise financing-demand evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.network_ingest import write_json_atomic
from src.xuzhou_enterprise_funding_demand import XuzhouEnterpriseFundingDemandAdapter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--lookback-days", type=int, default=400)
    parser.add_argument("--max-pages", type=int, default=45)
    args = parser.parse_args()

    payload = XuzhouEnterpriseFundingDemandAdapter(
        lookback_days=args.lookback_days,
        max_pages=args.max_pages,
    ).collect()
    write_json_atomic(args.output, payload)
    print(f"wrote {args.output}")
    print(
        "pages_fetched=", payload["discovery"]["pages_fetched"],
        "records_in_window=", payload["discovery"]["records_in_window"],
        "xuzhou_candidates=", payload["discovery"]["xuzhou_title_candidates"],
        "events=", payload["event_count"],
        "errors=", payload["error_count"],
        "latest_freshness=", payload["latest_freshness"],
    )
    for event in payload["events"]:
        print(json.dumps(event, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
