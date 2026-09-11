# Opportunity Routing Engine

A validation-first **Actor-First Regenerative Resource Activation & Orchestration Engine**.

The system exists to discover **real deficits, underused resources and the blockers that prevent them from creating value together**, then design bounded, transparent transaction routes that can be tested in reality.

It is deliberately split into two engines:

```text
DISCOVERY ENGINE
Data Sources
→ Macro Regime
→ Money Flow
→ Market / Industry Movement
→ Actor Segments
→ Psychology / Behavior
→ Success + Failure Case Mining
→ Need / Resource / Blocker Signals
→ Resource Imbalance Engine
→ Evidence-backed Candidate Pool
→ Comparable G0-G6 Ranking

ORCHESTRATION ENGINE
Selected Route-Testable Candidate
→ Hook Design
→ Transaction Objective
→ CapabilityUnit Decomposition
→ Resource Routing
→ Incentives / Trust / Acceptance
→ Execution / Settlement
→ Repeat / Learning
```

The Discovery Engine decides **where verified surplus and deficit may be failing to meet**. The Orchestration Engine decides **how to test and, only if reality supports it, repeatedly route resources without turning the operator into the permanent salesperson or worker**.

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
- `docs/FORMAL_TRUTH.md`

## 1. Core identity

Do not begin with a product, a favored vertical, an ERP/MES project, or what the operator personally knows how to sell.

Begin with reality:

> **Where is money, time, attention, risk or capacity moving; who lacks something valuable; who has a compatible resource that is genuinely underused; why are they not already transacting; and can that blocker be reduced without large irreversible capital?**

The deepest system objective is:

```text
VERIFIED DEFICIT / NEED
+
VERIFIED SURPLUS / UNDERUSED RESOURCE
+
OBSERVED TRANSACTION BLOCKER
→ BOUNDED RESOURCE-ACTIVATION ROUTE
→ REAL-WORLD TEST
→ ACCEPTED VALUE / SETTLEMENT
→ REPEAT / LEARNING / BETTER ALLOCATION
```

The operator is the initial **systems analyst / transaction architect / resource orchestrator**. The operator preferentially owns structural judgment, actor/resource mapping, Hook design, capability decomposition, acceptance/incentive design, route approval, risk boundaries and learning. Routine acquisition, research, delivery, coding, QA, logistics and support are themselves routable capabilities when reality justifies routing them.

## 2. Resource truth

A resource may be human skill/time, professional capability, a trusted channel, physical space/equipment/vehicles, inventory, local knowledge, data, software/AI capability, institutional access, logistics capacity, reputation/trust, demand aggregation, capital, or a reusable process/acceptance standard.

Resource state must always be explicit:

```text
HYPOTHETICAL — inferred only
DISCOVERED   — existence verified, no control/use commitment
OPTIONED     — provider explicitly agrees under stated conditions
OWNED        — controlled now
```

Underuse is a separate question:

```text
UNKNOWN / CLAIMED / OBSERVED / MEASURED
```

Therefore:

```text
resource exists != resource is spare
resource is spare != provider will supply it
DISCOVERED != OPTIONED
```

The system must not exploit weak actors by hiding economics, shifting unreasonable risk, or suppressing fair compensation. A structurally good route should create incremental value for payer, provider/resource owner and orchestrator.

## 3. Continuous data-source layer

Maintain recurring sources rather than depend on ad-hoc searches.

Current live evidence paths include:
- `CN_NBS` — National Bureau of Statistics / 国家数据 public-release API;
- `JS_STATS` — Jiangsu Statistics official releases;
- `XZ_GGZY` — Xuzhou public procurement notices.

The broader registry also tracks national finance/trade/employment sources, Jiangsu/Xuzhou government sources, public case sources, and planned authorized aggregate social/search sources.

Seed registry: `data/source_registry.csv`.

Every source must preserve geography, observation/publication period, units/denominator, access mode, freshness and provenance. Missing/stale data reduces confidence; missing does not become zero.

## 4. Money Flow Engine

Do not rank industries by growth alone.

Detect:

```text
WHO PAYS MORE / LESS
→ WHO RECEIVES MORE / LESS
→ CATEGORY SHARE SHIFT
→ PRICE VS VOLUME
→ POLICY VS INDEPENDENT DEMAND
→ ACCELERATION / DECELERATION
→ CHINA / JIANGSU / XUZHOU DIVERGENCE
→ ACTOR BEHAVIOR CHANGE
→ FRICTION / NEED
```

Divergence is often more useful than raw growth.

A government procurement event is strong evidence that an institution is paying for a bounded task. It is **not** automatic evidence of local supply scarcity, private-market demand or orchestration margin.

## 5. Psychology & Behavior Tracker

Track aggregate psychology/behavior signals such as value-for-money, spending caution, convenience/time value, trust/risk aversion, experience orientation, selective upgrading, repair/reuse/rental, emotional value and outcome certainty.

**Social-media salience is not population share.** Prefer public/authorized aggregate signals and corroborate psychology with real behavior/money.

## 6. Case Mining Engine

Study successful **and failed** cases. Do not copy products; extract mechanisms:

