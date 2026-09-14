"""Reviewed bridge from governed web research into the Observation Fabric.

ResearchEvidence proves that a source was found under a governed research mission.
It is not yet an ObservationEnvelope.  This bridge accepts a reviewed, bounded
capture of what the source actually supports and turns only that capture into the
source-neutral observation contract.

Important boundary: this module never pretends an interactive web capture is a
full raw page.  The payload hash fingerprints the reviewed capture itself and the
sampling boundary must say so explicitly.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from src.observation_fabric import EvidenceRef, ObservationEnvelope, SemanticClaim


BRIDGE_SCHEMA_VERSION = "reviewed-research-observations.v1"
BRIDGE_PARSER_VERSION = "research-observation-bridge.v1"
BUSINESS_PROMOTION = "NOT_PROMOTED"
FORBIDDEN_RECORD_FIELDS = frozenset(
    {
        "payer",
        "paid_need",
        "opportunity",
        "opportunity_score",
        "commercial_score",
        "route_testable",
        "business_promotion",
        "availability_confirmed",
        "permission_allowed",
    }
)


def _canonical_hash(value: Any) -> str:
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def _require_str(raw: Mapping[str, Any], name: str) -> str:
    value = raw.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} is required")
    return value.strip()


def _string_tuple(raw: Any, name: str) -> tuple[str, ...]:
    if not isinstance(raw, list) or not all(isinstance(item, str) and item.strip() for item in raw):
        raise ValueError(f"{name} must be a non-empty-string array")
    return tuple(item.strip() for item in raw)


def _research_evidence_index(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    values = payload.get("evidence")
    if not isinstance(values, list):
        raise ValueError("research evidence payload requires evidence[]")
    result: dict[str, Mapping[str, Any]] = {}
    for item in values:
        if not isinstance(item, Mapping):
            raise ValueError("research evidence record must be an object")
        evidence_id = _require_str(item, "evidence_id")
        if evidence_id in result:
            raise ValueError(f"duplicate research evidence id: {evidence_id}")
        result[evidence_id] = item
    return result


def build_reviewed_research_observations(
    research_evidence_payload: Mapping[str, Any],
    reviewed_payload: Mapping[str, Any],
) -> tuple[ObservationEnvelope, ...]:
    if reviewed_payload.get("schema_version") != BRIDGE_SCHEMA_VERSION:
        raise ValueError("unexpected reviewed research observation schema")
    if reviewed_payload.get("semantics") != "REVIEWED_SOURCE_CAPTURE_NOT_FULL_PAGE":
        raise ValueError("reviewed capture semantics must remain explicit")

    retrieved_at = _require_str(reviewed_payload, "retrieved_at")
    evidence_index = _research_evidence_index(research_evidence_payload)
    records = reviewed_payload.get("records")
    if not isinstance(records, list):
        raise ValueError("reviewed payload requires records[]")

    envelopes: list[ObservationEnvelope] = []
    seen_observations: set[str] = set()
    for raw in records:
        if not isinstance(raw, Mapping):
            raise ValueError("reviewed observation record must be an object")
        leaked = FORBIDDEN_RECORD_FIELDS & set(raw)
        if leaked:
            raise ValueError(f"commercial truth leaked into reviewed observation: {sorted(leaked)}")

        observation_id = _require_str(raw, "observation_id")
        if observation_id in seen_observations:
            raise ValueError(f"duplicate observation_id: {observation_id}")
        seen_observations.add(observation_id)

        research_evidence_id = _require_str(raw, "research_evidence_id")
        research_evidence = evidence_index.get(research_evidence_id)
        if research_evidence is None:
            raise ValueError(f"unknown research evidence id: {research_evidence_id}")

        source_origin = _require_str(raw, "source_origin_geography")
        if source_origin != research_evidence.get("origin_geography"):
            raise ValueError("reviewed source origin drifted from research evidence")
        relevance = _string_tuple(raw.get("relevance_geographies"), "relevance_geographies")
        if research_evidence.get("relevance_geography") not in relevance:
            raise ValueError("research relevance geography was lost during observation review")

        sampling_boundary = _require_str(raw, "sampling_boundary")
        if "NOT_FULL_PAGE" not in sampling_boundary:
            raise ValueError("reviewed web capture must disclose NOT_FULL_PAGE sampling")
        captured_payload = raw.get("captured_payload")
        if not isinstance(captured_payload, Mapping) or not captured_payload:
            raise ValueError("captured_payload must be a non-empty object")
        capture_hash = _canonical_hash(captured_payload)

        actor_ids = _string_tuple(raw.get("actor_ids", []), "actor_ids") if raw.get("actor_ids") else ()
        excerpt = _require_str(raw, "evidence_excerpt")
        evidence_ref = EvidenceRef(
            ref_id=research_evidence_id,
            locator=_require_str(research_evidence, "source_url"),
            excerpt=excerpt,
            content_hash=capture_hash,
        )

        claims_raw = raw.get("claims")
        if not isinstance(claims_raw, list) or not claims_raw:
            raise ValueError("reviewed observation requires claims[]")
        claims: list[SemanticClaim] = []
        for claim_raw in claims_raw:
            if not isinstance(claim_raw, Mapping):
                raise ValueError("claim must be an object")
            epistemic = _require_str(claim_raw, "epistemic_status")
            # Public-community material is an early signal surface, never a direct
            # world-fact observation merely because the agent could read it.
            if research_evidence.get("source_family") == "PUBLIC_COMMUNITY" and epistemic == "OBSERVED":
                raise ValueError("public community evidence cannot become OBSERVED world fact")
            actor_id = claim_raw.get("actor_id")
            if actor_id is not None and actor_id not in actor_ids:
                raise ValueError("claim actor_id must be declared by reviewed record")
            geography = claim_raw.get("geography")
            if geography is not None and geography not in relevance:
                raise ValueError("claim geography must be within reviewed relevance scope")
            claims.append(
                SemanticClaim(
                    claim_id=_require_str(claim_raw, "claim_id"),
                    primitive=_require_str(claim_raw, "primitive"),
                    concept=_require_str(claim_raw, "concept"),
                    epistemic_status=epistemic,
                    evidence_refs=(research_evidence_id,),
                    value=claim_raw.get("value"),
                    actor_id=(None if actor_id is None else str(actor_id)),
                    geography=(None if geography is None else str(geography)),
                    inference_depth=int(claim_raw.get("inference_depth", 0)),
                )
            )

        unknown_fields = tuple(str(v).strip() for v in raw.get("unknown_fields", []) if str(v).strip())
        envelopes.append(
            ObservationEnvelope(
                observation_id=observation_id,
                source_id=_require_str(raw, "source_id"),
                source_record_id=_require_str(raw, "source_record_id"),
                source_locator=_require_str(research_evidence, "source_url"),
                source_origin_geography=source_origin,
                relevance_geographies=relevance,
                source_tier=_require_str(raw, "source_tier"),
                observed_at=_require_str(raw, "observed_at"),
                retrieved_at=retrieved_at,
                parser_version=BRIDGE_PARSER_VERSION,
                raw_payload_hash=capture_hash,
                sampling_boundary=sampling_boundary,
                evidence=(evidence_ref,),
                claims=tuple(claims),
                published_at=(str(raw["published_at"]) if raw.get("published_at") else None),
                actor_ids=actor_ids,
                unknown_fields=unknown_fields,
            )
        )
    return tuple(envelopes)


def summarize_reviewed_research_observations(envelopes: tuple[ObservationEnvelope, ...]) -> dict[str, Any]:
    return {
        "schema_version": BRIDGE_SCHEMA_VERSION,
        "parser_version": BRIDGE_PARSER_VERSION,
        "observation_count": len(envelopes),
        "business_promotion": BUSINESS_PROMOTION,
        "observations": [item.as_dict() for item in envelopes],
        "governing_invariants": [
            "RESEARCH_EVIDENCE_NE_OBSERVATION_UNTIL_REVIEWED",
            "REVIEWED_CAPTURE_NE_FULL_PAGE_RAW_PAYLOAD",
            "SOURCE_CLAIM_NE_WORLD_FACT",
            "COMMUNITY_SALIENCE_NE_OBSERVED_WORLD_FACT",
            "OBSERVATION_NE_DEMAND",
            "OBSERVATION_NE_PAYER",
            "OBSERVATION_NE_OPPORTUNITY",
            "UNKNOWN_NE_PASS",
        ],
    }
