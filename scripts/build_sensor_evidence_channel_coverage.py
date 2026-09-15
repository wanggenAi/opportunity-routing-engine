#!/usr/bin/env python3
"""Build evidence-channel coverage from registries and latest live Observation coverage."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sensor_evidence_channel_coverage import (
    load_evidence_channel_registry,
    reconcile_sensor_evidence_channel_coverage,
)
from src.sensor_portfolio import load_operational_sources
from src.sensor_registry import load_sensor_candidates


def _load_object(path: str | Path) -> dict:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-registry", default="data/source_registry.csv")
    parser.add_argument("--candidates", default="data/sensor_candidates.json")
    parser.add_argument(
        "--channel-registry", default="data/evidence_channel_registry.json"
    )
    parser.add_argument("--live-observation-coverage", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    payload = reconcile_sensor_evidence_channel_coverage(
        load_operational_sources(args.source_registry),
        load_sensor_candidates(args.candidates),
        _load_object(args.live_observation_coverage),
        load_evidence_channel_registry(args.channel_registry),
    )

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
