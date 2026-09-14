"""Durable ingestion helpers for the real-world Observation Fabric."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Iterable, Mapping

from src.observation_fabric import ObservationEnvelope
from src.observation_store import SQLiteObservationStore


def source_content_fingerprint(envelope: ObservationEnvelope) -> str:
    """Fingerprint source semantics while ignoring collection clock time.

    Existing live collectors re-fetch unchanged source records on later runs. A newer
    retrieval timestamp alone is not a source revision and must not inflate evidence
    history. Parser changes remain material because they can change normalization.
    """

    payload = envelope.as_dict()
    payload.pop("observed_at", None)
    payload.pop("retrieved_at", None)
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def ingest_live_observations(
    store: SQLiteObservationStore,
    envelopes: Iterable[ObservationEnvelope],
) -> Counter[str]:
    items = tuple(envelopes)
    identities = [(item.source_id, item.observation_id) for item in items]
    if len(identities) != len(set(identities)):
        raise ValueError("current live batch produced duplicate observation identities")

    counts: Counter[str] = Counter()
    for envelope in items:
        current = store.current(envelope.source_id, envelope.observation_id)
        if (
            current is not None
            and current.parser_version == envelope.parser_version
            and source_content_fingerprint(current) == source_content_fingerprint(envelope)
        ):
            counts["UNCHANGED_SOURCE_CONTENT"] += 1
            continue
        transition = store.ingest(envelope)
        counts[transition.kind] += 1
    return counts


def summarize_live_store(
    store: SQLiteObservationStore,
    *,
    input_observation_count: int,
    transition_counts: Mapping[str, int],
    upstream_manifest: Mapping[str, object] | None = None,
) -> dict[str, object]:
    if int(transition_counts.get("OUT_OF_ORDER", 0)) > 0:
        raise ValueError(
            "live batch contains OUT_OF_ORDER observations; upstream run resolution regressed"
        )

    current_envelopes = tuple(store.iter_current())
    history_envelopes = store.query(include_history=True)
    source_counts: Counter[str] = Counter(item.source_id for item in current_envelopes)
    primitive_counts: Counter[str] = Counter()
    epistemic_counts: Counter[str] = Counter()
    concept_counts: Counter[str] = Counter()
    for envelope in current_envelopes:
        for claim in envelope.claims:
            primitive_counts[claim.primitive] += 1
            epistemic_counts[claim.epistemic_status] += 1
            concept_counts[claim.concept] += 1

    if any(state != "OBSERVED" for state in epistemic_counts):
        raise ValueError("first live adapters must not manufacture REPORTED/INFERRED claims")
    forbidden_concepts = {
        "PAID_NEED",
        "PAYER_CONFIRMED",
        "CURRENT_AVAILABILITY_CONFIRMED",
        "PERMISSION_ALLOWED",
        "ROUTE_TESTABLE",
        "OPPORTUNITY_CONFIRMED",
    }
    present_forbidden = sorted(forbidden_concepts & set(concept_counts))
    if present_forbidden:
        raise ValueError(f"live adapters created downstream truth: {present_forbidden}")

    actor_ids = {actor for item in current_envelopes for actor in item.actor_ids}
    geographies = {geo for item in current_envelopes for geo in item.relevance_geographies}
    return {
        "schema_version": "live-observation-fabric.v1",
        "fixture_only": False,
        "live_source_artifacts": True,
        "input_observation_count": input_observation_count,
        "current_observation_count": len(current_envelopes),
        "history_observation_count": len(history_envelopes),
        "transition_counts": dict(sorted(transition_counts.items())),
        "source_counts": dict(sorted(source_counts.items())),
        "primitive_counts": dict(sorted(primitive_counts.items())),
        "epistemic_counts": dict(sorted(epistemic_counts.items())),
        "actor_count": len(actor_ids),
        "geographies": sorted(geographies),
        "concept_count": len(concept_counts),
        "concepts": sorted(concept_counts),
        "upstream_manifest": dict(upstream_manifest) if upstream_manifest is not None else None,
        "truth_boundaries": [
            "OBSERVATION_NE_DEMAND",
            "DECLARED_PROCUREMENT_BUDGET_NE_PAYMENT",
            "PUBLIC_LISTING_NE_CONTROL",
            "PUBLIC_LISTING_NE_CURRENT_AVAILABILITY",
            "PUBLISHER_NE_OWNER",
            "RELISTING_NE_UNDERUSE",
            "NO_PAYER_PROMOTION",
            "NO_OPPORTUNITY_PROMOTION",
            "UNKNOWN_NE_PASS",
        ],
    }


GOVERNING_INVARIANTS = (
    "REFETCHED_UNCHANGED_SOURCE_NE_NEW_EVIDENCE",
    "PARSER_CHANGE_MAY_CREATE_REVISION",
    "LIVE_SOURCE_SELECTION_MUST_NOT_REGRESS",
    "DURABLE_HISTORY_MUST_NOT_RESET_SILENTLY",
    "LIVE_FABRIC_NE_COMMERCIAL_PROMOTION",
    "UNKNOWN_NE_PASS",
)
