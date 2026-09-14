#!/usr/bin/env python3
"""Bind lane/seed web research captures to exact governed query IDs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.research_execution_capture import (  # noqa: E402
    bind_captures_to_plan,
    capture_from_dict,
)


def _load_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _load_captures(path: Path) -> list[dict]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, dict):
        value = value.get("captures", [])
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError("capture input must be a JSON array or object with captures[]")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--captures", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    plan = _load_object(args.plan)
    captures = tuple(capture_from_dict(item) for item in _load_captures(args.captures))
    payload = bind_captures_to_plan(plan, captures)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "mission_id": payload["mission_id"],
        "evidence_count": payload["evidence_count"],
        "capture_schema_version": payload["capture_schema_version"],
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
