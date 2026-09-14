#!/usr/bin/env python3
"""Build strict program-level rebid CHANGE/FRICTION signals."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.procurement_rebid import build_procurement_rebid_signals


def _read_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Join explicit failed packages to later same-program procurement tenders"
    )
    parser.add_argument("--tender-json", required=True)
    parser.add_argument("--failure-json", required=True)
    parser.add_argument("--max-days-after-failure", type=int, default=45)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = build_procurement_rebid_signals(
        _read_json(args.tender_json),
        _read_json(args.failure_json),
        max_days_after_failure=args.max_days_after_failure,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output}")
    print(
        json.dumps(
            {
                "signal_count": result["signal_count"],
                "failed_package_evidence_count": result["failed_package_evidence_count"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
