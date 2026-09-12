#!/usr/bin/env python3
"""Build delegatable real-world validation packets from canonical queue tasks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.field_validation_packets import build_field_validation_packets


def _read(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build delegatable field validation packets")
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--queue", required=True)
    parser.add_argument("--provider-json", action="append", default=[])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    packets = build_field_validation_packets(
        _read(args.ledger),
        _read(args.queue),
        provider_payloads=[_read(path) for path in args.provider_json],
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(packets, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output}")
    print(json.dumps({
        "packet_count": packets["packet_count"],
        "skipped_count": packets["skipped_count"],
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
