# Data Source Registry

Status: `CANONICAL / DISCOVERY INFRASTRUCTURE`

Effective: 2026-09-14

See also `docs/DYNAMIC_SENSOR_FABRIC.md`.

## Purpose

The engine maintains a continuous, auditable source layer before generating opportunity conclusions. It must not depend on ad-hoc searches or one-off news reading.

The registry is **dynamic infrastructure**, not a closed catalog. Current platforms, websites and datasets are sensor instances. New sources may be discovered, qualified, activated, degraded and retired without changing the world-model ontology.

## Research geography policy

Default research priority is:

```text
PRIMARY RESEARCH DOMAIN: CHINA
PRIMARY EXECUTION LENS: CHINA → JIANGSU → XUZHOU
SECONDARY OBSERVATION LAYER: GLOBAL
CROSS-BORDER: EXCEPTION ONLY
```

Global sources are allowed and encouraged when they add information about China, Chinese actors/resources, possible transfer mechanisms, technology changes or counter-evidence. Foreign salience does not establish Chinese prevalence or demand.

## Source tiers

### Tier A — statistical / administrative / hard transaction truth
Examples include official statistics, administrative releases, payment/transaction aggregates and other sources with explicit denominator/methodology.

Use for macro regime, money flow, employment, demographics and verified transaction signals.

### Tier B — primary market / company / platform evidence
Examples include company filings/sites, hiring pages, price pages, marketplaces, public transaction records, industry associations and public platform data.

Use for actor state, market movement, price, utilization, capability and workflow evidence.

### Tier C — structured behavioral / social / search signals
Examples include authorized/public aggregate social-media search/trend outputs, search trends, public review aggregates, forum/community samples and topic-change signals.

Use for attention, perception, motive and behavior hypotheses. Do not infer population prevalence from raw social-media share.

### Tier D — anecdotal / exploratory evidence
Examples include individual public posts, interviews, local observations, media features and small cases.

Use to generate hypotheses and identify mechanisms, never as standalone macro truth.

## Platform names are not ontology

Examples such as Xiaohongshu, Douyin, Weibo, Zhihu, Bilibili, Reddit, X, Instagram, Telegram, GitHub, app reviews or future platforms are source records only.

```text
PLATFORM != ONTOLOGY
SOURCE CATEGORY != WORLD CATEGORY
TODAY'S PLATFORM LIST != DISCOVERY BOUNDARY
```

A future source not known today must be addable without adding a new semantic primitive or changing business strategy.

## Canonical source record

```text
source_id:
name:
source_tier: A/B/C/D
owner:
base_url:
origin_geography:
relevance_geographies:
actor_scope:
observable_dimensions:
access_mode: API/HTML/CSV/XLS/PDF/MANUAL/OTHER
refresh_cadence: DAILY/WEEKLY/MONTHLY/QUARTERLY/ANNUAL/EVENT
publication_lag:
historical_depth:
units:
revision_policy:
policy_contamination_risk:
personal_data_risk:
spam_manipulation_risk:
automation_allowed: YES/NO/UNKNOWN
unique_signal_value:
last_successful_fetch:
last_observed_period:
parser_adapter:
status: DISCOVERED/QUALIFIED/ACTIVE/DEGRADED/PAUSED/RETIRED
notes:
```

Existing CSV records may use the earlier smaller schema until migrated. Missing new metadata is `UNKNOWN`, not permission to infer it.

## Dynamic source lifecycle

```text
DISCOVERED
→ QUALIFIED
→ ACTIVE
→ DEGRADED
→ RETIRED
```

Qualification should ask:
- what actors/states/behaviors/resources can this source reveal?
- does it add unique signal value relative to existing sources?
- can provenance and time be retained?
- is access lawful and technically sustainable?
- what are its manipulation, sampling and privacy risks?
- how does source geography differ from the target/relevance geography?

Source discovery must not automatically activate a crawler. Access policy and evidence value are separate decisions.

## Domestic baseline sources

The baseline should continue covering China macro and market reality, including national statistical, finance, trade, employment and household indicators; Jiangsu official economic/market data; and Xuzhou/local evidence where available.

These are baseline observers, not a fixed list. Domestic consumer, enterprise, marketplace, hiring, review, search and community signals should be added when lawful, auditable and useful.

## Global auxiliary sources

The registry may include foreign/global social, developer, market, company, product-review and community sources when they can illuminate China-related questions.

Examples of legitimate uses:
- foreign perception/usage of a Chinese product or resource;
- early technology/business behavior that may create a China transfer hypothesis;
- failure modes to test against the domestic market;
- global changes that reprice Chinese/Jiangsu/Xuzhou resources.

Truth boundaries:

```text
GLOBAL SIGNAL != DOMESTIC FACT
FOREIGN TREND != CHINA DEMAND
FOREIGN SOCIAL SALIENCE != CHINESE CONSUMER PSYCHOLOGY
TRANSFER HYPOTHESIS != TRANSFERABILITY
```

## Update discipline

For every source adapter:
1. preserve source/origin geography separately from target/relevance geography;
2. preserve raw publication date and observation period;
3. distinguish flow, stock, price, volume and index values;
4. retain revisions rather than silently overwrite history;
5. store geography and denominator where available;
6. preserve source URL/ref and retrieval timestamp;
7. do not coerce missing values into zero;
8. expose stale/degraded source state;
9. retain contradictions and sampling limitations;
10. use manual fallback only with explicit provenance.

## Data-source health

Track where available:

```text
freshness_score
fetch_success_rate
schema_stability
revision_frequency
coverage_score
provenance_score
sampling_risk
manipulation_risk
unique_signal_value
```

A stale or broken source should reduce confidence rather than silently disappear.

## Governing invariant

> **全球都可以成为观察面，但主要研究中国现实。平台会变、来源会变，世界模型不能跟着平台列表重写；如果不能说明来源、时间、地理、样本边界和证据关系，该信号不能被提升成商业事实。**
