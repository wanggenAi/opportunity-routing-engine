"""Bind parsed GACC trade rows to exact source-row evidence.

The core GACC parser intentionally keeps transport/provenance separate from parsed
trade values.  Before those values can enter the source-neutral Observation Fabric,
we need a row-level lineage object rather than only a whole-page payload hash.

This module performs a fail-closed stable refetch of the already-selected official
GACC table pages.  The second payload must have the exact same SHA-256 as the first
fetch recorded by ``GaccTradeFlowAdapter``.  Only then are the normalized source
cells for each serialized Jiangsu/Xuzhou row attached to that row.

The independent Jiangsu HTTPS corroborator remains a dataset acceptance gate for
period / identity / import-export direction.  It is not treated as row-level value
corroboration.
"""

from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from typing import Any

from src.gacc_trade_flow import parse_html_tables
from src.html_ingest import normalize_whitespace


ROW_EVIDENCE_CONTRACT = "gacc-source-row-evidence.v1"


def _canonical_cells(cells: list[dict[str, Any]]) -> list[str]:
    result: list[str] = []
    for cell in cells:
        if not isinstance(cell, Mapping):
            raise ValueError("GACC parsed table cell must be an object")
        text = cell.get("text")
        if not isinstance(text, str):
            raise ValueError("GACC parsed table cell text must be a string")
        result.append(normalize_whitespace(text))
    return result


