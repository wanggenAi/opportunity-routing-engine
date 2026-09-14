#!/usr/bin/env python3
"""Build the truth-preserving opportunity funnel control plane."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.opportunity_funnel import build_opportunity_funnel


def _read_json(path: str | None) -> dict:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Join the canonical ledger and validation plans into a truth-preserving opportunity control plane"
    )
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--validation-queue")
    parser.add_argument("--field-packets")
    parser.add_argument("--focus-limit", type=int, default=5)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    funnel = build_opportunity_funnel(
        _read_json(args.ledger),
        _read_json(args.validation_queue),
        _read_json(args.field_packets),
        focus_limit=args.focus_limit,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(funnel, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output}")
    print(
        json.dumps(
            {
                "record_count": funnel["record_count"],
                "status_counts": funnel["status_counts"],
                "route_testable_count": funnel["route_testable_count"],
                "validation_focus_count": funnel["validation_focus_count"],
                "batch_next_action": funnel["batch_next_action"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
