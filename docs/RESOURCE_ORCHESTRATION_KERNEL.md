# Resource Orchestration Kernel

Status: `CANONICAL / LOCKED STRATEGIC MODEL`

Effective: 2026-09-10

This document defines the strategic kernel of the Opportunity Routing Engine. Vertical experiments may change. This kernel does not change merely because one experiment wins or fails.

## 1. What the system is

The system is a **real-world resource orchestration engine**.

Its job is not primarily to sell the operator's labor, build a marketplace, introduce two contacts, or choose one industry.

Its job is to repeatedly convert a valuable real-world outcome into a network of purchasable, replaceable, verifiable capabilities and coordinate those capabilities into a completed transaction.

Canonical definition:

> **Discover a real outcome worth paying for, decompose the work into capability units, route each unit to suitable resources, define incentives/interfaces/trust/acceptance, settle the transaction, and learn which combinations reliably work.**

The operator is the initial transaction architect and system governor. The operator is **not the default salesperson, provider, recruiter, runner, host, developer, designer, or support worker**.

## 2. Canonical chain

```text
ACTOR / CHANGE / FRICTION
→ DESIRED OUTCOME
→ BENEFICIARY / PAYER
→ TRANSACTION OBJECTIVE
→ CAPABILITY DECOMPOSITION
→ CAPABILITY UNITS
→ RESOURCE / PROVIDER ROUTING
→ INCENTIVE + INTERFACE + TRUST DESIGN
→ EXECUTION
→ ACCEPTANCE
→ SETTLEMENT
→ OUTCOME
→ REPUTATION / LEARNING
→ BETTER FUTURE ROUTING
```

Discovery and transaction proof still come before software.

## 3. The atomic unit is not a person — it is a Capability Unit

A person, company, AI model, venue, asset, institution or channel may provide one or many capabilities. The engine should reason about **capabilities first**, then route actors/resources to them.

Every recurring execution function should be representable as a `CapabilityUnit`:

```text
capability_unit_id:
purpose:
input:
required_output:
acceptance_criteria:
provider_class:
proof_required:
price_model:
payout_condition:
deadline / SLA:
dependencies:
trust / safety requirements:
replacement_rule:
failure / refund rule:
observed_cost:
observed_quality:
observed_reliability:
```

Examples of capability units:
- demand scouting;
- lead qualification;
- merchant / enterprise BD;
- participant recruitment;
- requirement interview;
- research;
- data cleaning;
- development;
- design;
- translation;
- venue provision;
- hosting / facilitation;
- logistics;
- identity / credential verification;
- QA;
- acceptance testing;
- customer support;
- collection / settlement administration.

**Sales and acquisition are capabilities. They are not automatically the operator's job.**

## 4. The orchestrator owns architecture, not every task

The initial orchestrator's non-delegated kernel is:

1. decide which outcome is worth testing;
2. define the transaction objective;
3. decompose the objective into capability units;
4. define interfaces between units;
5. define acceptance criteria;
6. design economic incentives and payout conditions;
7. define trust, safety and responsibility boundaries;
8. choose or approve capability routes;
9. arbitrate exceptions / acceptance when needed;
10. record outcomes and update routing rules.

Everything else is a candidate for delegation or automation.

Even the kernel may later become increasingly automated, but early validation must prove the logic manually before encoding it.

## 5. Delegation-first rule

For every task ask, in this order:

```text
Can this be eliminated?
Can this be automated safely?
Can this be delegated as a bounded capability unit?
Only if not, must the operator perform it temporarily?
```

Temporary operator execution is allowed for learning, but it creates technical debt in the business model.

A repeated task that depends on the operator personally is a **bottleneck to remove**, not a moat to celebrate.

## 6. Strategic fit: Delegatability

A commercially attractive opportunity is not automatically a strategic fit for this engine.

High-fit opportunities have:
- bounded outputs;
- observable acceptance criteria;
- multiple plausible capability providers;
- low or controllable switching cost;
- clear payout conditions;
- manageable dependencies;
- routable trust requirements;
- repeatable task interfaces;
- enough economic surplus to pay providers and the orchestration layer.

Low-fit opportunities have:
- value tied almost entirely to the operator's personal charisma/identity;
- unbounded bespoke work;
- recurring actions that cannot be specified or verified;
- tiny margins after acquisition/coordination;
- high liability that cannot be allocated safely;
- a single irreplaceable provider without durable contractual control.

## 7. Orchestrator value rule

