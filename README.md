# Opportunity Routing Engine

A validation-first **Actor-First Resource Orchestration Engine** for turning real-world needs into completed, accepted transactions by decomposing outcomes into purchasable capabilities, routing those capabilities to suitable resources, designing incentives/trust/acceptance, settling value, and learning from real outcomes.

> **Discover the outcome → identify the payer → decompose capabilities → route resources → define incentives/interfaces → execute → accept → settle → learn.**

The strategic kernel is locked in `docs/RESOURCE_ORCHESTRATION_KERNEL.md`.

## Mission

Build a reusable system that gets increasingly good at two things:

1. finding real outcomes for which someone has meaningful willingness to pay;
2. assembling the necessary capabilities so the outcome can be delivered **without requiring the operator to personally perform routine acquisition or delivery work**.

The project is not tied to one industry, customer type, geography, provider type or business model.

A cafe event, SME digital task, youth capability project, cross-border workflow or local service is only a test environment for the engine.

## Core identity

The system is **not** primarily:
- a freelancer marketplace;
- an agency selling founder labor;
- a lead reseller;
- a software product looking for users;
- a traditional intermediary that merely introduces two parties.

The system is a **transaction architecture + capability orchestration layer**.

It converts:

```text
ambiguous real-world objective
        ↓
transaction specification
        ↓
capability decomposition
        ↓
purchasable / replaceable task units
        ↓
resource routing
        ↓
accepted result + settlement
```

## Canonical chain

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
```

## Actor roles

Every serious opportunity should distinguish:
- `NEED_ACTOR`
- `BENEFICIARY`
- `PAYER`
- `SPONSOR` where relevant
- `RESOURCE_OWNER` where relevant
- `CAPABILITY_PROVIDER`
- `ORCHESTRATOR`

The actor with the need does not have to be the payer. The operator does not have to be the provider.

See `docs/ACTOR_MODEL.md`.

## Capability-first execution

The atomic execution unit is a `CapabilityUnit`, not a person.

A capability unit should define:

```text
purpose
input
required output
acceptance criteria
provider class
proof required
price model
payout condition
deadline / SLA
dependencies
trust / safety requirements
replacement rule
failure / refund rule
```

Examples:
- demand scouting;
- lead qualification;
- merchant / enterprise BD;
- participant recruitment;
- requirement interviews;
- research;
- development;
- design;
- venue/resource provision;
- hosting;
- logistics;
- QA;
- verification;
- settlement administration.

**Sales, acquisition and execution are capabilities. They are not automatically the operator's job.**

## Delegation-first rule

For every repeated action:

```text
Can it be eliminated?
Can it be automated safely?
Can it be delegated as a bounded capability unit?
Only then should the operator perform it temporarily.
```

Temporary founder execution is allowed for learning, but must be treated as business-model debt.

The first important system milestone is not maximum profit. It is:

> **O2 — delegated acquisition + delegated delivery while the operator retains transaction architecture and governance.**

See `docs/RESOURCE_ORCHESTRATION_KERNEL.md`.

## Economic truth

Every transaction must eventually measure:

```text
payer inflow
- demand-source / acquisition payout
- capability-provider payouts
- resource cost
- trust / QA cost
- refund / failure reserve
- operating cost
= cash contribution margin

