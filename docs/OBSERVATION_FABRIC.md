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

## Live production bridge

The first real production bridge consumes existing evidence artifacts instead of duplicating source collectors. Initial connected source families are:

```text
jiangsu-money-flow-live
→ official Jiangsu macro release metrics
→ CHANGE / STATE observations

regional-data-live
→ recent Xuzhou government procurement notices
→ STATE / FLOW / TIME / CONSTRAINT observations

resource-underuse-live
→ Xuzhou public and officially-discovered linked asset listings
→ RESOURCE / STATE / CHANGE observations
```

These are observation inputs only. Their live adapters preserve the source's existing truth boundaries:

```text
DECLARED PROCUREMENT BUDGET != PAYMENT
PROCUREMENT NOTICE != PAID NEED
PUBLIC LISTING != CONTROL
PUBLIC LISTING != CURRENT AVAILABILITY
PUBLISHER != OWNER
RELISTING != UNDERUSE
OBSERVED UNDERUSE REQUIRES EXPLICIT SOURCE TEXT
OBSERVATION != OPPORTUNITY
UNKNOWN != PASS
```

The Jiangsu macro adapter remains Actor-less because aggregate statistics do not identify an individual Actor. Xuzhou procurement remains Actor-less when the upstream collector has not extracted an explicit buyer identity. Asset owner Actors are source-scoped and created only from an explicit `owner_actor`; a publisher is never silently substituted for the owner.

## Cross-run durable state

`observation-fabric-live` restores the SQLite database from the latest successful prior live artifact before ingesting current upstream artifacts. If a prior successful live run exists but its durable artifact cannot be restored, the workflow fails rather than silently creating an empty replacement history. Only the first successful production run may bootstrap an empty store.

The live state artifact contains:

```text
observation_fabric_live.sqlite
observation_fabric_live_assessment.json
observation_fabric_current.jsonl
live_observation_upstream_manifest.json
```

The upstream manifest records the exact successful source runs used for that build. Artifact-chain persistence is an operational durability mechanism, not business truth.

A scheduled collector often re-fetches an unchanged source record. A later retrieval timestamp alone is not new evidence. If normalized source content and parser version are unchanged, the live pipeline reports `UNCHANGED_SOURCE_CONTENT` and does not inflate observation history. A changed source record or parser version may create a revision, preserving both old and new evidence.

Production validation must fail if durable current/history counts shrink after a prior state is restored, if SQLite integrity fails, if required source families disappear, or if ingress creates downstream payer/payment/availability/permission/route/opportunity truth.
