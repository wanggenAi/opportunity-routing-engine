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
from typing import Mapping, Sequence


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

    def as_dict(self) -> dict[str, object]:
        return {
            "outcome_id": self.outcome_id,
            "statement": self.statement,
            "truth_state": self.truth_state.value,
            "evidence_refs": list(self.evidence_refs),
            "contradiction_refs": list(self.contradiction_refs),
            "falsifiers": list(self.falsifiers),
        }


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

    def as_dict(self) -> dict[str, object]:
        return {
            "constraint_id": self.constraint_id,
            "outcome_id": self.outcome_id,
            "depth": self.depth,
            "causal_claim": self.causal_claim,
            "mechanism": self.mechanism,
            "truth_state": self.truth_state.value,
            "parent_constraint_id": self.parent_constraint_id,
            "support_refs": list(self.support_refs),
            "contradiction_refs": list(self.contradiction_refs),
            "discriminating_evidence_refs": list(self.discriminating_evidence_refs),
            "falsifiers": list(self.falsifiers),
            "intervention_implication": self.intervention_implication,
        }


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


    def as_dict(self) -> dict[str, object]:
        return {
            "record_id": self.record_id,
            "actor": self.actor,
            "current_state": self.current_state,
            "surface_phenomenon": self.surface_phenomenon,
            "surface_evidence_refs": list(self.surface_evidence_refs),
            "outcome_hypotheses": [
                item.as_dict() for item in self.outcome_hypotheses
            ],
            "selected_outcome_id": self.selected_outcome_id,
            "constraint_hypotheses": [
                item.as_dict() for item in self.constraint_hypotheses
            ],
            "lead_constraint_ids": list(self.lead_constraint_ids),
            "stop_reason": self.stop_reason.value if self.stop_reason else None,
            "decisive_unknown": self.decisive_unknown,
            "probe_eligible": self.probe_eligible,
            "notes": self.notes,
        }


