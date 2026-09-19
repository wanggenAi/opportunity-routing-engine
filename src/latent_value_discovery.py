"""Canonical latent-value discovery model.

Discovery starts from actors, state changes and unrealized value rather than from
explicit supply/demand listings.  The model is intentionally fail-closed: a complete
story is not enough to become validation-ready.  Independent evidence dimensions
must support the origin actor, the complementary side and the reason value is still
stranded.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping, Sequence

from src.causal_descent import (
    CausalDescentRecord,
    causal_descent_from_mapping,
    unbound_causal_evidence_refs,
    validate_causal_descent_for_promotion,
    validate_causal_projection,
)


class CandidateClass(str, Enum):
    """Architectural class of a discovered commercial hypothesis."""

    LATENT_VALUE_ACTIVATION = "LATENT_VALUE_ACTIVATION"
    EXPLICIT_DEMAND_EXECUTION = "EXPLICIT_DEMAND_EXECUTION"


class DiscoveryState(str, Enum):
    """Evidence maturity inside the latent-value discovery layer."""

    OBSERVED_PATTERN = "OBSERVED_PATTERN"
    LATENT_VALUE_HYPOTHESIS = "LATENT_VALUE_HYPOTHESIS"
    STRUCTURAL_FRICTION_HYPOTHESIS = "STRUCTURAL_FRICTION_HYPOTHESIS"
    COMPLEMENTARITY_HYPOTHESIS = "COMPLEMENTARITY_HYPOTHESIS"
    LATENT_CONNECTION_EVIDENCED = "LATENT_CONNECTION_EVIDENCED"
    VALIDATION_READY = "VALIDATION_READY"


class EvidenceKind(str, Enum):
    """What a source actually supports.

    These labels prevent a single macro article from silently supporting every leg of
    a latent-value story.
    """

    ORIGIN_STATE = "ORIGIN_STATE"
    ORIGIN_CHANGE = "ORIGIN_CHANGE"
    STRUCTURAL_FRICTION = "STRUCTURAL_FRICTION"
    COMPLEMENTARY_STATE = "COMPLEMENTARY_STATE"
    CONNECTION_PRESSURE = "CONNECTION_PRESSURE"
    MISSING_EDGE = "MISSING_EDGE"
    STRANDING_BARRIER = "STRANDING_BARRIER"
    VALUE_PRECEDENT = "VALUE_PRECEDENT"
    GENERAL_PATTERN = "GENERAL_PATTERN"


@dataclass(frozen=True)
class EvidenceRef:
    source_id: str
    claim: str
    kind: EvidenceKind = EvidenceKind.GENERAL_PATTERN

    def is_usable(self) -> bool:
        return bool(self.source_id.strip() and self.claim.strip())


@dataclass(frozen=True)
class LatentValueCandidate:
    """A hypothesis that value exists before a market-side label necessarily exists."""

    candidate_id: str
    actor: str
    observed_state: str
    observed_change: str
    hidden_or_underrecognized_value: str
    why_value_is_not_recognized_or_realized: str
    complementary_actor_hypothesis: str
    complementary_actor_state: str
    transformation_mechanism: str
    why_exchange_does_not_already_happen: str
    incremental_value_for_origin_actor: str
    incremental_value_for_complementary_actor: str
    orchestrator_value_capture_hypothesis: str
    cheapest_decisive_validation: str
    kill_conditions: str
    surface_phenomenon_or_friction: str = ""
    latent_outcome_hypothesis: str = ""
    structural_friction_hypothesis: str = ""
    structural_friction_truth_state: str = "INFERRED"
    alternative_explanations: tuple[str, ...] = ()
    persistent_mismatch: str = ""
    causal_descent: CausalDescentRecord | None = None
    causal_descent_record_id: str = ""
    causal_stop_reason: str = ""
    connection_pressure_hypothesis: str = ""
    observed_missing_edge: str = ""
    latent_connection_hypothesis: str = ""
    evidence: Sequence[EvidenceRef] = field(default_factory=tuple)
    source_mode: str = "LATENT_VALUE_DISCOVERY"

    def candidate_class(self) -> CandidateClass:
        if self.source_mode == "EXPLICIT_DEMAND":
            return CandidateClass.EXPLICIT_DEMAND_EXECUTION
        return CandidateClass.LATENT_VALUE_ACTIVATION


_REQUIRED_FIELDS = (
    "candidate_id",
    "actor",
    "observed_state",
    "hidden_or_underrecognized_value",
    "why_value_is_not_recognized_or_realized",
    "complementary_actor_hypothesis",
    "complementary_actor_state",
    "transformation_mechanism",
    "why_exchange_does_not_already_happen",
    "incremental_value_for_origin_actor",
    "incremental_value_for_complementary_actor",
    "orchestrator_value_capture_hypothesis",
    "cheapest_decisive_validation",
    "kill_conditions",
    "surface_phenomenon_or_friction",
    "latent_outcome_hypothesis",
    "structural_friction_hypothesis",
    "connection_pressure_hypothesis",
    "observed_missing_edge",
    "latent_connection_hypothesis",
)

_VALIDATION_EVIDENCE_KINDS = frozenset(
    {
        EvidenceKind.ORIGIN_STATE,
        EvidenceKind.STRUCTURAL_FRICTION,
        EvidenceKind.COMPLEMENTARY_STATE,
        EvidenceKind.CONNECTION_PRESSURE,
    }
)


def _canonical_evidence_kind(kind: EvidenceKind) -> EvidenceKind:
    # Compatibility-only legacy label. Canonical ontology uses MISSING_EDGE.
    if kind is EvidenceKind.STRANDING_BARRIER:
        return EvidenceKind.MISSING_EDGE
    return kind


def evidence_kinds(candidate: LatentValueCandidate) -> set[EvidenceKind]:
    return {
        _canonical_evidence_kind(item.kind)
        for item in candidate.evidence
        if item.is_usable()
    }


def missing_validation_evidence(candidate: LatentValueCandidate) -> list[EvidenceKind]:
    """Evidence dimensions still missing before a candidate is field-test ready."""

    present = evidence_kinds(candidate)
    missing = set(_VALIDATION_EVIDENCE_KINDS - present)
    if EvidenceKind.MISSING_EDGE not in present:
        missing.add(EvidenceKind.MISSING_EDGE)
    return sorted(missing, key=lambda item: item.value)


def _causal_projection_errors(
    *,
    actor: str,
    current_state: str,
    surface_phenomenon: str,
    latent_outcome_hypothesis: str,
    structural_friction_hypothesis: str,
    causal_descent: CausalDescentRecord | None,
    causal_descent_record_id: str = "",
    causal_stop_reason: str = "",
    available_evidence_refs: set[str] | None = None,
) -> list[str]:
    """Require promotable causal lineage, not an ID or narrative summary."""

    if causal_descent is None:
        return ["missing:causal_descent"]

    errors = [
        f"causal_descent:{error}"
        for error in validate_causal_descent_for_promotion(causal_descent)
    ]
    errors.extend(
        validate_causal_projection(
            causal_descent,
            actor=actor,
            current_state=current_state,
            surface_phenomenon=surface_phenomenon,
            latent_outcome_hypothesis=latent_outcome_hypothesis,
            structural_friction_hypothesis=structural_friction_hypothesis,
            record_id=causal_descent_record_id,
            stop_reason=causal_stop_reason,
        )
    )
    if available_evidence_refs is not None:
        for ref in unbound_causal_evidence_refs(
            causal_descent,
            available_evidence_refs,
        ):
            errors.append(f"causal_descent:unbound_evidence_ref:{ref}")
    return errors


def validate_candidate(candidate: LatentValueCandidate) -> list[str]:
    """Return fail-closed validation errors for a core discovery candidate."""

    errors: list[str] = []
    for name in _REQUIRED_FIELDS:
        value = getattr(candidate, name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing:{name}")

    if not (
        candidate.observed_change.strip()
        or candidate.persistent_mismatch.strip()
    ):
        errors.append("missing:observed_change_or_persistent_mismatch")

    usable_evidence = [item for item in candidate.evidence if item.is_usable()]
    if not usable_evidence:
        errors.append("missing:evidence")

    if candidate.candidate_class() is CandidateClass.EXPLICIT_DEMAND_EXECUTION:
        errors.append("explicit_demand_execution_is_not_core_latent_value_discovery")

    if candidate.structural_friction_truth_state != "EVIDENCED_STRUCTURE":
        errors.append("structural_friction_not_evidenced")

    if any(
        not isinstance(value, str) or not value.strip()
        for value in candidate.alternative_explanations
    ):
        errors.append("invalid:alternative_explanations")

    errors.extend(
        _causal_projection_errors(
            actor=candidate.actor,
            current_state=candidate.observed_state,
            surface_phenomenon=candidate.surface_phenomenon_or_friction,
            latent_outcome_hypothesis=candidate.latent_outcome_hypothesis,
            structural_friction_hypothesis=candidate.structural_friction_hypothesis,
            causal_descent=candidate.causal_descent,
            causal_descent_record_id=candidate.causal_descent_record_id,
            causal_stop_reason=candidate.causal_stop_reason,
            available_evidence_refs={
                item.source_id
                for item in candidate.evidence
                if item.is_usable()
            },
        )
    )

    if (
        candidate.hidden_or_underrecognized_value.strip()
        == candidate.complementary_actor_state.strip()
        and candidate.hidden_or_underrecognized_value.strip()
    ):
        errors.append("origin_value_and_complementary_state_must_be_distinct")

    for kind in missing_validation_evidence(candidate):
        errors.append(f"missing:evidence_kind:{kind.value}")

    return errors


def discovery_state(candidate: LatentValueCandidate) -> DiscoveryState:
    """Infer discovery maturity without promoting commercial truth."""

    usable = [item for item in candidate.evidence if item.is_usable()]
    if not usable:
        return DiscoveryState.OBSERVED_PATTERN

    if not candidate.hidden_or_underrecognized_value.strip():
        return DiscoveryState.OBSERVED_PATTERN

    if not (
        candidate.surface_phenomenon_or_friction.strip()
        and candidate.latent_outcome_hypothesis.strip()
        and candidate.structural_friction_hypothesis.strip()
        and candidate.structural_friction_truth_state == "EVIDENCED_STRUCTURE"
        and EvidenceKind.STRUCTURAL_FRICTION in evidence_kinds(candidate)
        and not _causal_projection_errors(
            actor=candidate.actor,
            current_state=candidate.observed_state,
            surface_phenomenon=candidate.surface_phenomenon_or_friction,
            latent_outcome_hypothesis=candidate.latent_outcome_hypothesis,
            structural_friction_hypothesis=candidate.structural_friction_hypothesis,
            causal_descent=candidate.causal_descent,
            causal_descent_record_id=candidate.causal_descent_record_id,
            causal_stop_reason=candidate.causal_stop_reason,
            available_evidence_refs={
                item.source_id
                for item in candidate.evidence
                if item.is_usable()
            },
        )
    ):
        return DiscoveryState.STRUCTURAL_FRICTION_HYPOTHESIS

    if not candidate.complementary_actor_hypothesis.strip():
        return DiscoveryState.LATENT_VALUE_HYPOTHESIS

    kinds = evidence_kinds(candidate)
    if not (
        candidate.connection_pressure_hypothesis.strip()
        and EvidenceKind.CONNECTION_PRESSURE in kinds
        and candidate.observed_missing_edge.strip()
        and {EvidenceKind.MISSING_EDGE, EvidenceKind.STRANDING_BARRIER}.intersection(kinds)
        and candidate.latent_connection_hypothesis.strip()
    ):
        return DiscoveryState.COMPLEMENTARITY_HYPOTHESIS

    if not (
        candidate.transformation_mechanism.strip()
        and candidate.why_exchange_does_not_already_happen.strip()
    ):
        return DiscoveryState.LATENT_CONNECTION_EVIDENCED

    if validate_candidate(candidate):
        return DiscoveryState.LATENT_CONNECTION_EVIDENCED

    return DiscoveryState.VALIDATION_READY


def _record_evidence_kinds(record: Mapping[str, object]) -> set[str]:
    raw = record.get("evidence")
    if not isinstance(raw, Iterable) or isinstance(raw, (str, bytes)):
        return set()

    kinds: set[str] = set()
    for item in raw:
        if isinstance(item, Mapping):
            kind = item.get("kind")
            source_id = item.get("source_id")
            claim = item.get("claim")
            if (
                isinstance(kind, str)
                and kind.strip()
                and isinstance(source_id, str)
                and source_id.strip()
                and isinstance(claim, str)
                and claim.strip()
            ):
                normalized = kind.strip()
                if normalized == "STRANDING_BARRIER":
                    normalized = "MISSING_EDGE"
                kinds.add(normalized)
    return kinds


def validate_candidate_record(record: Mapping[str, object]) -> list[str]:
    """Dictionary-schema guard for research outputs and generated artifacts."""

    errors: list[str] = []
    for name in _REQUIRED_FIELDS:
        value = record.get(name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing:{name}")

    observed_change = record.get("observed_change")
    persistent_mismatch = record.get("persistent_mismatch")
    if not (
        isinstance(observed_change, str) and observed_change.strip()
    ) and not (
        isinstance(persistent_mismatch, str) and persistent_mismatch.strip()
    ):
        errors.append("missing:observed_change_or_persistent_mismatch")

    evidence = record.get("evidence")
    if not isinstance(evidence, Iterable) or isinstance(evidence, (str, bytes)):
        errors.append("missing:evidence")
    else:
        evidence_items = list(evidence)
        if not evidence_items:
            errors.append("missing:evidence")

    if record.get("source_mode") == "EXPLICIT_DEMAND":
        errors.append("explicit_demand_execution_is_not_core_latent_value_discovery")

    if record.get("structural_friction_truth_state") != "EVIDENCED_STRUCTURE":
        errors.append("structural_friction_not_evidenced")

    alternatives = record.get("alternative_explanations", [])
    if not isinstance(alternatives, Iterable) or isinstance(alternatives, (str, bytes)):
        errors.append("invalid:alternative_explanations")
    elif any(
        not isinstance(value, str) or not value.strip()
        for value in alternatives
    ):
        errors.append("invalid:alternative_explanations")

    causal_descent: CausalDescentRecord | None = None
    raw_causal = record.get("causal_descent")
    if not isinstance(raw_causal, Mapping):
        errors.append("missing:causal_descent")
    else:
        try:
            causal_descent = causal_descent_from_mapping(raw_causal)
        except ValueError as exc:
            errors.append(f"invalid:causal_descent:{exc}")

    if causal_descent is not None:
        errors.extend(
            _causal_projection_errors(
                actor=str(record.get("actor") or ""),
                current_state=str(record.get("observed_state") or ""),
                surface_phenomenon=str(
                    record.get("surface_phenomenon_or_friction") or ""
                ),
                latent_outcome_hypothesis=str(
                    record.get("latent_outcome_hypothesis") or ""
                ),
                structural_friction_hypothesis=str(
                    record.get("structural_friction_hypothesis") or ""
                ),
                causal_descent=causal_descent,
                causal_descent_record_id=str(
                    record.get("causal_descent_record_id") or ""
                ),
                causal_stop_reason=str(record.get("causal_stop_reason") or ""),
                available_evidence_refs={
                    str(item.get("source_id") or "")
                    for item in record.get("evidence", [])
                    if isinstance(item, Mapping)
                    and str(item.get("source_id") or "").strip()
                },
            )
        )

    present_kinds = _record_evidence_kinds(record)
    for kind in sorted(_VALIDATION_EVIDENCE_KINDS, key=lambda item: item.value):
        if kind.value not in present_kinds:
            errors.append(f"missing:evidence_kind:{kind.value}")

    if "MISSING_EDGE" not in present_kinds:
        errors.append("missing:evidence_kind:MISSING_EDGE")

    return errors


GOVERNING_INVARIANTS = (
    "RESOURCE_LABEL_NOT_REQUIRED_FOR_VALUE_TO_EXIST",
    "RECENT_CHANGE_NE_UNIVERSAL_DISCOVERY_GATE",
    "PERSISTENT_STRUCTURAL_MISMATCH_MAY_BE_DISCOVERY_EVIDENCE",
    "DEMAND_LABEL_NOT_REQUIRED_FOR_DEFICIT_TO_EXIST",
    "SURFACE_FRICTION_NE_STRUCTURAL_FRICTION",
    "STRUCTURAL_FRICTION_HYPOTHESIS_NE_EVIDENCED_STRUCTURAL_FRICTION",
    "STRUCTURAL_FRICTION_NE_MISSING_EDGE",
    "CONNECTION_PRESSURE_NE_COMPLEMENTARITY",
    "MISSING_EDGE_NE_STRUCTURAL_FRICTION",
    "LEGACY_STRANDING_BARRIER_NORMALIZES_TO_MISSING_EDGE",
    "COUNTERFACTUAL_EXCHANGE_FOLLOWS_EVIDENCED_CONNECTION",
    "BUYER_COST_FIRST_NE_CONSTITUTION",
    "POTENTIAL_VALUE_NE_PROVEN_VALUE",
    "COMPLEMENTARITY_NE_TRANSACTIONABILITY",
    "CAUSAL_RECORD_ID_NE_CAUSAL_EVIDENCE",
    "CAUSAL_EVIDENCE_REF_MUST_BIND_TO_PERSISTED_EVIDENCE",
    "DENORMALIZED_CAUSAL_SUMMARY_MUST_MATCH_CAUSAL_LINEAGE",
    "NARRATIVE_COMPLETENESS_NE_EVIDENCE_COMPLETENESS",
    "EXPLICIT_DEMAND_EXECUTION_NE_CORE_LATENT_VALUE_DISCOVERY",
    "VALUE_DISCOVERY_PRECEDES_ORCHESTRATION",
    "UNKNOWN_NE_PASS",
)
