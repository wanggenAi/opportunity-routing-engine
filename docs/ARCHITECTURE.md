# Architecture — Actor-First Opportunity Routing Engine

## 1. System objective

Build a reusable engine that converts social/market change into falsifiable opportunity hypotheses by understanding changing actors, unmet needs, payers, available capabilities/resources, and possible transaction structures.

The architecture must remain domain-agnostic and payer-agnostic. Enterprise problems are one category, not the system boundary.

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

### `TransactionDesign`
The proposed exchange structure: roles, scope, price logic, trust, delivery, acceptance, risk allocation, compliance and failure conditions.

### `Opportunity`
A need + payer + capability + transaction structure that has passed sufficient evidence gates to justify testing.

### `Experiment`
A bounded test intended to falsify or validate one commercial assumption.

### `Outcome`
Observed result: no interest, refusal to pay, paid pilot, successful delivery, dispute, repeat purchase, referral, margin, trust failure, routing failure, etc.

## 4. Graph model

The long-run architecture should evolve toward three linked graphs.

### `Actor Graph`
Represents people/groups/organizations and relevant context, roles, recurring needs, behavior and trust relationships.

### `Capability Graph`
Represents skills, providers, assets, products, software, AI, geography, cost, availability, proof, quality and prior outcomes.

### `Transaction Graph`
Represents which actor-role/capability combinations were tested, at what price, through which channel, with what outcome.

The defensible learning layer comes from the interaction of all three graphs.

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
elderly beneficiary ← local helper
       ↑ payer: adult child

merchant demand ← student capability
       ↑ payer: merchant

consumer need ← another consumer's idle asset
       ↑ payer: consumer

student beneficiary ← project experience
       ↑ payer: enterprise / institution / sponsor
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
Does a supplier pay for access/conversion?
Can an institution sponsor the outcome?
Can advertising/subsidy fund it?
Can multiple actors share cost?
```

A weak direct-to-consumer payment signal should not automatically kill an opportunity if another payer has strong economic incentive.

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

## 11. Human-in-the-loop boundaries

Human review is required before:

- declaring an opportunity validated;
- contacting real actors where outreach is not already authorized;
- making commercial representations or commitments;
- routing vulnerable groups into high-trust or safety-sensitive interactions;
- pricing ambiguous/high-risk work;
- handling regulated labor, financial, medical, legal, childcare, eldercare, transport or safety-sensitive activities;
- significant capital expenditure;
- representing third parties without authority.

## 12. Automation maturity path

```text
manual actor interviews / observation
→ repeatable actor + need + payer schema
→ transaction logs
→ scripts / evidence collection
→ ranking / alerts
→ Actor Graph + Capability Graph
→ routing / trust workflows
→ orchestration
→ marketplace/platform only after transaction density
```

## 13. Future modules

### `signals`
Collect permitted social, behavioral, marketplace, pricing, employment, household, transaction and resource-utilization evidence.

### `actors`
Classify actor groups, context, roles and recurring behavior without forcing industry labels.

### `need_analysis`
Convert actor changes/frictions into explicit need hypotheses.

### `payer_analysis`
Identify and compare direct, family, enterprise, sponsor and multi-sided payer candidates.

### `evidence`
Validate payment behavior, workarounds, alternatives, frequency and contradictions.

### `actor_graph`
Represent actors, roles, recurring needs, trust constraints and relationships.

### `capability_graph`
Represent capabilities/resources, proof, geography, cost, availability, reliability and prior outcomes.

### `routing`
Rank candidate solutions and role combinations.

### `transaction_design`
Generate bounded transaction structures, trust mechanisms and acceptance conditions.

### `experiments`
Manage falsifiable tests, metrics, stop rules and outcomes.

### `learning`
Update priors and scores using real transaction outcomes.

## 14. Engineering rule

The system is not successful when it produces more enterprise ideas—or more ideas of any kind.

It succeeds only when it improves the rate at which we identify actor-specific opportunities that survive **real willingness-to-pay, delivery, trust and repeatability tests**.
