#!/usr/bin/env python3
"""Build persistent resource-composition runs from capability graph materializations."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.capability_graph_store import SQLiteCapabilityGraphStore
from src.composition_run_store import SQLiteCompositionRunStore
from src.requirement_bundle_registry import SQLiteRequirementBundleRegistry


def _time(raw: str | None) -> datetime | None:
    if raw is None:
        return None
    value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise ValueError("--as-of must be timezone-aware")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph-db", required=True)
    parser.add_argument("--requirement-db", required=True)
    parser.add_argument("--run-db", required=True)
    parser.add_argument("--bundle-id")
    parser.add_argument("--materialization-id", type=int)
    parser.add_argument("--as-of")
    parser.add_argument("--max-age-days", type=float, default=30.0)
    parser.add_argument("--max-actors", type=int, default=4)
    parser.add_argument("--max-hypotheses", type=int, default=100)
    parser.add_argument("--summary-output")
    args = parser.parse_args()

    as_of = _time(args.as_of)
    max_age = timedelta(days=args.max_age_days)
    if max_age < timedelta(0):
        raise ValueError("--max-age-days must not be negative")

    summaries: list[dict[str, object]] = []
    with SQLiteCapabilityGraphStore(args.graph_db) as graph, SQLiteRequirementBundleRegistry(
        args.requirement_db
    ) as requirements, SQLiteCompositionRunStore(args.run_db) as runs:
        if args.bundle_id:
            spec = requirements.active(args.bundle_id)
            if spec is None:
                raise ValueError(f"no active requirement bundle: {args.bundle_id}")
            specs = (spec,)
        else:
            specs = requirements.active_specs()
            if not specs:
                raise ValueError("no active requirement bundles")

        for spec in specs:
            run = runs.build_run(
                graph,
                spec,
                materialization_id=args.materialization_id,
                as_of=as_of,
                max_age=max_age,
                max_actors=args.max_actors,
                max_hypotheses=args.max_hypotheses,
            )
            hypotheses = runs.hypotheses(run.run_id)
            state_counts = Counter(item.state.value for item in hypotheses)
            summaries.append(
                {
                    "run_id": run.run_id,
                    "materialization_id": run.materialization_id,
                    "bundle_id": run.bundle_id,
                    "bundle_version": run.bundle_version,
                    "bundle_source_ref": run.bundle_source_ref,
                    "hypothesis_count": run.hypothesis_count,
                    "state_counts": dict(sorted(state_counts.items())),
                    "hypotheses": [
                        {
                            "state": item.state.value,
                            "actor_refs": list(item.actor_refs),
                            "source_signal_ids": list(item.source_signal_ids),
                            "contributions": [
                                {
                                    "capability_key": contribution.capability_key,
                                    "actor_refs": list(contribution.actor_refs),
                                    "strongest_evidence_status": contribution.strongest_evidence_status.value,
                                    "callable_actor_refs": list(contribution.callable_actor_refs),
                                    "source_signal_ids": list(contribution.source_signal_ids),
                                }
                                for contribution in item.contributions
                            ],
                        }
                        for item in hypotheses
                    ],
                }
            )

    payload = {
        "composition_runs": summaries,
        "truth_note": (
            "Requirement bundles are decomposition hypotheses, not demand or payer truth. "
            "Composition states describe structural capability coverage only; even callable "
            "coverage is not consent, access, safety approval, or transactionability."
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
