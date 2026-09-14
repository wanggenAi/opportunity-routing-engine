#!/usr/bin/env python3
"""Assess dynamic sensor candidates without activating collection."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sensor_registry import assess_sensor_candidate, load_sensor_candidates


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Assess source candidates for China relevance, qualification and activation readiness"
    )
    parser.add_argument("--candidates", default="data/sensor_candidates.json")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    candidates = load_sensor_candidates(args.candidates)
    assessments = [assess_sensor_candidate(item) for item in candidates]
    payload = {
        "kind": "DYNAMIC_SENSOR_CANDIDATE_ASSESSMENT",
        "candidate_count": len(candidates),
        "qualified_count": sum(bool(item["qualified"]) for item in assessments),
        "automation_ready_count": sum(
            bool(item["automation_ready"]) for item in assessments
        ),
        "assessments": assessments,
        "truth_boundaries": [
            "SOURCE_DISCOVERY_IS_NOT_SOURCE_ACTIVATION",
            "GLOBAL_SOURCE_IS_NOT_DOMESTIC_EVIDENCE",
            "PLATFORM_IS_NOT_ONTOLOGY",
        ],
    }

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
