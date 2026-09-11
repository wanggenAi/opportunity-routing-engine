#!/usr/bin/env python3
"""Collect recent Xuzhou construction-tender capital-flow evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.network_ingest import write_json_atomic
from src.xuzhou_construction_capex import XuzhouConstructionTenderAdapter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    payload = XuzhouConstructionTenderAdapter().collect_recent_events(limit=args.limit)
    write_json_atomic(args.output, payload)
    print(f"wrote {args.output}")
    print(
        "discovered=", payload["discovery"]["item_count"],
        "events=", payload["event_count"],
        "errors=", payload["error_count"],
        "amount_evidence=", payload["amount_evidence_count"],
        "funding_evidence=", payload["funding_evidence_count"],
        "reissues=", payload["reissue_count"],
    )
    for event in payload["events"]:
        print(
            json.dumps(
                {
                    "date": event["publication_date"],
                    "title": event["title"],
                    "contract_estimate_rmb": event["contract_estimate_rmb"],
                    "funding_source": event["funding_source"],
                    "tenderer": event["tenderer"],
                    "is_reissue": event["is_reissue"],
                    "evidence_state": event["evidence_state"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
