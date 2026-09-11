#!/usr/bin/env python3
"""Collect the newest official PBC regional AFRE table for one region."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.network_ingest import write_json_atomic
from src.pbc_regional_financing import PbcRegionalFinancingAdapter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", default="江苏")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    payload = PbcRegionalFinancingAdapter().collect_region(region=args.region)
    write_json_atomic(args.output, payload)
    observation = payload["region_observation"]
    print(f"wrote {args.output}")
    print(
        "title=", payload["table_title"],
        "release_date=", payload["release_date"],
        "region=", observation["region"],
        "flow_100m_cny=", observation["social_financing_flow_100m_cny"],
        "flow_trillion_cny=", observation["social_financing_flow_trillion_cny"],
        "workbook_rows=", payload["workbook_row_count"],
    )
    print("row_values=", json.dumps(observation["row_values"], ensure_ascii=False))
    print("header_context=", json.dumps(observation["header_context"], ensure_ascii=False))


if __name__ == "__main__":
    main()
