"""Time-aware ledger for live resource signals.

The ledger models repeated observations and semantic state changes. It deliberately
separates "stale/not recently observed" from "removed/disappeared": absence is not a
fact unless a source-specific complete snapshot contract proves it.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Mapping, Sequence

from src.live_resource_signals import SignalObservation


class TransitionKind(str, Enum):
    FIRST_SEEN = "FIRST_SEEN"
    REOBSERVED = "REOBSERVED"
    CHANGED = "CHANGED"
    OUT_OF_ORDER = "OUT_OF_ORDER"


@dataclass(frozen=True)
class SignalTransition:
    source_id: str
    signal_id: str
    kind: TransitionKind
    observed_at: datetime
    changed_dimensions: tuple[str, ...] = ()


@dataclass(frozen=True)
class SignalLedgerEntry:
    source_id: str
    signal_id: str
    actor_ref: str
    first_seen_at: datetime
    last_seen_at: datetime
    seen_count: int
    revision_count: int
    current_fingerprint: str
    current_payload: Mapping[str, object]
    previous_fingerprints: Sequence[str] = field(default_factory=tuple)

    def is_stale(self, as_of: datetime, max_age: timedelta) -> bool:
        if as_of.tzinfo is None:
            raise ValueError("as_of must be timezone-aware")
        if self.last_seen_at.tzinfo is None:
            return True
        age = as_of - self.last_seen_at
        return age > max_age


def _stable_value(value: object) -> object:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return {str(k): _stable_value(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, (list, tuple, set, frozenset)):
        normalized = [_stable_value(v) for v in value]
        if isinstance(value, (set, frozenset)):
            normalized = sorted(normalized, key=repr)
        return normalized
    return repr(value)


def semantic_payload(signal: SignalObservation) -> dict[str, object]:
    """Return only normalized world-state semantics, excluding page/text cosmetics."""

    facts = sorted(
        (
            {"key": fact.key.strip(), "value": _stable_value(fact.value)}
            for fact in signal.facts
            if fact.is_usable()
        ),
        key=lambda item: (str(item["key"]), repr(item["value"])),
    )
    capabilities = sorted(
        capability.capability_key.strip()
        for capability in signal.explicit_capabilities
        if capability.is_usable()
    )
    return {
        "actor_ref": signal.actor_ref.strip(),
        "geography": signal.geography.strip(),
        "facts": facts,
        "explicit_capabilities": capabilities,
        "availability": signal.availability.value,
        "permission": signal.permission.value,
    }


def semantic_fingerprint(signal: SignalObservation) -> str:
    raw = json.dumps(semantic_payload(signal), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _changed_dimensions(before: Mapping[str, object], after: Mapping[str, object]) -> tuple[str, ...]:
    keys = sorted(set(before) | set(after))
    return tuple(key for key in keys if before.get(key) != after.get(key))


def observe_signal(
    existing: SignalLedgerEntry | None,
    signal: SignalObservation,
) -> tuple[SignalLedgerEntry, SignalTransition]:
    """Apply one observation monotonically and emit an auditable transition."""

    errors = signal.validate()
    if errors:
        raise ValueError("invalid signal: " + ",".join(errors))

    payload = semantic_payload(signal)
    fingerprint = semantic_fingerprint(signal)

    if existing is None:
        entry = SignalLedgerEntry(
            source_id=signal.source_id,
            signal_id=signal.signal_id,
            actor_ref=signal.actor_ref,
            first_seen_at=signal.observed_at,
            last_seen_at=signal.observed_at,
            seen_count=1,
            revision_count=0,
            current_fingerprint=fingerprint,
            current_payload=payload,
        )
        return entry, SignalTransition(signal.source_id, signal.signal_id, TransitionKind.FIRST_SEEN, signal.observed_at)

    if existing.source_id != signal.source_id or existing.signal_id != signal.signal_id:
        raise ValueError("signal identity mismatch")
    if existing.actor_ref != signal.actor_ref:
        raise ValueError("actor identity changed for stable signal id")

    if signal.observed_at < existing.last_seen_at:
        return existing, SignalTransition(
            signal.source_id,
            signal.signal_id,
            TransitionKind.OUT_OF_ORDER,
            signal.observed_at,
        )

    if fingerprint == existing.current_fingerprint:
        entry = SignalLedgerEntry(
            **{**existing.__dict__, "last_seen_at": signal.observed_at, "seen_count": existing.seen_count + 1}
        )
        return entry, SignalTransition(signal.source_id, signal.signal_id, TransitionKind.REOBSERVED, signal.observed_at)

    changed = _changed_dimensions(existing.current_payload, payload)
    entry = SignalLedgerEntry(
        source_id=existing.source_id,
        signal_id=existing.signal_id,
        actor_ref=existing.actor_ref,
        first_seen_at=existing.first_seen_at,
        last_seen_at=signal.observed_at,
        seen_count=existing.seen_count + 1,
        revision_count=existing.revision_count + 1,
        current_fingerprint=fingerprint,
        current_payload=payload,
        previous_fingerprints=tuple(existing.previous_fingerprints) + (existing.current_fingerprint,),
    )
    return entry, SignalTransition(
        signal.source_id,
        signal.signal_id,
        TransitionKind.CHANGED,
        signal.observed_at,
        changed,
    )


class SignalLedger:
    """Small deterministic in-memory ledger; persistence adapters may sit below it."""

    def __init__(self) -> None:
        self._entries: dict[tuple[str, str], SignalLedgerEntry] = {}

    def ingest(self, signal: SignalObservation) -> SignalTransition:
        key = (signal.source_id, signal.signal_id)
        entry, transition = observe_signal(self._entries.get(key), signal)
        self._entries[key] = entry
        return transition

    def get(self, source_id: str, signal_id: str) -> SignalLedgerEntry | None:
        return self._entries.get((source_id, signal_id))

    def stale_entries(self, as_of: datetime, max_age: timedelta) -> tuple[SignalLedgerEntry, ...]:
        return tuple(entry for entry in self._entries.values() if entry.is_stale(as_of, max_age))


GOVERNING_INVARIANTS = (
    "TIME_IS_FIRST_CLASS",
    "RAW_TEXT_CHANGE_NE_WORLD_STATE_CHANGE",
    "REOBSERVED_NE_CHANGED",
    "NOT_RECENTLY_SEEN_NE_DISAPPEARED",
    "OUT_OF_ORDER_OBSERVATION_MUST_NOT_ROLL_BACK_STATE",
    "UNKNOWN_NE_PASS",
)