```text
context change
→ behavior change
→ friction
→ first Hook
→ payer
→ controlled / optioned resources
→ acceptance/economics
→ repeat loop
→ failure/bypass
→ reusable mechanism
```

`success story != base rate`.

## 7. Resource Imbalance Engine

The system must separately prove three sides:

```text
NEED SIGNAL
+
RESOURCE SIGNAL
+
BLOCKER SIGNAL
```

V1 emits only:

```text
NEED_ONLY
RESOURCE_ONLY
PAIR_HYPOTHESIS
ROUTE_TESTABLE
```

`ROUTE_TESTABLE` requires, at minimum:
- direct paid need evidence;
- identified payer;
- compatible resource at least `DISCOVERED`;
- underuse at least `OBSERVED`;
- transaction blocker at least `OBSERVED`;
- exact V1 capability and geography identity.

It means only that a cheap bounded route test is justified. It does not mean transaction-ready, profitable, scalable or G0-G6 approved.

## 8. Hook before outreach

The orchestrator should not contact actors empty-handed with `do you have work?`.

A Hook may be:
- pre-aggregated demand;
- optioned/qualified supply;
- verified information;
- measurable result/pilot;
- trusted distribution access;
- optioned idle resource;
- transparent conditional economics.

The Hook should convert uncertainty into a cheap, falsifiable transaction test.

## 9. Capital-light first principle

Before irreversible capital ask:

```text
Can payer pre-commit?
Can provider payout follow acceptance?
Can idle capacity be activated?
Can a partner contribute resources for revenue share?
Can each conditional commitment unlock the next resource?
```

This is transparent resource leverage, not deceptive promises or hidden liabilities.

## 10. CapabilityUnit

The atomic execution unit is a contractible capability with explicit input, output, acceptance, provider class, price/payout, SLA, trust/safety, replacement and failure rules.

A person, company, AI model, institution, asset or channel may provide one or many CapabilityUnits.

For human-capital activation, prefer:

```text
JOB TITLE → CAPABILITY UNIT
CV CLAIM   → PROOF / ACCEPTANCE
IDLE TIME  → CONDITIONAL CAPACITY
NO ACCESS  → TRUSTED DEMAND ROUTE
```

## 11. Regenerative circulation

The target is not a sequence of unrelated gigs.

```text
DEMAND PUMP
→ REPEATED TASK / ORDER EVENTS
→ REUSABLE TEMPLATES
→ REPLENISHING / REPLACEABLE SUPPLY
→ ACCEPTED OUTCOMES
→ SETTLEMENT
→ PERFORMANCE / TRUST DATA
→ BETTER ROUTING + LOWER FAILURE COST
→ MORE TRANSACTIONS
↺
```

## 12. Hard gates

```text
G0 Actor / role clarity
G1 Payer clarity
G2 Transactionability
G3 Legal / trust / safety
G4 Capability decomposability / delegatability
G5 Orchestration value
G6 Regenerative circulation / recurring demand
```

Scores never override failed/unknown truth gates. G4–G6 must all PASS before an opportunity becomes a core repeatable orchestration wedge.

## 13. Current project state

The repository is currently in **continuous discovery-stack construction and evidence collection**.

Completed/working foundations include:
- canonical Resource Activation Thesis;
- source registry and evidence/provenance rules;
- national NBS live ingestion with publication-lag handling;
- Jiangsu official-release ingestion;
- Xuzhou public-procurement ingestion;
- psychology/behavior evidence model;
- success/failure case-mining methodology;
- G0-G6 opportunity ranking discipline;
- Resource Imbalance Engine V1 under active integration.

The decisive missing evidence layer is now **resource-underuse sensing**: finding real, observable spare capabilities/assets and measuring why they are not already reaching paid demand.

Until the discovery stack produces a new comparable ranking from both deficit and surplus evidence, **no candidate is the canonical #1 project**.

## 14. Historical candidate status

Earlier discovery work ranked `Property-Anchored Community Living-Service Orchestration Backend` as a structural candidate and produced a launch design. That result remains useful historical evidence, but it is **not the current canonical #1** and must not receive first-found privilege.

Likewise, industrial overflow, youth micro-experience, skills-to-income, pet-care and other experiments remain evidence/candidate records rather than automatic current priorities.

They may re-enter only through the same current Resource Imbalance + G0-G6 comparison process.

## 15. Commercial discipline

```text
Complaint != Demand
Demand != Willingness to Pay
Trend != Business
Growth != Money-Flow Understanding
Paid Need != Resource Imbalance
Resource Exists != Resource Is Underused
DISCOVERED != OPTIONED
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

## 16. Software discipline

Do not build ERP/MES/CRM/marketplace infrastructure before real transaction density requires it.

Continue engineering the sensing/evidence stack only where automation removes a repeated discovery bottleneck. Automate transaction operations only after real repeated bottlenecks appear.

## Governing invariant

> **先把世界看清：找到真实的不足，找到真实的有余，证明为什么它们没有成交；再用一个真实钩子进入市场，定结果、拆能力、调资源、设利益，让交换形成可持续循环。任何一边靠想象补齐，都只能停留在 UNKNOWN。**
