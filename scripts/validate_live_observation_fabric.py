#!/usr/bin/env python3
"""Fail-closed production validation for the live Observation Fabric artifact."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assessment", type=Path, required=True)
    parser.add_argument("--store", type=Path, required=True)
    parser.add_argument("--previous-assessment", type=Path)
    args = parser.parse_args()

    data = _load(args.assessment)
    if data.get("fixture_only") is not False or data.get("live_source_artifacts") is not True:
        raise SystemExit("live artifact is mislabeled as fixture/non-live")
    if data.get("current_observation_count", 0) <= 0:
        raise SystemExit("live Observation Fabric contains no current observations")
    if data.get("history_observation_count", 0) < data.get("current_observation_count", 0):
        raise SystemExit("history count is smaller than current state")
    if data.get("epistemic_counts", {}).keys() - {"OBSERVED"}:
        raise SystemExit("live ingress manufactured non-observed epistemic states")

    required_sources = {"JS_STATS", "XZ_GGZY", "EJY365_XZ_LINKED"}
    missing = required_sources - set(data.get("source_counts", {}))
    if missing:
        raise SystemExit(f"required live source families missing: {sorted(missing)}")

    concepts = set(data.get("concepts", []))
    forbidden = {
        "PAID_NEED",
        "PAYER_CONFIRMED",
        "CURRENT_AVAILABILITY_CONFIRMED",
        "PERMISSION_ALLOWED",
        "ROUTE_TESTABLE",
        "OPPORTUNITY_CONFIRMED",
    }
    if concepts & forbidden:
        raise SystemExit(f"downstream truth leaked into Observation Fabric: {sorted(concepts & forbidden)}")
    if "DECLARED_PROCUREMENT_BUDGET" not in concepts:
        raise SystemExit("procurement budget observation is missing")
    if "PUBLICLY_LISTED_ASSET_OR_RIGHT" not in concepts:
        raise SystemExit("resource listing observation is missing")

    manifest = data.get("upstream_manifest")
    if not isinstance(manifest, dict) or len(manifest.get("upstream_runs", {})) != 3:
        raise SystemExit("upstream run provenance is incomplete")

    connection = sqlite3.connect(args.store)
    try:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    finally:
        connection.close()
    if integrity != "ok":
        raise SystemExit(f"SQLite integrity check failed: {integrity}")

    if args.previous_assessment is not None:
        previous = _load(args.previous_assessment)
        if data["current_observation_count"] < previous.get("current_observation_count", 0):
            raise SystemExit("durable current state shrank after restoring prior live artifact")
        if data["history_observation_count"] < previous.get("history_observation_count", 0):
            raise SystemExit("durable history shrank after restoring prior live artifact")

    print(json.dumps({
        "validated": True,
        "current_observation_count": data["current_observation_count"],
        "history_observation_count": data["history_observation_count"],
        "transition_counts": data.get("transition_counts", {}),
        "source_counts": data.get("source_counts", {}),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
