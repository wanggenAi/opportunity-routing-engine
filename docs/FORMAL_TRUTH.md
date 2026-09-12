# Formal Truth

Last updated: 2026-09-12

This document is the current commercial source of truth. Historical rankings and launch designs remain evidence, but they do not override the current truth stated here.

Canonical foundations:
- `docs/RESOURCE_ACTIVATION_THESIS.md`
- `docs/DATA_SOURCE_REGISTRY.md`
- `docs/DISCOVERY_ENGINE.md`
- `docs/MONEY_FLOW_ENGINE.md`
- `docs/PSYCHOLOGY_BEHAVIOR_TRACKER.md`
- `docs/CASE_MINING_ENGINE.md`
- `docs/RESOURCE_IMBALANCE_ENGINE.md`
- `docs/HOOK_ORCHESTRATION_DESIGN.md`
- `docs/RESOURCE_ORCHESTRATION_KERNEL.md`
- `docs/OPPORTUNITY_SCORECARD.md`

## 0. Resource activation purpose — LOCKED

The system does not exist merely to find a product to sell.

Its highest-level commercial purpose is:

> **discover underused, overlooked, fragmented, stranded or misallocated resources/capabilities; identify real unmet deficits; then design transparent, accepted and repeatable exchanges that let surplus and shortage create value for each other.**

The system searches both sides:

```text
VERIFIED NEED / DEFICIT
+
VERIFIED SURPLUS / UNDERUSED RESOURCE
+
OBSERVED TRANSACTION BLOCKER
→ BOUNDED RESOURCE-ACTIVATION ROUTE
→ REAL-WORLD TEST
→ ACCEPTED VALUE / SETTLEMENT
→ REPEAT / LEARNING / BETTER ALLOCATION
```

Large population, broad demand, market growth or idle capacity alone is not an opportunity.

Resource state must remain explicit:

```text
HYPOTHETICAL
DISCOVERED
OPTIONED
OWNED
```

Underuse is a separate axis:

```text
UNKNOWN
CLAIMED
OBSERVED
MEASURED
```

Therefore:

```text
resource exists != resource is spare
resource is spare != provider will supply it
DISCOVERED != OPTIONED
```

## 1. System identity — LOCKED

The project is an **Actor-First Regenerative Resource Orchestration Engine** with two distinct halves.

```text
DISCOVERY ENGINE
Data Sources
→ Macro
→ Money Flow
→ Market / Industry
→ Actor
→ Psychology / Behavior
→ Case Mining
→ Need / Resource / Blocker Signals
→ Resource Imbalance
→ Comparable Candidate Pool
→ G0-G6 Ranking

ORCHESTRATION ENGINE
Selected Route-Testable Candidate
→ Hook
→ Transaction Objective
→ CapabilityUnits
→ Resource Routing
→ Incentives / Trust / Acceptance
→ Execution / Settlement
→ Repeat / Learning
```

The discovery half must run before a business opportunity becomes canonical. The orchestration half captures a selected opportunity without turning the operator into the permanent salesperson or provider.

## 2. Discovery truth — LOCKED

Do not start from the operator's skills, a favored technology, an old launch document or one remembered idea.

Start from:
- GDP / sector structure;
- CPI / core CPI / service CPI;
- PPI / PMI / industrial production;
- household income/expenditure;
- retail / service retail / online consumption;
- employment / hiring;
- fixed investment / equipment investment;
- money / credit / deposits / loans where useful;
- imports / exports / cross-region flows;
- demographics / aging / households;
- policy / procurement;
- technology change;
- local industry/service-chain change;
- psychology and actual behavior;
- observable idle/underused skills, assets, channels and capacity.

Then zoom:

```text
China
→ Jiangsu
→ Xuzhou
→ district/county/industry/actor cluster
→ exact need/resource/blocker
→ exact payer
→ exact transaction route
```

Macro growth is search-direction evidence, not business proof.

## 3. Data-source truth — LOCKED

