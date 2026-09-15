# Live Observation Coverage

## Purpose

`ACTIVE_LIVE*` in `data/source_registry.csv` means the repository has a real live source path. It does **not** mean that source has already been normalized into the unified `ObservationEnvelope` store.

This layer reconciles three separate states:

1. **Production-live registry truth** — the operational source registry says the source has a live production path.
2. **Unified adapter support** — the Observation Fabric has an explicitly governed adapter mapping for that exact source identity.
3. **Latest Fabric observation truth** — the latest successful durable Observation Fabric artifact actually contains at least one current observation for that source.

These states must never be collapsed.

## Coverage states

For each production-live source:

- `OBSERVED_IN_LATEST_FABRIC`: exact source ID is governed by a unified adapter and is present in the latest Fabric artifact.
- `ADAPTER_SUPPORTED_NOT_OBSERVED`: adapter support exists, but the latest Fabric contains no current observation from the source.
- `NO_UNIFIED_ADAPTER`: source is production-live elsewhere in the repository but has not yet been normalized into the unified Fabric.
- `OBSERVED_WITHOUT_GOVERNED_ADAPTER_SUPPORT`: latest Fabric contains the source but no explicit adapter-support declaration exists. This is an integrity alert, not a success shortcut.

## Current governed adapter support

The explicit support manifest currently binds:

- `JS_STATS` → Jiangsu money-flow observation adapter
- `XZ_GGZY` → procurement and resource-underuse observation adapters
- `EJY365_XZ_LINKED` → resource-underuse observation adapter
- `JS_GGZY_XZ_MIRROR` → resource-underuse observation adapter

The support list is intentionally exact-source bound. A generic parser accepting arbitrary `source_id` values is not enough to claim governed support.

## Current production gap

At the introduction of this layer, the operational registry contains eight production-live source IDs. The latest verified unified Fabric contains current observations from three of those production-live sources:

- `JS_STATS`
- `XZ_GGZY`
- `EJY365_XZ_LINKED`

The following production-live sources remain outside the unified Observation Fabric and therefore require future adapter work before they can count as unified observation coverage:

- `CN_NBS`
- `CN_PBOC`
- `CN_PBOC_JS`
- `CN_CUSTOMS`
- `XZ_GOV_FINANCE_DEMAND`

This gap is architectural coverage debt, not evidence that those domains have zero activity.

## Production proof

`.github/workflows/live-observation-coverage-016.yml` downloads the latest successful `observation-fabric-live-state` artifact and reconciles it against the current source registry. It refuses to use an incomplete or failed latest Fabric run on push-triggered checks.

The workflow publishes a coverage artifact and asserts that no payer, paid-need, route-testable, opportunity, taxonomy activation or commercial score is manufactured.

## Truth boundaries

- `ACTIVE_LIVE_REGISTRY != OBSERVED_IN_FABRIC`
- `ADAPTER_SUPPORT != CURRENT_OBSERVATION`
- `SEPARATE_WORKFLOW != UNIFIED_FABRIC`
- `MISSING_FABRIC_SOURCE != ZERO_WORLD_ACTIVITY`
- `OBSERVED_SOURCE != COMPLETE_DOMAIN_COVERAGE`
- `UNKNOWN != PASS`

This layer is observation-governance infrastructure only. It does not create taxonomy or business truth.
