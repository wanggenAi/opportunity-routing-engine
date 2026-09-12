#!/usr/bin/env python3
"""Build an exact-project procurement lifecycle artifact."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.procurement_lifecycle import build_procurement_lifecycle


def _read_json(path: str | None) -> dict:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build exact-project tender -> result -> contract -> settlement lifecycle"
    )
    parser.add_argument("--tender-json", required=True)
    parser.add_argument(
        "--result-json",
        action="append",
        default=[],
        help="Official result/award JSON artifact; may be supplied multiple times",
    )
    parser.add_argument(
        "--contract-json",
        action="append",
        default=[],
        help="Normalized first-party contract/settlement JSON; may be supplied multiple times",
    )
    parser.add_argument("--geography", default="Xuzhou")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    lifecycle = build_procurement_lifecycle(
        _read_json(args.tender_json),
        [_read_json(path) for path in args.result_json],
        [_read_json(path) for path in args.contract_json],
        geography=args.geography,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(lifecycle, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output}")
    print(
        json.dumps(
            {
                "record_count": lifecycle["record_count"],
                "stage_counts": lifecycle["stage_counts"],
                "promotion_allowed_count": lifecycle["promotion_allowed_count"],
                "unlinked_evidence_count": len(lifecycle["unlinked_evidence"]),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
