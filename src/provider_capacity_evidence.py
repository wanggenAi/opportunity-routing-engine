"""Apply auditable provider-capacity evidence to canonical ResourceSignals.

This module closes the evidence-acquisition loop for RESOURCE_UNDERUSE without
weakening truth gates. Historical awards prove capability only. Provider statements
remain CLAIMED. OBSERVED/MEASURED underuse requires an auditable capacity artifact
such as an authorized schedule, unused-capacity record, or measured utilization
record bound to one exact canonical ResourceSignal.
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
    validate_resource,
)

_ALLOWED_BASIS_STATE = {
    "PROVIDER_STATED_SPARE_CAPACITY": "CLAIMED",
    "AUTHORIZED_CAPACITY_SCHEDULE": "OBSERVED",
    "VERIFIED_UNUSED_CAPACITY_RECORD": "OBSERVED",
    "MEASURED_UTILIZATION_RECORD": "MEASURED",
}
_UNDERUSE_RANK = {"UNKNOWN": 0, "CLAIMED": 1, "OBSERVED": 2, "MEASURED": 3}
_STATUS_ORDER = {
    "ROUTE_TESTABLE": 0,
    "PAIR_HYPOTHESIS": 1,
    "NEED_ONLY": 2,
    "RESOURCE_ONLY": 3,
}


def _text(value: object) -> str | None:
    text = str(value or "").strip()
    return text or None


def _tuple_text(values: object) -> tuple[str, ...]:
    if isinstance(values, str):
        values = [values]
    if not isinstance(values, (list, tuple)):
        return ()
    result: list[str] = []
    for value in values:
        text = _text(value)
        if text and text not in result:
            result.append(text)
    return tuple(result)


def _need(item: Mapping[str, Any]) -> NeedSignal:
    signal = NeedSignal(
        signal_id=str(item["signal_id"]),
        capability_key=str(item["capability_key"]),
        geography=str(item["geography"]),
        need_actor=str(item["need_actor"]),
        payer=_text(item.get("payer")),
        evidence_state=str(item["evidence_state"]),
        paid_event_count=int(item.get("paid_event_count") or 0),
        total_observed_spend_rmb=_text(item.get("total_observed_spend_rmb")),
        observation_period=_text(item.get("observation_period")),
        source_ids=_tuple_text(item.get("source_ids")),
        notes=str(item.get("notes") or ""),
    )
    validate_need(signal)
    return signal


def _resource(item: Mapping[str, Any]) -> ResourceSignal:
    signal = ResourceSignal(
        signal_id=str(item["signal_id"]),
        capability_key=str(item["capability_key"]),
        geography=str(item["geography"]),
        provider_actor=str(item["provider_actor"]),
        resource_state=str(item["resource_state"]),
        underuse_evidence_state=str(item["underuse_evidence_state"]),
        available_units=_text(item.get("available_units")),
        observation_period=_text(item.get("observation_period")),
        source_ids=_tuple_text(item.get("source_ids")),
        notes=str(item.get("notes") or ""),
    )
    validate_resource(signal)
    return signal


def _blocker(item: Mapping[str, Any]) -> BlockerSignal:
    return BlockerSignal(
        signal_id=str(item["signal_id"]),
        capability_key=str(item["capability_key"]),
        geography=str(item["geography"]),
        blocker_type=str(item["blocker_type"]),
        evidence_state=str(item["evidence_state"]),
        description=str(item["description"]),
        source_ids=_tuple_text(item.get("source_ids")),
        need_signal_id=_text(item.get("need_signal_id")),
    )


def _validate_evidence(item: Mapping[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    required = (
        "evidence_id",
        "resource_signal_id",
        "provider_actor",
        "capability_key",
        "geography",
        "underuse_evidence_state",
        "evidence_basis",
        "observation_period",
    )
    normalized = {key: _text(item.get(key)) for key in required}
    missing = [key for key, value in normalized.items() if not value]
    if missing:
        return None, f"MISSING_REQUIRED_FIELDS:{','.join(missing)}"

    state = normalized["underuse_evidence_state"]
    basis = normalized["evidence_basis"]
    expected_state = _ALLOWED_BASIS_STATE.get(str(basis))
    if expected_state is None:
        return None, "UNAPPROVED_EVIDENCE_BASIS"
    if state != expected_state:
        return None, "EVIDENCE_BASIS_STATE_MISMATCH"

    source_refs = _tuple_text(item.get("source_refs"))
    if not source_refs:
        return None, "SOURCE_REFS_REQUIRED"

    available_units = _text(item.get("available_units"))
    if state in {"OBSERVED", "MEASURED"} and not available_units:
        return None, "OBSERVED_UNDERUSE_REQUIRES_AVAILABLE_UNITS"

    return {
        **normalized,
        "available_units": available_units,
        "source_refs": source_refs,
        "notes": _text(item.get("notes")),
    }, None


def apply_provider_capacity_evidence_to_ledger(
    ledger: Mapping[str, Any],
    evidence_payloads: Iterable[Mapping[str, Any]],
    *,
    max_pairs_per_need: int = 5,
) -> dict[str, Any]:
    """Apply exact ResourceSignal-scoped underuse evidence and re-run canonical gates.

    Evidence never creates a provider/resource from scratch and never changes
    resource_state. It may only strengthen the underuse axis of an already canonical
    ResourceSignal when resource identity, provider, capability, and geography all
    match exactly.
    """

    signals = ledger.get("signals", {}) or {}
    needs = [_need(item) for item in signals.get("needs", []) or []]
    resources = [_resource(item) for item in signals.get("resources", []) or []]
    blockers = [_blocker(item) for item in signals.get("blockers", []) or []]

    resource_index = {resource.signal_id: index for index, resource in enumerate(resources)}
    applied: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    seen_evidence_ids: set[str] = set()

    for payload in evidence_payloads:
        for raw in payload.get("evidence", []) or []:
            if not isinstance(raw, Mapping):
                rejected.append({"reason": "EVIDENCE_RECORD_NOT_OBJECT"})
                continue
            evidence, error = _validate_evidence(raw)
            evidence_id = _text(raw.get("evidence_id"))
            if error:
                rejected.append({"evidence_id": evidence_id, "reason": error})
                continue
            assert evidence is not None
            evidence_id = str(evidence["evidence_id"])
            if evidence_id in seen_evidence_ids:
                rejected.append({"evidence_id": evidence_id, "reason": "DUPLICATE_EVIDENCE_ID"})
                continue
            seen_evidence_ids.add(evidence_id)

            resource_signal_id = str(evidence["resource_signal_id"])
            index = resource_index.get(resource_signal_id)
            if index is None:
                rejected.append({"evidence_id": evidence_id, "reason": "RESOURCE_SIGNAL_NOT_FOUND"})
                continue
            resource = resources[index]
            exact_identity = (
                str(evidence["provider_actor"]) == resource.provider_actor
                and str(evidence["capability_key"]) == resource.capability_key
                and str(evidence["geography"]) == resource.geography
            )
            if not exact_identity:
                rejected.append({"evidence_id": evidence_id, "reason": "RESOURCE_IDENTITY_MISMATCH"})
                continue

            incoming_state = str(evidence["underuse_evidence_state"])
            if _UNDERUSE_RANK[incoming_state] < _UNDERUSE_RANK[resource.underuse_evidence_state]:
                rejected.append({"evidence_id": evidence_id, "reason": "EVIDENCE_WEAKER_THAN_CURRENT_STATE"})
                continue

            source_ids = list(resource.source_ids)
            for source_ref in evidence["source_refs"]:
                if source_ref not in source_ids:
                    source_ids.append(source_ref)
            notes = [resource.notes] if resource.notes else []
            notes.append(
                "provider_capacity_evidence="
                f"{evidence_id}; basis={evidence['evidence_basis']}; "
                f"state={incoming_state}; period={evidence['observation_period']}"
            )
            if evidence.get("notes"):
                notes.append(str(evidence["notes"]))

            updated = replace(
                resource,
                underuse_evidence_state=incoming_state,
                available_units=evidence.get("available_units") or resource.available_units,
                observation_period=str(evidence["observation_period"]),
                source_ids=tuple(source_ids),
                notes="; ".join(notes),
            )
            validate_resource(updated)
            resources[index] = updated
            applied.append(
                {
                    "evidence_id": evidence_id,
                    "resource_signal_id": updated.signal_id,
                    "provider_actor": updated.provider_actor,
                    "capability_key": updated.capability_key,
                    "underuse_evidence_state": updated.underuse_evidence_state,
                    "available_units": updated.available_units,
                }
            )

    records = scan_imbalances(
        needs,
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
    result["signals"] = dict(signals)
    result["signals"]["resources"] = [asdict(resource) for resource in resources]
    result["status_counts"] = dict(sorted(status_counts.items()))
    result["blocking_reason_counts"] = dict(sorted(blocking_reason_counts.items()))
    result["route_testable_count"] = status_counts.get("ROUTE_TESTABLE", 0)
    result["records"] = [record.as_dict() for record in records]
    result["route_testable_records"] = [
        record.as_dict() for record in records if record.status == "ROUTE_TESTABLE"
    ]
    result["provider_capacity_evidence"] = {
        "policy": "EXACT_RESOURCE_SIGNAL_AND_IDENTITY_ONLY",
        "applied_count": len(applied),
        "rejected_count": len(rejected),
        "applied": applied,
        "rejected": rejected,
        "truth_note": (
            "Provider capability claims do not prove underuse. CLAIMED stays below the route gate; "
            "OBSERVED/MEASURED requires an auditable capacity artifact bound to the exact canonical resource."
        ),
    }
    return result
