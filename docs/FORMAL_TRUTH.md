# Formal Truth

Last updated: 2026-09-10

This document is the current commercial source of truth.

Canonical foundations:
- `docs/DATA_SOURCE_REGISTRY.md`
- `docs/DISCOVERY_ENGINE.md`
- `docs/MONEY_FLOW_ENGINE.md`
- `docs/PSYCHOLOGY_BEHAVIOR_TRACKER.md`
- `docs/CASE_MINING_ENGINE.md`
- `docs/HOOK_ORCHESTRATION_DESIGN.md`
- `docs/RESOURCE_ORCHESTRATION_KERNEL.md`
- `docs/OPPORTUNITY_SCORECARD.md`

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
→ Friction / Payer / Opportunity Pool
→ Comparable Ranking

ORCHESTRATION ENGINE
Selected Opportunity
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

Do not start from the operator's skills, a favored technology, or one remembered idea.

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
- psychology and actual behavior.

Then zoom:

```text
China
→ Jiangsu
→ Xuzhou
→ district/county/industry/actor cluster
→ exact friction
→ exact payer
```

Macro growth is a search direction, not business proof.

## 3. Data-source truth — LOCKED

Opportunity discovery must not depend on ad-hoc web searching alone.

Maintain `data/source_registry.csv` with:
- source identity;
- geography;
- indicator scope;
- observation/publication period;
- access method;
- refresh cadence;
- automation/terms status;
- provenance/freshness.

Missing/stale data reduces confidence. `missing != zero`.

## 4. Money-flow truth — LOCKED

Ask:

> **Where is money moving from, where is it moving to, who pays, who receives, and what changed work/behavior does that movement create?**

Track levels, growth, acceleration, share shifts, national/provincial/local divergence, price vs volume, policy effects and receiving/losing actors.

`nominal_growth != real_demand_growth`.

## 5. Psychology / behavior truth — LOCKED

Psychology changes and must be tracked, but:

`social-media salience != population share`.

Track aggregate themes such as value-for-money, spending caution, convenience/time value, trust/risk aversion, experience orientation, selective quality upgrading, repair/reuse/rental, emotional value, health/longevity and outcome certainty.

Any psychology thesis should be corroborated by observed behavior and money where possible. Do not build unnecessary individual psychographic profiles.

## 6. Case-mining truth — LOCKED

Continuously mine success and failure mechanisms:

```text
context change
→ actor behavior change
→ friction
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

## 7. Hook truth — LOCKED

Do not enter negotiation with only an idea and a request for cooperation.

A credible Hook may be:
- pre-aggregated demand;
- optioned/qualified supply;
- verified information;
- measurable result/pilot;
- trusted distribution/channel access;
- optioned idle capacity/resource;
- transparent conditional economics.

Resource state must be explicit:

```text
OWNED
OPTIONED
DISCOVERED
HYPOTHETICAL
```

Never represent a discovered/hypothetical resource as controlled.

## 8. Capital-light truth — LOCKED

Prefer transparent resource leverage over irreversible capital:
- conditional provider commitment;
- pay after accepted output;
- revenue share;
- customer deposit/precommitment;
- existing idle capacity;
- partner-contributed resource;
- staged commitments.

This is not permission for false demand, deceptive promises or hidden liabilities.

## 9. Execution truth — LOCKED

The atomic execution unit is a `CapabilityUnit`, not a person/job title.

The operator preferentially owns:
- systems analysis;
- structural judgment;
- actor/resource mapping;
- hook design;
- transaction architecture;
- capability decomposition;
- acceptance/interface design;
- incentive design;
- route approval;
- trust/risk boundaries;
- exception arbitration;
- learning updates.

Routine acquisition, sourcing, coding, research, delivery, QA, support and logistics are routable capabilities where feasible.

## 10. Sustainability truth — LOCKED

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

## 11. Hard gates — LOCKED

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

## 12. Evidence maturity

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

## 13. Commercial truth rules

```text
Complaint != Demand
Demand != Willingness to Pay
Trend != Business
Growth != Money-Flow Understanding
Market Size != Customer Acquisition
Social Salience != Population Share
Success Story != Base Rate
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

## 14. Discovery Cycle 001 — COMPLETE

Cycle 001 ran a clean-slate public-web discovery pass across China → Jiangsu → Xuzhou and produced:
- expanded source registry;
- money-flow snapshot;
- psychology/behavior snapshot;
- success/failure mechanism library;
- 38 opportunity seeds;
- comparable G0-G6 ranking;
- one selected first-validation candidate.

Canonical outputs:
- `docs/research/DISCOVERY_CYCLE_001_MONEY_FLOW_2026-09-10.md`
- `docs/research/DISCOVERY_CYCLE_001_PSYCHOLOGY_BEHAVIOR_2026-09-10.md`
- `docs/research/DISCOVERY_CYCLE_001_CASE_MECHANISMS_2026-09-10.md`
- `docs/research/DISCOVERY_CYCLE_001_OPPORTUNITY_POOL_2026-09-10.md`
- `docs/results/DISCOVERY_CYCLE_001_RANKING_2026-09-10.md`

