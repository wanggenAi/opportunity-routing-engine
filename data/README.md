# Data

This directory contains schemas, small reproducible samples, source registries, validation templates, and non-sensitive reference data for the discovery engine.

## Current discovery data model

- `source_registry.csv` — recurring source inventory and access/automation state.
- `money_flow_signal_template.csv` — normalized money-flow claims after raw evidence is interpreted.
- `demand_pump_probe_template.csv` — real-world recurring-demand validation ledger.

Live network collection is intentionally separated into:

```text
NETWORK RESPONSE
→ provenance envelope / raw payload
→ normalization
→ derived signal
→ money-flow / psychology / opportunity interpretation
```

Raw data is **not** automatically a business signal.

The first live adapter is `CN_NBS` (国家统计局/国家数据). The scheduled live workflow writes transient evidence under `.local/` and uploads it as a short-retention GitHub Actions artifact. This avoids noisy automated commits while the schema and source stability are still being validated.

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
- a source's public visibility does not automatically grant redistribution rights;
- social/search salience != population share;
- derived claims must retain source/provenance links.

Raw external data should remain outside Git when licensing, privacy, size or volatility makes repository storage inappropriate.
