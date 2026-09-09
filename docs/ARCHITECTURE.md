# Architecture — Actor-First Opportunity Routing Engine

## 1. System objective

Build a reusable engine that converts social/market change into falsifiable opportunity hypotheses by understanding changing actors, unmet needs, payers, available capabilities/resources, transaction frictions and possible transaction structures.

The architecture must remain domain-agnostic and payer-agnostic. Enterprise problems are one category, not the system boundary.

The operating priority is commercial truth, not software completeness.

## 2. Canonical pipeline

```text
SIGNAL SOURCES
  ├─ macro / policy / prices
  ├─ search behavior
  ├─ social complaints / workarounds
  ├─ consumer transactions / service orders
  ├─ marketplaces / gig tasks
  ├─ hiring / labor demand
  ├─ procurement / tenders / RFQs
  ├─ family / household coordination signals
  ├─ second-hand / rental / repair / sharing markets
  ├─ idle time / skill / asset signals
  └─ public transaction evidence
        ↓
INGEST / OBSERVE
        ↓
NORMALIZE / DEDUPE
        ↓
ACTOR & GROUP DETECTION
        ↓
CHANGE / BEHAVIOR / FRICTION DETECTION
        ↓
NEED HYPOTHESIS
        ↓
BENEFICIARY / PAYER IDENTIFICATION
        ↓
BEHAVIOR / PAYMENT EVIDENCE
        ↓
EXISTING SOLUTION ANALYSIS
        ↓
GAP CLASSIFICATION
        ↓
CAPABILITY / RESOURCE DISCOVERY
        ↓
TRANSACTION-STRUCTURE SEARCH
        ↓
OPPORTUNITY SCORING
        ↓
HUMAN REVIEW
        ↓
SMALL REAL-WORLD TEST
        ↓
OUTCOME CAPTURE
        ↓
LEARNING / MODEL UPDATE
```

Canonical gap classes are defined in `docs/THESIS_TRANSACTION_GAPS.md`:

```text
DEMAND_GAP
CAPABILITY_GAP
PRICE_GAP
TRUST_GAP
INFORMATION_GAP
GEOGRAPHY_GAP
TIME_GAP
COORDINATION_GAP
PAYER_SHIFT
TECHNOLOGY_SHIFT
```

## 3. Core entities

### `Actor`
A person, household, group, organization, institution, or resource-owning entity that participates in or is affected by a transaction.

Suggested fields:
- `actor_type`;
- `segment`;
- `geography`;
- `life_or_business_context`;
- `constraints`;
- `observable_behavior`;
- `trust_requirements`;
- `verification_status`.

### `ActorRole`
An actor may occupy one or more roles:
- `NEED_ACTOR`;
- `BENEFICIARY`;
- `PAYER`;
- `CAPABILITY_PROVIDER`;
- `RESOURCE_OWNER`;
- `SPONSOR`;
- `ORCHESTRATOR`.

Roles must not be assumed to collapse into a single buyer/provider pair.

### `Signal`
A raw observable: price movement, complaint, booking, purchase, search, job opening, tender, marketplace task, request for help, repair/rental activity, idle resource, etc.

### `NeedHypothesis`
A structured claim that a defined actor/group wants an outcome under constraints and current solutions create meaningful friction.

### `PayerHypothesis`
A structured claim about which actor has both incentive and ability to pay, including third-party and sponsored structures.

### `Capability`
A person, group, company, product, software system, AI model, specialist skill, physical asset, inventory, vehicle, space, dataset, institution, local presence, or composite workflow capable of satisfying the need.

### `Gap`
A structured explanation for why an economically meaningful outcome is not already transacting efficiently.

Required fields should eventually include:
- `primary_gap`;
- `secondary_gaps`;
- `evidence`;
- `economic_cost`;
- `blocking_mechanism`;
- `resolution_hypothesis`.

### `TrustRequirement`
A specific condition that must be satisfied for actors to transact safely and confidently: identity, qualification, scope, proof, access control, audit trail, escalation, dispute boundaries, insurance or accountable professional review where appropriate.

### `TransactionDesign`
The proposed exchange structure: roles, scope, price logic, trust, delivery, acceptance, risk allocation, compliance and failure conditions.

### `Opportunity`
A need + payer + capability + transaction structure that has passed sufficient evidence gates to justify testing.

