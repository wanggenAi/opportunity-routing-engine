#!/usr/bin/env python3
"""Build reviewed observations and semantic-alignment assessments for any governed Broad Discovery run.

The builder is deliberately run/domain neutral. Research captures remain search evidence
until a human/agent-reviewed bounded capture is supplied. Reviewed semantic alignments
may become PROMOTION_REVIEW_READY, but this script never promotes taxonomy or business
truth and never manufactures an exact source-native ObservedPattern from an alignment.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.emergent_taxonomy import ReviewedConceptAlignment, assess_reviewed_alignment  # noqa: E402
from src.observed_patterns import summarize_observed_patterns  # noqa: E402
from src.research_control_plane import build_research_plan, mission_from_dict  # noqa: E402
from src.research_execution_capture import bind_captures_to_plan, capture_from_dict  # noqa: E402
from src.research_observation_bridge import (  # noqa: E402
    BRIDGE_SCHEMA_VERSION,
    build_reviewed_research_observations,
    summarize_reviewed_research_observations,
)

ALIGNMENT_SCHEMA = "reviewed-concept-alignment.v1"
ALIGNMENT_SEMANTICS = "CANDIDATE_SEMANTIC_ALIGNMENT_NOT_TAXONOMY_PROMOTION"
REVIEW_SEMANTICS = "REVIEWED_SOURCE_CAPTURE_NOT_FULL_PAGE"
GENERIC_TRUTH_BOUNDARIES = (
    "SEARCH_CAPTURE_NE_OBSERVATION_UNTIL_REVIEWED",
    "REVIEWED_ALIGNMENT_NE_TAXONOMY_PROMOTION",
    "PROMOTION_REVIEW_READY_NE_TAXONOMY_PROMOTED",
    "PROMOTION_REVIEW_READY_NE_OBSERVED_PATTERN",
    "SOURCE_ACTION_NE_MARKET_ADOPTION",
    "SOURCE_REPORTED_VALUE_NE_SETTLEMENT",
    "CANDIDATE_NE_BUSINESS",
    "UNKNOWN_NE_PASS",
)


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _load_dynamic_terms(path: Path) -> list[str]:
    payload = _load_object(path)
    values = payload.get("dynamic_terms")
    if not isinstance(values, list) or not values or not all(isinstance(v, str) and v.strip() for v in values):
        raise ValueError("dynamic_terms must be a non-empty-string array")
    return [v.strip() for v in values]


def _build_research_evidence(mission_path: Path, dynamic_terms_path: Path, captures_path: Path) -> dict[str, Any]:
    mission = mission_from_dict(_load_object(mission_path))
    plan = build_research_plan(mission, dynamic_terms=_load_dynamic_terms(dynamic_terms_path))
    capture_payload = _load_object(captures_path)
    raw_captures = capture_payload.get("captures")
    if not isinstance(raw_captures, list):
        raise ValueError("captures payload requires captures[]")
    captures = tuple(capture_from_dict(item) for item in raw_captures)
    return bind_captures_to_plan(plan, captures)


def _combine_reviewed(reviewed_dir: Path) -> dict[str, Any]:
    paths = sorted(reviewed_dir.glob("*.json"))
    if not paths:
        raise ValueError("reviewed directory contains no JSON files")
    combined_records: list[dict[str, Any]] = []
    run_id: str | None = None
    retrieved_at: str | None = None
    for path in paths:
        payload = _load_object(path)
        if payload.get("schema_version") != BRIDGE_SCHEMA_VERSION:
            raise ValueError(f"unexpected reviewed schema in {path}")
        if payload.get("semantics") != REVIEW_SEMANTICS:
            raise ValueError(f"reviewed semantics drifted in {path}")
        current_run = str(payload.get("run_id") or "").strip()
        current_retrieved = str(payload.get("retrieved_at") or "").strip()
        if not current_run or not current_retrieved:
            raise ValueError(f"reviewed run metadata missing in {path}")
        if run_id is None:
            run_id = current_run
            retrieved_at = current_retrieved
        elif current_run != run_id or current_retrieved != retrieved_at:
            raise ValueError("split reviewed payload metadata is inconsistent")
        records = payload.get("records")
        if not isinstance(records, list):
            raise ValueError(f"reviewed file {path} requires records[]")
        combined_records.extend(records)
    return {
        "schema_version": BRIDGE_SCHEMA_VERSION,
        "semantics": REVIEW_SEMANTICS,
        "run_id": run_id,
        "retrieved_at": retrieved_at,
        "records": combined_records,
    }


def _alignment(raw: dict[str, Any]) -> ReviewedConceptAlignment:
    allowed = {
        "alignment_id",
        "candidate_concept",
        "primitive",
        "definition",
        "boundary",
        "counterexamples",
        "supporting_claim_refs",
        "alignment_rationale",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise ValueError(f"unknown alignment fields: {sorted(unknown)}")
    return ReviewedConceptAlignment(
        alignment_id=str(raw.get("alignment_id") or "").strip(),
        candidate_concept=str(raw.get("candidate_concept") or "").strip(),
        primitive=str(raw.get("primitive") or "").strip(),
        definition=str(raw.get("definition") or "").strip(),
        boundary=str(raw.get("boundary") or "").strip(),
        counterexamples=tuple(str(v).strip() for v in raw.get("counterexamples", []) if str(v).strip()),
        supporting_claim_refs=tuple(str(v).strip() for v in raw.get("supporting_claim_refs", []) if str(v).strip()),
        alignment_rationale=str(raw.get("alignment_rationale") or "").strip(),
    )


def _additional_truth_boundaries(payload: dict[str, Any]) -> tuple[str, ...]:
    values = payload.get("additional_truth_boundaries", [])
    if not isinstance(values, list) or not all(isinstance(v, str) and v.strip() for v in values):
        raise ValueError("additional_truth_boundaries must be a string array")
    normalized = tuple(v.strip() for v in values)
    if len(normalized) != len(set(normalized)):
        raise ValueError("additional_truth_boundaries must be unique")
    return normalized


def build_observation_review(
    *,
    mission_path: Path,
    dynamic_terms_path: Path,
    captures_path: Path,
    reviewed_dir: Path,
    alignments_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    research_evidence = _build_research_evidence(mission_path, dynamic_terms_path, captures_path)
    reviewed_payload = _combine_reviewed(reviewed_dir)
    envelopes = build_reviewed_research_observations(research_evidence, reviewed_payload)
    reviewed_summary = summarize_reviewed_research_observations(envelopes)

    alignment_payload = _load_object(alignments_path)
    if alignment_payload.get("schema_version") != ALIGNMENT_SCHEMA:
        raise ValueError("unexpected alignment schema version")
    if alignment_payload.get("semantics") != ALIGNMENT_SEMANTICS:
        raise ValueError("alignment semantics drifted")
    alignment_run_id = str(alignment_payload.get("run_id") or "").strip()
    if not alignment_run_id:
        raise ValueError("alignment run_id is required")
    raw_alignments = alignment_payload.get("alignments")
    if not isinstance(raw_alignments, list) or not raw_alignments:
        raise ValueError("alignment payload requires alignments[]")
    assessments = [assess_reviewed_alignment(_alignment(item), envelopes) for item in raw_alignments]

    exact_patterns = summarize_observed_patterns(
        envelopes,
        research_scope_state="BROAD_DISCOVERY_READY",
    )
    state_counts: dict[str, int] = {}
    for assessment in assessments:
        state_counts[assessment.state] = state_counts.get(assessment.state, 0) + 1

    truth_boundaries = tuple(dict.fromkeys(GENERIC_TRUTH_BOUNDARIES + _additional_truth_boundaries(alignment_payload)))
    result = {
        "schema_version": "broad-discovery-observation-review.v1",
        "run_id": alignment_run_id,
        "source_research_run_id": reviewed_payload.get("run_id"),
        "research_evidence_count": research_evidence.get("evidence_count"),
        "reviewed_observation_count": len(envelopes),
        "alignment_count": len(assessments),
        "alignment_state_counts": dict(sorted(state_counts.items())),
        "promotion_review_ready_count": state_counts.get("PROMOTION_REVIEW_READY", 0),
        "exact_observed_pattern_count": exact_patterns.get("observed_pattern_count", 0),
        "exact_unbound_pattern_count": exact_patterns.get("unbound_pattern_count", 0),
        "taxonomy_promotion": "NOT_PROMOTED",
        "business_promotion": "NOT_PROMOTED",
        "assessments": [item.as_dict() for item in assessments],
        "truth_boundaries": list(truth_boundaries),
    }
    return result, reviewed_summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mission", type=Path, required=True)
    parser.add_argument("--dynamic-terms", type=Path, required=True)
    parser.add_argument("--captures", type=Path, required=True)
    parser.add_argument("--reviewed-dir", type=Path, required=True)
    parser.add_argument("--alignments", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--observations-output", type=Path, required=True)
    args = parser.parse_args()

    result, reviewed_summary = build_observation_review(
        mission_path=args.mission,
        dynamic_terms_path=args.dynamic_terms,
        captures_path=args.captures,
        reviewed_dir=args.reviewed_dir,
        alignments_path=args.alignments,
    )

    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.observations_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.observations_output.write_text(json.dumps(reviewed_summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
