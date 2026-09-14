#!/usr/bin/env python3
"""Build a synthetic, non-production ontology lifecycle lineage artifact."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ontology_governance import OntologyConceptVersion, SQLiteOntologyRegistry


PREFIX = "concept:synthetic-lifecycle-010-"


def _version(
    suffix: str,
    version: int,
    change_kind: str,
    *,
    label: str | None = None,
    state: str = "ELIGIBLE",
) -> OntologyConceptVersion:
    concept_id = PREFIX + suffix
    return OntologyConceptVersion(
        concept_id=concept_id,
        version=version,
        primitive="FRICTION",
        preferred_label=label or suffix.upper().replace("-", "_"),
        aliases=(),
        definition=f"Synthetic lifecycle dry-run definition for {suffix} v{version}.",
        boundary="Synthetic lifecycle dry run only; never production ontology truth.",
        counterexamples=("Any production ontology, actor, payer, resource, or business claim.",),
        source_alignment_refs=(f"alignment:synthetic-lifecycle-010:{suffix}:{version}",),
        supporting_claim_refs=(f"claim:synthetic-lifecycle-010:{suffix}:{version}",),
        created_from_review_item_id=f"review:synthetic-lifecycle-010:{suffix}:{version}",
        change_kind=change_kind,
        version_state=state,
        rationale=f"Synthetic {change_kind} lifecycle dry run.",
    )


def build(db_path: Path) -> dict[str, object]:
    if db_path.exists():
        db_path.unlink()

    source_a_v1 = _version("source-a", 1, "CREATE")
    source_a_v2 = _version("source-a", 2, "REVISE")
    source_b_v1 = _version("source-b", 1, "CREATE")
    merged_v1 = _version("merged", 1, "MERGE")
    split_a_v1 = _version("split-a", 1, "SPLIT")
    split_b_v1 = _version("split-b", 1, "SPLIT")
    split_a_v2 = _version("split-a", 2, "RENAME", label="SPLIT_A_RENAMED")
    source_b_v2 = _version("source-b", 2, "DEPRECATE", state="DEPRECATED")

    with SQLiteOntologyRegistry(db_path) as registry:
        registry.register_version(source_a_v1)
        registry.register_version(source_a_v2)
        registry.add_lineage(
            from_concept_id=source_a_v2.concept_id,
            from_version=2,
            relation="REVISED_FROM",
            to_concept_id=source_a_v1.concept_id,
            to_version=1,
            rationale="Synthetic revise lineage.",
        )

        registry.register_version(source_b_v1)
        registry.register_version(merged_v1)
        for parent in (source_a_v2, source_b_v1):
            registry.add_lineage(
                from_concept_id=merged_v1.concept_id,
                from_version=1,
                relation="MERGED_FROM",
                to_concept_id=parent.concept_id,
                to_version=parent.version,
                rationale="Synthetic merge parent lineage.",
            )

        registry.register_version(split_a_v1)
        registry.register_version(split_b_v1)
        for child in (split_a_v1, split_b_v1):
            registry.add_lineage(
                from_concept_id=child.concept_id,
                from_version=1,
                relation="SPLIT_FROM",
                to_concept_id=merged_v1.concept_id,
                to_version=1,
                rationale="Synthetic split child lineage.",
            )

        registry.register_version(split_a_v2)
        registry.add_lineage(
            from_concept_id=split_a_v2.concept_id,
            from_version=2,
            relation="RENAMED_FROM",
            to_concept_id=split_a_v1.concept_id,
            to_version=1,
            rationale="Synthetic rename lineage.",
        )

        registry.register_version(source_b_v2)
        registry.add_lineage(
            from_concept_id=source_b_v1.concept_id,
            from_version=1,
            relation="DEPRECATED_BY",
            to_concept_id=source_b_v2.concept_id,
            to_version=2,
            rationale="Synthetic deprecation lineage.",
        )

        snapshot = registry.snapshot()

    relation_counts = Counter(edge["relation"] for edge in snapshot["lineage"])
    return {
        "schema_version": "ontology-lifecycle-lineage-dry-run.v1",
        "synthetic_only": True,
        "source": "SYNTHETIC_ONTOLOGY_LIFECYCLE_010",
        "registry_snapshot": snapshot,
        "lineage_relation_counts": dict(sorted(relation_counts.items())),
        "production_active_ontology_changes": 0,
        "taxonomy_promotion": "NOT_PROMOTED",
        "business_promotion": "NOT_PROMOTED",
        "truth_boundaries": [
            "SYNTHETIC_LIFECYCLE_NE_PRODUCTION_ONTOLOGY",
            "LIFECYCLE_LINEAGE_NE_TAXONOMY_PROMOTION",
            "ONTOLOGY_CONCEPT_NE_BUSINESS_OPPORTUNITY",
            "UNKNOWN_NE_PASS",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build(db_path)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "version_count": payload["registry_snapshot"]["version_count"],
        "lineage_relation_counts": payload["lineage_relation_counts"],
        "production_active_ontology_changes": payload["production_active_ontology_changes"],
        "taxonomy_promotion": payload["taxonomy_promotion"],
        "business_promotion": payload["business_promotion"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
