"""Compatibility wrapper around the canonical reviewed signal intake."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from src.live_resource_signals import SignalObservation
from src.live_signal_intake import records_from_path, signal_from_record as _signal_from_record


def signal_from_record(record: Mapping[str, object]) -> SignalObservation:
    """Use the single canonical fail-closed intake parser."""

    return _signal_from_record(record)


def load_records(path: str | Path) -> tuple[Mapping[str, object], ...]:
    """Materialize canonical JSON/JSONL intake records for the import CLI."""

    return tuple(records_from_path(path))


GOVERNING_INVARIANTS = (
    "ONE_CANONICAL_STRUCTURED_INTAKE_SEMANTICS",
    "STRUCTURED_IMPORT_NE_CONFIRMATION",
    "STRUCTURED_IMPORT_NE_COMMITMENT",
    "UNKNOWN_NE_PASS",
)
