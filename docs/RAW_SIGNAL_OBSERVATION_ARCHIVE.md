# Raw Signal Observation Archive

Status: `EVIDENCE INFRASTRUCTURE / APPEND-ONLY`

The live sensing system must preserve **what was observed** separately from **what the current algorithm concluded**.

## Why this exists

Inference rules, capability abstractions and composition logic will change over time.

If the system persists only derived states such as `CapabilityClaim` or current semantic fingerprints, a later rule improvement cannot safely answer:

> What would the new rule have concluded from the evidence we actually saw last month?

Therefore every durable live-sensing ingestion now has three distinct storage layers:

```text
RAW / REVIEWED SIGNAL OBSERVATION
        ↓
SEMANTIC TRANSITION HISTORY
        ↓
CURRENT SEMANTIC STATE
```

The first layer is evidence. The latter two are interpretations/state projections.

## Archived observation content

For each ingested `SignalObservation`, preserve where present:
- `source_id` / `signal_id`;
- `observed_at`;
- `actor_ref`;
- geography;
- raw text;
- source URL;
- observed facts including evidence text;
- explicit capability claims including evidence text;
- observed availability state;
- observed permission state.

The archive is append-only and queryable in ingestion order.

## Replay purpose

Future capability materialization should be able to run:

```text
ARCHIVED OBSERVATIONS
+
SELECTED / ACTIVE RULE VERSIONS
→ RE-DERIVED CAPABILITY CLAIMS
```

without modifying the archived observations.

This lets the system learn from rule changes while retaining provenance and falsifiability.

## Intake boundary

Reviewed/manual/source-neutral JSON intake is **not** a confirmation mechanism.

It may preserve:
- `UNKNOWN` availability;
- an explicitly observed public `ADVERTISED` availability signal.

It may not manufacture:
- `CONFIRMED` availability;
- `COMMITTED` availability;
- `ALLOWED` permission / operator control.

Those stronger states require a separate confirmation/authorization path with its own evidence.

## Hard boundaries

```text
RAW OBSERVATION != DERIVED CAPABILITY
RAW OBSERVATION != CURRENT WORLD STATE
INPUT JSON != CONFIRMED TRUTH
PUBLIC ADVERTISEMENT != CURRENT COMMITMENT
PUBLIC OBSERVATION != OPERATOR PERMISSION
RULE CHANGE != HISTORY REWRITE
REPLAYED INFERENCE != NEW OBSERVATION
UNKNOWN != PASS
```

## Implementation

`src/live_signal_store.py` stores:
- `signal_observation` — append-only original observation payloads for audit/replay;
- `signal_transition` — append-only semantic transitions;
- `signal_current` — current semantic state.

`src/live_signal_intake.py` is the canonical structured intake parser.
`src/structured_signal_import.py` delegates to that parser so separate import paths cannot drift into different truth semantics.
