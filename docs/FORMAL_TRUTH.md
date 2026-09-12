# Formal Truth

Last updated: 2026-09-12

This document is the current commercial source of truth. Historical rankings and launch designs remain evidence, but they do not override the current truth stated here.

Canonical foundations, in precedence order:
- `docs/LATENT_VALUE_DOCTRINE.md`
- `docs/ACCESS_FEASIBILITY_GATE.md`
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

`docs/LATENT_VALUE_DOCTRINE.md` is constitutional. Lower-level models, source adapters, current candidates and implementation convenience cannot override it.

## 0. Latent-value purpose — LOCKED

The system does not exist merely to find a product, explicit demand, supplier, lead or already-visible transaction.

Its highest-level commercial purpose is:

> **observe actors and reality deeply enough to discover value that is idle, hidden, fragmented, mispriced, misallocated, uncombined or not yet recognized by the actors themselves; identify complementary actor structures; prove what is real; then design transparent, accepted and repeatable exchanges that allow that value to circulate.**

The system does not begin from a permanent `DEMAND SIDE -> SUPPLY SIDE` split.

Every actor may simultaneously contain:
- resources;
- deficits;
- capabilities;
- underuse;
- trust;
- access;
- demand flow;
- information;
- relationships;
- latent value that appears only in combination with another actor.

The highest-order discovery model is:

```text
ACTOR
→ ENDOWMENT / STATE
→ CHANGE
→ BEHAVIOR
→ FRICTION / UNDERUSE / MISALLOCATION
→ LATENT_VALUE_HYPOTHESIS
→ COMPLEMENTARY_ACTOR
→ EXCHANGE_HYPOTHESIS
→ BLOCKER
→ EVIDENCE
→ BOUNDED VALIDATION
→ ACCEPTED VALUE / SETTLEMENT
→ REPEAT / LEARNING / BETTER ALLOCATION
```

`NeedSignal`, `ResourceSignal` and `BlockerSignal` are evidence projections inside this larger model. They do not define the whole ontology.

The engine must **discover boldly and promote conservatively**.

