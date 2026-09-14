#!/usr/bin/env python3
"""Build sustainability-gap assessments from production ObservedPattern evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pattern_sustainability import summarize_pattern_sustainability


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def build(*, patterns_path: Path, output_path: Path, source_pattern_run_id: int | None) -> dict:
    result = summarize_pattern_sustainability(
        _load(patterns_path),
        source_pattern_run_id=source_pattern_run_id,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patterns", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-pattern-run-id", type=int)
    args = parser.parse_args()
    result = build(
        patterns_path=args.patterns,
        output_path=args.output,
        source_pattern_run_id=args.source_pattern_run_id,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
