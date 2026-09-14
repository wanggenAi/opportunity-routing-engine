#!/usr/bin/env python3
"""Assess executed internet-research evidence against a governed mission plan."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.research_control_plane import (  # noqa: E402
    assess_research_coverage,
    evidence_from_dict,
    mission_from_dict,
)


def _load_object(path: str) -> dict:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _load_evidence(path: str) -> list[dict]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(value, dict):
        value = value.get("evidence", [])
    if not isinstance(value, list):
        raise ValueError("research evidence must be an array or an object with evidence[]")
    if not all(isinstance(item, dict) for item in value):
        raise ValueError("each research evidence record must be an object")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mission", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    mission = mission_from_dict(_load_object(args.mission))
    plan = _load_object(args.plan)
    if plan.get("mission", {}).get("mission_id") != mission.mission_id:
        raise ValueError("plan mission_id does not match mission config")

    records = [evidence_from_dict(item) for item in _load_evidence(args.evidence)]
    assessment = assess_research_coverage(mission, plan, records)
    payload = assessment.as_dict()
    payload["truth_notes"] = [
        "Research coverage measures breadth/diversity only; it does not prove an opportunity.",
        "Global auxiliary evidence without domestic corroboration remains hypothesis support only.",
        "Source discovery does not activate collection rights or production authority.",
        "BROAD_DISCOVERY_READY authorizes broad-discovery interpretation, not business promotion.",
    ]

    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
