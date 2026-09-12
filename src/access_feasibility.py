"""Fail-closed operator endowment, access, backing and visible-surplus model.

Commercial truth, current operator accessibility, and counterpart-visible surplus are separate
axes. A latent-value thesis can be true while the operator has no legitimate route to the
actor. A legitimate route can exist while the actor still has no concrete reason to engage.

Supporting analysis or presentation artifacts are subordinate. They do not substitute for real
backing, trusted entry, or a counterpart benefit the actor can understand and believe.
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
    COMMITTED_COMPLEMENTARY_ACTOR = "COMMITTED_COMPLEMENTARY_ACTOR"
    DIRECT_COLD = "DIRECT_COLD"


class OperatorFitState(str, Enum):
    UNASSESSED = "UNASSESSED"
    THIN = "THIN"
    CONTEXTUAL_CREDIBILITY = "CONTEXTUAL_CREDIBILITY"
    STRONG_CONTEXTUAL_CREDIBILITY = "STRONG_CONTEXTUAL_CREDIBILITY"


@dataclass(frozen=True)
class AccessEvidence:
    source_id: str
    claim: str

    def usable(self) -> bool:
        return bool(self.source_id.strip() and self.claim.strip())


@dataclass(frozen=True)
class OperatorCapabilityEnvelope:
    """Current operator endowments that can legitimately affect route feasibility.

    Keep this generic. Personal data does not belong in the public repository merely because
    the model can represent it. Runtime/profile data should be supplied only when appropriate.
    """

    professional_years: int = 0
    proven_domains: Sequence[str] = field(default_factory=tuple)
    accepted_delivery_contexts: Sequence[str] = field(default_factory=tuple)
    education_training: Sequence[str] = field(default_factory=tuple)
    cross_context_experience: Sequence[str] = field(default_factory=tuple)
    communication_trust_assets: Sequence[str] = field(default_factory=tuple)
    local_knowledge: Sequence[str] = field(default_factory=tuple)
    warm_paths: Sequence[str] = field(default_factory=tuple)
    institutional_roles: Sequence[str] = field(default_factory=tuple)
    reputation_references: Sequence[str] = field(default_factory=tuple)
    mobilizable_resources: Sequence[str] = field(default_factory=tuple)
    constraints: Sequence[str] = field(default_factory=tuple)


def operator_fit_state(profile: OperatorCapabilityEnvelope) -> OperatorFitState:
    """Estimate only whether the operator has substantive contextual credibility.

    This is deliberately coarse and does not imply counterpart willingness to engage.
    """

    substantive_signals = sum(
        bool(items)
        for items in (
            profile.proven_domains,
            profile.accepted_delivery_contexts,
            profile.education_training,
            profile.cross_context_experience,
            profile.reputation_references,
        )
    )
    trust_signals = sum(
        bool(items)
        for items in (
            profile.communication_trust_assets,
            profile.local_knowledge,
            profile.warm_paths,
            profile.institutional_roles,
        )
    )

    if profile.professional_years <= 0 and substantive_signals == 0:
        return OperatorFitState.THIN
    if profile.professional_years >= 5 and substantive_signals >= 2:
        if trust_signals >= 1:
            return OperatorFitState.STRONG_CONTEXTUAL_CREDIBILITY
        return OperatorFitState.CONTEXTUAL_CREDIBILITY
    if substantive_signals >= 1 or profile.professional_years >= 3:
        return OperatorFitState.CONTEXTUAL_CREDIBILITY
    return OperatorFitState.THIN


@dataclass(frozen=True)
class AccessFeasibility:
    candidate_id: str
    target_actor: str
    route_kind: AccessRouteKind
    legitimate_entry_path: str
    backing_leverage: str
    counterparty_reason_to_engage: str
    counterparty_visible_surplus: str
    surplus_realization_mechanism: str
    institutional_cover_or_referral: str
    status_trust_friction: str
    operator_credibility_assets: str
    missing_credibility: str
    operator_commitment: str
    counterparty_commitment_requested: str
    founder_identity_dependency: str
    first_value_packet: str = ""
    counterparty_downside: str = ""
    cultural_context_notes: str = ""
    evidence: Sequence[AccessEvidence] = field(default_factory=tuple)


_REQUIRED = (
    "candidate_id",
    "target_actor",
    "legitimate_entry_path",
    "backing_leverage",
    "counterparty_reason_to_engage",
    "counterparty_visible_surplus",
    "surplus_realization_mechanism",
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
        if record.backing_leverage.strip().lower() in {"", "none", "无", "没有"}:
            # Direct outreach may proceed without backing only if counterpart surplus is explicit.
            if not record.counterparty_visible_surplus.strip():
                errors.append("cold_access_without_backing_or_visible_surplus")
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

    weak_surplus = record.counterparty_visible_surplus.strip().lower()
    if weak_surplus in {
        "analysis",
        "insight",
        "ppt",
        "report",
        "分析",
        "认知",
        "ppt报告",
        "给他讲问题",
    }:
        errors.append("non_economic_or_non_concrete_surplus")

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
        AccessRouteKind.COMMITTED_COMPLEMENTARY_ACTOR,
    }:
        return AccessState.INTRODUCTION_READY

    if record.missing_credibility.strip():
        return AccessState.INTRODUCTION_READY

    if "unknown" in record.founder_identity_dependency.lower():
        return AccessState.ENGAGEMENT_READY

    return AccessState.VALIDATION_ACCESS_READY


ACCESS_INVARIANTS = (
    "VALUE_TRUTH_NE_OPERATOR_ACCESS",
    "OPERATOR_ACCESS_NE_COUNTERPARTY_VISIBLE_SURPLUS",
    "OPERATOR_ENDOWMENT_NE_COUNTERPARTY_CONSENT",
    "PUBLIC_ACTOR_NE_ACCESSIBLE_ACTOR",
    "PUBLIC_WINDOW_NE_STRONG_BACKING_BY_DEFAULT",
    "PERSONAL_CONFIDENCE_NE_COUNTERPARTY_REASON_TO_ENGAGE",
    "APPEARANCE_NE_CREDENTIAL",
    "REAL_WORK_HISTORY_IS_CREDIBILITY_EVIDENCE_WHEN_RELEVANT",
    "ANALYSIS_NE_SURPLUS",
    "PPT_NE_HOOK",
    "PROBLEM_EXPLANATION_NE_BENEFIT",
    "BACKING_MUST_BE_REAL",
    "COUNTERPARTY_SURPLUS_MUST_BE_LEGIBLE",
    "LOCAL_FIELD_PRIOR_NE_UNIVERSAL_FACT",
    "ACCESS_BLOCKED_NE_BAD_OPPORTUNITY",
)
