"""Persistence for the time-aware live signal ledger.

The in-memory ledger models semantic change. This module makes that state survive
process restarts without turning absence, staleness or storage artifacts into new
world-state evidence.
"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Mapping, Sequence

from src.live_signal_ledger import SignalLedger, SignalLedgerEntry


SCHEMA_VERSION = 1


def _parse_aware_datetime(name: str, value: object) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty ISO datetime")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a valid ISO datetime") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{name} must be timezone-aware")
    return parsed


def entry_to_record(entry: SignalLedgerEntry) -> dict[str, object]:
    return {
        "source_id": entry.source_id,
        "signal_id": entry.signal_id,
        "actor_ref": entry.actor_ref,
        "first_seen_at": entry.first_seen_at.isoformat(),
        "last_seen_at": entry.last_seen_at.isoformat(),
        "seen_count": entry.seen_count,
        "revision_count": entry.revision_count,
        "current_fingerprint": entry.current_fingerprint,
        "current_payload": dict(entry.current_payload),
        "previous_fingerprints": list(entry.previous_fingerprints),
    }


def entry_from_record(record: Mapping[str, object]) -> SignalLedgerEntry:
    def required_text(name: str) -> str:
        value = record.get(name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be non-empty")
        return value.strip()

    first_seen_at = _parse_aware_datetime("first_seen_at", record.get("first_seen_at"))
    last_seen_at = _parse_aware_datetime("last_seen_at", record.get("last_seen_at"))
    if last_seen_at < first_seen_at:
        raise ValueError("last_seen_at must not precede first_seen_at")

    seen_count = record.get("seen_count")
    revision_count = record.get("revision_count")
    if not isinstance(seen_count, int) or isinstance(seen_count, bool) or seen_count < 1:
        raise ValueError("seen_count must be a positive integer")
    if not isinstance(revision_count, int) or isinstance(revision_count, bool) or revision_count < 0:
        raise ValueError("revision_count must be a non-negative integer")
    if revision_count > seen_count - 1:
        raise ValueError("revision_count cannot exceed seen_count - 1")

    payload = record.get("current_payload")
    if not isinstance(payload, Mapping):
        raise ValueError("current_payload must be an object")

    previous = record.get("previous_fingerprints", [])
    if not isinstance(previous, Sequence) or isinstance(previous, (str, bytes)):
        raise ValueError("previous_fingerprints must be an array")
    previous_fingerprints = tuple(str(item).strip() for item in previous)
    if any(not item for item in previous_fingerprints):
        raise ValueError("previous_fingerprints cannot contain empty values")

    return SignalLedgerEntry(
        source_id=required_text("source_id"),
        signal_id=required_text("signal_id"),
        actor_ref=required_text("actor_ref"),
        first_seen_at=first_seen_at,
        last_seen_at=last_seen_at,
        seen_count=seen_count,
        revision_count=revision_count,
        current_fingerprint=required_text("current_fingerprint"),
        current_payload=dict(payload),
        previous_fingerprints=previous_fingerprints,
    )


class JsonSignalLedgerStore:
    """Atomic JSON persistence for deterministic ledger state.

    Storage is intentionally boring: one versioned document, fail-closed parsing and
    atomic replacement. A broken file never becomes an empty ledger silently.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> SignalLedger:
        ledger = SignalLedger()
        if not self.path.exists():
            return ledger

        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot read signal ledger: {self.path}") from exc

        if not isinstance(raw, Mapping):
            raise ValueError("signal ledger root must be an object")
        if raw.get("schema_version") != SCHEMA_VERSION:
            raise ValueError("unsupported signal ledger schema_version")
        records = raw.get("entries")
        if not isinstance(records, list):
            raise ValueError("signal ledger entries must be an array")

        for record in records:
            if not isinstance(record, Mapping):
                raise ValueError("signal ledger entry must be an object")
            ledger.restore_entry(entry_from_record(record))
        return ledger

    def save(self, ledger: SignalLedger) -> None:
        payload = {
            "schema_version": SCHEMA_VERSION,
            "entries": [entry_to_record(entry) for entry in ledger.entries()],
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"

        fd, tmp_name = tempfile.mkstemp(
            prefix=f".{self.path.name}.",
            suffix=".tmp",
            dir=str(self.path.parent),
            text=True,
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, self.path)
        except Exception:
            try:
                os.unlink(tmp_name)
            except FileNotFoundError:
                pass
            raise


GOVERNING_INVARIANTS = (
    "PROCESS_RESTART_NE_WORLD_RESET",
    "PERSISTED_STATE_NE_NEW_EVIDENCE",
    "CORRUPT_STORAGE_NE_EMPTY_WORLD",
    "ABSENCE_FROM_STORAGE_REFRESH_NE_RESOURCE_DISAPPEARED",
    "SCHEMA_MISMATCH_FAILS_CLOSED",
    "UNKNOWN_NE_PASS",
)