cash contribution margin
- operator shadow labor cost
= normalized orchestration margin
```

If the operator performs sales, delivery, QA or other execution for free, that time still receives a shadow cost. Founder free labor must not manufacture fake profitability.

## Why the orchestrator gets paid

The engine must create value beyond contact introduction through one or more of:
- turning vague demand into an executable brief;
- decomposing work into capability units;
- finding a better capability combination;
- qualification / trust;
- dependency management;
- QA and acceptance;
- replacement when execution fails;
- payment / settlement design;
- accumulated outcome/reliability data.

If buyer and provider can bypass the engine with almost no loss, the opportunity has weak orchestration value.

## Transaction gaps

The engine continues to scan for:

1. `DEMAND_GAP`
2. `CAPABILITY_GAP`
3. `PRICE_GAP`
4. `TRUST_GAP`
5. `INFORMATION_GAP`
6. `GEOGRAPHY_GAP`
7. `TIME_GAP`
8. `COORDINATION_GAP`
9. `PAYER_SHIFT`
10. `TECHNOLOGY_SHIFT`

A gap is not a business until a transaction can be designed around it.

See `docs/THESIS_TRANSACTION_GAPS.md`.

## Hard commercial discipline

```text
Complaint != Demand
Demand != Willingness to Pay
Trend != Business
Market Size != Customer Acquisition
Introduction != Orchestration Value
Founder Free Labor != Profit
LLM Confidence != Commercial Evidence
UNKNOWN != PASS
```

Real commitment, accepted delivery, settlement, repeat and replacement behavior outrank narrative evidence.

## Opportunity scoring

Use `docs/OPPORTUNITY_SCORECARD.md`.

The scorecard now explicitly tests:
- payer clarity;
- transactionability;
- capability decomposability / delegatability;
- orchestration value;
- legal/trust/safety feasibility;
- normalized economics.

A commercially attractive transaction that permanently depends on the operator personally doing the work is not a high-fit strategic opportunity for this engine.

## Current phase

**Phase 0 — Prove delegated orchestration through real transactions.**

The system-level target is:

```text
real payer
→ bounded transaction
→ acquisition capability routed
→ delivery capability routed
→ accepted result
→ payouts / settlement
→ operator does not personally perform routine acquisition or delivery
→ normalized economics recorded
→ repeat / replacement tested
```

Current portfolio interpretation:
- `EXP-008` — system-level delegated orchestration proof;
- `EXP-003` + `EXP-007` — preferred early digital/capability sandbox because outputs can often be bounded, routed and verified;
- `EXP-006` — retained as a multi-sided orchestration sandbox, but **no longer requires the operator to do street recruitment or merchant sales personally**;
- `EXP-004` — trust-layer research remains valid but is lower-priority because safety/trust burden is high.

No current vertical is commercially validated.

## Seven-graph learning architecture

If transaction density eventually justifies software, the learning architecture should evolve toward:

```text
Actor Graph
Demand Graph
Capability Graph
Orchestration / Task Graph
Trust Graph
Transaction / Settlement Graph
Outcome / Learning Graph
```

The new first-class `Orchestration / Task Graph` stores decomposition, task dependencies, interfaces, providers and replacement history.

See `docs/ARCHITECTURE.md`.

## Evidence before software

```text
observe
→ define transaction
→ decompose capability
→ route humans/resources manually
→ obtain real commitment
→ deliver
→ accept
→ settle
→ repeat / replace
→ identify recurring routing bottleneck
→ automate only that bottleneck
```

Do not build a marketplace first.

## Repository truth hierarchy

- `docs/RESOURCE_ORCHESTRATION_KERNEL.md` — locked strategic kernel
- `docs/FORMAL_TRUTH.md` — current commercial truth and priorities
- `docs/ACTOR_MODEL.md` — actor roles
- `docs/METHODOLOGY.md` — discovery/decomposition/orchestration method
- `docs/OPPORTUNITY_SCORECARD.md` — gates, weights and penalties
- `docs/ARCHITECTURE.md` — lifecycle and future system structure
- `docs/THESIS_TRANSACTION_GAPS.md` — gap ontology
- `docs/EXPERIMENT_*.md` — falsifiable vertical/system experiments
- `docs/research/` — evidence pools
- `docs/results/` — decision snapshots
- `data/` — structured observations / ledgers
- `src/` — automation only after repeated bottlenecks justify it

## Governing invariant

> **The engine should make a transaction work because the system designed and routed the right capabilities — not because the operator personally performed every difficult step.**
