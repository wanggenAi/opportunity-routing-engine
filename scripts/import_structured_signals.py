#!/usr/bin/env python3
"""Import reviewed structured observations into the durable signal ledger."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.live_signal_store import SQLiteSignalLedgerStore
from src.structured_signal_import import load_records, signal_from_record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--summary-output")
    args = parser.parse_args()

    records = load_records(args.input)
    counts: Counter[str] = Counter()
    errors: list[dict[str, object]] = []

    with SQLiteSignalLedgerStore(args.db) as store:
        for index, record in enumerate(records):
            try:
                signal = signal_from_record(record)
                transition = store.ingest(signal)
                counts[transition.kind.value] += 1
            except Exception as exc:
                errors.append({"record_index": index, "error": str(exc)})
        current_count = sum(1 for _ in store.iter_current())

    summary = {
        "input_record_count": len(records),
        "imported_transition_count": sum(counts.values()),
        "transition_counts": dict(sorted(counts.items())),
        "error_count": len(errors),
        "errors": errors,
        "current_signal_count": current_count,
        "truth_note": (
            "Structured import preserves reviewed observations only; it cannot create "
            "confirmed availability, commitment, or permission state."
        ),
    }
    rendered = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    print(rendered)

    if args.summary_output:
        output = Path(args.summary_output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
