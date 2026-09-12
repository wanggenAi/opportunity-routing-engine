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
from src.procurement_lifecycle import integrate_procurement_lifecycle
from src.resource_imbalance import BlockerSignal


def _read_json(path: str | None) -> dict:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _split_sources(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(part.strip() for part in value.split(";") if part.strip())


def _blocker_from_mapping(row: dict) -> BlockerSignal:
    sources = row.get("source_ids") or ()
    if isinstance(sources, str):
        sources = _split_sources(sources)
    else:
        sources = tuple(str(value).strip() for value in sources if str(value).strip())
    need_signal_id = str(row.get("need_signal_id") or "").strip() or None
    return BlockerSignal(
        signal_id=str(row["signal_id"]).strip(),
        capability_key=str(row["capability_key"]).strip(),
        geography=str(row["geography"]).strip(),
        blocker_type=str(row["blocker_type"]).strip(),
        evidence_state=str(row["evidence_state"]).strip(),
        description=str(row["description"]).strip(),
        source_ids=sources,
        need_signal_id=need_signal_id,
    )


def _load_blockers_csv(path: str | None) -> list[BlockerSignal]:
    if not path:
        return []
    result: list[BlockerSignal] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if not any((value or "").strip() for value in row.values()):
                continue
            result.append(_blocker_from_mapping(row))
    return result


def _load_blockers_json(paths: list[str]) -> list[BlockerSignal]:
    result: list[BlockerSignal] = []
    seen: set[str] = set()
    for path in paths:
        payload = _read_json(path)
        for row in payload.get("blockers", []) or []:
            blocker = _blocker_from_mapping(row)
            if blocker.signal_id in seen:
                continue
            seen.add(blocker.signal_id)
            result.append(blocker)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize live discovery artifacts and build Resource Imbalance ledger"
    )
    parser.add_argument("--procurement-json")
    parser.add_argument(
        "--resource-json", action="append", default=[],
        help="Resource-underuse JSON artifact; may be supplied multiple times",
    )
    parser.add_argument(
        "--provider-json", action="append", default=[],
        help="Historical capability-provider award artifact; may be supplied multiple times",
    )
    parser.add_argument(
        "--lifecycle-json",
        help="Exact-project procurement lifecycle artifact; only canonical settlement promotion is applied",
    )
    parser.add_argument("--blockers-csv", help="Optional evidence-reviewed canonical BlockerSignal CSV")
    parser.add_argument(
        "--blocker-json", action="append", default=[],
        help="Machine-readable blocker artifact; may be supplied multiple times",
    )
    parser.add_argument("--geography", default="Xuzhou")
    parser.add_argument("--max-pairs-per-need", type=int, default=5)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    procurement = _read_json(args.procurement_json)
    resources = [_read_json(path) for path in args.resource_json]
    providers = [_read_json(path) for path in args.provider_json]
    blockers = _load_blockers_csv(args.blockers_csv) + _load_blockers_json(args.blocker_json)
    ledger = build_live_imbalance_ledger(
        procurement, resources, blockers,
        provider_payloads=providers,
        geography=args.geography,
        max_pairs_per_need=args.max_pairs_per_need,
    )
    if args.lifecycle_json:
        ledger = integrate_procurement_lifecycle(
            ledger, _read_json(args.lifecycle_json),
            max_pairs_per_need=args.max_pairs_per_need,
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output}")
    print(json.dumps({
        "status_counts": ledger["status_counts"],
        "route_testable_count": ledger["route_testable_count"],
        "unbound_evidence": ledger["signal_counts"]["unbound_evidence"],
        "procurement_lifecycle": ledger.get("procurement_lifecycle"),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
