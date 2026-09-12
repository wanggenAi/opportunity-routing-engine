#!/usr/bin/env python3
"""Collect explicit first-party blockers from Xuzhou procurement notices."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.network_ingest import NetworkIngestError, write_json_atomic
from src.xuzhou_procurement_blockers import XuzhouProcurementBlockerAdapter


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--procurement-json", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.procurement_json).read_text(encoding="utf-8"))
        result = XuzhouProcurementBlockerAdapter().collect(payload)
        write_json_atomic(args.output, result)
        print(f"wrote {args.output}")
        print(json.dumps({
            "queried_event_count": result["queried_event_count"],
            "blocker_count": result["blocker_count"],
            "rejected_count": len(result["rejected"]),
        }, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, NetworkIngestError, ValueError) as exc:
        print(f"procurement blocker collection failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
