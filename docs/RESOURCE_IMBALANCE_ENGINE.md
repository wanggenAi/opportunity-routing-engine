# Resource Imbalance Engine

Status: `CANONICAL DISCOVERY COMPONENT / V1`

## Purpose

The Resource Imbalance Engine converts the Resource Activation Thesis into an evidence-gated discovery layer.

It does **not** ask only:

> Where is demand?

It asks three separate questions:

```text
WHERE IS A VERIFIED NEED / DEFICIT?
+
WHERE IS A VERIFIED RESOURCE / SURPLUS?
+
WHY ARE THEY NOT ALREADY TRANSACTING?
```

Only after all three sides have evidence may the system promote a pair into a bounded route test.

This layer exists specifically to prevent a common analytical error:

```text
paid demand observed
→ researcher imagines spare supply
→ researcher imagines a matching problem
→ labels it an opportunity
```

That chain is invalid.

`PAID NEED != RESOURCE IMBALANCE`.

## Canonical states

The engine emits four discovery states.

### `NEED_ONLY`

A need/deficit is observed, but no compatible resource signal exists yet.

Examples:
- a public institution is paying for maintenance;
- a merchant repeatedly hires temporary staff;
- households are paying high emergency-service prices;
- an enterprise repeatedly outsources data cleaning.

This is demand evidence only.

### `RESOURCE_ONLY`

A resource exists, but no compatible need signal exists yet.

Examples:
- a workshop reports idle machine hours;
- trained graduates have demonstrable spare capacity;
- a venue has measured unused weekday space;
- a delivery fleet has verified idle return legs.

This is resource evidence only.

### `PAIR_HYPOTHESIS`

Both sides are present, but at least one decisive route condition is still weak or unknown.

Typical missing conditions:
- need is observed but not paid;
- payer is unknown;
- resource exists but underuse is only claimed;
- resource is still hypothetical;
- transaction blocker is not observed;
- capability/geography identity is not clean enough.

A pair hypothesis is useful for research prioritization. It is **not** permission to claim a business opportunity.

### `ROUTE_TESTABLE`

V1 requires all of the following:

```text
need evidence >= PAID
payer identified
resource state >= DISCOVERED
resource underuse >= OBSERVED
transaction blocker >= OBSERVED
exact capability identity
exact geography identity
```

`ROUTE_TESTABLE` means only:

> There is enough evidence to justify a cheap, bounded real-world attempt to convert the mismatch into a transaction route.

It does **not** mean:
- the resource is controlled;
- the provider has accepted economics;
- a buyer will use the orchestrator;
- margins work;
- trust/legal/safety gates pass;
- the route repeats;
- the candidate passes G0-G6.

Those remain downstream validation questions.

## Need-side evidence

Canonical need evidence states:

```text
UNKNOWN
OBSERVED
PAID
REPEATED_PAID
```

`PAID` requires an identified payer and at least one real paid event.

`REPEATED_PAID` requires at least two paid events. Repeated public procurement can prove repeated institutional purchase of a task category, but does not by itself prove private-market demand or an available orchestration margin.

## Resource-side evidence

Resource control state remains canonical:

```text
HYPOTHETICAL
DISCOVERED
OPTIONED
OWNED
```

Underuse is a separate axis:

```text
UNKNOWN
CLAIMED
OBSERVED
MEASURED
```

This separation is mandatory because:

```text
resource exists != resource is spare
resource is spare != provider will supply it
provider will supply it != economics fit
```

Examples of stronger underuse evidence:
- measured idle machine hours;
- unused appointment slots from a real schedule;
- repeated empty venue periods;
- a provider's verified capacity/utilization records;
- a bounded sample showing trained people actively seeking additional paid utilization.

Self-reported `I have spare time` may be `CLAIMED`, not automatically `OBSERVED`.

### Provider capacity evidence — LOCKED

Historical awards, qualifications, tender participation and recent wins prove capability/activity only. They do not prove spare capacity.

Direct provider-capacity evidence uses the following bounded mapping:

```text
PROVIDER_STATED_SPARE_CAPACITY  -> CLAIMED
AUTHORIZED_CAPACITY_SCHEDULE    -> OBSERVED
VERIFIED_UNUSED_CAPACITY_RECORD -> OBSERVED
MEASURED_UTILIZATION_RECORD     -> MEASURED
```

