#!/usr/bin/env python3
"""Import explicit ontology review decisions into the append-only decision ledger."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ontology_review_intake import (
    SQLiteOntologyReviewDecisionStore,
    records_from_path,
    review_decision_event_from_record,
    review_items_by_id,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-queue", required=True)
    parser.add_argument("--decisions", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--snapshot-output", required=True)
    parser.add_argument("--format", default="auto", choices=("auto", "json", "jsonl"))
    args = parser.parse_args()

    queue = json.loads(Path(args.review_queue).read_text(encoding="utf-8"))
    if not isinstance(queue, dict):
        raise ValueError("review queue must be a JSON object")
    review_items = review_items_by_id(queue)

    imported = 0
    with SQLiteOntologyReviewDecisionStore(args.db) as store:
        for record in records_from_path(args.decisions, format=args.format):
            event = review_decision_event_from_record(record)
            review_item = review_items.get(event.review_item_id)
            if review_item is None:
                raise ValueError(f"unknown review_item_id: {event.review_item_id}")
            store.append(event, review_item)
            imported += 1
        snapshot = store.snapshot()

    output = Path(args.snapshot_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {"imported": imported, **{k: v for k, v in snapshot.items() if k != "events"}},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
