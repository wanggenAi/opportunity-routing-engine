"""Evidence-bound CN_PBOC adapter for the unified Observation Fabric.

The adapter consumes the already-collected official PBC financial-statistics artifact.
It treats the report as one source record, preserves each metric's exact source excerpt,
and separates level/flow facts from reported year-over-year changes.

Truth boundaries:
- aggregate money/credit statistics are not individual demand;
- financing/deposit/loan flow is not payment or paid need;
- macro state/change is not payer, blocker, route or opportunity;
- parsed values without metric-level source excerpts are rejected.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlparse

from src.observation_fabric import EvidenceRef, ObservationEnvelope, SemanticClaim


PARSER_VERSION = "pbc-observation-adapter.v1"

PRIMITIVE_BY_METRIC = {
    "social_financing_stock": "STATE",
    "social_financing_flow_ytd": "FLOW",
    "m2_balance": "STATE",
    "m1_balance": "STATE",
    "m0_balance": "STATE",
    "rmb_deposit_flow_ytd": "FLOW",
    "rmb_loan_flow_ytd": "FLOW",
    "interbank_lending_weighted_rate": "STATE",
    "pledged_repo_weighted_rate": "STATE",
    "fx_reserves": "STATE",
    "usd_cny_reference": "STATE",
}


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


def _official_pbc_url(value: object, field: str) -> str:
    url = _text(value, field)
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "www.pbc.gov.cn":
        raise ValueError(f"{field} must use official PBC HTTPS")
    return url


def _stable_id(prefix: str, *parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return f"{prefix}:{hashlib.sha256(payload).hexdigest()[:24]}"


def pbc_money_flow_observations(payload: Mapping[str, Any]) -> tuple[ObservationEnvelope, ...]:
    """Normalize one current official PBC financial-statistics report."""

    if payload.get("source_id") != "CN_PBOC":
        raise ValueError("unexpected PBC source_id")
    if payload.get("data_available") is not True:
        raise ValueError("PBC artifact has no available data")

    provenance = _mapping(payload.get("provenance"), "provenance")
    report_meta = _mapping(provenance.get("report"), "provenance.report")
    if report_meta.get("source_id") != "CN_PBOC":
        raise ValueError("PBC report provenance has unexpected source_id")
    locator = _official_pbc_url(report_meta.get("url"), "provenance.report.url")
    raw_hash = _sha256(report_meta.get("payload_sha256"), "provenance.report.payload_sha256")
    fetched_at = _text(report_meta.get("fetched_at_utc"), "provenance.report.fetched_at_utc")

    latest = _mapping(payload.get("latest_release"), "latest_release")
    if _official_pbc_url(latest.get("source_url"), "latest_release.source_url") != locator:
        raise ValueError("PBC latest_release source_url diverges from report provenance")
    title = _text(latest.get("title"), "latest_release.title")
    if not title.endswith("金融统计数据报告"):
        raise ValueError("unexpected PBC financial-statistics report title")
    release_date = _text(latest.get("release_date"), "latest_release.release_date")

    metrics = _mapping(latest.get("metrics"), "latest_release.metrics")
    metric_evidence = _mapping(latest.get("metric_evidence"), "latest_release.metric_evidence")
    if not metrics:
        raise ValueError("PBC report contains no metrics")
    if set(metrics) != set(metric_evidence):
        raise ValueError("PBC metric evidence coverage diverges from metrics")
    metric_count = latest.get("metric_count")
    if isinstance(metric_count, bool) or not isinstance(metric_count, int) or metric_count != len(metrics):
        raise ValueError("PBC metric_count diverges from metrics")

    evidence: list[EvidenceRef] = []
    claims: list[SemanticClaim] = []
    for metric_key in sorted(metrics):
        if metric_key not in PRIMITIVE_BY_METRIC:
            raise ValueError(f"unsupported PBC metric: {metric_key}")
        metric = _mapping(metrics[metric_key], f"metrics.{metric_key}")
        lineage = _mapping(metric_evidence[metric_key], f"metric_evidence.{metric_key}")
        if metric.get("value") is None:
            raise ValueError(f"PBC metric {metric_key} has null value")
        unit = _text(metric.get("unit"), f"metrics.{metric_key}.unit")
        value_excerpt = _text(lineage.get("value_excerpt"), f"metric_evidence.{metric_key}.value_excerpt")

        value_ref = f"report-value:{metric_key}"
        evidence.append(
            EvidenceRef(
                ref_id=value_ref,
                locator=locator,
                excerpt=value_excerpt,
                content_hash=raw_hash,
            )
        )
        base_concept = f"CN_PBOC_{metric_key.upper()}"
        claims.append(
            SemanticClaim(
                claim_id=metric_key,
                primitive=PRIMITIVE_BY_METRIC[metric_key],
                concept=base_concept,
                epistemic_status="OBSERVED",
                evidence_refs=(value_ref,),
                value={
                    "value": metric.get("value"),
                    "unit": unit,
                    "release_date": release_date,
                    "report_title": title,
                },
                geography="CN",
            )
        )

        if "yoy_pct" in metric:
            yoy = metric.get("yoy_pct")
            if yoy is None:
                raise ValueError(f"PBC metric {metric_key} has null yoy_pct")
            yoy_excerpt = _text(lineage.get("yoy_excerpt"), f"metric_evidence.{metric_key}.yoy_excerpt")
            yoy_ref = f"report-yoy:{metric_key}"
            evidence.append(
                EvidenceRef(
                    ref_id=yoy_ref,
                    locator=locator,
                    excerpt=yoy_excerpt,
                    content_hash=raw_hash,
                )
            )
            claims.append(
                SemanticClaim(
                    claim_id=f"{metric_key}_yoy",
                    primitive="CHANGE",
                    concept=f"{base_concept}_YOY",
                    epistemic_status="OBSERVED",
                    evidence_refs=(yoy_ref,),
                    value={
                        "value": yoy,
                        "unit": "percent",
                        "release_date": release_date,
                        "report_title": title,
                    },
                    geography="CN",
                )
            )
        elif lineage.get("yoy_excerpt") not in {None, ""}:
            raise ValueError(f"PBC metric {metric_key} has YoY evidence without yoy_pct")

    return (
        ObservationEnvelope(
            observation_id=_stable_id("obs:CN_PBOC:financial-report", release_date, title, locator),
            source_id="CN_PBOC",
            source_record_id=f"{release_date}:{title}",
            source_locator=locator,
            source_origin_geography="CN",
            relevance_geographies=("CN",),
            source_tier="OFFICIAL_CENTRAL_BANK_PRIMARY",
            observed_at=fetched_at,
            retrieved_at=fetched_at,
            parser_version=PARSER_VERSION,
            raw_payload_hash=raw_hash,
            sampling_boundary="LATEST_VISIBLE_OFFICIAL_PBC_FINANCIAL_STATISTICS_REPORT_EXACT_METRIC_EXCERPTS_ONLY",
            evidence=tuple(evidence),
            claims=tuple(claims),
            actor_ids=(),
            unknown_fields=("exact_publication_time",),
        ),
    )


GOVERNING_INVARIANTS = (
    "PBC_PARSED_METRIC_REQUIRES_EXACT_SOURCE_EXCERPT",
    "PBC_YOY_IS_SEPARATE_CHANGE_CLAIM",
    "AGGREGATE_MONEY_STATISTIC_NE_INDIVIDUAL_DEMAND",
    "MONEY_FLOW_NE_PAYMENT_OR_PAID_NEED",
    "MACRO_STATE_OR_CHANGE_NE_PAYER_OR_OPPORTUNITY",
    "UNKNOWN_NE_PASS",
)
