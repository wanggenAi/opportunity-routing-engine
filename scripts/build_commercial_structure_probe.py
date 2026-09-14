#!/usr/bin/env python3
"""Join reviewed taxonomy recurrence with direct commercialization evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.latent_value_discovery import validate_candidate_record  # noqa: E402
from src.structural_commercialization import (  # noqa: E402
    assess_structural_commercialization,
    evidence_from_dict,
    summarize_assessment,
)


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--recurrence", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    recurrence = _load(args.recurrence)
    candidate = _load(args.candidate)
    evidence_payload = _load(args.evidence)

    candidate_errors = validate_candidate_record(candidate)
    if candidate_errors:
        raise ValueError("latent-value candidate is not validation-ready: " + ",".join(candidate_errors))

    concept = str(evidence_payload.get("candidate_concept") or "")
    if not concept or concept != "IDLE_ASSET_SCENARIO_REPURPOSING":
        raise ValueError("unexpected commercial structure concept")
    aligned = [
        item for item in recurrence.get("alignments", [])
        if isinstance(item, dict) and item.get("candidate_concept") == concept
    ]
    if len(aligned) != 1:
        raise ValueError("exactly one matching reviewed alignment is required")
    if aligned[0].get("state") != "PROMOTION_REVIEW_READY":
        raise ValueError("candidate concept is not PROMOTION_REVIEW_READY")
    if recurrence.get("taxonomy_promotion") != "NOT_PROMOTED" or recurrence.get("business_promotion") != "NOT_PROMOTED":
        raise ValueError("upstream recurrence artifact violated promotion boundary")

    raw_records = evidence_payload.get("evidence")
    if not isinstance(raw_records, list) or not raw_records:
        raise ValueError("commercial evidence payload requires evidence[]")
    records = tuple(evidence_from_dict(item) for item in raw_records if isinstance(item, dict))
    if len(records) != len(raw_records):
        raise ValueError("commercial evidence item must be an object")

    assessment = assess_structural_commercialization(
        candidate_id=str(candidate.get("candidate_id") or ""),
        candidate_concept=concept,
        source_taxonomy_state=str(aligned[0]["state"]),
        evidence=records,
    )
    result = summarize_assessment(assessment, records)
    result["source_recurrence_run_id"] = recurrence.get("run_id")
    result["candidate_validation_state"] = "VALIDATION_READY"
    result["candidate_class"] = "LATENT_VALUE_ACTIVATION"
    result["truth_boundaries"] = [
        "PROMOTION_REVIEW_READY_NE_CANONICAL_TAXONOMY",
        "COMMERCIAL_STRUCTURE_EVIDENCE_NE_MARKET_ENTRY_DECISION",
        "REPEAT_MONETIZATION_NE_OUR_REVENUE",
        "RESOURCE_OWNER_PAYMENT_NE_ORCHESTRATOR_FIT",
        "STRUCTURE_VALIDATION_READY_NE_BUSINESS_PROMOTION",
        "COMPOUNDING_REMAINS_UNKNOWN_WITHOUT_OUTCOME_LINKED_MEASUREMENT",
    ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
