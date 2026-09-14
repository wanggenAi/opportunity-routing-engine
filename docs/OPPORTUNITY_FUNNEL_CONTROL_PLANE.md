# Opportunity Funnel Control Plane

## Purpose

The opportunity funnel is the operator-facing control plane between continuous discovery and bounded transaction testing.

It answers four questions from already-built canonical evidence:

1. How many live imbalance records exist in each canonical state?
2. Which `PAIR_HYPOTHESIS` records are closest to clearing their remaining evidence gates?
3. Which evidence-acquisition tasks and field packets already exist for those records?
4. Has any record actually reached `ROUTE_TESTABLE`, so the system should stop validating and run a bounded transaction test?

It does **not** replace the Resource Imbalance engine, validation queue, field validation packets, or opportunity scorecard.

## Truth boundary

The control plane is read-only over canonical truth.

It must never:

- promote `NEED_ONLY`, `RESOURCE_ONLY`, or `PAIR_HYPOTHESIS`;
- infer `PAID` from tender budgets, awards, contracts, or intent;
- infer current underuse from historical capability;
- invent a payer, blocker, resource, actor, or settlement;
- create a commercial-success probability or synthetic business score;
- declare a canonical #1 project merely because a pair has fewer missing gates.

Its ordering basis is explicitly:

`EVIDENCE_DISTANCE_ONLY_NOT_COMMERCIAL_RANKING`

That means a pair can be first in the validation focus because it is cheaper/closer to resolve while still being commercially inferior to another pair. Comparable commercial ranking remains downstream of sufficient evidence.

## Input lineage

The live control plane consumes only existing artifacts:

```text
xz_resource_imbalance_ledger.json
  + xz_pair_validation_queue.json
  + xz_field_validation_packets.json
  -> xz_opportunity_funnel.json
```

Canonical truth remains owned by `src/resource_imbalance.py` and the live ledger builder.

## Lanes

Each canonical record is projected into an operator lane:

| Canonical state | Operator lane | Default next action |
| --- | --- | --- |
| `NEED_ONLY` | `SUPPLY_DISCOVERY` | discover compatible resource |
| `RESOURCE_ONLY` | `DEMAND_DISCOVERY` | discover paid need |
| `PAIR_HYPOTHESIS` | `PAIR_VALIDATION` | execute the next canonical validation task |
| `ROUTE_TESTABLE` | `TRANSACTION_TEST` | run bounded transaction test |

Unknown states are held for review instead of being guessed into a lane.

## Validation focus

Only `PAIR_HYPOTHESIS` records may enter `validation_focus`.

The default focus limit is five. Ordering is deterministic:

1. fewer unresolved canonical evidence gates;
2. more already-materialized field packets;
3. capability key;
4. record ID.

The first two rules minimize evidence distance and execution setup. They do not estimate market size, margin, defensibility, or probability of success.

If queue coverage is missing, `missing_gate_count` remains unknown and the next action becomes `REBUILD_VALIDATION_QUEUE_OR_REVIEW_CANONICAL_GATES`. The control plane does not reconstruct missing truth from narrative fields.

## Batch decision

The artifact emits one batch-level next action:

```text
if ROUTE_TESTABLE exists:
    RUN_BOUNDED_TRANSACTION_TEST
elif PAIR_HYPOTHESIS validation focus exists:
    EXECUTE_PAIR_VALIDATION_FOCUS
elif one-sided need/resource records exist:
    EXPAND_COMPLEMENTARY_ACTOR_SENSING
else:
    EXPAND_REALITY_SENSING
```

This prevents the system from endlessly expanding discovery after a route-testable transaction candidate already exists.

## Production integration

`.github/workflows/opportunity-funnel-live.yml` runs after a successful `resource-imbalance-live` workflow and can also be manually dispatched.

It downloads the exact upstream live artifact, runs the repository test suite, builds `xz_opportunity_funnel.json`, asserts truth-boundary invariants, publishes a concise operator summary, and uploads the control-plane artifact.

The workflow intentionally consumes rather than mutates the upstream artifact. A future promotion must still come from newly ingested evidence and a canonical ledger rebuild.

## Current milestone interpretation

A useful milestone progression is:

```text
many raw observations
-> canonical NEED_ONLY / RESOURCE_ONLY records
-> PAIR_HYPOTHESIS
-> evidence-focused validation
-> ROUTE_TESTABLE
-> bounded real transaction attempt
-> accepted value / settlement
-> repeated transaction / learning
```

The funnel makes the middle of this chain operationally visible without pretending the final commercial proof already exists.
