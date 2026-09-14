#!/usr/bin/env python3
"""Build a truth-preserving Observation Fabric smoke/assessment artifact."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.emergent_taxonomy import assess_emergent_concept
from src.observation_fabric import semantic_observations_from_envelopes
from src.observation_import import envelope_from_record, load_raw_records
from src.observation_store import SQLiteObservationStore


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize heterogeneous reviewed observations into one durable source-neutral fabric"
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--known-concept", action="append", default=[])
    args = parser.parse_args()

    raw_records = load_raw_records(args.input)
    rejected: list[dict[str, object]] = []
    transitions: Counter[str] = Counter()

    with SQLiteObservationStore(args.db) as store:
        for index, record in enumerate(raw_records):
            try:
                envelope = envelope_from_record(record)
                transition = store.ingest(envelope)
                transitions[transition.kind] += 1
            except Exception as exc:
                rejected.append({"record_index": index, "error": str(exc)})
        envelopes = tuple(store.iter_current())

    semantics = semantic_observations_from_envelopes(envelopes)
    sources = {item.source_id for item in envelopes}
    actors = {
        actor_id
        for envelope in envelopes
        for actor_id in envelope.actor_ids
    }
    primitives = Counter(item.primitive for item in semantics)
    epistemic = Counter(
        claim.epistemic_status
        for envelope in envelopes
        for claim in envelope.claims
    )
    geographies = Counter(
        geography
        for envelope in envelopes
        for geography in envelope.relevance_geographies
    )
    lanes = Counter(envelope.research_lane for envelope in envelopes)
    concepts = {item.concept for item in semantics}
    known = set(args.known_concept) & concepts
    residual = sorted(concepts - known)
    unknown_fields = Counter(
        field_name
        for envelope in envelopes
        for field_name in envelope.unknown_fields
    )
    contradiction_count = sum(
        len(envelope.contradiction_refs)
        + sum(len(claim.contradiction_refs) for claim in envelope.claims)
        for envelope in envelopes
    )

    taxonomy = {
        concept: {
            "state": assessment.state,
            "observation_count": assessment.observation_count,
            "source_count": assessment.source_count,
            "actor_count": assessment.actor_count,
            "period_count": assessment.period_count,
            "reasons": list(assessment.reasons),
        }
        for concept in residual
        for assessment in [assess_emergent_concept(concept, semantics)]
    }

    provenance_complete_count = sum(
        1
        for envelope in envelopes
        if envelope.source_id
        and envelope.source_record_id
        and envelope.source_locator
        and envelope.raw_payload_hash
        and envelope.parser_version
        and envelope.evidence
    )
    fixture_only = bool(envelopes) and all(
        "FIXTURE" in envelope.source_tier for envelope in envelopes
    )

    artifact = {
        "artifact_kind": "OBSERVATION_FABRIC_ASSESSMENT",
        "schema_versions": sorted({item.schema_version for item in envelopes}),
        "observation_count": len(envelopes),
        "source_count": len(sources),
        "actor_count": len(actors),
        "primitive_coverage": dict(sorted(primitives.items())),
        "known_concept_count": len(known),
        "residual_unbound_count": len(residual),
        "residual_unbound_concepts": residual,
        "taxonomy_assessments": taxonomy,
        "epistemic_claim_counts": dict(sorted(epistemic.items())),
        "inferred_claim_count": epistemic.get("INFERRED", 0),
        "observed_reported_claim_count": epistemic.get("OBSERVED", 0)
        + epistemic.get("REPORTED", 0),
        "unknown_fields": dict(sorted(unknown_fields.items())),
        "rejected_observation_count": len(rejected),
        "rejected_observations": rejected,
        "contradiction_count": contradiction_count,
        "geography_distribution": dict(sorted(geographies.items())),
        "research_lane_distribution": dict(sorted(lanes.items())),
        "provenance_complete_count": provenance_complete_count,
        "provenance_incomplete_count": len(envelopes) - provenance_complete_count,
        "transition_counts": dict(sorted(transitions.items())),
        "fixture_only": fixture_only,
        "truth_boundaries": [
            "OBSERVATION_NE_INTERPRETATION",
            "SOURCE_CLAIM_NE_WORLD_FACT",
            "OBSERVATION_NE_DEMAND",
            "OBSERVATION_NE_PAYER",
            "OBSERVATION_NE_OPPORTUNITY",
            "SOCIAL_SALIENCE_NE_POPULATION_PREVALENCE",
            "GLOBAL_AUXILIARY_NE_DOMESTIC_FACT",
            "CONFIDENCE_NE_TRUTH_PROMOTION",
            "MISSING_NE_ZERO",
            "NO_EVIDENCE_NE_NEGATIVE_EVIDENCE",
        ],
        "truth_note": (
            "This artifact measures Observation Fabric behavior only. "
            "Fixture-only inputs are architecture evidence, not claims about the real world."
        ),
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(artifact, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
