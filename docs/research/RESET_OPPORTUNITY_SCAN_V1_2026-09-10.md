# Reset Opportunity Scan V1 — 2026-09-10

Status: `CURRENT RESEARCH / PRE-TRANSACTION`

This scan intentionally ignores all retired EXP conclusions. It starts again from the canonical two-engine model:

```text
DISCOVERY ENGINE
macro → money flow → market → actor psychology/behavior → friction → payer

RESOURCE ORCHESTRATION ENGINE
transaction objective → CapabilityUnits → resource routing → incentives → acceptance → settlement → learning
```

No numeric score below is a probability of success. Scores are structural prioritization aids only. `UNKNOWN != PASS`.

## 1. Macro regime and money flow

### China

2026 H1 GDP grew 4.7%. Services grew 5.2%, faster than secondary industry at 3.9%. Rental/business services grew 11.9% and information/software/IT services grew 10.7%.

2026 H1 household consumption expenditure grew 3.7% nominally. Education/culture/entertainment expenditure grew 4.9%, household goods/services 5.3%, and other goods/services 9.3%.

By 2026 Jan-Jul, goods retail grew only about 1.1%, while service retail grew about 5.0%; online services retail grew about 5.2%.

Interpretation: the regime is not simply `people stop spending`. It is structurally selective: services, information, business services, convenience and experience remain stronger than many traditional goods categories.

Sources:
- https://www.stats.gov.cn/sj/xwfbh/fbhwd/202607/t20260715_1964121.html
- https://www.stats.gov.cn/sj/zxfbhjd/202607/t20260715_1964129.html
- https://www.stats.gov.cn/sj/zxfb/202608/t20260817_1965056.html

### Jiangsu

2026 H1 service-sector value added grew 5.5%. Rental/business services grew 14.0%, information/software/IT services 10.9%, scientific research/technical services 7.1%. Production-service revenue grew 8.9% and contributed 76.6% of growth among above-scale service firms. Equipment-purchase investment grew 15.0% despite total fixed-asset investment falling.

Interpretation: money is moving toward productive services, digital capability and equipment efficiency rather than broad indiscriminate expansion.

Sources:
- https://www.jiangsu.gov.cn/art/2026/7/22/art_34151_11806875.html
- https://www.jiangsu.gov.cn/art/2026/7/22/art_88350_11806880.html

### Xuzhou

2026 H1 Xuzhou GDP reached RMB 484.69bn. Above-scale industrial value added grew 6.1%; service revenue grew 5.4%; information/software/IT value added grew 15.2%; rental/business services grew 15.1%; social retail grew 4.4%; online goods retail by reporting units grew 13.0%.

The city's 2026-2030 service plan explicitly emphasizes production-service chain strengthening and engineering machinery moving from `sell products` toward `product + full lifecycle service`.

Sources:
- https://www.jiangsu.gov.cn/art/2026/7/31/art_33718_11806875.html
- https://szb.cnxz.com.cn/xzrb/pad/con/202606/28/content_51954.html

## 2. Psychology / decision logic inferred from behavior

These are hypotheses supported by behavior, not population shares:

1. `BUDGET_DISCIPLINE + OUTCOME_CERTAINTY` — broad spending is selective; actors prefer purchases with measurable output and lower irreversible commitment.
2. `FLEXIBILITY_OVER_FIXED_HEADCOUNT` — service growth plus outsourced/project delivery and OPC development suggest value in flexible capability rather than permanent staffing for every task.
3. `SPEED / CONVENIENCE` — online/service channels grow faster, suggesting actors value shorter coordination paths.
4. `RISK_AVERSION` — buyers increasingly require measurable acceptance, traceability, qualification and reliable service rather than raw contact introductions.
5. `SMALL_FAST_PRECISE` — Xuzhou's official SME digital-transformation program explicitly promotes `小快轻准` solutions, reinforcing a preference for bounded, low-cost, fast-result modules.

These hypotheses must continue to be tracked by the Consumer Psychology & Behavior Tracker and verified against transaction behavior.

## 3. Sustainability filter — new hard strategic requirement

A first project should not depend on isolated demand. Prefer a self-renewing transaction loop:

