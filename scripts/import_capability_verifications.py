#!/usr/bin/env python3
"""Import reviewed capability verification/falsification evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.capability_verification_intake import verification_events_from_path
from src.capability_verification_store import SQLiteCapabilityVerificationStore


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--format", choices=("auto", "json", "jsonl"), default="auto")
    parser.add_argument("--summary-output")
    args = parser.parse_args()

    imported: list[dict[str, object]] = []
    with SQLiteCapabilityVerificationStore(args.db) as store:
        for event in verification_events_from_path(args.input, format=args.format):
            store.append(event)
            stored = store.get(event.verification_id)
            if stored is None:
                raise RuntimeError("registered verification disappeared")
            imported.append(
                {
                    "verification_id": stored.verification_id,
                    "actor_ref": stored.actor_ref,
                    "capability_key": stored.capability_key,
                    "verdict": stored.verdict.value,
                    "verified_at": stored.verified_at.isoformat(),
                    "evidence_ref": stored.evidence_ref,
                    "availability": stored.availability.value,
                    "permission": stored.permission.value,
                    "related_signal_refs": list(stored.related_signal_refs),
                }
            )

    summary = {
        "imported_count": len(imported),
        "imported": imported,
        "truth_note": (
            "Capability verification is a separate reviewed evidence layer. It may confirm "
            "or reject a capability and may explicitly verify availability/permission, but "
            "it does not establish counterpart consent, access approval, payer commitment, "
            "safety approval, or transaction readiness."
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
