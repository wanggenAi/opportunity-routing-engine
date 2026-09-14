"""Evidence-gated recurrence detection over current Observation Fabric identities.

This module implements the canonical ``OBSERVED_PATTERN`` discovery state from
``docs/DISCOVERY_ENGINE.md``.  It detects exact repeated semantic structures; it
does not infer latent value, demand, payer, opportunity, monetization, or a
regenerative business loop.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Iterable

from src.observation_fabric import ObservationEnvelope


PATTERN_SCHEMA_VERSION = "observed-pattern.v1"
PATTERN_STATES = frozenset({"UNBOUND", "OBSERVED_PATTERN"})
ORDERING_BASIS = "EVIDENCE_RECURRENCE_ONLY_NOT_COMMERCIAL_RANKING"
BUSINESS_PROMOTION = "NOT_PROMOTED"
DOWNSTREAM_UNKNOWNS = (
    "LATENT_VALUE_NOT_ESTABLISHED",
    "COMPLEMENTARY_ACTOR_NOT_ESTABLISHED",
    "TRANSFORMATION_MECHANISM_NOT_ESTABLISHED",
    "REGENERATING_EVENT_FLOW_NOT_ESTABLISHED",
    "PAYER_NOT_ESTABLISHED",
    "REPEAT_MONETIZATION_NOT_ESTABLISHED",
    "COMPOUNDING_NOT_ESTABLISHED",
)


@dataclass(frozen=True)
class PatternGate:
    """Operational recurrence threshold, never a commercial-truth threshold."""

    min_observations: int = 3
    min_actors: int = 2
    min_periods: int = 2
    min_sources: int = 1

    def __post_init__(self) -> None:
        for name, value in asdict(self).items():
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise ValueError(f"{name} must be an integer >= 1")


@dataclass(frozen=True)
class ObservedPattern:
    pattern_id: str
    state: str
    primitive: str
    concept: str
    geography: str
    observation_count: int
    actor_count: int
    source_count: int
    period_count: int
    observed_claim_count: int
    epistemic_counts: dict[str, int]
    first_observed_at: str | None
    last_observed_at: str | None
    supporting_observation_refs: tuple[str, ...]
    supporting_claim_refs: tuple[str, ...]
    supporting_actor_ids: tuple[str, ...]
    supporting_source_ids: tuple[str, ...]
    supporting_periods: tuple[str, ...]
    missing_pattern_evidence: tuple[str, ...]
    evidence_cautions: tuple[str, ...]
    business_promotion: str = BUSINESS_PROMOTION
    downstream_unknowns: tuple[str, ...] = DOWNSTREAM_UNKNOWNS
    schema_version: str = PATTERN_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.state not in PATTERN_STATES:
            raise ValueError(f"unsupported pattern state: {self.state}")
        if self.business_promotion != BUSINESS_PROMOTION:
            raise ValueError("ObservedPattern cannot promote commercial truth")
        if not self.pattern_id or not self.primitive or not self.concept or not self.geography:
            raise ValueError("pattern identity fields are required")

    def as_dict(self) -> dict:
        return asdict(self)


def _date_key(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("observation time must be timezone-aware")
    return parsed.date().isoformat()


def _pattern_id(primitive: str, concept: str, geography: str) -> str:
    payload = json.dumps(
        [primitive, concept, geography],
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return "pattern-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]


def _claim_geography(envelope: ObservationEnvelope, claim) -> str:
    if claim.geography:
        return claim.geography
    if len(envelope.relevance_geographies) == 1:
        return envelope.relevance_geographies[0]
    return "UNSPECIFIED"


def _claim_actor(envelope: ObservationEnvelope, claim) -> str | None:
    if claim.actor_id:
        return claim.actor_id
    if len(envelope.actor_ids) == 1:
        return envelope.actor_ids[0]
    return None


def build_observed_patterns(
    envelopes: Iterable[ObservationEnvelope],
    *,
    gate: PatternGate | None = None,
) -> tuple[ObservedPattern, ...]:
    """Build exact evidence-recurrence groups from current observation identities.

    The caller should pass current Observation Fabric identities, not historical
    revisions.  The function still deduplicates by ``(source_id, observation_id)``
    inside each exact ``(primitive, concept, geography)`` group so multiple claims
    or accidental duplicate inputs cannot manufacture recurrence.

    Only direct ``OBSERVED`` claims satisfy recurrence gates. ``REPORTED`` and
    ``INFERRED`` claims remain visible in epistemic counts but cannot promote a
    group into ``OBSERVED_PATTERN``.
    """

    active_gate = gate or PatternGate()
    groups: dict[tuple[str, str, str], dict] = defaultdict(
        lambda: {
            "epistemic_counts": Counter(),
            "observation_refs": set(),
            "claim_refs": set(),
            "actors": set(),
            "sources": set(),
            "periods": set(),
            "observed_times": [],
            "observed_claim_count": 0,
        }
    )

    for envelope in envelopes:
        for claim in envelope.claims:
            geography = _claim_geography(envelope, claim)
            key = (claim.primitive, claim.concept, geography)
            group = groups[key]
            group["epistemic_counts"][claim.epistemic_status] += 1
            if claim.epistemic_status != "OBSERVED":
                continue

            observation_ref = f"{envelope.source_id}::{envelope.observation_id}"
            claim_ref = f"{observation_ref}::{claim.claim_id}"
            group["observation_refs"].add(observation_ref)
            group["claim_refs"].add(claim_ref)
            group["sources"].add(envelope.source_id)
            group["periods"].add(_date_key(envelope.observed_at))
            group["observed_times"].append(envelope.observed_at)
            group["observed_claim_count"] += 1
            actor_id = _claim_actor(envelope, claim)
            if actor_id:
                group["actors"].add(actor_id)

    patterns: list[ObservedPattern] = []
    for (primitive, concept, geography), group in groups.items():
        observation_count = len(group["observation_refs"])
        actor_count = len(group["actors"])
        source_count = len(group["sources"])
        period_count = len(group["periods"])

        missing: list[str] = []
        if observation_count < active_gate.min_observations:
            missing.append("INSUFFICIENT_OBSERVATION_RECURRENCE")
        if actor_count < active_gate.min_actors:
            missing.append("INSUFFICIENT_ACTOR_DIVERSITY")
        if period_count < active_gate.min_periods:
            missing.append("INSUFFICIENT_TIME_PERSISTENCE")
        if source_count < active_gate.min_sources:
            missing.append("INSUFFICIENT_SOURCE_DIVERSITY")

        cautions: list[str] = []
        if source_count == 1:
            cautions.append("SINGLE_SOURCE_ONLY")
        if group["epistemic_counts"].get("REPORTED", 0):
            cautions.append("REPORTED_CLAIMS_EXCLUDED_FROM_PATTERN_GATE")
        if group["epistemic_counts"].get("INFERRED", 0):
            cautions.append("INFERRED_CLAIMS_EXCLUDED_FROM_PATTERN_GATE")

        state = "OBSERVED_PATTERN" if observation_count > 0 and not missing else "UNBOUND"
        observed_times = sorted(group["observed_times"])
        patterns.append(
            ObservedPattern(
                pattern_id=_pattern_id(primitive, concept, geography),
                state=state,
                primitive=primitive,
                concept=concept,
                geography=geography,
                observation_count=observation_count,
                actor_count=actor_count,
                source_count=source_count,
                period_count=period_count,
                observed_claim_count=group["observed_claim_count"],
                epistemic_counts=dict(sorted(group["epistemic_counts"].items())),
                first_observed_at=observed_times[0] if observed_times else None,
                last_observed_at=observed_times[-1] if observed_times else None,
                supporting_observation_refs=tuple(sorted(group["observation_refs"])),
                supporting_claim_refs=tuple(sorted(group["claim_refs"])),
                supporting_actor_ids=tuple(sorted(group["actors"])),
                supporting_source_ids=tuple(sorted(group["sources"])),
                supporting_periods=tuple(sorted(group["periods"])),
                missing_pattern_evidence=tuple(missing),
                evidence_cautions=tuple(cautions),
            )
        )

    # Evidence recurrence ordering is an operator convenience only. It is not a
    # commercial ranking and cannot change pattern state.
    patterns.sort(
        key=lambda item: (
            item.state != "OBSERVED_PATTERN",
            -item.observation_count,
            -item.actor_count,
            -item.period_count,
            item.primitive,
            item.concept,
            item.geography,
        )
    )
    return tuple(patterns)


def summarize_observed_patterns(
    envelopes: Iterable[ObservationEnvelope],
    *,
    gate: PatternGate | None = None,
    source_observation_run_id: int | None = None,
) -> dict:
    current = tuple(envelopes)
    active_gate = gate or PatternGate()
    patterns = build_observed_patterns(current, gate=active_gate)
    state_counts = Counter(item.state for item in patterns)
    return {
        "schema_version": PATTERN_SCHEMA_VERSION,
        "ordering_basis": ORDERING_BASIS,
        "pattern_gate": asdict(active_gate),
        "pattern_gate_semantics": "OPERATIONAL_EVIDENCE_THRESHOLD_NOT_COMMERCIAL_TRUTH",
        "input_current_observation_count": len(current),
        "source_observation_run_id": source_observation_run_id,
        "pattern_count": len(patterns),
        "observed_pattern_count": state_counts.get("OBSERVED_PATTERN", 0),
        "unbound_pattern_count": state_counts.get("UNBOUND", 0),
        "state_counts": dict(sorted(state_counts.items())),
        "business_promotion": BUSINESS_PROMOTION,
        "patterns": [item.as_dict() for item in patterns],
        "governing_invariants": [
            "CURRENT_IDENTITY_ONLY_NOT_HISTORY_EVENT_COUNT",
            "EXACT_SEMANTIC_KEY_NO_LLM_MERGE",
            "OBSERVED_ONLY_CAN_SATISFY_PATTERN_GATE",
            "PATTERN_NE_LATENT_VALUE",
            "PATTERN_NE_DEMAND",
            "PATTERN_NE_PAYER",
            "PATTERN_NE_OPPORTUNITY",
            "PATTERN_NE_REGENERATIVE_LOOP",
            "UNKNOWN_NE_PASS",
        ],
    }
