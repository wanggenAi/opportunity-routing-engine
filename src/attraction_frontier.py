"""Pareto frontier for attraction-first discovery.

Attraction is multi-objective. Critical dimensions are deliberately non-compensatory:
a slightly stronger value jump should not erase weaker participant pull, a worse
decision window, or poorer operator control.

This module therefore uses Pareto dominance rather than a weighted total score to
allocate deep-discovery attention among profiles that have already passed the
HIGH_ATTRACTION_BEACON hard floor.

For the small candidate sets expected during a scan, the O(n^2) non-dominated sort is
preferred because it is transparent, deterministic, auditable, and simpler than more
complex skyline indexes. Replace it only when measured candidate volume justifies it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from src.attraction_discovery import (
    AttractionBeaconState,
    AttractionDiscoveryProfile,
    attraction_beacon_state,
    validate_attraction_profile,
)


PARETO_OBJECTIVES: tuple[str, ...] = (
    "a_voluntary_motion",
    "b_voluntary_motion",
    "state_dependent_value_jump",
    "decision_window",
    "bridge_compression",
    "activation_ease",
    "self_propulsion",
    "operator_control",
    "a_discoverability",
    "b_discoverability",
    "match_resolvability",
)


@dataclass(frozen=True)
class AttractionFrontierResult:
    eligible_signal_ids: tuple[str, ...]
    frontier_signal_ids: tuple[str, ...]
    dominance_layers: tuple[tuple[str, ...], ...]
    dominated_by: dict[str, tuple[str, ...]]
    excluded_signal_ids: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "method": "PARETO_NON_DOMINATED_SORT",
            "objectives": list(PARETO_OBJECTIVES),
            "eligible_signal_ids": list(self.eligible_signal_ids),
            "frontier_signal_ids": list(self.frontier_signal_ids),
            "dominance_layers": [list(layer) for layer in self.dominance_layers],
            "dominated_by": {
                signal_id: list(dominators)
                for signal_id, dominators in sorted(self.dominated_by.items())
            },
            "excluded_signal_ids": list(self.excluded_signal_ids),
            "truth_notes": [
                "Pareto position allocates discovery attention; it is not market validation.",
                "Only profiles already classified HIGH_ATTRACTION_BEACON may enter the frontier.",
                "No weighted total score may override a weak critical attraction dimension.",
                "Two distinct profiles with identical objective vectors may both remain non-dominated.",
            ],
        }


def attraction_vector(profile: AttractionDiscoveryProfile) -> tuple[int, ...]:
    errors = validate_attraction_profile(profile)
    if errors:
        raise ValueError(
            f"invalid attraction profile {profile.signal_id!r}: {', '.join(errors)}"
        )
    return tuple(int(getattr(profile, name)) for name in PARETO_OBJECTIVES)


def dominates(
    left: AttractionDiscoveryProfile,
    right: AttractionDiscoveryProfile,
) -> bool:
    """Return True when left is no worse everywhere and strictly better somewhere."""

    left_vector = attraction_vector(left)
    right_vector = attraction_vector(right)
    return all(a >= b for a, b in zip(left_vector, right_vector)) and any(
        a > b for a, b in zip(left_vector, right_vector)
    )


def _validate_unique_ids(
    profiles: Sequence[AttractionDiscoveryProfile],
) -> None:
    signal_ids = [profile.signal_id for profile in profiles]
    duplicates = sorted(
        signal_id
        for signal_id in set(signal_ids)
        if signal_ids.count(signal_id) > 1
    )
    if duplicates:
        raise ValueError(f"duplicate attraction signal ids: {duplicates}")


def _eligible(
    profiles: Sequence[AttractionDiscoveryProfile],
) -> tuple[list[AttractionDiscoveryProfile], list[AttractionDiscoveryProfile]]:
    eligible: list[AttractionDiscoveryProfile] = []
    excluded: list[AttractionDiscoveryProfile] = []
    for profile in profiles:
        if attraction_beacon_state(profile) is AttractionBeaconState.HIGH_ATTRACTION_BEACON:
            eligible.append(profile)
        else:
            excluded.append(profile)
    return eligible, excluded


def non_dominated_layers(
    profiles: Iterable[AttractionDiscoveryProfile],
) -> AttractionFrontierResult:
    """Return deterministic Pareto layers over high-attraction profiles.

    Layer 0 is the Pareto frontier. Layer 1 is the frontier after removing layer 0,
    and so on. These layers are attention tiers, not probability or commercial value
    rankings.
    """

    items = list(profiles)
    _validate_unique_ids(items)
    eligible, excluded = _eligible(items)

    remaining = {profile.signal_id: profile for profile in eligible}
    all_eligible = dict(remaining)
    layers: list[tuple[str, ...]] = []
    dominated_by: dict[str, tuple[str, ...]] = {}

    for signal_id, profile in sorted(all_eligible.items()):
        dominators = tuple(
            sorted(
                other_id
                for other_id, other in all_eligible.items()
                if other_id != signal_id and dominates(other, profile)
            )
        )
        dominated_by[signal_id] = dominators

    while remaining:
        current = tuple(
            sorted(
                signal_id
                for signal_id, profile in remaining.items()
                if not any(
                    other_id != signal_id and dominates(other, profile)
                    for other_id, other in remaining.items()
                )
            )
        )
        if not current:
            raise RuntimeError("Pareto sort made no progress")
        layers.append(current)
        for signal_id in current:
            del remaining[signal_id]

    frontier = layers[0] if layers else ()
    return AttractionFrontierResult(
        eligible_signal_ids=tuple(sorted(all_eligible)),
        frontier_signal_ids=frontier,
        dominance_layers=tuple(layers),
        dominated_by=dominated_by,
        excluded_signal_ids=tuple(sorted(profile.signal_id for profile in excluded)),
    )


def pareto_frontier(
    profiles: Iterable[AttractionDiscoveryProfile],
) -> tuple[str, ...]:
    return non_dominated_layers(profiles).frontier_signal_ids


GOVERNING_INVARIANTS = (
    "HARD_ATTRACTION_FLOOR_PRECEDES_PARETO",
    "PARETO_NE_MARKET_VALIDATION",
    "NON_COMPENSATORY_OBJECTIVES_NE_WEIGHTED_TOTAL_SCORE",
    "DOMINATED_SIGNAL_SHOULD_NOT_CONSUME_FIRST_DEEP_DIVE_ATTENTION",
    "IDENTICAL_NON_DOMINATED_VECTORS_MAY_COEXIST",
    "DISCOVERABILITY_AND_MATCH_RESOLVABILITY_ARE_NON_COMPENSATORY",
    "ALGORITHM_COMPLEXITY_MUST_BE_JUSTIFIED_BY_MEASURED_SCALE",
)
