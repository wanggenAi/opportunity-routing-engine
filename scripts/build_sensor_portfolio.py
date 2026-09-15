#!/usr/bin/env python3
"""Build one reconciled view of operational sources and dynamic sensor candidates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sensor_portfolio import load_operational_sources, reconcile_sensor_portfolio
from src.sensor_registry import load_sensor_candidates


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-registry", default="data/source_registry.csv")
    parser.add_argument("--candidates", default="data/sensor_candidates.json")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    operational = load_operational_sources(args.source_registry)
    candidates = load_sensor_candidates(args.candidates)
    payload = reconcile_sensor_portfolio(operational, candidates)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
