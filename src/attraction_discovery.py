"""Attraction-first discovery beacon.

The engine should not begin by collecting every real friction and only later ask
whether anyone cares. It should preferentially search where reality already shows
voluntary energy and a large state-dependent value jump.

This module is an attention allocator, not commercial proof. It decides whether a
reality pattern deserves expensive causal descent and external validation effort.
Evidence remains mandatory; a clever story cannot create attraction.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from math import prod
from typing import Sequence


class AttractionBeaconState(str, Enum):
    UNASSESSED = "UNASSESSED"
    LOW_ATTRACTION = "LOW_ATTRACTION"
    RESEARCH_ONLY = "RESEARCH_ONLY"
    HIGH_ATTRACTION_BEACON = "HIGH_ATTRACTION_BEACON"


@dataclass(frozen=True)
class AttractionEvidence:
    source_id: str
    claim: str

    def is_usable(self) -> bool:
        return bool(self.source_id.strip() and self.claim.strip())


@dataclass(frozen=True)
class AttractionDiscoveryProfile:
    """Pre-formation evidence for where the engine should spend discovery attention.

    Scores are ordinal evidence states, not market-size estimates:
      0 = absent/contradicted
      1 = weak/inferred
      2 = observable/material
      3 = intense/repeated/direct

    HIGH_ATTRACTION_BEACON is weakest-link dominated. Large upside cannot compensate
    for a dead participant side, a locked decision window or founder labor.
    """

    signal_id: str
    reality_pattern: str
    a_actor: str
    b_actor: str
    candidate_bridge: str

    a_voluntary_motion: int
    b_voluntary_motion: int
    state_dependent_value_jump: int
    decision_window: int
    bridge_compression: int
    activation_ease: int
    self_propulsion: int
    operator_control: int

    a_motion_evidence: Sequence[AttractionEvidence] = field(default_factory=tuple)
    b_motion_evidence: Sequence[AttractionEvidence] = field(default_factory=tuple)
    value_jump_evidence: Sequence[AttractionEvidence] = field(default_factory=tuple)
    decision_window_evidence: Sequence[AttractionEvidence] = field(default_factory=tuple)
    bridge_compression_evidence: Sequence[AttractionEvidence] = field(default_factory=tuple)
    activation_evidence: Sequence[AttractionEvidence] = field(default_factory=tuple)
    self_propulsion_evidence: Sequence[AttractionEvidence] = field(default_factory=tuple)
    operator_control_evidence: Sequence[AttractionEvidence] = field(default_factory=tuple)

    founder_delivery_required: bool = False
    founder_sales_required_per_transaction: bool = False
    explanation_burden_high: bool = False


_SCORE_EVIDENCE = {
    "a_voluntary_motion": "a_motion_evidence",
    "b_voluntary_motion": "b_motion_evidence",
    "state_dependent_value_jump": "value_jump_evidence",
    "decision_window": "decision_window_evidence",
    "bridge_compression": "bridge_compression_evidence",
    "activation_ease": "activation_evidence",
    "self_propulsion": "self_propulsion_evidence",
    "operator_control": "operator_control_evidence",
}


def _usable(items: Sequence[AttractionEvidence]) -> bool:
    return any(item.is_usable() for item in items)


def validate_attraction_profile(profile: AttractionDiscoveryProfile) -> list[str]:
    errors: list[str] = []

    for name in ("signal_id", "reality_pattern", "a_actor", "b_actor", "candidate_bridge"):
        if not str(getattr(profile, name)).strip():
            errors.append(f"missing:{name}")

    for score_name, evidence_name in _SCORE_EVIDENCE.items():
        value = getattr(profile, score_name)
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 3:
            errors.append(f"invalid:{score_name}")
            continue
        if value > 0 and not _usable(getattr(profile, evidence_name)):
            errors.append(f"missing_evidence:{score_name}")

    return errors


def attraction_beacon_index(profile: AttractionDiscoveryProfile) -> float:
    """0-100 geometric diagnostic; never used to override hard floors."""

    if validate_attraction_profile(profile):
        return 0.0
    values = tuple(getattr(profile, name) for name in _SCORE_EVIDENCE)
    return round((prod(value / 3 for value in values) ** (1 / len(values))) * 100, 2)


def attraction_beacon_state(profile: AttractionDiscoveryProfile) -> AttractionBeaconState:
    if validate_attraction_profile(profile):
        return AttractionBeaconState.UNASSESSED

    core = (
        profile.a_voluntary_motion,
        profile.b_voluntary_motion,
        profile.state_dependent_value_jump,
        profile.decision_window,
        profile.bridge_compression,
        profile.activation_ease,
        profile.operator_control,
    )

    # Immediate kills: no bilateral motion, value already locked, tiny state jump,
    # or a bridge whose value is recurring founder labor/sales.
    if (
        profile.a_voluntary_motion <= 1
        or profile.b_voluntary_motion <= 1
        or profile.state_dependent_value_jump <= 1
        or profile.decision_window <= 1
        or profile.bridge_compression <= 1
        or profile.operator_control <= 1
        or profile.founder_delivery_required
        or profile.founder_sales_required_per_transaction
        or profile.explanation_burden_high
    ):
        return AttractionBeaconState.LOW_ATTRACTION

    # Strong attraction means no critical side needs to be pushed and the bridge
    # releases a legible value jump while decisions are still movable.
    if all(value >= 2 for value in core) and profile.self_propulsion >= 2:
        return AttractionBeaconState.HIGH_ATTRACTION_BEACON

    return AttractionBeaconState.RESEARCH_ONLY


def discovery_attention_allowed(profile: AttractionDiscoveryProfile) -> bool:
    """Whether the signal deserves deep causal/connection investigation now."""

    return attraction_beacon_state(profile) is AttractionBeaconState.HIGH_ATTRACTION_BEACON


def attraction_beacon_summary(profile: AttractionDiscoveryProfile) -> dict[str, object]:
    return {
        **asdict(profile),
        "beacon_state": attraction_beacon_state(profile).value,
        "beacon_index": attraction_beacon_index(profile),
        "discovery_attention_allowed": discovery_attention_allowed(profile),
        "governing_invariants": [
            "ATTRACTION_GUIDES_WHERE_DISCOVERY_LOOKS_FIRST",
            "REAL_FRICTION_NE_ATTRACTIVE_POSITION",
            "BILATERAL_VOLUNTARY_MOTION_REQUIRED",
            "STATE_DEPENDENT_VALUE_JUMP_REQUIRED",
            "DECISION_WINDOW_MUST_STILL_BE_MOVABLE",
            "NARROW_BRIDGE_SHOULD_UNLOCK_DISPROPORTIONATE_VALUE",
            "WEAKEST_LINK_DOMINATES",
            "FOUNDER_LABOR_NE_OPERATOR_CONTROL",
            "CLEVER_STORY_NE_PARTICIPANT_PULL",
            "HIGH_ATTRACTION_NE_MARKET_VALIDATION",
        ],
    }
