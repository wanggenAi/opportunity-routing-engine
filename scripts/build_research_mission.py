#!/usr/bin/env python3
"""Build a bounded internet-research mission and explicit empty coverage state."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.research_control_plane import (  # noqa: E402
    build_research_plan,
    empty_coverage_assessment,
    mission_from_dict,
)


def _load_dynamic_terms(path: str | None) -> list[str]:
    if not path:
        return []
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [str(item).strip() for item in payload if str(item).strip()]
    if isinstance(payload, dict):
        values = payload.get("dynamic_terms", [])
        if not isinstance(values, list):
            raise ValueError("dynamic_terms must be an array")
        return [str(item).strip() for item in values if str(item).strip()]
    raise ValueError("dynamic term payload must be an array or object")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mission", required=True)
    parser.add_argument("--dynamic-terms")
    parser.add_argument("--as-of-date", help="ISO date override; defaults to the mission config")
    parser.add_argument("--plan-output", required=True)
    parser.add_argument("--coverage-output", required=True)
    args = parser.parse_args()

    mission_payload = json.loads(Path(args.mission).read_text(encoding="utf-8"))
    if not isinstance(mission_payload, dict):
        raise ValueError("mission file must contain a JSON object")
    mission = mission_from_dict(mission_payload)
    if args.as_of_date:
        date.fromisoformat(args.as_of_date)
        mission = replace(mission, as_of_date=args.as_of_date)

    dynamic_terms = _load_dynamic_terms(args.dynamic_terms)
    plan = build_research_plan(mission, dynamic_terms=dynamic_terms)
    coverage = empty_coverage_assessment(mission, plan)

    plan_path = Path(args.plan_output)
    coverage_path = Path(args.coverage_output)
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    coverage_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    coverage_path.write_text(json.dumps(coverage, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "mission_id": mission.mission_id,
                "as_of_date": mission.as_of_date,
                "query_count": plan["query_count"],
                "coverage_state": coverage["state"],
                "broad_discovery_use_authorized": coverage["broad_discovery_use_authorized"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
