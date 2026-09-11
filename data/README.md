# Data

This directory contains schemas, small reproducible samples, source registries, validation templates, and non-sensitive reference data for the discovery engine.

## Current discovery data model

- `source_registry.csv` — recurring source inventory and access/automation state.
- `money_flow_signal_template.csv` — normalized money-flow claims after raw evidence is interpreted.
- `demand_pump_probe_template.csv` — real-world recurring-demand validation ledger.
- `need_signal_template.csv` — verified deficit/need-side evidence, including payer and paid-event state.
- `resource_signal_template.csv` — verified resource/control state plus a separate underuse-evidence axis.
- `blocker_signal_template.csv` — observed explanation for why compatible need/resource actors are not already transacting.

Resource imbalance inputs must stay separated:

```text
NEED SIGNAL
+
RESOURCE SIGNAL
+
BLOCKER SIGNAL
→ Resource Imbalance Engine
→ NEED_ONLY / RESOURCE_ONLY / PAIR_HYPOTHESIS / ROUTE_TESTABLE
```

`ROUTE_TESTABLE` is only permission for a cheap bounded route test. It is not transaction readiness, scale readiness, or G0-G6 approval.

Live network collection is intentionally separated into:

```text
NETWORK RESPONSE
→ provenance envelope / raw payload
→ normalization
→ derived signal
→ money-flow / psychology / resource-imbalance / opportunity interpretation
```

Raw data is **not** automatically a business signal.

The first live adapters include `CN_NBS` (国家统计局/国家数据), `JS_STATS` (江苏省统计局), and `XZ_GGZY` (徐州市公共资源交易中心). Scheduled live workflows write transient evidence under `.local/` and upload it as short-retention GitHub Actions artifacts. This avoids noisy automated commits while schemas and source stability are being validated.

When a source becomes stable and redistribution/storage rights are clear, selected normalized snapshots may be promoted into versioned repository data.

## Do not commit

- secrets or API keys;
- credentials/session tokens/cookies;
- private personal contact data;
- licensed exports whose storage/redistribution rights are unclear;
- unnecessary individual-level social-media profiles;
- sensitive supplier/customer commercial data without permission;
- private communications unless deliberately redacted and permitted.

## Truth rules

- missing data != zero;
- stale data != current evidence;
- HTML/login/challenge pages != successful ingestion;
- paid need != verified spare resource;
- resource existence != underuse;
- DISCOVERED != OPTIONED;
- a source's public visibility does not automatically grant redistribution rights;
- social/search salience != population share;
- derived claims must retain source/provenance links.

Raw external data should remain outside Git when licensing, privacy, size or volatility makes repository storage inappropriate.