Hypothesis generation may be broad. Canonical promotion remains fail-closed and evidence-bound.

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
Potential Value != Proven Value
Latent Value Hypothesis != Verified Resource
resource exists != resource is spare
resource is spare != provider will supply it
DISCOVERED != OPTIONED
Complementarity != Transactionability
UNKNOWN != PASS
```

## 1. System identity — LOCKED

The project is an **Actor-First Regenerative Latent-Value Orchestration Engine** with two distinct halves.

```text
DISCOVERY ENGINE
Data Sources
→ Macro / Money Flow / Market Structure
→ Actor
→ Endowment / State / Change
→ Psychology / Behavior
→ Friction / Underuse / Misallocation
→ Latent Value Hypothesis
→ Complementary Actor Search
→ Need / Resource / Blocker Evidence Projections
→ Resource Imbalance / Exchange Hypothesis
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
→ Repeat / Learning / Better Allocation
```

The discovery half must run before a business opportunity becomes canonical. The orchestration half captures a selected opportunity without turning the operator into the permanent salesperson or provider.

A source adapter is an observer, not the strategy.
A data field is an observation, not the ontology.
A procurement feed is one sensor, not the business model.
A current candidate is a sample, not the identity of the engine.

## 2. Discovery truth — LOCKED

Do not start from the operator's skills, a favored technology, an old launch document, one remembered idea, a supplier catalog or an explicit demand feed.

Start from broad reality:
- GDP / sector structure;
- CPI / core CPI / service CPI;
- PPI / PMI / industrial production;
- household income/expenditure;
- retail / service retail / online consumption;
- employment / hiring / layoffs / project cycles;
- fixed investment / equipment investment;
- money / credit / deposits / loans where useful;
- imports / exports / cross-region flows;
- demographics / aging / households;
- policy / procurement;
- technology change;
- local industry/service-chain change;
- psychology and actual behavior;
- repeated manual work and workarounds;
- idle/underused skills, assets, channels and capacity;
- low utilization, repeated repricing, excess inventory and stranded assets;
- relationships, trust, reputation, distribution and installed-base resources;
- fragmented resources or demand that become valuable only after aggregation;
- combinations whose value is not visible when each actor is viewed alone.

Then zoom:

```text
China
→ Jiangsu
→ Xuzhou
→ district/county/industry/actor cluster
→ actor endowment/state/change
→ observed friction/underuse/misalallocation
→ latent value hypothesis
→ complementary actor
→ exact need/resource/blocker evidence
→ exact payer
→ exact transaction route
```

The engine must search for **what actors may not know about themselves**: hidden capability, hidden deficit, underused relationships, packaging gaps, coordination gaps and unrealized exchange structures.

Macro growth is search-direction evidence, not business proof.

## 3. Data-source truth — LOCKED

Opportunity discovery must not depend on ad-hoc web searching alone.

Maintain `data/source_registry.csv` with source identity, geography, indicator scope, observation/publication period, access method, refresh cadence, automation/terms status, provenance and freshness.

Missing/stale data reduces confidence. `missing != zero`.

Prefer lawful free/open/official data for the MVP. Paid connectors are not required merely to make the system look complete.

A data source must not redefine the ontology. Source-specific fields map into the world model; the world model must not be redesigned around the easiest available field.

## 4. Money-flow truth — LOCKED

Ask:

> **Where is money moving from, where is it moving to, who pays, who receives, and what changed work/behavior does that movement create?**

Track levels, growth, acceleration, share shifts, national/provincial/local divergence, price vs volume, policy effects and receiving/losing actors.

`nominal_growth != real_demand_growth`.

A public procurement budget is evidence of an intended bounded purchase process. It is not automatically evidence of completed payment, supply scarcity, private-market demand or orchestration margin.

Money-flow evidence can reveal actor changes and latent-value search zones, but money movement alone does not prove an exchange opportunity.

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
→ actor state / behavior change
→ friction / underuse / misallocation
→ latent-value insight
→ complementary actor structure
→ exchange hypothesis
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

`Need / Resource / Blocker` is the current fail-closed evidence gate for transaction promotion. It is not the whole discovery ontology.

Before calling an exchange route testable, separately prove:

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
Potential Value != Proven Value
Latent Value Hypothesis != Verified Resource
Observed Friction != Paid Need
Paid Need != Resource Imbalance
Resource Exists != Resource Is Underused
Underused != Available
Complementarity != Transactionability
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

The current production objective is to connect live source adapters to the broader latent-value discovery model and Resource Imbalance Engine without semantic invention.

Live normalization rules:
- use narrow, auditable capability classification where canonical promotion is involved;
- ambiguous or unclassified evidence stays unbound;
- do not use LLM confidence to manufacture a capability identity;
- do not infer payer from beneficiary, project title or budget holder language without source evidence;
- do not promote a procurement budget into `PAID` merely because money is quoted;
- do not turn repeated asset listing into an observed blocker without evidence of the blocker type;
- bind source-specific transaction blockers to the exact need/transaction identity; capability and geography equality alone are insufficient;
- for explicitly multi-package procurement, preserve package scope through lifecycle evidence; package-specific or package-unresolved settlement must not promote a project-level Need;
- preserve the source item and the reason it did not promote;
- preserve upstream actor/state/friction observations even when they are not yet canonical Need/Resource/Blocker signals.

The unified live evidence system should show not only promoted pairs, but also why evidence remained hypothesis, `NEED_ONLY`, `RESOURCE_ONLY`, `PAIR_HYPOTHESIS` or unbound.

## 9. Hook truth — LOCKED

Do not enter negotiation with only an idea and a request for cooperation.

A credible Hook may be:
- pre-aggregated demand;
- optioned/qualified supply;
- verified information;
- measurable result/pilot;
- trusted distribution/channel access;
- optioned idle capacity/resource;
- transparent conditional economics;
- a newly packaged or aggregated latent resource with explicit acceptance conditions.

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

The operator preferentially owns systems analysis, structural judgment, latent-value discovery, actor/resource mapping, Hook design, transaction architecture, capability decomposition, acceptance/interface design, incentive design, route approval, trust/risk boundaries, exception arbitration and learning updates.

Routine acquisition, sourcing, coding, research, delivery, QA, support and logistics are routable capabilities where feasible.

## 12. Sustainability truth — LOCKED

A core project must behave like a circulation system:

```text
Latent Value / Demand Pump
→ repeated task/order/resource events
→ reusable transaction/capability templates
→ replenishing/replaceable resources
→ accepted outcomes
→ settlement
→ performance/trust data
→ better discovery/routing / lower future failure cost
→ more value activation
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

