"""Turn clean PAIR_HYPOTHESIS records into explicit evidence-acquisition work.

The queue is a planning artifact, not evidence. It never changes a Resource
Imbalance state and never upgrades UNKNOWN/CLAIMED facts to PASS. Each task names
one missing canonical gate and the minimum evidence that would be required before a
future ledger build could reconsider the pair.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Mapping


_CANONICAL_TARGETS = (
    "PAYER_IDENTITY",
    "PAID_NEED",
    "RESOURCE_UNDERUSE",
    "TRANSACTION_BLOCKER",
)


def _index_signals(ledger: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    signals = ledger.get("signals", {}) or {}
    needs = {
        str(item.get("signal_id")): item
        for item in signals.get("needs", []) or []
        if item.get("signal_id")
    }
    resources = {
        str(item.get("signal_id")): item
        for item in signals.get("resources", []) or []
        if item.get("signal_id")
    }
    return needs, resources


def _task(
    *,
    record: Mapping[str, Any],
    target: str,
    priority: int,
    channel: str,
    instruction: str,
    pass_condition: str,
    fail_condition: str,
    forbidden_inference: str,
) -> dict[str, Any]:
    if target not in _CANONICAL_TARGETS:
        raise ValueError(f"unsupported validation target: {target}")
    record_id = str(record.get("record_id") or "").strip()
    if not record_id:
        raise ValueError("PAIR_HYPOTHESIS record_id is required")
    return {
        "task_id": f"VALIDATE::{record_id}::{target}",
        "record_id": record_id,
        "capability_key": record.get("capability_key"),
        "geography": record.get("geography"),
        "target_gate": target,
        "priority": priority,
        "channel": channel,
        "instruction": instruction,
        "pass_condition": pass_condition,
        "fail_condition": fail_condition,
        "forbidden_inference": forbidden_inference,
        "state_effect": "NONE_UNTIL_NEW_EVIDENCE_IS_INGESTED",
    }


def build_pair_validation_queue(ledger: Mapping[str, Any]) -> dict[str, Any]:
    """Build a deterministic validation queue from PAIR_HYPOTHESIS records only."""

    needs, resources = _index_signals(ledger)
    pair_records = [
        record
        for record in ledger.get("records", []) or []
        if record.get("status") == "PAIR_HYPOTHESIS"
    ]
    tasks: list[dict[str, Any]] = []
    pairs: list[dict[str, Any]] = []

    for record in pair_records:
        need = needs.get(str(record.get("need_signal_id") or ""), {})
        resource = resources.get(str(record.get("resource_signal_id") or ""), {})
        record_tasks: list[dict[str, Any]] = []

        if not record.get("payer"):
            record_tasks.append(
                _task(
                    record=record,
                    target="PAYER_IDENTITY",
                    priority=10,
                    channel="FIRST_PARTY_PUBLIC_RECORD",
                    instruction=(
                        "Resolve the exact buyer/payer identity from the same-project official "
                        "procurement notice, result, contract, or payment record. Preserve buyer, "
                        "budget source, and actual payer as separate fields when they differ."
                    ),
                    pass_condition=(
                        "A first-party record explicitly identifies the actor responsible for the "
                        "transaction payment or an exact legally accountable procuring payer."
                    ),
                    fail_condition=(
                        "Only an agency, platform, budget source, or inferred government entity is "
                        "available without an explicit payer relationship."
                    ),
                    forbidden_inference="procurement buyer name or fiscal budget != proven payer unless the source explicitly binds the role",
                )
            )

        if record.get("need_evidence_state") not in {"PAID", "REPEATED_PAID"}:
            record_tasks.append(
                _task(
                    record=record,
                    target="PAID_NEED",
                    priority=20,
                    channel="FIRST_PARTY_RESULT_CONTRACT_PAYMENT",
                    instruction=(
                        "Find an exact-project award/result, signed contract, accepted invoice, or "
                        "payment record that proves money actually committed or paid for this "
                        "capability; preserve project/package identity."
                    ),
                    pass_condition=(
                        "At least one exact-identity paid/awarded transaction is evidenced with a "
                        "named counterparty and amount; repeated paid status requires two or more "
                        "distinct paid events."
                    ),
                    fail_condition=(
                        "Only a budget, tender notice, intention, estimate, or market inquiry exists."
                    ),
                    forbidden_inference="published budget or tender amount != PAID need",
                )
            )

        if record.get("underuse_evidence_state") not in {"OBSERVED", "MEASURED"}:
            record_tasks.append(
                _task(
                    record=record,
                    target="RESOURCE_UNDERUSE",
                    priority=30,
                    channel="PROVIDER_OR_AUTHORIZED_CAPACITY_PROBE",
                    instruction=(
                        "Verify current spare capacity for the named provider/capability using "
                        "observable capacity evidence: unused service slots, idle crew/equipment "
                        "hours, unfilled capacity, or another auditable utilization measure."
                    ),
                    pass_condition=(
                        "Current underuse is OBSERVED or MEASURED for the exact provider capability, "
                        "with date/scope and source retained."
                    ),
                    fail_condition=(
                        "Provider merely says it can do the work, has historical qualifications, or "
                        "appears in an award directory without observable spare capacity."
                    ),
                    forbidden_inference="historical capability or willingness claim != observed underuse",
                )
            )

        if record.get("blocker_evidence_state") not in {"OBSERVED", "MEASURED"}:
            record_tasks.append(
                _task(
                    record=record,
                    target="TRANSACTION_BLOCKER",
                    priority=40,
                    channel="COUNTERPARTY_OR_ROUTE_PROBE",
                    instruction=(
                        "Observe why a verified need and verified provider capability are not already "
                        "transacting: price, trust, information, geography, time, coordination, payer "
                        "shift, or another canonical blocker. Record the concrete failed/manual step."
                    ),
                    pass_condition=(
                        "A specific canonical blocker is OBSERVED or MEASURED from a real buyer, "
                        "provider, transaction attempt, or first-party process record."
                    ),
                    fail_condition=(
                        "The blocker is only hypothesized from narrative similarity or generic market friction."
                    ),
                    forbidden_inference="pair existence or relisting != observed transaction blocker",
                )
            )

        tasks.extend(record_tasks)
        pairs.append(
            {
                "record_id": record.get("record_id"),
                "capability_key": record.get("capability_key"),
                "geography": record.get("geography"),
                "need_signal_id": record.get("need_signal_id"),
                "resource_signal_id": record.get("resource_signal_id"),
                "need_actor": need.get("need_actor"),
                "provider_actor": resource.get("provider_actor"),
                "current_need_evidence_state": record.get("need_evidence_state"),
                "current_resource_state": record.get("resource_state"),
                "current_underuse_evidence_state": record.get("underuse_evidence_state"),
                "current_blocker_evidence_state": record.get("blocker_evidence_state"),
                "current_payer": record.get("payer"),
                "missing_gate_count": len(record_tasks),
                "task_ids": [item["task_id"] for item in record_tasks],
            }
        )

    tasks.sort(key=lambda item: (item["priority"], item["capability_key"] or "", item["task_id"]))
    pairs.sort(key=lambda item: (item["capability_key"] or "", item["record_id"] or ""))
    target_counts = Counter(task["target_gate"] for task in tasks)

    return {
        "queue_kind": "PAIR_HYPOTHESIS_EVIDENCE_ACQUISITION",
        "geography": ledger.get("geography"),
        "pair_hypothesis_count": len(pair_records),
        "queued_pair_count": len(pairs),
        "task_count": len(tasks),
        "target_counts": dict(sorted(target_counts.items())),
        "pairs": pairs,
        "tasks": tasks,
        "truth_notes": [
            "This queue is a planning artifact and does not modify Resource Imbalance truth states.",
            "Task priority is an evidence-cost heuristic, not probability of commercial success.",
            "UNKNOWN and CLAIMED remain below OBSERVED; DISCOVERED remains below OPTIONED.",
            "A task disappears only after a future evidence ingestion changes the canonical ledger state.",
        ],
    }
