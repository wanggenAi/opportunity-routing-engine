"""Observation Fabric adapter for public QuestMobile research findings.

The adapter preserves source-native public research excerpts as EVIDENCE claims. It
intentionally does not parse report prose into hard demand, payment, payer, local
Xuzhou state, market size or opportunity truth.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from datetime import date
from typing import Any
from urllib.parse import urlparse

from src.observation_fabric import EvidenceRef, ObservationEnvelope, SemanticClaim


SOURCE_ID = "QM"
PARSER_VERSION = "questmobile-research-observation-adapter.v1"
HOST = "www.questmobile.com.cn"
REQUIRED_TRUTH_BOUNDARIES = frozenset({
    "PUBLIC_REPORT_PAGE_ONLY",
    "NO_LOGIN_OR_PAID_DATABASE",
    "NO_OCR_OR_IMAGE_METRIC_EXTRACTION",
    "NO_TEXT_FINDING_NE_ZERO",
    "RESEARCH_REPORT_NE_CURRENT_LOCAL_REALITY",
    "REPORTED_SAMPLE_OR_PANEL_NE_CENSUS",
    "RESEARCH_FINDING_NE_PAID_DEMAND",
    "RESEARCH_FINDING_NE_PAYER",
    "RESEARCH_FINDING_NE_PAYMENT",
    "RESEARCH_FINDING_NE_OPPORTUNITY",
    "EXACT_EXCERPT_REQUIRED",
    "UNKNOWN_NE_PASS",
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


def _official_report_url(value: object, field: str, report_id: str) -> str:
    url = _text(value, field)
    parsed = urlparse(url)
    if (
        parsed.scheme != "https"
        or parsed.hostname != HOST
        or parsed.path != f"/research/report/{report_id}/"
    ):
        raise ValueError(f"{field} must be the canonical QuestMobile report URL")
    return url


def _published_at(value: object) -> tuple[str, str]:
    publication_date = _text(value, "publication_date")
    try:
        date.fromisoformat(publication_date)
    except ValueError as exc:
        raise ValueError("publication_date must be an ISO date") from exc
    return publication_date, f"{publication_date}T00:00:00+08:00"


def _stable_id(prefix: str, *parts: str) -> str:
    raw = "\x1f".join(parts).encode("utf-8")
    return f"{prefix}:{hashlib.sha256(raw).hexdigest()[:24]}"


def questmobile_public_research_observations(
    payload: Mapping[str, Any],
) -> tuple[ObservationEnvelope, ...]:
    """Normalize public research excerpts without manufacturing market truth."""

    if payload.get("schema_version") != "questmobile-public-research.v1":
        raise ValueError("unsupported QuestMobile producer schema")
    if payload.get("source_id") != SOURCE_ID:
        raise ValueError("unexpected QuestMobile source_id")
    if payload.get("data_available") is not True:
        raise ValueError("QuestMobile producer artifact has no available data")
    if payload.get("collection_scope") != "LATEST_PUBLIC_RESEARCH_REPORTS_ONLY":
        raise ValueError("QuestMobile collection scope drifted")

    truth_boundaries = set(payload.get("truth_boundaries") or ())
    missing = REQUIRED_TRUTH_BOUNDARIES - truth_boundaries
    if missing:
        raise ValueError(f"QuestMobile truth boundaries missing: {sorted(missing)}")

    reports = payload.get("reports")
    if not isinstance(reports, list) or not reports:
        raise ValueError("QuestMobile reports are required")
    report_count = payload.get("report_count")
    if isinstance(report_count, bool) or not isinstance(report_count, int) or report_count != len(reports):
        raise ValueError("QuestMobile report_count diverges from reports")

    declared_total = payload.get("text_finding_count")
    if isinstance(declared_total, bool) or not isinstance(declared_total, int) or declared_total <= 0:
        raise ValueError("QuestMobile text_finding_count must be positive")

    envelopes: list[ObservationEnvelope] = []
    observed_finding_count = 0
    seen_report_ids: set[str] = set()
    for report_index, raw_report in enumerate(reports):
        report = _mapping(raw_report, f"reports[{report_index}]")
        if report.get("source_id") != SOURCE_ID:
            raise ValueError("QuestMobile report source_id drifted")
        report_id = _text(report.get("report_id"), f"reports[{report_index}].report_id")
        if not report_id.isdigit():
            raise ValueError("QuestMobile report_id must be numeric")
        if report_id in seen_report_ids:
            raise ValueError(f"duplicate QuestMobile report_id: {report_id}")
        seen_report_ids.add(report_id)

        title = _text(report.get("title"), f"reports[{report_index}].title")
        publication_date, published_at = _published_at(report.get("publication_date"))
        if report.get("source_authority") != "QuestMobile研究院":
            raise ValueError("QuestMobile report source authority drifted")
        source_url = _official_report_url(
            report.get("source_url"), f"reports[{report_index}].source_url", report_id
        )
        raw_hash = _sha256(
            report.get("provenance_sha256"), f"reports[{report_index}].provenance_sha256"
        )
        provenance = _mapping(report.get("provenance"), f"reports[{report_index}].provenance")
        if provenance.get("source_id") != SOURCE_ID:
            raise ValueError("QuestMobile detail provenance source_id drifted")
        if _official_report_url(
            provenance.get("url"), f"reports[{report_index}].provenance.url", report_id
        ) != source_url:
            raise ValueError("QuestMobile detail provenance URL diverges from report URL")
        if _sha256(
            provenance.get("payload_sha256"),
            f"reports[{report_index}].provenance.payload_sha256",
        ) != raw_hash:
            raise ValueError("QuestMobile detail provenance hash diverges from report hash")
        fetched_at = _text(
            provenance.get("fetched_at_utc"),
            f"reports[{report_index}].provenance.fetched_at_utc",
        )

        findings = report.get("findings")
        if not isinstance(findings, list):
            raise ValueError("QuestMobile findings must be an array")
        finding_count = report.get("finding_count")
        if isinstance(finding_count, bool) or not isinstance(finding_count, int) or finding_count != len(findings):
            raise ValueError("QuestMobile finding_count diverges from findings")
        finding_state = report.get("finding_evidence_state")
        if not findings:
            if finding_state != "NO_TEXT_FINDING":
                raise ValueError("empty QuestMobile findings require NO_TEXT_FINDING state")
            continue
        if finding_state != "TEXT_FINDINGS_OBSERVED":
            raise ValueError("QuestMobile textual findings require observed evidence state")

        category_text = report.get("category_text")
        if category_text is not None and not isinstance(category_text, str):
            raise ValueError("QuestMobile category_text must be string or null")

        evidence: list[EvidenceRef] = []
        claims: list[SemanticClaim] = []
        seen_finding_ids: set[str] = set()
        for finding_index, raw_finding in enumerate(findings):
            finding = _mapping(
                raw_finding,
                f"reports[{report_index}].findings[{finding_index}]",
            )
            finding_id = _text(
                finding.get("finding_id"),
                f"reports[{report_index}].findings[{finding_index}].finding_id",
            )
            if finding_id in seen_finding_ids:
                raise ValueError("duplicate QuestMobile finding_id within report")
            seen_finding_ids.add(finding_id)
            attribution = _text(
                finding.get("attribution"),
                f"reports[{report_index}].findings[{finding_index}].attribution",
            )
            if attribution not in {"QuestMobile", "QuestAuto"}:
                raise ValueError("unsupported QuestMobile finding attribution")
            excerpt = _text(
                finding.get("excerpt"),
                f"reports[{report_index}].findings[{finding_index}].excerpt",
            )
            if f"{attribution}数据显示" not in excerpt:
                raise ValueError("QuestMobile finding attribution diverges from exact excerpt")
            excerpt_hash = _sha256(
                finding.get("excerpt_sha256"),
                f"reports[{report_index}].findings[{finding_index}].excerpt_sha256",
            )
            if hashlib.sha256(excerpt.encode("utf-8")).hexdigest() != excerpt_hash:
                raise ValueError("QuestMobile finding excerpt hash mismatch")

            ref_id = f"report-finding:{finding_id}"
            evidence.append(
                EvidenceRef(
                    ref_id=ref_id,
                    locator=source_url,
                    excerpt=excerpt,
                    content_hash=raw_hash,
                )
            )
            claims.append(
                SemanticClaim(
                    claim_id=f"finding:{finding_id}",
                    primitive="EVIDENCE",
                    concept="PUBLIC_RESEARCH_FINDING_EXCERPT",
                    epistemic_status="OBSERVED",
                    evidence_refs=(ref_id,),
                    value={
                        "report_id": report_id,
                        "report_title": title,
                        "publication_date": publication_date,
                        "source_authority": "QuestMobile研究院",
                        "category_text": category_text,
                        "finding_attribution": attribution,
                        "excerpt_sha256": excerpt_hash,
                        "representativeness_status": "NOT_ESTABLISHED_FROM_PUBLIC_PAGE",
                        "current_local_reality_status": "NOT_ESTABLISHED",
                        "paid_demand_status": "NOT_ESTABLISHED",
                    },
                    geography="CN",
                )
            )
            observed_finding_count += 1

        envelopes.append(
            ObservationEnvelope(
                observation_id=_stable_id(
                    "obs:QM:public-research",
                    report_id,
                    source_url,
                ),
                source_id=SOURCE_ID,
                source_record_id=f"questmobile-report:{report_id}",
                source_locator=source_url,
                source_origin_geography="CN",
                relevance_geographies=("CN",),
                source_tier="PUBLIC_RESEARCH_REPORT_PRIMARY",
                observed_at=fetched_at,
                retrieved_at=fetched_at,
                published_at=published_at,
                parser_version=PARSER_VERSION,
                raw_payload_hash=raw_hash,
                sampling_boundary=(
                    "LATEST_PUBLIC_QUESTMOBILE_REPORTS_TEXT_FINDINGS_ONLY; "
                    "NATIONAL_RESEARCH_NE_LOCAL_REALITY; NO_IMAGE_OCR"
                ),
                evidence=tuple(evidence),
                claims=tuple(claims),
                actor_ids=(),
                unknown_fields=(
                    "exact_publication_time",
                    "panel_or_sample_representativeness",
                    "jiangsu_applicability",
                    "xuzhou_applicability",
                    "payer_identity",
                    "payment_status",
                    "opportunity_state",
                ),
            )
        )

    if observed_finding_count != declared_total:
        raise ValueError("QuestMobile declared text_finding_count diverges from adapted findings")
    if not envelopes:
        raise ValueError("QuestMobile producer contains no text-supported reports to adapt")
    return tuple(envelopes)


GOVERNING_INVARIANTS = (
    "PUBLIC_RESEARCH_FINDING_IS_EVIDENCE_NOT_HARD_MARKET_FACT",
    "QUESTMOBILE_NATIONAL_RESEARCH_NE_XUZHOU_REALITY",
    "RESEARCH_SAMPLE_OR_PANEL_NE_CENSUS",
    "RESEARCH_FINDING_NE_PAID_DEMAND",
    "RESEARCH_FINDING_NE_PAYER_OR_PAYMENT",
    "RESEARCH_FINDING_NE_OPPORTUNITY",
    "IMAGE_ONLY_EVIDENCE_REMAINS_UNOBSERVED_BY_THIS_ADAPTER",
    "UNKNOWN_NE_PASS",
)
