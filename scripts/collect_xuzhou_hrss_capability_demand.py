#!/usr/bin/env python3
"""Collect latest structured Xuzhou HRSS public recruitment capability demand."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.network_ingest import write_json_atomic
from src.xuzhou_hrss_capability_demand import XuzhouHrssCapabilityDemandAdapter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--scan-limit", type=int, default=15)
    args = parser.parse_args()

    payload = XuzhouHrssCapabilityDemandAdapter().collect_latest_structured(
        scan_limit=args.scan_limit
    )
    write_json_atomic(args.output, payload)
    obs = payload["observation"]
    print(f"wrote {args.output}")
    print(
        "article=", payload["article_title"],
        "publication_date=", payload["publication_date"],
        "freshness=", payload["freshness"]["status"],
        "sheet=", obs["sheet_name"],
        "demand_units=", obs["demand_unit_count"],
        "explicit_headcount=", obs["total_requested_headcount"],
    )
    print(
        "sample=",
        json.dumps(obs["demand_units"][:5], ensure_ascii=False, sort_keys=True),
    )
    print(
        "inspected_articles=",
        json.dumps(payload["inspected_articles"], ensure_ascii=False, sort_keys=True),
    )


if __name__ == "__main__":
    main()