```text
recurring demand aggregator
→ repeated task stream
→ standardized CapabilityUnits
→ replaceable providers
→ acceptance + settlement
→ reliability data
→ lower next-transaction cost
→ more demand / more capable supply
↺
```

Required questions:
- Does the demand source keep receiving new work?
- Does each customer/project create multiple task events rather than one event only?
- Can supply replenish continuously?
- Does transaction history improve future routing?
- Can the orchestration layer retain value after first introduction?

## 4. Candidate pool

### Candidate 1 — Industrial / digital service-provider overflow delivery router

Canonical idea:

> Do not sell directly to hundreds of manufacturers first. Attach to service providers that already own customer relationships and recurring project obligations, and become their managed overflow-delivery layer for bounded non-core tasks.

Current Xuzhou evidence is unusually strong:
- 2026-2027 official plan targets 650 SME digital transformations;
- at least 20 digital-transformation service providers are to be selected;
- at least 120 `small-fast-light-precise` products/solutions are targeted;
- providers are responsible for implementation/system integration, training/capability building, operations/support, data reporting/synchronization, ecosystem collaboration and case/knowledge output;
- the program is rolling through 2027 rather than one fixed batch;
- providers face tracking/ranking and performance pressure;
- current local service providers have large existing client bases and ongoing implementation operations;
- OPC communities create a replenishing pool of small technical providers and already route enterprise tasks to small teams.

Important public evidence:
- 650-firm / 20-provider / 120-solution target: https://www.keceyun.com/policy/newsdetail/707992.html
- provider duties / dynamic management: https://www.keceyun.com/policy/newsdetail/591323.html
- service-provider requirements: https://www.keceyun.com/policy/newsdetail/557532.html
- rolling project filing: https://www.keceyun.com/policy/newsdetail/617272.html
- current evaluation/acceptance work: https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260825/9438c73c-e609-4750-9711-5802528d0757.html
- OPC demand routing: https://szb.cnxz.com.cn/xzrb/pad/con/202608/13/content_54294.html
- software outsourcing as a real procurement form in Jiangsu: https://www.tcrcb.com/zjnshrcb/qtlm/jzcg/cggg/1307037/index.html

Possible first CapabilityUnits — intentionally low-risk / bounded:
- implementation-document normalization;
- training material / SOP production from an approved source pack;
- test-case execution in a sandbox/demo environment;
- anonymized data-cleaning / migration-template preparation;
- public-source customer/industry research packs;
- non-sensitive knowledge-base structuring;
- delivery evidence / progress-material organization that does not impersonate the official evaluator;
- simple internal automation on non-sensitive data where acceptance is explicit.

Do NOT begin with:
- official audit/evaluation/acceptance decisions;
- regulated accounting/legal work;
- unauthorized access to customer systems/data;
- uncontrolled on-site production changes;
- labor dispatch or disguised employment;
- subcontracting where the upstream contract prohibits it.

Demand-source model:

```text
service provider with existing projects
→ identifies an overflow / low-leverage bounded task
→ sends task objective + constraints
→ orchestrator converts to CapabilityUnit
→ provider pool competes / is routed
→ QA / acceptance
→ upstream service provider pays
```

Why sustainable:
- one service provider can generate many tasks across many clients;
- each implementation creates repeated stages and artifacts;
- provider supply can replenish through OPC/freelancer/student/specialist channels;
- completion data builds a reusable reliability graph;
- the wedge can later extend from digital-transformation providers to other production-service providers.

Critical UNKNOWN:
> Will real service providers pay an external orchestration layer for bounded overflow delivery rather than keep work in-house or hire/contract directly?

Provisional structural score: **90 / 100**.
Hard gates: G0 PASS; G1 UNKNOWN for exact external-orchestrator payment; G2 plausible PASS for carefully bounded tasks; G3 PASS/CONDITIONAL by task; G4 strong; G5 UNKNOWN until repeat/bypass test.
Decision: **#1 — START TARGETED VALIDATION NOW.**

### Candidate 2 — Cross-border commerce recurring operations task router

Xuzhou has five provincial cross-border e-commerce parks, eleven public overseas warehouses, nearly 1,000 registered cross-border e-commerce enterprises, seven key industrial belts, and newly strengthened Google/TikTok/Coupang service infrastructure.

