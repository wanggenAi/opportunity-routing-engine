#!/usr/bin/env python3
"""Import reviewed requirement decompositions into the versioned registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.requirement_bundle_intake import requirement_specs_from_path
from src.requirement_bundle_registry import SQLiteRequirementBundleRegistry


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--format", choices=("auto", "json", "jsonl"), default="auto")
    parser.add_argument("--summary-output")
    args = parser.parse_args()

    imported: list[dict[str, object]] = []
    with SQLiteRequirementBundleRegistry(args.db) as registry:
        for spec in requirement_specs_from_path(args.input, format=args.format):
            registry.register(spec)
            stored = registry.get(spec.bundle_id, spec.version)
            if stored is None:
                raise RuntimeError("registered requirement bundle disappeared")
            imported.append(
                {
                    "bundle_id": stored.bundle_id,
                    "version": stored.version,
                    "required_capabilities": list(stored.required_capabilities),
                    "geography": stored.geography,
                    "source_ref": stored.source_ref,
                    "active": stored.active,
                }
            )
        active = [
            {"bundle_id": spec.bundle_id, "version": spec.version}
            for spec in registry.active_specs()
        ]

    summary = {
        "imported_count": len(imported),
        "imported": imported,
        "active_bundles": active,
        "truth_note": (
            "Imported requirement bundles are reviewed capability decompositions only. "
            "They do not establish demand confirmation, payer commitment, consent, access, "
            "or transaction readiness."
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
