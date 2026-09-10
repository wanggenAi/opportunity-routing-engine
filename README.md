# Opportunity Routing Engine

A validation-first **Actor-First Regenerative Resource Orchestration Engine**.

The system is deliberately split into two engines:

```text
DISCOVERY ENGINE
Data Sources
→ Macro Regime
→ Money Flow
→ Market / Industry Movement
→ Actor Segments
→ Psychology / Behavior
→ Case Mining
→ Friction / Payer / Opportunity

ORCHESTRATION ENGINE
Opportunity Evaluation
→ Hook Design
→ Transaction Objective
→ CapabilityUnit Decomposition
→ Resource Routing
→ Incentives / Trust / Acceptance
→ Execution / Settlement
→ Repeat / Learning
```

The discovery engine decides **where to look and what may be worth doing**.
The orchestration engine decides **how to capture the opportunity without turning the operator into the permanent salesperson or worker**.

Canonical foundations:
- `docs/DATA_SOURCE_REGISTRY.md`
- `docs/DISCOVERY_ENGINE.md`
- `docs/MONEY_FLOW_ENGINE.md`
- `docs/PSYCHOLOGY_BEHAVIOR_TRACKER.md`
- `docs/CASE_MINING_ENGINE.md`
- `docs/HOOK_ORCHESTRATION_DESIGN.md`
- `docs/RESOURCE_ORCHESTRATION_KERNEL.md`
- `docs/OPPORTUNITY_SCORECARD.md`
- `docs/FORMAL_TRUTH.md`

## 1. Core identity

Do not begin with a product, a favored vertical, an ERP/MES project, or what the operator personally knows how to sell.

Begin with reality:

> **Where is money, time, attention, risk or capacity moving; which actors are changing behavior; what friction is created; and who has economic reason to pay to remove it?**

Only after a credible opportunity is discovered does the system ask how to organize resources around it.

The operator is the initial **systems analyst / transaction architect / resource orchestrator**. The operator preferentially owns:
- structural judgment;
- opportunity evaluation;
- actor/resource mapping;
- hook design;
- capability decomposition;
- interface and acceptance design;
- incentive design;
- route approval;
- risk/trust boundaries;
- exception arbitration;
- learning-system updates.

Routine acquisition, coding, research, delivery, QA, logistics and support are capabilities that may be delegated or safely automated.

## 2. Continuous data-source layer

The engine must maintain recurring sources rather than depend on ad-hoc web searches.

Initial sources include:
- National Bureau of Statistics / 国家数据;
- Ministry of Commerce / 商务数据中心 / 商务预报;
- People's Bank of China;
- General Administration of Customs;
- Ministry of Human Resources and Social Security;
- Jiangsu statistical/economic-operation sources;
- Xuzhou statistical/government sources;
- Xuzhou public-resource transaction data;
- authorized/public market, company, hiring, platform and behavioral signals.

Every source must preserve geography, observation period, publication date, units, denominator, revision state and provenance.

Seed registry: `data/source_registry.csv`.

## 3. Money Flow Engine

The system should not merely rank industries by growth.

It should detect:

```text
WHO PAYS MORE / LESS
→ WHO RECEIVES MORE / LESS
→ WHICH CATEGORY GAINS / LOSES SHARE
→ PRICE VS VOLUME
→ POLICY VS INDEPENDENT DEMAND
→ ACCELERATION / DECELERATION
→ NATIONAL / JIANGSU / XUZHOU DIVERGENCE
→ ACTOR BEHAVIOR CHANGE
→ NEW FRICTION
```

Divergences are particularly valuable:
- services rising faster than goods;
- online rising faster than offline;
- county/rural growth differing from urban;
- equipment investment rising while broad investment weakens;
- repair/rental rising while new durable purchases weaken;
- demand/orders rising while delivery capacity lags.

Schema: `data/money_flow_signal_template.csv`.

## 4. Psychology & Behavior Tracker

Human decision psychology changes, but social-media salience is not population share.

Track:
- signal salience;
- momentum;
- behavioral corroboration;
- money-flow corroboration;
- geography / actor segment;
- representative survey share only when sampling supports it.

Prefer aggregate/public/authorized signals. Do not build unnecessary individual psychographic profiles.

## 5. Case Mining Engine

The engine must study successful **and failed** cases.

Do not copy products. Extract mechanisms:

```text
what changed
→ what actor behavior changed
→ what friction was noticed
→ what first hook opened the door
→ who paid
→ what resources were controlled / borrowed / partnered
→ how acceptance worked
→ how economics worked
→ whether demand repeated
→ why competitors failed or bypass occurred
```