Opportunity discovery must not depend on ad-hoc web searching alone.

Maintain `data/source_registry.csv` with source identity, geography, indicator scope, observation/publication period, access method, refresh cadence, automation/terms status, provenance and freshness.

Missing/stale data reduces confidence. `missing != zero`.

Prefer lawful free/open/official data for the MVP. Paid connectors are not required merely to make the system look complete.

## 4. Money-flow truth — LOCKED

Ask:

> **Where is money moving from, where is it moving to, who pays, who receives, and what changed work/behavior does that movement create?**

Track levels, growth, acceleration, share shifts, national/provincial/local divergence, price vs volume, policy effects and receiving/losing actors.

`nominal_growth != real_demand_growth`.

A public procurement budget is evidence of an intended bounded purchase process. It is not automatically evidence of completed payment, supply scarcity, private-market demand or orchestration margin.

## 5. Psychology / behavior truth — LOCKED

Psychology changes and must be tracked, but:

`social-media salience != population share`.

Track aggregate themes such as value-for-money, spending caution, convenience/time value, trust/risk aversion, experience orientation, selective quality upgrading, repair/reuse/rental, emotional value, health/longevity and outcome certainty.

Any psychology thesis should be corroborated by observed behavior and money where possible. Do not build unnecessary individual psychographic profiles.

Cycle 001 has already produced a usable baseline psychology/behavior snapshot. The next job is recurring refresh and better local signal coverage, not pretending the first snapshot is permanent truth.

## 6. Case-mining truth — LOCKED

Continuously mine success and failure mechanisms:

```text
context change
→ actor behavior change
→ friction / resource imbalance
→ opportunity insight
→ first hook
→ first payer commitment
→ resource stack
→ acceptance/economics
→ repeat loop
→ failure/bypass/moat
→ reusable mechanism
```

`success story != base rate`.

## 7. Resource Imbalance truth — LOCKED

Before calling something an opportunity, separately prove:

```text
VERIFIED NEED / DEFICIT
+
VERIFIED RESOURCE / SURPLUS
+
OBSERVED TRANSACTION BLOCKER
```

Canonical V1 states:

```text
NEED_ONLY
RESOURCE_ONLY
PAIR_HYPOTHESIS
ROUTE_TESTABLE
```

`ROUTE_TESTABLE` requires at minimum:
- direct paid need evidence;
- identified payer;
- compatible resource at least `DISCOVERED`;
- resource underuse at least `OBSERVED`;
- transaction blocker at least `OBSERVED`;
- exact capability identity;
- exact geography identity.

`ROUTE_TESTABLE` means only that a cheap bounded route test is justified. It does not mean transaction-ready, profitable, scalable or G0-G6 approved.

Hard boundaries:

```text
Paid Need != Resource Imbalance
Resource Exists != Resource Is Underused
Relisting != Underuse
Relisting != Proven Blocker Type
Transaction-Scoped Blocker != Capability-Wide Blocker
Project ID Match != Package Scope Match
Budget != Completed Payment
DISCOVERED != OPTIONED
UNKNOWN != PASS
```

A blocker observed inside one bounded transaction or procurement event must stay scoped to that exact Need unless the source independently proves that the same blocker exists at the wider capability/geography market level. Capability and geography equality alone are not sufficient evidence to reuse a transaction-scoped blocker across Needs.

For procurement lifecycle evidence, matching `project_id` is necessary but not sufficient when the project contains multiple procurement packages. Package-specific settlement cannot promote a project-level Need. Missing package scope is `UNKNOWN`, not evidence of whole-project settlement. Whole-project promotion requires explicit source evidence that the settlement covers the project as a whole or all procurement packages.

## 8. Live evidence normalization truth — LOCKED

The current production objective is to connect live source adapters to the Resource Imbalance Engine without semantic invention.

