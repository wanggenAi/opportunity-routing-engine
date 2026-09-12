# Architecture — Actor-First Latent-Value Orchestration Engine

Constitutional parent: `docs/LATENT_VALUE_DOCTRINE.md`.

## 1. System objective

Build a reusable engine that discovers and activates unrealized value in the real world by:

1. observing actors, endowments, constraints, state changes and behavior;
2. detecting friction, underuse, misallocation, fragmentation and costly workarounds;
3. forming evidence-linked `LatentValueHypothesis` records;
4. finding complementary actors whose resources, deficits, access, trust or flows may combine into new value;
5. proving canonical Need / Resource / Blocker / payer / payment evidence without semantic invention;
6. defining a bounded transaction objective;
7. decomposing the objective into `CapabilityUnit`s;
8. routing those units to suitable resources/providers;
9. designing incentives, interfaces, trust, acceptance and replacement;
10. executing and settling;
11. learning from real performance and improving future discovery/routing.

The architecture is domain-agnostic, provider-agnostic and source-agnostic. The operator is not the default capability provider.

A source adapter is an observer, not the strategy. A data field is an observation, not the ontology. A current candidate is a sample, not the business identity.

## 2. Constitutional dependency direction

```text
WORLD MODEL / DOCTRINE
        ↓
DISCOVERY MODEL
        ↓
EVIDENCE MODEL
        ↓
DECISION / VALIDATION MODEL
        ↓
ORCHESTRATION MODEL
        ↓
SOFTWARE MODULES
        ↓
IMPLEMENTATION DETAILS
```

Never reverse this direction.

A website, API, source schema, procurement feed, current candidate or convenient implementation must never redefine the business architecture.

## 3. Canonical pipeline

```text
REALITY / SIGNALS
        ↓
ACTOR
        ↓
ENDOWMENT / STATE / CONSTRAINTS
        ↓
CHANGE
        ↓
BEHAVIOR
        ↓
FRICTION / UNDERUSE / MISALLOCATION / WORKAROUND
        ↓
LATENT VALUE HYPOTHESIS
        ↓
COMPLEMENTARY ACTOR SEARCH
        ↓
EXCHANGE HYPOTHESIS
        ↓
NEED / RESOURCE / BLOCKER EVIDENCE PROJECTIONS
        ↓
BENEFICIARY / PAYER / PAYMENT EVIDENCE
        ↓
ROUTE-TESTABILITY GATES
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
BETTER FUTURE DISCOVERY + ROUTING + ALLOCATION
```

This pipeline deliberately separates **broad discovery** from **conservative promotion**.

The engine may hypothesize hidden value broadly. It must promote opportunities only through fail-closed evidence gates.

## 4. Core entities

### `Actor`
Person, household, group, organization, institution, community, resource-owning entity, channel or other value-bearing node.

An Actor is not permanently a buyer or supplier.

### `ActorRole`
One or more of:
- `NEED_ACTOR`
- `BENEFICIARY`
- `PAYER`
- `SPONSOR`
- `RESOURCE_OWNER`
- `CAPABILITY_PROVIDER`
- `DEMAND_SOURCE`
- `TRUST_SOURCE`
- `CHANNEL_OWNER`
- `ORCHESTRATOR`

Roles may coexist on the same actor and may change by transaction.

### `ActorState`
Observed condition of the actor at a point/period in time, including where relevant:
- workload / utilization;
- inventory / capacity;
- hiring / layoffs;
- pricing / repricing;
- workflow;
- access / distribution;
- trust / reputation;
- cash-flow / spending;
- project cycle;
- constraints;
- recurring workarounds.

### `ActorChange`
Evidence-linked change between states. Change is often more informative than a static profile because it reveals newly created surplus, deficit, urgency or misallocation.

### `Endowment`
A thing an actor has or can potentially mobilize: capability, asset, time, relationship, trust, audience, access, data, location, installed base, recurring demand flow, inventory, process or other usable input.

### `Friction`
Observed recurring cost, delay, workaround, uncertainty, rejection, coordination burden, access gap or structural obstacle.

Friction is not automatically paid demand.

