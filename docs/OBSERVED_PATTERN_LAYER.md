# Observed Pattern Layer

Status: `IMPLEMENTATION OF CANONICAL DISCOVERY STATE`

Parents:
- `docs/LATENT_VALUE_DOCTRINE.md`
- `docs/DISCOVERY_ENGINE.md`
- `docs/OBSERVATION_FABRIC.md`

## Purpose

This layer implements the existing canonical discovery transition:

```text
OBSERVATIONS / PROVENANCE
→ exact repeated semantic structure
→ OBSERVED_PATTERN
→ only later: LATENT_VALUE_HYPOTHESIS
```

It answers a deliberately narrow question:

> **Which directly observed semantic structures recur across current source identities, actors and time?**

It does **not** answer whether the structure is valuable, monetizable, an opportunity, a Demand Pump, or a regenerative business system.

## Exact grouping

Pattern identity is exact:

```text
semantic primitive
+ concept
+ geography
```

There is no LLM similarity merge and no synonym promotion in this layer. Two concepts that look similar remain separate unless a different, evidence-governed taxonomy process explicitly reconciles them.

## Current identity rule

Pattern recurrence is computed from the current version of each Observation Fabric identity.

```text
SOURCE_ID + OBSERVATION_ID
```

Historical revisions, out-of-order captures and repeated re-fetches are retained in the durable Observation Fabric for provenance, but they do not count as additional recurrence events here.

This prevents collector activity from masquerading as world recurrence.

## Epistemic rule

Only semantic claims with:

```text
OBSERVED
```

may satisfy the pattern gate.

`REPORTED` and `INFERRED` claims may remain visible in diagnostics but cannot bootstrap a pattern into `OBSERVED_PATTERN`.

## Operational evidence gate

The initial production gate is:

```text
min_observations = 3
min_actors       = 2
min_periods      = 2 independent calendar dates
min_sources      = 1
```

These are operational evidence thresholds, not universal laws and not commercial-truth thresholds. The exact thresholds are emitted in every artifact.

Source diversity is always disclosed. A single lawful official source may observe multiple actors over time, so `min_sources=1` is permitted for pattern existence; a single-source pattern is explicitly marked `SINGLE_SOURCE_ONLY` and may need corroboration downstream.

## States

```text
UNBOUND
OBSERVED_PATTERN
```

`UNBOUND` means the exact semantic group exists but lacks one or more recurrence gates.

`OBSERVED_PATTERN` means only that recurrence, actor diversity, time persistence and configured source requirements are satisfied.

## Hard boundaries

```text
PATTERN != LATENT VALUE
PATTERN != NEED
PATTERN != PAID NEED
PATTERN != PAYER
PATTERN != AVAILABLE RESOURCE
PATTERN != OPPORTUNITY
PATTERN != DEMAND PUMP
PATTERN != REGENERATIVE LOOP
PATTERN != CORE BUSINESS
```

Every pattern record therefore remains:

```text
business_promotion = NOT_PROMOTED
```

and explicitly preserves downstream unknowns for latent value, complementary actors, transformation mechanism, regenerating event flow, payer, repeat monetization and compounding.

## Production flow

```text
observation-fabric-live
→ durable current ObservationEnvelope identities
→ exact pattern grouping
→ evidence gate
→ observed-pattern-live-state artifact
```

The production validator reopens the source SQLite store and verifies that every support reference is current and every supporting claim is directly `OBSERVED`.

## Strategic use

Observed patterns become inputs to later discovery work. The next layer may ask:

- what hidden or underrecognized value may exist behind this repeated structure?
- why is that value not already realized?
- which complementary actor state could unlock it?
- what reusable transformation mechanism could change the state?
- what naturally regenerates new events?
- what evidence would falsify the hypothesis?

Those questions belong to `LATENT_VALUE_HYPOTHESIS` / archetype testing. They must not be answered by this layer merely because recurrence is visible.

## Governing invariant

> **Count repeated reality, not repeated collection; detect structure before inventing meaning; promote a pattern only on direct evidence, and leave commercial interpretation downstream.**