Live normalization rules:
- use narrow, auditable capability classification;
- ambiguous or unclassified evidence stays unbound;
- do not use LLM confidence to manufacture a capability identity;
- do not infer payer from beneficiary, project title or budget holder language without source evidence;
- do not promote a procurement budget into `PAID` merely because money is quoted;
- do not turn repeated asset listing into an observed blocker without evidence of the blocker type;
- bind source-specific transaction blockers to the exact need/transaction identity; capability and geography equality alone are insufficient;
- for explicitly multi-package procurement, preserve package scope through lifecycle evidence; package-specific or package-unresolved settlement must not promote a project-level Need;
- preserve the source item and the reason it did not promote.

The unified live imbalance ledger should therefore show not only promoted pairs, but also why evidence remained `NEED_ONLY`, `RESOURCE_ONLY`, `PAIR_HYPOTHESIS` or unbound.

## 9. Hook truth — LOCKED

Do not enter negotiation with only an idea and a request for cooperation.

A credible Hook may be:
- pre-aggregated demand;
- optioned/qualified supply;
- verified information;
- measurable result/pilot;
- trusted distribution/channel access;
- optioned idle capacity/resource;
- transparent conditional economics.

Never represent a discovered/hypothetical resource as controlled.

## 10. Capital-light truth — LOCKED

Prefer transparent resource leverage over irreversible capital:
- conditional provider commitment;
- pay after accepted output;
- revenue share;
- customer deposit/precommitment;
- existing idle capacity;
- partner-contributed resource;
- staged commitments.

This is not permission for false demand, deceptive promises or hidden liabilities.

## 11. Execution truth — LOCKED

The atomic execution unit is a `CapabilityUnit`, not a person/job title.

The operator preferentially owns systems analysis, structural judgment, actor/resource mapping, Hook design, transaction architecture, capability decomposition, acceptance/interface design, incentive design, route approval, trust/risk boundaries, exception arbitration and learning updates.

Routine acquisition, sourcing, coding, research, delivery, QA, support and logistics are routable capabilities where feasible.

## 12. Sustainability truth — LOCKED

A core project must behave like a circulation system:

```text
Demand Pump
→ repeated task/order events
→ reusable transaction/capability templates
→ replenishing/replaceable supply
→ accepted outcomes
→ settlement
→ performance/trust data
→ better routing / lower future failure cost
→ more transactions
↺
```

A profitable one-off can be tactical but cannot define the core system.

## 13. Hard gates — LOCKED

```text
G0 Actor / role clarity
G1 Payer clarity
G2 Transactionability
G3 Legal / trust / safety
G4 Capability decomposability / delegatability
G5 Orchestration value
G6 Regenerative circulation / recurring demand
```

G4-G6 must all PASS before a candidate becomes a core repeatable platform wedge.

## 14. Evidence maturity — LOCKED

```text
L0 statement
L1 observed behavior/workaround
L2 exact terms accepted verbally
L3 real commitment/deposit/signed task
L4 completed accepted transaction + settlement
L5 repeat/referral
L6 delegated repeat/provider replacement/alternate route
L7 recurring Demand Pump produces multiple transactions and routing improves
```

## 15. Commercial truth rules — LOCKED

```text
Complaint != Demand
Demand != Willingness to Pay
Trend != Business
Growth != Money-Flow Understanding
Market Size != Customer Acquisition
Social Salience != Population Share
Success Story != Base Rate
Idle Resource != Valuable Resource
Resource Existence != Resource Control
Introduction != Orchestration Value
Founder Free Labor != Profit
Capability Claim != Capability Proof
One Provider != Replaceable Supply
One Transaction != Repeatability
One Customer != Demand Pump
Recurring Sales Effort != Regenerative Demand
LLM Confidence != Commercial Evidence
UNKNOWN != PASS
```

## 16. Discovery Cycle 001 — HISTORICAL BASELINE, COMPLETE

Cycle 001 ran a clean-slate public-web discovery pass across China → Jiangsu → Xuzhou and produced:
- expanded source registry;
- money-flow snapshot;
- psychology/behavior snapshot;
- success/failure mechanism library;
- 38 opportunity seeds;
- comparable G0-G6 ranking;
- historical launch designs.

