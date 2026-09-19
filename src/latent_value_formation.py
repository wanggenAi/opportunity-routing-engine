"""Evidence-bound bridge from actor state + psychology to latent-value formation.

This module exists upstream of canonical transaction promotion. It connects
objective endowments/state changes with aggregate psychology/behavior evidence and
heterogeneous complementary world nodes, then asks whether reality already shows
pressure toward a latent connection between those nodes.

Only after that connection pressure is evidenced may a counterfactual exchange
mechanism become validation-ready. Counterfactual design describes execution
mechanics for an evidenced connection; it must not manufacture the connection.

It deliberately does *not* create paid demand, payer truth, resource availability,
transactionability, or commercial opportunity truth. Those remain downstream
Resource Imbalance / route-testability concerns.

Core boundary:

    OBJECTIVE ENDOWMENT / STATE / CHANGE
    + PSYCHOLOGY / BEHAVIOR EVIDENCE
    + SURFACE PHENOMENON / UNDERUSE / MISALIGNMENT
    -> LATENT / UNFORMED OUTCOME HYPOTHESIS
    -> STRUCTURAL FRICTION HYPOTHESIS
    + ALTERNATIVE-EXPLANATION / CORROBORATING EVIDENCE
    -> EVIDENCED STRUCTURAL FRICTION
    + COMPLEMENTARY WORLD NODES
    + CONNECTION PRESSURE EVIDENCE
    -> LATENT CONNECTION / VALUE FORMATION HYPOTHESIS
    -> COUNTERFACTUAL EXCHANGE MECHANICS
    != PAID NEED
    != TRANSACTION

Psychology is aggregate/segment evidence. This bridge must not be used to build
unnecessary individual psychographic profiles or to infer sensitive traits.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence

from src.causal_descent import (
    CausalDescentRecord,
    CausalDescentState,
    causal_descent_state,
    validate_causal_descent_for_promotion,
)
from src.latent_value_discovery import (
    EvidenceKind,
    EvidenceRef,
    LatentValueCandidate,
)
from src.psychology_tracker import PsychologySnapshot


class FormationState(str, Enum):
    """Maturity of an evidence-bound latent-value formation hypothesis."""

    OBSERVED_TRANSITION = "OBSERVED_TRANSITION"
    RESOURCE_PSYCHOLOGY_MISALIGNMENT_HYPOTHESIS = (
        "RESOURCE_PSYCHOLOGY_MISALIGNMENT_HYPOTHESIS"
    )
    STRUCTURAL_FRICTION_HYPOTHESIS = "STRUCTURAL_FRICTION_HYPOTHESIS"
    STRUCTURAL_FRICTION_EVIDENCED = "STRUCTURAL_FRICTION_EVIDENCED"
    LATENT_VALUE_FORMATION_HYPOTHESIS = "LATENT_VALUE_FORMATION_HYPOTHESIS"
    COMPLEMENTARITY_HYPOTHESIS = "COMPLEMENTARITY_HYPOTHESIS"
    LATENT_CONNECTION_EVIDENCED = "LATENT_CONNECTION_EVIDENCED"
    VALIDATION_READY = "VALIDATION_READY"


class StructuralFrictionTruthState(str, Enum):
    """Truth boundary for causal-depth claims."""

    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    EVIDENCED_STRUCTURE = "EVIDENCED_STRUCTURE"


class FormationEvidenceKind(str, Enum):
    """Independent evidence dimensions used before a formation can be validated."""

    OBJECTIVE_ENDOWMENT = "OBJECTIVE_ENDOWMENT"
    ORIGIN_STATE = "ORIGIN_STATE"
    ORIGIN_CHANGE = "ORIGIN_CHANGE"
    UNDERUSE_MISALIGNMENT = "UNDERUSE_MISALIGNMENT"
    OBSERVED_BEHAVIOR = "OBSERVED_BEHAVIOR"
    STRUCTURAL_FRICTION = "STRUCTURAL_FRICTION"
    COMPLEMENTARY_NODE = "COMPLEMENTARY_NODE"
    CONNECTION_PRESSURE = "CONNECTION_PRESSURE"
    MISSING_EDGE = "MISSING_EDGE"
    STRANDING_BARRIER = "STRANDING_BARRIER"
    COUNTERFACTUAL_PRECEDENT = "COUNTERFACTUAL_PRECEDENT"
    MONEY_BEHAVIOR = "MONEY_BEHAVIOR"
    GENERAL_CONTEXT = "GENERAL_CONTEXT"


@dataclass(frozen=True)
class FormationEvidenceRef:
    source_id: str
    claim: str
    kind: FormationEvidenceKind

    def is_usable(self) -> bool:
        return bool(self.source_id.strip() and self.claim.strip())


@dataclass(frozen=True)
class ComplementaryWorldNode:
    """A heterogeneous node that may participate in a latent connection.

    ``node_type`` is intentionally open-ended. It may describe a person, group,
    organization, asset, channel, data source, space, equipment, capital, authority,
    software, trust relation, demand stream, or a future node type not yet named.
    Node complementarity alone is not evidence that a latent connection exists.
    """

    node_id: str
    node_type: str
    observed_state: str
    contribution_hypothesis: str
    controller_or_owner: str = "UNKNOWN"
    evidence_refs: tuple[str, ...] = ()

    def is_usable(self) -> bool:
        return bool(
            self.node_id.strip()
            and self.node_type.strip()
            and self.observed_state.strip()
            and self.contribution_hypothesis.strip()
            and self.evidence_refs
            and all(isinstance(ref, str) and ref.strip() for ref in self.evidence_refs)
        )


@dataclass(frozen=True)
class ContradictionEvidence:
    source_id: str
    claim: str
    material: bool = True
    resolved: bool = False

    def is_usable(self) -> bool:
        return bool(self.source_id.strip() and self.claim.strip())


@dataclass(frozen=True)
class LatentValueFormationHypothesis:
    """A pre-demand hypothesis about value that may be formed by recombination.

    The origin actor is represented as an aggregate segment or non-personal actor
    class. Psychology evidence must come from ``PsychologySnapshot`` records with
    provenance retained by the psychology tracker.

    ``counterfactual_exchange_design`` is retained for schema compatibility, but its
    semantics are downstream: it describes minimum execution mechanics for an
    already-evidenced latent connection. It is not evidence that the connection
    exists and cannot by itself make the hypothesis validation-ready.
    """

    candidate_id: str
    actor_segment: str
    geography: str
    objective_endowments: tuple[str, ...]
    observed_state: str
    observed_change: str
    underused_or_misaligned_value: str
    resource_psychology_disequilibrium: str
    observed_behavior: str
    latent_outcome_hypothesis: str
    complementary_nodes: Sequence[ComplementaryWorldNode]
    counterfactual_exchange_design: str
    why_exchange_does_not_already_happen: str
    incremental_value_for_origin_actor: str
    incremental_value_for_complementary_nodes: str
    orchestrator_value_capture_hypothesis: str
    cheapest_decisive_validation: str
    kill_conditions: str
    surface_phenomenon_or_friction: str = ""
    structural_friction_hypothesis: str = ""
    structural_friction_truth_state: StructuralFrictionTruthState = (
        StructuralFrictionTruthState.INFERRED
    )
    alternative_explanations: tuple[str, ...] = ()
    resource_state_disequilibrium: str = ""
    causal_descent: CausalDescentRecord | None = None
    connection_pressure_hypothesis: str = ""
    observed_missing_edge: str = ""
    latent_connection_hypothesis: str = ""
    psychology_snapshots: Sequence[PsychologySnapshot] = field(default_factory=tuple)
    evidence: Sequence[FormationEvidenceRef] = field(default_factory=tuple)
    contradictions: Sequence[ContradictionEvidence] = field(default_factory=tuple)


_REQUIRED_TEXT_FIELDS = (
    "candidate_id",
    "actor_segment",
    "geography",
    "observed_state",
    "observed_change",
    "underused_or_misaligned_value",
    "observed_behavior",
    "latent_outcome_hypothesis",
    "surface_phenomenon_or_friction",
    "structural_friction_hypothesis",
    "connection_pressure_hypothesis",
    "observed_missing_edge",
    "latent_connection_hypothesis",
    "counterfactual_exchange_design",
    "why_exchange_does_not_already_happen",
    "incremental_value_for_origin_actor",
    "incremental_value_for_complementary_nodes",
    "orchestrator_value_capture_hypothesis",
    "cheapest_decisive_validation",
    "kill_conditions",
)

_VALIDATION_EVIDENCE_KINDS = frozenset(
    {
        FormationEvidenceKind.OBJECTIVE_ENDOWMENT,
        FormationEvidenceKind.ORIGIN_STATE,
        FormationEvidenceKind.ORIGIN_CHANGE,
        FormationEvidenceKind.UNDERUSE_MISALIGNMENT,
        FormationEvidenceKind.OBSERVED_BEHAVIOR,
        FormationEvidenceKind.STRUCTURAL_FRICTION,
        FormationEvidenceKind.COMPLEMENTARY_NODE,
        FormationEvidenceKind.CONNECTION_PRESSURE,
    }
)


def evidence_kinds(
    hypothesis: LatentValueFormationHypothesis,
) -> set[FormationEvidenceKind]:
    return {item.kind for item in hypothesis.evidence if item.is_usable()}


def missing_validation_evidence(
    hypothesis: LatentValueFormationHypothesis,
) -> list[FormationEvidenceKind]:
    present = evidence_kinds(hypothesis)
    missing = set(_VALIDATION_EVIDENCE_KINDS - present)
    if not {
        FormationEvidenceKind.MISSING_EDGE,
        FormationEvidenceKind.STRANDING_BARRIER,
    }.intersection(present):
        missing.add(FormationEvidenceKind.MISSING_EDGE)
    return sorted(missing, key=lambda item: item.value)


def _usable_psychology_snapshots(
    hypothesis: LatentValueFormationHypothesis,
) -> list[PsychologySnapshot]:
    return [
        snapshot
        for snapshot in hypothesis.psychology_snapshots
        if snapshot.actor_segment == hypothesis.actor_segment
        and snapshot.supporting_evidence_refs
    ]


def _has_perception_or_motive(
    hypothesis: LatentValueFormationHypothesis,
) -> bool:
    return any(
        snapshot.semantic_primitive in {"PERCEPTION", "MOTIVE"}
        for snapshot in _usable_psychology_snapshots(hypothesis)
    )


def _has_behavior_corroboration(
    hypothesis: LatentValueFormationHypothesis,
) -> bool:
    for snapshot in _usable_psychology_snapshots(hypothesis):
        if snapshot.semantic_primitive == "BEHAVIOR" and snapshot.supporting_evidence_refs:
            return True
        if snapshot.behavior_evidence_refs:
            return True
    return False


def _material_unresolved_contradictions(
    hypothesis: LatentValueFormationHypothesis,
) -> list[ContradictionEvidence]:
    return [
        item
        for item in hypothesis.contradictions
        if item.is_usable() and item.material and not item.resolved
    ]


def validate_formation(
    hypothesis: LatentValueFormationHypothesis,
) -> list[str]:
    """Return fail-closed errors before a hypothesis becomes validation-ready.

    ``VALIDATION_READY`` means that objective evidence shows enough directional
    pressure toward the proposed latent connection to justify spending scarce human
    or external validation capital on the remaining decisive uncertainty. It does
    not mean paid need, payer, resource control, willingness to pay, or
    transactionability has been established.
    """

    errors: list[str] = []

    for name in _REQUIRED_TEXT_FIELDS:
        value = getattr(hypothesis, name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing:{name}")

    if not hypothesis.objective_endowments:
        errors.append("missing:objective_endowments")
    elif any(
        not isinstance(value, str) or not value.strip()
        for value in hypothesis.objective_endowments
    ):
        errors.append("invalid:objective_endowments")

    usable_evidence = [item for item in hypothesis.evidence if item.is_usable()]
    if not usable_evidence:
        errors.append("missing:evidence")

    for kind in missing_validation_evidence(hypothesis):
        errors.append(f"missing:evidence_kind:{kind.value}")

    usable_psychology = _usable_psychology_snapshots(hypothesis)
    if usable_psychology and not _has_behavior_corroboration(hypothesis):
        errors.append("missing:psychology_behavior_corroboration")

    if not (
        hypothesis.resource_state_disequilibrium.strip()
        or hypothesis.resource_psychology_disequilibrium.strip()
    ):
        errors.append("missing:resource_state_or_psychology_disequilibrium")

    if hypothesis.structural_friction_truth_state is not StructuralFrictionTruthState.EVIDENCED_STRUCTURE:
        errors.append("structural_friction_not_evidenced")

    if hypothesis.causal_descent is None:
        errors.append("missing:causal_descent")
    else:
        if hypothesis.causal_descent.actor != hypothesis.actor_segment:
            errors.append("causal_descent_actor_mismatch")
        for causal_error in validate_causal_descent_for_promotion(
            hypothesis.causal_descent
        ):
            errors.append(f"causal_descent:{causal_error}")

    if not hypothesis.alternative_explanations:
        errors.append("missing:alternative_explanations")
    elif any(
        not isinstance(value, str) or not value.strip()
        for value in hypothesis.alternative_explanations
    ):
        errors.append("invalid:alternative_explanations")

    for snapshot in hypothesis.psychology_snapshots:
        if snapshot.actor_segment != hypothesis.actor_segment:
            errors.append(
                f"psychology_actor_segment_mismatch:{snapshot.actor_segment}"
            )

    if not hypothesis.complementary_nodes:
        errors.append("missing:complementary_nodes")
    else:
        invalid_nodes = [
            node.node_id or "UNKNOWN"
            for node in hypothesis.complementary_nodes
            if not node.is_usable()
        ]
        for node_id in invalid_nodes:
            errors.append(f"invalid:complementary_node:{node_id}")

    if _material_unresolved_contradictions(hypothesis):
        errors.append("unresolved_material_contradiction")

    return errors


def formation_state(hypothesis: LatentValueFormationHypothesis) -> FormationState:
    """Infer formation maturity without silently manufacturing connection truth."""

    kinds = evidence_kinds(hypothesis)
    objective_core = {
        FormationEvidenceKind.OBJECTIVE_ENDOWMENT,
        FormationEvidenceKind.ORIGIN_STATE,
        FormationEvidenceKind.ORIGIN_CHANGE,
    }.issubset(kinds)

    if not objective_core or not hypothesis.objective_endowments:
        return FormationState.OBSERVED_TRANSITION

    if not (
        hypothesis.underused_or_misaligned_value.strip()
        and (
            hypothesis.resource_state_disequilibrium.strip()
            or hypothesis.resource_psychology_disequilibrium.strip()
        )
    ):
        return FormationState.RESOURCE_PSYCHOLOGY_MISALIGNMENT_HYPOTHESIS

    if not (
        FormationEvidenceKind.UNDERUSE_MISALIGNMENT in kinds
        and FormationEvidenceKind.OBSERVED_BEHAVIOR in kinds
        and _has_behavior_corroboration(hypothesis)
        and hypothesis.latent_outcome_hypothesis.strip()
    ):
        return FormationState.RESOURCE_PSYCHOLOGY_MISALIGNMENT_HYPOTHESIS

    if not (
        hypothesis.surface_phenomenon_or_friction.strip()
        and hypothesis.structural_friction_hypothesis.strip()
        and hypothesis.alternative_explanations
        and FormationEvidenceKind.STRUCTURAL_FRICTION in kinds
        and hypothesis.structural_friction_truth_state
        is StructuralFrictionTruthState.EVIDENCED_STRUCTURE
        and hypothesis.causal_descent is not None
        and causal_descent_state(hypothesis.causal_descent)
        is CausalDescentState.EVIDENCED_STRUCTURAL_FRICTION
        and not validate_causal_descent_for_promotion(hypothesis.causal_descent)
    ):
        return FormationState.STRUCTURAL_FRICTION_HYPOTHESIS

    if not (
        hypothesis.complementary_nodes
        and FormationEvidenceKind.COMPLEMENTARY_NODE in kinds
    ):
        return FormationState.STRUCTURAL_FRICTION_EVIDENCED

    if not (
        hypothesis.connection_pressure_hypothesis.strip()
        and FormationEvidenceKind.CONNECTION_PRESSURE in kinds
        and hypothesis.observed_missing_edge.strip()
        and {
            FormationEvidenceKind.MISSING_EDGE,
            FormationEvidenceKind.STRANDING_BARRIER,
        }.intersection(kinds)
        and hypothesis.latent_connection_hypothesis.strip()
    ):
        return FormationState.COMPLEMENTARITY_HYPOTHESIS

    if _material_unresolved_contradictions(hypothesis):
        return FormationState.COMPLEMENTARITY_HYPOTHESIS

    if not (
        hypothesis.counterfactual_exchange_design.strip()
        and hypothesis.why_exchange_does_not_already_happen.strip()
    ):
        return FormationState.LATENT_CONNECTION_EVIDENCED

    if validate_formation(hypothesis):
        return FormationState.LATENT_CONNECTION_EVIDENCED

    return FormationState.VALIDATION_READY


def _map_evidence_kind(kind: FormationEvidenceKind) -> EvidenceKind:
    if kind in {
        FormationEvidenceKind.OBJECTIVE_ENDOWMENT,
        FormationEvidenceKind.ORIGIN_STATE,
        FormationEvidenceKind.UNDERUSE_MISALIGNMENT,
        FormationEvidenceKind.OBSERVED_BEHAVIOR,
    }:
        return EvidenceKind.ORIGIN_STATE
    if kind is FormationEvidenceKind.ORIGIN_CHANGE:
        return EvidenceKind.ORIGIN_CHANGE
    if kind is FormationEvidenceKind.STRUCTURAL_FRICTION:
        return EvidenceKind.STRUCTURAL_FRICTION
    if kind is FormationEvidenceKind.COMPLEMENTARY_NODE:
        return EvidenceKind.COMPLEMENTARY_STATE
    if kind in {
        FormationEvidenceKind.MISSING_EDGE,
        FormationEvidenceKind.STRANDING_BARRIER,
    }:
        return EvidenceKind.STRANDING_BARRIER
    if kind is FormationEvidenceKind.COUNTERFACTUAL_PRECEDENT:
        return EvidenceKind.VALUE_PRECEDENT
    # Connection pressure is a formation-level relationship observation. The
    # canonical discovery model currently has no dedicated relationship evidence
    # enum, so preserve it as GENERAL_PATTERN rather than inventing a false state.
    return EvidenceKind.GENERAL_PATTERN


def to_latent_value_candidate(
    hypothesis: LatentValueFormationHypothesis,
) -> LatentValueCandidate:
    """Project a validated formation into the canonical latent-value model.

    Projection is intentionally unavailable before ``VALIDATION_READY``. Even after
    projection, the result remains ``LATENT_VALUE_DISCOVERY``; it does not create a
    NeedSignal, payer, payment evidence, ResourceSignal or route-testable status.
    """

    if formation_state(hypothesis) is not FormationState.VALIDATION_READY:
        raise ValueError("formation must be VALIDATION_READY before projection")

    nodes = [node for node in hypothesis.complementary_nodes if node.is_usable()]
    node_hypothesis = "; ".join(
        f"{node.node_type}:{node.node_id} -> {node.contribution_hypothesis}"
        for node in nodes
    )
    node_states = "; ".join(
        f"{node.node_type}:{node.node_id} = {node.observed_state}" for node in nodes
    )

    evidence = tuple(
        EvidenceRef(
            source_id=item.source_id,
            claim=item.claim,
            kind=_map_evidence_kind(item.kind),
        )
        for item in hypothesis.evidence
        if item.is_usable()
    )

    return LatentValueCandidate(
        candidate_id=hypothesis.candidate_id,
        actor=hypothesis.actor_segment,
        observed_state=hypothesis.observed_state,
        observed_change=hypothesis.observed_change,
        hidden_or_underrecognized_value=hypothesis.underused_or_misaligned_value,
        why_value_is_not_recognized_or_realized=(
            hypothesis.resource_state_disequilibrium
            or hypothesis.resource_psychology_disequilibrium
        ),
        complementary_actor_hypothesis=node_hypothesis,
        complementary_actor_state=node_states,
        transformation_mechanism=hypothesis.counterfactual_exchange_design,
        why_exchange_does_not_already_happen=(
            hypothesis.why_exchange_does_not_already_happen
        ),
        incremental_value_for_origin_actor=(
            hypothesis.incremental_value_for_origin_actor
        ),
        incremental_value_for_complementary_actor=(
            hypothesis.incremental_value_for_complementary_nodes
        ),
        orchestrator_value_capture_hypothesis=(
            hypothesis.orchestrator_value_capture_hypothesis
        ),
        cheapest_decisive_validation=hypothesis.cheapest_decisive_validation,
        kill_conditions=hypothesis.kill_conditions,
        surface_phenomenon_or_friction=hypothesis.surface_phenomenon_or_friction,
        latent_outcome_hypothesis=hypothesis.latent_outcome_hypothesis,
        structural_friction_hypothesis=hypothesis.structural_friction_hypothesis,
        structural_friction_truth_state=hypothesis.structural_friction_truth_state.value,
        alternative_explanations=hypothesis.alternative_explanations,
        evidence=evidence,
        source_mode="LATENT_VALUE_DISCOVERY",
    )


GOVERNING_INVARIANTS = (
    "OBJECTIVE_RESOURCE_NE_UTILIZED_RESOURCE",
    "PSYCHOLOGY_SIGNAL_NE_DEMAND",
    "PSYCHOLOGY_EVIDENCE_NE_UNIVERSAL_FORMATION_GATE",
    "OBJECTIVE_CAUSAL_EVIDENCE_MAY_FORM_STRUCTURE_WITHOUT_PSYCHOLOGY",
    "MOTIVE_HYPOTHESIS_NE_WILLINGNESS_TO_PAY",
    "BEHAVIOR_SIGNAL_NE_TRANSACTION",
    "SURFACE_FRICTION_NE_STRUCTURAL_FRICTION",
    "STRUCTURAL_FRICTION_HYPOTHESIS_NE_EVIDENCED_STRUCTURAL_FRICTION",
    "ONE_PLAUSIBLE_CAUSE_NE_STRUCTURAL_TRUTH",
    "CAUSAL_DESCENT_STOPS_AT_DECISION_USEFUL_FALSIFIABLE_FRONTIER",
    "STRUCTURAL_FRICTION_NE_MISSING_EDGE",
    "BUYER_COST_FIRST_NE_CONSTITUTION",
    "CONNECTION_INVENTION_NE_CONNECTION_DISCOVERY",
    "COMPLEMENTARITY_NE_LATENT_CONNECTION",
    "CONNECTION_HYPOTHESIS_NE_CONNECTION_PRESSURE_EVIDENCE",
    "COUNTERFACTUAL_EXCHANGE_NE_LATENT_CONNECTION_EVIDENCE",
    "LATENT_CONNECTION_NE_ACCEPTED_EXCHANGE",
    "COUNTERFACTUAL_EXCHANGE_NE_ACCEPTED_EXCHANGE",
    "LATENT_VALUE_FORMATION_NE_COMMERCIAL_OPPORTUNITY",
    "COMPLEMENTARITY_NE_TRANSACTIONABILITY",
    "ACTOR_SEGMENT_NE_INDIVIDUAL_PSYCHOGRAPHIC_PROFILE",
    "UNKNOWN_NE_PASS",
)