### `LatentValueHypothesis`
A falsifiable claim that potentially realizable value exists in an actor, endowment, relationship, behavior pattern, state change or structural position but is not yet fully recognized, packaged, connected, trusted, priced or activated.

Minimum conceptual fields:

```text
id
actor_ids
observation_refs
value_mechanism
why_value_is_currently_unrealized
complementarity_requirements
falsifiers
maturity
```

`LatentValueHypothesis != Verified Resource`.

### `ComplementarityHypothesis`
A claim that two or more actors have states/endowments/deficits whose combination may create incremental value.

`Complementarity != Transactionability`.

### `NeedSignal`
Evidence projection representing a bounded deficit/outcome need. It is not the full actor model.

### `ResourceSignal`
Evidence projection representing a bounded resource/capability. It is not the full actor model.

### `BlockerSignal`
Evidence projection representing why a specific exchange is not already occurring.

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

A resource may be valuable only in combination with another actor and may not be recognized by its owner as commercially useful.

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
Evidence-linked conclusion that changes future discovery hypotheses, scores, routes, trust rules, task templates or provider reliability.

## 5. Learning graph architecture

The long-run system evolves toward linked graphs. The previous seven graphs remain useful, but a latent-value layer sits upstream of them.

### 5.1 Actor / State Graph
Who exists, what roles they occupy, what they have, constraints, relationships, state, changes and observable behavior.

Answers:
> What exists here, what changed, and what may be newly underused, costly or valuable?

### 5.2 Latent Value / Complementarity Graph
Evidence-linked hypotheses about unrealized value and which actor combinations could unlock it.

Stores:
- latent-value hypothesis;
- observation refs;
- possible value mechanism;
- complementary actor requirements;
- blocker hypotheses;
- falsifiers;
- validation status.

Answers:
> What value might exist that the actors have not yet recognized or connected?

### 5.3 Demand Graph
Desired outcomes, workarounds, frequency, urgency, substitutes and payment/time/risk evidence.

Answers:
> What outcome is valuable and how costly is the current workaround?

### 5.4 Capability / Resource Graph
Capability units, resource claims, proof, cost, geography, availability, underuse, reliability, acceptance rate and prior outcomes.

Answers:
> What resources exist, what is actually available/underused, and what can perform each required function?

### 5.5 Orchestration / Task Graph
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

### 5.6 Trust Graph
Verification, credentials, safety/compliance, access rules, prior reliability, disputes and trust dependencies.

Answers:
> What must be true for these resources/actors to transact safely?

### 5.7 Transaction / Settlement Graph
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

### 5.8 Outcome / Learning Graph
Accepted/rejected outputs, failures, replacements, repeat, referrals and evidence-linked learning.

Answers:
> What did reality teach us, and how should future discovery and routing change?

## 6. Why the Orchestration / Task Graph is first-class

A buyer/provider marketplace model is insufficient because many valuable outcomes require multiple capabilities and because the useful resource may not initially be packaged as supply at all.

Example:

```text
repeated costly workaround
  ↓
latent-value hypothesis
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
underused trusted community
  +
fragmented merchant capacity
  +
participant demand pattern
  ↓
new exchange design
  ├─ merchant BD
  ├─ venue/resource
  ├─ participant acquisition
  ├─ booking
  ├─ hosting
  └─ attendance/settlement
```

The engine's long-run intelligence comes from learning **what value exists, which combinations matter, and how to decompose and compose execution**, not merely matching two names.

## 7. Capability routing

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

## 8. Discovery and demand acquisition architecture

Explicit demand acquisition is only one observation channel, not the starting ontology.

Potential observation/acquisition resources include:
- commissioned BD;
- referrers/connectors;
- associations/communities;
- content/inbound;
- procurement/RFQ sources;
- online task channels;
- adjacent service providers;
- institutional partners;
- utilization/asset records;
- hiring/project-cycle evidence;
- complaints/workarounds;
- repricing/relisting history;
- public operational data;
- field agents.

The engine should distinguish:

