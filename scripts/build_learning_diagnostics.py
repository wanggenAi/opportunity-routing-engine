#!/usr/bin/env python3
"""Build review-only source/rule/composition learning diagnostics."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.capability_graph_store import SQLiteCapabilityGraphStore
from src.capability_verification_store import SQLiteCapabilityVerificationStore
from src.composition_outcome_store import SQLiteCompositionOutcomeStore
from src.composition_run_store import SQLiteCompositionRunStore
from src.composition_validation_store import SQLiteCompositionValidationStore
from src.learning_attribution import (
    claim_verification_diagnostics,
    composition_learning_diagnostic,
    rule_verification_summaries,
    source_verification_summaries,
)


def _time(raw: str | None) -> datetime:
    if raw is None:
        return datetime.now(timezone.utc)
    value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise ValueError("--as-of must be timezone-aware")
    return value


def _jsonable(value):
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if hasattr(value, "__dataclass_fields__"):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph-db", required=True)
    parser.add_argument("--verification-db", required=True)
    parser.add_argument("--run-db", required=True)
    parser.add_argument("--validation-db", required=True)
    parser.add_argument("--outcome-db", required=True)
    parser.add_argument("--run-id", type=int, required=True)
    parser.add_argument("--hypothesis-index", type=int, default=0)
    parser.add_argument("--as-of")
    parser.add_argument("--minimum-linked-verifications", type=int, default=5)
    parser.add_argument("--summary-output")
    args = parser.parse_args()

    if args.minimum_linked_verifications < 1:
        raise ValueError("--minimum-linked-verifications must be at least 1")
    as_of = _time(args.as_of)

    with SQLiteCapabilityGraphStore(args.graph_db) as graph, SQLiteCapabilityVerificationStore(
        args.verification_db
    ) as verification, SQLiteCompositionRunStore(args.run_db) as runs, SQLiteCompositionValidationStore(
        args.validation_db
    ) as validations, SQLiteCompositionOutcomeStore(args.outcome_db) as outcomes:
        run = runs.get_run(args.run_id)
        if run is None:
            raise ValueError("unknown --run-id")
        claims = claim_verification_diagnostics(
            graph,
            verification,
            materialization_id=run.materialization_id,
            as_of=as_of,
        )
        source_summaries = source_verification_summaries(
            claims,
            minimum_linked_verifications=args.minimum_linked_verifications,
        )
        rule_summaries = rule_verification_summaries(
            claims,
            minimum_linked_verifications=args.minimum_linked_verifications,
        )
        composition = composition_learning_diagnostic(
            graph,
            runs,
            validations,
            outcomes,
            run_id=args.run_id,
            hypothesis_index=args.hypothesis_index,
            as_of=as_of,
        )

    payload = {
        "as_of": as_of.isoformat(),
        "minimum_linked_verifications": args.minimum_linked_verifications,
        "claim_verification_diagnostics": _jsonable(claims),
        "source_verification_summaries": _jsonable(source_summaries),
        "rule_verification_summaries": _jsonable(rule_summaries),
        "composition_learning_diagnostic": _jsonable(composition),
        "truth_note": (
            "These are evidence-lineage diagnostics, not causal attribution. Exact related "
            "signal refs are required before a verification is linked to a source/rule. "
            "Unverified claims remain UNRESOLVED, low sample is not low quality, and review "
            "signals never mutate rules, sources, requirements, or routing policy automatically."
        ),
    }
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    print(rendered)
    if args.summary_output:
        output = Path(args.summary_output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