def _row_sha256(cells: list[str]) -> str:
    encoded = json.dumps(
        cells,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _stable_table_rows(
    *,
    client: Any,
    provenance: Mapping[str, Any],
    table_number: int,
) -> tuple[list[list[dict[str, Any]]], dict[str, Any]]:
    url = provenance.get("url")
    expected_sha = provenance.get("payload_sha256")
    if not isinstance(url, str) or not url:
        raise ValueError(f"GACC table {table_number} provenance URL is missing")
    if not isinstance(expected_sha, str) or len(expected_sha) != 64:
        raise ValueError(f"GACC table {table_number} payload SHA-256 is missing")

    env = client.fetch(
        url,
        request_name=f"gacc.row_evidence.table_{table_number}",
    )
    meta = env.metadata()
    actual_sha = meta.get("payload_sha256")
    if env.url != url:
        raise ValueError(f"GACC table {table_number} row-evidence refetch URL changed")
    if actual_sha != expected_sha:
        raise ValueError(
            f"GACC table {table_number} changed between parse and row-evidence refetch"
        )
    if meta.get("source_id") != "CN_CUSTOMS":
        raise ValueError(f"GACC table {table_number} refetch source identity changed")

    return parse_html_tables(env.html, base_url=env.url), dict(meta)


def _find_exact_row(
    rows: list[list[dict[str, Any]]],
    *,
    name: str,
    table_number: int,
    table_meta: Mapping[str, Any],
) -> dict[str, Any]:
    target = normalize_whitespace(name).casefold()
    matches: list[list[str]] = []
    for cells in rows:
        normalized = _canonical_cells(cells)
        if normalized and normalized[0].casefold() == target:
            matches.append(normalized)
    if len(matches) != 1:
        raise ValueError(
            f"GACC table {table_number} row identity {name!r} matched {len(matches)} rows"
        )

    cells = matches[0]
    return {
        "contract": ROW_EVIDENCE_CONTRACT,
        "source_id": "CN_CUSTOMS",
        "table_number": table_number,
        "source_url": table_meta["url"],
        "source_payload_sha256": table_meta["payload_sha256"],
        "row_identity": cells[0],
        "row_cells": cells,
        "row_text": " | ".join(cells),
        "row_sha256": _row_sha256(cells),
        "parser_contract": (
            "GACC_TABLE_8_IMPORTER_EXPORTER_LOCATION_V1"
            if table_number == 8
            else "GACC_TABLE_11_SPECIFIC_AREA_V1"
        ),
    }


def _attach_row(
    row: dict[str, Any] | None,
    *,
    rows: list[list[dict[str, Any]]],
    table_number: int,
    table_meta: Mapping[str, Any],
) -> None:
    if row is None:
        return
    name = row.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("GACC serialized trade row is missing a stable name")
    row["source_row_evidence"] = _find_exact_row(
        rows,
        name=name,
        table_number=table_number,
        table_meta=table_meta,
    )


def enrich_gacc_trade_row_evidence(payload: Mapping[str, Any], *, client: Any) -> dict[str, Any]:
    """Return a copy of a GACC payload with stable row-level source evidence."""

    if payload.get("source_id") != "CN_CUSTOMS":
        raise ValueError("row evidence enrichment requires CN_CUSTOMS payload")
    if payload.get("transport_security") != "PLAINTEXT_HTTP":
        raise ValueError("unexpected GACC transport security state")
    if payload.get("corroboration_required") is not True:
        raise ValueError("GACC row evidence must preserve corroboration requirement")

    result = copy.deepcopy(dict(payload))
    table8_provenance = result.get("table_8_provenance")
    table11_provenance = result.get("table_11_provenance")
    if not isinstance(table8_provenance, Mapping) or not isinstance(table11_provenance, Mapping):
        raise ValueError("GACC table provenance is incomplete")

    table8_rows, table8_meta = _stable_table_rows(
        client=client,
        provenance=table8_provenance,
        table_number=8,
    )
    table11_rows, table11_meta = _stable_table_rows(
        client=client,
        provenance=table11_provenance,
        table_number=11,
    )

    jiangsu = result.get("jiangsu_importer_exporter_location")
    xuzhou_location = result.get("xuzhou_importer_exporter_location")
    areas = result.get("xuzhou_specific_areas")
    if not isinstance(jiangsu, dict):
        raise ValueError("GACC Jiangsu row is missing")
    if xuzhou_location is not None and not isinstance(xuzhou_location, dict):
        raise ValueError("GACC Xuzhou location row must be an object or null")
    if not isinstance(areas, list):
        raise ValueError("GACC Xuzhou specific-area rows must be a list")
    if any(not isinstance(item, dict) for item in areas):
        raise ValueError("GACC Xuzhou specific-area row must be an object")

    _attach_row(
        jiangsu,
        rows=table8_rows,
        table_number=8,
        table_meta=table8_meta,
    )
    _attach_row(
        xuzhou_location,
        rows=table8_rows,
        table_number=8,
        table_meta=table8_meta,
    )
    for row in areas:
        _attach_row(
            row,
            rows=table11_rows,
            table_number=11,
            table_meta=table11_meta,
        )

    result["row_evidence_contract"] = ROW_EVIDENCE_CONTRACT
    result["row_evidence_complete"] = True
    boundaries = list(result.get("truth_boundaries") or [])
    for boundary in (
        "ROW_EVIDENCE_REQUIRES_STABLE_REFETCH",
        "WHOLE_PAGE_HASH_NE_ROW_LEVEL_LINEAGE",
        "CORROBORATION_GATE_NE_ROW_LEVEL_VALUE_CONFIRMATION",
        "DERIVED_TOTAL_NE_SOURCE_CELL",
    ):
        if boundary not in boundaries:
            boundaries.append(boundary)
    result["truth_boundaries"] = boundaries
    validate_gacc_trade_row_evidence(result)
    return result


def _validate_bound_row(
    row: Mapping[str, Any],
    *,
    provenance: Mapping[str, Any],
    table_number: int,
) -> None:
    name = row.get("name")
    evidence = row.get("source_row_evidence")
    if not isinstance(name, str) or not isinstance(evidence, Mapping):
        raise ValueError("GACC trade row lacks row-level evidence")
    if evidence.get("contract") != ROW_EVIDENCE_CONTRACT:
        raise ValueError("GACC trade row has unsupported row evidence contract")
    if evidence.get("source_id") != "CN_CUSTOMS" or evidence.get("table_number") != table_number:
        raise ValueError("GACC trade row evidence source/table identity mismatch")
    if evidence.get("source_url") != provenance.get("url"):
        raise ValueError("GACC trade row evidence URL mismatch")
    if evidence.get("source_payload_sha256") != provenance.get("payload_sha256"):
        raise ValueError("GACC trade row evidence payload hash mismatch")
    cells = evidence.get("row_cells")
    if not isinstance(cells, list) or not cells or any(not isinstance(x, str) for x in cells):
        raise ValueError("GACC trade row evidence cells are invalid")
    if normalize_whitespace(cells[0]).casefold() != normalize_whitespace(name).casefold():
        raise ValueError("GACC trade row evidence identity does not match parsed row")
    if evidence.get("row_text") != " | ".join(cells):
        raise ValueError("GACC trade row evidence text does not match cells")
    if evidence.get("row_sha256") != _row_sha256(cells):
        raise ValueError("GACC trade row evidence hash does not match cells")


def validate_gacc_trade_row_evidence(payload: Mapping[str, Any]) -> None:
    """Fail closed unless every serialized GACC row has exact row-level lineage."""

    if payload.get("row_evidence_contract") != ROW_EVIDENCE_CONTRACT:
        raise ValueError("GACC row evidence contract is missing")
    if payload.get("row_evidence_complete") is not True:
        raise ValueError("GACC row evidence is not marked complete")
    table8 = payload.get("table_8_provenance")
    table11 = payload.get("table_11_provenance")
    if not isinstance(table8, Mapping) or not isinstance(table11, Mapping):
        raise ValueError("GACC row evidence validation requires table provenance")

    jiangsu = payload.get("jiangsu_importer_exporter_location")
    if not isinstance(jiangsu, Mapping):
        raise ValueError("GACC Jiangsu row is missing")
    _validate_bound_row(jiangsu, provenance=table8, table_number=8)

    xuzhou_location = payload.get("xuzhou_importer_exporter_location")
    if xuzhou_location is not None:
        if not isinstance(xuzhou_location, Mapping):
            raise ValueError("GACC Xuzhou location row is invalid")
        _validate_bound_row(xuzhou_location, provenance=table8, table_number=8)

    areas = payload.get("xuzhou_specific_areas")
    if not isinstance(areas, list):
        raise ValueError("GACC Xuzhou specific-area rows are invalid")
    for row in areas:
        if not isinstance(row, Mapping):
            raise ValueError("GACC Xuzhou specific-area row is invalid")
        _validate_bound_row(row, provenance=table11, table_number=11)
