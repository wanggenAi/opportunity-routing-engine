# Architecture — Actor-First Resource Orchestration Engine

## 1. System objective

Build a reusable engine that converts real-world needs into completed accepted transactions by:

1. identifying actors, outcomes and payers;
2. defining a bounded transaction objective;
3. decomposing the objective into `CapabilityUnit`s;
4. routing those units to suitable resources/providers;
5. designing incentives, interfaces, trust, acceptance and replacement;
6. executing and settling;
7. learning from real performance.

Strategic kernel: `docs/RESOURCE_ORCHESTRATION_KERNEL.md`.

The architecture is domain-agnostic and provider-agnostic. The operator is not the default capability provider.

## 2. Canonical pipeline

```text
SIGNALS / ACTORS / CHANGES
        ↓
BEHAVIOR + FRICTION
        ↓
DESIRED OUTCOME
        ↓
BENEFICIARY / PAYER
        ↓
PAYMENT / WORKAROUND EVIDENCE
        ↓
TRANSACTION OBJECTIVE
        ↓
CAPABILITY DECOMPOSITION
        ↓
CAPABILITY UNIT SPECIFICATION
        ↓
RESOURCE / PROVIDER DISCOVERY
        ↓
ROUTE CONSTRUCTION
        ↓
INCENTIVE + INTERFACE + TRUST DESIGN
        ↓
COMMITMENT
        ↓
EXECUTION
        ↓
ACCEPTANCE / QA
        ↓
SETTLEMENT
        ↓
OUTCOME / MARGIN / RELIABILITY
        ↓
LEARNING / REPUTATION UPDATE
        ↓
BETTER FUTURE ROUTING
```

## 3. Core entities

### `Actor`
Person, household, group, organization, institution or resource-owning entity.

### `ActorRole`
One or more of:
- `NEED_ACTOR`
- `BENEFICIARY`
- `PAYER`
- `SPONSOR`
- `RESOURCE_OWNER`
- `CAPABILITY_PROVIDER`
- `ORCHESTRATOR`

### `DesiredOutcome`
The measurable result an actor wants under defined constraints.

### `PayerHypothesis`
Who has sufficient incentive/ability to pay and what evidence supports it.

### `TransactionObjective`
A bounded commercial objective containing payer, beneficiary, scope, inputs, final output, acceptance, timing, price logic and failure conditions.

### `CapabilityUnit`
A contractible execution function.

Minimum conceptual fields:

```text
id
purpose
input
required_output
acceptance_criteria
provider_class
proof_required
price_model
payout_condition
sla
dependencies
trust_safety_requirements
replacement_rule
failure_rule
```

### `Resource`
A person, organization, AI/software system, asset, venue, equipment, dataset, distribution channel, audience, access right, inventory or other usable input.

### `CapabilityClaim`
A resource's assertion that it can perform a capability unit.

### `CapabilityProof`
Evidence that the resource can actually produce the required output: prior accepted work, test, credential where relevant, verified sample, transaction outcome or other proof.

### `Route`
A proposed assignment of capability units to resources, including dependencies and fallback providers.

### `IncentiveContract`
Defines payout event, amount/formula, timing, quality conditions, refund/clawback boundaries where appropriate and success/failure conditions.

### `TrustRequirement`
Identity, qualification, access, safety, evidence, audit, insurance, professional review, escalation or other condition required for the transaction.

### `Acceptance`
Decision/evidence that an output satisfies explicit criteria.

### `Settlement`
Money/economic consideration flowing from payer/sponsor through the transaction to providers/resources/orchestrator, including refunds and revenue shares.

### `Outcome`
Observed result: refusal, commitment, accepted delivery, defect, replacement, dispute, repeat, referral, margin, failure, etc.

### `Learning`
Evidence-linked conclusion that changes future scores, routes, trust rules, task templates or provider reliability.

## 4. Seven-graph learning architecture

The long-run system evolves toward **seven linked graphs**.

### 4.1 Actor Graph
Who exists, what roles they occupy, context, relationships, constraints and observable behavior.

Answers:
> Who needs, benefits, pays, owns resources, provides capability or sponsors?

### 4.2 Demand Graph
Desired outcomes, workarounds, frequency, urgency, substitutes and payment/time/risk evidence.

Answers:
> What outcome is valuable and how costly is the current workaround?

### 4.3 Capability Graph
Capability units, resource claims, proof, cost, geography, availability, reliability, acceptance rate and prior outcomes.

Answers:
> Who/what can perform each required function, at what expected total cost and reliability?

### 4.4 Orchestration / Task Graph
The decomposition of transaction objectives into capability units and their dependency edges.

Stores:
- task/capability-unit templates;
- required inputs/outputs;
- dependencies;
- handoff interfaces;
- acceptance criteria;
- assigned/fallback resources;
- bottlenecks;
- replacement history.

Answers:
> How should this outcome be decomposed and assembled?

### 4.5 Trust Graph
Verification, credentials, safety/compliance, access rules, prior reliability, disputes and trust dependencies.

Answers:
> What must be true for these resources/actors to transact safely?

### 4.6 Transaction / Settlement Graph
Real transaction attempts and economic flows.

Stores:
- payer/sponsor;
- transaction objective;
- selected route;
- commitments;
- payouts;
- acquisition cost;
- provider/resource cost;
- QA/trust cost;
- refunds;
- operator shadow cost;
- cash margin;
- normalized orchestration margin.