The cycle is broad enough to remove first-found-candidate privilege. It is not the end of continuous discovery; source adapters and future refresh cycles remain required.

## 15. Current money-flow truth — Cycle 001

Current evidence supports a selective-migration regime, not `nobody spends`:
- services outperform broad goods retail nationally;
- Xuzhou retail/service/tourism growth is stronger than broad Jiangsu retail;
- households are value-sensitive but continue paying for experience, convenience and selective upgrading;
- equipment/information investment remains stronger than broad fixed investment;
- Xuzhou stock housing creates repair/turnover/service work;
- property firms seek resident-service/value-added extensions;
- engineering machinery is expanding lifecycle/aftermarket activity;
- public procurement exposes recurring institutional budgets;
- policy-subsidized flows must be separated from independent demand.

## 16. Current ranking — Cycle 001

Top adjusted structural candidates:

1. **Property-Anchored Community Living-Service Orchestration Backend — 75**
2. Stock-home turnover / repair / handover orchestration — 74
3. Cross-border seller/export recurring operations routing — 72
4. Public-procurement demand intelligence + qualified-supplier support — 71
5. High-intent visitor → local service/merchant orchestration — 70
6. OPC demand-access + delivery-governance route — 69
7. Used engineering-machinery trusted transaction support — 67
8. Engineering-machinery aftermarket routing — 65
9. County agricultural logistics/cold-chain routing — 65

These scores are **not success probabilities**.

## 17. Current selected first-validation candidate — CANONICAL FOR NEXT TEST

# Property-Anchored Community Living-Service Orchestration Backend

Chinese working name:

> **物业锚定的社区生活服务后台编排**

Why selected first:
- Xuzhou has 2,237 residential communities and 690+ property-service firms, giving a dense concentrated access layer;
- local property operators are already extending convenience/value-added services and face incentive to improve service economics/resident satisfaction;
- property can act as the resident-facing demand front door;
- delivery can be routed to external providers;
- bounded low-risk service tasks can be accepted objectively;
- provider capacity can be optioned without payroll/inventory;
- property can be approached with a zero-upfront backend proposition rather than a generic platform pitch;
- repeat household orders can test G6 without reacquiring each resident individually.

Launch design:
- `docs/launch/PROPERTY_ANCHORED_COMMUNITY_SERVICE_START_2026-09-10.md`

## 18. Current critical unknowns — DO NOT HIDE

The #1 candidate is not commercially validated.

### G1 UNKNOWN
Will real Xuzhou residents buy through a property-mediated service route at prices that support provider + operations + orchestration economics?

### G5 UNKNOWN
Will the orchestration backend add enough recurring value in qualification, SLA, acceptance, complaint/rework, replacement and settlement to prevent simple property-provider bypass?

### G6 UNKNOWN
Will one property/community repeatedly generate real paid orders without reacquiring the channel from zero?

If these fail, the candidate loses #1 status and the next ranked candidate advances.

## 19. First Hook — LOCKED FOR VALIDATION, NOT SCALE

Before asking a property to cooperate, obtain an `OPTIONED SUPPLY PACK` from 2–3 low-risk household-service categories.

Initial allowed examples:
- home deep cleaning;
- appliance cleaning;
- move-in/move-out cleaning.

The provider commitment should define price rule, service area, response time, scope/exclusions, completion evidence, rework rule, payout event and capacity — with no salary, no inventory and no guaranteed volume.

Then property hook:

> **Property pays zero upfront and hires no new staff. Real resident orders trigger service. The backend manages provider qualification/routing, SLA, acceptance, complaint/rework, replacement and settlement. Run a small real-order pilot first.**

Do not pitch an app/platform.

## 20. First validation threshold

Phase A — option supply:
- >=3 providers accept order-based conditional cooperation;
- >=2 categories have viable routes/backup;
- price/SLA/acceptance can be written clearly.

Phase B — property demand pump:
- 5 qualified property decision-makers;
- >=3 report repeated resident requests outside basic property scope;
- >=2 reveal existing workaround/referral/provider;
- >=1 authorizes a bounded real-resident pilot.

Phase C — payment:
- >=5 real paid resident orders in one pilot;
- external providers perform delivery;
- backend QA/acceptance/replacement function is actually exercised;
- all economics are recorded.

Phase D — G6:
- same property/community sends further orders without channel reacquisition;
- preferably provider replacement succeeds.

## 21. Explicitly paused / demoted candidate

`Industrial Service Overflow Routing Network` remains in the opportunity pool but is no longer canonical #1. Its old Issue #9 is paused/closed.

## 22. Software truth

Do not build ERP, MES, WMS, CRM or a broad marketplace because they are adjacent to an opportunity.

Discovery software is justified first:
- source registry;
- normalized money-flow signals;
- psychology aggregation;
- case records;
- opportunity ranking.

Transaction software is justified only after repeated real bottlenecks appear.

## 23. Governing truth — LOCKED

> **先把世界看清：维护数据源，追钱流，察人心，拆成功与失败案例，找到真实摩擦；再带着一个真实钩子进入市场，定结果、拆能力、调资源、设利益，让交易形成可持续循环。**
