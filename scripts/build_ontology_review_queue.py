#!/usr/bin/env python3
"""Materialize a non-promoting ontology governance queue from observation review."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ontology_governance import build_ontology_review_queue  # noqa: E402


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--observation-review", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    queue = build_ontology_review_queue(_load(args.observation_review))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "queue_kind": queue["queue_kind"],
                "review_ready_count": queue["review_ready_count"],
                "candidate_not_queued_count": queue["candidate_not_queued_count"],
                "active_ontology_changes": queue["active_ontology_changes"],
                "taxonomy_promotion": queue["taxonomy_promotion"],
                "business_promotion": queue["business_promotion"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
