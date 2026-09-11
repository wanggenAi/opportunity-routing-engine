#!/usr/bin/env python3
"""Collect the newest official PBC financial-statistics report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.network_ingest import write_json_atomic
from src.pbc_money_flow import PbcMoneyFlowAdapter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    payload = PbcMoneyFlowAdapter().collect_latest()
    write_json_atomic(args.output, payload)
    latest = payload["latest_release"]
    print(f"wrote {args.output}")
    print(
        "title=", latest["title"],
        "release_date=", latest["release_date"],
        "metric_count=", latest["metric_count"],
        "freshness=", payload["freshness"]["status"],
        "age_days=", payload["freshness"]["age_days"],
    )
    print(
        json.dumps(
            {key: value for key, value in latest["metrics"].items() if key in {
                "social_financing_stock",
                "social_financing_flow_ytd",
                "m2_balance",
                "m1_balance",
                "m0_balance",
            }},
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
