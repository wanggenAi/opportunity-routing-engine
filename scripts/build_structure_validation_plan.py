#!/usr/bin/env python3
"""Materialize non-canonical structure validation queue and field packets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.structure_validation_planning import (  # noqa: E402
    build_structure_field_packets,
    build_structure_validation_queue,
)


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commercial-structure", type=Path, required=True)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--queue-output", type=Path, required=True)
    parser.add_argument("--packets-output", type=Path, required=True)
    args = parser.parse_args()

    artifact = _load(args.commercial_structure)
    profile = _load(args.profile) if args.profile else None
    queue = build_structure_validation_queue(artifact, profile=profile)
    packets = build_structure_field_packets(queue)

    args.queue_output.parent.mkdir(parents=True, exist_ok=True)
    args.packets_output.parent.mkdir(parents=True, exist_ok=True)
    args.queue_output.write_text(json.dumps(queue, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.packets_output.write_text(json.dumps(packets, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "candidate_id": queue["candidate_id"],
        "validation_profile_id": queue["validation_profile"]["profile_id"],
        "task_count": queue["task_count"],
        "packet_count": packets["packet_count"],
        "business_promotion": queue["business_promotion"],
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
