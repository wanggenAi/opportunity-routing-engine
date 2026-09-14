"""Evidence-distance control plane for live opportunity discovery.

This module joins canonical Resource Imbalance records with downstream validation
planning artifacts. It never promotes canonical state and never invents a
commercial score. Its ordering is strictly an evidence-distance heuristic for
choosing the next bounded validation work.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Mapping, Sequence

CANONICAL_STATUSES = (
    "NEED_ONLY",
    "RESOURCE_ONLY",
    "PAIR_HYPOTHESIS",
    "ROUTE_TESTABLE",
)


def _text(value: Any) -> str | None:
    if value is None:
        return None
    value = str(value).strip()
    return value or None


def _list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, (list, tuple)) else []


def _by_id(items: Sequence[Mapping[str, Any]], key: str) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for item in items:
        item_id = _text(item.get(key))
        if item_id:
            result[item_id] = item
    return result


def _status_lane(status: str | None) -> str:
    return {
        "ROUTE_TESTABLE": "TRANSACTION_TEST",
        "PAIR_HYPOTHESIS": "PAIR_VALIDATION",
        "NEED_ONLY": "SUPPLY_DISCOVERY",
        "RESOURCE_ONLY": "DEMAND_DISCOVERY",
    }.get(status or "", "HOLD_UNKNOWN_STATE")


def _next_action(status: str | None, tasks: Sequence[Mapping[str, Any]]) -> str:
    if status == "ROUTE_TESTABLE":
        return "RUN_BOUNDED_TRANSACTION_TEST"
    if status == "PAIR_HYPOTHESIS":
        if tasks:
            first = min(
                tasks,
                key=lambda item: (
                    int(item.get("priority") or 10_000),
                    _text(item.get("target_gate")) or "",
                    _text(item.get("task_id")) or "",
                ),
            )
            return f"VALIDATE::{_text(first.get('target_gate')) or 'UNKNOWN_GATE'}"
        return "REBUILD_VALIDATION_QUEUE_OR_REVIEW_CANONICAL_GATES"
    if status == "NEED_ONLY":
        return "DISCOVER_COMPATIBLE_RESOURCE"
    if status == "RESOURCE_ONLY":
        return "DISCOVER_PAID_NEED"
    return "REVIEW_CANONICAL_STATE"


def build_opportunity_funnel(
    ledger: Mapping[str, Any],
    validation_queue: Mapping[str, Any] | None = None,
    field_packets: Mapping[str, Any] | None = None,
    *,
    focus_limit: int = 5,
) -> dict[str, Any]:
    """Build a truth-preserving opportunity control plane.

    ``focus_limit`` only limits the pair-validation focus list. It does not
    suppress records from the funnel and does not create a commercial ranking.
    """

    if focus_limit < 0:
        raise ValueError("focus_limit must be >= 0")

    validation_queue = validation_queue or {}
    field_packets = field_packets or {}
    records = [item for item in _list(ledger.get("records")) if isinstance(item, Mapping)]
    tasks = [item for item in _list(validation_queue.get("tasks")) if isinstance(item, Mapping)]
    pairs = [item for item in _list(validation_queue.get("pairs")) if isinstance(item, Mapping)]
    packets = [item for item in _list(field_packets.get("packets")) if isinstance(item, Mapping)]

    pair_by_record = _by_id(pairs, "record_id")
    tasks_by_record: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    packets_by_record: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for task in tasks:
        record_id = _text(task.get("record_id"))
        if record_id:
            tasks_by_record[record_id].append(task)
    for packet in packets:
        record_id = _text(packet.get("record_id"))
        if record_id:
            packets_by_record[record_id].append(packet)

    funnel_records: list[dict[str, Any]] = []
    for record in records:
        record_id = _text(record.get("record_id")) or ""
        status = _text(record.get("status"))
        record_tasks = tasks_by_record.get(record_id, [])
        record_packets = packets_by_record.get(record_id, [])
        pair = pair_by_record.get(record_id)
        if status == "PAIR_HYPOTHESIS":
            if pair is not None and isinstance(pair.get("missing_gate_count"), int):
                missing_gate_count = int(pair["missing_gate_count"])
            else:
                missing_gate_count = len(record_tasks) if record_tasks else None
        elif status == "ROUTE_TESTABLE":
            missing_gate_count = 0
        else:
            missing_gate_count = None

        missing_gates = sorted(
            {
                gate
                for gate in (_text(task.get("target_gate")) for task in record_tasks)
                if gate is not None
            }
        )
        field_ready_gates = sorted(
            {
                gate
                for gate in (_text(packet.get("target_gate")) for packet in record_packets)
                if gate is not None
            }
        )

        funnel_records.append(
            {
                "record_id": record_id or None,
                "status": status,
                "lane": _status_lane(status),
                "capability_key": record.get("capability_key"),
                "geography": record.get("geography"),
                "need_signal_id": record.get("need_signal_id"),
                "resource_signal_id": record.get("resource_signal_id"),
                "payer": record.get("payer"),
                "need_evidence_state": record.get("need_evidence_state"),
                "resource_state": record.get("resource_state"),
                "underuse_evidence_state": record.get("underuse_evidence_state"),
                "blocker_evidence_state": record.get("blocker_evidence_state"),
                "blocking_reasons": _list(record.get("blocking_reasons")),
                "missing_gate_count": missing_gate_count,
                "missing_gates": missing_gates,
                "open_task_ids": sorted(
                    task_id
                    for task_id in (_text(task.get("task_id")) for task in record_tasks)
                    if task_id is not None
                ),
                "field_packet_ids": sorted(
                    packet_id
                    for packet_id in (_text(packet.get("packet_id")) for packet in record_packets)
                    if packet_id is not None
                ),
                "field_ready_gates": field_ready_gates,
                "next_action": _next_action(status, record_tasks),
            }
        )

    status_counts = Counter(item.get("status") or "UNKNOWN" for item in funnel_records)
    pair_candidates = [item for item in funnel_records if item.get("status") == "PAIR_HYPOTHESIS"]
    pair_candidates.sort(
        key=lambda item: (
            item.get("missing_gate_count") is None,
            item.get("missing_gate_count") if item.get("missing_gate_count") is not None else 10_000,
            -len(item.get("field_packet_ids") or []),
            _text(item.get("capability_key")) or "",
            _text(item.get("record_id")) or "",
        )
    )
    validation_focus = pair_candidates[:focus_limit]
    route_testable = [item for item in funnel_records if item.get("status") == "ROUTE_TESTABLE"]
    route_testable.sort(
        key=lambda item: (
            _text(item.get("capability_key")) or "",
            _text(item.get("record_id")) or "",
        )
    )

    if route_testable:
        batch_next_action = "RUN_BOUNDED_TRANSACTION_TEST"
    elif validation_focus:
        batch_next_action = "EXECUTE_PAIR_VALIDATION_FOCUS"
    elif status_counts.get("NEED_ONLY") or status_counts.get("RESOURCE_ONLY"):
        batch_next_action = "EXPAND_COMPLEMENTARY_ACTOR_SENSING"
    else:
        batch_next_action = "EXPAND_REALITY_SENSING"

    return {
        "funnel_kind": "TRUTH_PRESERVING_OPPORTUNITY_CONTROL_PLANE",
        "geography": ledger.get("geography"),
        "record_count": len(funnel_records),
        "status_counts": dict(sorted(status_counts.items())),
        "route_testable_count": len(route_testable),
        "transaction_test_ready": bool(route_testable),
        "pair_hypothesis_count": len(pair_candidates),
        "validation_focus_count": len(validation_focus),
        "validation_focus_limit": focus_limit,
        "batch_next_action": batch_next_action,
        "ordering_basis": "EVIDENCE_DISTANCE_ONLY_NOT_COMMERCIAL_RANKING",
        "records": funnel_records,
        "route_testable_records": route_testable,
        "validation_focus": validation_focus,
        "truth_notes": [
            "This artifact is a control plane over canonical truth; it does not promote or mutate Resource Imbalance state.",
            "Validation focus ordering is evidence-distance only and is not a probability, value, or commercial-success ranking.",
            "ROUTE_TESTABLE means eligible for a bounded transaction test, not proven profitable and not canonical #1.",
            "PAIR_HYPOTHESIS missing gates come only from the canonical validation queue; absent queue coverage is surfaced, not guessed.",
            "Only real settlement/payment evidence may satisfy PAID need; capability evidence never implies current underuse.",
        ],
    }
