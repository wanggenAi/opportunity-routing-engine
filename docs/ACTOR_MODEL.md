# Actor Model

## Purpose

The engine is actor-first but executes capability-first.

An `Actor` is a participant in the economic system. A `CapabilityUnit` is a bounded function required to complete a transaction. Do not confuse the two.

Strategic kernel: `docs/RESOURCE_ORCHESTRATION_KERNEL.md`.

## 1. Actor

An `Actor` is any person, household, group, organization, institution or resource-owning entity relevant to an opportunity.

Examples include individuals, households, students, graduates, workers, merchants, freelancers, enterprises, manufacturers, institutions, communities, public bodies, overseas actors and owners of idle skills/assets/space/data/access.

## 2. Canonical actor roles

### `NEED_ACTOR`
Experiences the friction or unmet need.

### `BENEFICIARY`
Receives the solved outcome.

### `PAYER`
Provides money or other economically meaningful consideration.

### `SPONSOR`
Pays or subsidizes because another actor's outcome creates value for the sponsor.

### `RESOURCE_OWNER`
Controls a resource used in the transaction: time, skill, space, equipment, inventory, data, access, audience, distribution, capital or another scarce input.

### `CAPABILITY_PROVIDER`
Commits to perform one or more bounded capability units.

### `ORCHESTRATOR`
Defines the transaction objective, decomposes required capabilities, defines interfaces/incentives/trust/acceptance, routes resources, governs exceptions, settles or verifies settlement, and learns from outcomes.

One actor may hold several roles.

**The operator is not automatically the `CAPABILITY_PROVIDER`.**

## 3. Capability Unit

A capability is not merely a skill label such as `developer`, `salesperson` or `designer`.

A routable `CapabilityUnit` is a contractible unit of work:

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
deadline_sla:
dependencies:
trust_safety_requirements:
replacement_rule:
failure_refund_rule:
```

Examples:

```text
"sales"
→ weak capability description

"Reach 20 qualified Xuzhou SME decision-makers from an approved target list and produce >=3 booked requirement interviews; payout RMB X per attended qualified interview"
→ routable capability unit
```

```text
"find young people"
→ weak capability description

"Recruit 8 qualified participants who place the defined refundable deposit for the same event; payout per valid deposit / attendance"
→ routable capability unit
```

## 4. Execution-function map

Common functions should be modeled as capabilities rather than silently assigned to the operator:

```text
Demand access
├─ signal collection
├─ target discovery
├─ lead qualification
├─ outreach
├─ BD / closing
└─ participant recruitment

Problem definition
├─ interview
├─ requirement extraction
├─ scope definition
└─ acceptance design

Delivery
├─ research
├─ software / AI
├─ data work
├─ design / content
├─ specialist work
├─ physical execution
├─ venue / equipment
└─ logistics

Trust / governance
├─ identity / credential verification
├─ QA
├─ acceptance testing
├─ evidence capture
├─ exception handling
└─ dispute boundaries

Settlement
├─ collection
├─ provider payout
├─ refunds
└─ revenue-share accounting
```

## 5. Demand-source actor is not necessarily the orchestrator

The actor who discovers or reaches the payer may itself be a capability provider.

Example:

```text
PAYER: local merchant
        ↑
BD / demand-source provider
        ↑
ORCHESTRATOR defines target + qualification + payout
        ↓
DELIVERY provider(s)
```

The operator does not need to personally cold-call the payer for the transaction to be valid.

What matters is whether demand access itself can be bounded, priced and verified.

## 6. Provider identity is replaceable; capability contract should remain stable

The long-run goal is not to accumulate names in a contact list.

The engine should learn:
- which capability unit is needed;
- which providers can satisfy it;
- at what cost;
- with what reliability;
- under what constraints;
- how quickly a failed provider can be replaced.

A high-value capability graph therefore links actors to **proven outputs**, not only claimed skills.

## 7. Common orchestration structures

### Simple delegated delivery
```text
Need actor / payer
        ↓
Orchestrator defines outcome
        ↓
Capability provider delivers
```

### Delegated acquisition + delivery
```text
Demand-source / BD provider
        ↓
qualified payer
        ↓
Orchestrator
   ├─ capability A
   ├─ capability B
   └─ QA / acceptance
        ↓
accepted outcome
```

### Sponsored multi-sided
```text
Beneficiary
   ↑
Sponsor / payer
   ↓
Orchestrator
   ├─ acquisition capability
   ├─ resource owner
   ├─ delivery capability
   └─ QA / measurement
```

### Composite resource route
```text
Desired outcome
        ↓
Orchestrator decomposes
   ├─ AI capability
   ├─ human specialist
   ├─ local resource
   └─ verifier
        ↓
accepted composite output
```

## 8. Actor record schema

Recommended minimum actor fields:

```text
actor_id:
actor_type:
segment:
geography:
roles:
context:
current_behavior:
constraints:
trust_requirements:
ability_to_pay:
observed_payment_behavior:
resources_claimed:
capabilities_claimed:
capabilities_proven:
source:
observed_at:
verification_status:
confidence:
```

Do not store unnecessary sensitive personal data.

## 9. Opportunity role map

Every promoted opportunity should include:

```text
Need actor:
Beneficiary:
Payer:
Sponsor (if any):
Resource owner(s):
Required capability units:
Candidate capability providers:
Demand-source capability:
QA / acceptance capability:
Orchestrator value:
Transaction type:
```

If payer is unknown, test payer discovery. If capability units cannot be defined, the opportunity is not orchestration-ready.

## 10. Governing principle

**Ask not only who needs, pays and solves. Ask what exact capabilities are required, whether each can be contracted and replaced, and what value remains for the orchestrator after everyone is paid.**
