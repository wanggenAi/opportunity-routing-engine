"""Truth-preserving official macro/credit adapters for the Observation Fabric.

These adapters normalize already-collected public official artifacts. They preserve
aggregate measurement semantics and never project macro aggregates into individual
demand, payer, payment, route-testable, taxonomy or opportunity truth.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import Any
from urllib.parse import urlparse

from src.observation_fabric import EvidenceRef, ObservationEnvelope, SemanticClaim

PARSER_VERSION = "official-macro-observation-adapters.v1"


def _mapping(value: object, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return value


def _sequence(value: object, field: str) -> Sequence[object]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    return value


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} is required")
    return value.strip()


def _sha256(value: object, field: str) -> str:
    result = _text(value, field).lower()
    if len(result) != 64 or any(ch not in "0123456789abcdef" for ch in result):
        raise ValueError(f"{field} must be a SHA-256 hex digest")
    return result


def _official_url(value: object, field: str, *, hosts: set[str]) -> str:
    url = _text(value, field)
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in hosts:
        raise ValueError(f"{field} must use an approved official HTTPS host")
    return url


def _stable_id(prefix: str, *parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return f"{prefix}:{hashlib.sha256(payload).hexdigest()[:24]}"


def _evidence_excerpt(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def nbs_macro_watchlist_observations(
    payload: Mapping[str, Any],
) -> tuple[ObservationEnvelope, ...]:
    """Convert exact-identity available NBS watchlist records into observations."""

    if payload.get("source_id") != "CN_NBS":
        raise ValueError("unexpected NBS source_id")

    groups = _sequence(payload.get("groups"), "groups")
    request_by_hash: dict[str, Mapping[str, Any]] = {}
    for index, raw_group in enumerate(groups):
        group = _mapping(raw_group, f"groups[{index}]")
        request = _mapping(group.get("request"), f"groups[{index}].request")
        if request.get("source_id") != "CN_NBS":
            raise ValueError("NBS request has unexpected source_id")
        digest = _sha256(request.get("payload_sha256"), "NBS request payload_sha256")
        _official_url(
            request.get("url"),
            "NBS request url",
            hosts={"data.stats.gov.cn"},
        )
        if digest in request_by_hash:
            raise ValueError(f"duplicate NBS request payload hash: {digest}")
        request_by_hash[digest] = request

    signals = _sequence(payload.get("signals"), "signals")
    result: list[ObservationEnvelope] = []
    seen_records: set[tuple[str, str]] = set()
    available_count = 0
    for index, raw_signal in enumerate(signals):
        signal = _mapping(raw_signal, f"signals[{index}]")
        status = _text(signal.get("status"), f"signals[{index}].status")
        if status != "AVAILABLE":
            continue
        available_count += 1
        if signal.get("source_id") != "CN_NBS":
            raise ValueError("NBS signal has unexpected source_id")
        if signal.get("identity_status") != "MATCH":
            raise ValueError("available NBS signal must have exact identity match")
        if signal.get("geography") != "China":
            raise ValueError("NBS signal geography must be China")

        signal_id = _text(signal.get("signal_id"), f"signals[{index}].signal_id")
        metric_kind = _text(signal.get("metric_kind"), f"signals[{index}].metric_kind")
        if metric_kind in {"level", "index"}:
            primitive = "STATE"
        elif metric_kind in {"yoy_growth", "cumulative_growth"}:
            primitive = "CHANGE"
        else:
            raise ValueError(f"unsupported NBS metric_kind: {metric_kind}")

        selected = _mapping(signal.get("selected_record"), f"signals[{index}].selected_record")
        if selected.get("source_id") != "CN_NBS":
            raise ValueError("NBS selected record has unexpected source_id")
        if selected.get("value_present") is not True:
            raise ValueError("available NBS selected record must contain a value")
        period_code = _text(selected.get("period_code"), "NBS selected period_code")
        if str(selected.get("value")) != str(signal.get("value")):
            raise ValueError(f"NBS signal {signal_id} value diverges from selected record")
        if str(selected.get("unit")) != str(signal.get("actual_unit")):
            raise ValueError(f"NBS signal {signal_id} unit diverges from selected record")
        if str(selected.get("indicator_label")) != str(signal.get("actual_label")):
            raise ValueError(f"NBS signal {signal_id} label diverges from selected record")

        request_hash = _sha256(signal.get("request_sha256"), f"NBS signal {signal_id} request_sha256")
        request = request_by_hash.get(request_hash)
        if request is None:
            raise ValueError(f"NBS signal {signal_id} request provenance is missing")
        fetched_at = _text(signal.get("fetched_at_utc"), f"NBS signal {signal_id} fetched_at_utc")
        if fetched_at != _text(request.get("fetched_at_utc"), "NBS request fetched_at_utc"):
            raise ValueError(f"NBS signal {signal_id} fetch timestamp diverges from request")
        locator = _official_url(
            request.get("url"),
            "NBS request url",
            hosts={"data.stats.gov.cn"},
        )

        identity = (signal_id, period_code)
        if identity in seen_records:
            raise ValueError(f"duplicate NBS signal-period record: {identity}")
        seen_records.add(identity)
        ref_id = f"record:{signal_id}:{period_code}"
        evidence = EvidenceRef(
            ref_id=ref_id,
            locator=locator,
            excerpt=_evidence_excerpt(selected),
            content_hash=request_hash,
        )
        claim = SemanticClaim(
            claim_id=signal_id,
            primitive=primitive,
            concept=signal_id,
            epistemic_status="OBSERVED",
            evidence_refs=(ref_id,),
            value={
                "value": selected.get("value"),
                "unit": selected.get("unit"),
                "metric_kind": metric_kind,
                "indicator_label": selected.get("indicator_label"),
                "indicator_id": selected.get("indicator_id"),
                "period_code": period_code,
                "period_name": selected.get("period_name"),
                "frequency": selected.get("frequency"),
                "area_code": selected.get("area_code"),
                "area_name": selected.get("area_name"),
                "period_lag": signal.get("period_lag"),
            },
            geography="CN",
        )
        result.append(
            ObservationEnvelope(
                observation_id=_stable_id("obs:CN_NBS:macro", signal_id, period_code),
                source_id="CN_NBS",
                source_record_id=f"{signal_id}:{period_code}",
                source_locator=locator,
                source_origin_geography="CN",
                relevance_geographies=("CN",),
                source_tier="OFFICIAL_GOVERNMENT_PRIMARY",
                observed_at=fetched_at,
                retrieved_at=fetched_at,
                parser_version=PARSER_VERSION,
                raw_payload_hash=request_hash,
                sampling_boundary="CONFIGURED_NBS_MACRO_WATCHLIST_AVAILABLE_EXACT_IDENTITY_MATCH_ONLY",
                evidence=(evidence,),
                claims=(claim,),
                actor_ids=(),
                unknown_fields=("publication_date", "exact_publication_time"),
            )
        )

    declared_available = payload.get("available_signal_count")
    if isinstance(declared_available, bool) or not isinstance(declared_available, int):
        raise ValueError("NBS available_signal_count must be an integer")
    if declared_available != available_count:
        raise ValueError("NBS available_signal_count diverges from signals")
    if not result:
        raise ValueError("NBS watchlist contains no available exact-identity observations")
    return tuple(result)


def pbc_jiangsu_credit_observations(
    payload: Mapping[str, Any],
) -> tuple[ObservationEnvelope, ...]:
    """Convert evidence-backed PBC Jiangsu monthly RMB balance rows into one observation."""

    if payload.get("source_id") != "CN_PBOC_JS":
        raise ValueError("unexpected PBC Jiangsu source_id")
    if payload.get("data_available") is not True:
        raise ValueError("PBC Jiangsu artifact has no available data")
    if payload.get("geography") != "Jiangsu":
        raise ValueError("unexpected PBC Jiangsu geography")

    provenance = _mapping(payload.get("provenance"), "provenance")
    xls = _mapping(provenance.get("xls"), "provenance.xls")
    if xls.get("source_id") != "CN_PBOC_JS":
        raise ValueError("PBC Jiangsu XLS provenance has unexpected source_id")
    locator = _official_url(
        xls.get("url"),
        "provenance.xls.url",
        hosts={"nanjing.pbc.gov.cn"},
    )
    raw_hash = _sha256(xls.get("payload_sha256"), "provenance.xls.payload_sha256")
    fetched_at = _text(xls.get("fetched_at_utc"), "provenance.xls.fetched_at_utc")

    observation = _mapping(payload.get("observation"), "observation")
    period = _text(payload.get("observation_period"), "observation_period")
    period_key = _text(observation.get("period_key"), "observation.period_key")
    unit = _text(observation.get("unit"), "observation.unit")
    if unit != "100m_cny":
        raise ValueError("PBC Jiangsu observation unit must be 100m_cny")
    if observation.get("period_gate") != "EXPLICIT_PERIOD_HEADER":
        raise ValueError("PBC Jiangsu observation lacks explicit period header gate")

    metrics = _mapping(observation.get("metrics"), "observation.metrics")
    metric_evidence = _mapping(observation.get("metric_evidence"), "observation.metric_evidence")
    if not metric_evidence:
        raise ValueError("PBC Jiangsu observation contains no metric evidence")

    evidence: list[EvidenceRef] = []
    claims: list[SemanticClaim] = []
    for metric_key in sorted(metric_evidence):
        raw_evidence = _mapping(metric_evidence[metric_key], f"metric_evidence.{metric_key}")
        if metric_key not in metrics:
            raise ValueError(f"PBC Jiangsu evidence has no metric value: {metric_key}")
        raw_value = raw_evidence.get("raw_value")
        if metrics[metric_key] != raw_value:
            raise ValueError(f"PBC Jiangsu metric {metric_key} diverges from evidence row")
        row_values = raw_evidence.get("row_values")
        if not isinstance(row_values, list) or not row_values:
            raise ValueError(f"PBC Jiangsu metric {metric_key} row_values are required")
        label_token = _text(raw_evidence.get("label_token"), f"metric_evidence.{metric_key}.label_token")
        ref_id = f"xls-row:{metric_key}"
        evidence_payload = {
            "period_key": period_key,
            "label_token": label_token,
            "raw_value": raw_value,
            "row_number_1based": raw_evidence.get("row_number_1based"),
            "value_column_1based": raw_evidence.get("value_column_1based"),
            "row_values": row_values,
        }
        evidence.append(
            EvidenceRef(
                ref_id=ref_id,
                locator=locator,
                excerpt=_evidence_excerpt(evidence_payload),
                content_hash=raw_hash,
            )
        )
        concept = f"CN_PBOC_JS_{metric_key.upper()}"
        claims.append(
            SemanticClaim(
                claim_id=metric_key,
                primitive="STATE",
                concept=concept,
                epistemic_status="OBSERVED",
                evidence_refs=(ref_id,),
                value={
                    "value": raw_value,
                    "unit": unit,
                    "period": period,
                    "period_key": period_key,
                    "label_token": label_token,
                    "release_date": payload.get("release_date"),
                    "table_title": payload.get("table_title"),
                    "sheet_name": observation.get("sheet_name"),
                },
                geography="CN-JS",
            )
        )

    return (
        ObservationEnvelope(
            observation_id=_stable_id(
                "obs:CN_PBOC_JS:credit",
                period,
                _text(observation.get("sheet_name"), "observation.sheet_name"),
            ),
            source_id="CN_PBOC_JS",
            source_record_id=f"{period}:{period_key}",
            source_locator=locator,
            source_origin_geography="CN-JS",
            relevance_geographies=("CN-JS",),
            source_tier="OFFICIAL_CENTRAL_BANK_REGIONAL_PRIMARY",
            observed_at=fetched_at,
            retrieved_at=fetched_at,
            parser_version=PARSER_VERSION,
            raw_payload_hash=raw_hash,
            sampling_boundary="LATEST_PUBLIC_PBC_JIANGSU_RMB_CREDIT_XLS_EXACT_PERIOD_EVIDENCE_ROWS_ONLY",
            evidence=tuple(evidence),
            claims=tuple(claims),
            actor_ids=(),
            unknown_fields=("exact_publication_time",),
        ),
    )


GOVERNING_INVARIANTS = (
    "OFFICIAL_MACRO_AGGREGATE_NE_INDIVIDUAL_DEMAND",
    "CREDIT_BALANCE_NE_PAID_NEED",
    "MONEY_OR_CREDIT_STATE_NE_PAYER",
    "MACRO_CHANGE_NE_OPPORTUNITY",
    "DERIVED_UNIT_CONVERSION_NE_DUPLICATE_OBSERVATION",
    "SOURCE_IDENTITY_MUST_MATCH_EVIDENCE_PROVENANCE",
    "UNKNOWN_NE_PASS",
)
