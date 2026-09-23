"""Machine-enforced strategic anti-drift guard for attraction scans.

This module prevents a fresh scan from satisfying local transaction/economic gates
while silently abandoning the repository's regenerative latent-value formation
objective. It is intentionally narrow: it does not score commercial quality and it
does not promote anything. It only rejects scans that claim strategic attraction
without evidence that a regenerative field exists independently of one transaction.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence


ENFORCEMENT_START_SCAN = 142

REGENERATIVE_FIELD_DIMENSIONS = (
    "actor_a_replenishment",
    "actor_b_replenishment",
    "recurring_connection_pressure",
    "recurring_missing_edge",
    "recurring_event_source",
)

REQUIRED_DRIFT_AUDIT_FLAGS = (
    "regenerative_field_revalidated",
    "explicit_transaction_seed_not_ontology",
    "next_search_boundary_rederived_from_broad_reality",
)

EXPLICIT_TRANSACTION_SEED_KINDS = frozenset(
    {
        "EXPLICIT_TASK",
        "GIG",
        "RFQ",
        "PROCUREMENT_NOTICE",
        "BUYER_BRIEF",
        "ASSET_LISTING",
        "SINGLE_TRANSACTION",
        "PRICE_SPREAD",
    }
)


def _scan_number(scan_id: Any) -> int | None:
    text = str(scan_id or "").strip()
    prefix = "ATTRACTION_SCAN_"
    if not text.startswith(prefix):
        return None
    suffix = text[len(prefix) :]
    return int(suffix) if suffix.isdigit() else None


def _refs(value: Any) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return ()
    return tuple(str(item).strip() for item in value if str(item).strip())


def validate_regenerative_field_gate(
    gate: Mapping[str, Any] | None,
    *,
    formation_id: str,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(gate, Mapping):
        return [f"{formation_id}:missing_regenerative_field_gate"]

    for dimension in REGENERATIVE_FIELD_DIMENSIONS:
        raw = gate.get(dimension)
        if not isinstance(raw, Mapping):
            errors.append(f"{formation_id}:missing_dimension:{dimension}")
            continue
        if str(raw.get("state") or "") != "EVIDENCED":
            errors.append(f"{formation_id}:dimension_not_evidenced:{dimension}")
        if not _refs(raw.get("evidence_refs")):
            errors.append(f"{formation_id}:missing_evidence_refs:{dimension}")

    seed_kind = str(gate.get("seed_kind") or "").strip().upper()
    if seed_kind in EXPLICIT_TRANSACTION_SEED_KINDS and not _refs(
        gate.get("independent_field_evidence_refs")
    ):
        errors.append(
            f"{formation_id}:explicit_transaction_seed_without_independent_field_evidence"
        )

    return errors


def strategic_drift_errors(scan: Mapping[str, Any]) -> list[str]:
    """Return fail-closed strategic drift errors for current/future scans.

    Historical scans before the enforcement boundary remain audit history. Starting
    with Scan 142, every scan must prove the anti-drift audit itself, and every
    claimed high-attraction beacon must include an evidence-bound regenerative-field
    gate.
    """

    scan_number = _scan_number(scan.get("scan_id"))
    if scan_number is None:
        return ["invalid_scan_id"]
    if scan_number < ENFORCEMENT_START_SCAN:
        return []

    errors: list[str] = []
    drift_audit = scan.get("drift_audit")
    if not isinstance(drift_audit, Mapping):
        errors.append("missing_drift_audit")
    else:
        for flag in REQUIRED_DRIFT_AUDIT_FLAGS:
            if drift_audit.get(flag) is not True:
                errors.append(f"drift_audit_not_true:{flag}")

    high = scan.get("high_attraction_beacons")
    high_rows = high if isinstance(high, list) else []
    for index, raw in enumerate(high_rows):
        if not isinstance(raw, Mapping):
            errors.append(f"high_attraction_beacon_{index}:invalid_record")
            continue
        formation_id = str(raw.get("formation_id") or f"high_attraction_beacon_{index}")
        errors.extend(
            validate_regenerative_field_gate(
                raw.get("regenerative_field_gate"),
                formation_id=formation_id,
            )
        )

    return errors


def strategic_drift_guard_passes(scan: Mapping[str, Any]) -> bool:
    return not strategic_drift_errors(scan)