### `Experiment`
A bounded test intended to falsify or validate one commercial assumption.

### `Outcome`
Observed result: no interest, refusal to pay, deposit, paid pilot, successful delivery, dispute, repeat purchase, referral, margin, trust failure, routing failure, etc.

### `Learning`
A conclusion that is explicitly tied to one or more outcomes and can change future priors, scores, routing rules or stop rules.

## 4. Long-run graph model

The long-run system should evolve toward **six linked graphs**, not a single marketplace database.

### 4.1 `Actor Graph`
Represents people, groups, households, organizations and institutions, including roles, context, relationships, constraints and observable behavior.

Answers:
> Who is changing, who benefits, who loses, who pays, who owns resources?

### 4.2 `Demand Graph`
Represents recurring needs, desired outcomes, current workarounds, frequency, urgency, substitutes and evidence of payment/time/risk spent.

Answers:
> What outcome is being sought, by whom, and how costly is the current workaround?

### 4.3 `Capability Graph`
Represents skills, providers, assets, products, software, AI, geography, cost, availability, proof, quality and prior outcomes.

Answers:
> What can solve the need, where is it, when is it available, and how trustworthy is the capability claim?

### 4.4 `Trust Graph`
Represents identity/qualification evidence, prior outcomes, references, access constraints, safety/compliance requirements, dispute history, verification mechanisms and trust dependencies between actors.

Answers:
> What must be true before these actors will safely transact?

### 4.5 `Transaction Graph`
Represents tested combinations of need actor, beneficiary, payer, capability provider, resource owner/sponsor and orchestrator, including scope, price, acquisition channel, acceptance criteria, gap types and economics.

Answers:
> Which actor-role-capability structures actually converted into bounded exchanges?

### 4.6 `Outcome / Learning Graph`
Represents what happened after testing: refusal, payment, delivery, defects, refunds, repeat, referral, margin and the learning derived from those outcomes.

Answers:
> What did reality teach us, and which future opportunity decisions should change because of it?

### Why six graphs

A two-sided list of buyers and providers is not enough.

The defensible learning layer comes from linking:

```text
Actor
→ Demand
→ Capability
→ Trust requirements
→ Transaction design
→ Outcome
→ Learning
↺
```

The system should become better at recognizing **which gap prevents a transaction and which intervention actually changes the outcome**.

## 5. Market structures

The engine must search across:

```text
B2B
B2C
C2C
C2B
SPONSORED / THIRD-PARTY-PAYER
MULTI-SIDED
```

Examples:

```text
elderly beneficiary ← qualified provider
       ↑ payer: adult child / institution

merchant need ← student capability
       ↑ payer: merchant

consumer need ← another consumer's idle asset
       ↑ payer: consumer

youth participant ← hosted experience
       ↑ payer: participant / venue / blended
```

No structure is preferred until evidence shows stronger economics and transaction feasibility.

## 6. Opportunity lifecycle

```text
SIGNAL
→ ACTOR_IDENTIFIED
→ HYPOTHESIS
→ PAYER_HYPOTHESIS
→ EVIDENCED
→ TRANSACTION_DESIGNED
→ TEST_READY
→ TRANSACTION_TEST
→ VALIDATED / REJECTED / DORMANT
→ REPEATABLE
→ SCALE_CANDIDATE
```

No lifecycle transition may be made solely because an LLM expresses confidence.

A candidate with `PAYER = UNKNOWN` may be investigated, but cannot be promoted into a serious transaction test until the specific test defines a payer and obtains adequate commitment evidence.

## 7. Capability routing

Do not assume the solution is a company or supplier.

```text
Need
  ├─ AI can solve directly
  ├─ operator can solve
  ├─ individual / student / freelancer can solve
  ├─ skilled worker / local helper can solve
  ├─ company / manufacturer can solve
  ├─ software / product can solve
  ├─ idle asset / space / inventory / vehicle can solve
  ├─ institution can solve
  └─ composite route
```

Routing should optimize for success probability, trust, safety, quality, speed, convenience and economics—not merely lowest price.

## 8. Payer routing

The engine must explicitly test alternative payer structures.

For a real need, ask:

