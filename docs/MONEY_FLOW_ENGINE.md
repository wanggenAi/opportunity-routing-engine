# Money Flow Engine

Status: `CANONICAL / DISCOVERY INFRASTRUCTURE`

Effective: 2026-09-10

## Purpose

Convert macro, transaction and market data into explicit, falsifiable statements about **where money is moving, where it is leaving, and which actors are changing behavior because of that movement**.

The engine does not ask only `which sector is growing?`. It asks:

> **Who is paying more, who is receiving more, what category lost share, what changed in price vs volume, what is policy-driven, and what new friction appears along the route?**

## Canonical chain

```text
RAW INDICATOR
→ NORMALIZED SERIES
→ CHANGE / ACCELERATION / DIVERGENCE
→ MONEY-FLOW CLAIM
→ RECEIVER / LOSER ACTORS
→ BEHAVIORAL EXPLANATION
→ FRICTION HYPOTHESIS
→ OPPORTUNITY WATCHLIST
```

## Core lenses

### 1. Household money
Track where households allocate:
- food/basic goods;
- discretionary goods;
- services;
- healthcare;
- education/culture/entertainment;
- travel/leisure;
- housing/rent/repair;
- mobility;
- durable goods;
- digital/online consumption;
- savings/deposits/debt where evidence exists.

### 2. Enterprise money
Track:
- fixed-asset investment;
- equipment/tool investment;
- software/information-service spending proxies;
- outsourced professional/business services;
- hiring vs project-based capability demand;
- maintenance/aftermarket/service spending;
- marketing/customer-acquisition expenditure proxies;
- logistics/supply-chain spending;
- compliance/testing/certification/procurement where observable.

### 3. Government / institutional money
Track:
- procurement;
- subsidies;
- public investment;
- service outsourcing;
- recurring operating contracts;
- grants and policy pilots.

Treat government money separately from independent private willingness to pay.

### 4. Cross-region / cross-border money
Track:
- imports/exports;
- tourism inflow/outflow;
- cross-city consumption;
- e-commerce flows;
- industrial chain transfers;
- inbound/outbound business-service demand.

## Required transformations

For every important series compute where meaningful:

```text
level
YoY change
MoM / QoQ change
3-period momentum
12-period trend
share of parent category
share change
relative growth vs benchmark
acceleration / deceleration
price-vs-volume interpretation
policy-supported flag
```

Do not calculate a metric when the denominator or series definition changed without adjustment.

## Divergence is often more useful than growth

High-value discovery signals include:

```text
services ↑ while goods flat
online ↑ while offline flat
county/rural ↑ faster than city
repair/rental ↑ while new durable purchase ↓
equipment investment ↑ while total investment ↓
hiring ↓ while outsourcing/project work ↑
traffic ↑ but merchant revenue flat
orders ↑ but delivery capacity flat
consumer attention ↑ but transaction volume flat
```

A divergence can expose a gap that simple industry-growth ranking misses.

## Price vs real demand

Nominal spending growth can be caused by price inflation rather than greater real demand.

Whenever possible separate:
- price change;
- volume/quantity change;
- mix upgrade/downgrade;
- policy subsidy effects.

`nominal_growth != real_demand_growth`.

## Geography stack

Every major flow should be compared across:

```text
China
→ Jiangsu
→ Xuzhou
→ district/county where possible
→ exact market/actor cluster
```

Useful local opportunity often appears where Xuzhou diverges from national/provincial averages.

## Money-flow claim schema

```text
flow_id:
observation_period:
geography:
from_category_or_actor:
to_category_or_actor:
indicator:
level:
change:
benchmark_change:
divergence:
price_effect:
volume_effect:
policy_effect:
receiver_actor:
loser_actor:
likely_decision_logic:
behavioral_corroboration:
source_ids:
confidence:
next_probe:
```

## Example interpretation pattern

Suppose:
- broad retail +1%;
- services +5%;
- tourism/leisure >+10%;
- durable goods weak;
- household confidence cautious.

Do not conclude `people are spending more`.

A better claim is:

> Households appear to be reallocating a portion of discretionary spending from selected durables/brand-heavy goods toward service/experience categories while remaining price sensitive.

Then the engine must seek behavioral and local corroboration before generating opportunities.

## Opportunity promotion rule

A money-flow signal can enter the opportunity watchlist only when it identifies:
1. a receiving or losing actor;
2. a plausible changed behavior;
3. a friction or unmet outcome;
4. at least one observable payer/workaround path to investigate.

It does **not** become a business merely because the category grows.

## Output cadence

Recommended:
- daily: procurement, high-frequency market/price/news/behavior signals;
- weekly: behavioral/social and transaction anomaly summary;
- monthly: CPI/PPI/retail/trade/finance/employment/money-flow update;
- quarterly: GDP/income/expenditure/investment/sector structure reset;
- annual: structural demographic/industry baseline.

## Governing invariant

> **Do not ask only where money is. Ask where it is moving, why actors changed behavior, what work the movement creates, and who has economic reason to pay to remove the resulting friction.**
