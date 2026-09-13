"""Neutral live-signal model for discovering latent real-world capabilities.

Sensors observe public reality; they do not define strategy. Platform adapters must
normalize raw items into explicit facts/capability claims. Derived capabilities stay
INFERRED until independently confirmed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Mapping, Protocol, Sequence


class EvidenceStatus(str, Enum):
    INFERRED = "INFERRED"
    OBSERVED = "OBSERVED"
    CONFIRMED = "CONFIRMED"


class AvailabilityState(str, Enum):
    UNKNOWN = "UNKNOWN"
    ADVERTISED = "ADVERTISED"
    CONFIRMED = "CONFIRMED"
    COMMITTED = "COMMITTED"


class PermissionState(str, Enum):
    UNKNOWN = "UNKNOWN"
    ALLOWED = "ALLOWED"
    RESTRICTED = "RESTRICTED"


@dataclass(frozen=True)
class ObservedFact:
    key: str
    value: object
    evidence_text: str

    def is_usable(self) -> bool:
        return bool(self.key.strip() and self.evidence_text.strip())


@dataclass(frozen=True)
class ExplicitCapability:
    capability_key: str
    evidence_text: str

    def is_usable(self) -> bool:
        return bool(self.capability_key.strip() and self.evidence_text.strip())


@dataclass(frozen=True)
class SignalObservation:
    signal_id: str
    source_id: str
    observed_at: datetime
    actor_ref: str
    geography: str = ""
    raw_text: str = ""
    source_url: str = ""
    facts: Sequence[ObservedFact] = field(default_factory=tuple)
    explicit_capabilities: Sequence[ExplicitCapability] = field(default_factory=tuple)
    availability: AvailabilityState = AvailabilityState.UNKNOWN
    permission: PermissionState = PermissionState.UNKNOWN

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.signal_id.strip(): errors.append("missing:signal_id")
        if not self.source_id.strip(): errors.append("missing:source_id")
        if not self.actor_ref.strip(): errors.append("missing:actor_ref")
        if self.observed_at.tzinfo is None: errors.append("observed_at_must_be_timezone_aware")
        if not any(x.is_usable() for x in self.facts) and not any(x.is_usable() for x in self.explicit_capabilities):
            errors.append("missing:observable_content")
        return errors

    def fact_map(self) -> dict[str, object]:
        return {x.key: x.value for x in self.facts if x.is_usable()}


class SensorAdapter(Protocol):
    def normalize(self, raw: Mapping[str, object]) -> SignalObservation: ...


@dataclass(frozen=True)
class FactCondition:
    key: str
    expected_value: object = True


@dataclass(frozen=True)
class CapabilityInferenceRule:
    rule_id: str
    conditions: Sequence[FactCondition]
    capability_key: str
    rationale: str

    def matches(self, signal: SignalObservation) -> bool:
        facts = signal.fact_map()
        return bool(self.rule_id.strip() and self.capability_key.strip() and self.rationale.strip() and self.conditions and all(c.key.strip() and facts.get(c.key) == c.expected_value for c in self.conditions))


@dataclass(frozen=True)
class CapabilityClaim:
    actor_ref: str
    capability_key: str
    evidence_status: EvidenceStatus
    source_signal_ids: Sequence[str]
    rationale: str
    last_observed_at: datetime
    geography: str = ""
    availability: AvailabilityState = AvailabilityState.UNKNOWN
    permission: PermissionState = PermissionState.UNKNOWN
    inference_rule_id: str = ""

    def is_fresh(self, as_of: datetime, max_age: timedelta) -> bool:
        if as_of.tzinfo is None: raise ValueError("as_of must be timezone-aware")
        if self.last_observed_at.tzinfo is None: return False
        age = as_of - self.last_observed_at
        return timedelta(0) <= age <= max_age

    def is_callable(self, as_of: datetime, max_age: timedelta) -> bool:
        return self.evidence_status is EvidenceStatus.CONFIRMED and self.availability in {AvailabilityState.CONFIRMED, AvailabilityState.COMMITTED} and self.permission is PermissionState.ALLOWED and self.is_fresh(as_of, max_age)


def extract_capability_claims(signal: SignalObservation, rules: Sequence[CapabilityInferenceRule] = ()) -> list[CapabilityClaim]:
    if signal.validate(): return []
    claims: list[CapabilityClaim] = []
    for explicit in signal.explicit_capabilities:
        if explicit.is_usable():
            claims.append(CapabilityClaim(signal.actor_ref, explicit.capability_key.strip(), EvidenceStatus.OBSERVED, (signal.signal_id,), explicit.evidence_text.strip(), signal.observed_at, signal.geography, signal.availability, signal.permission))
    for rule in rules:
        if rule.matches(signal):
            claims.append(CapabilityClaim(signal.actor_ref, rule.capability_key.strip(), EvidenceStatus.INFERRED, (signal.signal_id,), rule.rationale.strip(), signal.observed_at, signal.geography, signal.availability, signal.permission, rule.rule_id.strip()))
    return claims


def confirm_capability(claim: CapabilityClaim, *, confirmation_signal_id: str, confirmed_at: datetime, availability: AvailabilityState, permission: PermissionState) -> CapabilityClaim:
    if not confirmation_signal_id.strip(): raise ValueError("confirmation_signal_id is required")
    if confirmed_at.tzinfo is None: raise ValueError("confirmed_at must be timezone-aware")
    return CapabilityClaim(claim.actor_ref, claim.capability_key, EvidenceStatus.CONFIRMED, tuple(claim.source_signal_ids) + (confirmation_signal_id.strip(),), claim.rationale, confirmed_at, claim.geography, availability, permission, claim.inference_rule_id)


GOVERNING_INVARIANTS = (
    "SENSOR_IS_OBSERVER_NOT_STRATEGY",
    "CAPABILITY_NAMESPACE_IS_OPEN_ENDED",
    "OBSERVED_FACT_NE_INFERRED_CAPABILITY",
    "INFERRED_CAPABILITY_NE_CONFIRMED_CAPABILITY",
    "ADVERTISED_NE_CONFIRMED_AVAILABLE",
    "CAPABILITY_EVIDENCE_NE_PERMISSION",
    "STALE_SIGNAL_NE_CURRENT_AVAILABILITY",
    "UNKNOWN_NE_PASS",
)
