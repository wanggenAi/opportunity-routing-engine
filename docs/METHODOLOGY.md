# Methodology — Discover Outcomes, Orchestrate Capabilities

## 1. Purpose

This document defines how the Opportunity Routing Engine converts real-world change into **delegatable, verifiable transactions**.

Strategic kernel: `docs/RESOURCE_ORCHESTRATION_KERNEL.md`.

The method is empirical:

> Observe actors and changing behavior, find a valuable desired outcome, identify the payer, decompose the outcome into capability units, route those units to resources, define incentives/trust/acceptance, execute, settle and learn.

## 2. Unit of opportunity analysis

The discovery unit remains:

```text
Actor × Change × Friction × Desired Outcome × Payer
```

The execution unit becomes:

```text
Transaction Objective × Capability Units × Resource Routes × Acceptance × Settlement
```

Do not begin from a product, platform, provider list or assumed operator task.

## 3. Canonical reasoning chain

```text
ACTOR / CHANGE / BEHAVIOR
→ FRICTION
→ DESIRED OUTCOME
→ BENEFICIARY
→ PAYER
→ CURRENT WORKAROUND
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

## 4. Discovery stage

### A — Actor / change
Identify who is changing and what changed.

### B — Behavior / friction
Find observable behavior, delay, cost, risk, mismatch, idle resource or repeated workaround.

### C — Desired outcome
Write the need as an outcome, not a product request:

> `[actor] needs [measurable outcome] under [constraints] because the current workaround costs [money/time/risk/opportunity].`

### D — Beneficiary / payer
Separate who receives value from who pays.

Test direct, family, employer, institution, sponsor, supplier, merchant, platform and multi-sided payer structures where relevant.

### E — Payment evidence
Look for actual purchases, budgets, procurement, hiring, paid substitutes, deposits, costly workarounds, sponsor spend, repeat behavior and explicit economic loss.

Complaint and interest remain weak evidence.

## 5. Convert demand into a transaction objective

Do not route a vague request such as:

> "I need AI."

Convert it into something measurable, e.g.:

> "For 300 historical quotations, create a searchable structured dataset and generate a draft quotation from a defined product/input schema, with human final approval, within 5 working days."

A `TransactionObjective` should define:

```text
payer:
beneficiary:
desired outcome:
scope:
inputs available:
required final output:
acceptance criteria:
deadline:
budget / price logic:
trust / legal boundaries:
failure / refund condition:
```

If the outcome cannot be bounded, do not pretend it is ready to route.

## 6. Capability decomposition

Ask:

> What functions must succeed for this outcome to be accepted?

Break the transaction into the smallest economically useful units, not into arbitrary microtasks.

Example:

```text
Customer quotation improvement
├─ requirement interview
├─ data extraction / cleaning
├─ pricing-rule clarification
├─ template generation
├─ automation implementation
├─ QA against sample cases
└─ final acceptance
```

For a youth event:

```text
Event outcome
├─ merchant acquisition / BD
├─ venue / coffee capability
├─ participant recruitment
├─ booking / collection
├─ hosting
├─ attendance verification
└─ settlement / feedback
```

This means the operator does not have to personally sell to merchants or recruit participants.

## 7. Capability Unit specification

For each recurring capability unit define:

```text
purpose:
input:
required_output:
acceptance_criteria:
provider_class:
proof_required:
price_model:
payout_condition:
deadline_sla:
dependencies:
trust_safety_requirements:
replacement_rule:
failure_refund_rule:
```

A capability that cannot be specified or verified is not safely routable yet.

## 8. Demand acquisition is a capability

Do not equate `finding demand` with `the operator must sell`.

Possible demand-source routes include:
- commissioned BD;
- industry connectors;
- merchants/service providers with existing relationships;
- communities;
- associations;
- referral partners;
- online inbound;
- procurement/RFQ feeds;
- public task boards;
- platform channels;
- existing providers who detect adjacent needs.

A demand-source capability can be paid by:
- qualified meeting;
- accepted lead;
- converted payer;
- completed transaction;
- recurring account revenue.

The payout event must be explicit and should avoid rewarding low-quality spam.

## 9. Resource routing

For each capability unit, search across:
- individual specialists;
- students / graduates;
- freelancers;
- businesses;
- institutions;
- AI / software;
- physical assets / venues / equipment;
- channels / audiences;
- composite routes.

Routing should optimize expected accepted outcome, not lowest quoted price.

Consider:

```text
output fit
reliability
proof
speed
availability
trust/safety
revision probability
replacement ease
total economic cost
```

## 10. Incentive and interface design

Every multi-party transaction requires explicit interfaces.

For each edge between capability units define:
- what input is handed over;
- format / completeness requirements;
- deadline;
- who accepts it;
- what happens on defect;
- payout trigger.

Prefer economic incentives tied to observable outcomes:
- fixed accepted-output fee;
- qualified-lead fee;
- conversion fee;
- milestone payment;
- success fee;
- minimum guarantee + variable share;
- quality / repeat bonus.

Do not rely on informal goodwill for essential execution.

## 11. Orchestrator value test

Before promoting an opportunity, ask:

> What becomes materially better because the orchestration layer exists?

Possible answers:
- demand becomes precise;
- multiple capabilities are composed;
- providers are qualified;
- trust is manufactured;
- failures are replaced;
- QA/acceptance is standardized;
- settlement is simpler;
- buyer coordination cost falls;
- outcome accountability improves;
- accumulated reliability data improves future routing.

If the answer is only `we introduce A to B`, orchestration value is weak.

## 12. Delegation-first execution

For every task:

```text
ELIMINATE?
↓ no
AUTOMATE SAFELY?
↓ no
DELEGATE AS BOUNDED CAPABILITY?
↓ no
OPERATOR TEMPORARILY EXECUTES
```

Temporary operator execution is allowed only as a learning shortcut.

Record:
- reason operator performed it;
- time spent;
- estimated market replacement cost;
- plan to externalize it.

The system should progressively move from O0 to O2+ as defined in `RESOURCE_ORCHESTRATION_KERNEL.md`.

## 13. Economic accounting

For each real test record:

```text
payer_inflow:
demand_source_payout:
provider_payouts:
resource_costs:
qa_trust_costs:
refund_failure_reserve:
other_operating_costs:
cash_contribution_margin:
operator_hours_by_function:
operator_shadow_rate:
operator_shadow_cost:
normalized_orchestration_margin:
```

A positive cash margin with large unpaid operator labor is not proof of repeatable economics.

## 14. Smallest decisive test

Prefer a test that proves the routing system, not founder hustle.

Examples:
- pay a connector only for a qualified attended buyer interview;
- route one bounded digital task to a provider and verify accepted output;
- hire/reward a participant recruiter for real deposits rather than recruit personally;
- let a merchant BD resource obtain one authorized venue commitment;
- replace one failed provider and still deliver on time;
- complete one transaction where acquisition and delivery are both delegated.

## 15. Evidence levels

```text
L0 narrative / stated opinion
L1 recent behavior / workaround
L2 exact price / transaction terms accepted verbally
L3 real deposit / authorized commitment / signed task
L4 completed accepted transaction + settlement
L5 repeat / referral
L6 delegated repeat with provider replacement or multiple routes
```

`L6` is strategically important because it begins to prove the engine rather than one provider relationship.

## 16. Intervention contamination

Successful cases may be distorted by government subsidy, public traffic, platform subsidy, free resources, grants, influencer exposure, festivals or institutional mandates.

Separate:
- `DEMAND_EVIDENCE`;
- `CAPABILITY_EVIDENCE`;
- `SPONSOR_EVIDENCE`;
- `INDEPENDENT_PAYER_EVIDENCE`.

When a payer thesis depends materially on intervention, use a comparable control without that support before generalizing.

## 17. Opportunity anti-patterns

Downgrade or reject models based on:
- founder charisma / personal relationships as permanent execution requirement;
- pure contact forwarding;
- unbounded bespoke work;
- tasks with no objective acceptance;
- low-ticket work whose acquisition/support/coordination overwhelms margin;
- one irreplaceable provider;
- safety/liability that cannot be bounded;
- free founder labor used to manufacture apparent profit;
- heavy software/capital before payer proof;
- demand where direct buyer-provider access removes virtually all orchestration value.

## 18. Operator role

The operator is primarily:

```text
opportunity judge
+ transaction architect
+ capability decomposer
+ incentive designer
+ routing governor
+ trust/risk architect
+ acceptance governor
+ learning-system owner
```

The operator is **not** presumed to be the salesperson, developer, researcher, recruiter, host or runner.

If the operator temporarily performs one of those roles, the system should treat it as a capability slot awaiting replacement.

## 19. Governing maxim

**Find the outcome. Split the work. Price the capabilities. Route the resources. Verify the result. Settle everyone. Learn which combination works.**
