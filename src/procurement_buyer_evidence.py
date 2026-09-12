"""Exact first-party procurement buyer evidence for current pair hypotheses.

Buyer identity is an Actor fact, not payment truth. This module only accepts a buyer
explicitly named inside the official procurement notice's buyer-information section.
It never infers buyer from the title and never copies buyer into payer.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, replace
import re
from typing import Any, Iterable, Mapping

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace
from src.resource_imbalance import BlockerSignal, NeedSignal, ResourceSignal, scan_imbalances, validate_need

XZ_GGZY_HOST = "ggzy.zwb.xz.gov.cn"
BUYER_ROLE_BASIS = "EXPLICIT_PROCUREMENT_BUYER_SECTION"
QUERY_STRATEGY = "EXACT_PAIR_NEED_EVENT_URL_PLUS_EXPLICIT_BUYER_SECTION"
_UNRESOLVED_BUYER = "UNRESOLVED_PUBLIC_PROCUREMENT_BUYER"
_STATUS_ORDER = {"ROUTE_TESTABLE": 0, "PAIR_HYPOTHESIS": 1, "NEED_ONLY": 2, "RESOURCE_ONLY": 3}


def _text(value: object) -> str | None:
    text = str(value or "").strip()
    return text or None


def _plain_html(html: str) -> str:
    text = re.sub(r"<br\s*/?>", " ", html, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    from html import unescape
    return normalize_whitespace(unescape(text))


def _section(text: str, start_marker: str, end_markers: tuple[str, ...]) -> str | None:
    start = text.find(start_marker)
    if start < 0:
        return None
    tail = text[start + len(start_marker):]
    ends = [tail.find(marker) for marker in end_markers if tail.find(marker) >= 0]
    if ends:
        tail = tail[: min(ends)]
    return normalize_whitespace(tail)


def _field(section: str | None, label: str, next_labels: tuple[str, ...]) -> str | None:
    if not section:
        return None
    pattern = rf"{re.escape(label)}\s*[：:]?\s*(.+?)"
    stops = "|".join(rf"\s+{re.escape(item)}\s*[：:]?" for item in next_labels)
    if stops:
        pattern += rf"(?={stops}|$)"
    else:
        pattern += "$"
    match = re.search(pattern, section)
    if not match:
        return None
    return normalize_whitespace(match.group(1))


def extract_explicit_buyer(html: str, visible_text: str = "") -> dict[str, str | None] | None:
    """Extract only the explicit `采购人信息` section; never use title inference."""

    candidates = [normalize_whitespace(visible_text), _plain_html(html)]
    for text in candidates:
        section = _section(text, "采购人信息", ("采购代理机构信息", "项目联系方式"))
        if not section:
            continue
        buyer = _field(section, "单位名称", ("单位地址", "联系人", "联系电话"))
        if not buyer or len(buyer) > 160:
            continue
        if any(marker in buyer for marker in ("采购代理机构", "项目联系人", "联系电话")):
            continue
        return {
            "buyer_actor": buyer,
            "buyer_address": _field(section, "单位地址", ("联系人", "联系电话")),
            "buyer_contact_name": _field(section, "联系人", ("联系电话",)),
            "buyer_phone": _field(section, "联系电话", ()),
        }
    return None


def collect_pair_buyer_evidence(
    ledger: Mapping[str, Any],
    procurement_payload: Mapping[str, Any],
    *,
    client: PublicHtmlClient | None = None,
) -> dict[str, Any]:
    """Fetch buyer evidence only for current pair-hypothesis Needs."""

    client = client or PublicHtmlClient(
        source_id="XZ_GGZY_BUYER",
        allowed_hosts={XZ_GGZY_HOST},
        timeout_seconds=30,
        retries=2,
    )
    pair_need_ids = {
        _text(record.get("need_signal_id"))
        for record in ledger.get("records", []) or []
        if record.get("status") == "PAIR_HYPOTHESIS" and _text(record.get("need_signal_id"))
    }
    event_by_need: dict[str, Mapping[str, Any]] = {}
    for event in procurement_payload.get("events", []) or []:
        if not isinstance(event, Mapping):
            continue
        source_id = _text(event.get("source_id")) or "XZ_GGZY"
        project_id = _text(event.get("project_id"))
        if project_id:
            event_by_need[f"LIVE_NEED::{source_id}::{project_id}"] = event

    evidence: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for need_signal_id in sorted(pair_need_ids):
        event = event_by_need.get(need_signal_id)
        if event is None:
            errors.append({"need_signal_id": need_signal_id, "reason": "EXACT_PROCUREMENT_EVENT_MISSING"})
            continue
        project_id = _text(event.get("project_id"))
        url = _text(event.get("url"))
        if not project_id or not url:
            errors.append({"need_signal_id": need_signal_id, "reason": "PROJECT_ID_OR_URL_MISSING"})
            continue
        try:
            envelope = client.fetch(url, request_name="xz_ggzy.procurement_buyer.detail")
            doc = html_to_document(envelope.html, base_url=url)
            plain = _plain_html(envelope.html)
            if project_id not in doc.get("text", "") and project_id not in plain:
                errors.append({"need_signal_id": need_signal_id, "reason": "EXACT_PROJECT_ID_REVALIDATION_FAILED", "url": url})
                continue
            buyer = extract_explicit_buyer(envelope.html, doc.get("text", ""))
            if buyer is None:
                errors.append({"need_signal_id": need_signal_id, "reason": "EXPLICIT_BUYER_SECTION_UNRESOLVED", "url": url})
                continue
            evidence.append({
                "evidence_id": f"BUYER::{need_signal_id}",
                "need_signal_id": need_signal_id,
                "project_id": project_id,
                "source_id": _text(event.get("source_id")) or "XZ_GGZY",
                "source_url": url,
                "role_basis": BUYER_ROLE_BASIS,
                **buyer,
                "provenance": envelope.metadata(),
            })
        except Exception as exc:
            errors.append({"need_signal_id": need_signal_id, "reason": "BUYER_EVIDENCE_FETCH_FAILED", "url": url, "error": str(exc)})

    return {
        "source_id": "XZ_GGZY_BUYER",
        "query_strategy": QUERY_STRATEGY,
        "requested_need_count": len(pair_need_ids),
        "evidence_count": len(evidence),
        "error_count": len(errors),
        "buyer_evidence": evidence,
        "errors": errors,
        "truth_note": "Explicit procurement buyer is Actor evidence only; buyer is never promoted to payer without separate payment-role evidence.",
    }


def _need(item: Mapping[str, Any]) -> NeedSignal:
    return NeedSignal(
        signal_id=str(item["signal_id"]), capability_key=str(item["capability_key"]),
        geography=str(item["geography"]), need_actor=str(item["need_actor"]), payer=_text(item.get("payer")),
        evidence_state=str(item["evidence_state"]), paid_event_count=int(item.get("paid_event_count") or 0),
        total_observed_spend_rmb=_text(item.get("total_observed_spend_rmb")),
        observation_period=_text(item.get("observation_period")), source_ids=tuple(item.get("source_ids") or ()),
        notes=str(item.get("notes") or ""),
    )


def _resource(item: Mapping[str, Any]) -> ResourceSignal:
    return ResourceSignal(
        signal_id=str(item["signal_id"]), capability_key=str(item["capability_key"]), geography=str(item["geography"]),
        provider_actor=str(item["provider_actor"]), resource_state=str(item["resource_state"]),
        underuse_evidence_state=str(item["underuse_evidence_state"]), available_units=_text(item.get("available_units")),
        observation_period=_text(item.get("observation_period")), source_ids=tuple(item.get("source_ids") or ()),
        notes=str(item.get("notes") or ""),
    )


def _blocker(item: Mapping[str, Any]) -> BlockerSignal:
    return BlockerSignal(
        signal_id=str(item["signal_id"]), capability_key=str(item["capability_key"]), geography=str(item["geography"]),
        blocker_type=str(item["blocker_type"]), evidence_state=str(item["evidence_state"]),
        description=str(item["description"]), source_ids=tuple(item.get("source_ids") or ()),
        need_signal_id=_text(item.get("need_signal_id")),
    )


def apply_buyer_evidence(
    ledger: Mapping[str, Any], buyer_payload: Mapping[str, Any], *, max_pairs_per_need: int = 5
) -> dict[str, Any]:
    """Apply exact buyer Actor evidence without changing payer or Need evidence state."""

    signals = ledger.get("signals", {}) or {}
    needs = [_need(item) for item in signals.get("needs", []) or []]
    resources = [_resource(item) for item in signals.get("resources", []) or []]
    blockers = [_blocker(item) for item in signals.get("blockers", []) or []]
    evidence_by_need = {
        str(item.get("need_signal_id")): item
        for item in buyer_payload.get("buyer_evidence", []) or []
        if item.get("need_signal_id")
    }

    updated_needs: list[NeedSignal] = []
    decisions: list[dict[str, Any]] = []
    for need in needs:
        item = evidence_by_need.get(need.signal_id)
        if item is None:
            updated_needs.append(need)
            continue
        buyer = _text(item.get("buyer_actor"))
        source_url = _text(item.get("source_url"))
        provenance = item.get("provenance") or {}
        valid = (
            buyer is not None
            and item.get("role_basis") == BUYER_ROLE_BASIS
            and source_url in set(need.source_ids)
            and provenance.get("http_status") == 200
            and bool(provenance.get("payload_sha256"))
        )
        if not valid:
            updated_needs.append(need)
            decisions.append({"need_signal_id": need.signal_id, "applied": False, "reason": "BUYER_EVIDENCE_INVALID_OR_IDENTITY_MISMATCH"})
            continue
        if need.need_actor not in {_UNRESOLVED_BUYER, buyer}:
            updated_needs.append(need)
            decisions.append({"need_signal_id": need.signal_id, "applied": False, "reason": "EXISTING_NEED_ACTOR_CONFLICT"})
            continue
        source_ids = list(need.source_ids)
        if source_url not in source_ids:
            source_ids.append(source_url)
        updated = replace(
            need,
            need_actor=buyer,
            source_ids=tuple(source_ids),
            notes=f"{need.notes}; buyer_actor_basis={BUYER_ROLE_BASIS}; payer_remains_independent".strip("; "),
        )
        if updated.payer != need.payer or updated.evidence_state != need.evidence_state:
            raise ValueError("buyer evidence attempted to mutate payer or Need evidence state")
        validate_need(updated)
        updated_needs.append(updated)
        decisions.append({"need_signal_id": need.signal_id, "applied": True, "buyer_actor": buyer, "reason": BUYER_ROLE_BASIS})

    records = scan_imbalances(updated_needs, resources, blockers, max_pairs_per_need=max_pairs_per_need)
    records = sorted(records, key=lambda r: (_STATUS_ORDER.get(r.status, 99), r.capability_key, r.geography, r.record_id))
    status_counts = Counter(r.status for r in records)
    blocking_reason_counts = Counter(reason for r in records if r.status != "ROUTE_TESTABLE" for reason in r.reasons)

    result = dict(ledger)
    result["signals"] = {
        "needs": [asdict(item) for item in updated_needs],
        "resources": [asdict(item) for item in resources],
        "blockers": [asdict(item) for item in blockers],
    }
    result["status_counts"] = dict(sorted(status_counts.items()))
    result["blocking_reason_counts"] = dict(sorted(blocking_reason_counts.items()))
    result["route_testable_count"] = status_counts.get("ROUTE_TESTABLE", 0)
    result["records"] = [r.as_dict() for r in records]
    result["route_testable_records"] = [r.as_dict() for r in records if r.status == "ROUTE_TESTABLE"]
    result["procurement_buyer_evidence"] = {
        "query_strategy": buyer_payload.get("query_strategy"),
        "evidence_count": buyer_payload.get("evidence_count", 0),
        "applied_count": sum(1 for item in decisions if item.get("applied")),
        "decisions": decisions,
    }
    truth_notes = list(result.get("truth_notes", []) or [])
    note = "Explicit procurement buyer may resolve Need Actor identity, but buyer remains separate from payer and cannot upgrade PAID truth."
    if note not in truth_notes:
        truth_notes.append(note)
    result["truth_notes"] = truth_notes
    return result