## 13A. Operator access feasibility — LOCKED

`VALUE / EXCHANGE TRUTH` and `CURRENT OPERATOR ACCESS / EXECUTION FEASIBILITY` are separate axes.

The operator is also an Actor. Its evidenced endowments may include:
- real years of professional work;
- accepted project / delivery history;
- technical and domain literacy;
- systems-analysis and coordination ability;
- education / training;
- cross-region or international experience;
- communication / trust-building ability;
- local knowledge;
- relationships / warm paths;
- reputation / references;
- capital, data, distribution or other mobilizable resources.

These endowments can materially reduce access friction when relevant to the target actor. They do not create entitlement to counterpart time, confidential knowledge, reputation or institutional resources.

For every high-trust or high-status actor, separately establish:

```text
LEGITIMATE ENTRY PATH
+
COUNTERPARTY REASON TO ENGAGE
+
FIRST VALUE PACKET
+
ROLE / STATUS LEGITIMACY
+
BOUNDED COUNTERPARTY ASK
+
EVIDENCE OF ACCESS ROUTE
```

Preferred route order:

```text
PUBLIC INSTITUTIONAL WINDOW
→ AUTHORIZED PROGRAM / EVENT
→ WARM REFERRAL
→ RECOGNIZED PROFESSIONAL ROLE
→ DIRECT COLD OUTREACH ONLY WITH A STRONG VALUE PACKET
```

Canonical access states:

```text
UNASSESSED
ACCESS_BLOCKED
INTRODUCTION_READY
ENGAGEMENT_READY
VALIDATION_ACCESS_READY
```

`ACCESS_BLOCKED` does not falsify the underlying opportunity. It means the current operator route is not executable yet.

Hard boundaries:

```text
VALUE_TRUTH != OPERATOR_ACCESS
OPERATOR_ENDOWMENT != COUNTERPARTY CONSENT
PUBLIC ACTOR != ACCESSIBLE ACTOR
PERSONAL CONFIDENCE != COUNTERPARTY REASON TO ENGAGE
APPEARANCE != CREDENTIAL
REAL WORK HISTORY CAN BE CREDIBILITY EVIDENCE WHEN RELEVANT
MONEY != ONLY FORM OF RECIPROCITY
LOCAL CULTURAL HYPOTHESIS != UNIVERSAL FACT
```

The engine must prefer opportunities where access gaps can be bridged transparently through institutions, useful evidence, bounded reciprocity, professional roles or warm routes rather than deceptive status claims or permanent founder hustling.

## 14. Evidence maturity — LOCKED

```text
L0 statement / latent-value hypothesis
L1 observed behavior/workaround/state change
L2 exact terms accepted verbally
L3 real commitment/deposit/signed task
L4 completed accepted transaction + settlement
L5 repeat/referral
L6 delegated repeat/provider replacement/alternate route
L7 recurring Demand Pump produces multiple transactions and routing improves
```

## 15. Commercial truth rules — LOCKED