The engine must create more value than contact introduction.

Valid orchestration value may come from:
- converting ambiguous demand into a precise brief;
- decomposing work into cheaper/faster capability units;
- finding combinations a buyer would not efficiently assemble alone;
- qualification and trust;
- dependency management;
- quality assurance;
- acceptance design;
- outcome accountability;
- replacement when a capability fails;
- payment / settlement structure;
- accumulated performance data that improves future routing.

If buyer and provider can transact directly with almost no loss after first introduction, and the engine contributes no recurring governance/trust/quality advantage, bypass risk is real and the opportunity should be downgraded.

## 8. Economic truth

For every transaction calculate:

```text
PAYER INFLOW
- acquisition / demand-source payout
- capability-provider payouts
- resource costs
- QA / trust / verification costs
- refunds / expected failure reserve
- payment / operating costs
= CASH CONTRIBUTION MARGIN

CASH CONTRIBUTION MARGIN
- OPERATOR SHADOW LABOR COST
= NORMALIZED ORCHESTRATION MARGIN
```

`OPERATOR SHADOW LABOR COST` must be recorded for work the operator performs personally even when no cash wage is paid.

This prevents a transaction from appearing profitable only because the founder works for free.

Early experiments may accept low or negative normalized margin **only when explicitly buying information**. A repeatable model requires positive normalized orchestration economics.

## 9. Incentive design

Do not ask resources to "help" when the transaction depends on them.

Prefer explicit economic contracts such as:
- fixed fee for accepted output;
- per-qualified-lead payout;
- per-converted-payer payout;
- per-attendee payout;
- milestone payment;
- success fee;
- minimum guarantee + variable share;
- revenue share;
- sponsor contribution;
- quality/repeat bonus.

Payout must be tied to an observable event whenever feasible.

The engine should minimize incentives that reward volume while externalizing quality or safety risk.

## 10. Capability routing rule

Routing optimizes for expected completed outcome, not lowest nominal price.

Candidate route score should eventually consider:

```text
fit to required output
× probability of acceptance
× reliability
× speed
× trust / safety suitability
× availability
× replaceability
× economics
```

A cheap provider with high revision/failure probability can be the expensive route.

## 11. Operator-independence milestones

The system matures through these stages:

### O0 — Operator does everything
Useful only for learning. Not the target model.

### O1 — Delegated delivery
Operator may source demand but another resource performs delivery.

### O2 — Delegated acquisition + delegated delivery
Demand sourcing / BD and delivery are both performed by capability providers. Operator designs and governs the transaction.

### O3 — Repeatable orchestration
The same transaction template completes repeatedly with replaceable providers and stable acceptance/economics.

### O4 — Partially automated routing
Repeated bottlenecks are automated; humans remain where judgment/trust requires them.

### O5 — Network orchestration engine
Multiple demand and capability channels can be composed using accumulated outcome/reliability data without the operator personally executing routine work.

**The first major system milestone is O2, not maximum first-order profit.**

## 12. The system is industry-agnostic

A cafe event, SME automation task, research project, youth capability project, translation task, local service, cross-border workflow or another safe transaction is only a **test environment**.

No vertical defines the system.

Prefer early environments that make orchestration easiest to falsify:
- clear payer;
- bounded output;
- short cycle;
- low legal/safety risk;
- multiple potential providers;
- measurable acceptance;
- ability to delegate acquisition and delivery;
- low capital requirement.

## 13. Seven-graph learning architecture

If enough real transactions justify software, the engine should learn through seven linked graphs:

```text
Actor Graph
Demand Graph
Capability Graph
Orchestration / Task Graph
Trust Graph
Transaction / Settlement Graph
Outcome / Learning Graph
```

The new first-class `Orchestration / Task Graph` records decomposition, dependencies, capability interfaces and who performed each unit.

## 14. What we are NOT optimizing for

Do not optimize for:
- the operator personally earning the highest fee per job;
- keeping execution work because the operator can do it better;
- headcount;
- number of ideas;
- number of suppliers;
- number of leads;
- GMV without margin/quality;
- a marketplace UI;
- software sophistication before repeat transactions;
- a single vertical narrative.

Optimize for:

```text
completed accepted outcomes
× repeatability
× delegatability
× normalized orchestration margin
× learning compounding
```

subject to truth, legal, trust and safety constraints.

## 15. Governing invariant

> **The engine should make a transaction work because the system designed and routed the right capabilities — not because the operator personally performed every difficult step.**
