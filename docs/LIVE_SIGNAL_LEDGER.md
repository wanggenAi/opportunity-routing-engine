# Live Signal Ledger — Time and State-Change Semantics

Status: `CANONICAL LIVE-SENSING SUPPORT`

Effective: 2026-09-13

Parent: `docs/LIVE_RESOURCE_SENSING.md`.

## Purpose

A live resource sensor is useful only if the engine can distinguish a new state from a repeated observation, a cosmetic page change, stale evidence and a true semantic change.

The ledger therefore models **observed time and state transitions**, not merely the latest scraped record.

## Identity

A source adapter must provide a stable pair:

```text
(source_id, signal_id)
```

A stable signal id cannot silently change actor identity. If a source reuses identifiers for different actors/items, the adapter must create a source-specific identity strategy rather than letting the ledger merge them.

## Canonical transitions

```text
FIRST_SEEN
REOBSERVED
CHANGED
OUT_OF_ORDER
```

- `FIRST_SEEN`: no prior record exists for this stable signal identity.
- `REOBSERVED`: the normalized world-state semantics are unchanged; only observation time/seen count advances.
- `CHANGED`: at least one normalized semantic dimension changed.
- `OUT_OF_ORDER`: an older observation arrived after a newer one; it must not roll current state backward.

## Semantic fingerprint

The ledger fingerprints normalized semantics rather than raw page text.

Current semantic dimensions include:
- actor identity;
- geography;
- normalized observed facts;
- explicit capability claims;
- availability state;
- permission state.

Cosmetic wording/HTML changes are not world-state changes by themselves.

```text
RAW_TEXT_CHANGE != WORLD_STATE_CHANGE
```

## Time semantics

Each ledger entry keeps:
- first seen time;
- last seen time;
- seen count;
- revision count;
- current semantic fingerprint;
- previous fingerprints.

A freshness policy may mark an entry stale for current reasoning.

But:

```text
STALE != DISAPPEARED
NOT_RECENTLY_SEEN != REMOVED
```

The engine may declare disappearance/removal only when a source adapter can prove a complete-snapshot/removal contract for that source. Ordinary search/list absence is not sufficient.

## Why this matters

The commercially useful signal is often a transition:
- availability changes from advertised to confirmed;
- an asset is repriced;
- a capability is newly advertised;
- a location changes;
- a constraint appears;
- the same behavior repeats over time.

These transitions may later support actor-state/change and latent-value hypotheses. They do not themselves prove paid demand, resource control or transactionability.

## Implementation

- `src/live_signal_ledger.py`
  - deterministic semantic payload/fingerprint;
  - monotonic observation handling;
  - transition emission;
  - staleness detection;
  - in-memory ledger contract.
- `tests/test_live_signal_ledger.py`
  - first seen/reobservation;
  - cosmetic text changes;
  - semantic availability changes;
  - out-of-order protection;
  - staleness boundary;
  - stable identity guard.

The in-memory implementation defines semantics. A durable SQLite/JSONL adapter may be added below this contract without changing discovery ontology.

## Next engineering layer

The next useful implementation is durable storage + replay, followed by one lawful sensor adapter.

Correct order:

```text
NEUTRAL SIGNAL CONTRACT
-> TIME/STATE LEDGER
-> DURABLE STORAGE + REPLAY
-> AUDITABLE CAPABILITY RULE REGISTRY
-> ONE LAWFUL LIVE SENSOR
-> MEASURE SIGNAL/RULE USEFULNESS
-> EXPAND SENSOR BREADTH
```

Do not build many brittle platform scrapers before the ledger and truth boundaries can preserve what those scrapers observe.

## Invariants

```text
TIME_IS_FIRST_CLASS
RAW_TEXT_CHANGE != WORLD_STATE_CHANGE
REOBSERVED != CHANGED
NOT_RECENTLY_SEEN != DISAPPEARED
OUT_OF_ORDER_OBSERVATION_MUST_NOT_ROLL_BACK_STATE
SOURCE ABSENCE != REMOVAL WITHOUT COMPLETE-SNAPSHOT PROOF
UNKNOWN != PASS
```
