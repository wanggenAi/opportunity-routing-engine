#!/usr/bin/env python3
"""Build exact recurring-pattern evidence from the durable Observation Fabric."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.observation_store import SQLiteObservationStore
from src.observed_patterns import PatternGate, summarize_observed_patterns


def build(
    *,
    store_path: Path,
    output_path: Path,
    source_run_id: int | None,
    min_observations: int,
    min_actors: int,
    min_periods: int,
    min_sources: int,
) -> dict:
    gate = PatternGate(
        min_observations=min_observations,
        min_actors=min_actors,
        min_periods=min_periods,
        min_sources=min_sources,
    )
    with SQLiteObservationStore(store_path) as store:
        current = tuple(store.iter_current())
    summary = summarize_observed_patterns(
        current,
        gate=gate,
        source_observation_run_id=source_run_id,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--store", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-run-id", type=int)
    parser.add_argument("--min-observations", type=int, default=3)
    parser.add_argument("--min-actors", type=int, default=2)
    parser.add_argument("--min-periods", type=int, default=2)
    parser.add_argument("--min-sources", type=int, default=1)
    args = parser.parse_args()
    result = build(
        store_path=args.store,
        output_path=args.output,
        source_run_id=args.source_run_id,
        min_observations=args.min_observations,
        min_actors=args.min_actors,
        min_periods=args.min_periods,
        min_sources=args.min_sources,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
