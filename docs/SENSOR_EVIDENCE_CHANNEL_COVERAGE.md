# Sensor Evidence Channel Coverage

This layer measures **what kinds of evidence the world-observation system can actually sense now**. It is intentionally separate from both source liveness and execution capability coverage.

The chain is:

`source surface -> production-live registry -> governed Observation adapter -> latest Fabric observation -> evidence channel coverage`

A platform/source is a collection surface, not an ontology category. Evidence channels are stored in `data/evidence_channel_registry.json` so they can evolve without changing the semantic kernel or introducing permanent platform enums.

## Current governed channels

The current registry has six evidence channels:

- `OFFICIAL_STRUCTURAL_BASELINE`: official statistical, monetary, labor, trade and policy baselines.
- `HARD_BEHAVIOR_MONEY`: harder money/credit/trade/procurement/listing/financing traces.
- `LOCAL_REALITY`: Jiangsu/Xuzhou institutional, enterprise, media, asset and service evidence.
- `SEARCH_INTENT`: search-demand/salience evidence.
- `SOCIAL_PUBLIC_DISCOURSE`: public social/content perception, motive, behavior and friction evidence.
- `REPRESENTATIVE_RESEARCH`: public sampled/synthesized research context beyond anecdotal cases and official aggregates.

These are registry records, not code enums. They may be revised, split or extended when evidence warrants it.

## Coverage states

`OBSERVED_PRODUCTION` means at least one source bound to the channel is actually present in the latest durable Observation Fabric.

`PRODUCTION_LIVE_NOT_OBSERVED` means a source is marked production-live but has no current Fabric observation. This is a fail-closed operational gap.

`REGISTERED_NONLIVE_ONLY` means the system knows relevant surfaces, but none is currently production-observed. Manual/free/case-only/disabled/review-required sources remain visible here and do not count as live sensing.

`CANDIDATE_ONLY` means only dynamic sensor candidates are known.

## Current expected production result

With the current registries and the 8/8 live Observation source coverage, three channels are genuinely observed:

- `OFFICIAL_STRUCTURAL_BASELINE`
- `HARD_BEHAVIOR_MONEY`
- `LOCAL_REALITY`

Three remain explicit blind spots:

- `SEARCH_INTENT`
- `SOCIAL_PUBLIC_DISCOURSE`
- `REPRESENTATIVE_RESEARCH`

This is the important distinction: **8/8 production source coverage is not six-of-six evidence-channel coverage**.

For example, `BAIDU_INDEX` being registered and manually viewable does not make `SEARCH_INTENT` production-observed. Likewise, Weibo/Xiaohongshu/Douyin/Zhihu manual surfaces and Reddit/X/Instagram/Telegram candidates do not make `SOCIAL_PUBLIC_DISCOURSE` live China-primary evidence.

## Truth boundaries

- One observed source does not make a channel complete or representative.
- Search salience is not paid demand.
- Social discourse is not market demand.
- A research report is not current local reality.
- Hard behavioral/money evidence is not payment, payer confirmation or opportunity truth.
- Registered/manual/candidate sources are not silently promoted to production observations.
- Global auxiliary evidence is not China-primary evidence.
- `UNKNOWN != PASS`.
