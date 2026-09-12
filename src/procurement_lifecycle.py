"""Exact-project procurement lifecycle normalization and paid-need promotion.

This module deliberately keeps procurement lifecycle state separate from the
canonical NeedEvidence enum. Tender, award/result, contract, and settlement are
different facts:

- tender only -> observed need;
- exact-project result/award -> RESULT_FOUND, not PAID;
- exact-project signed contract -> CONTRACT_FOUND, not PAID by itself;
- exact-project first-party settlement/payment evidence with an explicit payer and
  settled amount -> SETTLEMENT_PROVEN and eligible to promote the matching
  NeedSignal to PAID.

Joining is fail-closed and exact on ``project_id`` only. Titles, capability
similarity, supplier similarity, dates, and LLM semantics are never used as
lifecycle join keys.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, replace
from typing import Any, Iterable, Mapping

from src.resource_imbalance import (
    BlockerSignal,
    NeedSignal,
    ResourceSignal,
    scan_imbalances,
    validate_need,
)

LIFECYCLE_STAGES = {
    "TENDER_ONLY",
    "RESULT_FOUND",
    "CONTRACT_FOUND",
    "SETTLEMENT_PROVEN",
}

_STATUS_ORDER = {
    "ROUTE_TESTABLE": 0,
    "PAIR_HYPOTHESIS": 1,
    "NEED_ONLY": 2,
    "RESOURCE_ONLY": 3,
}


def _text(value: object) -> str | None:
    text = str(value or "").strip()
    return text or None


def _unique(values: Iterable[object]) -> list[str]:
    result: list[str] = []
    for value in values:
        text = _text(value)
        if text and text not in result:
            result.append(text)
    return result


def _single(values: Iterable[object]) -> tuple[str | None, bool]:
    items = _unique(values)
    if len(items) == 1:
        return items[0], False
    return None, len(items) > 1


def _provenance_hash(item: Mapping[str, Any]) -> str | None:
    provenance = item.get("provenance")
    if isinstance(provenance, Mapping):
        return _text(
            provenance.get("payload_sha256")
            or provenance.get("sha256")
            or provenance.get("content_sha256")
        )
    return _text(item.get("provenance_sha256"))


def _source_url(item: Mapping[str, Any]) -> str | None:
    return _text(item.get("url") or item.get("source_url"))


def _evidence_projection(item: Mapping[str, Any], *, kind: str) -> dict[str, Any]:
    return {
        "kind": kind,
        "project_id": _text(item.get("project_id")),
        "project_name": _text(item.get("project_name") or item.get("title")),
        "url": _source_url(item),
        "publication_date": _text(item.get("publication_date")),
        "buyer_actor": _text(item.get("buyer_actor")),
        "payer_actor": _text(item.get("payer_actor")),
        "supplier_actor": _text(item.get("supplier_name") or item.get("supplier_actor")),
        "package_name": _text(item.get("package_name")),
        "tender_budget_rmb": _text(item.get("budget_rmb")),
        "award_amount_rmb": _text(item.get("award_amount_rmb")),
        "contract_amount_rmb": _text(item.get("contract_amount_rmb")),
        "settled_amount_rmb": _text(item.get("settled_amount_rmb")),
        "contract_signed": item.get("contract_signed") is True,
        "settlement_proven": item.get("settlement_proven") is True,
        "provenance_sha256": _provenance_hash(item),
    }


def _dedupe(items: Iterable[Mapping[str, Any]], *, kind: str) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for item in items:
        projected = _evidence_projection(item, kind=kind)
        identity = (
            projected["project_id"],
            projected["url"],
            projected["supplier_actor"],
            projected["package_name"],
            projected["award_amount_rmb"],
            projected["contract_amount_rmb"],
            projected["settled_amount_rmb"],
        )
        if identity in seen:
            continue
        seen.add(identity)
        result.append(projected)
    return result


def _items(payload: Mapping[str, Any], *keys: str) -> list[Mapping[str, Any]]:
    for key in keys:
        values = payload.get(key)
        if isinstance(values, list):
            return [item for item in values if isinstance(item, Mapping)]
    return []


def build_procurement_lifecycle(
    tender_payload: Mapping[str, Any] | None,
    result_payloads: Iterable[Mapping[str, Any]] = (),
    contract_payloads: Iterable[Mapping[str, Any]] = (),
    *,
    geography: str = "Xuzhou",
) -> dict[str, Any]:
    """Build exact-project lifecycle records from normalized first-party artifacts."""

    tenders = _items(tender_payload or {}, "events")
    results: list[Mapping[str, Any]] = []
    contracts: list[Mapping[str, Any]] = []
    for payload in result_payloads:
        results.extend(_items(payload, "awards", "results"))
    for payload in contract_payloads:
        contracts.extend(_items(payload, "contracts", "settlements"))

    results_by_project: dict[str, list[Mapping[str, Any]]] = {}
    contracts_by_project: dict[str, list[Mapping[str, Any]]] = {}
    unlinked: list[dict[str, Any]] = []

    for item in results:
        project_id = _text(item.get("project_id"))
        if project_id:
            results_by_project.setdefault(project_id, []).append(item)
        else:
            unlinked.append(
                {
                    "side": "RESULT",
                    "reason": "PROJECT_ID_MISSING",
                    "url": _source_url(item),
                    "title": _text(item.get("project_name") or item.get("title")),
                }
            )

    for item in contracts:
        project_id = _text(item.get("project_id"))
        if project_id:
            contracts_by_project.setdefault(project_id, []).append(item)
        else:
            unlinked.append(
                {
                    "side": "CONTRACT",
                    "reason": "PROJECT_ID_MISSING",
                    "url": _source_url(item),
                    "title": _text(item.get("project_name") or item.get("title")),
                }
            )

    tender_project_ids = {
        project_id
        for project_id in (_text(item.get("project_id")) for item in tenders)
        if project_id
    }
    for project_id, items in results_by_project.items():
        if project_id not in tender_project_ids:
            for item in items:
                unlinked.append(
                    {
                        "side": "RESULT",
                        "reason": "NO_EXACT_TENDER_PROJECT_ID_MATCH",
                        "project_id": project_id,
                        "url": _source_url(item),
                        "title": _text(item.get("project_name") or item.get("title")),
                    }
                )
    for project_id, items in contracts_by_project.items():
        if project_id not in tender_project_ids:
            for item in items:
                unlinked.append(
                    {
                        "side": "CONTRACT",
                        "reason": "NO_EXACT_TENDER_PROJECT_ID_MATCH",
                        "project_id": project_id,
                        "url": _source_url(item),
                        "title": _text(item.get("project_name") or item.get("title")),
                    }
                )

    records: list[dict[str, Any]] = []
    seen_tender_ids: set[str] = set()
    for ordinal, tender in enumerate(tenders, start=1):
        project_id = _text(tender.get("project_id"))
        if not project_id:
            unlinked.append(
                {
                    "side": "TENDER",
                    "reason": "PROJECT_ID_MISSING",
                    "url": _source_url(tender),
                    "title": _text(tender.get("project_name") or tender.get("title")),
                }
            )
            continue
        if project_id in seen_tender_ids:
            unlinked.append(
                {
                    "side": "TENDER",
                    "reason": "DUPLICATE_CURRENT_TENDER_PROJECT_ID",
                    "project_id": project_id,
                    "url": _source_url(tender),
                }
            )
            continue
        seen_tender_ids.add(project_id)

        matching_results = results_by_project.get(project_id, [])
        matching_contracts = contracts_by_project.get(project_id, [])
        tender_evidence = _dedupe([tender], kind="TENDER")
        result_evidence = _dedupe(matching_results, kind="RESULT")
        contract_evidence = _dedupe(matching_contracts, kind="CONTRACT")

        settlement_items = [
            item for item in matching_contracts if item.get("settlement_proven") is True
        ]
        if settlement_items:
            stage = "SETTLEMENT_PROVEN"
        elif matching_contracts:
            stage = "CONTRACT_FOUND"
        elif matching_results:
            stage = "RESULT_FOUND"
        else:
            stage = "TENDER_ONLY"

        project_name, project_name_conflict = _single(
            [
                tender.get("project_name"),
                *[item.get("project_name") for item in matching_results],
                *[item.get("project_name") for item in matching_contracts],
            ]
        )
        if project_name is None:
            project_name = _text(tender.get("project_name") or tender.get("title"))

        buyer_actor, buyer_conflict = _single(
            [
                *[item.get("buyer_actor") for item in matching_results],
                *[item.get("buyer_actor") for item in matching_contracts],
            ]
        )
        payer_actor, payer_conflict = _single(
            [item.get("payer_actor") for item in settlement_items]
        )
        supplier_actor, supplier_conflict = _single(
            [
                *[
                    item.get("supplier_name") or item.get("supplier_actor")
                    for item in matching_results
                ],
                *[
                    item.get("supplier_name") or item.get("supplier_actor")
                    for item in matching_contracts
                ],
            ]
        )
        tender_budget_rmb, tender_budget_conflict = _single([tender.get("budget_rmb")])
        award_amount_rmb, award_amount_conflict = _single(
            [item.get("award_amount_rmb") for item in matching_results]
        )
        contract_amount_rmb, contract_amount_conflict = _single(
            [item.get("contract_amount_rmb") for item in matching_contracts]
        )
        settled_amount_rmb, settled_amount_conflict = _single(
            [item.get("settled_amount_rmb") for item in settlement_items]
        )

        urls = _unique(
            [
                _source_url(tender),
                *[_source_url(item) for item in matching_results],
                *[_source_url(item) for item in matching_contracts],
            ]
        )
        hashes = _unique(
            [
                _provenance_hash(tender),
                *[_provenance_hash(item) for item in matching_results],
                *[_provenance_hash(item) for item in matching_contracts],
            ]
        )
        settlement_urls = _unique(_source_url(item) for item in settlement_items)
        settlement_hashes = _unique(_provenance_hash(item) for item in settlement_items)

        unresolved: list[str] = []
        conflicts = {
            "PROJECT_NAME_CONFLICT": project_name_conflict,
            "BUYER_IDENTITY_CONFLICT": buyer_conflict,
            "PAYER_IDENTITY_CONFLICT": payer_conflict,
            "SUPPLIER_IDENTITY_CONFLICT": supplier_conflict,
            "TENDER_BUDGET_CONFLICT": tender_budget_conflict,
            "AWARD_AMOUNT_CONFLICT": award_amount_conflict,
            "CONTRACT_AMOUNT_CONFLICT": contract_amount_conflict,
            "SETTLED_AMOUNT_CONFLICT": settled_amount_conflict,
        }
        unresolved.extend(name for name, active in conflicts.items() if active)
        if not buyer_actor:
            unresolved.append("BUYER_ACTOR")
        if not payer_actor:
            unresolved.append("PAYER_ACTOR")
        if stage != "SETTLEMENT_PROVEN":
            unresolved.append("SETTLEMENT_EVIDENCE")
        if stage == "SETTLEMENT_PROVEN" and not settled_amount_rmb:
            unresolved.append("SETTLED_AMOUNT")
        if stage == "SETTLEMENT_PROVEN" and (not settlement_urls or not settlement_hashes):
            unresolved.append("SETTLEMENT_SOURCE_PROVENANCE")
        if not supplier_actor and stage != "TENDER_ONLY":
            unresolved.append("SUPPLIER_ACTOR")

        promotion_allowed = (
            stage == "SETTLEMENT_PROVEN"
            and payer_actor is not None
            and settled_amount_rmb is not None
            and not any(conflicts.values())
            and bool(settlement_urls)
            and bool(settlement_hashes)
        )
        if promotion_allowed:
            promotion_reason = "EXACT_PROJECT_FIRST_PARTY_SETTLEMENT_WITH_EXPLICIT_PAYER"
        elif stage == "TENDER_ONLY":
            promotion_reason = "TENDER_ONLY_BUDGET_IS_NOT_PAYMENT"
        elif stage == "RESULT_FOUND":
            promotion_reason = "AWARD_RESULT_IS_NOT_SETTLEMENT"
        elif stage == "CONTRACT_FOUND":
            promotion_reason = "SIGNED_CONTRACT_IS_NOT_SETTLEMENT"
        elif payer_actor is None:
            promotion_reason = "SETTLEMENT_PAYER_UNRESOLVED"
        elif settled_amount_rmb is None:
            promotion_reason = "SETTLEMENT_AMOUNT_UNRESOLVED"
        elif not settlement_urls or not settlement_hashes:
            promotion_reason = "SETTLEMENT_SOURCE_PROVENANCE_UNRESOLVED"
        elif any(conflicts.values()):
            promotion_reason = "LIFECYCLE_IDENTITY_CONFLICT"
        else:
            promotion_reason = "SETTLEMENT_EVIDENCE_INSUFFICIENT"

        source_id = _text(tender.get("source_id")) or "XZ_GGZY"
        records.append(
            {
                "project_id": project_id,
                "need_signal_id": f"LIVE_NEED::{source_id}::{project_id}",
                "project_name": project_name,
                "geography": geography,
                "tender_evidence": tender_evidence,
                "result_evidence": result_evidence,
                "contract_evidence": contract_evidence,
                "buyer_actor": buyer_actor,
                "payer_actor": payer_actor,
                "supplier_actor": supplier_actor,
                "supplier_actors": _unique(
                    [
                        *[
                            item.get("supplier_name") or item.get("supplier_actor")
                            for item in matching_results
                        ],
                        *[
                            item.get("supplier_name") or item.get("supplier_actor")
                            for item in matching_contracts
                        ],
                    ]
                ),
                "tender_budget_rmb": tender_budget_rmb,
                "award_amount_rmb": award_amount_rmb,
                "award_amounts_rmb": _unique(
                    item.get("award_amount_rmb") for item in matching_results
                ),
                "contract_amount_rmb": contract_amount_rmb,
                "contract_amounts_rmb": _unique(
                    item.get("contract_amount_rmb") for item in matching_contracts
                ),
                "settled_amount_rmb": settled_amount_rmb,
                "lifecycle_stage": stage,
                "evidence_urls": urls,
                "provenance_hashes": hashes,
                "promotion_allowed": promotion_allowed,
                "promotion_reason": promotion_reason,
                "unresolved_fields": sorted(set(unresolved)),
                "exact_join_key": project_id,
                "join_policy": "EXACT_PROJECT_ID_ONLY",
                "ordinal": ordinal,
            }
        )

    stage_counts = Counter(record["lifecycle_stage"] for record in records)
    promotion_count = sum(1 for record in records if record["promotion_allowed"])
    return {
        "geography": geography,
        "join_policy": "EXACT_PROJECT_ID_ONLY",
        "source_input_counts": {
            "tenders": len(tenders),
            "results": len(results),
            "contracts": len(contracts),
        },
        "record_count": len(records),
        "stage_counts": dict(sorted(stage_counts.items())),
        "promotion_allowed_count": promotion_count,
        "records": sorted(records, key=lambda item: (item["project_id"], item["ordinal"])),
        "unlinked_evidence": unlinked,
        "truth_notes": [
            "Lifecycle joins use exact project_id only; fuzzy title, capability equality, supplier similarity, date proximity, and LLM semantics are forbidden join keys.",
            "Tender budget remains OBSERVED need evidence and never proves completed payment.",
            "Exact-project result/award creates RESULT_FOUND but does not promote canonical NeedEvidence to PAID.",
            "Exact-project signed contract creates CONTRACT_FOUND but does not prove payment by itself.",
            "PAID promotion requires exact-project first-party settlement evidence, an explicit payer, a settled amount, auditable source provenance, and no identity conflict.",
            "buyer_actor and payer_actor remain separate roles; buyer is never copied into payer automatically.",
        ],
    }


def _need_from_dict(item: Mapping[str, Any]) -> NeedSignal:
    return NeedSignal(
        signal_id=str(item["signal_id"]),
        capability_key=str(item["capability_key"]),
        geography=str(item["geography"]),
        need_actor=str(item["need_actor"]),
        payer=_text(item.get("payer")),
        evidence_state=str(item["evidence_state"]),
        paid_event_count=int(item.get("paid_event_count") or 0),
        total_observed_spend_rmb=_text(item.get("total_observed_spend_rmb")),
        observation_period=_text(item.get("observation_period")),
        source_ids=tuple(item.get("source_ids") or ()),
        notes=str(item.get("notes") or ""),
    )


def _resource_from_dict(item: Mapping[str, Any]) -> ResourceSignal:
    return ResourceSignal(
        signal_id=str(item["signal_id"]),
        capability_key=str(item["capability_key"]),
        geography=str(item["geography"]),
        provider_actor=str(item["provider_actor"]),
        resource_state=str(item["resource_state"]),
        underuse_evidence_state=str(item["underuse_evidence_state"]),
        available_units=_text(item.get("available_units")),
        observation_period=_text(item.get("observation_period")),
        source_ids=tuple(item.get("source_ids") or ()),
        notes=str(item.get("notes") or ""),
    )


def _blocker_from_dict(item: Mapping[str, Any]) -> BlockerSignal:
    return BlockerSignal(
        signal_id=str(item["signal_id"]),
        capability_key=str(item["capability_key"]),
        geography=str(item["geography"]),
        blocker_type=str(item["blocker_type"]),
        evidence_state=str(item["evidence_state"]),
        description=str(item["description"]),
        source_ids=tuple(item.get("source_ids") or ()),
    )


def integrate_procurement_lifecycle(
    ledger: Mapping[str, Any],
    lifecycle: Mapping[str, Any],
    *,
    max_pairs_per_need: int = 5,
) -> dict[str, Any]:
    """Apply only lifecycle promotions that satisfy the canonical PAID gate.

    Pair status is never mutated directly. After any allowed NeedSignal promotion,
    the canonical Resource Imbalance Engine is re-run from normalized signals.
    """

    signals = ledger.get("signals", {}) or {}
    needs = [_need_from_dict(item) for item in signals.get("needs", []) or []]
    resources = [
        _resource_from_dict(item) for item in signals.get("resources", []) or []
    ]
    blockers = [
        _blocker_from_dict(item) for item in signals.get("blockers", []) or []
    ]

    lifecycle_by_signal = {
        str(record.get("need_signal_id")): record
        for record in lifecycle.get("records", []) or []
        if record.get("need_signal_id")
    }
    promoted_needs: list[NeedSignal] = []
    decisions: list[dict[str, Any]] = []
    for need in needs:
        record = lifecycle_by_signal.get(need.signal_id)
        if not record or record.get("promotion_allowed") is not True:
            promoted_needs.append(need)
            if record:
                decisions.append(
                    {
                        "project_id": record.get("project_id"),
                        "need_signal_id": need.signal_id,
                        "applied": False,
                        "from_state": need.evidence_state,
                        "to_state": need.evidence_state,
                        "reason": record.get("promotion_reason"),
                    }
                )
            continue

        if record.get("lifecycle_stage") != "SETTLEMENT_PROVEN":
            raise ValueError("promotion_allowed lifecycle record is not SETTLEMENT_PROVEN")
        payer = _text(record.get("payer_actor"))
        settled_amount = _text(record.get("settled_amount_rmb"))
        if not payer or not settled_amount:
            raise ValueError("promotion_allowed lifecycle record lacks payer or settled amount")

        source_ids = list(need.source_ids)
        for url in record.get("evidence_urls", []) or []:
            text = _text(url)
            if text and text not in source_ids:
                source_ids.append(text)
        updated = replace(
            need,
            need_actor=_text(record.get("buyer_actor")) or need.need_actor,
            payer=payer,
            evidence_state="PAID",
            paid_event_count=max(1, need.paid_event_count),
            total_observed_spend_rmb=settled_amount,
            source_ids=tuple(source_ids),
            notes=(
                f"{need.notes}; exact_project_lifecycle=SETTLEMENT_PROVEN; "
                f"promotion_reason={record.get('promotion_reason')}"
            ).strip("; "),
        )
        validate_need(updated)
        promoted_needs.append(updated)
        decisions.append(
            {
                "project_id": record.get("project_id"),
                "need_signal_id": need.signal_id,
                "applied": True,
                "from_state": need.evidence_state,
                "to_state": "PAID",
                "reason": record.get("promotion_reason"),
            }
        )

    records = scan_imbalances(
        promoted_needs,
        resources,
        blockers,
        max_pairs_per_need=max_pairs_per_need,
    )
    records = sorted(
        records,
        key=lambda record: (
            _STATUS_ORDER.get(record.status, 99),
            record.capability_key,
            record.geography,
            record.record_id,
        ),
    )
    status_counts = Counter(record.status for record in records)
    blocking_reason_counts = Counter(
        reason
        for record in records
        if record.status != "ROUTE_TESTABLE"
        for reason in record.reasons
    )

    result = dict(ledger)
    result["signals"] = {
        "needs": [asdict(signal) for signal in promoted_needs],
        "resources": [asdict(signal) for signal in resources],
        "blockers": [asdict(signal) for signal in blockers],
    }
    result["status_counts"] = dict(sorted(status_counts.items()))
    result["blocking_reason_counts"] = dict(sorted(blocking_reason_counts.items()))
    result["route_testable_count"] = status_counts.get("ROUTE_TESTABLE", 0)
    result["records"] = [record.as_dict() for record in records]
    result["route_testable_records"] = [
        record.as_dict() for record in records if record.status == "ROUTE_TESTABLE"
    ]
    result["procurement_lifecycle"] = {
        "join_policy": lifecycle.get("join_policy"),
        "record_count": lifecycle.get("record_count", 0),
        "stage_counts": lifecycle.get("stage_counts", {}),
        "promotion_allowed_count": lifecycle.get("promotion_allowed_count", 0),
        "promotion_decisions": decisions,
        "unlinked_evidence_count": len(lifecycle.get("unlinked_evidence", []) or []),
    }
    truth_notes = list(result.get("truth_notes", []) or [])
    lifecycle_note = (
        "Procurement lifecycle can promote a live need to PAID only from exact-project "
        "SETTLEMENT_PROVEN first-party evidence with an explicit payer and settled amount."
    )
    if lifecycle_note not in truth_notes:
        truth_notes.append(lifecycle_note)
    result["truth_notes"] = truth_notes
    return result
