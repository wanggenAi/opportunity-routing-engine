#!/usr/bin/env python3
"""Collect the newest official PBC Jiangsu monthly credit/deposit table."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.network_ingest import write_json_atomic
from src.pbc_jiangsu_credit import PbcJiangsuCreditAdapter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    payload = PbcJiangsuCreditAdapter().collect()
    write_json_atomic(args.output, payload)
    observation = payload["observation"]
    print(f"wrote {args.output}")
    print(
        "title=", payload["table_title"],
        "period=", payload["observation_period"],
        "release_date=", payload["release_date"],
        "freshness=", payload["freshness"]["status"],
        "sheet=", observation["sheet_name"],
        "period_gate=", observation["period_gate"],
    )
    print("metrics=", json.dumps(observation["metrics"], ensure_ascii=False, sort_keys=True))
    print("header_context=", json.dumps(observation["header_context"], ensure_ascii=False))


if __name__ == "__main__":
    main()
