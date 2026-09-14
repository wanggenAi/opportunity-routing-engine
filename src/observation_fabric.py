"""Source-neutral event-level observation contract.

The Observation Fabric records what a source actually supports before any business,
resource, demand, payer or opportunity projection. Concepts are intentionally open-
ended; only the stable semantic primitive namespace is closed.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Iterable

from src.semantic_kernel import SEMANTIC_PRIMITIVES, SemanticObservation


OBSERVATION_SCHEMA_VERSION = "observation-envelope.v1"
EPISTEMIC_STATES = frozenset({"OBSERVED", "REPORTED", "INFERRED"})


def _aware_datetime(value: str, field_name: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field_name} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return parsed


def _json_serializable(value: Any) -> None:
    try:
        json.dumps(value, ensure_ascii=False, sort_keys=True)
    except TypeError as exc:
        raise ValueError("semantic claim value must be JSON-serializable") from exc


@dataclass(frozen=True)
class EvidenceRef:
    ref_id: str
    locator: str
    excerpt: str = ""
    content_hash: str = ""

    def __post_init__(self) -> None:
        if not self.ref_id.strip():
            raise ValueError("evidence ref_id is required")
        if not self.locator.strip():
            raise ValueError("evidence locator is required")
        if self.content_hash and len(self.content_hash.strip()) < 16:
            raise ValueError("content_hash is too short to be an evidence fingerprint")


@dataclass(frozen=True)
class SemanticClaim:
    claim_id: str
    primitive: str
    concept: str
    epistemic_status: str
    evidence_refs: tuple[str, ...]
    value: Any = None
    actor_id: str | None = None
    geography: str | None = None
    inference_depth: int = 0
    contradiction_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.claim_id.strip():
            raise ValueError("claim_id is required")
        if self.primitive not in SEMANTIC_PRIMITIVES:
            raise ValueError(f"unknown semantic primitive: {self.primitive}")
        if not self.concept.strip():
            raise ValueError("concept is required")
        if self.epistemic_status not in EPISTEMIC_STATES:
            raise ValueError(f"unsupported epistemic_status: {self.epistemic_status}")
        if not self.evidence_refs:
            raise ValueError("semantic claim requires evidence_refs")
        if self.inference_depth < 0:
            raise ValueError("inference_depth must be >= 0")
        if self.epistemic_status != "INFERRED" and self.inference_depth != 0:
            raise ValueError("only INFERRED claims may have inference_depth > 0")
        if self.epistemic_status == "INFERRED" and self.inference_depth < 1:
            raise ValueError("INFERRED claims require inference_depth >= 1")
        _json_serializable(self.value)


@dataclass(frozen=True)
class ObservationEnvelope:
    observation_id: str
    source_id: str
    source_record_id: str
    source_locator: str
    source_origin_geography: str
    relevance_geographies: tuple[str, ...]
    source_tier: str
    observed_at: str
    retrieved_at: str
    parser_version: str
    raw_payload_hash: str
    sampling_boundary: str
    evidence: tuple[EvidenceRef, ...]
    claims: tuple[SemanticClaim, ...]
    published_at: str | None = None
    actor_ids: tuple[str, ...] = ()
    unknown_fields: tuple[str, ...] = ()
    contradiction_refs: tuple[str, ...] = ()
    supersedes_observation_id: str | None = None
    schema_version: str = OBSERVATION_SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name in (
            "observation_id",
            "source_id",
            "source_record_id",
            "source_locator",
            "source_origin_geography",
            "source_tier",
            "parser_version",
            "raw_payload_hash",
            "sampling_boundary",
            "schema_version",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} is required")
        if self.schema_version != OBSERVATION_SCHEMA_VERSION:
            raise ValueError(f"unsupported schema_version: {self.schema_version}")
        if not self.relevance_geographies:
            raise ValueError("relevance_geographies are required")
        _aware_datetime(self.observed_at, "observed_at")
        _aware_datetime(self.retrieved_at, "retrieved_at")
        if self.published_at is not None:
            _aware_datetime(self.published_at, "published_at")
        digest = self.raw_payload_hash.strip().lower()
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise ValueError("raw_payload_hash must be a SHA-256 hex digest")
        if not self.evidence:
            raise ValueError("observation requires evidence")
        if not self.claims:
            raise ValueError("observation requires at least one semantic claim")

        evidence_ids = [item.ref_id for item in self.evidence]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("duplicate evidence ref_id")
        claim_ids = [item.claim_id for item in self.claims]
        if len(claim_ids) != len(set(claim_ids)):
            raise ValueError("duplicate claim_id")

        available_refs = set(evidence_ids)
        for claim in self.claims:
            missing = set(claim.evidence_refs) - available_refs
            if missing:
                raise ValueError(
                    f"claim {claim.claim_id} references unknown evidence: {sorted(missing)}"
                )
            missing_contradictions = set(claim.contradiction_refs) - available_refs
            if missing_contradictions:
                raise ValueError(
                    f"claim {claim.claim_id} references unknown contradiction evidence: "
                    f"{sorted(missing_contradictions)}"
                )
        missing_envelope_contradictions = set(self.contradiction_refs) - available_refs
        if missing_envelope_contradictions:
            raise ValueError(
                "observation references unknown contradiction evidence: "
                f"{sorted(missing_envelope_contradictions)}"
            )

    @property
    def research_lane(self) -> str:
        origin = self.source_origin_geography.upper()
        if origin == "CN" or origin.startswith("CN-"):
            return "CHINA_PRIMARY"
        return "GLOBAL_AUXILIARY"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def semantic_observations_from_envelope(
    envelope: ObservationEnvelope,
) -> tuple[SemanticObservation, ...]:
    """Project envelope claims into the existing primitive-level abstraction."""

    result: list[SemanticObservation] = []
    default_actor = envelope.actor_ids[0] if len(envelope.actor_ids) == 1 else None
    default_geo = (
        envelope.relevance_geographies[0]
        if len(envelope.relevance_geographies) == 1
        else None
    )
    for claim in envelope.claims:
        result.append(
            SemanticObservation(
                observation_id=f"{envelope.observation_id}:{claim.claim_id}",
                primitive=claim.primitive,
                concept=claim.concept,
                source_id=envelope.source_id,
                observed_at=envelope.observed_at,
                evidence_refs=tuple(claim.evidence_refs),
                actor_id=claim.actor_id or default_actor,
                geography=claim.geography or default_geo,
                epistemic_status=claim.epistemic_status,
            )
        )
    return tuple(result)


def semantic_observations_from_envelopes(
    envelopes: Iterable[ObservationEnvelope],
) -> tuple[SemanticObservation, ...]:
    return tuple(
        semantic
        for envelope in envelopes
        for semantic in semantic_observations_from_envelope(envelope)
    )


def project_to_resource_signal(envelope: ObservationEnvelope):
    """Conservative bridge to the legacy resource/capability signal model.

    Only directly OBSERVED claims are eligible. REPORTED or INFERRED claims are never
    upgraded into ObservedFact/ExplicitCapability. Availability and permission are
    always UNKNOWN because the Observation Fabric cannot create those downstream
    transaction states.
    """

    from src.live_resource_signals import (
        AvailabilityState,
        ExplicitCapability,
        ObservedFact,
        PermissionState,
        SignalObservation,
    )

    if len(envelope.actor_ids) != 1:
        return None

    observed_claims = tuple(
        claim for claim in envelope.claims if claim.epistemic_status == "OBSERVED"
    )
    facts = tuple(
        ObservedFact(
            key=f"{claim.primitive.lower()}:{claim.concept}",
            value=claim.value,
            evidence_text=";".join(claim.evidence_refs),
        )
        for claim in observed_claims
    )
    capabilities = tuple(
        ExplicitCapability(
            capability_key=claim.concept,
            evidence_text=";".join(claim.evidence_refs),
        )
        for claim in observed_claims
        if claim.primitive == "CAPABILITY"
    )
    if not facts and not capabilities:
        return None

    source_url = ""
    for item in envelope.evidence:
        if item.locator.startswith("https://"):
            source_url = item.locator
            break

    signal = SignalObservation(
        signal_id=envelope.observation_id,
        source_id=envelope.source_id,
        observed_at=_aware_datetime(envelope.observed_at, "observed_at"),
        actor_ref=envelope.actor_ids[0],
        geography=(
            envelope.relevance_geographies[0]
            if len(envelope.relevance_geographies) == 1
            else ""
        ),
        raw_text="",
        source_url=source_url,
        facts=facts,
        explicit_capabilities=capabilities,
        availability=AvailabilityState.UNKNOWN,
        permission=PermissionState.UNKNOWN,
    )
    errors = signal.validate()
    if errors:
        raise ValueError("resource signal projection is invalid: " + ",".join(errors))
    return signal


GOVERNING_INVARIANTS = (
    "DISCOVER_DO_NOT_INVENT",
    "OBSERVATION_NE_INTERPRETATION",
    "SOURCE_CLAIM_NE_WORLD_FACT",
    "SOCIAL_SALIENCE_NE_POPULATION_PREVALENCE",
    "REPORTED_MOTIVE_NE_OBSERVED_MOTIVE",
    "INFERRED_FRICTION_NE_CONFIRMED_FRICTION",
    "OBSERVATION_NE_DEMAND",
    "OBSERVATION_NE_PAYER",
    "OBSERVATION_NE_OPPORTUNITY",
    "CONFIDENCE_NE_TRUTH_PROMOTION",
    "MISSING_NE_ZERO",
    "NO_EVIDENCE_NE_NEGATIVE_EVIDENCE",
    "RECOMMENDATION_NE_CONSENT",
    "ACTOR_AUTONOMY",
    "NO_COERCIVE_ROUTING",
    "NO_MORAL_PERSONALITY_SCORING",
    "NO_ARTIFICIAL_DEPENDENCY",
)
