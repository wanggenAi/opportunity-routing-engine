#!/usr/bin/env python3
"""Fail closed if a planning-only research artifact claims executed coverage or business truth."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    parser.add_argument("--coverage", required=True)
    args = parser.parse_args()

    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    coverage = json.loads(Path(args.coverage).read_text(encoding="utf-8"))

    if plan.get("schema_version") != "research-control-plane.v1":
        raise SystemExit("unexpected research plan schema")
    if int(plan.get("query_count", 0)) <= 0:
        raise SystemExit("research plan must contain query tasks")
    if coverage.get("state") != "CALIBRATION_ONLY":
        raise SystemExit("planning workflow must remain CALIBRATION_ONLY before evidence execution")
    if coverage.get("broad_discovery_use_authorized") is not False:
        raise SystemExit("planning workflow cannot authorize broad discovery use")
    if int(coverage.get("evidence_count", -1)) != 0:
        raise SystemExit("planning workflow cannot manufacture internet evidence")
    if "NO_RESEARCH_EVIDENCE_EXECUTED" not in set(coverage.get("blockers", [])):
        raise SystemExit("empty research execution blocker is required")

    truth = set(plan.get("truth_boundaries", []))
    required = {
        "RESEARCH_PLAN_NE_EVIDENCE",
        "SEARCH_RESULT_NE_OBSERVATION_UNTIL_PROVENANCE_CAPTURED",
        "GLOBAL_AUXILIARY_NE_DOMESTIC_FACT",
        "SOURCE_DISCOVERY_NE_SOURCE_ACTIVATION",
        "COVERAGE_NE_COMMERCIAL_TRUTH",
        "CROSS_BORDER_EXCEPTION_ONLY",
    }
    missing = sorted(required - truth)
    if missing:
        raise SystemExit(f"missing research truth boundaries: {missing}")

    print(
        json.dumps(
            {
                "validated": True,
                "mission_id": coverage.get("mission_id"),
                "query_count": plan.get("query_count"),
                "coverage_state": coverage.get("state"),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
