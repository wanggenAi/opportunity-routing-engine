#!/usr/bin/env python3
"""Import reviewed validation evidence for exact composition hypotheses."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.composition_run_store import SQLiteCompositionRunStore
from src.composition_validation_intake import validation_events_from_path
from src.composition_validation_store import SQLiteCompositionValidationStore


def _time(raw: str | None) -> datetime:
    if raw is None:
        return datetime.now(timezone.utc)
    value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise ValueError("--as-of must be timezone-aware")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--run-db", required=True)
    parser.add_argument("--validation-db", required=True)
    parser.add_argument("--format", choices=("auto", "json", "jsonl"), default="auto")
    parser.add_argument("--as-of")
    parser.add_argument("--summary-output")
    args = parser.parse_args()

    as_of = _time(args.as_of)
    imported: list[dict[str, object]] = []
    touched: set[tuple[int, int]] = set()

    with SQLiteCompositionRunStore(args.run_db) as runs, SQLiteCompositionValidationStore(
        args.validation_db
    ) as validations:
        for event in validation_events_from_path(args.input, format=args.format):
            validations.append(event, composition_runs=runs)
            stored = validations.get(event.validation_id)
            if stored is None:
                raise RuntimeError("registered composition validation disappeared")
            touched.add((stored.composition_run_id, stored.hypothesis_index))
            imported.append(
                {
                    "validation_id": stored.validation_id,
                    "composition_run_id": stored.composition_run_id,
                    "hypothesis_index": stored.hypothesis_index,
                    "dimension": stored.dimension.value,
                    "value": stored.value,
                    "observed_at": stored.observed_at.isoformat(),
                    "evidence_ref": stored.evidence_ref,
                    "subject_ref": stored.subject_ref,
                }
            )

        projections: list[dict[str, object]] = []
        for run_id, hypothesis_index in sorted(touched):
            projection = validations.projection(
                run_id,
                hypothesis_index,
                composition_runs=runs,
                as_of=as_of,
            )
            projections.append(
                {
                    "composition_run_id": run_id,
                    "hypothesis_index": hypothesis_index,
                    "composition_state": projection.composition_state.value,
                    "access_state": projection.access_state.value,
                    "transaction_gates": projection.transaction_gates(),
                    "bounded_transaction_ready": projection.bounded_transaction_ready,
                    "evidence_snapshot_fingerprint": projection.evidence_snapshot_fingerprint,
                }
            )

    summary = {
        "imported_count": len(imported),
        "imported": imported,
        "projections": projections,
        "as_of": as_of.isoformat(),
        "truth_note": (
            "Validation evidence is dimension-specific and bound to an exact composition run "
            "and hypothesis. G0-G3 are projections only; no event self-declares transaction "
            "readiness, and this layer does not create G4-G6 strategic truth."
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
