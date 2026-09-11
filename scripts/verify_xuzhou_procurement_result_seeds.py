#!/usr/bin/env python3
"""Verify research navigation seeds against official Xuzhou result details."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.network_ingest import NetworkIngestError, write_json_atomic
from src.provider_evidence_seeds import (
    load_procurement_result_seeds,
    verify_procurement_result_seeds,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Treat research-discovered official result URLs as navigation seeds only, "
            "then re-fetch and reclassify the first-party details before emitting awards"
        )
    )
    parser.add_argument("--seeds", required=True)
    parser.add_argument("--require-verified", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    try:
        seeds = load_procurement_result_seeds(args.seeds)
        payload = verify_procurement_result_seeds(seeds)
        if args.output:
            write_json_atomic(args.output, payload)
            print(f"wrote {args.output}")
        else:
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        if args.require_verified and payload["verified_seed_count"] == 0:
            print("no navigation seed was verified by official detail evidence", file=sys.stderr)
            return 3
        return 0
    except (NetworkIngestError, ValueError) as exc:
        print(f"seed verification failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
