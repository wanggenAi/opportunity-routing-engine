#!/usr/bin/env python3
"""Build a residual/novelty artifact for a governed Broad Discovery run."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_broad_discovery_observation_review import (  # noqa: E402
    ALIGNMENT_SCHEMA,
    ALIGNMENT_SEMANTICS,
    _alignment,
    _build_research_evidence,
    _combine_reviewed,
    _load_object,
)
from src.research_observation_bridge import build_reviewed_research_observations  # noqa: E402
from src.residual_novelty import (  # noqa: E402
    model_cluster_suggestion_from_dict,
    summarize_residual_novelty,
)


def _load_model_suggestions(path: Path | None):
    if path is None:
        return ()
    payload = _load_object(path)
    values = payload.get("suggestions")
    if not isinstance(values, list):
        raise ValueError("model suggestion payload requires suggestions[]")
    return tuple(model_cluster_suggestion_from_dict(item) for item in values)


def build_residual_novelty_run(
    *,
    mission_path: Path,
    dynamic_terms_path: Path,
    captures_path: Path,
    reviewed_dir: Path,
    alignments_path: Path,
    model_suggestions_path: Path | None = None,
) -> dict[str, Any]:
    research_evidence = _build_research_evidence(mission_path, dynamic_terms_path, captures_path)
    reviewed_payload = _combine_reviewed(reviewed_dir)
    envelopes = build_reviewed_research_observations(research_evidence, reviewed_payload)

    alignment_payload = _load_object(alignments_path)
    if alignment_payload.get("schema_version") != ALIGNMENT_SCHEMA:
        raise ValueError("unexpected alignment schema version")
    if alignment_payload.get("semantics") != ALIGNMENT_SEMANTICS:
        raise ValueError("alignment semantics drifted")
    raw_alignments = alignment_payload.get("alignments")
    if not isinstance(raw_alignments, list):
        raise ValueError("alignment payload requires alignments[]")
    alignments = tuple(_alignment(item) for item in raw_alignments)
    suggestions = _load_model_suggestions(model_suggestions_path)

    summary = summarize_residual_novelty(
        envelopes,
        reviewed_alignments=alignments,
        model_suggestions=suggestions,
    )
    summary["source_research_run_id"] = reviewed_payload.get("run_id")
    summary["source_alignment_run_id"] = alignment_payload.get("run_id")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mission", type=Path, required=True)
    parser.add_argument("--dynamic-terms", type=Path, required=True)
    parser.add_argument("--captures", type=Path, required=True)
    parser.add_argument("--reviewed-dir", type=Path, required=True)
    parser.add_argument("--alignments", type=Path, required=True)
    parser.add_argument("--model-suggestions", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = build_residual_novelty_run(
        mission_path=args.mission,
        dynamic_terms_path=args.dynamic_terms,
        captures_path=args.captures,
        reviewed_dir=args.reviewed_dir,
        alignments_path=args.alignments,
        model_suggestions_path=args.model_suggestions,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