Recurring task classes exist in platform operations, listing, data, customer service, document processing, multilingual content and after-sales operations.

Sources:
- https://szb.cnxz.com.cn/xzrb/pad/con/202606/16/content_51388.html
- https://doc.jiangsu.gov.cn/art/2026/6/3/art_79053_11791156.html

Strengths:
- extremely recurring;
- remotely deliverable;
- abundant supply;
- demand can be aggregated by parks/agencies/sellers;
- strong future geographic expansion.

Weaknesses:
- strong incumbent outsourcing agencies;
- AI is rapidly compressing commodity task value;
- direct bypass risk is high;
- low-value content/listing work can become price competition.

Provisional raw score: 86. Apply an initial -10 incumbent/bypass risk until a narrower unresolved gap is proven. Adjusted: **76**.
Decision: **#2 — attractive second wedge, but do not begin with generic cross-border operations.**

### Candidate 3 — Engineering-machinery aftermarket resource orchestration

Xuzhou is deliberately building global spare-parts dispatch, remanufacturing, used-equipment trading and digital operations dispatch as a second growth engine. Engineering machinery is moving from equipment sale to lifecycle service.

Sources:
- https://www.jiangsu.gov.cn/art/2026/7/21/art_33718_11808010.html
- https://szb.cnxz.com.cn/xzrb/pad/con/202604/20/content_48842.html
- https://www.xcmg.com/aboutus/news-detail-1128971.htm

Potential capability units:
- parts identification / documentation;
- public-source supplier search;
- translation/localization;
- shipment/status coordination;
- remote triage support under qualified technical authority;
- local-language customer communication;
- evidence collection;
- non-safety-critical aftermarket administration.

Strengths:
- high-value recurring lifecycle demand;
- strong local industrial density;
- global expansion;
- orchestration and replacement can matter substantially.

Weaknesses:
- trust, technical qualification, liability and response-time burden;
- major OEMs already operate large service networks;
- actual entry point for an independent orchestrator is not yet proven;
- physical/on-site dependencies reduce first-test speed.

Provisional raw score: 84; -15 for heavy physical/custom dependency in the broad form = **69**.
Decision: **#3 — strategically interesting long-run vertical; first narrow it to low-risk aftermarket information/coordination units.**

### Candidate 4 — OPC shared-operations / task routing

Xuzhou has multiple OPC communities and plans continued expansion. Public reporting describes technical founders with real projects but weak customer access and business capacity. An OPC business-matching event already helped one founder obtain two enterprise orders and three simultaneous projects.

Source:
- https://szb.cnxz.com.cn/xzrb/pad/con/202608/13/content_54294.html

Strengths:
- excellent capability-supply pool;
- repeat project potential;
- actors are easy to cluster geographically;
- very good for provider discovery.

Weaknesses:
- many OPC actors need demand more than they supply demand;
- subsidized/free ecosystem services may reduce willingness to pay the orchestration layer;
- budgets can be thin;
- can collapse into a generic freelancer marketplace.

Provisional raw score: 79; apply -10 until paid orchestration/bypass is disproven = **69**.
Decision: **use mainly as supply and partner channel, not first payer market.**

### Candidate 5 — Property/community household-service routing

Policy and household spending support recurring convenience/home services, and `property + life services` is explicitly encouraged.

Source:
- https://www.jiangsu.gov.cn/art/2026/6/11/art_46143_11783953.html

Strengths:
- recurring local demand;
- property/community can aggregate users;
- provider supply can be modular.

Weaknesses:
- low ticket size;
- home access / safety / quality disputes;
- strong incumbents and local relationship dependence;
- coordination cost can overwhelm margin.

Provisional raw score: 80; -20 trust/home-access penalty = **60**.
Decision: **not the first project.**

### Candidate 6 — Elder-care / family-service coordination

Xuzhou has more than 2.29m people aged 60+, and Jiangsu is expanding home/community care and standardized dispatch/monitoring loops.

Sources:
- https://www.jiangsu.gov.cn/art/2026/7/3/art_33718_11804670.html
- https://mzt.jiangsu.gov.cn/art/2026/6/20/art_78628_11798731.html

Strengths:
- enormous recurring need;
- strong sponsor/family/institution payer possibilities;
- coordination layer can be valuable.

