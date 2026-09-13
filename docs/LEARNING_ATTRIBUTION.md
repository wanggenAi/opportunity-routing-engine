# Learning Attribution Diagnostics

Status: `REVIEW-ONLY EVIDENCE-LINEAGE DIAGNOSTICS`

## Purpose

The engine now preserves source observations, capability-rule versions, graph materializations, capability verification, requirement versions, composition runs, transaction validation and execution outcomes.

This layer connects those histories for **review**. It does not create self-modifying rules or causal claims.

```text
PRESERVED LINEAGE
-> LINKED VERIFICATION COUNTS
-> COMPOSITION EXPOSURE
-> TRANSACTION / OUTCOME CONTEXT
-> REVIEW SIGNAL
-> HUMAN / EXPLICIT RULE-SOURCE REVIEW
```

## Attribution means lineage, not causal credit

A source or rule may appear upstream of a successful or failed route without being the cause of that result.

```text
SOURCE / RULE EXPOSED IN ROUTE
!=
SOURCE / RULE CAUSED OUTCOME
```

A route may fail because of access, consent, payer commitment, economics, delivery, settlement, timing or many other downstream factors even when the capability inference was correct.

Likewise, one successful transaction does not prove every source, rule or composition decision was optimal.

## Exact linked verification

Source/rule verification diagnostics are deliberately stricter than actor-capability matching.

A verification event is linked to a graph claim only when all are true:

```text
same actor_ref
+
same capability_key
+
verification.related_signal_refs explicitly contains source_id::signal_id
+
verification time >= claim observation time
```

Therefore:

```text
ACTOR + CAPABILITY MATCH != SOURCE / RULE ATTRIBUTION
OLDER VERIFICATION != VERIFICATION OF A NEWER CLAIM
NO RELATED SIGNAL REF != LINKED VERIFICATION
```

When the exact relation is absent, the graph claim remains `UNRESOLVED` for source/rule diagnostics even if the actor-capability pair has some other verification event.

## Claim diagnostic states

```text
CONFIRMED
REJECTED
UNRESOLVED
```

`UNRESOLVED` is not negative evidence.

```text
NO VERIFICATION != REJECTION
NO RESPONSE != FAILURE
STALE / UNTESTED != FALSE
```

## Source and rule summaries

For each source id, diagnostics report:
- claim output count;
- linked confirmed count;
- linked rejected count;
- unresolved count;
- linked-verification count;
- review signal.

For each inference-rule version, the same counts are computed only over claims carrying an `inference_rule_id`. Explicit OBSERVED capability claims are not silently credited to inference rules.

Current review signals:

```text
NO_LINKED_VERIFICATION
INSUFFICIENT_LINKED_VERIFICATION
MIXED_LINKED_VERIFICATION
REVIEW_REJECTION_CLUSTER
POSITIVE_LINKED_EVIDENCE
```

These are review cues, not automated actions.

The minimum linked-verification threshold is explicit and configurable. Below that threshold, evidence remains `INSUFFICIENT_LINKED_VERIFICATION` regardless of whether the few observed results are positive or negative.

## No automatic mutation

Diagnostics never:
- activate/deactivate a capability rule;
- create a new rule version;
- suppress a source;
- rewrite a Requirement Bundle;
- reorder providers as a quality ranking;
- promote G0-G6;
- promote L3-L7;
- claim causal accuracy.

```text
REVIEW SIGNAL != AUTOMATIC RULE MUTATION
REVIEW SIGNAL != AUTOMATIC SOURCE SUPPRESSION
LOW SAMPLE != LOW QUALITY
```

Any rule/source change remains a separate explicit reviewed action with versioned history.

## Composition learning diagnostic

For one exact `composition_run_id + hypothesis_index`, the diagnostic exposes:
- bundle id/version;
- graph materialization id;
- composition state;
- selected actor refs;
- source ids recoverable from the graph contributions;
- inference-rule ids recoverable from the graph contributions;
- current time-scoped G0-G3 projection;
- bounded-transaction-ready state;
- outcome evidence maturity;
- outcome event count;
- accepted+settled transaction count;
- transactions containing failure evidence;
- outcome event-type counts.

These fields answer:

> Which preserved inputs were present in this route, and what downstream evidence exists?

They do **not** answer:

> Which input caused the outcome?

## Failure interpretation

Keep failure level explicit.

```text
CAPABILITY REJECTION
!=
ACCESS FAILURE
!=
CONSENT FAILURE
!=
PAYER FAILURE
!=
ECONOMICS FAILURE
!=
DELIVERY REJECTION
!=
SETTLEMENT FAILURE
```

Only explicit capability verification may directly count toward a capability rule/source's linked CONFIRMED/REJECTED totals.

Downstream route/outcome failures remain contextual evidence around a composition, not automatic negative labels on upstream rules or sensors.

## CLI

```bash
python scripts/build_learning_diagnostics.py \
  --graph-db state/capability-graph.db \
  --verification-db state/capability-verification.db \
  --run-db state/composition-runs.db \
  --validation-db state/composition-validation.db \
  --outcome-db state/composition-outcomes.db \
  --run-id 1 \
  --hypothesis-index 0 \
  --as-of 2026-09-13T22:00:00+08:00 \
  --minimum-linked-verifications 5
```

The output is deterministic for the same preserved databases, run/hypothesis, time boundary and review threshold.

## Next learning boundary

This diagnostic slice deliberately stops before automated optimization.

Future learning may compare repeated route mechanisms, requirement versions and source/rule histories, but it must preserve:

```text
CORRELATION / LINEAGE != CAUSALITY
PAST SUCCESS != FUTURE GUARANTEE
OUTCOME FAILURE != CAPABILITY INFERENCE FAILURE
INSUFFICIENT SAMPLE != NEGATIVE EVIDENCE
MODEL RECOMMENDATION != AUTHORITY TO CHANGE CANONICAL RULES
```

The goal is a better review surface for accumulated real evidence, not a self-reinforcing scoring loop.
