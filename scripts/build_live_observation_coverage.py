#!/usr/bin/env python3
"""Build registry → adapter → latest Observation Fabric coverage state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.live_observation_coverage import reconcile_live_observation_coverage
from src.sensor_portfolio import load_operational_sources


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reconcile production-live registry sources with unified Observation Fabric coverage"
    )
    parser.add_argument("--source-registry", default="data/source_registry.csv")
    parser.add_argument("--fabric-assessment", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    assessment = json.loads(Path(args.fabric_assessment).read_text(encoding="utf-8"))
    if not isinstance(assessment, dict):
        raise ValueError("fabric assessment must contain a JSON object")
    operational = load_operational_sources(args.source_registry)
    payload = reconcile_live_observation_coverage(operational, assessment)

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
