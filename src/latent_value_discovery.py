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


class CandidateClass(str, Enum):
    """Architectural class of a discovered commercial hypothesis."""

    LATENT_VALUE_ACTIVATION = "LATENT_VALUE_ACTIVATION"
    EXPLICIT_DEMAND_EXECUTION = "EXPLICIT_DEMAND_EXECUTION"


class DiscoveryState(str, Enum):
    """Evidence maturity inside the latent-value discovery layer."""

    OBSERVED_PATTERN = "OBSERVED_PATTERN"
    LATENT_VALUE_HYPOTHESIS = "LATENT_VALUE_HYPOTHESIS"
    COMPLEMENTARITY_HYPOTHESIS = "COMPLEMENTARITY_HYPOTHESIS"
    VALIDATION_READY = "VALIDATION_READY"


class EvidenceKind(str, Enum):
    """What a source actually supports.

    These labels prevent a single macro article from silently supporting every leg of
    a latent-value story.
    """

    ORIGIN_STATE = "ORIGIN_STATE"
    ORIGIN_CHANGE = "ORIGIN_CHANGE"
    COMPLEMENTARY_STATE = "COMPLEMENTARY_STATE"
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
    "observed_change",
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
)

_VALIDATION_EVIDENCE_KINDS = frozenset(
    {
        EvidenceKind.ORIGIN_STATE,
        EvidenceKind.COMPLEMENTARY_STATE,
        EvidenceKind.STRANDING_BARRIER,
    }
)


def evidence_kinds(candidate: LatentValueCandidate) -> set[EvidenceKind]:
    return {item.kind for item in candidate.evidence if item.is_usable()}


def missing_validation_evidence(candidate: LatentValueCandidate) -> list[EvidenceKind]:
    """Evidence dimensions still missing before a candidate is field-test ready."""

    present = evidence_kinds(candidate)
    return sorted(_VALIDATION_EVIDENCE_KINDS - present, key=lambda item: item.value)


def validate_candidate(candidate: LatentValueCandidate) -> list[str]:
    """Return fail-closed validation errors for a core discovery candidate."""

    errors: list[str] = []
    for name in _REQUIRED_FIELDS:
        value = getattr(candidate, name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing:{name}")

    usable_evidence = [item for item in candidate.evidence if item.is_usable()]
    if not usable_evidence:
        errors.append("missing:evidence")

    if candidate.candidate_class() is CandidateClass.EXPLICIT_DEMAND_EXECUTION:
        errors.append("explicit_demand_execution_is_not_core_latent_value_discovery")

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
        candidate.complementary_actor_hypothesis.strip()
        and candidate.transformation_mechanism.strip()
        and candidate.why_exchange_does_not_already_happen.strip()
    ):
        return DiscoveryState.LATENT_VALUE_HYPOTHESIS

    if validate_candidate(candidate):
        return DiscoveryState.COMPLEMENTARITY_HYPOTHESIS

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
                kinds.add(kind.strip())
    return kinds


def validate_candidate_record(record: Mapping[str, object]) -> list[str]:
    """Dictionary-schema guard for research outputs and generated artifacts."""

    errors: list[str] = []
    for name in _REQUIRED_FIELDS:
        value = record.get(name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing:{name}")

    evidence = record.get("evidence")
    if not isinstance(evidence, Iterable) or isinstance(evidence, (str, bytes)):
        errors.append("missing:evidence")
    else:
        evidence_items = list(evidence)
        if not evidence_items:
            errors.append("missing:evidence")

    if record.get("source_mode") == "EXPLICIT_DEMAND":
        errors.append("explicit_demand_execution_is_not_core_latent_value_discovery")

    present_kinds = _record_evidence_kinds(record)
    for kind in sorted(_VALIDATION_EVIDENCE_KINDS, key=lambda item: item.value):
        if kind.value not in present_kinds:
            errors.append(f"missing:evidence_kind:{kind.value}")

    return errors


GOVERNING_INVARIANTS = (
    "RESOURCE_LABEL_NOT_REQUIRED_FOR_VALUE_TO_EXIST",
    "DEMAND_LABEL_NOT_REQUIRED_FOR_DEFICIT_TO_EXIST",
    "POTENTIAL_VALUE_NE_PROVEN_VALUE",
    "COMPLEMENTARITY_NE_TRANSACTIONABILITY",
    "NARRATIVE_COMPLETENESS_NE_EVIDENCE_COMPLETENESS",
    "EXPLICIT_DEMAND_EXECUTION_NE_CORE_LATENT_VALUE_DISCOVERY",
    "VALUE_DISCOVERY_PRECEDES_ORCHESTRATION",
    "UNKNOWN_NE_PASS",
)
