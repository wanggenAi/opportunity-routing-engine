# Requirement Bundle Registry and Composition Runs

## Purpose

The resource side is now persistent through the Signal Ledger and Resource Capability Graph. The demand/decomposition side must be equally auditable.

Canonical bridge:

```text
OPPORTUNITY / DESIRED OUTCOME
-> VERSIONED REQUIREMENT BUNDLE
-> EXACT CAPABILITY GRAPH MATERIALIZATION
-> PERSISTENT COMPOSITION RUN
-> STRUCTURAL COVERAGE HYPOTHESES
-> ACCESS / CONSENT / PAYER / TRANSACTION GATES
```

## Requirement bundle truth

A `RequirementBundleSpec` records one version of a capability decomposition:

- `bundle_id`;
- `version`;
- required low-level capability keys;
- geography;
- `source_ref` pointing back to the opportunity/outcome that motivated the decomposition;
- rationale;
- explicit active/inactive state.

A bundle is **not** evidence that demand is real.

```text
REGISTERED REQUIREMENT BUNDLE
!= COUNTERPARTY REQUIREMENT CONFIRMED
!= PAYER EXISTS
!= PAYER COMMITTED
!= TRANSACTION READY
```

Changing the decomposition requires a new version. Historical versions remain queryable.

## Composition run lineage

Every persistent composition run freezes:

- exact capability graph `materialization_id`;
- graph ruleset fingerprint;
- graph observation snapshot fingerprint;
- exact requirement `bundle_id` + version;
- bundle source reference and rationale;
- `as_of` time;
- freshness window;
- maximum actors and hypothesis cap;
- resulting minimal-cover hypotheses.

The same exact input tuple is idempotent. A graph change, requirement version change, freshness-time change, or composition parameter change produces a distinct run.

## Composition states

Existing semantics remain unchanged:

```text
HYPOTHESIS_COMPOSED
DISCOVERED_COMPOSED
CALLABLE_COMPOSED
```

These states answer a structural resource question only.

`CALLABLE_COMPOSED` still does not mean:

- counterpart consent;
- legal permission for the transaction;
- access to premises/data/assets;
- safety approval;
- payer commitment;
- acceptable economics;
- transactionability.

## Production entry point

```bash
python scripts/build_resource_compositions_from_graph.py \
  --graph-db data/capability_graph.db \
  --requirement-db data/requirements.db \
  --run-db data/composition_runs.db \
  --bundle-id opportunity-123-capabilities \
  --summary-output artifacts/composition_summary.json
```

Omit `--bundle-id` to run every active requirement bundle.

The output preserves actor ids, exact globally unambiguous signal lineage, contribution evidence status and callable actor refs. Ordering is deterministic and is not a person/provider quality ranking.

## Governing invariants

```text
REQUIREMENT_BUNDLE_IS_DECOMPOSITION_NOT_DEMAND_TRUTH
BUNDLE_CHANGE_REQUIRES_NEW_VERSION
ACTIVE_BUNDLE_VERSION_IS_EXPLICIT
BUNDLE_SOURCE_REF_IS_REQUIRED
COMPOSITION_RUN_INPUTS_ARE_IMMUTABLE
COMPOSITION_RUN_LINKS_EXACT_GRAPH_MATERIALIZATION
COMPOSITION_RUN_LINKS_EXACT_REQUIREMENT_VERSION
MINIMAL_COVER_NE_BEST_ROUTE
CALLABLE_COMPOSED_NE_COUNTERPARTY_CONSENT
CALLABLE_COMPOSED_NE_TRANSACTIONABILITY
UNKNOWN_NE_PASS
```
