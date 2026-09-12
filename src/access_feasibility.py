"""Fail-closed operator access and legitimacy model.

Commercial truth and operator accessibility are separate axes. A latent-value thesis can be
true while the current operator has no legitimate reason, route, trust or value packet that
would justify counterpart attention. This module prevents the engine from silently turning
"valuable actor exists" into "operator can contact and mobilize that actor".
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence


class AccessState(str, Enum):
    UNASSESSED = "UNASSESSED"
    ACCESS_BLOCKED = "ACCESS_BLOCKED"
    INTRODUCTION_READY = "INTRODUCTION_READY"
    ENGAGEMENT_READY = "ENGAGEMENT_READY"
    VALIDATION_ACCESS_READY = "VALIDATION_ACCESS_READY"


class AccessRouteKind(str, Enum):
    PUBLIC_INSTITUTIONAL_WINDOW = "PUBLIC_INSTITUTIONAL_WINDOW"
    AUTHORIZED_PROGRAM_OR_EVENT = "AUTHORIZED_PROGRAM_OR_EVENT"
    WARM_REFERRAL = "WARM_REFERRAL"
    PROFESSIONAL_ROLE = "PROFESSIONAL_ROLE"
    DIRECT_COLD = "DIRECT_COLD"


@dataclass(frozen=True)
class AccessEvidence:
    source_id: str
    claim: str

    def usable(self) -> bool:
        return bool(self.source_id.strip() and self.claim.strip())


@dataclass(frozen=True)
class AccessFeasibility:
    candidate_id: str
    target_actor: str
    route_kind: AccessRouteKind
    legitimate_entry_path: str
    counterparty_reason_to_engage: str
    first_value_packet: str
    institutional_cover_or_referral: str
    status_trust_friction: str
    operator_credibility_assets: str
    missing_credibility: str
    operator_commitment: str
    counterparty_commitment_requested: str
    founder_identity_dependency: str
    cultural_context_notes: str = ""
    evidence: Sequence[AccessEvidence] = field(default_factory=tuple)


_REQUIRED = (
    "candidate_id",
    "target_actor",
    "legitimate_entry_path",
    "counterparty_reason_to_engage",
    "first_value_packet",
    "status_trust_friction",
    "operator_commitment",
    "counterparty_commitment_requested",
    "founder_identity_dependency",
)


def validate_access(record: AccessFeasibility) -> list[str]:
    errors: list[str] = []
    for name in _REQUIRED:
        value = getattr(record, name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing:{name}")

    if not any(item.usable() for item in record.evidence):
        errors.append("missing:access_evidence")

    if record.route_kind is AccessRouteKind.DIRECT_COLD:
        if not record.first_value_packet.strip():
            errors.append("cold_access_without_value_packet")
        if not record.counterparty_reason_to_engage.strip():
            errors.append("cold_access_without_counterparty_reason")

    if record.counterparty_commitment_requested.strip().lower() in {
        "cooperate",
        "help me",
        "meet me",
        "合作",
        "帮我",
        "见我",
    }:
        errors.append("unbounded_counterparty_ask")

    return errors


def access_state(record: AccessFeasibility) -> AccessState:
    errors = validate_access(record)
    if errors:
        return AccessState.ACCESS_BLOCKED

    if not record.institutional_cover_or_referral.strip() and record.route_kind in {
        AccessRouteKind.PUBLIC_INSTITUTIONAL_WINDOW,
        AccessRouteKind.AUTHORIZED_PROGRAM_OR_EVENT,
        AccessRouteKind.WARM_REFERRAL,
        AccessRouteKind.PROFESSIONAL_ROLE,
    }:
        return AccessState.INTRODUCTION_READY

    if record.missing_credibility.strip():
        return AccessState.INTRODUCTION_READY

    if "unknown" in record.founder_identity_dependency.lower():
        return AccessState.ENGAGEMENT_READY

    return AccessState.VALIDATION_ACCESS_READY


ACCESS_INVARIANTS = (
    "VALUE_TRUTH_NE_OPERATOR_ACCESS",
    "PUBLIC_ACTOR_NE_ACCESSIBLE_ACTOR",
    "PERSONAL_CONFIDENCE_NE_COUNTERPARTY_REASON_TO_ENGAGE",
    "APPEARANCE_NE_CREDENTIAL",
    "MONEY_NE_ONLY_FORM_OF_RECIPROCITY",
    "INSTITUTIONAL_ROUTE_PREFERRED_OVER_STATUS_BLIND_COLD_OUTREACH",
    "LOCAL_CULTURAL_HYPOTHESIS_NE_UNIVERSAL_FACT",
    "ACCESS_BLOCKED_NE_BAD_OPPORTUNITY",
)