Answers:
> Which structures actually produced accepted output and viable settlement?

### 4.7 Outcome / Learning Graph
Accepted/rejected outputs, failures, replacements, repeat, referrals and evidence-linked learning.

Answers:
> What did reality teach us, and how should future routing change?

## 5. Why the Orchestration / Task Graph is first-class

A buyer/provider marketplace model is insufficient because many valuable outcomes require multiple capabilities.

Example:

```text
payer need
  ↓
requirement definition
  ↓
research/data capability
  ↓
technical capability
  ↓
QA capability
  ↓
accepted output
```

Another:

```text
youth event objective
  ├─ merchant BD
  ├─ venue/coffee resource
  ├─ participant acquisition
  ├─ booking
  ├─ hosting
  └─ attendance/settlement
```

The engine's long-run intelligence comes from learning **decomposition and composition**, not merely matching two names.

## 6. Capability routing

Routing candidate score should eventually estimate:

```text
P(accepted outcome | route)
× speed / availability
× trust/safety suitability
× replaceability
× economic surplus
```

Operationally consider:
- fit to required output;
- proof quality;
- historical acceptance;
- revision/failure probability;
- cost;
- SLA;
- location;
- dependency risk;
- fallback availability.

Lowest nominal quote is not necessarily the cheapest completed route.

## 7. Demand acquisition architecture

Demand access itself is a capability layer.

Potential acquisition resources:
- commissioned BD;
- referrers/connectors;
- associations/communities;
- content/inbound;
- procurement/RFQ sources;
- online task channels;
- adjacent service providers;
- institutional partners.

The engine should record:

```text
source
qualification definition
payout trigger
qualified leads
accepted meetings
converted payers
CAC / source payout
repeat quality
```

This removes the architectural assumption that the operator must personally sell.

## 8. Orchestrator kernel vs routable execution

### Initial kernel
Prefer to keep under orchestrator control:
- opportunity selection;
- transaction design;
- capability decomposition;
- interface/acceptance definition;
- incentive design;
- route approval;
- risk/trust boundaries;
- exception arbitration;
- learning updates.

### Routable by default
- lead sourcing;
- outreach / sales;
- recruitment;
- research;
- coding;
- design;
- translation;
- physical execution;
- hosting;
- logistics;
- routine QA where objective;
- collection/support administration.

A routable function temporarily performed by the operator remains a capability slot, not part of the operator's permanent identity.

## 9. Economic architecture

A transaction record should eventually support:

```text
payer_inflow
- demand_source_payout
- provider_payouts
- resource_costs
- qa_trust_costs
- expected_failure_refund_reserve
- operating/payment_costs
= cash_contribution_margin

cash_contribution_margin
- operator_shadow_cost
= normalized_orchestration_margin
```

Positive cash margin with unpaid founder execution is not enough for repeatability.

## 10. Lifecycle

```text
SIGNAL
→ ACTOR / OUTCOME HYPOTHESIS
→ PAYER HYPOTHESIS
→ EVIDENCED
→ TRANSACTION_OBJECTIVE
→ CAPABILITY_DECOMPOSED
→ ROUTE_DESIGNED
→ COMMITMENT
→ EXECUTION
→ ACCEPTED / REJECTED
→ SETTLED
→ REPEATABLE
→ DELEGATED_REPEAT
→ SCALE_CANDIDATE
```

Evidence maturity:

```text
L0 narrative
L1 behavior/workaround
L2 exact terms accepted verbally
L3 commitment/deposit/signed task
L4 accepted transaction + settlement
L5 repeat/referral
L6 delegated repeat / provider replacement / alternate route succeeds
```

## 11. Operator-independence maturity

```text
O0 operator does acquisition + delivery
O1 delivery delegated
O2 acquisition + delivery delegated
O3 repeatable transaction template with replaceable providers
O4 recurring routing bottlenecks partly automated
O5 network orchestration engine
```

The first system-level milestone is O2.

## 12. Human-in-the-loop boundaries

Human judgment remains mandatory where needed for:
- strategic opportunity promotion;
- ambiguous acceptance;
- high-trust/safety-sensitive work;
- legal/regulatory interpretation;
- vulnerable groups;
- material commercial commitments;
- disputes/exceptions;
- provider qualification where evidence is insufficient.

Automation must not erase responsibility boundaries.

## 13. Automation maturity path

```text
real manual transaction
→ stable transaction objective
→ stable capability decomposition
→ repeated provider routing
→ provider replacement evidence
→ normalized economics
→ recurring bottleneck
→ small automation
→ task/routing graph
→ broader orchestration software
```

Do not reverse this sequence.

## 14. Future modules

Potential modules only after evidence justifies them:

- `signals`
- `actors`
- `demand_graph`
- `transaction_objectives`
- `capability_units`
- `capability_graph`
- `orchestration_graph`
- `provider_proof`
- `routing`
- `incentives`
- `trust_graph`
- `acceptance`
- `settlement`
- `transaction_graph`
- `outcomes`
- `learning`

## 15. Engineering success definition

The architecture succeeds only if it increases the rate at which the engine can produce:

```text
real payer
+ bounded objective
+ correct capability decomposition
+ delegated resource route
+ accepted result
+ settlement
+ provider replacement
+ normalized orchestration margin
+ repeatable learning
```

**The engine is not a database of people. It is a system for composing capabilities into accepted economic outcomes.**
