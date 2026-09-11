#!/usr/bin/env python3
"""Build evidence-acquisition tasks from PAIR_HYPOTHESIS records."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.validation_queue import build_pair_validation_queue


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a truth-preserving validation queue from a Resource Imbalance ledger"
    )
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    ledger = json.loads(Path(args.ledger).read_text(encoding="utf-8"))
    queue = build_pair_validation_queue(ledger)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output}")
    print(
        json.dumps(
            {
                "pair_hypothesis_count": queue["pair_hypothesis_count"],
                "task_count": queue["task_count"],
                "target_counts": queue["target_counts"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
