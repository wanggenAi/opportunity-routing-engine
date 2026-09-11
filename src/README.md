# Source Code

Application/product code still waits for repeated commercial evidence.

The repository explicitly permits **discovery/evidence pipeline code** when it reduces a repeated sensing or validation bottleneck without pretending that code proves demand.

Current modules:

- `opportunity_ranker.py` — canonical G0-G6 score/gate discipline.
- `psychology_tracker.py` — evidence-weighted aggregate psychology/behavior signals; social salience is never converted into population share.
- `network_ingest.py` — provenance-safe HTTPS/JSON ingestion core with host allowlists, retries, response-size limits, payload hashes, atomic writes and explicit rejection of HTML/challenge responses.
- `nbs_adapter.py` — live adapter for the 2026 National Bureau of Statistics `国家数据` public-release API: catalog tree, indicators, time metadata and value retrieval.

CLI:

```bash
python scripts/collect_nbs.py probe
python scripts/collect_nbs.py discover --page monthData --keyword 居民消费价格
python scripts/collect_nbs.py values --page monthData --cid <cid> --indicator-id <indicator-id> --period 202608
```

The NBS adapter intentionally uses the current UUID/catalog release API rather than the retired legacy `easyquery` contract.

## Evidence-pipeline rules

- `network failure != zero`;
- `HTML/challenge != data`;
- `missing/stale != PASS`;
- preserve source, request, fetch time and response hash;
- keep raw evidence separate from derived money-flow claims;
- do not bypass login/access controls;
- licensed/private data must not be committed unless storage and redistribution are explicitly permitted;
- live-network health belongs in a separate workflow so external outages do not invalidate deterministic unit tests.

Broad SaaS/product automation remains blocked until repeated paid transactions justify it.
