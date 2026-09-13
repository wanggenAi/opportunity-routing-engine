#!/usr/bin/env python3
"""Import reviewed real-world outcome evidence for composition hypotheses."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.composition_outcome_intake import outcome_events_from_path
from src.composition_outcome_store import SQLiteCompositionOutcomeStore
from src.composition_run_store import SQLiteCompositionRunStore
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
    parser.add_argument("--outcome-db", required=True)
    parser.add_argument("--format", choices=("auto", "json", "jsonl"), default="auto")
    parser.add_argument("--as-of")
    parser.add_argument("--summary-output")
    args = parser.parse_args()

    as_of = _time(args.as_of)
    imported: list[dict[str, object]] = []
    touched: set[tuple[int, int]] = set()

    with SQLiteCompositionRunStore(args.run_db) as runs, SQLiteCompositionValidationStore(
        args.validation_db
    ) as validations, SQLiteCompositionOutcomeStore(args.outcome_db) as outcomes:
        for event in outcome_events_from_path(args.input, format=args.format):
            outcomes.append(
                event,
                composition_runs=runs,
                validations=validations,
            )
            stored = outcomes.get(event.outcome_id)
            if stored is None:
                raise RuntimeError("registered outcome disappeared")
            touched.add((stored.composition_run_id, stored.hypothesis_index))
            imported.append(
                {
                    "outcome_id": stored.outcome_id,
                    "composition_run_id": stored.composition_run_id,
                    "hypothesis_index": stored.hypothesis_index,
                    "transaction_ref": stored.transaction_ref,
                    "event_type": stored.event_type.value,
                    "observed_at": stored.observed_at.isoformat(),
                    "evidence_ref": stored.evidence_ref,
                    "amount": stored.amount,
                    "currency": stored.currency,
                }
            )

        projections: list[dict[str, object]] = []
        for run_id, hypothesis_index in sorted(touched):
            projection = outcomes.projection(run_id, hypothesis_index, as_of=as_of)
            projections.append(
                {
                    "composition_run_id": run_id,
                    "hypothesis_index": hypothesis_index,
                    "evidence_maturity": projection.evidence_maturity,
                    "event_count": projection.event_count,
                    "transaction_count": projection.transaction_count,
                    "accepted_settled_transaction_count": projection.accepted_settled_transaction_count,
                    "failed_transaction_count": projection.failed_transaction_count,
                    "commitment_observed": projection.commitment_observed,
                    "referral_observed": projection.referral_observed,
                    "l6_mechanism_observed": projection.l6_mechanism_observed,
                    "settlement_totals": dict(projection.settlement_totals),
                    "latest_event_type": None
                    if projection.latest_event_type is None
                    else projection.latest_event_type.value,
                    "evidence_snapshot_fingerprint": projection.evidence_snapshot_fingerprint,
                }
            )

    summary = {
        "imported_count": len(imported),
        "imported": imported,
        "projections": projections,
        "as_of": as_of.isoformat(),
        "truth_note": (
            "Outcome events are atomic observed facts bound to an exact composition and "
            "transaction-validation snapshot. Evidence maturity is a conservative projection; "
            "settlement does not prove profitability, one success does not prove repeatability, "
            "and this layer never promotes G4-G6 or L7 by itself."
        ),
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
