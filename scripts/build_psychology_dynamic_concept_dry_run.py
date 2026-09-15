#!/usr/bin/env python3
"""Build a synthetic proof that psychology concepts are open and fail-closed."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.psychology_tracker import (  # noqa: E402
    PSYCHOLOGY_PRIMITIVES,
    PSYCHOLOGY_SEED_CONCEPTS,
    PsychologySignal,
    aggregate_snapshot,
)


SOCIAL_ONLY_CONCEPT = "SYNTHETIC_POST_2030_DECISION_DEFERRAL"
TRIANGULATED_CONCEPT = "SYNTHETIC_CERTAINTY_PREMIUM_SIGNAL"
PRIMITIVE_ISOLATION_CONCEPT = "SYNTHETIC_SHARED_LABEL_DIFFERENT_PRIMITIVE"


def _signal(
    idx: int,
    *,
    concept: str,
    source_type: str,
    primitive: str = "PERCEPTION",
    behavior: float = 0.0,
    money: float = 0.0,
) -> PsychologySignal:
    day = 10 + idx
    return PsychologySignal(
        signal_id=f"synthetic-{idx}",
        observed_at=date(2026, 9, day),
        source_date=date(2026, 9, day),
        source_type=source_type,
        source_name=f"synthetic-source-{idx}",
        geography="CN",
        actor_segment="SYNTHETIC_CONSUMERS",
        psychology_dimension=concept,
        direction=0.8,
        intensity=0.8,
        behavior_corroboration=behavior,
        money_corroboration=money,
        provenance_quality="HIGH",
        semantic_primitive=primitive,
    )


def build_dry_run() -> dict:
    social_only = [
        _signal(1, concept=SOCIAL_ONLY_CONCEPT, source_type="D_SOCIAL_MEDIA_LANGUAGE"),
        _signal(2, concept=SOCIAL_ONLY_CONCEPT, source_type="D_SOCIAL_MEDIA_LANGUAGE"),
        _signal(3, concept=SOCIAL_ONLY_CONCEPT, source_type="C_SEARCH_PLATFORM_TREND"),
        _signal(4, concept=SOCIAL_ONLY_CONCEPT, source_type="C_SEARCH_PLATFORM_TREND"),
        _signal(5, concept=SOCIAL_ONLY_CONCEPT, source_type="D_SOCIAL_MEDIA_LANGUAGE"),
    ]
    triangulated = [
        _signal(
            6,
            concept=TRIANGULATED_CONCEPT,
            source_type="A_HARD_MONEY_BEHAVIOR",
            behavior=0.9,
            money=0.8,
        ),
        _signal(
            7,
            concept=TRIANGULATED_CONCEPT,
            source_type="A_HARD_MONEY_BEHAVIOR",
            behavior=0.8,
            money=0.8,
        ),
        _signal(
            8,
            concept=TRIANGULATED_CONCEPT,
            source_type="B_REPRESENTATIVE_RESEARCH",
            behavior=0.5,
            money=0.4,
        ),
        _signal(
            9,
            concept=TRIANGULATED_CONCEPT,
            source_type="C_SEARCH_PLATFORM_TREND",
            behavior=0.4,
            money=0.3,
        ),
        _signal(
            10,
            concept=TRIANGULATED_CONCEPT,
            source_type="D_SOCIAL_MEDIA_LANGUAGE",
            behavior=0.3,
            money=0.2,
        ),
    ]
    primitive_isolation = [
        _signal(
            11,
            concept=PRIMITIVE_ISOLATION_CONCEPT,
            source_type="D_SOCIAL_MEDIA_LANGUAGE",
            primitive="PERCEPTION",
        ),
        _signal(
            12,
            concept=PRIMITIVE_ISOLATION_CONCEPT,
            source_type="D_SOCIAL_MEDIA_LANGUAGE",
            primitive="MOTIVE",
        ),
    ]

    social_snapshot = aggregate_snapshot(
        social_only,
        as_of=date(2026, 9, 25),
        geography="CN",
        actor_segment="SYNTHETIC_CONSUMERS",
        psychology_dimension=SOCIAL_ONLY_CONCEPT,
        semantic_primitive="PERCEPTION",
    )
    triangulated_snapshot = aggregate_snapshot(
        triangulated,
        as_of=date(2026, 9, 25),
        geography="CN",
        actor_segment="SYNTHETIC_CONSUMERS",
        psychology_dimension=TRIANGULATED_CONCEPT,
        semantic_primitive="PERCEPTION",
    )
    perception_snapshot = aggregate_snapshot(
        primitive_isolation,
        as_of=date(2026, 9, 25),
        geography="CN",
        actor_segment="SYNTHETIC_CONSUMERS",
        psychology_dimension=PRIMITIVE_ISOLATION_CONCEPT,
        semantic_primitive="PERCEPTION",
    )
    motive_snapshot = aggregate_snapshot(
        primitive_isolation,
        as_of=date(2026, 9, 25),
        geography="CN",
        actor_segment="SYNTHETIC_CONSUMERS",
        psychology_dimension=PRIMITIVE_ISOLATION_CONCEPT,
        semantic_primitive="MOTIVE",
    )

    return {
        "schema_version": "psychology-dynamic-concept-dry-run.v1",
        "synthetic_only": True,
        "stable_semantic_primitives": sorted(PSYCHOLOGY_PRIMITIVES),
        "seed_concept_count": len(PSYCHOLOGY_SEED_CONCEPTS),
        "novel_concepts": [SOCIAL_ONLY_CONCEPT, TRIANGULATED_CONCEPT],
        "novel_concepts_are_seed_nodes": [
            SOCIAL_ONLY_CONCEPT in PSYCHOLOGY_SEED_CONCEPTS,
            TRIANGULATED_CONCEPT in PSYCHOLOGY_SEED_CONCEPTS,
        ],
        "social_search_only": asdict(social_snapshot),
        "triangulated": asdict(triangulated_snapshot),
        "primitive_isolation": {
            "concept": PRIMITIVE_ISOLATION_CONCEPT,
            "perception_signal_count": perception_snapshot.signal_count,
            "motive_signal_count": motive_snapshot.signal_count,
            "perception_primitive": perception_snapshot.semantic_primitive,
            "motive_primitive": motive_snapshot.semantic_primitive,
        },
        "automatic_taxonomy_promotion_count": 0,
        "active_ontology_changes": 0,
        "taxonomy_promotion": "NOT_PROMOTED",
        "business_promotion": "NOT_PROMOTED",
        "truth_boundaries": [
            "SEED_TAXONOMY_NE_VALIDATION_BOUNDARY",
            "NEW_PSYCHOLOGY_CONCEPT_NE_CORE_CODE_CHANGE",
            "STABLE_PRIMITIVE_NE_DYNAMIC_CONCEPT",
            "SOCIAL_SALIENCE_NE_POPULATION_SHARE",
            "SEARCH_INTEREST_NE_PAID_DEMAND",
            "BEHAVIOR_CORROBORATION_NE_PAYER",
            "MONEY_CORROBORATION_NE_BUSINESS_OPPORTUNITY",
            "PSYCHOLOGY_SIGNAL_NE_TAXONOMY_PROMOTION",
            "UNKNOWN_NE_PASS",
        ],
    }


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: build_psychology_dynamic_concept_dry_run.py OUTPUT.json")
    output = Path(sys.argv[1])
    payload = build_dry_run()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
