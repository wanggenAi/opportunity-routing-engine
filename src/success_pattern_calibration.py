"""Success-pattern calibration for attraction-first discovery.

Successful businesses are evidence about mechanisms that can work, not candidate
templates and never commercial proof for a new formation.  This module lets the
engine learn reusable structural motifs from independent precedents while preserving
the existing Attraction Field hard floors.

The key invariant is:

    PRECEDENT -> SEARCH PRIOR
    PRECEDENT != CANDIDATE EVIDENCE
    URGENCY -> MORE / BETTER SEARCH
    URGENCY != LOWER GATES
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import FrozenSet, Sequence

from src.attraction_discovery import (
    AttractionBeaconState,
    AttractionDiscoveryProfile,
    attraction_beacon_state,
)


class PrecedentEvidenceClass(str, Enum):
    OFFICIAL = "OFFICIAL"
    FOUNDER_INTERVIEW = "FOUNDER_INTERVIEW"
    CREDIBLE_SECONDARY = "CREDIBLE_SECONDARY"
    COMMUNITY_SELF_REPORT = "COMMUNITY_SELF_REPORT"


class CalibrationState(str, Enum):
    LOW_ATTRACTION_REJECT = "LOW_ATTRACTION_REJECT"
    INSUFFICIENT_PRECEDENT_SUPPORT = "INSUFFICIENT_PRECEDENT_SUPPORT"
    CALIBRATED_HIGH_ATTRACTION_SEARCH_DIRECTION = (
        "CALIBRATED_HIGH_ATTRACTION_SEARCH_DIRECTION"
    )


@dataclass(frozen=True)
class SuccessPrecedent:
    precedent_id: str
    source_url: str
    evidence_class: PrecedentEvidenceClass
    observed_result: str
    mechanisms: FrozenSet[str]
    transfer_claim: str
    anti_copy_warning: str
    negative_control: bool = False


@dataclass(frozen=True)
class SearchDirection:
    direction_id: str
    attraction_profile: AttractionDiscoveryProfile
    mechanisms: FrozenSet[str]


@dataclass(frozen=True)
class LaunchUrgencyPolicy:
    decision_deadline: date
    minimum_precedents_per_cycle: int = 8
    minimum_source_classes: int = 3
    minimum_independent_support_per_mechanism: int = 2


def validate_precedent(precedent: SuccessPrecedent) -> list[str]:
    errors: list[str] = []
    if not precedent.precedent_id.strip():
        errors.append("missing:precedent_id")
    if not precedent.source_url.startswith(("https://", "http://")):
        errors.append("invalid:source_url")
    if not precedent.observed_result.strip():
        errors.append("missing:observed_result")
    if not precedent.mechanisms:
        errors.append("missing:mechanisms")
    if not precedent.transfer_claim.strip():
        errors.append("missing:transfer_claim")
    if not precedent.anti_copy_warning.strip():
        errors.append("missing:anti_copy_warning")
    return errors


def precedent_cycle_is_broad_enough(
    precedents: Sequence[SuccessPrecedent], policy: LaunchUrgencyPolicy
) -> bool:
    valid = [p for p in precedents if not validate_precedent(p)]
    source_classes = {p.evidence_class for p in valid}
    return (
        len(valid) >= policy.minimum_precedents_per_cycle
        and len(source_classes) >= policy.minimum_source_classes
    )


def independently_supported_mechanisms(
    precedents: Sequence[SuccessPrecedent],
    minimum_independent_support: int = 2,
) -> frozenset[str]:
    support: dict[str, set[str]] = {}
    for precedent in precedents:
        if validate_precedent(precedent) or precedent.negative_control:
            continue
        for mechanism in precedent.mechanisms:
            support.setdefault(mechanism, set()).add(precedent.precedent_id)
    return frozenset(
        mechanism
        for mechanism, precedent_ids in support.items()
        if len(precedent_ids) >= minimum_independent_support
    )


def calibrate_search_direction(
    direction: SearchDirection,
    precedents: Sequence[SuccessPrecedent],
    policy: LaunchUrgencyPolicy,
) -> CalibrationState:
    # Precedents never override attraction.  A low-attraction direction stays dead
    # even if many famous companies used a superficially similar mechanism.
    if (
        attraction_beacon_state(direction.attraction_profile)
        is not AttractionBeaconState.HIGH_ATTRACTION_BEACON
    ):
        return CalibrationState.LOW_ATTRACTION_REJECT

    if not precedent_cycle_is_broad_enough(precedents, policy):
        return CalibrationState.INSUFFICIENT_PRECEDENT_SUPPORT

    supported = independently_supported_mechanisms(
        precedents,
        minimum_independent_support=policy.minimum_independent_support_per_mechanism,
    )
    if len(direction.mechanisms & supported) < 2:
        return CalibrationState.INSUFFICIENT_PRECEDENT_SUPPORT

    return CalibrationState.CALIBRATED_HIGH_ATTRACTION_SEARCH_DIRECTION


def high_attraction_experiment_allowed(
    profile: AttractionDiscoveryProfile,
    *,
    decisive_unknown: str,
    reversible: bool,
    founder_manufactured_demand: bool,
) -> bool:
    """Allow only a decisive cheap reality test on an already high-attraction field."""

    return (
        attraction_beacon_state(profile)
        is AttractionBeaconState.HIGH_ATTRACTION_BEACON
        and bool(decisive_unknown.strip())
        and reversible
        and not founder_manufactured_demand
    )


def deadline_response(
    policy: LaunchUrgencyPolicy,
    *,
    as_of: date,
    retained_high_attraction_formations: int,
) -> str:
    """Urgency changes search behavior, never the commercial truth threshold."""

    if as_of <= policy.decision_deadline:
        return "CONTINUE_CALIBRATED_HIGH_BREADTH_SEARCH"
    if retained_high_attraction_formations > 0:
        return "VALIDATE_ONLY_EXISTING_HIGH_ATTRACTION_SURVIVORS"
    return "EXPAND_SOURCE_UNIVERSE_AND_MECHANISM_DIVERSITY_DO_NOT_RELAX_GATES"
