#!/usr/bin/env python3
"""Collect project-personnel capability demand from official Xuzhou tenders."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.network_ingest import write_json_atomic
from src.xuzhou_project_capability_demand import XuzhouProjectCapabilityDemandAdapter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    payload = XuzhouProjectCapabilityDemandAdapter().collect_recent_events(limit=args.limit)
    write_json_atomic(args.output, payload)
    print(f"wrote {args.output}")
    print(
        "discovered=", payload["discovery"]["item_count"],
        "events=", payload["event_count"],
        "errors=", payload["error_count"],
        "requirements=", payload["requirement_count"],
        "employment_tie_events=", payload["employment_tie_event_count"],
        "social_insurance_events=", payload["social_insurance_proof_event_count"],
    )
    for event in payload["events"][:8]:
        print(
            json.dumps(
                {
                    "date": event["publication_date"],
                    "title": event["title"],
                    "requirements": event["requirements"],
                    "transaction_constraints": event["transaction_constraints"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
