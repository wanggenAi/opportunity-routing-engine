#!/usr/bin/env python3
"""Build an evidence-gated resource-imbalance ledger from CSV signal files."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from src.resource_imbalance import (
    BlockerSignal,
    NeedSignal,
    ResourceSignal,
    scan_imbalances,
)


def _split_sources(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(part.strip() for part in value.split(";") if part.strip())


def _optional(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    return text or None


def _rows(path: str | None) -> list[dict[str, str]]:
    if not path:
        return []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_needs(path: str | None) -> list[NeedSignal]:
    result: list[NeedSignal] = []
    for row in _rows(path):
        if not any((value or "").strip() for value in row.values()):
            continue
        result.append(
            NeedSignal(
                signal_id=row["signal_id"].strip(),
                capability_key=row["capability_key"].strip(),
                geography=row["geography"].strip(),
                need_actor=row["need_actor"].strip(),
                payer=_optional(row.get("payer")),
                evidence_state=row["evidence_state"].strip(),
                paid_event_count=int((row.get("paid_event_count") or "0").strip() or 0),
                total_observed_spend_rmb=_optional(row.get("total_observed_spend_rmb")),
                observation_period=_optional(row.get("observation_period")),
                source_ids=_split_sources(row.get("source_ids")),
                notes=(row.get("notes") or "").strip(),
            )
        )
    return result


def load_resources(path: str | None) -> list[ResourceSignal]:
    result: list[ResourceSignal] = []
    for row in _rows(path):
        if not any((value or "").strip() for value in row.values()):
            continue
        result.append(
            ResourceSignal(
                signal_id=row["signal_id"].strip(),
                capability_key=row["capability_key"].strip(),
                geography=row["geography"].strip(),
                provider_actor=row["provider_actor"].strip(),
                resource_state=row["resource_state"].strip(),
                underuse_evidence_state=row["underuse_evidence_state"].strip(),
                available_units=_optional(row.get("available_units")),
                observation_period=_optional(row.get("observation_period")),
                source_ids=_split_sources(row.get("source_ids")),
                notes=(row.get("notes") or "").strip(),
            )
        )
    return result


def load_blockers(path: str | None) -> list[BlockerSignal]:
    result: list[BlockerSignal] = []
    for row in _rows(path):
        if not any((value or "").strip() for value in row.values()):
            continue
        result.append(
            BlockerSignal(
                signal_id=row["signal_id"].strip(),
                capability_key=row["capability_key"].strip(),
                geography=row["geography"].strip(),
                blocker_type=row["blocker_type"].strip(),
                evidence_state=row["evidence_state"].strip(),
                description=row["description"].strip(),
                source_ids=_split_sources(row.get("source_ids")),
            )
        )
    return result


def build_snapshot(
    need_path: str | None,
    resource_path: str | None,
    blocker_path: str | None,
    *,
    max_pairs_per_need: int = 5,
) -> dict[str, object]:
    needs = load_needs(need_path)
    resources = load_resources(resource_path)
    blockers = load_blockers(blocker_path)
    records = scan_imbalances(
        needs,
        resources,
        blockers,
        max_pairs_per_need=max_pairs_per_need,
    )
    counts = Counter(record.status for record in records)
    return {
        "input_counts": {
            "needs": len(needs),
            "resources": len(resources),
            "blockers": len(blockers),
        },
        "status_counts": dict(sorted(counts.items())),
        "record_count": len(records),
        "records": [record.as_dict() for record in records],
        "truth_note": (
            "ROUTE_TESTABLE justifies a bounded route test only; it does not mean "
            "transaction-ready, scalable, or G0-G6 approved."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--needs", help="CSV containing NeedSignal rows")
    parser.add_argument("--resources", help="CSV containing ResourceSignal rows")
    parser.add_argument("--blockers", help="CSV containing BlockerSignal rows")
    parser.add_argument("--max-pairs-per-need", type=int, default=5)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    snapshot = build_snapshot(
        args.needs,
        args.resources,
        args.blockers,
        max_pairs_per_need=args.max_pairs_per_need,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output}")
    print(json.dumps(snapshot["status_counts"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
