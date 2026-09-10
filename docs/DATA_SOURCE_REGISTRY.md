# Data Source Registry

Status: `CANONICAL / DISCOVERY INFRASTRUCTURE`

Effective: 2026-09-10

## Purpose

The Opportunity Routing Engine must maintain a continuous, auditable data-source layer before generating opportunity conclusions.

The system should not depend on ad-hoc searches or one-off news reading. Every recurring source should be registered with provenance, geography, cadence, dimensions, access method, quality tier and update state.

## Source tiers

### Tier A — official statistical / administrative truth
Examples:
- National Bureau of Statistics / 国家数据;
- provincial and city statistical bureaus;
- People's Bank of China and financial-statistics releases;
- Ministry of Commerce / 商务数据中心 / 商务预报;
- General Administration of Customs and customs statistics;
- Ministry of Human Resources and Social Security / employment releases;
- government procurement / public resource transaction platforms;
- official population, health, education, housing, transport and industry datasets.

Use for macro regime, money-flow, employment, demographic and verified transaction signals.

### Tier B — primary market / company / platform evidence
Examples:
- listed-company filings;
- company official sites and price pages;
- hiring pages;
- public procurement awards;
- platform public trend/transaction data;
- industry association releases;
- public marketplace listings and observable price/volume signals.

Use for market movement, payer behavior, capacity, prices and task/workflow evidence.

### Tier C — structured behavioral / social signals
Examples:
- authorized/public aggregate social-media search/trend outputs;
- search-trend products;
- public review aggregates;
- forum/community discussion sampled under documented methods;
- news-frequency and topic-change signals.

Use for psychology/attention hypotheses. Do not infer population prevalence from raw social-media share.

### Tier D — anecdotal / exploratory evidence
Examples:
- individual posts;
- interviews;
- local observations;
- media feature stories;
- small case studies.

Use to generate hypotheses and identify mechanisms, never as standalone macro truth.

## Canonical source record

```text
source_id:
name:
source_tier: A/B/C/D
owner:
base_url:
geography:
actor_scope:
indicator_scope:
access_mode: API/HTML/CSV/XLS/PDF/MANUAL/OTHER
refresh_cadence: DAILY/WEEKLY/MONTHLY/QUARTERLY/ANNUAL/EVENT
publication_lag:
historical_depth:
units:
revision_policy:
policy_contamination_risk:
personal_data_risk:
automation_allowed: YES/NO/UNKNOWN
last_successful_fetch:
last_observed_period:
parser_adapter:
status: ACTIVE/DEGRADED/PAUSED
notes:
```

## Initial mandatory registry

### National macro
- National Bureau of Statistics `stats.gov.cn` / `data.stats.gov.cn`
  - GDP, CPI, PPI, PMI, industrial production, retail, fixed investment, income/expenditure, unemployment, population.
- Ministry of Commerce `mofcom.gov.cn` / `data.mofcom.gov.cn`
  - consumption market, e-commerce, trade, FDI/ODI, service/commodity market monitoring.
- People's Bank of China `pbc.gov.cn`
  - money/credit, household deposits/loans, social financing, payment/financial conditions where relevant.
- General Administration of Customs `customs.gov.cn`
  - import/export by product, geography, firm/trade type where available.
- Ministry of Human Resources and Social Security `mohrss.gov.cn`
  - employment, labor-market and policy signals.

### Jiangsu
- Jiangsu Provincial Bureau of Statistics `tj.jiangsu.gov.cn`.
- Jiangsu provincial government economic-operation releases.
- Jiangsu commerce / industry / human-resources / culture-tourism departments where indicators are material.

### Xuzhou
- Xuzhou municipal government/statistical releases.
- Xuzhou public resource transaction center `ggzy.zwb.xz.gov.cn`.
- Xuzhou commerce, industry, culture-tourism, human-resources, housing, transport and district-level official releases.

## Update discipline

For every source adapter:
1. preserve raw publication date and observation period;
2. distinguish flow, stock, price, volume and index values;
3. retain revisions rather than silently overwrite history;
4. store geography and denominator;
5. preserve source URL and retrieval timestamp;
6. do not coerce missing values into zero;
7. expose stale/degraded source state;
8. use manual fallback only with explicit provenance.

## Data-source health

Track:

```text
freshness_score
fetch_success_rate
schema_stability
revision_frequency
coverage_score
provenance_score
```

A stale or broken source should reduce confidence rather than silently disappear.

## Governing invariant

> **If we cannot say where a number came from, what period it represents, what population/market it covers and whether it was revised, it cannot drive an opportunity decision.**
