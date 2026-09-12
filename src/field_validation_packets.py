"""Build delegatable real-world validation packets from canonical evidence gaps.

The packet layer is execution planning only. It never upgrades canonical truth states.
It converts selected validation-queue tasks into bounded, auditable work that a field
agent or authorized remote researcher can execute without reinterpreting the model.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping

_FIELD_TARGETS = {"RESOURCE_UNDERUSE", "TRANSACTION_BLOCKER"}


def _text(value: object) -> str | None:
    text = str(value or "").strip()
    return text or None


def _index_by_id(items: Iterable[Mapping[str, Any]], key: str) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for item in items:
        identity = _text(item.get(key))
        if identity:
            result[identity] = item
    return result


def _provider_awards(payloads: Iterable[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    result: list[Mapping[str, Any]] = []
    for payload in payloads:
        for item in payload.get("awards", []) or []:
            if isinstance(item, Mapping):
                result.append(item)
    return result


def _resolve_provider_evidence(
    resource: Mapping[str, Any],
    awards: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    provider = _text(resource.get("provider_actor"))
    source_ids = {str(value).strip() for value in resource.get("source_ids", []) or [] if str(value).strip()}
    exact = [
        award
        for award in awards
        if _text(award.get("supplier_name")) == provider
        and _text(award.get("url")) in source_ids
    ]
    if len(exact) != 1:
        return {
            "resolution_state": "UNRESOLVED" if not exact else "AMBIGUOUS",
            "provider_actor": provider,
            "source_refs": sorted(source_ids),
            "truth_note": "No unique source-backed provider award metadata was resolved; do not guess contact details.",
        }

    award = exact[0]
    return {
        "resolution_state": "RESOLVED",
        "provider_actor": provider,
        "supplier_address": _text(award.get("supplier_address")),
        "supplier_credit_code": _text(award.get("supplier_credit_code")),
        "historical_project_id": _text(award.get("project_id")),
        "historical_package_name": _text(award.get("package_name")),
        "historical_award_url": _text(award.get("url")),
        "historical_award_amount_rmb": _text(award.get("award_amount_rmb")),
        "truth_note": "Historical award metadata proves provider identity/capability only; it does not prove current spare capacity.",
    }


def _underuse_questions(capability_key: str | None) -> list[str]:
    capability = capability_key or "该能力"
    return [
        f"请确认当前针对 {capability} 是否存在可接受新增任务的具体空余能力；不要只回答‘能做’或‘有资质’。",
        "如果有，请记录可用数量/班组/设备/时段、可用起止日期，以及证据来自排班、设备台账、空余工位或其他可核验记录。",
        "如果只有口头表示‘有空’，按 CLAIMED 记录；只有授权排班、可核验空余记录或实测利用率才能进入 OBSERVED/MEASURED。",
        "记录证据来源、日期、联系人角色和原始材料位置；不要替对方推断利用率。",
    ]


def _blocker_questions() -> list[str]:
    return [
        "围绕这一个具体需求与这一个具体 provider，确认为什么当前不能直接形成交易，而不是讨论泛泛行业问题。",
        "记录真实卡点属于价格、信任、信息、地域、时间、协调、付款主体变化或其他明确阻塞中的哪一种。",
        "必须保留一个具体失败步骤、拒绝条件、人工绕行步骤或第一方流程证据；推测和市场常识不算 OBSERVED。",
        "如果无法观察到具体阻塞，结果必须保持 UNKNOWN。",
    ]


def build_field_validation_packets(
    ledger: Mapping[str, Any],
    validation_queue: Mapping[str, Any],
    *,
    provider_payloads: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Build bounded field/remote execution packets for real-world evidence gaps."""

    records = _index_by_id(ledger.get("records", []) or [], "record_id")
    signals = ledger.get("signals", {}) or {}
    resources = _index_by_id(signals.get("resources", []) or [], "signal_id")
    needs = _index_by_id(signals.get("needs", []) or [], "signal_id")
    awards = _provider_awards(provider_payloads)

    packets: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    for task in validation_queue.get("tasks", []) or []:
        target = _text(task.get("target_gate"))
        if target not in _FIELD_TARGETS:
            continue
        record_id = _text(task.get("record_id"))
        record = records.get(record_id or "")
        if record is None:
            skipped.append({"task_id": task.get("task_id"), "reason": "PAIR_RECORD_MISSING"})
            continue
        resource_id = _text(record.get("resource_signal_id"))
        need_id = _text(record.get("need_signal_id"))
        resource = resources.get(resource_id or "")
        need = needs.get(need_id or "")
        if resource is None or need is None:
            skipped.append({"task_id": task.get("task_id"), "reason": "CANONICAL_SIGNAL_MISSING"})
            continue

        provider_evidence = _resolve_provider_evidence(resource, awards)
        if target == "RESOURCE_UNDERUSE":
            execution_mode = "PROVIDER_CAPACITY_PROBE"
            questions = _underuse_questions(_text(record.get("capability_key")))
            capture_contract = task.get("evidence_capture") or {}
        else:
            execution_mode = "COUNTERPARTY_ROUTE_BLOCKER_PROBE"
            questions = _blocker_questions()
            capture_contract = {
                "required_identity": {
                    "need_signal_id": need_id,
                    "resource_signal_id": resource_id,
                    "provider_actor": resource.get("provider_actor"),
                    "capability_key": record.get("capability_key"),
                    "geography": record.get("geography"),
                },
                "required_fields": [
                    "evidence_id",
                    "blocker_type",
                    "evidence_state",
                    "description",
                    "observation_period",
                    "source_refs",
                ],
                "minimum_state_for_gate": "OBSERVED",
                "promotion_policy": "EXACT_PAIR_OR_EXACT_NEED_ONLY",
            }

        packets.append(
            {
                "packet_id": f"FIELD::{task.get('task_id')}",
                "task_id": task.get("task_id"),
                "record_id": record_id,
                "target_gate": target,
                "execution_mode": execution_mode,
                "execution_owner": "DELEGATABLE_FIELD_AGENT_OR_AUTHORIZED_REMOTE_RESEARCHER",
                "capability_key": record.get("capability_key"),
                "geography": record.get("geography"),
                "need_signal_id": need_id,
                "resource_signal_id": resource_id,
                "need_actor": need.get("need_actor"),
                "provider_actor": resource.get("provider_actor"),
                "provider_evidence": provider_evidence,
                "objective": task.get("instruction"),
                "questions": questions,
                "pass_condition": task.get("pass_condition"),
                "fail_condition": task.get("fail_condition"),
                "forbidden_inference": task.get("forbidden_inference"),
                "capture_contract": capture_contract,
                "state_effect": "NONE_UNTIL_CAPTURED_EVIDENCE_IS_INGESTED_AND_CANONICAL_ENGINE_REBUILDS",
            }
        )

    packets.sort(key=lambda item: (item["target_gate"], item["capability_key"] or "", item["packet_id"]))
    return {
        "packet_kind": "DELEGATABLE_REAL_WORLD_VALIDATION",
        "geography": ledger.get("geography"),
        "packet_count": len(packets),
        "skipped_count": len(skipped),
        "packets": packets,
        "skipped": skipped,
        "truth_notes": [
            "Field packets are execution plans, not evidence and not opportunities.",
            "Historical provider awards may supply identity/address context but never prove current underuse.",
            "A packet cannot change canonical state; captured evidence must be ingested and the canonical engine rebuilt.",
            "Generic capability claims, guessed contacts, and inferred spare capacity remain forbidden.",
        ],
    }
