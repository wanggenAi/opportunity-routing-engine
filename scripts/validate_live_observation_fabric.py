#!/usr/bin/env python3
"""Fail-closed production validation for the live Observation Fabric artifact."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

UPSTREAM_KEYS = (
    "jiangsu_money_flow",
    "regional_data",
    "resource_underuse",
    "nbs_macro",
    "pbc_jiangsu_credit",
    "pbc_money_flow",
    "xuzhou_financing_demand",
    "gacc_trade_flow",
)


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def upstream_run_ids(data: dict) -> dict[str, int]:
    manifest = data.get("upstream_manifest")
    if not isinstance(manifest, dict):
        raise SystemExit("upstream run provenance is incomplete")
    runs = manifest.get("upstream_runs")
    if not isinstance(runs, dict) or set(runs) != set(UPSTREAM_KEYS):
        raise SystemExit("upstream run provenance is incomplete")

    result: dict[str, int] = {}
    for key in UPSTREAM_KEYS:
        run = runs.get(key)
        if not isinstance(run, dict):
            raise SystemExit(f"upstream run metadata is invalid: {key}")
        database_id = run.get("databaseId")
        if isinstance(database_id, bool) or not isinstance(database_id, int) or database_id <= 0:
            raise SystemExit(f"upstream run databaseId is invalid: {key}")
        if run.get("conclusion") != "success":
            raise SystemExit(f"upstream run is not successful: {key}")
        status = run.get("status")
        if status is not None and status != "completed":
            raise SystemExit(f"upstream run is not completed: {key}")
        result[key] = database_id
    return result


def validate_upstream_monotonicity(data: dict, previous: dict) -> None:
    current_ids = upstream_run_ids(data)
    previous_ids = upstream_run_ids(previous)
    regressions = {
        key: (previous_ids[key], current_ids[key])
        for key in UPSTREAM_KEYS
        if current_ids[key] < previous_ids[key]
    }
    if regressions:
        detail = ", ".join(
            f"{key}:{before}->{after}"
            for key, (before, after) in sorted(regressions.items())
        )
        raise SystemExit(f"upstream run lineage regressed: {detail}")


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

    required_sources = {
        "JS_STATS",
        "XZ_GGZY",
        "EJY365_XZ_LINKED",
        "CN_NBS",
        "CN_PBOC_JS",
        "CN_PBOC",
        "XZ_GOV_FINANCE_DEMAND",
        "CN_CUSTOMS",
    }
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
    if "CN_RETAIL_CURRENT" not in concepts or "CN_RETAIL_YOY" not in concepts:
        raise SystemExit("required NBS macro observations are missing")
    if "CN_PBOC_JS_TOTAL_DEPOSITS_100M_CNY" not in concepts:
        raise SystemExit("required PBC Jiangsu deposit observation is missing")
    if "CN_PBOC_JS_TOTAL_LOANS_100M_CNY" not in concepts:
        raise SystemExit("required PBC Jiangsu loan observation is missing")
    for concept in (
        "CN_PBOC_SOCIAL_FINANCING_STOCK",
        "CN_PBOC_SOCIAL_FINANCING_FLOW_YTD",
        "CN_PBOC_M2_BALANCE",
        "CN_PBOC_M2_BALANCE_YOY",
    ):
        if concept not in concepts:
            raise SystemExit(f"required national PBC observation is missing: {concept}")
    for concept in (
        "XZ_SCOPED_DIRECT_ENTERPRISE_FINANCING_DEMAND",
        "XZ_SCOPED_GRANTED_CREDIT_AMOUNT",
        "XZ_SCOPED_BENEFICIARY_ENTERPRISE_COUNT",
    ):
        if concept not in concepts:
            raise SystemExit(f"required Xuzhou financing-demand observation is missing: {concept}")
    for concept in (
        "CN_CUSTOMS_IMPORTER_EXPORTER_LOCATION_EXPORTS_YTD",
        "CN_CUSTOMS_IMPORTER_EXPORTER_LOCATION_IMPORTS_YTD",
        "CN_CUSTOMS_SPECIFIC_AREA_TOTAL_YTD",
        "CN_CUSTOMS_SPECIFIC_AREA_EXPORTS_YOY",
    ):
        if concept not in concepts:
            raise SystemExit(f"required GACC trade-flow observation is missing: {concept}")

    upstream_run_ids(data)

    connection = sqlite3.connect(args.store)
    try:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    finally:
        connection.close()
    if integrity != "ok":
        raise SystemExit(f"SQLite integrity check failed: {integrity}")

    if args.previous_assessment is not None:
        previous = _load(args.previous_assessment)
        previous_runs = previous.get("upstream_manifest", {}).get("upstream_runs", {})
        if isinstance(previous_runs, dict) and set(previous_runs) == set(UPSTREAM_KEYS):
            validate_upstream_monotonicity(data, previous)
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
        "upstream_run_ids": upstream_run_ids(data),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