`OBSERVED` or `MEASURED` additionally requires a concrete `available_units` description and an observation period. Examples include `2 crews available 2026-09-20 to 2026-09-24`, `3 unused service slots on the authorized schedule`, or a measured utilization record showing unused machine hours.

Provider-capacity evidence may only strengthen an already-canonical `ResourceSignal`. It must match all of:

```text
resource_signal_id
provider_actor
capability_key
geography
```

It cannot create a resource from scratch, cannot change `resource_state`, and cannot turn a statement of willingness into observed underuse. Evidence is ingested through the explicit provider-capacity evidence path; rejected identity/basis/state records remain non-promoting evidence.

Therefore:

```text
Historical Capability != Current Underuse
Active Bidding != Current Underuse
Recent Award != Current Underuse
Provider Statement != OBSERVED Underuse
```

## Blocker evidence

A resource mismatch needs an explanation for why normal market exchange has not already removed it.

Canonical blocker types remain:

1. `DEMAND_GAP`
2. `CAPABILITY_GAP`
3. `PRICE_GAP`
4. `TRUST_GAP`
5. `INFORMATION_GAP`
6. `GEOGRAPHY_GAP`
7. `TIME_GAP`
8. `COORDINATION_GAP`
9. `PAYER_SHIFT`
10. `TECHNOLOGY_SHIFT`

Blocker evidence states:

```text
UNKNOWN
CLAIMED
OBSERVED
MEASURED
```

Examples:
- buyers repeatedly say they cannot find providers with a required acceptance standard;
- providers report demand exists but acquisition cost destroys margins;
- work exists only in short bursts too small for a full-time hire;
- geographic deadhead time prevents normal providers from serving a route;
- trust/home-entry risk blocks an otherwise obvious service exchange.

## V1 matching rule

V1 requires exact:

```text
capability_key
+
geography
```

The engine intentionally does not infer that two labels are equivalent and does not silently route across geography.

Transaction-scoped blockers additionally require exact `need_signal_id` identity. A blocker from one bounded procurement/transaction cannot satisfy another Need merely because capability and geography match.

Later versions may add:
- explicit capability ontology;
- parent/child CapabilityUnits;
- travel radius;
- remote-delivery compatibility;
- substitution rules;
- quality tiers;
- temporal availability windows.

Those must be explicit models, not hidden assumptions.

## Public procurement interpretation

The Xuzhou procurement adapter can provide strong need-side evidence.

A procurement notice may establish:
- a named institutional task;
- an identified payer class;
- a budget or other monetary evidence;
- procurement method;
- timing/contract constraints;
- repeated occurrence when aggregated over time.

It does **not** establish:
- local private supply scarcity;
- idle resource availability;
- independent private demand;
- provider willingness;
- orchestration economics.

Therefore the code path `procurement_event_to_need(...)` creates only a `NeedSignal`.

It cannot create a `ResourceSignal` or `ROUTE_TESTABLE` record on its own.

## Resource discovery priority

After paid need-side feeds are working, the next highest-value sensing layer is **resource underuse**.

Priority sources should answer questions such as:
- Which skills are demonstrably available but under-utilized?
- Which service providers have empty slots or weak demand access?
- Which machines/vehicles/spaces have measured spare capacity?
- Which organizations hold distribution/trust/resources they are not fully monetizing?
- Which graduates/workers can demonstrate bounded CapabilityUnits but lack buyer access?

The system should prefer observable utilization/capacity evidence over broad claims such as `people are unemployed` or `shops are quiet`.

## Relationship to Opportunity Ranker

The layers are sequential:

```text
raw evidence
→ need/resource/blocker signals
→ Resource Imbalance Engine
→ NEED_ONLY / RESOURCE_ONLY / PAIR_HYPOTHESIS / ROUTE_TESTABLE
→ bounded transaction test
→ G0-G6 Opportunity Ranker
→ Hook / orchestration design
```

Resource imbalance is therefore an upstream candidate-generation gate, not a replacement for the commercial scorecard.

## Governing rule

> **先分别证明“缺什么”“谁有余”“为什么没成交”，再谈机会。任何一边靠想象补齐，都只能停留在 UNKNOWN。**
