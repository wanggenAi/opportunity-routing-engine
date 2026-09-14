"""Plan bounded real-world validation for a STRUCTURE_VALIDATION_READY candidate.

This layer is deliberately non-canonical. Tasks and packets are execution plans,
not evidence. They cannot promote taxonomy, opportunity, route, payer or business
truth. The pair-specific validation queue remains unchanged; this module applies
the same fail-closed planning discipline to a higher-level recurrent structure.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Mapping


QUEUE_KIND = "STRUCTURE_EVIDENCE_ACQUISITION"
PACKET_KIND = "DELEGATABLE_STRUCTURE_VALIDATION"


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


def build_structure_validation_queue(artifact: Mapping[str, Any]) -> dict[str, Any]:
    candidate_id, concept = _require_ready(artifact)
    tasks = [
        {
            "task_id": f"VALIDATE_STRUCTURE::{candidate_id}::LOCAL_CASE_PANEL",
            "candidate_id": candidate_id,
            "candidate_concept": concept,
            "task_role": "LOCAL_TRANSFERABILITY_PREREQUISITE",
            "target_gate": "LOCAL_CASE_PANEL",
            "priority": 10,
            "geography_scope": ["CN-JS-XUZHOU", "CN-JS"],
            "instruction": "Collect 5-10 current low-utilization asset cases from at least three independent owners and record the same bounded intake/constraint/transformation fields for every case.",
            "pass_condition": "At least five current cases across at least three independent owners have auditable source/owner identity and a complete comparable case record.",
            "fail_condition": "Cases are historical anecdotes, duplicate assets, lack owner identity, or cannot be represented with a stable comparable intake schema.",
            "forbidden_inference": "public listing or policy mention != owner willingness, delegation, availability or paid mandate",
            "capture_contract": {
                "target_case_count_min": 5,
                "target_case_count_max": 10,
                "min_independent_owners": 3,
                "required_fields": [
                    "case_id", "owner_actor", "asset_identity", "asset_type", "geography",
                    "current_use_state", "underuse_evidence", "rights_constraints",
                    "approval_constraints", "candidate_scenarios", "operator_route",
                    "search_minutes", "coordination_minutes", "approval_step_count",
                    "qa_rework_count", "cycle_days", "outcome_state", "source_refs"
                ],
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
            "geography_scope": ["CN-JS-XUZHOU", "CN-JS"],
            "instruction": "Verify at least two distinct Jiangsu/Xuzhou paid mandates for bounded asset-operation, transaction, repurposing or activation services using first-party contract/settlement/payment records.",
            "pass_condition": "Two or more distinct mandates identify the service scope, payer, provider, settled or paid amount/payment basis, date and first-party source.",
            "fail_condition": "Evidence stops at policy, asking price, tender budget, award, unsigned intent or provider marketing without settlement/payment proof.",
            "forbidden_inference": "national service-class monetization != local paid mandate; tender budget/award != payment",
            "capture_contract": {
                "min_distinct_paid_mandates": 2,
                "required_fields": [
                    "mandate_id", "payer_actor", "provider_actor", "service_scope",
                    "payment_basis", "settled_amount", "settlement_date", "source_refs"
                ],
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
            "geography_scope": ["CN-JS-XUZHOU", "CN-JS"],
            "depends_on": [f"VALIDATE_STRUCTURE::{candidate_id}::LOCAL_CASE_PANEL"],
            "instruction": "Use time-ordered later cases to test whether prior case data, templates, rules, accepted constraints or trusted counterpart knowledge measurably improves later execution economics or reliability.",
            "pass_condition": "At least two later cases across at least two owners explicitly reuse prior artifacts and show measurable improvement on at least two predeclared execution metrics without degrading acceptance/quality; provenance and reused artifact refs are preserved.",
            "fail_condition": "Later cases show no measurable improvement, require materially bespoke founder-led work from zero, or observed improvements cannot be linked to any reused artifact/rule/data/trust asset.",
            "forbidden_inference": "database size, digital platform adoption, repeated revenue or case count != compounding",
            "capture_contract": {
                "min_later_cases": 2,
                "min_independent_owners_in_later_cases": 2,
                "required_reuse_fields": ["reused_case_refs", "reused_template_refs", "reused_rule_refs", "reused_counterparty_refs"],
                "predeclared_metrics": ["search_minutes", "coordination_minutes", "approval_step_count", "qa_rework_count", "cycle_days", "acceptance_state"],
                "comparison_policy": "COMPARE_TIME_ORDERED_LATER_CASES_WITH_PRIOR_COMPARABLE_CASE_BASELINE",
            },
            "state_effect": "NONE_UNTIL_OUTCOME_LINKED_EVIDENCE_IS_REVIEWED_AND_GATE_REBUILT",
        },
    ]
    return {
        "queue_kind": QUEUE_KIND,
        "candidate_id": candidate_id,
        "candidate_concept": concept,
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
            "Digitalization and data accumulation do not prove compounding without later-case outcome measurements.",
        ],
    }


def build_structure_field_packets(queue: Mapping[str, Any]) -> dict[str, Any]:
    if queue.get("queue_kind") != QUEUE_KIND:
        raise ValueError("unexpected structure validation queue kind")
    if queue.get("business_promotion") != "NOT_PROMOTED":
        raise ValueError("field packets cannot originate from promoted business truth")

    packets = []
    for task in queue.get("tasks", []) or []:
        if not isinstance(task, Mapping):
            raise ValueError("structure validation task must be an object")
        target = str(task.get("target_gate") or "")
        questions = {
            "LOCAL_CASE_PANEL": [
                "这个资产现在具体如何使用，什么证据证明低利用/闲置？",
                "权利、用途、审批、消防、改造、招租/运营等约束分别是什么？",
                "从发现资产到形成一个可执行场景，需要经过哪些固定步骤，哪些步骤每次都不同？",
                "完整记录搜索、协调、审批、返工与总周期，不凭印象估算。",
            ],
            "LOCAL_PAID_MANDATE": [
                "谁是实际付款主体，谁是服务提供方，服务边界是什么？",
                "保存合同/结算/付款第一方证据与金额/计费方式；预算、挂牌价、中标价不能替代付款。",
                "确认这是独立 mandate，而不是同一合同的重复页面或同一交易的不同公告。",
            ],
            "COMPOUNDING": [
                "本案具体复用了此前哪一个数据字段、模板、规则、审批路径或可信 counterpart？",
                "复用前后 search/coordination/approval/QA/cycle 指标分别是多少？",
                "如果变快/变便宜，是否存在资产更简单、审批更少等替代解释？",
                "如果没有改善或仍需从零设计，按否证记录，不解释成学习曲线。",
            ],
        }.get(target)
        if questions is None:
            raise ValueError(f"unsupported structure field target: {target}")
        packets.append({
            "packet_id": f"FIELD::{task.get('task_id')}",
            "task_id": task.get("task_id"),
            "candidate_id": task.get("candidate_id"),
            "candidate_concept": task.get("candidate_concept"),
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
            "depends_on": task.get("depends_on", []),
            "state_effect": task.get("state_effect"),
        })
    return {
        "packet_kind": PACKET_KIND,
        "candidate_id": queue.get("candidate_id"),
        "packet_count": len(packets),
        "packets": packets,
        "business_promotion": "NOT_PROMOTED",
        "truth_notes": [
            "Packets are instructions for evidence collection, not evidence themselves.",
            "A completed questionnaire without source material does not satisfy any canonical gate.",
            "Observed negative results and kill conditions must be preserved rather than optimized away.",
        ],
    }