Case mining must include survivorship-bias controls.

## 6. Opportunity discovery

Only after the sensing layers produce evidence should the engine promote opportunity candidates.

Canonical funnel:

```text
MACRO
→ MONEY FLOW
→ MARKET
→ ACTOR
→ PSYCHOLOGY / BEHAVIOR
→ CASE MECHANISM
→ FRICTION
→ DESIRED OUTCOME
→ PAYER
→ TRANSACTION GAP
→ ORCHESTRATION FIT
```

Macro growth is a search direction, not business proof.

## 7. Hook before outreach

The orchestrator should not contact actors empty-handed with `do you have work?`.

Before targeted outreach define a `Hook`:
- demand evidence;
- pre-qualified capability;
- verified information;
- measurable outcome/pilot;
- distribution access;
- idle-resource access;
- transparent capital structure such as deposit, milestone, success fee or revenue share.

Resource states must be honest:
- `OWNED`;
- `OPTIONED`;
- `DISCOVERED`;
- `HYPOTHETICAL`.

Never present discovered/hypothetical resources as already controlled.

## 8. Capital-light first principle

The initial system should minimize irreversible capital before payer proof.

Ask:

```text
Can payer pre-commit?
Can a deposit fund execution?
Can provider payout follow acceptance?
Can idle capacity reduce marginal cost?
Can a partner contribute resources for revenue share?
Can each commitment unlock the next resource?
```

This is transparent resource leverage, not deceptive `free money` or hidden liability.

## 9. CapabilityUnit

The atomic execution unit is a contractible capability:

```text
purpose
input
required output
acceptance criteria
provider class
proof required
price / payout condition
SLA
dependencies
trust / safety requirements
replacement rule
failure / refund rule
```

A person, company, AI model, institution, asset or channel may provide one or many CapabilityUnits.

## 10. Regenerative circulation

The target is not a sequence of unrelated gigs.

A core opportunity should support:

```text
RECURRING DEMAND SOURCE / DEMAND PUMP
→ REPEATED TASK EVENTS
→ REUSABLE TRANSACTION / CAPABILITY TEMPLATES
→ REPLENISHING / REPLACEABLE SUPPLY
→ ACCEPTED OUTCOMES
→ SETTLEMENT
→ PERFORMANCE / TRUST DATA
→ LOWER COST + BETTER ROUTING
→ MORE DEMAND / BETTER SUPPLY
↺
```

## 11. Hard gates

```text
G0 Actor / role clarity
G1 Payer clarity
G2 Transactionability
G3 Legal / trust / safety
G4 Capability decomposability / delegatability
G5 Orchestration value
G6 Regenerative circulation / recurring demand
```

G4–G6 must all PASS before an opportunity becomes a core repeatable platform wedge.

## 12. Current phase — DISCOVERY STACK REBUILD

As of 2026-09-10, **no business opportunity is canonical #1**.

The prior provisional `Industrial Service Overflow Routing Network` has been demoted back to a candidate and its validation issue paused because the system moved to execution before the continuous discovery stack was complete.

Current priority:

```text
1. maintain data-source registry
2. generate normalized macro / money-flow signals
3. track psychology / behavior
4. mine successful + failed mechanisms
5. produce a broad Xuzhou/Jiangsu opportunity pool
6. score the pool using G0-G6
7. only then choose the strongest project
8. design a targeted Hook before outreach
9. validate with minimal capital
```

No candidate should become #1 because it was researched first.

## 13. Commercial discipline

```text
Complaint != Demand
Demand != Willingness to Pay
Trend != Business
Growth != Money-Flow Understanding
Social Salience != Population Share
Success Story != Base Rate
Market Size != Customer Acquisition
Introduction != Orchestration Value
Founder Free Labor != Profit
Capability Claim != Capability Proof
One Customer != Demand Pump
One Transaction != Repeatability
LLM Confidence != Commercial Evidence
UNKNOWN != PASS
```

## 14. Software discipline

Do not build ERP/MES/CRM/marketplace infrastructure before real transaction density requires it.

Build only the lightweight discovery infrastructure needed to maintain evidence and compare opportunities. Automate further only when a repeated bottleneck is proven.

## Governing invariant

> **先把世界看清：维护数据源，追钱流，察人心，拆成功与失败案例，找到真实摩擦；再带着一个真实钩子进入市场，定结果、拆能力、调资源、设利益，让交易形成可持续循环。**
