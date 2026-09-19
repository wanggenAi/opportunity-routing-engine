"""Causal-depth model for latent-value discovery.

The repository must not confuse a visible symptom with the commercially relevant
constraint underneath it. This module makes causal descent explicit while
preserving a hard boundary between inference and evidence.

The model intentionally does not claim that every real-world phenomenon has one
single metaphysical root cause. The useful target is the deepest decision-relevant,
falsifiable causal frontier supported by evidence. Multiple constraints may remain
jointly causal.

Canonical direction:

    OBSERVED SURFACE SIGNAL
    -> competing LATENT OUTCOME hypotheses
    -> competing STRUCTURAL CONSTRAINT hypotheses
    -> discriminating evidence / falsifiers / contradiction search
    -> decision-useful causal frontier
    != PRODUCT
    != MISSING EDGE
    != COMMERCIAL OPPORTUNITY
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence


class CausalTruthState(str, Enum):
    """Epistemic maturity of an outcome or causal claim."""

    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    EVIDENCED_STRUCTURE = "EVIDENCED_STRUCTURE"


class CausalDescentState(str, Enum):
    """Maturity of the causal-descent layer only."""

    SURFACE_SIGNAL = "SURFACE_SIGNAL"
    LATENT_OUTCOME_HYPOTHESIS = "LATENT_OUTCOME_HYPOTHESIS"
    CAUSAL_HYPOTHESIS_SET = "CAUSAL_HYPOTHESIS_SET"
    DECISIVE_UNKNOWN = "DECISIVE_UNKNOWN"
    EVIDENCED_STRUCTURAL_FRICTION = "EVIDENCED_STRUCTURAL_FRICTION"


class CausalStopReason(str, Enum):
    """Why causal descent stops at the current structural frontier."""

    INTERVENTION_RELEVANT_BOUNDARY = "INTERVENTION_RELEVANT_BOUNDARY"
    NO_DEEPER_FALSIFIABLE_LAYER = "NO_DEEPER_FALSIFIABLE_LAYER"
    EVIDENCE_LIMIT_REACHED = "EVIDENCE_LIMIT_REACHED"
    MULTI_CAUSAL_FRONTIER = "MULTI_CAUSAL_FRONTIER"


@dataclass(frozen=True)
class LatentOutcomeHypothesis:
    """Product-agnostic state transition an Actor appears to be seeking/avoiding."""

    outcome_id: str
    statement: str
    truth_state: CausalTruthState = CausalTruthState.INFERRED
    evidence_refs: tuple[str, ...] = ()
    contradiction_refs: tuple[str, ...] = ()
    falsifiers: tuple[str, ...] = ()

    def is_usable(self) -> bool:
        return bool(
            self.outcome_id.strip()
            and self.statement.strip()
            and self.evidence_refs
            and all(isinstance(ref, str) and ref.strip() for ref in self.evidence_refs)
        )


@dataclass(frozen=True)
class StructuralConstraintHypothesis:
    """One falsifiable explanation for why a latent state transition is blocked."""

    constraint_id: str
    outcome_id: str
    depth: int
    causal_claim: str
    mechanism: str
    truth_state: CausalTruthState = CausalTruthState.INFERRED
    parent_constraint_id: str = ""
    support_refs: tuple[str, ...] = ()
    contradiction_refs: tuple[str, ...] = ()
    discriminating_evidence_refs: tuple[str, ...] = ()
    falsifiers: tuple[str, ...] = ()
    intervention_implication: str = ""

    def is_usable(self) -> bool:
        return bool(
            self.constraint_id.strip()
            and self.outcome_id.strip()
            and isinstance(self.depth, int)
            and not isinstance(self.depth, bool)
            and self.depth >= 1
            and self.causal_claim.strip()
            and self.mechanism.strip()
        )


@dataclass(frozen=True)
class CausalDescentRecord:
    """Evidence-bound causal reconstruction for one Actor/surface signal.

    lead_constraint_ids identifies the currently best-supported causal frontier.
    It may contain more than one id because real systems can be multi-causal.

    probe_eligible is deliberately narrow: broad sensing has reduced the remaining
    uncertainty to one decisive causal question. It does not validate an opportunity.
    """

    record_id: str
    actor: str
    current_state: str
    surface_phenomenon: str
    surface_evidence_refs: tuple[str, ...]
    outcome_hypotheses: Sequence[LatentOutcomeHypothesis]
    selected_outcome_id: str
    constraint_hypotheses: Sequence[StructuralConstraintHypothesis]
    lead_constraint_ids: tuple[str, ...]
    stop_reason: CausalStopReason | None = None
    decisive_unknown: str = ""
    probe_eligible: bool = False
    notes: str = ""


def _outcomes(record: CausalDescentRecord) -> dict[str, LatentOutcomeHypothesis]:
    return {item.outcome_id: item for item in record.outcome_hypotheses}


def _constraints(
    record: CausalDescentRecord,
) -> dict[str, StructuralConstraintHypothesis]:
    return {item.constraint_id: item for item in record.constraint_hypotheses}


def validate_causal_descent(record: CausalDescentRecord) -> list[str]:
    """Validate internal consistency without claiming commercial truth."""

    errors: list[str] = []

    for name in ("record_id", "actor", "current_state", "surface_phenomenon"):
        value = getattr(record, name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing:{name}")

    if not record.surface_evidence_refs:
        errors.append("missing:surface_evidence_refs")
    elif any(
        not isinstance(ref, str) or not ref.strip()
        for ref in record.surface_evidence_refs
    ):
        errors.append("invalid:surface_evidence_refs")

    outcome_ids = [item.outcome_id for item in record.outcome_hypotheses]
    if len(outcome_ids) != len(set(outcome_ids)):
        errors.append("duplicate:outcome_id")
    outcomes = _outcomes(record)

    if record.selected_outcome_id not in outcomes:
        errors.append("selected_outcome_not_found")

    for outcome in record.outcome_hypotheses:
        if not outcome.is_usable():
            errors.append(f"invalid:outcome:{outcome.outcome_id or 'UNKNOWN'}")
        if outcome.truth_state is CausalTruthState.EVIDENCED_STRUCTURE:
            if not outcome.falsifiers:
                errors.append(f"missing:outcome_falsifiers:{outcome.outcome_id}")

    constraint_ids = [item.constraint_id for item in record.constraint_hypotheses]
    if len(constraint_ids) != len(set(constraint_ids)):
        errors.append("duplicate:constraint_id")
    constraints = _constraints(record)

    for constraint in record.constraint_hypotheses:
        if not constraint.is_usable():
            errors.append(
                f"invalid:constraint:{constraint.constraint_id or 'UNKNOWN'}"
            )
            continue
        if constraint.outcome_id not in outcomes:
            errors.append(
                f"constraint_outcome_not_found:{constraint.constraint_id}"
            )
        if constraint.parent_constraint_id:
            parent = constraints.get(constraint.parent_constraint_id)
            if parent is None:
                errors.append(
                    f"constraint_parent_not_found:{constraint.constraint_id}"
                )
            elif parent.depth >= constraint.depth:
                errors.append(
                    f"constraint_depth_not_deeper_than_parent:{constraint.constraint_id}"
                )

        if constraint.truth_state is CausalTruthState.EVIDENCED_STRUCTURE:
            if not constraint.support_refs:
                errors.append(
                    f"missing:constraint_support:{constraint.constraint_id}"
                )
            if not constraint.discriminating_evidence_refs:
                errors.append(
                    f"missing:discriminating_evidence:{constraint.constraint_id}"
                )
            if not constraint.falsifiers:
                errors.append(
                    f"missing:constraint_falsifiers:{constraint.constraint_id}"
                )

    if len(record.lead_constraint_ids) != len(set(record.lead_constraint_ids)):
        errors.append("duplicate:lead_constraint_id")
    for constraint_id in record.lead_constraint_ids:
        constraint = constraints.get(constraint_id)
        if constraint is None:
            errors.append(f"lead_constraint_not_found:{constraint_id}")
        elif (
            record.selected_outcome_id
            and constraint.outcome_id != record.selected_outcome_id
        ):
            errors.append(f"lead_constraint_wrong_outcome:{constraint_id}")

    if record.probe_eligible and not record.decisive_unknown.strip():
        errors.append("probe_eligible_requires_decisive_unknown")

    if record.stop_reason is not None and not record.lead_constraint_ids:
        errors.append("stop_reason_requires_lead_constraint")

    return errors


def causal_descent_state(record: CausalDescentRecord) -> CausalDescentState:
    """Infer maturity without rewarding a polished causal story."""

    outcomes = _outcomes(record)
    selected = outcomes.get(record.selected_outcome_id)
    if selected is None or not selected.is_usable():
        return CausalDescentState.SURFACE_SIGNAL

    if not record.constraint_hypotheses or not record.lead_constraint_ids:
        return CausalDescentState.LATENT_OUTCOME_HYPOTHESIS

    constraints = _constraints(record)
    lead = [
        constraints[item]
        for item in record.lead_constraint_ids
        if item in constraints
    ]
    if not lead:
        return CausalDescentState.CAUSAL_HYPOTHESIS_SET

    evidenced = [
        item
        for item in lead
        if item.truth_state is CausalTruthState.EVIDENCED_STRUCTURE
        and item.support_refs
        and item.discriminating_evidence_refs
        and item.falsifiers
    ]

    if len(evidenced) != len(lead):
        if record.probe_eligible and record.decisive_unknown.strip():
            return CausalDescentState.DECISIVE_UNKNOWN
        return CausalDescentState.CAUSAL_HYPOTHESIS_SET

    if (
        selected.truth_state is not CausalTruthState.EVIDENCED_STRUCTURE
        or not selected.falsifiers
        or record.stop_reason is None
    ):
        return CausalDescentState.CAUSAL_HYPOTHESIS_SET

    return CausalDescentState.EVIDENCED_STRUCTURAL_FRICTION


def validate_causal_descent_for_promotion(
    record: CausalDescentRecord,
) -> list[str]:
    """Fail closed before causal structure may drive candidate promotion.

    Hypothesis generation can be broad. Promotion requires competing explanations,
    falsifiability, discriminating evidence and an explicit stop rule so the system
    does not mistake a compelling story for a deep causal truth.
    """

    errors = validate_causal_descent(record)

    if (
        causal_descent_state(record)
        is not CausalDescentState.EVIDENCED_STRUCTURAL_FRICTION
    ):
        errors.append("causal_descent_not_evidenced")

    selected = _outcomes(record).get(record.selected_outcome_id)
    if (
        selected is not None
        and selected.truth_state is not CausalTruthState.EVIDENCED_STRUCTURE
    ):
        errors.append("latent_outcome_not_evidenced")

    same_outcome_constraints = [
        item
        for item in record.constraint_hypotheses
        if item.outcome_id == record.selected_outcome_id
    ]
    if len(same_outcome_constraints) < 2:
        errors.append("missing:competing_causal_explanation")

    if not record.stop_reason:
        errors.append("missing:causal_stop_reason")

    return list(dict.fromkeys(errors))


GOVERNING_INVARIANTS = (
    "SURFACE_SIGNAL_NE_CAUSAL_EXPLANATION",
    "STATED_REQUEST_NE_LATENT_OUTCOME",
    "LATENT_OUTCOME_HYPOTHESIS_NE_FACT",
    "ONE_PLAUSIBLE_CAUSE_NE_STRUCTURAL_TRUTH",
    "DEEPER_STORY_NE_DEEPER_TRUTH",
    "ROOT_CAUSE_LANGUAGE_NE_SINGLE_CAUSE_ASSUMPTION",
    "STRUCTURAL_FRICTION_MAY_BE_MULTI_CAUSAL",
    "STRUCTURAL_FRICTION_NE_MISSING_EDGE",
    "CAUSAL_DESCENT_STOPS_AT_DEEPEST_DECISION_USEFUL_FALSIFIABLE_FRONTIER",
    "INFERRED_STRUCTURE_MAY_GUIDE_EXPLORATION_BUT_NOT_PROMOTION",
    "DECISIVE_UNKNOWN_MAY_JUSTIFY_BOUNDED_PROBE",
    "UNKNOWN_NE_PASS",
)
