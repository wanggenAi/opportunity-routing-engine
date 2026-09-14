"""Sustainability guard between observed recurrence and business archetypes.

An ``OBSERVED_PATTERN`` is evidence that a structure recurs.  It is not evidence
that the structure is standardizable, repeatedly monetizable, compounding, or
attached to a naturally regenerating event source.  This module makes those
unknowns explicit before any archetype/business promotion is allowed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


SUSTAINABILITY_SCHEMA_VERSION = "pattern-sustainability.v1"
AXIS_STATES = frozenset({"EVIDENCED", "UNKNOWN"})
CORE_BUSINESS_STATE = "PATTERN_ONLY"
BUSINESS_PROMOTION = "NOT_PROMOTED"
SUSTAINABILITY_AXES = (
    "RECURRENCE",
    "POPULATION",
    "STANDARDIZABILITY",
    "REPEAT_MONETIZATION",
    "COMPOUNDING",
)


@dataclass(frozen=True)
class SustainabilityAxis:
    state: str
    evidence_refs: tuple[str, ...]
    rationale: str

    def __post_init__(self) -> None:
        if self.state not in AXIS_STATES:
            raise ValueError(f"unsupported sustainability axis state: {self.state}")
        if self.state == "EVIDENCED" and not self.evidence_refs:
            raise ValueError("EVIDENCED sustainability axis requires evidence refs")
        if not self.rationale.strip():
            raise ValueError("sustainability axis rationale is required")


@dataclass(frozen=True)
class PatternSustainabilityAssessment:
    pattern_id: str
    primitive: str
    concept: str
    geography: str
    source_pattern_state: str
    axes: dict[str, SustainabilityAxis]
    regenerating_event_flow: SustainabilityAxis
    complementary_actor_structure: SustainabilityAxis
    core_business_state: str
    business_promotion: str
    missing_core_gates: tuple[str, ...]
    validation_tasks: tuple[dict[str, str], ...]
    source_observation_refs: tuple[str, ...]
    evidence_cautions: tuple[str, ...]
    schema_version: str = SUSTAINABILITY_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.source_pattern_state != "OBSERVED_PATTERN":
            raise ValueError("sustainability assessment requires OBSERVED_PATTERN input")
        if set(self.axes) != set(SUSTAINABILITY_AXES):
            raise ValueError("sustainability axes are incomplete or unexpected")
        if self.core_business_state != CORE_BUSINESS_STATE:
            raise ValueError("pattern evidence alone cannot become a core business candidate")
        if self.business_promotion != BUSINESS_PROMOTION:
            raise ValueError("pattern sustainability guard cannot promote business truth")

    def as_dict(self) -> dict:
        return asdict(self)


def _task(task_type: str, evidence_required: str, falsifier: str) -> dict[str, str]:
    return {
        "task_type": task_type,
        "evidence_required": evidence_required,
        "falsifier": falsifier,
    }


def assess_pattern_sustainability(
    pattern: dict,
    *,
    allow_validation_tasks: bool = True,
) -> PatternSustainabilityAssessment:
    """Assess what an observed pattern proves and, more importantly, does not prove.

    This first gate intentionally has no promotion path beyond ``PATTERN_ONLY``.
    Later evidence from transactions/outcomes or reviewed hypothesis records must be
    joined explicitly; recurrence is never allowed to self-promote into a business.

    When the upstream research scope is calibration/partial, validation tasks may be
    suppressed so framework test patterns do not become an operator execution queue.
    """

    if pattern.get("state") != "OBSERVED_PATTERN":
        raise ValueError("only OBSERVED_PATTERN records may enter sustainability assessment")
    if pattern.get("business_promotion") != "NOT_PROMOTED":
        raise ValueError("source pattern already violated business-promotion boundary")

    observation_refs = tuple(pattern.get("supporting_observation_refs") or ())
    actor_ids = tuple(pattern.get("supporting_actor_ids") or ())
    periods = tuple(pattern.get("supporting_periods") or ())
    if not observation_refs:
        raise ValueError("observed pattern requires observation support")
    if not actor_ids:
        raise ValueError("observed pattern requires actor support for sustainability gate")
    if not periods:
        raise ValueError("observed pattern requires time support for sustainability gate")

    recurrence = SustainabilityAxis(
        state="EVIDENCED",
        evidence_refs=observation_refs,
        rationale=(
            "The source pattern passed direct-observation recurrence and time-persistence "
            "gates. This proves repeated observation, not a Demand Pump."
        ),
    )
    population = SustainabilityAxis(
        state="EVIDENCED",
        evidence_refs=observation_refs,
        rationale=(
            "The source pattern passed the configured distinct-Actor gate. This proves "
            "multi-Actor occurrence inside the observed universe, not market prevalence."
        ),
    )
    standardizability = SustainabilityAxis(
        state="UNKNOWN",
        evidence_refs=(),
        rationale=(
            "Repeated structure does not prove that one reusable transformation, interface, "
            "acceptance rule, or CapabilityUnit template can resolve it."
        ),
    )
    repeat_monetization = SustainabilityAxis(
        state="UNKNOWN",
        evidence_refs=(),
        rationale=(
            "No repeated accepted settlement/payment evidence is supplied by an "
            "ObservedPattern record. Listing values or procurement budgets do not qualify."
        ),
    )
    compounding = SustainabilityAxis(
        state="UNKNOWN",
        evidence_refs=(),
        rationale=(
            "No repeated outcome evidence proves that prior transactions/data/trust/rules "
            "make later routing cheaper, safer, faster, or more reliable."
        ),
    )
    regenerating_event_flow = SustainabilityAxis(
        state="UNKNOWN",
        evidence_refs=(),
        rationale=(
            "Time persistence does not identify the mechanism that naturally regenerates "
            "new task/order/resource events without fresh founder-led hunting."
        ),
    )
    complementary_actor_structure = SustainabilityAxis(
        state="UNKNOWN",
        evidence_refs=(),
        rationale=(
            "Pattern recurrence alone does not establish which complementary Actor class "
            "receives incremental value or why an exchange should exist."
        ),
    )

    axes = {
        "RECURRENCE": recurrence,
        "POPULATION": population,
        "STANDARDIZABILITY": standardizability,
        "REPEAT_MONETIZATION": repeat_monetization,
        "COMPOUNDING": compounding,
    }
    missing = (
        "STANDARDIZABILITY",
        "REPEAT_MONETIZATION",
        "COMPOUNDING",
        "REGENERATING_EVENT_FLOW",
        "COMPLEMENTARY_ACTOR_STRUCTURE",
    )
    candidate_tasks = (
        _task(
            "ESTABLISH_REUSABLE_TRANSFORMATION_MECHANISM",
            "Evidence from multiple independent cases that the same bounded intervention/template changes the repeated state with stable acceptance criteria.",
            "Each case needs materially bespoke founder work or a different transformation mechanism.",
        ),
        _task(
            "ESTABLISH_COMPLEMENTARY_ACTOR_STRUCTURE",
            "Observed counterpart Actor class with a concrete incremental gain from activating or resolving the repeated structure.",
            "No counterpart shows a concrete surplus or actors already transact efficiently without orchestration.",
        ),
        _task(
            "ESTABLISH_REGENERATING_EVENT_FLOW",
            "Evidence of a lifecycle, installed base, workflow, channel, or Actor behavior that naturally emits new events over time.",
            "New events appear only after unrelated founder-led prospecting each time.",
        ),
        _task(
            "ESTABLISH_REPEAT_MONETIZATION",
            "At least repeated accepted economic settlement for the same underlying transformation/route, with payer identity and scope preserved.",
            "Only budgets, asking prices, one-off payment, subsidy intent, or unaccepted quotes are found.",
        ),
        _task(
            "ESTABLISH_COMPOUNDING_MECHANISM",
            "Outcome-linked evidence that prior data, templates, trust, routing, or rules measurably reduce later search/coordination/QA/failure cost or improve acceptance.",
            "Every new event restarts discovery, trust, delivery design, and acquisition from zero.",
        ),
    )
    tasks = candidate_tasks if allow_validation_tasks else ()

    return PatternSustainabilityAssessment(
        pattern_id=str(pattern["pattern_id"]),
        primitive=str(pattern["primitive"]),
        concept=str(pattern["concept"]),
        geography=str(pattern["geography"]),
        source_pattern_state="OBSERVED_PATTERN",
        axes=axes,
        regenerating_event_flow=regenerating_event_flow,
        complementary_actor_structure=complementary_actor_structure,
        core_business_state=CORE_BUSINESS_STATE,
        business_promotion=BUSINESS_PROMOTION,
        missing_core_gates=missing,
        validation_tasks=tasks,
        source_observation_refs=observation_refs,
        evidence_cautions=tuple(pattern.get("evidence_cautions") or ()),
    )


def summarize_pattern_sustainability(
    observed_pattern_artifact: dict,
    *,
    source_pattern_run_id: int | None = None,
) -> dict:
    if observed_pattern_artifact.get("business_promotion") != "NOT_PROMOTED":
        raise ValueError("source pattern artifact violated business-promotion boundary")
    patterns = observed_pattern_artifact.get("patterns")
    if not isinstance(patterns, list):
        raise ValueError("source pattern artifact must contain patterns array")

    research_scope_state = str(
        observed_pattern_artifact.get("research_scope_state") or "CALIBRATION_ONLY"
    )
    validation_execution_authorized = research_scope_state == "BROAD_DISCOVERY_READY"

    assessments = tuple(
        assess_pattern_sustainability(
            pattern,
            allow_validation_tasks=validation_execution_authorized,
        )
        for pattern in patterns
        if isinstance(pattern, dict) and pattern.get("state") == "OBSERVED_PATTERN"
    )
    return {
        "schema_version": SUSTAINABILITY_SCHEMA_VERSION,
        "source_pattern_run_id": source_pattern_run_id,
        "source_observation_run_id": observed_pattern_artifact.get("source_observation_run_id"),
        "source_research_scope_state": research_scope_state,
        "validation_execution_authorized": validation_execution_authorized,
        "source_observed_pattern_count": observed_pattern_artifact.get("observed_pattern_count", 0),
        "assessment_count": len(assessments),
        "validation_task_count": sum(len(item.validation_tasks) for item in assessments),
        "core_business_candidate_count": 0,
        "business_promotion": BUSINESS_PROMOTION,
        "assessment_semantics": "SUSTAINABILITY_GAP_DIAGNOSTIC_NOT_ARCHETYPE_PROMOTION",
        "assessments": [item.as_dict() for item in assessments],
        "governing_invariants": [
            "CALIBRATION_PATTERN_NE_OPERATOR_VALIDATION_BACKLOG",
            "RECURRENCE_NE_DEMAND_PUMP",
            "MULTI_ACTOR_NE_POPULATION_PREVALENCE",
            "REPEATED_STRUCTURE_NE_STANDARDIZABLE_TRANSFORMATION",
            "BUDGET_OR_LISTING_PRICE_NE_REPEAT_MONETIZATION",
            "DATA_ACCUMULATION_NE_COMPOUNDING",
            "PATTERN_NE_ARCHETYPE",
            "PATTERN_NE_REGENERATIVE_LOOP",
            "ONE_TRANSACTION_NE_REPEATABILITY",
            "UNKNOWN_NE_PASS",
        ],
    }
