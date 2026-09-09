# Discovery Engine — Macro to Money to Actor to Friction

Status: `CANONICAL / LOCKED DISCOVERY LOGIC`

Effective: 2026-09-10

This document defines the **front half** of the Opportunity Routing Engine.

The resource-orchestration reset does **not** replace this discovery logic. It changes how validated opportunities are executed, not how the system discovers where economic opportunity is forming.

Canonical execution kernel: `docs/RESOURCE_ORCHESTRATION_KERNEL.md`.

## 1. Core principle

Do not begin with a product, startup idea, app, industry fashion or the operator's existing skill.

Begin by asking:

> **Where is money, time, attention, risk or productive capacity moving — and which actors are being forced to change behavior because of it?**

Discovery proceeds from broad reality toward narrow transaction hypotheses.

## 2. Canonical discovery funnel

```text
MACRO REGIME
→ MONEY FLOW
→ MARKET / INDUSTRY MOVEMENT
→ CONSUMPTION / INVESTMENT / EMPLOYMENT SHIFT
→ DEMOGRAPHIC / SOCIAL / TECHNOLOGY CHANGE
→ ACTOR SEGMENT
→ PSYCHOLOGY / DECISION LOGIC
→ OBSERVED BEHAVIOR
→ FRICTION / WORKAROUND
→ DESIRED OUTCOME
→ PAYER HYPOTHESIS
→ TRANSACTION GAP
→ ORCHESTRATION-FIT FILTER
```

Only after this funnel produces a credible opportunity does the Resource Orchestration Kernel take over.

## 3. Layer A — Macro regime

Track the economic environment before interpreting local anecdotes.

Core indicators include where available:
- GDP and sector contribution;
- CPI / core CPI / service CPI;
- PPI where relevant;
- household disposable income and median income;
- household consumption expenditure and category mix;
- social retail sales;
- service retail sales;
- online goods / online service retail;
- fixed-asset investment;
- manufacturing investment / equipment investment;
- real-estate investment and transactions;
- imports / exports;
- employment / unemployment / hiring signals;
- demographic structure / aging / household change;
- credit / financing / business confidence where useful;
- policy subsidies, procurement and public investment.

Macro indicators are not businesses. They tell the engine where to investigate next.

## 4. Layer B — Money flow

Translate macro indicators into explicit statements about where spending or investment is accelerating, weakening or migrating.

Examples:

```text
goods → services
ownership → rental / repair / second-hand
large durable purchases → smaller high-frequency experiences
housing / fixed assets → selective equipment / digital investment
offline retail → online / instant retail
local-only consumption → cross-city / destination consumption
product export → lifecycle service / aftermarket
full-time headcount → flexible / project-based capability
brand premium → value-for-money + emotional-value split
```

For every money-flow claim record:
- amount or growth rate where available;
- comparison period;
- geography;
- actor receiving money;
- actor losing share;
- source;
- whether the movement is policy-supported or independently occurring.

## 5. Layer C — Market and industry movement

Move from aggregate money to sectors and transaction chains.

Ask:
- which industries are gaining revenue / orders / footfall / exports?
- which industries are losing volume but gaining service revenue?
- where are margins migrating downstream or upstream?
- where is investment shifting from assets to operations, software, maintenance or service?
- where are firms explicitly adding new service layers?
- which formerly internal functions are becoming externalized?
- which markets are growing while service capacity, standards or trust lag behind?

Prefer evidence from actual revenue, orders, procurement, exports, service volumes, hiring and policy implementation over forecasts alone.

## 6. Layer D — Actor segmentation

Do not treat "consumers" or "companies" as one actor.

Relevant segments may include:
- young adults;
- students / graduates;
- middle-aged households;
- parents;
- elderly people / adult children;
- pet owners;
- rural / county consumers;
- cross-city visitors;
- merchants;
- self-employed operators;
- SMEs;
- manufacturers;
- exporters;
- dealers;
- service providers;
- technicians;
- owners of idle assets / capacity / skills / channels;
- institutions / sponsors.

For each actor ask:
- what changed?
- what do they now spend more/less on?
- what are they postponing?
- what risk are they avoiding?
- what work are they doing manually?
- what are they outsourcing?
- what capacity is idle?

## 7. Layer E — Psychology / decision logic

Psychology is a behavioral hypothesis, not a slogan.