Weaknesses:
- vulnerable-person safety;
- medical/care/licensing boundaries;
- severe trust and liability burden;
- public/subsidized provision changes payer economics.

Initial penalties make this a poor first sandbox despite market importance.
Decision: **REJECT AS FIRST PROJECT; revisit only with qualified institutional partners.**

## 5. Ranking

| Rank | Candidate | Adjusted structural score | Why |
|---|---|---:|---|
| 1 | Industrial/digital service-provider overflow delivery router | 90 | Recurring demand aggregators + bounded delivery + high delegation + strong local policy/market timing |
| 2 | Cross-border recurring operations task router | 76 | Very recurring and remote, but commodity competition / AI / bypass risk |
| 3 | Engineering-machinery aftermarket orchestration | 69 | Strong long-run economics and local advantage, but trust/physical complexity slows first proof |
| 4 | OPC shared-operations router | 69 | Strong supply pool, weaker payer clarity; better as capability source |
| 5 | Property/community household-service routing | 60 | Recurring but trust/low-ticket economics are unattractive for first proof |
| 6 | Elder-care coordination | <50 after broad safety/regulatory penalties | Important market, wrong first sandbox |

## 6. Current best-bet hypothesis

The highest-fit first project is:

# **Industrial Service Overflow Routing Network**

Chinese working name:

> **制造业/数字化服务商交付溢出任务编排网络**

It is not a freelancer marketplace and not a staffing agency.

The object being sold is not `a person`; it is an **accepted CapabilityUnit outcome**.

The first market wedge is Xuzhou digital-transformation / industrial software service providers because current demand is unusually dense and observable. The platform identity remains broader: it can later route recurring capability units from cross-border operations, industrial aftermarket and other production-service chains.

## 7. Self-renewing circulation model

```text
UPSTREAM DEMAND PUMP
service providers / agencies / channels already receiving client work
        ↓
TASK QUEUE
small / urgent / low-leverage / cross-skill / overflow delivery units
        ↓
ORCHESTRATOR
scope → decompose → price → acceptance → route → replacement
        ↓
CAPABILITY POOL
OPC / freelancers / specialists / students / AI / small studios
        ↓
ACCEPTED OUTPUT
        ↓
SETTLEMENT
payer → provider payout → orchestration margin
        ↓
OUTCOME DATA
quality / speed / revisions / reliability / economics
        ↓
BETTER ROUTING + LOWER RISK
        ↓
more upstream demand + better providers
        ↺
```

This is the desired `blood circulation` property. The system should not require a new founder-led sales campaign for every task.

## 8. Cheapest decisive first validation

Do not build software. Do not recruit 100 providers. Do not contact 650 manufacturers.

Target only **5 qualified demand aggregators** first:
- official/local digital-transformation service providers with existing manufacturing clients;
- industrial software / ERP / MES implementation providers;
- OPC / enterprise-service operators that already receive project demand.

Ask each one for the last 30 days:
1. How many small/urgent delivery tasks consumed senior staff time but did not require senior judgment?
2. Which tasks were delayed because the team was busy?
3. Which tasks were outsourced, hired for, or reluctantly done internally?
4. Can one task be stripped of sensitive data and specified with objective acceptance?
5. What does the task currently cost in staff hours or external fee?
6. Would they pay for **accepted output**, not a freelancer introduction?
7. Can they release one real paid pilot now?

PASS for first phase:
- at least 3 of 5 can name a real recent overflow task;
- at least 2 permit one task to be specified under confidentiality/compliance constraints;
- at least 1 makes a real paid commitment for an accepted bounded output.

FAIL / redesign:
- 5 qualified providers have no recurring overflow;
- contracts consistently prohibit delegation/subcontracting of any useful unit;
- only on-site/sensitive/core consulting remains;
- they prefer direct hiring/freelancers and see no value in orchestrated QA/replacement;
- task economics cannot support provider payout + orchestration margin.

## 9. Immediate action rule

The next piece of information the engine needs is not another trend article. It is one real service provider saying either:

> `Yes, here is a bounded task and I will pay RMB X when it passes acceptance.`

or:

> `No, and here is exactly why this structure is uneconomic / prohibited / unnecessary.`

Both outcomes are valuable.
