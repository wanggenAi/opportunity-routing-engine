#!/usr/bin/env python3
"""Collect one live China → Jiangsu → Xuzhou money-flow evidence snapshot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.money_flow_snapshot import collect_money_flow_snapshot
from src.network_ingest import write_json_atomic


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    snapshot = collect_money_flow_snapshot()
    write_json_atomic(args.output, snapshot)
    print(f"wrote {args.output}")
    print("schema_version=", snapshot["schema_version"])
    print("status_counts=", json.dumps(snapshot["status_counts"], sort_keys=True))
    print("answerability=", json.dumps(snapshot["answerability"], ensure_ascii=False, sort_keys=True))

    for key, feed in snapshot["feeds"].items():
        print(
            "feed=",
            json.dumps(
                {
                    "key": key,
                    "geography": feed["geography"],
                    "role": feed["evidence_role"],
                    "status": feed["status"],
                    "error_type": feed["error_type"],
                    "error": feed["error"],
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
        )


if __name__ == "__main__":
    main()
