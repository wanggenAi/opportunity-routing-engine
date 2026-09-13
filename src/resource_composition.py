"""Evidence-preserving multi-actor resource composition hypotheses.

This module bridges capability discovery and transaction design. It answers only a
structural question: which minimal sets of actor-linked capability claims cover a
bounded RequirementBundle, and at what evidence/callability maturity?

It does not rank people, make employment/eligibility decisions, infer consent, or
claim that a composition is transaction-ready.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from itertools import combinations
from typing import Sequence

from src.capability_coverage import RequirementBundle
from src.live_resource_signals import CapabilityClaim, EvidenceStatus


class CompositionState(str, Enum):
    HYPOTHESIS_COMPOSED = "HYPOTHESIS_COMPOSED"
    DISCOVERED_COMPOSED = "DISCOVERED_COMPOSED"
    CALLABLE_COMPOSED = "CALLABLE_COMPOSED"


_EVIDENCE_RANK = {
    EvidenceStatus.INFERRED: 0,
    EvidenceStatus.OBSERVED: 1,
    EvidenceStatus.CONFIRMED: 2,
}


@dataclass(frozen=True)
class CapabilityContribution:
    capability_key: str
    actor_refs: tuple[str, ...]
    strongest_evidence_status: EvidenceStatus
    callable_actor_refs: tuple[str, ...]
    source_signal_ids: tuple[str, ...]


@dataclass(frozen=True)
class ResourceCompositionHypothesis:
    bundle_id: str
    actor_refs: tuple[str, ...]
    state: CompositionState
    contributions: tuple[CapabilityContribution, ...]
    source_signal_ids: tuple[str, ...]

    @property
    def is_multi_actor(self) -> bool:
        return len(self.actor_refs) > 1


def _geography_compatible(claim: CapabilityClaim, bundle: RequirementBundle) -> bool:
    if not bundle.geography.strip():
        return True
    return bool(
        claim.geography.strip()
        and claim.geography.strip() == bundle.geography.strip()
    )


def _relevant_claims(
    claims: Sequence[CapabilityClaim], bundle: RequirementBundle
) -> tuple[CapabilityClaim, ...]:
    required = {item.capability_key.strip() for item in bundle.required_capabilities}
    return tuple(
        claim
        for claim in claims
        if claim.actor_ref.strip()
        and claim.capability_key.strip() in required
        and _geography_compatible(claim, bundle)
    )


def _actor_capability_map(
    claims: Sequence[CapabilityClaim],
) -> dict[str, frozenset[str]]:
    result: dict[str, set[str]] = {}
    for claim in claims:
        result.setdefault(claim.actor_ref.strip(), set()).add(claim.capability_key.strip())
    return {actor: frozenset(keys) for actor, keys in result.items()}


def _covers(
    actors: Sequence[str],
    actor_capabilities: dict[str, frozenset[str]],
    required: frozenset[str],
) -> bool:
    covered: set[str] = set()
    for actor in actors:
        covered.update(actor_capabilities.get(actor, ()))
    return required.issubset(covered)


def _is_minimal_cover(
    actors: tuple[str, ...],
    actor_capabilities: dict[str, frozenset[str]],
    required: frozenset[str],
) -> bool:
    if not _covers(actors, actor_capabilities, required):
        return False
    if len(actors) == 1:
        return True
    return all(
        not _covers(
            tuple(candidate for candidate in actors if candidate != removed),
            actor_capabilities,
            required,
        )
        for removed in actors
    )


def _contribution(
    capability_key: str,
    selected_actors: tuple[str, ...],
    claims: Sequence[CapabilityClaim],
    *,
    as_of: datetime,
    max_age: timedelta,
) -> CapabilityContribution:
    supporting = tuple(
        claim
        for claim in claims
        if claim.actor_ref.strip() in selected_actors
        and claim.capability_key.strip() == capability_key
    )
    if not supporting:
        raise ValueError(f"composition is missing capability: {capability_key}")

    strongest = max(
        (claim.evidence_status for claim in supporting),
        key=lambda state: _EVIDENCE_RANK[state],
    )
    callable_actors = tuple(
        sorted(
            {
                claim.actor_ref.strip()
                for claim in supporting
                if claim.is_callable(as_of, max_age)
            }
        )
    )
    source_ids = tuple(
        sorted(
            {
                source_id
                for claim in supporting
                for source_id in claim.source_signal_ids
                if source_id.strip()
            }
        )
    )
    return CapabilityContribution(
        capability_key=capability_key,
        actor_refs=tuple(sorted({claim.actor_ref.strip() for claim in supporting})),
        strongest_evidence_status=strongest,
        callable_actor_refs=callable_actors,
        source_signal_ids=source_ids,
    )


def _composition_state(
    contributions: Sequence[CapabilityContribution],
) -> CompositionState:
    if all(item.callable_actor_refs for item in contributions):
        return CompositionState.CALLABLE_COMPOSED
    if all(
        item.strongest_evidence_status
        in {EvidenceStatus.OBSERVED, EvidenceStatus.CONFIRMED}
        for item in contributions
    ):
        return CompositionState.DISCOVERED_COMPOSED
    return CompositionState.HYPOTHESIS_COMPOSED


def generate_composition_hypotheses(
    claims: Sequence[CapabilityClaim],
    bundle: RequirementBundle,
    *,
    as_of: datetime | None = None,
    max_age: timedelta = timedelta(days=30),
    max_actors: int = 4,
    max_hypotheses: int = 100,
) -> tuple[ResourceCompositionHypothesis, ...]:
    """Generate deterministic minimal capability-cover compositions.

    Ordering is only for reproducibility: smaller actor sets first, then lexical actor
    ids. It is not a quality, suitability, employment, trust, or commercial ranking.
    """

    errors = bundle.validate()
    if errors:
        raise ValueError("invalid requirement bundle: " + ",".join(errors))
    if max_actors < 1:
        raise ValueError("max_actors must be at least 1")
    if max_hypotheses < 1:
        raise ValueError("max_hypotheses must be at least 1")
    if as_of is None:
        as_of = datetime.now(timezone.utc)
    if as_of.tzinfo is None:
        raise ValueError("as_of must be timezone-aware")
    if max_age < timedelta(0):
        raise ValueError("max_age must not be negative")

    relevant = _relevant_claims(claims, bundle)
    actor_capabilities = _actor_capability_map(relevant)
    actors = tuple(sorted(actor_capabilities))
    required = frozenset(
        item.capability_key.strip() for item in bundle.required_capabilities
    )

    results: list[ResourceCompositionHypothesis] = []
    upper = min(max_actors, len(actors))
    for size in range(1, upper + 1):
        for selected in combinations(actors, size):
            if not _is_minimal_cover(selected, actor_capabilities, required):
                continue

            contributions = tuple(
                _contribution(
                    capability_key,
                    selected,
                    relevant,
                    as_of=as_of,
                    max_age=max_age,
                )
                for capability_key in sorted(required)
            )
            source_ids = tuple(
                sorted(
                    {
                        source_id
                        for contribution in contributions
                        for source_id in contribution.source_signal_ids
                    }
                )
            )
            results.append(
                ResourceCompositionHypothesis(
                    bundle_id=bundle.bundle_id,
                    actor_refs=selected,
                    state=_composition_state(contributions),
                    contributions=contributions,
                    source_signal_ids=source_ids,
                )
            )
            if len(results) >= max_hypotheses:
                return tuple(results)

    return tuple(results)


GOVERNING_INVARIANTS = (
    "CAPABILITY_COMPOSITION_NE_PERSON_RANKING",
    "COMPOSITION_HYPOTHESIS_NE_EMPLOYMENT_DECISION",
    "HYPOTHESIS_COMPOSED_NE_DISCOVERED_COMPOSED",
    "DISCOVERED_COMPOSED_NE_CALLABLE_COMPOSED",
    "CALLABLE_COMPOSED_NE_COUNTERPARTY_CONSENT",
    "CALLABLE_COMPOSED_NE_TRANSACTIONABILITY",
    "COMPOSITION_NE_ACCESS_OR_BACKING",
    "MINIMAL_COVER_NE_BEST_ROUTE",
    "UNKNOWN_NE_PASS",
)
