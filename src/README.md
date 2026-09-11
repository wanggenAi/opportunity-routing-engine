# Source Code

Application/product code still waits for repeated commercial evidence.

The repository explicitly permits **discovery/evidence pipeline code** when it reduces a repeated sensing or validation bottleneck without pretending that code proves demand.

Current modules:

- `opportunity_ranker.py` — canonical G0-G6 score/gate discipline.
- `psychology_tracker.py` — evidence-weighted aggregate psychology/behavior signals; social salience is never converted into population share.
- `network_ingest.py` — provenance-safe HTTPS/JSON ingestion core with host allowlists, retries, response-size limits, payload hashes, atomic writes and explicit rejection of HTML/challenge responses.
- `nbs_adapter.py` — live adapter for the 2026 National Bureau of Statistics `国家数据` public-release API: catalog tree, indicators, time metadata and value retrieval.
- `regional_adapters.py` — Jiangsu Statistics and Xuzhou public-procurement evidence adapters.
- `resource_underuse_adapters.py` — Xuzhou public property-rights sensor for verified listed assets, explicit idle/vacant language and repeat-listing allocation friction.
- `resource_imbalance.py` — evidence-gated need/resource/blocker pairing. It emits only `NEED_ONLY`, `RESOURCE_ONLY`, `PAIR_HYPOTHESIS`, or `ROUTE_TESTABLE`; one-sided evidence cannot become an opportunity claim.

CLI:

```bash
python scripts/collect_nbs.py probe
python scripts/collect_nbs.py discover --page monthData --keyword 居民消费价格
python scripts/collect_nbs.py values --page monthData --cid <cid> --indicator-id <indicator-id> --period 202608
python scripts/collect_regional.py xuzhou-procurement-events --limit 10 --output .local/xz_procurement_recent.json
python scripts/collect_resource_underuse.py xuzhou-public-assets \
  --limit 20 \
  --output .local/xz_public_asset_underuse.json
python scripts/build_resource_imbalances.py \
  --needs data/need_signals.csv \
  --resources data/resource_signals.csv \
  --blockers data/blocker_signals.csv \
  --output .local/resource_imbalances.json
```

The NBS adapter intentionally uses the current UUID/catalog release API rather than the retired legacy `easyquery` contract.

The Resource Imbalance Engine deliberately requires exact capability/geography identity in V1. Public procurement can create paid need-side evidence, but cannot invent resource scarcity, spare capacity, provider willingness, or orchestration margin.

The first resource-side live sensor is deliberately conservative:

```text
public asset listing          → resource_state = DISCOVERED
explicit source 闲置 / 空置   → underuse = OBSERVED
second/third/repeated listing → allocation friction observed
```

A repeated listing does **not** automatically become underuse, and a public listing is never upgraded to `OPTIONED` merely because it is open to the market.

## Evidence-pipeline rules

- `network failure != zero`;
- `HTML/challenge != data`;
- `missing/stale != PASS`;
- `paid demand != resource availability`;
- `resource existence != underuse`;
- `relisting != underuse`;
- `DISCOVERED != OPTIONED`;
- preserve source, request, fetch time and response hash;
- keep raw evidence separate from derived money-flow/resource claims;
- do not bypass login/access controls;
- licensed/private data must not be committed unless storage and redistribution are explicitly permitted;
- live-network health belongs in a separate workflow so external outages do not invalidate deterministic unit tests.

Broad SaaS/product automation remains blocked until repeated paid transactions justify it.