def _string_tuple(value: object, *, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{field_name} must be a list of strings")
    items = tuple(str(item) for item in value)
    if any(not item.strip() for item in items):
        raise ValueError(f"{field_name} contains an empty value")
    return items


def causal_descent_from_mapping(raw: Mapping[str, object]) -> CausalDescentRecord:
    """Parse persisted causal lineage without silently accepting malformed enums."""

    raw_outcomes = raw.get("outcome_hypotheses")
    if not isinstance(raw_outcomes, Sequence) or isinstance(raw_outcomes, (str, bytes)):
        raise ValueError("outcome_hypotheses must be a list")

    outcomes: list[LatentOutcomeHypothesis] = []
    for index, item in enumerate(raw_outcomes):
        if not isinstance(item, Mapping):
            raise ValueError(f"outcome_hypotheses[{index}] must be an object")
        try:
            truth_state = CausalTruthState(str(item.get("truth_state") or "INFERRED"))
        except ValueError as exc:
            raise ValueError(
                f"invalid outcome truth_state at index {index}"
            ) from exc
        outcomes.append(
            LatentOutcomeHypothesis(
                outcome_id=str(item.get("outcome_id") or ""),
                statement=str(item.get("statement") or ""),
                truth_state=truth_state,
                evidence_refs=_string_tuple(
                    item.get("evidence_refs"),
                    field_name=f"outcome_hypotheses[{index}].evidence_refs",
                ),
                contradiction_refs=_string_tuple(
                    item.get("contradiction_refs"),
                    field_name=f"outcome_hypotheses[{index}].contradiction_refs",
                ),
                falsifiers=_string_tuple(
                    item.get("falsifiers"),
                    field_name=f"outcome_hypotheses[{index}].falsifiers",
                ),
            )
        )

    raw_constraints = raw.get("constraint_hypotheses")
    if not isinstance(raw_constraints, Sequence) or isinstance(
        raw_constraints, (str, bytes)
    ):
        raise ValueError("constraint_hypotheses must be a list")

    constraints: list[StructuralConstraintHypothesis] = []
    for index, item in enumerate(raw_constraints):
        if not isinstance(item, Mapping):
            raise ValueError(f"constraint_hypotheses[{index}] must be an object")
        try:
            truth_state = CausalTruthState(str(item.get("truth_state") or "INFERRED"))
        except ValueError as exc:
            raise ValueError(
                f"invalid constraint truth_state at index {index}"
            ) from exc
        depth = item.get("depth", 0)
        if not isinstance(depth, int) or isinstance(depth, bool):
            raise ValueError(f"constraint_hypotheses[{index}].depth must be an integer")
        constraints.append(
            StructuralConstraintHypothesis(
                constraint_id=str(item.get("constraint_id") or ""),
                outcome_id=str(item.get("outcome_id") or ""),
                depth=depth,
                causal_claim=str(item.get("causal_claim") or ""),
                mechanism=str(item.get("mechanism") or ""),
                truth_state=truth_state,
                parent_constraint_id=str(item.get("parent_constraint_id") or ""),
                support_refs=_string_tuple(
                    item.get("support_refs"),
                    field_name=f"constraint_hypotheses[{index}].support_refs",
                ),
                contradiction_refs=_string_tuple(
                    item.get("contradiction_refs"),
                    field_name=f"constraint_hypotheses[{index}].contradiction_refs",
                ),
                discriminating_evidence_refs=_string_tuple(
                    item.get("discriminating_evidence_refs"),
                    field_name=(
                        f"constraint_hypotheses[{index}]."
                        "discriminating_evidence_refs"
                    ),
                ),
                falsifiers=_string_tuple(
                    item.get("falsifiers"),
                    field_name=f"constraint_hypotheses[{index}].falsifiers",
                ),
                intervention_implication=str(
                    item.get("intervention_implication") or ""
                ),
            )
        )

    raw_stop = raw.get("stop_reason")
    stop_reason: CausalStopReason | None = None
    if raw_stop not in (None, ""):
        try:
            stop_reason = CausalStopReason(str(raw_stop))
        except ValueError as exc:
            raise ValueError("invalid causal stop_reason") from exc

    return CausalDescentRecord(
        record_id=str(raw.get("record_id") or ""),
        actor=str(raw.get("actor") or ""),
        current_state=str(raw.get("current_state") or ""),
        surface_phenomenon=str(raw.get("surface_phenomenon") or ""),
        surface_evidence_refs=_string_tuple(
            raw.get("surface_evidence_refs"),
            field_name="surface_evidence_refs",
        ),
        outcome_hypotheses=tuple(outcomes),
        selected_outcome_id=str(raw.get("selected_outcome_id") or ""),
        constraint_hypotheses=tuple(constraints),
        lead_constraint_ids=_string_tuple(
            raw.get("lead_constraint_ids"),
            field_name="lead_constraint_ids",
        ),
        stop_reason=stop_reason,
        decisive_unknown=str(raw.get("decisive_unknown") or ""),
        probe_eligible=bool(raw.get("probe_eligible", False)),
        notes=str(raw.get("notes") or ""),
    )


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

    if (
        record.stop_reason is CausalStopReason.MULTI_CAUSAL_FRONTIER
        and len(record.lead_constraint_ids) < 2
    ):
        errors.append("multi_causal_frontier_requires_multiple_lead_constraints")

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

    if record.stop_reason is CausalStopReason.EVIDENCE_LIMIT_REACHED:
        return CausalDescentState.CAUSAL_HYPOTHESIS_SET

    if (
        record.stop_reason is CausalStopReason.MULTI_CAUSAL_FRONTIER
        and len(lead) < 2
    ):
        return CausalDescentState.CAUSAL_HYPOTHESIS_SET

    return CausalDescentState.EVIDENCED_STRUCTURAL_FRICTION


def _normalized_text(value: str) -> str:
    return " ".join(value.split()).strip().casefold()


def validate_causal_projection(
    record: CausalDescentRecord,
    *,
    actor: str,
    current_state: str,
    surface_phenomenon: str,
    latent_outcome_hypothesis: str,
    structural_friction_hypothesis: str,
    record_id: str = "",
    stop_reason: str = "",
) -> list[str]:
    """Prevent denormalized summaries from drifting from canonical causal lineage."""

    errors: list[str] = []

    if _normalized_text(record.actor) != _normalized_text(actor):
        errors.append("causal_descent_actor_mismatch")
    if _normalized_text(record.current_state) != _normalized_text(current_state):
        errors.append("causal_current_state_projection_mismatch")
    if _normalized_text(record.surface_phenomenon) != _normalized_text(
        surface_phenomenon
    ):
        errors.append("surface_phenomenon_projection_mismatch")

    outcomes = {item.outcome_id: item for item in record.outcome_hypotheses}
    selected = outcomes.get(record.selected_outcome_id)
    if selected is None:
        errors.append("causal_descent_selected_outcome_missing")
    elif _normalized_text(selected.statement) != _normalized_text(
        latent_outcome_hypothesis
    ):
        errors.append("latent_outcome_projection_mismatch")

    constraints = {
        item.constraint_id: item for item in record.constraint_hypotheses
    }
    lead = [
        constraints[item]
        for item in record.lead_constraint_ids
        if item in constraints
    ]
    if len(lead) == 1 and _normalized_text(lead[0].causal_claim) != _normalized_text(
        structural_friction_hypothesis
    ):
        errors.append("structural_friction_projection_mismatch")

    if record_id and record_id != record.record_id:
        errors.append("causal_descent_record_id_mismatch")

    expected_stop = record.stop_reason.value if record.stop_reason is not None else ""
    if stop_reason and stop_reason != expected_stop:
        errors.append("causal_stop_reason_mismatch")

    return errors


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
    elif record.stop_reason is CausalStopReason.EVIDENCE_LIMIT_REACHED:
        errors.append("causal_evidence_limit_reached")

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
