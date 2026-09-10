# Discovery Engine — Continuous Opportunity Radar

Status: `CANONICAL / LOCKED DISCOVERY LOGIC`

Effective: 2026-09-10

This document defines the **front half** of the Opportunity Routing Engine.

The resource-orchestration kernel does not replace discovery. It only starts after discovery has produced a credible opportunity.

Related canonical modules:
- `docs/DATA_SOURCE_REGISTRY.md`
- `docs/MONEY_FLOW_ENGINE.md`
- `docs/PSYCHOLOGY_BEHAVIOR_TRACKER.md`
- `docs/CASE_MINING_ENGINE.md`
- `docs/HOOK_ORCHESTRATION_DESIGN.md`
- `docs/RESOURCE_ORCHESTRATION_KERNEL.md`

## 1. Core principle

Do not begin with a product, startup idea, ERP/MES project, industry fashion or the operator's existing skill.

Begin by asking:

> **Where is money, time, attention, risk or productive capacity moving — and which actors are being forced to change behavior because of it?**

Then ask:

> **Which successful or failed market cases reveal a reusable mechanism for capturing the resulting friction?**

Only then generate opportunity hypotheses.

## 2. Canonical discovery funnel

```text
DATA SOURCE LAYER
→ MACRO REGIME
→ MONEY FLOW
→ MARKET / INDUSTRY MOVEMENT
→ CONSUMPTION / INVESTMENT / EMPLOYMENT SHIFT
→ DEMOGRAPHIC / SOCIAL / TECHNOLOGY CHANGE
→ ACTOR SEGMENT
→ PSYCHOLOGY / DECISION LOGIC
→ OBSERVED BEHAVIOR
→ CASE-MECHANISM MINING
→ FRICTION / WORKAROUND
→ DESIRED OUTCOME
→ PAYER HYPOTHESIS
→ TRANSACTION GAP
→ ORCHESTRATION-FIT FILTER
→ HOOK HYPOTHESIS
```

The system should continuously maintain the first ten layers. It should not wait for a human to ask a new question before looking at reality again.

## 3. Layer 0 — Data source maintenance

Maintain recurring data sources with provenance, cadence, geography and health state.

Required source classes:
- national macro/statistics;
- money/credit/trade/employment;
- Jiangsu regional statistics;
- Xuzhou local statistics and policy;
- procurement/public transaction data;
- company/platform primary evidence;
- authorized/public behavioral/social signals;
- case-study sources.

For each source preserve:
- observation period;
- publication date;
- units/denominator;
- geography;
- revision state;
- retrieval state;
- source URL.

Ad-hoc browsing may add evidence but must not replace the registry.

## 4. Layer A — Macro regime

Track the broad environment before interpreting anecdotes.

Core indicators include where available:
- GDP and sector contribution;
- CPI / core CPI / service CPI;
- PPI;
- PMI / industrial production;
- household disposable income and consumption expenditure;
- social retail and service retail;
- online goods/service retail;
- fixed investment / manufacturing / equipment investment;
- real-estate investment and transactions;
- money/credit/deposit/loan conditions;
- imports/exports;
- employment/unemployment/hiring;
- demographics / aging / household change;
- policy subsidies / procurement / public investment.

Macro indicators are **search-direction evidence**, not business proof.

## 5. Layer B — Money Flow Engine

Translate indicators into explicit statements about where economic activity is moving.

Ask:
- who is paying more/less?
- who is receiving more/less?
- what category is gaining/losing share?
- is change price-driven or volume-driven?
- is it policy-subsidized or independently recurring?
- is Xuzhou diverging from Jiangsu/China?

Examples of useful flow hypotheses:

```text
goods → services
new purchase → repair / rental / second-hand
large durable purchase → smaller high-frequency experience
broad fixed investment → selective equipment / IP / digital investment
offline → online / instant retail
city → county / rural consumption
product sale → lifecycle service / aftermarket
full-time staffing → project / outsourced capability
brand premium → value-for-money + selective emotional value
```

Divergence often matters more than raw growth.

## 6. Layer C — Market / industry movement

Move from aggregate flow to transaction chains.

Ask:
- which industries gain revenue/orders/traffic/exports?
- where are margins migrating upstream/downstream?
- what formerly internal work is externalizing?
- what capacity is becoming idle?
- where is demand growing faster than service/coordination capacity?
- what new policy/technology creates new payer/workflow roles?

Prefer real revenue, orders, procurement, hiring and operational evidence over forecasts.

## 7. Layer D — Actor segmentation

Do not treat `consumer` or `enterprise` as one actor.

