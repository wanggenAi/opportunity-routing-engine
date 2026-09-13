#!/usr/bin/env python3
"""Materialize the current Resource Capability Graph from durable signal evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.capability_graph_store import SQLiteCapabilityGraphStore
from src.capability_rule_registry import SQLiteCapabilityRuleRegistry
from src.live_signal_store import SQLiteSignalLedgerStore


def _claim_summary(claim) -> dict[str, str]:
    return {
        "actor_ref": claim.actor_ref,
        "capability_key": claim.capability_key,
        "evidence_status": claim.evidence_status.value,
        "source_signal_ref": claim.source_signal_ref,
        "inference_rule_id": claim.inference_rule_id,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--signal-db", required=True)
    parser.add_argument("--rule-db", required=True)
    parser.add_argument("--graph-db", required=True)
    parser.add_argument("--summary-output")
    args = parser.parse_args()

    with SQLiteSignalLedgerStore(args.signal_db) as signals, SQLiteCapabilityRuleRegistry(
        args.rule_db
    ) as rules, SQLiteCapabilityGraphStore(args.graph_db) as graph:
        previous = graph.latest_materialization()
        current = graph.materialize_current(signals, rules)

        added = ()
        removed = ()
        if previous is not None and previous.materialization_id != current.materialization_id:
            diff = graph.diff(previous.materialization_id, current.materialization_id)
            added = diff.added
            removed = diff.removed

        summary = {
            "materialization_id": current.materialization_id,
            "previous_materialization_id": (
                previous.materialization_id if previous is not None else None
            ),
            "observation_count": current.observation_count,
            "claim_count": current.claim_count,
            "active_rule_ids": list(current.active_rule_ids),
            "ruleset_fingerprint": current.ruleset_fingerprint,
            "observation_snapshot_fingerprint": current.observation_snapshot_fingerprint,
            "added_claim_count": len(added),
            "removed_claim_count": len(removed),
            "added_claims": [_claim_summary(claim) for claim in added],
            "removed_claims": [_claim_summary(claim) for claim in removed],
            "truth_note": (
                "The capability graph is a derived evidence snapshot. INFERRED and OBSERVED "
                "claims are not confirmations, permissions, consent, or transaction truth."
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
