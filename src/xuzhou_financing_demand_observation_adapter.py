"""Fail-closed Observation Fabric adapter for scoped Xuzhou financing demand.

This adapter consumes the official Jiangsu Government evidence artifact produced by
`xuzhou-enterprise-funding-demand-live`. It records only what the source explicitly
supports for a named program/batch. A reported financing-demand amount is a scoped
STATE, not realized money flow, payment, payer confirmation, or opportunity truth.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from datetime import date
from typing import Any
from urllib.parse import urlparse

from src.observation_fabric import EvidenceRef, ObservationEnvelope, SemanticClaim


PARSER_VERSION = "xuzhou-financing-demand-observation-adapter.v1"
REQUIRED_TRUTH_BOUNDARIES = frozenset({
    "DIRECT_DEMAND_EVIDENCE_IS_NEED_ONLY",
    "SCOPED_PROGRAM_IS_NOT_CITYWIDE_TOTAL",
    "SME_IS_NOT_PRIVATE_ENTERPRISE",
    "MISSING_DEMAND_IS_NOT_ZERO",
    "NO_CROSS_PROGRAM_SUM",
    "NO_CROSS_PERIOD_SUM",
    "NO_SURPLUS_RESOURCE_INFERENCE",
    "NO_OPPORTUNITY_INFERENCE",
})


def _mapping(value: object, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return value


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} is required")
    return value.strip()


def _sha256(value: object, field: str) -> str:
    digest = _text(value, field).lower()
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise ValueError(f"{field} must be a SHA-256 hex digest")
    return digest


def _official_detail_url(value: object, field: str) -> str:
    url = _text(value, field)
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "www.jiangsu.gov.cn" or "/art_" not in parsed.path:
        raise ValueError(f"{field} must be an official Jiangsu Government detail URL")
    return url


def _positive_decimal_text(value: object, field: str) -> str:
    raw = _text(value, field)
    try:
        numeric = float(raw)
    except ValueError as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if numeric <= 0:
        raise ValueError(f"{field} must be positive")
    return raw


def _stable_id(prefix: str, *parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return f"{prefix}:{hashlib.sha256(payload).hexdigest()[:24]}"


def _published_at(publication_date: str) -> str:
    try:
        date.fromisoformat(publication_date)
    except ValueError as exc:
        raise ValueError("publication_date must be ISO date") from exc
    return f"{publication_date}T00:00:00+08:00"


def xuzhou_financing_demand_observations(
    payload: Mapping[str, Any],
) -> tuple[ObservationEnvelope, ...]:
    """Normalize explicit scoped financing-demand events without commercial promotion."""

    if payload.get("source_id") != "XZ_GOV_FINANCE_DEMAND":
        raise ValueError("unexpected Xuzhou financing-demand source_id")
    if payload.get("evidence_kind") != "SCOPED_DIRECT_ENTERPRISE_FINANCING_DEMAND":
        raise ValueError("unexpected Xuzhou financing-demand evidence_kind")
    if payload.get("data_available") is not True:
        raise ValueError("Xuzhou financing-demand artifact has no available data")
    if payload.get("geography") != "Xuzhou":
        raise ValueError("unexpected Xuzhou financing-demand geography")

    truth_boundaries = set(payload.get("truth_boundaries") or ())
    missing_boundaries = REQUIRED_TRUTH_BOUNDARIES - truth_boundaries
    if missing_boundaries:
        raise ValueError(f"financing-demand truth boundaries missing: {sorted(missing_boundaries)}")

    events = payload.get("events")
    if not isinstance(events, list) or not events:
        raise ValueError("Xuzhou financing-demand events are required")
    event_count = payload.get("event_count")
    if isinstance(event_count, bool) or not isinstance(event_count, int) or event_count != len(events):
        raise ValueError("event_count diverges from financing-demand events")

    provenance = _mapping(payload.get("provenance"), "provenance")
    detail_pages = provenance.get("detail_pages")
    if not isinstance(detail_pages, list) or not detail_pages:
        raise ValueError("detail-page provenance is required")

    detail_by_url: dict[str, Mapping[str, Any]] = {}
    for index, item in enumerate(detail_pages):
        meta = _mapping(item, f"provenance.detail_pages[{index}]")
        url = _official_detail_url(meta.get("url"), f"provenance.detail_pages[{index}].url")
        if meta.get("source_id") != "XZ_GOV_FINANCE_DEMAND":
            raise ValueError("detail-page provenance has unexpected source_id")
        if url in detail_by_url:
            raise ValueError(f"duplicate detail-page provenance URL: {url}")
        _sha256(meta.get("payload_sha256"), f"provenance.detail_pages[{index}].payload_sha256")
        _text(meta.get("fetched_at_utc"), f"provenance.detail_pages[{index}].fetched_at_utc")
        detail_by_url[url] = meta

    envelopes: list[ObservationEnvelope] = []
    for index, raw_event in enumerate(events):
        event = _mapping(raw_event, f"events[{index}]")
        if event.get("source_id") != "XZ_GOV_FINANCE_DEMAND":
            raise ValueError("event has unexpected source_id")
        if event.get("evidence_role") != "DIRECT_SCOPED_ENTERPRISE_FINANCING_DEMAND":
            raise ValueError("event has unexpected evidence_role")
        if event.get("geography") != "Xuzhou":
            raise ValueError("event has unexpected geography")
        if event.get("coverage_scope") != "SCOPED_PROGRAM_OR_REPORTED_BATCH":
            raise ValueError("event must remain scoped to its reported program/batch")
        if event.get("aggregation_allowed") is not False:
            raise ValueError("financing-demand events must prohibit aggregation")
        if event.get("source_authority") != "徐州市政府办公室":
            raise ValueError("event source authority drifted")

        source_url = _official_detail_url(event.get("source_url"), f"events[{index}].source_url")
        detail = detail_by_url.get(source_url)
        if detail is None:
            raise ValueError("event lacks matching detail-page provenance")
        raw_hash = _sha256(event.get("provenance_sha256"), f"events[{index}].provenance_sha256")
        if raw_hash != _sha256(detail.get("payload_sha256"), "detail payload_sha256"):
            raise ValueError("event provenance hash diverges from detail-page provenance")
        fetched_at = _text(detail.get("fetched_at_utc"), "detail fetched_at_utc")

        matched_text = _text(event.get("matched_text"), f"events[{index}].matched_text")
        title = _text(event.get("title"), f"events[{index}].title")
        program_name = _text(event.get("program_name"), f"events[{index}].program_name")
        publication_date = _text(event.get("publication_date"), f"events[{index}].publication_date")
        demand_amount = _positive_decimal_text(
            event.get("demand_amount_cny_100m"),
            f"events[{index}].demand_amount_cny_100m",
        )
        actor_scope = _text(event.get("actor_scope"), f"events[{index}].actor_scope")
        private_explicit = event.get("private_enterprise_scope_explicit")
        if not isinstance(private_explicit, bool):
            raise ValueError("private_enterprise_scope_explicit must be boolean")
        if actor_scope != "PRIVATE_ENTERPRISE" and private_explicit:
            raise ValueError("non-private actor scope cannot be relabeled private enterprise")

        evidence_ref = f"event-text:{index}"
        evidence = (
            EvidenceRef(
                ref_id=evidence_ref,
                locator=source_url,
                excerpt=matched_text,
                content_hash=raw_hash,
            ),
        )
        common = {
            "program_name": program_name,
            "actor_scope": actor_scope,
            "private_enterprise_scope_explicit": private_explicit,
            "coverage_scope": "SCOPED_PROGRAM_OR_REPORTED_BATCH",
            "publication_date": publication_date,
            "source_title": title,
            "aggregation_allowed": False,
        }
        claims: list[SemanticClaim] = [
            SemanticClaim(
                claim_id="scoped_financing_demand",
                primitive="STATE",
                concept="XZ_SCOPED_DIRECT_ENTERPRISE_FINANCING_DEMAND",
                epistemic_status="OBSERVED",
                evidence_refs=(evidence_ref,),
                value={**common, "demand_amount_cny_100m": demand_amount},
                geography="CN-JS-XZ",
            )
        ]

        granted_credit = event.get("granted_credit_amount_cny_100m")
        if granted_credit is not None:
            claims.append(
                SemanticClaim(
                    claim_id="scoped_granted_credit",
                    primitive="STATE",
                    concept="XZ_SCOPED_GRANTED_CREDIT_AMOUNT",
                    epistemic_status="OBSERVED",
                    evidence_refs=(evidence_ref,),
                    value={
                        **common,
                        "granted_credit_amount_cny_100m": _positive_decimal_text(
                            granted_credit,
                            f"events[{index}].granted_credit_amount_cny_100m",
                        ),
                        "settlement_status": "NOT_ESTABLISHED",
                    },
                    geography="CN-JS-XZ",
                )
            )

        beneficiaries = event.get("beneficiary_enterprises")
        if beneficiaries is not None:
            if isinstance(beneficiaries, bool) or not isinstance(beneficiaries, int) or beneficiaries <= 0:
                raise ValueError("beneficiary_enterprises must be a positive integer")
            claims.append(
                SemanticClaim(
                    claim_id="beneficiary_enterprises",
                    primitive="STATE",
                    concept="XZ_SCOPED_BENEFICIARY_ENTERPRISE_COUNT",
                    epistemic_status="OBSERVED",
                    evidence_refs=(evidence_ref,),
                    value={**common, "beneficiary_enterprises": beneficiaries},
                    geography="CN-JS-XZ",
                )
            )

        envelopes.append(
            ObservationEnvelope(
                observation_id=_stable_id(
                    "obs:XZ_GOV_FINANCE_DEMAND",
                    source_url,
                    publication_date,
                    program_name,
                ),
                source_id="XZ_GOV_FINANCE_DEMAND",
                source_record_id=_stable_id("record:XZ_GOV_FINANCE_DEMAND", source_url),
                source_locator=source_url,
                source_origin_geography="CN-JS",
                relevance_geographies=("CN-JS-XZ",),
                source_tier="OFFICIAL_PROVINCIAL_GOVERNMENT_PRIMARY",
                observed_at=fetched_at,
                retrieved_at=fetched_at,
                published_at=_published_at(publication_date),
                parser_version=PARSER_VERSION,
                raw_payload_hash=raw_hash,
                sampling_boundary=(
                    "SCOPED_PROGRAM_OR_REPORTED_BATCH_ONLY; NO_CROSS_PROGRAM_OR_PERIOD_AGGREGATION"
                ),
                evidence=evidence,
                claims=tuple(claims),
                actor_ids=(),
                unknown_fields=(
                    "exact_publication_time",
                    "payment_status",
                    "payer_identity",
                    "current_unmet_remainder",
                ),
            )
        )

    return tuple(envelopes)


GOVERNING_INVARIANTS = (
    "DIRECT_FINANCING_DEMAND_IS_SCOPED_STATE_NOT_REALIZED_FLOW",
    "GRANTED_CREDIT_NE_PAYMENT",
    "SME_SCOPE_NE_PRIVATE_ENTERPRISE",
    "SCOPED_PROGRAM_NE_CITYWIDE_TOTAL",
    "NO_CROSS_PROGRAM_OR_PERIOD_AGGREGATION",
    "FINANCING_DEMAND_NE_PAYER_OR_PAID_NEED",
    "FINANCING_DEMAND_NE_OPPORTUNITY",
    "UNKNOWN_NE_PASS",
)
