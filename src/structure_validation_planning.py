"""Plan bounded real-world validation for a STRUCTURE_VALIDATION_READY candidate.

This layer is deliberately non-canonical. Tasks and packets are execution plans,
not evidence. They cannot promote taxonomy, opportunity, route, payer or business
truth. Domain-specific details belong in a reviewed validation profile rather than
being hard-coded into the core planning model.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Mapping


QUEUE_KIND = "STRUCTURE_EVIDENCE_ACQUISITION"
PACKET_KIND = "DELEGATABLE_STRUCTURE_VALIDATION"
PROFILE_SCHEMA_VERSION = "structure-validation-profile.v1"

_DEFAULT_PROFILE: dict[str, Any] = {
    "profile_id": "GENERIC_STRUCTURE_VALIDATION_V1",
    "candidate_concept": None,
    "geography_scope": ["CN-JS-XUZHOU", "CN-JS"],
    "case_unit": "BOUNDED_CURRENT_STRUCTURE_CASE",
    "target_case_count_min": 5,
    "target_case_count_max": 10,
    "min_independent_focal_actors": 3,
    "min_later_cases": 2,
    "min_independent_focal_actors_in_later_cases": 2,
    "local_case_required_fields": [
        "case_id",
        "focal_actor",
        "actor_roles",
        "geography",
        "current_state",
        "recurring_event_type",
        "transformation_or_routing_steps",
        "constraints",
        "search_minutes",
        "coordination_minutes",
        "handoff_count",
        "qa_rework_count",
        "cycle_days",
        "outcome_state",
        "source_refs",
    ],
    "local_paid_required_fields": [
        "mandate_id",
        "payer_actor",
        "provider_actor",
        "service_scope",
        "payment_basis",
        "settlement_state",
        "settled_amount",
        "settlement_date",
        "source_refs",
    ],
    "compounding_reuse_fields": [
        "reused_case_refs",
        "reused_template_refs",
        "reused_rule_refs",
        "reused_routing_refs",
        "reused_prior_outcome_refs",
    ],
    "compounding_metrics": [
        "search_minutes",
        "coordination_minutes",
        "handoff_count",
        "qa_rework_count",
        "cycle_days",
        "acceptance_state",
    ],
    "privacy_constraints": [],
    "prohibited_fields": [],
}

_ALLOWED_PROFILE_FIELDS = frozenset(_DEFAULT_PROFILE)


def _string_list(value: object, name: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be an array")
    values = [str(item).strip() for item in value if str(item).strip()]
    if len(values) != len(value):
        raise ValueError(f"{name} must contain non-empty strings only")
    if not allow_empty and not values:
        raise ValueError(f"{name} cannot be empty")
    if len(values) != len(set(values)):
        raise ValueError(f"{name} cannot contain duplicates")
    return values


def _positive_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def normalize_structure_validation_profile(
    profile: Mapping[str, Any] | None,
    *,
    candidate_concept: str,
) -> dict[str, Any]:
    """Return a strict domain profile while keeping the planner domain-agnostic."""

    merged = dict(_DEFAULT_PROFILE)
    if profile is not None:
        unknown = sorted(set(profile) - _ALLOWED_PROFILE_FIELDS)
        if unknown:
            raise ValueError(f"unknown structure validation profile fields: {unknown}")
        merged.update(profile)

    profile_id = str(merged.get("profile_id") or "").strip()
    if not profile_id:
        raise ValueError("validation profile_id is required")
    declared_concept = merged.get("candidate_concept")
    if declared_concept is not None and str(declared_concept).strip() != candidate_concept:
        raise ValueError("validation profile candidate_concept does not match structure artifact")

    case_unit = str(merged.get("case_unit") or "").strip()
    if not case_unit:
        raise ValueError("validation profile case_unit is required")

    result = {
        "schema_version": PROFILE_SCHEMA_VERSION,
        "profile_id": profile_id,
        "candidate_concept": candidate_concept,
        "geography_scope": _string_list(merged.get("geography_scope"), "geography_scope"),
        "case_unit": case_unit,
        "target_case_count_min": _positive_int(merged.get("target_case_count_min"), "target_case_count_min"),
        "target_case_count_max": _positive_int(merged.get("target_case_count_max"), "target_case_count_max"),
        "min_independent_focal_actors": _positive_int(
            merged.get("min_independent_focal_actors"), "min_independent_focal_actors"
        ),
        "min_later_cases": _positive_int(merged.get("min_later_cases"), "min_later_cases"),
        "min_independent_focal_actors_in_later_cases": _positive_int(
            merged.get("min_independent_focal_actors_in_later_cases"),
            "min_independent_focal_actors_in_later_cases",
        ),
        "local_case_required_fields": _string_list(
            merged.get("local_case_required_fields"), "local_case_required_fields"
        ),
        "local_paid_required_fields": _string_list(
            merged.get("local_paid_required_fields"), "local_paid_required_fields"
        ),
        "compounding_reuse_fields": _string_list(
            merged.get("compounding_reuse_fields"), "compounding_reuse_fields"
        ),
        "compounding_metrics": _string_list(merged.get("compounding_metrics"), "compounding_metrics"),
        "privacy_constraints": _string_list(
            merged.get("privacy_constraints", []), "privacy_constraints", allow_empty=True
        ),
        "prohibited_fields": _string_list(
            merged.get("prohibited_fields", []), "prohibited_fields", allow_empty=True
        ),
    }
    if result["target_case_count_max"] < result["target_case_count_min"]:
        raise ValueError("target_case_count_max cannot be below target_case_count_min")

    prohibited = set(result["prohibited_fields"])
    required = (
        set(result["local_case_required_fields"])
        | set(result["local_paid_required_fields"])
        | set(result["compounding_reuse_fields"])
        | set(result["compounding_metrics"])
    )
    overlap = sorted(prohibited & required)
    if overlap:
        raise ValueError(f"prohibited fields cannot be required: {overlap}")
    return result


def _require_ready(artifact: Mapping[str, Any]) -> tuple[str, str]:
    if artifact.get("commercial_structure_state") != "STRUCTURE_VALIDATION_READY":
        raise ValueError("structure validation planning requires STRUCTURE_VALIDATION_READY")
    if artifact.get("business_promotion") != "NOT_PROMOTED":
        raise ValueError("validation planning cannot start from promoted business truth")
    candidate_id = str(artifact.get("candidate_id") or "").strip()
    concept = str(artifact.get("candidate_concept") or "").strip()
    if not candidate_id or not concept:
        raise ValueError("candidate identity is required")
    missing = tuple(str(v) for v in artifact.get("missing_dimensions", []) if str(v))
    if missing != ("COMPOUNDING",):
        raise ValueError("this validation plan is scoped to the single remaining COMPOUNDING gap")
    return candidate_id, concept


def build_structure_validation_queue(
    artifact: Mapping[str, Any],
    *,
    profile: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    candidate_id, concept = _require_ready(artifact)
    resolved = normalize_structure_validation_profile(profile, candidate_concept=concept)
    geographies = resolved["geography_scope"]
    privacy = resolved["privacy_constraints"]

    tasks = [
        {
            "task_id": f"VALIDATE_STRUCTURE::{candidate_id}::LOCAL_CASE_PANEL",
            "candidate_id": candidate_id,
            "candidate_concept": concept,
            "task_role": "LOCAL_TRANSFERABILITY_PREREQUISITE",
            "target_gate": "LOCAL_CASE_PANEL",
            "priority": 10,
            "geography_scope": geographies,
            "instruction": (
                "Collect a bounded panel of current comparable structure/process cases across independent focal actors. "
                "Use the same reviewed schema and predeclared execution metrics for every case; preserve negative cases."
            ),
            "pass_condition": (
                f"At least {resolved['target_case_count_min']} current comparable cases across at least "
                f"{resolved['min_independent_focal_actors']} independent focal actors have auditable source identity, "
                "complete reviewed fields and predeclared metrics."
            ),
            "fail_condition": (
                "Cases are historical anecdotes, duplicate representations of the same event, lack actor/source identity, "
                "or cannot be represented through the same bounded comparable schema."
            ),
            "forbidden_inference": (
                "policy mention, network participation, public listing or provider designation != willingness, availability, "
                "settlement, transactionability or paid mandate"
            ),
            "capture_contract": {
                "case_unit": resolved["case_unit"],
                "target_case_count_min": resolved["target_case_count_min"],
                "target_case_count_max": resolved["target_case_count_max"],
                "min_independent_focal_actors": resolved["min_independent_focal_actors"],
                "required_fields": resolved["local_case_required_fields"],
                "privacy_constraints": privacy,
                "prohibited_fields": resolved["prohibited_fields"],
            },
            "state_effect": "NONE_UNTIL_CAPTURED_EVIDENCE_IS_REVIEWED",
        },
        {
            "task_id": f"VALIDATE_STRUCTURE::{candidate_id}::LOCAL_PAID_MANDATES",
            "candidate_id": candidate_id,
            "candidate_concept": concept,
            "task_role": "LOCAL_MONETIZATION_CORROBORATION",
            "target_gate": "LOCAL_PAID_MANDATE",
            "priority": 20,
            "geography_scope": geographies,
            "instruction": (
                "Corroborate at least two distinct local/regional paid mandates for the same bounded service/orchestration class "
                "using first-party settlement or payment evidence. Contract/award evidence may be retained but cannot substitute for settlement."
            ),
            "pass_condition": (
                "Two or more independent mandates identify payer, provider, bounded service scope, settlement/payment state, "
                "amount or payment basis, date and first-party source evidence."
            ),
            "fail_condition": (
                "Evidence stops at policy, budget, asking price, award, unsigned intent, signed contract without settlement/payment, "
                "or provider marketing."
            ),
            "forbidden_inference": (
                "national service-class monetization != our revenue or local buyer willingness; budget/award/signed contract != settlement"
            ),
            "capture_contract": {
                "min_distinct_paid_mandates": 2,
                "required_fields": resolved["local_paid_required_fields"],
                "privacy_constraints": privacy,
                "prohibited_fields": resolved["prohibited_fields"],
            },
            "state_effect": "LOCAL_CORROBORATION_ONLY_NOT_GLOBAL_GATE_PROMOTION",
        },
        {
            "task_id": f"VALIDATE_STRUCTURE::{candidate_id}::COMPOUNDING",
            "candidate_id": candidate_id,
            "candidate_concept": concept,
            "task_role": "CORE_MISSING_DIMENSION",
            "target_gate": "COMPOUNDING",
            "priority": 30,
            "geography_scope": geographies,
            "depends_on": [f"VALIDATE_STRUCTURE::{candidate_id}::LOCAL_CASE_PANEL"],
            "instruction": (
                "Use time-ordered later comparable cases to test whether specific reusable artifacts from prior cases "
                "measurably improve later execution economics, reliability or acceptance while controlling for obvious case differences."
            ),
            "pass_condition": (
                f"At least {resolved['min_later_cases']} later cases across at least "
                f"{resolved['min_independent_focal_actors_in_later_cases']} independent focal actors explicitly reuse prior "
                "data/templates/rules/routing/trust/outcome artifacts and show measurable improvement on at least two "
                "predeclared metrics without degrading acceptance/quality; provenance and reused-artifact refs are preserved."
            ),
            "fail_condition": (
                "Later cases show no measurable improvement, still require materially bespoke operator work from zero, "
                "or observed improvement cannot be linked to a reused artifact/rule/data/trust/outcome asset after considering confounders."
            ),
            "forbidden_inference": (
                "database size, platform adoption, automation, one-time efficiency gain, repeated revenue or case count != compounding"
            ),
            "capture_contract": {
                "case_unit": resolved["case_unit"],
                "min_later_cases": resolved["min_later_cases"],
                "min_independent_focal_actors_in_later_cases": resolved[
                    "min_independent_focal_actors_in_later_cases"
                ],
                "required_reuse_fields": resolved["compounding_reuse_fields"],
                "predeclared_metrics": resolved["compounding_metrics"],
                "comparison_policy": "COMPARE_TIME_ORDERED_LATER_CASES_WITH_PRIOR_COMPARABLE_CASE_BASELINE",
                "privacy_constraints": privacy,
                "prohibited_fields": resolved["prohibited_fields"],
            },
            "state_effect": "NONE_UNTIL_OUTCOME_LINKED_EVIDENCE_IS_REVIEWED_AND_GATE_REBUILT",
        },
    ]
    return {
        "queue_kind": QUEUE_KIND,
        "candidate_id": candidate_id,
        "candidate_concept": concept,
        "validation_profile": resolved,
        "source_structure_state": artifact.get("commercial_structure_state"),
        "source_missing_dimensions": list(artifact.get("missing_dimensions", [])),
        "task_count": len(tasks),
        "target_counts": dict(sorted(Counter(task["target_gate"] for task in tasks).items())),
        "tasks": tasks,
        "business_promotion": "NOT_PROMOTED",
        "truth_notes": [
            "This queue is a planning artifact, not evidence and not a business recommendation.",
            "Only COMPOUNDING is a missing core structure dimension; local case and paid-mandate tasks are prerequisites/corroboration.",
            "National repeat monetization evidence does not prove our revenue or local buyer willingness.",
            "Contract/award evidence does not prove settlement; network participation does not prove spare capacity.",
            "Digitalization and data accumulation do not prove compounding without time-ordered later-case outcome measurements.",
            "Domain-specific collection requirements belong in the reviewed validation profile, not in the core planner ontology.",
        ],
    }


def build_structure_field_packets(queue: Mapping[str, Any]) -> dict[str, Any]:
    if queue.get("queue_kind") != QUEUE_KIND:
        raise ValueError("unexpected structure validation queue kind")
    if queue.get("business_promotion") != "NOT_PROMOTED":
        raise ValueError("field packets cannot originate from promoted business truth")

    profile = queue.get("validation_profile")
    if not isinstance(profile, Mapping):
        raise ValueError("structure validation queue requires validation_profile")
    privacy = list(profile.get("privacy_constraints", []))

    packets = []
    for task in queue.get("tasks", []) or []:
        if not isinstance(task, Mapping):
            raise ValueError("structure validation task must be an object")
        target = str(task.get("target_gate") or "")
        questions = {
            "LOCAL_CASE_PANEL": [
                "这个 bounded case / process event 的 actor 与角色是什么，当前状态和 recurring event 是什么？",
                "哪些步骤、约束、接口与验收条件在不同案例中稳定重复，哪些必须保留为 case-specific？",
                "完整记录搜索、协调、交接、返工和总周期等预声明指标，不凭印象估算。",
                "保留失败、异常和无法比较的案例；不要为了形成模式而删除反例。",
            ],
            "LOCAL_PAID_MANDATE": [
                "谁是实际付款主体，谁是服务提供方，服务边界是什么？",
                "优先保存第一方 settlement/payment 证据；预算、中标、签约合同只能按各自真实状态记录。",
                "确认这是独立 mandate，而不是同一合同/交易的重复页面或不同公告。",
            ],
            "COMPOUNDING": [
                "本案具体复用了此前哪条数据、模板、规则、routing 路径、可信关系或 prior outcome？",
                "复用前后的预声明 search/coordination/handoff/QA/cycle/acceptance 指标分别是多少？",
                "如果变快、变便宜或更可靠，是否存在案例更简单、角色更少、政策变化等替代解释？",
                "如果没有改善或仍需从零设计，按否证记录，不把熟练度、自动化或案例数量解释成 compounding。",
            ],
        }.get(target)
        if questions is None:
            raise ValueError(f"unsupported structure field target: {target}")
        if privacy:
            questions.append("严格遵守 validation profile 的 privacy/prohibited-field 边界，只采集完成该验证所必需的最小信息。")
        packets.append({
            "packet_id": f"FIELD::{task.get('task_id')}",
            "task_id": task.get("task_id"),
            "candidate_id": task.get("candidate_id"),
            "candidate_concept": task.get("candidate_concept"),
            "validation_profile_id": profile.get("profile_id"),
            "case_unit": profile.get("case_unit"),
            "target_gate": target,
            "task_role": task.get("task_role"),
            "geography_scope": task.get("geography_scope"),
            "execution_owner": "DELEGATABLE_FIELD_AGENT_OR_AUTHORIZED_REMOTE_RESEARCHER",
            "objective": task.get("instruction"),
            "questions": questions,
            "pass_condition": task.get("pass_condition"),
            "fail_condition": task.get("fail_condition"),
            "forbidden_inference": task.get("forbidden_inference"),
            "capture_contract": task.get("capture_contract"),
            "privacy_constraints": privacy,
            "depends_on": task.get("depends_on", []),
            "state_effect": task.get("state_effect"),
        })
    return {
        "packet_kind": PACKET_KIND,
        "candidate_id": queue.get("candidate_id"),
        "validation_profile_id": profile.get("profile_id"),
        "packet_count": len(packets),
        "packets": packets,
        "business_promotion": "NOT_PROMOTED",
        "truth_notes": [
            "Packets are instructions for evidence collection, not evidence themselves.",
            "A completed questionnaire without source material does not satisfy any canonical gate.",
            "Observed negative results and kill conditions must be preserved rather than optimized away.",
            "Collect only the minimum authorized information required by the validation profile.",
        ],
    }
