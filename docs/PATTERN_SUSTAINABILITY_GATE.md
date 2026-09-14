# Pattern Sustainability Gate

Status: `DISCOVERY / STRATEGIC GUARD`

Parents:
- `docs/LATENT_VALUE_DOCTRINE.md`
- `docs/DISCOVERY_ENGINE.md`
- `docs/RESOURCE_ORCHESTRATION_KERNEL.md`
- `docs/OBSERVED_PATTERN_LAYER.md`

## Purpose

The engine now has production evidence that some semantic structures recur. That is necessary but still far below a sustainable business system.

This gate exists to enforce:

```text
OBSERVED_PATTERN
!=
OPPORTUNITY_ARCHETYPE
!=
REGENERATIVE_LOOP
!=
CORE BUSINESS
```

Its job is to state exactly what recurrence proves, what it does not prove, and which evidence must be collected next.

## Five sustainability axes

Every recurring structure is evaluated against the user's strategic requirements:

```text
1. RECURRENCE
2. POPULATION
3. STANDARDIZABILITY
4. REPEAT_MONETIZATION
5. COMPOUNDING
```

A separate gate asks whether there is a concrete mechanism that naturally regenerates new events without fresh founder-led hunting.

### `RECURRENCE`

May be `EVIDENCED` from an `OBSERVED_PATTERN` because the source pattern already passed direct-observation and time-persistence gates.

This proves repeated observation only.

```text
RECURRENCE != DEMAND PUMP
```

### `POPULATION`

May be `EVIDENCED` from an `OBSERVED_PATTERN` because the source pattern already passed its distinct-Actor gate.

This proves multi-Actor occurrence inside the observed universe only.

```text
MULTI_ACTOR != POPULATION PREVALENCE
```

### `STANDARDIZABILITY`

Remains `UNKNOWN` until multiple independent cases show that the same bounded transformation, interface, acceptance rule or CapabilityUnit template can repeatedly change the state.

```text
REPEATED PROBLEM != STANDARDIZABLE SOLUTION
```

### `REPEAT_MONETIZATION`

Remains `UNKNOWN` until repeated accepted economic settlement is evidenced for the same underlying transformation/route, with payer and scope preserved.

```text
BUDGET != SETTLEMENT
LISTING PRICE != SETTLEMENT
ONE PAYMENT != REPEAT MONETIZATION
```

### `COMPOUNDING`

Remains `UNKNOWN` until outcome-linked evidence shows that prior data, templates, trust, routing or rules measurably improve later execution or reduce search/coordination/QA/failure cost.

```text
MORE STORED DATA != COMPOUNDING
```

## Regenerating event flow

Time persistence is not enough. The system must eventually identify a lifecycle, installed base, recurring workflow, channel, Actor behavior or other mechanism that naturally emits new task/order/resource events.

```text
REPEATED HISTORICAL EVENTS
!=
PROVEN REGENERATING EVENT SOURCE
```

A route that requires unrelated founder-led customer hunting for every event does not pass this gate.

## Complementary Actor structure

A recurring structure is not yet an exchange. The engine still needs evidence about which complementary Actor class receives concrete incremental surplus and why the exchange is not already happening efficiently.

```text
PATTERN != COMPLEMENTARITY
COMPLEMENTARITY != TRANSACTIONABILITY
```

## Current state

This first implementation is deliberately one-way:

```text
OBSERVED_PATTERN
→ PATTERN_ONLY
→ explicit sustainability evidence gaps
```

There is **no automatic promotion path** from this module to `ARCHETYPE_CANDIDATE` or `REGENERATIVE_LOOP_CANDIDATE`.

Later modules may join independently evidenced transformation, settlement and outcome records. They must not infer those facts from recurrence.

## Validation tasks

Each pattern receives the following explicit validation tasks:

1. `ESTABLISH_REUSABLE_TRANSFORMATION_MECHANISM`
2. `ESTABLISH_COMPLEMENTARY_ACTOR_STRUCTURE`
3. `ESTABLISH_REGENERATING_EVENT_FLOW`
4. `ESTABLISH_REPEAT_MONETIZATION`
5. `ESTABLISH_COMPOUNDING_MECHANISM`

Every task records both:
- evidence required;
- a falsifier / kill condition.

This keeps research falsifiable rather than turning missing evidence into narrative confidence.

## Production chain

```text
observation-fabric-live
→ observed-pattern-live
→ pattern-sustainability-live
```

The production validator requires every `OBSERVED_PATTERN` to receive a sustainability assessment and hard-locks:

```text
core_business_state = PATTERN_ONLY
business_promotion = NOT_PROMOTED
```

until later independent evidence paths exist.

## Governing invariant

> **重复发生只证明“这件事反复发生”；可持续商业必须另外证明同一机制可复用、同类 Actor 足够多、能够反复结算、事件会自然再生，而且每次交付都会让下一次更便宜、更快、更可靠。任何一项缺证据，都保持 UNKNOWN。**
