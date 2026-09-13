"""Capability-bundle coverage for latent-resource composition.

This module evaluates whether a set of evidence-linked capability claims covers a
bounded capability requirement. It does not rank people, make employment decisions,
or declare a transaction ready. Coverage is only an input to later human-reviewed
resource composition.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Sequence

from src.live_resource_signals import CapabilityClaim, EvidenceStatus


class CoverageState(str, Enum):
    INCOMPLETE = "INCOMPLETE"
    HYPOTHESIS_COVERED = "HYPOTHESIS_COVERED"
    DISCOVERED_COVERED = "DISCOVERED_COVERED"
    CALLABLE_COVERED = "CALLABLE_COVERED"


@dataclass(frozen=True)
class CapabilityRequirement:
    capability_key: str


@dataclass(frozen=True)
class RequirementBundle:
    bundle_id: str
    required_capabilities: Sequence[CapabilityRequirement]
    geography: str = ""

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.bundle_id.strip(): errors.append("missing:bundle_id")
        keys = [x.capability_key.strip() for x in self.required_capabilities]
        if not keys or any(not key for key in keys): errors.append("missing:required_capabilities")
        if len(keys) != len(set(keys)): errors.append("duplicate:required_capabilities")
        return errors


@dataclass(frozen=True)
class CoverageResult:
    bundle_id: str
    state: CoverageState
    covered_capabilities: tuple[str, ...]
    inferred_only_capabilities: tuple[str, ...]
    missing_capabilities: tuple[str, ...]
    callable_capabilities: tuple[str, ...]


def _geography_compatible(claim: CapabilityClaim, bundle: RequirementBundle) -> bool:
    if not bundle.geography.strip(): return True
    return bool(claim.geography.strip() and claim.geography.strip() == bundle.geography.strip())


def evaluate_coverage(
    claims: Sequence[CapabilityClaim],
    bundle: RequirementBundle,
    *,
    as_of: datetime | None = None,
    max_age: timedelta = timedelta(days=30),
) -> CoverageResult:
    """Evaluate capability coverage without promoting it to transaction truth."""

    if bundle.validate(): raise ValueError("invalid requirement bundle")
    if as_of is None: as_of = datetime.now(timezone.utc)
    if as_of.tzinfo is None: raise ValueError("as_of must be timezone-aware")

    required = tuple(x.capability_key.strip() for x in bundle.required_capabilities)
    by_key: dict[str, list[CapabilityClaim]] = {}
    for claim in claims:
        if _geography_compatible(claim, bundle):
            by_key.setdefault(claim.capability_key, []).append(claim)

    covered = tuple(sorted(k for k in required if k in by_key))
    missing = tuple(sorted(k for k in required if k not in by_key))
    inferred_only = tuple(sorted(
        k for k in required if k in by_key and all(x.evidence_status is EvidenceStatus.INFERRED for x in by_key[k])
    ))
    callable_keys = tuple(sorted(
        k for k in required if k in by_key and any(x.is_callable(as_of, max_age) for x in by_key[k])
    ))

    if missing:
        state = CoverageState.INCOMPLETE
    elif len(callable_keys) == len(required):
        state = CoverageState.CALLABLE_COVERED
    elif all(any(x.evidence_status in {EvidenceStatus.OBSERVED, EvidenceStatus.CONFIRMED} for x in by_key[k]) for k in required):
        state = CoverageState.DISCOVERED_COVERED
    else:
        state = CoverageState.HYPOTHESIS_COVERED

    return CoverageResult(bundle.bundle_id, state, covered, inferred_only, missing, callable_keys)


GOVERNING_INVARIANTS = (
    "LOW_LEVEL_CAPABILITY_COVERAGE_NE_JOB_TITLE_MATCH",
    "HYPOTHESIS_COVERED_NE_DISCOVERED_COVERED",
    "DISCOVERED_COVERED_NE_CALLABLE_COVERED",
    "CALLABLE_COVERED_NE_TRANSACTIONABILITY",
    "NO_AUTOMATED_EMPLOYMENT_OR_ELIGIBILITY_DECISION",
    "UNKNOWN_NE_PASS",
)
