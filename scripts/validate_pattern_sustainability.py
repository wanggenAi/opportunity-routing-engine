#!/usr/bin/env python3
"""Validate that recurring patterns cannot self-promote into sustainable business truth."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


AXES = {
    "RECURRENCE",
    "POPULATION",
    "STANDARDIZABILITY",
    "REPEAT_MONETIZATION",
    "COMPOUNDING",
}
MISSING_CORE_GATES = {
    "STANDARDIZABILITY",
    "REPEAT_MONETIZATION",
    "COMPOUNDING",
    "REGENERATING_EVENT_FLOW",
    "COMPLEMENTARY_ACTOR_STRUCTURE",
}
VALIDATION_TASKS = {
    "ESTABLISH_REUSABLE_TRANSFORMATION_MECHANISM",
    "ESTABLISH_COMPLEMENTARY_ACTOR_STRUCTURE",
    "ESTABLISH_REGENERATING_EVENT_FLOW",
    "ESTABLISH_REPEAT_MONETIZATION",
    "ESTABLISH_COMPOUNDING_MECHANISM",
}
FORBIDDEN_KEYS = {
    "commercial_score",
    "opportunity_score",
    "payer",
    "paid_need",
    "route_testable",
    "archetype_confirmed",
    "regenerative_loop_confirmed",
    "scale_ready",
}


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assessment", type=Path, required=True)
    parser.add_argument("--source-patterns", type=Path, required=True)
    parser.add_argument("--expected-source-run-id", type=int)
    args = parser.parse_args()

    data = _load(args.assessment)
    source = _load(args.source_patterns)
    if data.get("schema_version") != "pattern-sustainability.v1":
        raise SystemExit("unexpected sustainability schema")
    if data.get("assessment_semantics") != "SUSTAINABILITY_GAP_DIAGNOSTIC_NOT_ARCHETYPE_PROMOTION":
        raise SystemExit("sustainability assessment semantics drifted")
    if data.get("business_promotion") != "NOT_PROMOTED":
        raise SystemExit("sustainability gate attempted business promotion")
    if data.get("core_business_candidate_count") != 0:
        raise SystemExit("pattern-only evidence created a core business candidate")
    if args.expected_source_run_id is not None and data.get("source_pattern_run_id") != args.expected_source_run_id:
        raise SystemExit("sustainability artifact points to the wrong pattern run")
    if data.get("source_observation_run_id") != source.get("source_observation_run_id"):
        raise SystemExit("Observation Fabric lineage was not preserved")

    scope_state = str(source.get("research_scope_state") or "CALIBRATION_ONLY")
    expected_execution_authorized = scope_state == "BROAD_DISCOVERY_READY"
    if data.get("source_research_scope_state") != scope_state:
        raise SystemExit("sustainability artifact lost research scope lineage")
    if data.get("validation_execution_authorized") is not expected_execution_authorized:
        raise SystemExit("sustainability execution authorization drifted from research scope")

    source_patterns = {
        item["pattern_id"]: item
        for item in source.get("patterns", [])
        if isinstance(item, dict) and item.get("state") == "OBSERVED_PATTERN"
    }
    assessments = data.get("assessments")
    if not isinstance(assessments, list):
        raise SystemExit("assessments must be an array")
    if data.get("assessment_count") != len(assessments):
        raise SystemExit("assessment_count mismatch")
    if data.get("source_observed_pattern_count") != len(source_patterns):
        raise SystemExit("source observed-pattern count mismatch")
    if len(assessments) != len(source_patterns):
        raise SystemExit("not every observed pattern received a sustainability assessment")

    seen: set[str] = set()
    observed_task_count = 0
    for item in assessments:
        if not isinstance(item, dict):
            raise SystemExit("sustainability assessment must be an object")
        leaked = FORBIDDEN_KEYS & set(item)
        if leaked:
            raise SystemExit(f"downstream commercial truth leaked into sustainability record: {sorted(leaked)}")
        pattern_id = item.get("pattern_id")
        if pattern_id not in source_patterns or pattern_id in seen:
            raise SystemExit("sustainability pattern identity is missing, unknown, or duplicated")
        seen.add(pattern_id)
        pattern = source_patterns[pattern_id]
        for key in ("primitive", "concept", "geography"):
            if item.get(key) != pattern.get(key):
                raise SystemExit(f"pattern identity drifted: {key}")
        if item.get("source_pattern_state") != "OBSERVED_PATTERN":
            raise SystemExit("non-observed pattern entered sustainability gate")
        if item.get("core_business_state") != "PATTERN_ONLY":
            raise SystemExit("pattern evidence self-promoted beyond PATTERN_ONLY")
        if item.get("business_promotion") != "NOT_PROMOTED":
            raise SystemExit("individual sustainability assessment attempted promotion")
        if set(item.get("missing_core_gates") or []) != MISSING_CORE_GATES:
            raise SystemExit("pattern sustainability guard lost required unknown gates")
        if item.get("source_observation_refs") != pattern.get("supporting_observation_refs"):
            raise SystemExit("pattern support lineage changed during sustainability assessment")

        axes = item.get("axes")
        if not isinstance(axes, dict) or set(axes) != AXES:
            raise SystemExit("sustainability axes are incomplete")
        for evidenced in ("RECURRENCE", "POPULATION"):
            axis = axes[evidenced]
            if axis.get("state") != "EVIDENCED" or not axis.get("evidence_refs"):
                raise SystemExit(f"{evidenced} lost direct pattern evidence")
        for unknown in ("STANDARDIZABILITY", "REPEAT_MONETIZATION", "COMPOUNDING"):
            axis = axes[unknown]
            if axis.get("state") != "UNKNOWN" or axis.get("evidence_refs"):
                raise SystemExit(f"{unknown} was inferred from recurrence without evidence")

        for name in ("regenerating_event_flow", "complementary_actor_structure"):
            axis = item.get(name)
            if not isinstance(axis, dict) or axis.get("state") != "UNKNOWN" or axis.get("evidence_refs"):
                raise SystemExit(f"{name} was promoted without evidence")

        tasks = item.get("validation_tasks")
        if not isinstance(tasks, list):
            raise SystemExit("validation_tasks must be an array")
        task_types = {task.get("task_type") for task in tasks if isinstance(task, dict)}
        if expected_execution_authorized:
            if task_types != VALIDATION_TASKS:
                raise SystemExit("broad-scope sustainability validation tasks are incomplete")
        elif tasks:
            raise SystemExit("calibration/partial research scope created an operator validation backlog")

        for task in tasks:
            if not task.get("evidence_required") or not task.get("falsifier"):
                raise SystemExit("validation task lacks evidence requirement or falsifier")
        observed_task_count += len(tasks)

    if data.get("validation_task_count") != observed_task_count:
        raise SystemExit("validation_task_count mismatch")

    print(json.dumps({
        "validated": True,
        "source_research_scope_state": scope_state,
        "validation_execution_authorized": expected_execution_authorized,
        "validation_task_count": observed_task_count,
        "assessment_count": len(assessments),
        "core_business_candidate_count": 0,
        "business_promotion": "NOT_PROMOTED",
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
