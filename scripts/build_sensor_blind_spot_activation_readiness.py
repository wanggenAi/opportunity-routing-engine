#!/usr/bin/env python3
"""Build activation-readiness state for current evidence-channel blind spots."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sensor_blind_spot_activation_readiness import (
    reconcile_blind_spot_activation_readiness,
)
from src.sensor_portfolio import load_operational_sources
from src.sensor_registry import load_sensor_candidates


def _load_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-registry", type=Path, default=Path("data/source_registry.csv"))
    parser.add_argument("--candidates", type=Path, default=Path("data/sensor_candidates.json"))
    parser.add_argument("--evidence-channel-coverage", type=Path, required=True)
    parser.add_argument("--douyin-permission-evidence", type=Path, required=True)
    parser.add_argument("--evidence-channel-run-id", type=int, required=True)
    parser.add_argument("--douyin-permission-run-id", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.evidence_channel_run_id <= 0 or args.douyin_permission_run_id <= 0:
        raise ValueError("upstream run ids must be positive")

    payload = reconcile_blind_spot_activation_readiness(
        load_operational_sources(args.source_registry),
        load_sensor_candidates(args.candidates),
        _load_object(args.evidence_channel_coverage),
        permission_probes={
            "DOUYIN_OPENAPI": _load_object(args.douyin_permission_evidence),
        },
    )
    payload["upstream_runs"] = {
        "sensor_evidence_channel_coverage": args.evidence_channel_run_id,
        "douyin_openapi_permission_probe": args.douyin_permission_run_id,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
