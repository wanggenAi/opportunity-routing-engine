#!/usr/bin/env python3
"""Build reviewed ResearchEvidence into a bounded Observation Fabric snapshot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.observation_store import SQLiteObservationStore  # noqa: E402
from src.observed_patterns import summarize_observed_patterns  # noqa: E402
from src.research_observation_bridge import (  # noqa: E402
    build_reviewed_research_observations,
    summarize_reviewed_research_observations,
)


def _object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--research-evidence", type=Path, required=True)
    parser.add_argument("--reviewed", type=Path, required=True)
    parser.add_argument("--observations-output", type=Path, required=True)
    parser.add_argument("--store-output", type=Path, required=True)
    parser.add_argument("--patterns-output", type=Path, required=True)
    parser.add_argument(
        "--research-scope-state",
        choices=["CALIBRATION_ONLY", "PARTIAL_DISCOVERY", "BROAD_DISCOVERY_READY"],
        required=True,
    )
    args = parser.parse_args()

    envelopes = build_reviewed_research_observations(
        _object(args.research_evidence),
        _object(args.reviewed),
    )
    summary = summarize_reviewed_research_observations(envelopes)

    args.observations_output.parent.mkdir(parents=True, exist_ok=True)
    args.observations_output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    args.store_output.parent.mkdir(parents=True, exist_ok=True)
    if args.store_output.exists():
        args.store_output.unlink()
    transitions = []
    with SQLiteObservationStore(args.store_output) as store:
        for envelope in envelopes:
            transition = store.ingest(envelope)
            transitions.append(
                {
                    "source_id": transition.source_id,
                    "observation_id": transition.observation_id,
                    "kind": transition.kind,
                    "history_sequence_id": transition.history_sequence_id,
                    "envelope_hash": transition.envelope_hash,
                }
            )

    pattern_summary = summarize_observed_patterns(
        envelopes,
        research_scope_state=args.research_scope_state,
    )
    args.patterns_output.parent.mkdir(parents=True, exist_ok=True)
    args.patterns_output.write_text(
        json.dumps(pattern_summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "observation_count": len(envelopes),
                "transition_counts": {
                    kind: sum(1 for item in transitions if item["kind"] == kind)
                    for kind in sorted({item["kind"] for item in transitions})
                },
                "research_scope_state": args.research_scope_state,
                "observed_pattern_count": pattern_summary["observed_pattern_count"],
                "unbound_pattern_count": pattern_summary["unbound_pattern_count"],
                "business_promotion": summary["business_promotion"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
