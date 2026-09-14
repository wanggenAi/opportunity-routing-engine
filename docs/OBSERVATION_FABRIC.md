# Observation Fabric

Status: `CANONICAL / LOCKED OBSERVATION TRUTH`

Effective: 2026-09-14

## Dependency direction

```text
SENSOR
→ RAW ITEM
→ OBSERVATION ENVELOPE
→ SEMANTIC CLAIMS
→ INTERPRETATION / CORROBORATION
→ RESIDUAL / EMERGENT TAXONOMY
→ WORLD MODEL
→ FRICTION / RESOURCE / CHANGE
→ OPPORTUNITY HYPOTHESIS
→ COMMERCIAL EVIDENCE GATES
→ ROUTING / EXECUTION
```

Never collapse this to `SOURCE → BUSINESS IDEA` or force all world evidence into the legacy resource `SignalObservation` model.

## ObservationEnvelope

An envelope records what one source supports at a bounded time/scope. It preserves source identity, source-record identity, locator, origin/relevance geography, source tier, publication/observation/retrieval time, parser version, raw payload fingerprint, schema version, sampling boundary, evidence, zero or more Actors, N semantic claims, explicit unknowns, contradictions and revision lineage.

Aggregate observations may legitimately have no Actor. Do not invent one for downstream convenience.

Each claim maps to one stable Semantic Kernel primitive. `concept` stays open-ended. Epistemic state is explicit: `OBSERVED`, `REPORTED`, or `INFERRED`.

```text
SOURCE CLAIM != WORLD FACT
SOCIAL SALIENCE != POPULATION PREVALENCE
REPORTED MOTIVE != OBSERVED MOTIVE
INFERRED FRICTION != CONFIRMED FRICTION
OBSERVATION != DEMAND
OBSERVATION != PAYER
OBSERVATION != OPPORTUNITY
CONFIDENCE != TRUTH PROMOTION
MISSING != ZERO
UNKNOWN != FALSE
NO EVIDENCE != NEGATIVE EVIDENCE
```

A source revision appends history; it does not silently overwrite old evidence.

## Actor autonomy

The system optimizes information quality, matching quality, friction reduction, transaction feasibility, risk transparency, voluntary choice and real outcomes. It does not treat compliance with the system as value.

Canonical invariants:

```text
ACTOR_AUTONOMY
NO_COERCIVE_ROUTING
NO_MORAL_PERSONALITY_SCORING
OBSERVATION_NE_JUDGMENT
RECOMMENDATION_NE_CONSENT
VALUE_FROM_FRICTION_REDUCTION
NO_ARTIFICIAL_DEPENDENCY
```

System recommendation is not consent. Interest is not commitment. A discovered provider has not agreed to transact. Buyer friction does not mean the buyer accepts our solution. Actor rejection is valid evidence, not an error condition. A stable direct relationship that bypasses the orchestrator is not automatically a bad outcome. The orchestrator must earn value by reducing real friction rather than manufacturing switching or exit cost.

## Future sources

A future platform must be able to join the Sensor Registry and emit ObservationEnvelope records using existing primitives and previously unseen concepts without modifying the Semantic Kernel. New concepts remain residual/unbound until evidence diversity and persistence justify review.

`NEW PLATFORM != NEW WORLD MODEL`.

Domestic-origin observations are China-primary. Foreign/global observations remain global-auxiliary and cannot become Chinese domestic facts without domestic corroboration.

## Durable store

The first implementation uses SQLite. It must provide deterministic ingestion, idempotency, append history, revision/out-of-order protection, provenance retention, and query by source, Actor, primitive, concept, time and geography. SQLite is storage, not ontology.

## Compatibility boundary

```text
RAW SOURCE
→ OBSERVATION FABRIC
→ SEMANTIC CLAIMS
→ WORLD MODEL / TAXONOMY
→ specific downstream projections
```

The legacy resource bridge is one-way and conservative. Only `OBSERVED` claims may project into legacy observed facts/capabilities. `REPORTED` or `INFERRED` claims are never upgraded. The Observation Fabric never creates confirmed availability, permission, payer, paid need, underuse or opportunity truth.

## Production smoke

Architecture fixtures may prove heterogeneous normalization, storage and taxonomy flow, but must be labelled fixture-only and never represented as real-world evidence. Smoke artifacts may report observation/source/Actor counts, primitive coverage, residual concepts, epistemic counts, unknowns, contradictions, geography lanes, provenance completeness and schema versions. They must not manufacture opportunity counts.