```text
OBSERVATION SOURCE
vs
ACTOR STATE
vs
LATENT VALUE HYPOTHESIS
vs
EXPLICIT DEMAND
vs
PAID NEED
```

For explicit demand sources, record:

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

This removes the architectural assumption that the operator must personally sell and also prevents explicit lead sources from defining the whole discovery system.

## 9. Orchestrator kernel vs routable execution

### Initial kernel
Prefer to keep under orchestrator control:
- world-model / doctrine integrity;
- structural observation and judgment;
- latent-value hypothesis formation;
- opportunity selection;
- complementary-actor / exchange design;
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
- field validation;
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

## 10. Economic architecture

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

Latent value is not monetizable by definition; economics must be proven through real commitments, accepted outcomes and settlement.

## 11. Lifecycle

Discovery lifecycle:

```text
OBSERVATION
→ ACTOR_STATE
→ CHANGE / FRICTION / UNDERUSE
→ LATENT_VALUE_HYPOTHESIS
→ COMPLEMENTARITY_HYPOTHESIS
→ EXCHANGE_HYPOTHESIS
→ EVIDENCE PROJECTION
→ ROUTE_TESTABLE
```

Transaction lifecycle:

```text
ROUTE_TESTABLE
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
L0 narrative / latent-value hypothesis
L1 behavior/workaround/state-change observation
L2 exact terms accepted verbally
L3 commitment/deposit/signed task
L4 accepted transaction + settlement
L5 repeat/referral
L6 delegated repeat / provider replacement / alternate route succeeds
L7 recurring Demand Pump produces multiple transactions and routing improves
```

## 12. Operator-independence maturity

```text
O0 operator does acquisition + delivery
O1 delivery delegated
O2 acquisition + delivery delegated
O3 repeatable transaction template with replaceable providers
O4 recurring discovery/routing bottlenecks partly automated
O5 network orchestration engine
```

The first system-level milestone is O2.

## 13. Human-in-the-loop boundaries

Human judgment remains mandatory where needed for:
- strategic opportunity promotion;
- latent-value hypotheses with material ambiguity;
- ambiguous acceptance;
- high-trust/safety-sensitive work;
- legal/regulatory interpretation;
- vulnerable groups;
- material commercial commitments;
- disputes/exceptions;
- provider qualification where evidence is insufficient.

Automation must not erase responsibility boundaries.

## 14. Automation maturity path

```text
broad observation
→ repeated useful actor/state signals
→ stable evidence projection
→ real manual validation/transaction
→ stable transaction objective
→ stable capability decomposition
→ repeated provider routing
→ provider replacement evidence
→ normalized economics
→ recurring bottleneck
→ small automation
→ discovery/task/routing graphs
→ broader orchestration software
```

Do not reverse this sequence.

## 15. Architectural veto for new features

Before building a material feature, answer:

1. What latent value, actor state, behavior, friction, resource or exchange structure does it help observe, validate or activate?
2. Does it help discover value that may not already be explicitly stated?
3. Does it preserve the distinction between hypothesis and evidence?
4. Does it improve connection of complementary actors without making the operator permanent labor?
5. Is it reusable capability rather than overfitting to one website, source or candidate?
6. Does it preserve fail-closed canonical promotion?

If the first four answers are weak, it is not a core-priority architecture feature.

## 16. Future modules

Potential modules only after evidence justifies them:

- `signals`
- `actors`
- `actor_state`
- `actor_change`
- `endowments`
- `latent_value_hypotheses`
- `complementarity_graph`
- `exchange_hypotheses`
- `demand_graph`
- `resource_graph`
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

## 17. Engineering success definition

The architecture succeeds only if it increases the rate at which the engine can produce:

```text
useful real-world observation
+ evidenced latent-value hypothesis
+ complementary actor structure
+ real payer
+ bounded objective
+ correct capability decomposition
+ delegated resource route
+ accepted result
+ settlement
+ provider replacement
+ normalized orchestration margin
+ repeatable learning
```

**The engine is not a database of buyers and suppliers. It is a system for seeing unrealized value, proving what is real, composing complementary actors/capabilities, and turning that structure into accepted economic outcomes.**
