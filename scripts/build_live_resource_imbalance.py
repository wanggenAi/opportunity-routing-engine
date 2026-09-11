#!/usr/bin/env python3
"""Build the live Resource Imbalance ledger from discovery artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.live_imbalance_ledger import build_live_imbalance_ledger
from src.resource_imbalance import BlockerSignal


def _read_json(path: str | None) -> dict:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _split_sources(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(part.strip() for part in value.split(";") if part.strip())


def _load_blockers(path: str | None) -> list[BlockerSignal]:
    if not path:
        return []
    result: list[BlockerSignal] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize live discovery artifacts and build Resource Imbalance ledger"
    )
    parser.add_argument("--procurement-json")
    parser.add_argument(
        "--resource-json",
        action="append",
        default=[],
        help="Resource-underuse JSON artifact; may be supplied multiple times",
    )
    parser.add_argument(
        "--provider-json",
        action="append",
        default=[],
        help="Historical capability-provider award artifact; may be supplied multiple times",
    )
    parser.add_argument(
        "--blockers-csv",
        help="Optional evidence-reviewed canonical BlockerSignal CSV",
    )
    parser.add_argument("--geography", default="Xuzhou")
    parser.add_argument("--max-pairs-per-need", type=int, default=5)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    procurement = _read_json(args.procurement_json)
    resources = [_read_json(path) for path in args.resource_json]
    providers = [_read_json(path) for path in args.provider_json]
    blockers = _load_blockers(args.blockers_csv)
    ledger = build_live_imbalance_ledger(
        procurement,
        resources,
        blockers,
        provider_payloads=providers,
        geography=args.geography,
        max_pairs_per_need=args.max_pairs_per_need,
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output}")
    print(
        json.dumps(
            {
                "status_counts": ledger["status_counts"],
                "route_testable_count": ledger["route_testable_count"],
                "unbound_evidence": ledger["signal_counts"]["unbound_evidence"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
