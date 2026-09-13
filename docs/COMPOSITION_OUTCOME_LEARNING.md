# Composition Outcome & Learning Ledger

Status: `CANONICAL EXECUTION-OUTCOME EVIDENCE / FAIL-CLOSED`

## Purpose

Discovery, capability verification, resource composition and transaction validation answer what appears possible and what is ready to test.

This layer records what **actually happened** after a bounded route became transaction-ready.

Every outcome event binds to:

```text
composition_run_id
+
hypothesis_index
+
transaction_ref
+
validation_as_of
+
validation_snapshot_fingerprint
```

The exact validation snapshot is recomputed when the event is appended. Outcome evidence is rejected unless that snapshot was `bounded_transaction_ready` at that time.

This prevents later evidence from being used to rewrite the truth state under which an earlier route test actually ran.

## Atomic outcome events

```text
ROUTE_TEST_STARTED
DEPOSIT_OBSERVED
AUTHORIZED_COMMITMENT_OBSERVED
SIGNED_TASK_OBSERVED
DELIVERY_ACCEPTED
DELIVERY_REJECTED
SETTLEMENT_OBSERVED
SETTLEMENT_FAILED
REFERRAL_OBSERVED
DELEGATED_REPEAT_OBSERVED
PROVIDER_REPLACEMENT_SUCCEEDED
ALTERNATE_ROUTE_SUCCEEDED
ROUTE_FAILED
```

Each event is append-only and requires timezone-aware observation time, evidence reference and evidence note.

`SETTLEMENT_OBSERVED` additionally requires an explicit positive amount and currency.

## Transaction identity is mandatory

Acceptance and settlement may promote maturity only when they refer to the **same `transaction_ref`**.

```text
acceptance on transaction A
+
settlement on transaction B
!=
L4
```

This prevents unrelated events from being stitched into a false completed transaction.

## Conservative evidence maturity

The projection follows the existing canonical maturity ladder:

```text
L0 statement / no execution proof here
L3 deposit / authorized commitment / signed task
L4 completed accepted transaction + settlement
L5 repeat / referral
L6 delegated repeat / provider replacement / alternate route succeeds
L7 regenerative loop
```

This ledger intentionally does not manufacture L1/L2 from outcome events; those belong upstream.

### L3

At least one transaction has explicit:
- deposit evidence; or
- authorized commitment evidence; or
- signed task evidence.

### L4

At least one exact transaction has both:

```text
DELIVERY_ACCEPTED
+
SETTLEMENT_OBSERVED
```

Settlement alone is not L4. Acceptance alone is not L4.

### L5

Requires L4 plus either:
- a second distinct accepted + settled transaction; or
- referral evidence.

One successful transaction is not repeatability.

### L6

Requires L5 plus evidence of one orchestration mechanism on a successful transaction:
- delegated repeat;
- successful provider replacement; or
- successful alternate route.

### L7

**Never inferred by this store.**

L7 requires evidence that a recurring Demand Pump sends multiple transactions and that routing cost/risk or reliability actually improves. That is strategic/circulation truth and must be evaluated separately.

## Failures remain first-class evidence

Failure events are preserved instead of deleting or overwriting a route:

```text
ROUTE_FAILED
DELIVERY_REJECTED
SETTLEMENT_FAILED
```

A later failure does not erase a historically accepted and settled transaction. Conversely, one historical success does not hide current failure evidence.

```text
FAILED ROUTE != FALSE LATENT-VALUE THESIS
FAILED DELIVERY != NO DEMAND
SETTLEMENT FAILURE != NO CAPABILITY
```

Failures should later feed mechanism learning: which combinations fail capability verification, access, consent, delivery, economics or settlement, and which route changes repair them.

## Economic boundaries

The ledger aggregates observed settlement totals by currency but does not infer profit.

```text
SETTLEMENT != PROFITABILITY
REVENUE != NORMALIZED ORCHESTRATION MARGIN
FOUNDER FREE LABOR != ZERO COST
```

Profitability still requires the economics defined by the Resource Orchestration Kernel, including provider payouts, acquisition cost, QA/trust cost, failure reserve, operating costs and operator shadow labor.

## Reviewed intake

Use:

```bash
python scripts/import_composition_outcomes.py \
  --input outcomes.jsonl \
  --run-db state/composition-runs.db \
  --validation-db state/composition-validation.db \
  --outcome-db state/composition-outcomes.db \
  --as-of 2026-09-13T21:00:00+08:00
```

Input is explicit-allowlist JSON/JSONL. It accepts one atomic outcome event at a time.

Derived claims are rejected, including:

```text
evidence_maturity
transaction_success
profitable
repeatable
scale_ready
regenerative_loop
G0-G6
L3-L7
```

## Governing boundaries

```text
ROUTE_TEST_STARTED != COUNTERPARTY COMMITMENT
COMMITMENT != DELIVERY ACCEPTANCE
DELIVERY ACCEPTANCE != SETTLEMENT
SETTLEMENT != PROFITABILITY
ONE ACCEPTED+SETTLED TRANSACTION != REPEATABILITY
REPEAT != DELEGATED ORCHESTRATION
L6 != G4/G5/G6 PASS AUTOMATICALLY
OUTCOME HISTORY != DISCOVERY TRUTH REWRITE
L7 IS NOT INFERRED HERE
```

The purpose of outcome learning is not to declare victory. It is to preserve enough real execution truth that future discovery, routing and transaction design can learn from what actually worked and failed.
