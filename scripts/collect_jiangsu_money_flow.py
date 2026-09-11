#!/usr/bin/env python3
"""Collect the newest official Jiangsu economic-operation money-flow release."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.jiangsu_money_flow import JiangsuMoneyFlowAdapter
from src.network_ingest import write_json_atomic


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    payload = JiangsuMoneyFlowAdapter().collect()
    write_json_atomic(args.output, payload)
    print(f"wrote {args.output}")
    print(
        "title=", payload["release_title"],
        "publication_date=", payload["publication_date"],
        "observation_period=", payload["observation_period"],
        "freshness=", payload["freshness"]["status"],
        "metric_count=", payload["metric_count"],
    )
    print("metrics=", json.dumps(payload["metrics"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