Examples of decision logics to test:
- value-for-money / budget discipline;
- emotional value / "悦己";
- convenience and time-saving;
- trust and risk aversion;
- small-trial preference over large commitment;
- desire for verified outcomes rather than information;
- preference for local / immediate response;
- willingness to pay for certainty, accountability or speed;
- household sponsor paying for another family member;
- merchant paying for qualified traffic;
- manufacturer paying to preserve uptime / customer retention.

Any psychology claim should be linked to observed behavior, spending, search, transaction or repeated workaround evidence.

## 8. Layer F — Behavior before stated demand

Prefer actions over opinions.

Strong behavioral sensors include:
- real purchases / bookings;
- queueing / footfall tied to spend;
- repeat / referral;
- hiring;
- procurement / tender / RFQ;
- paid promotion;
- outsourcing;
- repair / maintenance orders;
- resale / rental / relisting;
- emergency sourcing;
- refunds / disputes;
- price comparison / downgrade behavior;
- use of informal helpers;
- expensive manual coordination;
- cross-city travel for consumption;
- firms building service networks after export growth.

## 9. Layer G — Friction and current workaround

A growing market without friction may have no new opportunity.

Find where actors still pay in:
- money;
- time;
- waiting;
- travel;
- errors;
- downtime;
- risk;
- coordination burden;
- trust burden;
- opportunity cost;
- customer churn;
- duplicate work.

Record the workaround currently used and why it remains imperfect.

## 10. Layer H — Desired outcome and payer

Convert friction into a measurable outcome:

> `[actor] wants [measurable outcome] within [time/price/risk constraints], because the current workaround costs [economic loss].`

Then identify who has economic incentive to pay.

Need actor, beneficiary and payer may differ.

## 11. Layer I — Transaction-gap classification

Classify why a satisfactory transaction is not already happening efficiently:

```text
DEMAND_GAP
CAPABILITY_GAP
PRICE_GAP
TRUST_GAP
INFORMATION_GAP
GEOGRAPHY_GAP
TIME_GAP
COORDINATION_GAP
PAYER_SHIFT
TECHNOLOGY_SHIFT
```

The gap ontology remains in `docs/THESIS_TRANSACTION_GAPS.md`.

## 12. Layer J — Orchestration-fit filter

This is the bridge between discovery and execution.

A real market opportunity may still be wrong for this engine.

Prefer hypotheses where:
- payer is identifiable;
- desired outcome can be bounded;
- execution decomposes into capability units;
- acquisition itself can be delegated or sourced through a channel;
- multiple resources can satisfy core capability units;
- output can be accepted objectively enough;
- trust/safety can be bounded;
- economic surplus can pay all participants and leave orchestration margin;
- the orchestrator adds value beyond introduction;
- a failed provider can be replaced without rebuilding the entire transaction.

Reject/downgrade opportunities that are large markets but depend permanently on founder charisma, personal sales, unbounded craftsmanship or unsafe/high-liability execution.

## 13. Evidence hierarchy

Use three evidence layers:

```text
MACRO EVIDENCE
  shows where to look

MARKET / BEHAVIOR EVIDENCE
  shows actors are actually changing and money/work is moving

TRANSACTION EVIDENCE
  shows our exact structure can capture value
```

Never promote macro growth directly into a business claim.

## 14. Geographic zoom

The engine may scan globally/nationally and validate locally.

Recommended zoom:

```text
China / global macro
→ Jiangsu / regional structure
→ Xuzhou / local money flow
→ district / cluster / industry chain
→ exact payer / provider / transaction
```

Xuzhou is a laboratory because local verification is feasible, not because opportunities must be local forever.

## 15. Discovery output schema

Every promoted opportunity candidate should include:

```text
macro_signal:
money_flow:
market_shift:
actor_segment:
psychology_decision_logic:
observed_behavior:
friction:
current_workaround:
desired_outcome:
payer_hypothesis:
payment_evidence:
transaction_gap:
existing_solution:
why_unresolved:
likely_capability_units:
demand_source_routes:
orchestration_value:
delegatability:
trust_safety_boundary:
cheapest_decisive_validation:
sources:
confidence:
```

## 16. Governing invariant

> **The macro layer tells us where the river is flowing. Actor behavior tells us where the current is strongest. Transaction evidence tells us whether we can build a bridge that people will actually pay to cross.**
