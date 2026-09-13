# Persistent Resource Capability Graph

## Purpose

The Resource Capability Graph is a **derived, replayable evidence layer** between live sensing and resource composition.

Canonical flow:

```text
RAW SIGNAL OBSERVATIONS
-> ACCEPTED CURRENT SIGNAL STATE
-> ACTIVE VERSIONED INFERENCE RULES
-> IMMUTABLE CAPABILITY MATERIALIZATION
-> CAPABILITY COVERAGE / RESOURCE COMPOSITION
-> REAL-WORLD VALIDATION
```

The graph is not a supplier directory and is not source truth. Raw observations remain the evidence authority.

## Materialization model

Each materialization freezes:

- the exact current accepted raw observation snapshot;
- the exact active capability-rule versions;
- all explicit `OBSERVED` capability claims;
- all rule-derived `INFERRED` capability claims;
- exact `(source_id, signal_id)` provenance;
- geography, availability and permission state carried from the signal;
- the inference rule id/version for inferred claims.

A rule change creates a **new materialization**. Earlier materializations are not rewritten.

Re-running against the same observation snapshot and the same active rule set is idempotent.

## Lineage identity

A bare `signal_id` is not globally unique because two sensors can emit the same item id.

Persistent graph lineage therefore uses:

```text
(source_id, signal_id)
```

When graph claims are exported back into the generic `CapabilityClaim` contract, the source reference is rendered as:

```text
source_id::signal_id
```

This prevents cross-sensor provenance collisions without breaking the existing signal model.

## Current-state replay

The raw archive may contain out-of-order observations. Materialization does not blindly use the last row inserted.

For every stable `(source_id, signal_id)` identity, the graph rebuild step:

1. recovers the latest accepted raw observation;
2. checks its observation time against the signal ledger current state;
3. checks its semantic fingerprint against the current ledger fingerprint;
4. fails closed if raw evidence and semantic current state cannot be reconciled.

Therefore:

```text
ARCHIVED != CURRENT
OUT_OF_ORDER != CURRENT
CURRENT_STATE_WITHOUT_RAW_EVIDENCE != MATERIALIZABLE
```

## Rule replay

Rule versions are immutable in the capability rule registry. Activating a new version and re-running materialization produces a new graph snapshot.

The graph store can diff two materializations. A rule change can therefore be audited as:

```text
materialization N
  rule-a@v1 -> capability.x

materialization N+1
  rule-a@v2 -> capability.y

DIFF
  removed: capability.x / rule-a@v1
  added:   capability.y / rule-a@v2
```

This is the first learning primitive for testing whether inference-rule changes improve or degrade discovery.

## Truth boundaries

The graph never upgrades evidence merely because it is persisted.

```text
INFERRED != OBSERVED
OBSERVED != CONFIRMED
ADVERTISED != CONFIRMED AVAILABLE
UNKNOWN PERMISSION != ALLOWED
GRAPH CLAIM != CALLABLE RESOURCE
CALLABLE RESOURCE != COUNTERPARTY CONSENT
CAPABILITY COVERAGE != TRANSACTIONABILITY
```

Ordinary structured/public observation intake cannot self-declare `CONFIRMED`, `COMMITTED`, or `ALLOWED` state.

A future confirmation workflow must produce those states through separate evidence and must preserve its own provenance.

## Production entry point

```bash
python scripts/materialize_capability_graph.py \
  --signal-db data/live_signals.db \
  --rule-db data/capability_rules.db \
  --graph-db data/capability_graph.db \
  --summary-output artifacts/capability_graph_summary.json
```

The command emits:

- materialization id;
- previous materialization id;
- active rule ids;
- observation and claim counts;
- observation/ruleset fingerprints;
- added/removed claim counts;
- exact added/removed claim lineage.

## Composition boundary

`SQLiteCapabilityGraphStore.capability_claims()` exports ordinary `CapabilityClaim` objects, so existing capability coverage and multi-actor composition logic can consume the graph directly.

This does **not** mean the graph selects the best person, supplier, employer, counterparty, or commercial route. Composition remains structural evidence only.

## Governing invariants

```text
RAW_OBSERVATION_IS_EVIDENCE_AUTHORITY
CAPABILITY_GRAPH_IS_DERIVED_NOT_SOURCE_TRUTH
RULE_VERSION_CHANGE_CREATES_NEW_MATERIALIZATION
MATERIALIZATION_HISTORY_IS_IMMUTABLE
SOURCE_ID_PLUS_SIGNAL_ID_IS_LINEAGE_IDENTITY
OUT_OF_ORDER_OBSERVATION_MUST_NOT_BECOME_CURRENT_GRAPH_STATE
INFERRED_NE_OBSERVED
OBSERVED_NE_CONFIRMED
GRAPH_CLAIM_NE_CALLABILITY
GRAPH_CLAIM_NE_TRANSACTIONABILITY
UNKNOWN_NE_PASS
```