```text
Potential Value != Proven Value
Latent Value Hypothesis != Verified Resource
Complaint != Demand
Demand != Willingness to Pay
Observed Friction != Paid Need
Trend != Business
Growth != Money-Flow Understanding
Market Size != Customer Acquisition
Social Salience != Population Share
Success Story != Base Rate
Idle Resource != Valuable Resource
Resource Existence != Resource Control
Underused != Available
Complementarity != Transactionability
Introduction != Orchestration Value
Founder Free Labor != Profit
Capability Claim != Capability Proof
One Provider != Replaceable Supply
One Transaction != Repeatability
One Customer != Demand Pump
Recurring Sales Effort != Regenerative Demand
Operator Endowment != Counterparty Consent
Public Actor != Accessible Actor
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
actor/state/change observation
+ latent-value hypothesis
+ complementary actor hypothesis
+ live need evidence
+ live resource/underuse evidence
+ observed blocker evidence
+ operator access feasibility
→ Resource Imbalance / exchange classification
→ evidence-backed candidate pool
→ same G0-G6 comparison
→ selected Hook
→ cheapest decisive real-world test
```

## 18. Current production evidence — 2026-09-12

Working live evidence paths already include national/Jiangsu/Xuzhou money-flow sources, Xuzhou public procurement, regional financing evidence, public resource-underuse sensors and delegatable validation packets.

These source paths are observers. They are not the engine's business identity.

Resource-underuse Sensor 001 has verified that Xuzhou/Jiangsu official public-resource sources can expose:
- discovered public assets;
- repeated listings / allocation friction;
- explicit `空置/闲置` evidence in some historical records;
- repricing across repeated listings.

These facts prove resource/underuse evidence only within their exact scope. They do not prove compatible paid demand or a profitable route.

The production system currently preserves strict Resource Imbalance promotion while beginning to externalize evidence-acquisition work as delegatable field-validation packets.

The decisive next gap is to expand from source-specific explicit signals toward **broader actor-state and latent-value sensing**, while also proving whether the current operator can legitimately access the actors required for validation, without weakening canonical evidence gates.

## 19. Current next actions — CANONICAL

Engineering priority:
1. maintain broad macro, money-flow, psychology, behavior and live evidence sensors;
2. expand actor-state, change, utilization, underuse and latent-value sensing beyond already-stated demand;
3. treat procurement/marketplace/listing feeds as observers rather than the ontology;
4. normalize evidence into canonical signal records without losing upstream actor/state/friction observations;
5. generate complementary-actor and exchange hypotheses from evidence, not imagination;
6. evaluate current-operator access feasibility separately from opportunity truth;
7. preserve fail-closed payer, payment, underuse, blocker, package and identity gates;
8. route field-solvable evidence/access gaps into delegatable validation tasks;
9. create a fresh broad candidate pool from resulting evidence;
10. apply the same G0-G6 ranking plus access-state comparison;
11. select one strongest route-testable and access-feasible candidate and run the cheapest decisive real transaction test.

## 20. Software truth — LOCKED

Do not build ERP, MES, WMS, CRM or a broad marketplace because they are adjacent to an opportunity.

Software is justified first where it removes repeated cognition, observation, evidence or orchestration bottlenecks:
- source registry;
- actor/state/change observations;
- normalized money-flow signals;
- psychology aggregation;
- case records;
- latent-value hypotheses;
- Need/Resource/Blocker evidence projections;
- Resource Imbalance ledger;
- complementary-actor / exchange hypotheses;
- operator access-feasibility records;
- validation task generation;
- opportunity ranking.

Transaction software is justified only after repeated real transaction bottlenecks appear.

Code must remain downstream of cognition and architecture. A technically elegant component that optimizes the wrong world model is negative progress.

## 21. Governing truth — LOCKED

> **先观其所自：不把世界预设成“需求方与供给方”，而是观察每个 Actor 已有什么、缺什么、正在发生什么、哪些价值被闲置、遮蔽、错配或尚未成形；再以证据证明潜在价值，以结构找到互补关系，同时诚实评估操盘者自身已有的能力、信用、入口与缺口；只有在价值真实、关系可达、交换有诚意、规则可接受时，才以信任、激励和可验收能力让原本彼此无关的价值发生连接。发现可以大胆，晋级必须保守；代码永远服务于认知与架构，任何具体网站、数据字段、现有候选都不得反过来定义系统。**