#!/usr/bin/env python3
"""Collect latest verified Xuzhou macro release from Jiangsu official mirror."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.network_ingest import write_json_atomic
from src.xuzhou_macro_mirror import XuzhouMacroMirrorAdapter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-pages", type=int, default=35)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    payload = XuzhouMacroMirrorAdapter().collect_latest(max_pages=args.max_pages)
    write_json_atomic(args.output, payload)
    release = payload["release"]
    print(f"wrote {args.output}")
    print(
        "title=", release["title"],
        "publication_date=", release["publication_date"],
        "metric_count=", release["metric_count"],
        "pages_scanned=", payload["discovery"]["pages_scanned"],
        "freshness=", payload["freshness"],
    )
    print(
        "metrics=",
        json.dumps(
            {item["signal_id"]: item["value"] for item in release["metrics"]},
            ensure_ascii=False,
            sort_keys=True,
        ),
    )


if __name__ == "__main__":
    main()
