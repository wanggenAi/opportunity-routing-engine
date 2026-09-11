"""Compile live discovery artifacts into a truth-preserving imbalance ledger.

This module is deliberately conservative. Live source payloads are not allowed to
become opportunities merely because text looks semantically related. Only narrow,
auditable classification rules may bind source evidence to a canonical
``capability_key``. Unclassified or ambiguous evidence is retained as unbound
evidence instead of being guessed into a pair.

Important boundaries:
- a procurement notice with a published budget is OBSERVED need evidence here;
  it is not treated as completed payment and the payer remains unresolved unless a
  source-specific adapter proves the payer separately;
- a public asset listing is DISCOVERED resource evidence; explicit idle/vacant
  language may raise underuse to OBSERVED through the existing source adapter;
- repeated listing is allocation friction, not automatically a canonical blocker;
- no BlockerSignal is manufactured from generic relisting or narrative similarity;
- ROUTE_TESTABLE can only be emitted by the canonical Resource Imbalance Engine.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, replace
from typing import Any, Iterable, Mapping, Sequence

from src.resource_imbalance import (
    BlockerSignal,
    NeedSignal,
    ResourceSignal,
    scan_imbalances,
    validate_need,
    validate_resource,
)
from src.resource_signal_adapters import public_asset_listing_to_resource


@dataclass(frozen=True)
class CapabilityClassification:
    capability_key: str | None
    matched_rule: str | None
    reason: str


# Rules intentionally use explicit phrases rather than embeddings, fuzzy matching or
# LLM inference. A source item matching more than one capability is left unbound.
_PROCUREMENT_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("INDUSTRIAL_SPACE_LEASE", ("厂房租赁", "厂房租用", "生产用房租赁")),
    ("OFFICE_SPACE_LEASE", ("办公用房租赁", "办公场所租赁", "办公房屋租赁")),
    ("FACILITY_CLEANING_SERVICE", ("保洁服务", "清洁服务")),
    ("PROPERTY_MANAGEMENT_SERVICE", ("物业管理服务",)),
    (
        "EQUIPMENT_MAINTENANCE_SERVICE",
        ("设备维保服务", "设备维护服务", "设备维修保养服务"),
    ),
)

_RESOURCE_RULES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("INDUSTRIAL_SPACE_LEASE", "LEASE", ("厂房", "生产用房")),
    ("OFFICE_SPACE_LEASE", "LEASE", ("办公用房", "办公场所", "写字楼")),
    (
        "INDUSTRIAL_EQUIPMENT_TRANSFER",
        "TRANSFER",
        ("机械设备", "机器设备", "生产设备"),
    ),
)

_STATUS_ORDER = {
    "ROUTE_TESTABLE": 0,
    "PAIR_HYPOTHESIS": 1,
    "NEED_ONLY": 2,
    "RESOURCE_ONLY": 3,
}


def _clean_text(*values: object) -> str:
    return " ".join(str(value).strip() for value in values if str(value or "").strip())


def _classify_unique(
    text: str,
    candidates: Sequence[tuple[str, str]],
) -> CapabilityClassification:
    matches: list[tuple[str, str]] = []
    for capability_key, rule in candidates:
        if rule in text:
            matches.append((capability_key, rule))

    keys = sorted({capability_key for capability_key, _ in matches})
    if not keys:
        return CapabilityClassification(None, None, "NO_EXACT_CAPABILITY_RULE")
    if len(keys) > 1:
        return CapabilityClassification(None, None, "AMBIGUOUS_EXACT_CAPABILITY_RULE")

    capability_key = keys[0]
    matched_rule = next(rule for key, rule in matches if key == capability_key)
    return CapabilityClassification(capability_key, matched_rule, "EXACT_RULE_MATCH")


def classify_procurement_event(event: Mapping[str, Any]) -> CapabilityClassification:
    """Classify only narrow, explicit procurement phrases into capability keys."""

    text = _clean_text(event.get("project_name"), event.get("title"))
    candidates = [
        (capability_key, phrase)
        for capability_key, phrases in _PROCUREMENT_RULES
        for phrase in phrases
    ]
    return _classify_unique(text, candidates)


def classify_resource_listing(listing: Mapping[str, Any]) -> CapabilityClassification:
    """Classify a listing only when asset wording and transaction mode agree."""

    mode = str(listing.get("listing_mode") or "UNKNOWN").strip().upper()
    text = _clean_text(listing.get("title"), listing.get("location"))
    candidates = [
        (capability_key, phrase)
        for capability_key, required_mode, phrases in _RESOURCE_RULES
        if mode == required_mode
        for phrase in phrases
    ]
    return _classify_unique(text, candidates)


def _source_refs(item: Mapping[str, Any]) -> tuple[str, ...]:
    refs: list[str] = []
    for key in ("source_id", "discovery_source_id", "url", "discovery_url"):
        value = str(item.get(key) or "").strip()
        if value and value not in refs:
            refs.append(value)
    return tuple(refs)


def _unbound(
    *,
    side: str,
    item: Mapping[str, Any],
    reason: str,
    matched_rule: str | None = None,
) -> dict[str, Any]:
    return {
        "side": side,
        "source_id": str(item.get("source_id") or "").strip() or None,
        "title": str(item.get("title") or item.get("project_name") or "").strip()
        or None,
        "url": str(item.get("url") or "").strip() or None,
        "reason": reason,
        "matched_rule": matched_rule,
    }


def procurement_event_to_live_need(
    event: Mapping[str, Any],
    *,
    ordinal: int,
    geography: str = "Xuzhou",
) -> tuple[NeedSignal | None, dict[str, Any] | None]:
    """Normalize one procurement event without upgrading budget into payment proof."""

    classification = classify_procurement_event(event)
    if classification.capability_key is None:
        return None, _unbound(
            side="NEED",
            item=event,
            reason=classification.reason,
            matched_rule=classification.matched_rule,
        )

    source_id = str(event.get("source_id") or "XZ_GGZY").strip()
    identity = str(event.get("project_id") or event.get("url") or ordinal).strip()
    budget = event.get("budget_rmb")
    notes = [
        f"classification_rule={classification.matched_rule}",
        "normalized from live public procurement evidence",
        "published procurement budget is not completed payment evidence",
        "payer actor remains unresolved in the current source schema",
    ]
    if budget not in (None, ""):
        notes.append(f"published_budget_rmb={budget}")

    signal = NeedSignal(
        signal_id=f"LIVE_NEED::{source_id}::{identity}",
        capability_key=classification.capability_key,
        geography=geography,
        need_actor="UNRESOLVED_PUBLIC_PROCUREMENT_BUYER",
        payer=None,
        evidence_state="OBSERVED",
        paid_event_count=0,
        total_observed_spend_rmb=None,
        observation_period=str(event.get("publication_date") or "").strip() or None,
        source_ids=_source_refs(event),
        notes="; ".join(notes),
    )
    validate_need(signal)
    return signal, None


def public_listing_to_live_resource(
    listing: Mapping[str, Any],
    *,
    ordinal: int,
    geography: str = "Xuzhou",
) -> tuple[ResourceSignal | None, dict[str, Any] | None]:
    """Normalize one classified listing while preserving resource truth boundaries."""

    classification = classify_resource_listing(listing)
    if classification.capability_key is None:
        return None, _unbound(
            side="RESOURCE",
            item=listing,
            reason=classification.reason,
            matched_rule=classification.matched_rule,
        )

    owner = str(listing.get("owner_actor") or "").strip()
    if not owner:
        return None, _unbound(
            side="RESOURCE",
            item=listing,
            reason="RESOURCE_OWNER_UNRESOLVED",
            matched_rule=classification.matched_rule,
        )

    source_id = str(listing.get("source_id") or "XZ_GGZY").strip()
    identity = str(
        listing.get("project_id")
        or listing.get("monitoring_code")
        or listing.get("url")
        or ordinal
    ).strip()
    signal = public_asset_listing_to_resource(
        listing,
        signal_id=f"LIVE_RESOURCE::{source_id}::{identity}",
        capability_key=classification.capability_key,
        provider_actor=owner,
        geography=geography,
    )
    signal = replace(
        signal,
        notes=(
            f"{signal.notes}; classification_rule={classification.matched_rule}; "
            "classification_policy=EXACT_ALLOWLIST"
        ),
    )
    validate_resource(signal)
    return signal, None


def _sorted_records(records: Iterable[Any]) -> list[Any]:
    return sorted(
        records,
        key=lambda record: (
            _STATUS_ORDER.get(record.status, 99),
            record.capability_key,
            record.geography,
            record.record_id,
        ),
    )


def build_live_imbalance_ledger(
    procurement_payload: Mapping[str, Any] | None,
    resource_payloads: Iterable[Mapping[str, Any]] = (),
    blockers: Iterable[BlockerSignal] = (),
    *,
    geography: str = "Xuzhou",
    max_pairs_per_need: int = 5,
) -> dict[str, Any]:
    """Build an auditable live ledger from source artifacts.

    The output keeps normalized signals, unbound evidence and promotion reasons so
    later automation can explain both what was promoted and what was deliberately
    withheld.
    """

    needs: list[NeedSignal] = []
    resources: list[ResourceSignal] = []
    unbound: list[dict[str, Any]] = []

    events = list((procurement_payload or {}).get("events", []) or [])
    for ordinal, event in enumerate(events, start=1):
        signal, rejected = procurement_event_to_live_need(
            event,
            ordinal=ordinal,
            geography=geography,
        )
        if signal is not None:
            needs.append(signal)
        if rejected is not None:
            unbound.append(rejected)

    listing_count = 0
    for payload in resource_payloads:
        listings = list(payload.get("listings", []) or [])
        for listing in listings:
            listing_count += 1
            signal, rejected = public_listing_to_live_resource(
                listing,
                ordinal=listing_count,
                geography=geography,
            )
            if signal is not None:
                resources.append(signal)
            if rejected is not None:
                unbound.append(rejected)

    blocker_list = list(blockers)
    records = _sorted_records(
        scan_imbalances(
            needs,
            resources,
            blocker_list,
            max_pairs_per_need=max_pairs_per_need,
        )
    )
    status_counts = Counter(record.status for record in records)
    blocking_reason_counts = Counter(
        reason
        for record in records
        if record.status != "ROUTE_TESTABLE"
        for reason in record.reasons
    )

    return {
        "geography": geography,
        "source_input_counts": {
            "procurement_events": len(events),
            "resource_listings": listing_count,
            "blockers": len(blocker_list),
        },
        "signal_counts": {
            "needs": len(needs),
            "resources": len(resources),
            "blockers": len(blocker_list),
            "unbound_evidence": len(unbound),
        },
        "status_counts": dict(sorted(status_counts.items())),
        "blocking_reason_counts": dict(sorted(blocking_reason_counts.items())),
        "route_testable_count": status_counts.get("ROUTE_TESTABLE", 0),
        "signals": {
            "needs": [asdict(signal) for signal in needs],
            "resources": [asdict(signal) for signal in resources],
            "blockers": [asdict(signal) for signal in blocker_list],
        },
        "records": [record.as_dict() for record in records],
        "route_testable_records": [
            record.as_dict() for record in records if record.status == "ROUTE_TESTABLE"
        ],
        "unbound_evidence": unbound,
        "truth_notes": [
            "Capability classification is a deterministic exact allowlist; ambiguous/unclassified evidence remains unbound.",
            "Published procurement budget is not completed payment; current procurement normalization remains OBSERVED with payer unresolved.",
            "Public listing proves DISCOVERED resource only; explicit idle/vacant source text is required for OBSERVED underuse.",
            "Relisting is allocation friction only and does not manufacture a BlockerSignal.",
            "ROUTE_TESTABLE is emitted only by the canonical Resource Imbalance Engine gates.",
        ],
    }
