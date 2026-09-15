"""Corroboration-gated CN_CUSTOMS adapter for the unified Observation Fabric.

Only source-native GACC rows with exact row-level lineage may enter the Fabric. The
current official artifact contains one Jiangsu importer/exporter-location row and
Xuzhou specific-customs-area rows; absence of a Xuzhou whole-city row stays UNKNOWN.

The independent Jiangsu Government HTTPS source is an acceptance gate for period,
Jiangsu identity and import/export direction only. It does not confirm GACC USD row
values and is never used as row-level monetary evidence.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlparse

from src.gacc_trade_row_evidence import validate_gacc_trade_row_evidence
from src.observation_fabric import EvidenceRef, ObservationEnvelope, SemanticClaim


PARSER_VERSION = "gacc-trade-observation-adapter.v1"
REQUIRED_TRUTH_BOUNDARIES = frozenset({
    "PLAINTEXT_HTTP_REQUIRES_CORROBORATION",
    "TABLE8_TOTAL_DERIVED_ONLY_FROM_COMPLETE_EXPORT_IMPORT",
    "IMPORTER_EXPORTER_LOCATION_IS_NOT_DOMESTIC_ORIGIN_DESTINATION",
    "SPECIFIC_AREA_IS_NOT_WHOLE_XUZHOU",
    "NO_CROSS_TABLE_SUM",
    "MISSING_STAYS_UNKNOWN",
    "TRADE_FLOW_IS_NOT_UNMET_NEED",
    "TRADE_FLOW_IS_NOT_SURPLUS_RESOURCE",
    "NO_TRANSACTION_BLOCKER_INFERENCE",
    "NO_OPPORTUNITY_INFERENCE",
    "ROW_EVIDENCE_REQUIRES_STABLE_REFETCH",
    "WHOLE_PAGE_HASH_NE_ROW_LEVEL_LINEAGE",
    "CORROBORATION_GATE_NE_ROW_LEVEL_VALUE_CONFIRMATION",
    "DERIVED_TOTAL_NE_SOURCE_CELL",
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


def _number(value: str, field: str) -> float:
    raw = value.strip().replace(",", "").replace("%", "")
    try:
        return float(raw)
    except ValueError as exc:
        raise ValueError(f"{field} row evidence is not numeric") from exc


def _numeric(value: object, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be numeric")
    return float(value)


def _same_number(value: object, source_cell: str, field: str) -> float:
    parsed = _numeric(value, field)
    evidence = _number(source_cell, field)
    if parsed != evidence:
        raise ValueError(f"{field} diverges from exact GACC row evidence")
    return parsed


def _stable_id(prefix: str, *parts: str) -> str:
    raw = "\x1f".join(parts).encode("utf-8")
    return f"{prefix}:{hashlib.sha256(raw).hexdigest()[:24]}"


def _official_gacc_http(value: object, field: str) -> str:
    url = _text(value, field)
    parsed = urlparse(url)
    if parsed.scheme != "http" or parsed.hostname != "english.customs.gov.cn" or not parsed.path.lower().startswith("/statics/"):
        raise ValueError(f"{field} must be an official GACC HTTP detail URL")
    return url


def _official_jiangsu_https(value: object, field: str) -> str:
    url = _text(value, field)
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "jszwb.jiangsu.gov.cn":
        raise ValueError(f"{field} must be the governed Jiangsu HTTPS corroboration source")
    return url


def _validate_corroboration(payload: Mapping[str, Any]) -> tuple[str, str, str]:
    if payload.get("transport_security") != "PLAINTEXT_HTTP":
        raise ValueError("CN_CUSTOMS transport security drifted")
    if payload.get("corroboration_required") is not True:
        raise ValueError("CN_CUSTOMS must remain corroboration-required")
    if payload.get("corroboration_status") != "PERIOD_IDENTITY_DIRECTION_CORROBORATED":
        raise ValueError("CN_CUSTOMS requires successful period/identity/direction corroboration")

    period = _text(payload.get("period"), "period")
    corroboration = _mapping(payload.get("corroboration"), "corroboration")
    if corroboration.get("source_id") != "JS_GOV":
        raise ValueError("unexpected CN_CUSTOMS corroboration source")
    if corroboration.get("period") != period:
        raise ValueError("CN_CUSTOMS corroboration period diverges from GACC period")
    if corroboration.get("geography") != "Jiangsu":
        raise ValueError("CN_CUSTOMS corroboration geography drifted")
    if corroboration.get("basis") != "PERIOD_IDENTITY_DIRECTION_ONLY":
        raise ValueError("CN_CUSTOMS corroboration basis drifted")
    if corroboration.get("monetary_value_comparison") != "UNAVAILABLE_CROSS_CURRENCY":
        raise ValueError("CN_CUSTOMS monetary values must not be treated as directly corroborated")
    if corroboration.get("reported_currency") != "CNY":
        raise ValueError("CN_CUSTOMS corroboration currency drifted")

    provenance = _mapping(corroboration.get("provenance"), "corroboration.provenance")
    if provenance.get("source_id") != "JS_GOV":
        raise ValueError("CN_CUSTOMS corroboration provenance source drifted")
    url = _official_jiangsu_https(provenance.get("url"), "corroboration.provenance.url")
    digest = _sha256(provenance.get("payload_sha256"), "corroboration.provenance.payload_sha256")
    _text(provenance.get("fetched_at_utc"), "corroboration.provenance.fetched_at_utc")
    return period, url, digest


def _row_evidence(row: Mapping[str, Any], *, expected_table: int) -> tuple[list[str], str, str]:
    evidence = _mapping(row.get("source_row_evidence"), "source_row_evidence")
    if evidence.get("contract") != "gacc-source-row-evidence.v1":
        raise ValueError("unsupported GACC row-evidence contract")
    if evidence.get("source_id") != "CN_CUSTOMS" or evidence.get("table_number") != expected_table:
        raise ValueError("GACC row-evidence source/table identity mismatch")
    cells = evidence.get("row_cells")
    if not isinstance(cells, list) or any(not isinstance(item, str) for item in cells):
        raise ValueError("GACC row-evidence cells are invalid")
    if len(cells) != (7 if expected_table == 8 else 10):
        raise ValueError("GACC row-evidence cell count drifted")
    name = _text(row.get("name"), "row.name")
    if cells[0].strip().casefold() != name.casefold():
        raise ValueError("GACC row identity diverges from exact evidence")
    locator = _official_gacc_http(evidence.get("source_url"), "source_row_evidence.source_url")
    raw_hash = _sha256(evidence.get("source_payload_sha256"), "source_row_evidence.source_payload_sha256")
    _sha256(evidence.get("row_sha256"), "source_row_evidence.row_sha256")
    if _text(evidence.get("row_text"), "source_row_evidence.row_text") != " | ".join(cells):
        raise ValueError("GACC row text diverges from row cells")
    return cells, locator, raw_hash


def _claim(
    *,
    claim_id: str,
    primitive: str,
    concept: str,
    evidence_ref: str,
    value: float,
    unit: str,
    period: str,
    period_scope: str,
    entity_name: str,
    entity_scope: str,
    geography: str,
    table_number: int,
    total_basis: str | None = None,
) -> SemanticClaim:
    payload: dict[str, Any] = {
        "value": value,
        "unit": unit,
        "period": period,
        "period_scope": period_scope,
        "entity_name": entity_name,
        "entity_scope": entity_scope,
        "table_number": table_number,
        "corroboration_status": "PERIOD_IDENTITY_DIRECTION_CORROBORATED",
        "corroboration_basis": "PERIOD_IDENTITY_DIRECTION_ONLY",
        "monetary_value_comparison": "UNAVAILABLE_CROSS_CURRENCY",
    }
    if total_basis is not None:
        payload["total_basis"] = total_basis
    return SemanticClaim(
        claim_id=claim_id,
        primitive=primitive,
        concept=concept,
        epistemic_status="OBSERVED",
        evidence_refs=(evidence_ref,),
        value=payload,
        geography=geography,
    )


def _table8_envelope(
    row: Mapping[str, Any],
    *,
    period: str,
    fetched_at: str,
    corroboration_url: str,
    corroboration_hash: str,
) -> ObservationEnvelope:
    cells, locator, raw_hash = _row_evidence(row, expected_table=8)
    if row.get("total_basis") != "DERIVED_EXPORT_PLUS_IMPORT":
        raise ValueError("GACC table-8 total basis drifted")

    exports_month = _same_number(row.get("exports_month_usd_thousand"), cells[1], "exports_month_usd_thousand")
    exports_ytd = _same_number(row.get("exports_ytd_usd_thousand"), cells[2], "exports_ytd_usd_thousand")
    imports_month = _same_number(row.get("imports_month_usd_thousand"), cells[3], "imports_month_usd_thousand")
    imports_ytd = _same_number(row.get("imports_ytd_usd_thousand"), cells[4], "imports_ytd_usd_thousand")
    exports_yoy = _same_number(row.get("exports_yoy_percent"), cells[5], "exports_yoy_percent")
    imports_yoy = _same_number(row.get("imports_yoy_percent"), cells[6], "imports_yoy_percent")
    if row.get("total_yoy_percent") is not None:
        raise ValueError("GACC table-8 derived total must not manufacture total YoY")
    if _numeric(row.get("total_month_usd_thousand"), "total_month_usd_thousand") != exports_month + imports_month:
        raise ValueError("GACC table-8 derived monthly total is inconsistent")
    if _numeric(row.get("total_ytd_usd_thousand"), "total_ytd_usd_thousand") != exports_ytd + imports_ytd:
        raise ValueError("GACC table-8 derived YTD total is inconsistent")

    name = _text(row.get("name"), "row.name")
    if name.casefold() not in {"jiangsu", "jiangsu province", "xuzhou"}:
        raise ValueError("unexpected GACC table-8 governed row identity")
    geography = "CN-JS-XZ" if name.casefold() == "xuzhou" else "CN-JS"
    entity_scope = "IMPORTER_EXPORTER_LOCATION"
    row_ref = "gacc-row:table8"
    claims = (
        _claim(claim_id="exports_month", primitive="FLOW", concept="CN_CUSTOMS_IMPORTER_EXPORTER_LOCATION_EXPORTS_MONTH", evidence_ref=row_ref, value=exports_month, unit="USD_THOUSAND", period=period, period_scope="MONTH", entity_name=name, entity_scope=entity_scope, geography=geography, table_number=8),
        _claim(claim_id="exports_ytd", primitive="FLOW", concept="CN_CUSTOMS_IMPORTER_EXPORTER_LOCATION_EXPORTS_YTD", evidence_ref=row_ref, value=exports_ytd, unit="USD_THOUSAND", period=period, period_scope="YTD", entity_name=name, entity_scope=entity_scope, geography=geography, table_number=8),
        _claim(claim_id="imports_month", primitive="FLOW", concept="CN_CUSTOMS_IMPORTER_EXPORTER_LOCATION_IMPORTS_MONTH", evidence_ref=row_ref, value=imports_month, unit="USD_THOUSAND", period=period, period_scope="MONTH", entity_name=name, entity_scope=entity_scope, geography=geography, table_number=8),
        _claim(claim_id="imports_ytd", primitive="FLOW", concept="CN_CUSTOMS_IMPORTER_EXPORTER_LOCATION_IMPORTS_YTD", evidence_ref=row_ref, value=imports_ytd, unit="USD_THOUSAND", period=period, period_scope="YTD", entity_name=name, entity_scope=entity_scope, geography=geography, table_number=8),
        _claim(claim_id="exports_yoy", primitive="CHANGE", concept="CN_CUSTOMS_IMPORTER_EXPORTER_LOCATION_EXPORTS_YOY", evidence_ref=row_ref, value=exports_yoy, unit="PERCENT", period=period, period_scope="YTD_REPORTED_CHANGE", entity_name=name, entity_scope=entity_scope, geography=geography, table_number=8),
        _claim(claim_id="imports_yoy", primitive="CHANGE", concept="CN_CUSTOMS_IMPORTER_EXPORTER_LOCATION_IMPORTS_YOY", evidence_ref=row_ref, value=imports_yoy, unit="PERCENT", period=period, period_scope="YTD_REPORTED_CHANGE", entity_name=name, entity_scope=entity_scope, geography=geography, table_number=8),
    )
    identity = f"{period}:table8:{name}"
    return ObservationEnvelope(
        observation_id=_stable_id("obs:CN_CUSTOMS", identity),
        source_id="CN_CUSTOMS",
        source_record_id=identity,
        source_locator=locator,
        source_origin_geography="CN",
        relevance_geographies=(geography,),
        source_tier="OFFICIAL_CUSTOMS_PRIMARY_PLAINTEXT_CORROBORATION_GATED",
        observed_at=fetched_at,
        retrieved_at=fetched_at,
        parser_version=PARSER_VERSION,
        raw_payload_hash=raw_hash,
        sampling_boundary="GACC_TABLE_8_GOVERNED_ROWS_ONLY; IMPORTER_EXPORTER_LOCATION_NE_DOMESTIC_ORIGIN_DESTINATION; DERIVED_TOTAL_NOT_EMITTED",
        evidence=(
            EvidenceRef(ref_id=row_ref, locator=locator, excerpt=" | ".join(cells), content_hash=raw_hash),
            EvidenceRef(ref_id="jiangsu-https-corroboration", locator=corroboration_url, content_hash=corroboration_hash),
        ),
        claims=claims,
        unknown_fields=("domestic_origin_destination_mapping", "payer_identity", "payment_status", "opportunity_state"),
    )


def _table11_envelope(
    row: Mapping[str, Any],
    *,
    period: str,
    fetched_at: str,
    corroboration_url: str,
    corroboration_hash: str,
) -> ObservationEnvelope:
    cells, locator, raw_hash = _row_evidence(row, expected_table=11)
    if row.get("total_basis") != "EXPLICIT_GACC":
        raise ValueError("GACC specific-area total must remain explicit source data")
    name = _text(row.get("name"), "row.name")
    if "xuzhou" not in name.casefold():
        raise ValueError("unexpected governed GACC specific-area identity")

    fields = (
        ("total_month_usd_thousand", 1, "total_month", "FLOW", "CN_CUSTOMS_SPECIFIC_AREA_TOTAL_MONTH", "MONTH", "USD_THOUSAND"),
        ("total_ytd_usd_thousand", 2, "total_ytd", "FLOW", "CN_CUSTOMS_SPECIFIC_AREA_TOTAL_YTD", "YTD", "USD_THOUSAND"),
        ("exports_month_usd_thousand", 3, "exports_month", "FLOW", "CN_CUSTOMS_SPECIFIC_AREA_EXPORTS_MONTH", "MONTH", "USD_THOUSAND"),
        ("exports_ytd_usd_thousand", 4, "exports_ytd", "FLOW", "CN_CUSTOMS_SPECIFIC_AREA_EXPORTS_YTD", "YTD", "USD_THOUSAND"),
        ("imports_month_usd_thousand", 5, "imports_month", "FLOW", "CN_CUSTOMS_SPECIFIC_AREA_IMPORTS_MONTH", "MONTH", "USD_THOUSAND"),
        ("imports_ytd_usd_thousand", 6, "imports_ytd", "FLOW", "CN_CUSTOMS_SPECIFIC_AREA_IMPORTS_YTD", "YTD", "USD_THOUSAND"),
        ("total_yoy_percent", 7, "total_yoy", "CHANGE", "CN_CUSTOMS_SPECIFIC_AREA_TOTAL_YOY", "YTD_REPORTED_CHANGE", "PERCENT"),
        ("exports_yoy_percent", 8, "exports_yoy", "CHANGE", "CN_CUSTOMS_SPECIFIC_AREA_EXPORTS_YOY", "YTD_REPORTED_CHANGE", "PERCENT"),
        ("imports_yoy_percent", 9, "imports_yoy", "CHANGE", "CN_CUSTOMS_SPECIFIC_AREA_IMPORTS_YOY", "YTD_REPORTED_CHANGE", "PERCENT"),
    )
    row_ref = "gacc-row:table11"
    claims = tuple(
        _claim(
            claim_id=claim_id,
            primitive=primitive,
            concept=concept,
            evidence_ref=row_ref,
            value=_same_number(row.get(field), cells[index], field),
            unit=unit,
            period=period,
            period_scope=scope,
            entity_name=name,
            entity_scope="SPECIFIC_CUSTOMS_AREA",
            geography="CN-JS-XZ",
            table_number=11,
            total_basis="EXPLICIT_GACC" if claim_id.startswith("total_") else None,
        )
        for field, index, claim_id, primitive, concept, scope, unit in fields
    )
    identity = f"{period}:table11:{name}"
    return ObservationEnvelope(
        observation_id=_stable_id("obs:CN_CUSTOMS", identity),
        source_id="CN_CUSTOMS",
        source_record_id=identity,
        source_locator=locator,
        source_origin_geography="CN",
        relevance_geographies=("CN-JS-XZ",),
        source_tier="OFFICIAL_CUSTOMS_PRIMARY_PLAINTEXT_CORROBORATION_GATED",
        observed_at=fetched_at,
        retrieved_at=fetched_at,
        parser_version=PARSER_VERSION,
        raw_payload_hash=raw_hash,
        sampling_boundary="GACC_TABLE_11_EXPLICIT_XUZHOU_SPECIFIC_AREAS_ONLY; SPECIFIC_CUSTOMS_AREA_NE_WHOLE_XUZHOU; NO_CROSS_AREA_SUM",
        evidence=(
            EvidenceRef(ref_id=row_ref, locator=locator, excerpt=" | ".join(cells), content_hash=raw_hash),
            EvidenceRef(ref_id="jiangsu-https-corroboration", locator=corroboration_url, content_hash=corroboration_hash),
        ),
        claims=claims,
        unknown_fields=("whole_xuzhou_trade_flow", "domestic_origin_destination_mapping", "payer_identity", "payment_status", "opportunity_state"),
    )


def gacc_trade_flow_observations(payload: Mapping[str, Any]) -> tuple[ObservationEnvelope, ...]:
    """Normalize corroboration-gated GACC trade rows without geographic promotion."""

    if payload.get("source_id") != "CN_CUSTOMS" or payload.get("evidence_kind") != "CUSTOMS_TRADE_FLOW":
        raise ValueError("unexpected CN_CUSTOMS artifact identity")
    if payload.get("unit") != "USD_THOUSAND":
        raise ValueError("unexpected CN_CUSTOMS unit")
    if payload.get("row_evidence_complete") is not True:
        raise ValueError("CN_CUSTOMS row-level evidence is incomplete")
    validate_gacc_trade_row_evidence(payload)
    missing = REQUIRED_TRUTH_BOUNDARIES - set(payload.get("truth_boundaries") or ())
    if missing:
        raise ValueError(f"CN_CUSTOMS truth boundaries missing: {sorted(missing)}")

    period, corroboration_url, corroboration_hash = _validate_corroboration(payload)
    table8 = _mapping(payload.get("table_8_provenance"), "table_8_provenance")
    table11 = _mapping(payload.get("table_11_provenance"), "table_11_provenance")
    table8_time = _text(table8.get("fetched_at_utc"), "table_8_provenance.fetched_at_utc")
    table11_time = _text(table11.get("fetched_at_utc"), "table_11_provenance.fetched_at_utc")

    envelopes: list[ObservationEnvelope] = []
    jiangsu = _mapping(payload.get("jiangsu_importer_exporter_location"), "jiangsu_importer_exporter_location")
    envelopes.append(_table8_envelope(jiangsu, period=period, fetched_at=table8_time, corroboration_url=corroboration_url, corroboration_hash=corroboration_hash))

    xuzhou_whole = payload.get("xuzhou_importer_exporter_location")
    if xuzhou_whole is not None:
        envelopes.append(_table8_envelope(_mapping(xuzhou_whole, "xuzhou_importer_exporter_location"), period=period, fetched_at=table8_time, corroboration_url=corroboration_url, corroboration_hash=corroboration_hash))

    areas = payload.get("xuzhou_specific_areas")
    if not isinstance(areas, list):
        raise ValueError("CN_CUSTOMS Xuzhou specific-area collection must be a list")
    if xuzhou_whole is None and not areas:
        raise ValueError("CN_CUSTOMS has no explicit Xuzhou whole-city or specific-area evidence")
    for index, raw in enumerate(areas):
        envelopes.append(_table11_envelope(_mapping(raw, f"xuzhou_specific_areas[{index}]"), period=period, fetched_at=table11_time, corroboration_url=corroboration_url, corroboration_hash=corroboration_hash))

    return tuple(envelopes)


GOVERNING_INVARIANTS = (
    "PLAINTEXT_GACC_ROW_REQUIRES_CORROBORATION_GATE",
    "GACC_ROW_CLAIM_REQUIRES_EXACT_ROW_EVIDENCE",
    "CORROBORATION_GATE_NE_ROW_LEVEL_VALUE_CONFIRMATION",
    "IMPORTER_EXPORTER_LOCATION_NE_DOMESTIC_ORIGIN_DESTINATION",
    "SPECIFIC_CUSTOMS_AREA_NE_WHOLE_XUZHOU",
    "TABLE8_DERIVED_TOTAL_IS_NOT_EMITTED_AS_SOURCE_NATIVE_CLAIM",
    "TRADE_FLOW_NE_PAYMENT_OR_PAID_NEED",
    "TRADE_FLOW_NE_OPPORTUNITY",
    "UNKNOWN_NE_PASS",
)
