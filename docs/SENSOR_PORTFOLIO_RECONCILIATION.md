# Sensor Portfolio Reconciliation

Status: `SENSOR GOVERNANCE / FAIL-CLOSED`

Effective: 2026-09-15

Parents:
- `docs/DYNAMIC_SENSOR_FABRIC.md`
- `data/source_registry.csv`
- `data/sensor_candidates.json`

## Why this layer exists

The repository contains two legitimate but different registries:

1. `source_registry.csv` — operationally known sources, including automated live collectors, manual surfaces, case-only sources and disabled paths;
2. `sensor_candidates.json` — newly discovered sources moving through `DISCOVERED → QUALIFIED → ACTIVE → DEGRADED → RETIRED` governance.

Without reconciliation, a discovered candidate can be mistaken for coverage, or a manual platform entry can look equivalent to a production collector.

## Production coverage rule

Operational registry:

```text
status starts with ACTIVE_LIVE
→ production live coverage
```

Everything else remains registered but non-live unless another explicit governed source establishes active collection.

Candidate registry:

```text
lifecycle_state == ACTIVE
AND automation_ready == true
→ candidate production live coverage
```

In particular:

```text
DISCOVERED != coverage
QUALIFIED != coverage
ACTIVE_READY != ACTIVE collection
PUBLIC_MANUAL != automated sensor
REGISTERED source != observed evidence
```

## Platform surfaces

Named platforms are source surfaces, not ontology categories.

The current operational registry already contains domestic surfaces such as public/manual Baidu Index, Weibo, Xiaohongshu, Douyin and Zhihu entries. Their existence in the registry is useful, but it does not imply automated access, legal automation permission, representative sampling, demand, payment, or production coverage.

New global candidates such as Reddit/X/Instagram/Telegram similarly remain candidates until China relevance, unique signal value, access mode, permission and explicit activation are evidenced.

## Registry overlap

If the same `source_id` appears in both registries, the portfolio compares their production-live truth. A disagreement becomes:

```text
REGISTRY_STATE_MISMATCH
```

A mismatch is surfaced; it is never silently resolved to PASS.

## Governing boundaries

```text
DISCOVERED_SOURCE != PRODUCTION_COVERAGE
QUALIFIED_SOURCE != PRODUCTION_COVERAGE
ACTIVE_READY != ACTIVE_COLLECTION
MANUAL_SURFACE != AUTOMATED_LIVE_SENSOR
REGISTERED_SOURCE != LIVE_OBSERVATION
GLOBAL_CANDIDATE != CHINA_PRIMARY_EVIDENCE
PLATFORM != ONTOLOGY
REGISTRY_MISMATCH != PASS
UNKNOWN != PASS
```

The reconciled portfolio is a bookkeeping and coverage-truth layer. It does not activate collection or manufacture observations.
