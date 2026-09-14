#!/usr/bin/env python3
"""Build targeted structural-recurrence evidence without rewriting source concepts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.emergent_taxonomy import (  # noqa: E402
    ReviewedConceptAlignment,
    assess_reviewed_alignment,
)
from src.observed_patterns import summarize_observed_patterns  # noqa: E402
from src.research_observation_bridge import (  # noqa: E402
    build_reviewed_research_observations,
)


ALIGNMENT_SCHEMA = "reviewed-concept-alignment.v1"


def _load_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _alignment(raw: dict) -> ReviewedConceptAlignment:
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent-research-evidence", type=Path, required=True)
    parser.add_argument("--parent-reviewed", type=Path, required=True)
    parser.add_argument("--research-evidence", type=Path, required=True)
    parser.add_argument("--reviewed", type=Path, required=True)
    parser.add_argument("--alignments", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    parent = build_reviewed_research_observations(
        _load_object(args.parent_research_evidence),
        _load_object(args.parent_reviewed),
    )
    current = build_reviewed_research_observations(
        _load_object(args.research_evidence),
        _load_object(args.reviewed),
    )
    envelopes = parent + current

    alignment_payload = _load_object(args.alignments)
    if alignment_payload.get("schema_version") != ALIGNMENT_SCHEMA:
        raise ValueError("unexpected alignment schema version")
    if alignment_payload.get("semantics") != "CANDIDATE_SEMANTIC_ALIGNMENT_NOT_TAXONOMY_PROMOTION":
        raise ValueError("alignment semantics drifted")
    raw_alignments = alignment_payload.get("alignments")
    if not isinstance(raw_alignments, list) or not raw_alignments:
        raise ValueError("alignment payload requires alignments[]")

    assessments = [assess_reviewed_alignment(_alignment(item), envelopes) for item in raw_alignments]
    exact_patterns = summarize_observed_patterns(
        envelopes,
        research_scope_state="BROAD_DISCOVERY_READY",
    )
    state_counts: dict[str, int] = {}
    for item in assessments:
        state_counts[item.state] = state_counts.get(item.state, 0) + 1

    result = {
        "schema_version": "structural-recurrence-probe.v1",
        "run_id": alignment_payload.get("run_id"),
        "parent_observation_count": len(parent),
        "current_observation_count": len(current),
        "combined_observation_count": len(envelopes),
        "alignment_count": len(assessments),
        "alignment_state_counts": dict(sorted(state_counts.items())),
        "promotion_review_ready_count": state_counts.get("PROMOTION_REVIEW_READY", 0),
        "taxonomy_promotion": "NOT_PROMOTED",
        "business_promotion": "NOT_PROMOTED",
        "exact_observed_pattern_count": exact_patterns["observed_pattern_count"],
        "exact_unbound_pattern_count": exact_patterns["unbound_pattern_count"],
        "alignments": [item.as_dict() for item in assessments],
        "truth_boundaries": [
            "TARGETED_FOLLOWUP_NE_BROAD_COVERAGE_RUN",
            "SOURCE_NATIVE_CONCEPTS_REMAIN_IMMUTABLE",
            "REVIEWED_ALIGNMENT_NE_SEMANTIC_REWRITE",
            "PROMOTION_REVIEW_READY_NE_TAXONOMY_PROMOTED",
            "TAXONOMY_REVIEW_NE_OBSERVED_PATTERN",
            "TAXONOMY_REVIEW_NE_PAID_NEED",
            "TAXONOMY_REVIEW_NE_BUSINESS_OPPORTUNITY",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