Canonical historical outputs:
- `docs/research/DISCOVERY_CYCLE_001_MONEY_FLOW_2026-09-10.md`
- `docs/research/DISCOVERY_CYCLE_001_PSYCHOLOGY_BEHAVIOR_2026-09-10.md`
- `docs/research/DISCOVERY_CYCLE_001_CASE_MECHANISMS_2026-09-10.md`
- `docs/research/DISCOVERY_CYCLE_001_OPPORTUNITY_POOL_2026-09-10.md`
- `docs/results/DISCOVERY_CYCLE_001_RANKING_2026-09-10.md`

The Cycle 001 scores remain useful historical evidence. They are **not current success probabilities and no longer establish a canonical winner** after the Resource Imbalance reset.

## 17. Current project state — CANONICAL

**There is currently no canonical #1 business project.**

Property-Anchored Community Living-Service Orchestration Backend, Industrial Service Overflow Routing Network, stock-home turnover, export operations, procurement support, visitor/merchant routing, machinery aftermarket and every other historical candidate are all evidence/candidate records only.

No candidate receives first-found privilege or survives merely because a launch document, Issue or prior score exists.

A candidate may become current #1 only after a fresh comparable cycle based on the current evidence discipline:

```text
live need evidence
+ live resource/underuse evidence
+ observed blocker evidence
→ Resource Imbalance classification
→ evidence-backed candidate pool
→ same G0-G6 comparison
→ selected Hook
→ cheapest decisive real-world test
```

## 18. Current production evidence — 2026-09-11

Working live evidence paths already include national/Jiangsu/Xuzhou money-flow sources, Xuzhou public procurement, regional financing evidence and public resource-underuse sensors.

Resource-underuse Sensor 001 has verified that Xuzhou/Jiangsu official public-resource sources can expose:
- discovered public assets;
- repeated listings / allocation friction;
- explicit `空置/闲置` evidence in some historical records;
- repricing across repeated listings.

These facts prove resource/underuse evidence only within their exact scope. They do not prove compatible paid demand or a profitable route.

The decisive engineering gap is now **integration**, not invention of another high-level framework:

```text
LIVE SOURCE ARTIFACTS
→ canonical NeedSignal / ResourceSignal / BlockerSignal
→ unified Resource Imbalance ledger
→ explainable promotion / non-promotion
→ fresh comparable opportunity ranking
```

## 19. Current next actions — CANONICAL

Engineering priority:
1. keep live money-flow and need sensors healthy;
2. expand observable resource-underuse history and source coverage;
3. normalize live evidence into canonical signal records;
4. build and publish a daily auditable imbalance ledger;
5. add blocker sensing only when blocker type/evidence is genuinely observed;
6. improve payer-resolved paid-need evidence rather than treating budgets as payments;
7. create a fresh broad candidate pool from the resulting imbalance evidence;
8. apply the same G0-G6 ranking;
9. select one strongest route-testable candidate and run the cheapest decisive real transaction test.

## 20. Software truth — LOCKED

Do not build ERP, MES, WMS, CRM or a broad marketplace because they are adjacent to an opportunity.

Discovery software is justified first where it removes repeated truth/research bottlenecks:
- source registry;
- normalized money-flow signals;
- psychology aggregation;
- case records;
- Need/Resource/Blocker signals;
- Resource Imbalance ledger;
- opportunity ranking.

Transaction software is justified only after repeated real transaction bottlenecks appear.

## 21. Governing truth — LOCKED

> **先把世界看清：维护数据源，追钱流，察人心，分别证明“谁缺、谁有余、为什么没成交”；任何一边靠想象补齐都只能停留在 UNKNOWN。只有当真实需要、真实闲置资源和真实阻塞点能在同一能力与地域上对齐，才允许进入低成本现实验证；再定结果、拆能力、调资源、设利益，让交换形成可持续循环。**
