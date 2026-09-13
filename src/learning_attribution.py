"""Conservative, review-only learning attribution over preserved execution lineage.

This module does not mutate rules, source status, requirement bundles, or routing policy.
It answers narrower audit questions:

1. Which graph claim outputs have later explicit verification linked to the exact
   source signal that produced them?
2. How many linked outcomes are CONFIRMED / REJECTED / UNRESOLVED for each source
   and inference-rule version?
3. Which source/rule lineages were exposed in one exact composition hypothesis, and
   what downstream validation/outcome evidence exists for that hypothesis?

The word "attribution" here means evidence-lineage attribution, not causal credit.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable, Sequence

from src.capability_graph_store import CapabilityGraphClaim, SQLiteCapabilityGraphStore
from src.capability_verification_store import (
    CapabilityVerificationEvent,
    SQLiteCapabilityVerificationStore,
    VerificationVerdict,
)
from src.composition_outcome_store import OutcomeEventType, SQLiteCompositionOutcomeStore
from src.composition_run_store import SQLiteCompositionRunStore
from src.composition_validation_store import SQLiteCompositionValidationStore
from src.live_resource_signals import EvidenceStatus


class LinkedVerificationState(str, Enum):
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"
    UNRESOLVED = "UNRESOLVED"


class ReviewSignal(str, Enum):
    NO_LINKED_VERIFICATION = "NO_LINKED_VERIFICATION"
    INSUFFICIENT_LINKED_VERIFICATION = "INSUFFICIENT_LINKED_VERIFICATION"
    MIXED_LINKED_VERIFICATION = "MIXED_LINKED_VERIFICATION"
    REVIEW_REJECTION_CLUSTER = "REVIEW_REJECTION_CLUSTER"
    POSITIVE_LINKED_EVIDENCE = "POSITIVE_LINKED_EVIDENCE"


@dataclass(frozen=True)
class ClaimVerificationDiagnostic:
    materialization_id: int
    actor_ref: str
    capability_key: str
    source_id: str
    source_signal_ref: str
    evidence_status: EvidenceStatus
    inference_rule_id: str
    claim_last_observed_at: datetime
    linked_state: LinkedVerificationState
    linked_verification_id: str = ""
    linked_verified_at: datetime | None = None


@dataclass(frozen=True)
class LineageVerificationSummary:
    lineage_id: str
    claim_output_count: int
    confirmed_count: int
    rejected_count: int
    unresolved_count: int
    linked_verification_count: int
    review_signal: ReviewSignal


@dataclass(frozen=True)
class CompositionLearningDiagnostic:
    composition_run_id: int
    hypothesis_index: int
    bundle_id: str
    bundle_version: int
    materialization_id: int
    composition_state: str
    actor_refs: tuple[str, ...]
    source_ids: tuple[str, ...]
    inference_rule_ids: tuple[str, ...]
    transaction_gates: tuple[tuple[str, str], ...]
    bounded_transaction_ready: bool
    outcome_evidence_maturity: str
    outcome_event_count: int
    accepted_settled_transaction_count: int
    transactions_with_failure_evidence: int
    outcome_event_types: tuple[tuple[str, int], ...]
    truth_note: str = (
        "Source/rule presence is lineage exposure only. Downstream success or failure does "
        "not establish causal credit or blame for every exposed input."
    )


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    return value.astimezone(timezone.utc)


def _latest_linked_verification(
    claim: CapabilityGraphClaim,
    events: Sequence[CapabilityVerificationEvent],
) -> CapabilityVerificationEvent | None:
    """Return latest explicit verification that links the exact source signal.

    Actor/capability equality alone is insufficient for source/rule learning. The event
    must explicitly cite the claim's globally unique `source_id::signal_id`, and it must
    be at least as new as the claim observation it evaluates.
    """

    matches = [
        event
        for event in events
        if event.actor_ref == claim.actor_ref
        and event.capability_key == claim.capability_key
        and claim.source_signal_ref in {ref.strip() for ref in event.related_signal_refs}
        and _utc(event.verified_at) >= _utc(claim.last_observed_at)
    ]
    if not matches:
        return None
    return max(matches, key=lambda event: _utc(event.verified_at))


def claim_verification_diagnostics(
    graph_store: SQLiteCapabilityGraphStore,
    verification_store: SQLiteCapabilityVerificationStore,
    *,
    materialization_id: int,
    as_of: datetime,
) -> tuple[ClaimVerificationDiagnostic, ...]:
    if as_of.tzinfo is None:
        raise ValueError("as_of must be timezone-aware")
    if graph_store.get_materialization(materialization_id) is None:
        raise ValueError("unknown materialization_id")

    events = verification_store.events(as_of=as_of)
    diagnostics: list[ClaimVerificationDiagnostic] = []
    for claim in graph_store.claims(materialization_id):
        linked = _latest_linked_verification(claim, events)
        if linked is None:
            state = LinkedVerificationState.UNRESOLVED
            verification_id = ""
            verified_at = None
        else:
            state = (
                LinkedVerificationState.CONFIRMED
                if linked.verdict is VerificationVerdict.CONFIRMED
                else LinkedVerificationState.REJECTED
            )
            verification_id = linked.verification_id
            verified_at = linked.verified_at
        diagnostics.append(
            ClaimVerificationDiagnostic(
                materialization_id=materialization_id,
                actor_ref=claim.actor_ref,
                capability_key=claim.capability_key,
                source_id=claim.source_id,
                source_signal_ref=claim.source_signal_ref,
                evidence_status=claim.evidence_status,
                inference_rule_id=claim.inference_rule_id,
                claim_last_observed_at=claim.last_observed_at,
                linked_state=state,
                linked_verification_id=verification_id,
                linked_verified_at=verified_at,
            )
        )
    return tuple(diagnostics)


def _review_signal(
    *,
    confirmed: int,
    rejected: int,
    minimum_linked_verifications: int,
) -> ReviewSignal:
    linked = confirmed + rejected
    if linked == 0:
        return ReviewSignal.NO_LINKED_VERIFICATION
    if linked < minimum_linked_verifications:
        return ReviewSignal.INSUFFICIENT_LINKED_VERIFICATION
    if confirmed and rejected:
        return ReviewSignal.MIXED_LINKED_VERIFICATION
    if rejected:
        return ReviewSignal.REVIEW_REJECTION_CLUSTER
    return ReviewSignal.POSITIVE_LINKED_EVIDENCE


def _summaries(
    diagnostics: Sequence[ClaimVerificationDiagnostic],
    *,
    lineage_ids: Iterable[str],
    selector,
    minimum_linked_verifications: int,
) -> tuple[LineageVerificationSummary, ...]:
    if minimum_linked_verifications < 1:
        raise ValueError("minimum_linked_verifications must be at least 1")
    result: list[LineageVerificationSummary] = []
    for lineage_id in sorted(set(lineage_ids)):
        selected = [item for item in diagnostics if selector(item) == lineage_id]
        confirmed = sum(
            item.linked_state is LinkedVerificationState.CONFIRMED for item in selected
        )
        rejected = sum(
            item.linked_state is LinkedVerificationState.REJECTED for item in selected
        )
        unresolved = sum(
            item.linked_state is LinkedVerificationState.UNRESOLVED for item in selected
        )
        linked = confirmed + rejected
        result.append(
            LineageVerificationSummary(
                lineage_id=lineage_id,
                claim_output_count=len(selected),
                confirmed_count=confirmed,
                rejected_count=rejected,
                unresolved_count=unresolved,
                linked_verification_count=linked,
                review_signal=_review_signal(
                    confirmed=confirmed,
                    rejected=rejected,
                    minimum_linked_verifications=minimum_linked_verifications,
                ),
            )
        )
    return tuple(result)


def source_verification_summaries(
    diagnostics: Sequence[ClaimVerificationDiagnostic],
    *,
    minimum_linked_verifications: int = 5,
) -> tuple[LineageVerificationSummary, ...]:
    return _summaries(
        diagnostics,
        lineage_ids=(item.source_id for item in diagnostics),
        selector=lambda item: item.source_id,
        minimum_linked_verifications=minimum_linked_verifications,
    )


def rule_verification_summaries(
    diagnostics: Sequence[ClaimVerificationDiagnostic],
    *,
    minimum_linked_verifications: int = 5,
) -> tuple[LineageVerificationSummary, ...]:
    inferred = tuple(item for item in diagnostics if item.inference_rule_id.strip())
    return _summaries(
        inferred,
        lineage_ids=(item.inference_rule_id for item in inferred),
        selector=lambda item: item.inference_rule_id,
        minimum_linked_verifications=minimum_linked_verifications,
    )


def _hypothesis_graph_claims(
    graph_store: SQLiteCapabilityGraphStore,
    *,
    materialization_id: int,
    hypothesis,
) -> tuple[CapabilityGraphClaim, ...]:
    result: list[CapabilityGraphClaim] = []
    seen: set[tuple[object, ...]] = set()
    for contribution in hypothesis.contributions:
        source_refs = set(contribution.source_signal_ids)
        for actor_ref in contribution.actor_refs:
            for claim in graph_store.claims(
                materialization_id,
                actor_ref=actor_ref,
                capability_key=contribution.capability_key,
            ):
                if claim.source_signal_ref not in source_refs:
                    continue
                key = (
                    claim.actor_ref,
                    claim.capability_key,
                    claim.source_id,
                    claim.signal_id,
                    claim.evidence_status.value,
                    claim.inference_rule_id,
                )
                if key not in seen:
                    seen.add(key)
                    result.append(claim)
    return tuple(result)


def composition_learning_diagnostic(
    graph_store: SQLiteCapabilityGraphStore,
    run_store: SQLiteCompositionRunStore,
    validation_store: SQLiteCompositionValidationStore,
    outcome_store: SQLiteCompositionOutcomeStore,
    *,
    run_id: int,
    hypothesis_index: int,
    as_of: datetime,
) -> CompositionLearningDiagnostic:
    if as_of.tzinfo is None:
        raise ValueError("as_of must be timezone-aware")
    run = run_store.get_run(run_id)
    if run is None:
        raise ValueError("unknown composition_run_id")
    hypotheses = run_store.hypotheses(run_id)
    if hypothesis_index < 0 or hypothesis_index >= len(hypotheses):
        raise ValueError("unknown composition hypothesis index")
    hypothesis = hypotheses[hypothesis_index]

    linked_claims = _hypothesis_graph_claims(
        graph_store,
        materialization_id=run.materialization_id,
        hypothesis=hypothesis,
    )
    source_ids = tuple(sorted({claim.source_id for claim in linked_claims}))
    rule_ids = tuple(
        sorted(
            {
                claim.inference_rule_id
                for claim in linked_claims
                if claim.inference_rule_id.strip()
            }
        )
    )

    validation = validation_store.projection(
        run_id,
        hypothesis_index,
        composition_runs=run_store,
        as_of=as_of,
    )
    outcome = outcome_store.projection(run_id, hypothesis_index, as_of=as_of)
    type_counts: dict[str, int] = {}
    for event in outcome_store.events(run_id, hypothesis_index, as_of=as_of):
        key = event.event_type.value
        type_counts[key] = type_counts.get(key, 0) + 1

    return CompositionLearningDiagnostic(
        composition_run_id=run_id,
        hypothesis_index=hypothesis_index,
        bundle_id=run.bundle_id,
        bundle_version=run.bundle_version,
        materialization_id=run.materialization_id,
        composition_state=hypothesis.state.value,
        actor_refs=hypothesis.actor_refs,
        source_ids=source_ids,
        inference_rule_ids=rule_ids,
        transaction_gates=tuple(sorted(validation.transaction_gates().items())),
        bounded_transaction_ready=validation.bounded_transaction_ready,
        outcome_evidence_maturity=outcome.evidence_maturity,
        outcome_event_count=outcome.event_count,
        accepted_settled_transaction_count=outcome.accepted_settled_transaction_count,
        transactions_with_failure_evidence=outcome.failed_transaction_count,
        outcome_event_types=tuple(sorted(type_counts.items())),
    )


GOVERNING_INVARIANTS = (
    "ATTRIBUTION_MEANS_LINEAGE_NOT_CAUSAL_CREDIT",
    "ACTOR_CAPABILITY_MATCH_NE_SOURCE_RULE_ATTRIBUTION",
    "EXACT_RELATED_SIGNAL_REF_REQUIRED_FOR_LINKED_VERIFICATION",
    "OLDER_VERIFICATION_NE_NEWER_CLAIM_VERIFICATION",
    "NO_VERIFICATION_NE_REJECTION",
    "OUTCOME_FAILURE_NE_CAPABILITY_INFERENCE_FAILURE",
    "SUCCESS_NE_CAUSAL_CREDIT_TO_ALL_INPUTS",
    "LOW_SAMPLE_NE_LOW_QUALITY",
    "REVIEW_SIGNAL_NE_AUTOMATIC_RULE_MUTATION",
    "REVIEW_SIGNAL_NE_AUTOMATIC_SOURCE_SUPPRESSION",
    "UNKNOWN_NE_PASS",
)
