#!/usr/bin/env python3
"""Ingest neutral live observations into the durable signal ledger."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.live_signal_intake import signals_from_path
from src.live_signal_store import SQLiteSignalLedgerStore


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="neutral JSON or JSONL observation file")
    parser.add_argument("--db", required=True, help="SQLite signal-ledger path")
    parser.add_argument("--format", choices=("auto", "json", "jsonl"), default="auto")
    parser.add_argument("--summary-output", help="optional JSON summary path")
    args = parser.parse_args()

    counts: Counter[str] = Counter()
    total = 0
    with SQLiteSignalLedgerStore(args.db) as store:
        for signal in signals_from_path(args.input, format=args.format):
            transition = store.ingest(signal)
            counts[transition.kind.value] += 1
            total += 1

        current_count = sum(1 for _ in store.iter_current())

    summary = {
        "input": str(Path(args.input)),
        "db": str(Path(args.db)),
        "ingested": total,
        "transition_counts": dict(sorted(counts.items())),
        "current_signal_count": current_count,
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))

    if args.summary_output:
        output = Path(args.summary_output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