Segments may include:
- young adults;
- students/graduates;
- parents/families;
- middle-aged households;
- elderly/adult children;
- rural/county residents;
- travelers/visitors;
- merchants/self-employed operators;
- SMEs/manufacturers/exporters;
- service providers/technicians;
- owners of idle assets/capacity/skills/channels;
- institutions/sponsors.

For each ask:
- what changed?
- what do they spend more/less on?
- what do they postpone?
- what risk do they avoid?
- what do they search for?
- what do they outsource?
- what capacity is idle?

## 8. Layer E — Psychology / decision logic

Psychology is dynamic and must be tracked, but it is a behavioral hypothesis, not a slogan.

Track dimensions such as:
- spending caution;
- value-for-money;
- small-trial preference;
- emotional/self-reward value;
- convenience/time-saving;
- trust/risk aversion;
- experience orientation;
- selective quality upgrade;
- health/longevity;
- repair/reuse/rental;
- social connection/belonging;
- willingness to pay for certainty/outcome.

Any psychology claim should be cross-checked against money and behavior.

`social salience != population share`.

## 9. Layer F — Behavior before opinions

Strong behavioral sensors include:
- purchases/bookings;
- repeat/referral;
- hiring;
- procurement/tender/RFQ;
- paid promotion;
- outsourcing;
- repair/maintenance orders;
- resale/rental/relisting;
- price-comparison/downgrade behavior;
- use of informal helpers;
- expensive manual coordination;
- cross-city travel for consumption;
- queue/traffic tied to spend;
- refunds/disputes;
- firms adding service networks after product growth.

## 10. Layer G — Case Mining

Continuously mine successful and failed cases.

Do not copy what a successful company sells. Extract mechanism:

```text
context change
→ actor behavior change
→ friction noticed
→ first hook
→ why counterparty engaged
→ payer
→ resources controlled / borrowed / partnered
→ delivery / acceptance
→ economics
→ repeat loop / Demand Pump
→ bypass / failure / moat
```

For every attractive success pattern seek a failed comparator or incumbent alternative.

## 11. Layer H — Friction / workaround

A growing market without unresolved friction may have no new opportunity.

Look for costs in:
- money;
- time;
- waiting;
- travel;
- errors;
- downtime;
- trust;
- coordination;
- opportunity cost;
- customer churn;
- duplicate work;
- idle capacity.

Record what actors currently do instead and why it remains imperfect.

## 12. Layer I — Desired outcome and payer

Convert friction into a measurable outcome:

> `[actor] wants [measurable outcome] within [time/price/risk constraints], because the current workaround costs [economic loss].`

Then identify:
- need actor;
- beneficiary;
- payer;
- sponsor/resource owner where relevant.

Need actor != payer by default.

## 13. Layer J — Transaction gap

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

## 14. Layer K — Orchestration fit

A real market opportunity may still be wrong for this engine.

Prefer when:
- payer is identifiable;
- outcome can be bounded;
- work decomposes into CapabilityUnits;
- acquisition can be targeted/delegated;
- multiple resources can satisfy key units;
- acceptance is observable;
- safety/legal risk is bounded;
- enough economic surplus exists for all parties;
- orchestration adds value beyond introduction;
- recurring demand can form a Demand Pump;
- failed providers can be replaced.

## 15. Layer L — Hook hypothesis

Before outreach, define what controlled value the orchestrator can bring.

Potential hooks:
- verified demand;
- pre-qualified capability;
- unique/verified information;
- measurable pilot/outcome;
- distribution access;
- idle-resource access;
- transparent conditional economics.

Do not approach a counterparty with only `do you have work?`.

## 16. Geographic zoom

Recommended zoom:

```text
China / global
→ Jiangsu
→ Xuzhou
→ district/county
→ industry / actor cluster
→ exact payer / resource / transaction
```

Xuzhou is the first laboratory because local verification is feasible, not because the system must stay local.

## 17. Discovery output schema

Every promoted opportunity candidate should include:

```text
macro_signal:
money_flow:
market_shift:
actor_segment:
psychology_decision_logic:
observed_behavior:
case_mechanism_analogs:
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
likely_hook:
resource_state_owned_optioned_discovered_hypothetical:
orchestration_value:
delegatability:
regenerative_loop:
trust_safety_boundary:
cheapest_decisive_validation:
sources:
confidence:
```

## 18. Promotion discipline

A candidate should not become `#1` because it was discovered first or researched most deeply.

The system should first create a **broad comparable pool**, then apply the same G0-G6 scorecard and evidence standards across candidates.

## 19. Governing invariant

> **The data layer tells us what is changing. Money flow tells us where economic energy moves. Psychology and behavior tell us why actors change decisions. Cases teach us reusable mechanisms. Only then do we choose where to place the hook and how to orchestrate resources.**