```text
Can the beneficiary pay?
If not, does a family member pay?
Does an employer gain enough to pay?
Does a supplier or venue pay for access/conversion?
Can an institution sponsor the outcome?
Can advertising/subsidy fund it?
Can multiple actors share cost?
```

A weak direct-to-consumer payment signal should not automatically kill an opportunity if another payer has strong economic incentive.

A theoretical sponsor is not enough. Record the sponsor's own measurable benefit and seek real commitment.

## 9. Opportunity score inputs

Scoring consumes explicit evidence for:
- actor pain severity;
- frequency / density;
- payer clarity;
- observed payment/workaround behavior;
- supply/capability availability;
- current-solution weakness;
- acquisition feasibility;
- trust/safety burden;
- delivery controllability;
- transaction simplicity;
- time-to-first-cash;
- unit economics;
- legal/regulatory risk;
- defensibility / learning value;
- operator fit.

The canonical scoring weights and penalties remain in `docs/OPPORTUNITY_SCORECARD.md`.

## 10. Evidence model

Every important assertion should retain where applicable:
- `actor`;
- `role`;
- `value`;
- `source` / provenance;
- `observed_at`;
- `source_date`;
- `verification_status`;
- `confidence`;
- `contradictions`;
- `notes`.

Derived conclusions must trace back to source evidence.

## 11. Outcome-linked learning rule

A `Learning` record must point to evidence or an outcome.

Valid examples:
- six of ten qualified participants placed deposits at RMB 49;
- five venues refused cash sponsorship but three offered free space only;
- owners paid for pet sitting but refused stranger home access even with ID verification;
- a provider completed five transactions with zero revisions and two repeats.

Invalid:
- "the market seems promising";
- "AI says this category should grow";
- "the score is high".

The engine should eventually use outcome evidence to update priors for actor segments, payer structures, acquisition channels, trust controls and capability routes.

## 12. Human-in-the-loop boundaries

Human review is required before:
- declaring an opportunity validated;
- contacting real actors where outreach is not already authorized;
- making commercial representations or commitments;
- routing vulnerable groups into high-trust or safety-sensitive interactions;
- pricing ambiguous/high-risk work;
- handling regulated labor, financial, medical, legal, childcare, eldercare, transport or safety-sensitive activities;
- significant capital expenditure;
- representing third parties without authority.

## 13. Automation maturity path

```text
manual actor interviews / observation
→ repeatable actor + need + payer schema
→ transaction logs
→ scripts / evidence collection
→ ranking / alerts
→ linked Actor + Demand + Capability + Trust + Transaction + Outcome graphs
→ routing / trust workflows
→ orchestration
→ marketplace/platform only after transaction density
```

## 14. Future modules

### `signals`
Collect permitted social, behavioral, marketplace, pricing, employment, household, transaction and resource-utilization evidence.

### `actors`
Classify actor groups, context, roles and recurring behavior without forcing industry labels.

### `demand_graph`
Represent needs, behavior, workarounds, frequency, payment evidence and demand migration.

### `need_analysis`
Convert actor changes/frictions into explicit need hypotheses.

### `payer_analysis`
Identify and compare direct, family, enterprise, sponsor and multi-sided payer candidates.

### `gap_analysis`
Classify and test demand, capability, price, trust, information, geography, time, coordination, payer and technology gaps.

### `evidence`
Validate payment behavior, workarounds, alternatives, frequency and contradictions.

### `actor_graph`
Represent actors, roles, recurring needs, context and relationships.

### `capability_graph`
Represent capabilities/resources, proof, geography, cost, availability, reliability and prior outcomes.

### `trust_graph`
Represent verification, qualification, safety/compliance constraints, access rules, prior reliability and trust relationships.

### `routing`
Rank candidate capabilities and actor-role combinations.

### `transaction_graph`
Represent transaction designs and real attempts.

### `transaction_design`
Generate bounded transaction structures, trust mechanisms and acceptance conditions.

### `experiments`
Manage falsifiable tests, metrics, stop rules and outcomes.

### `learning`
Capture outcomes and update future opportunity priors only from traceable evidence.

## 15. Engineering rule

The system is not successful when it produces more enterprise ideas—or more ideas of any kind.

It succeeds only when it improves the rate at which we identify actor-specific opportunities that survive **real willingness-to-pay, delivery, trust and repeatability tests**.
