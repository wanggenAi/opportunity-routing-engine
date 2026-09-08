# Architecture — Opportunity Routing Engine

## 1. System objective

Build a reusable engine that converts social/market change into falsifiable commercial opportunity hypotheses and, when evidence is sufficient, routes those opportunities toward real capabilities and transactions.

The architecture must remain domain-agnostic. Cross-border B2B is one vertical, not the system boundary.

## 2. Canonical pipeline

```text
SIGNAL SOURCES
  ├─ macro / policy / prices
  ├─ search behavior
  ├─ social complaints / workarounds
  ├─ marketplaces / service tasks
  ├─ hiring / labor demand
  ├─ procurement / tenders / RFQs
  ├─ company actions / budgets
  ├─ product / service prices
  ├─ second-hand / idle assets
  └─ public transaction evidence
        ↓
INGEST / OBSERVE
        ↓
NORMALIZE / DEDUPE
        ↓
TREND & FRICTION DETECTION
        ↓
DEMAND HYPOTHESIS
        ↓
BEHAVIOR / PAYMENT EVIDENCE
        ↓
EXISTING SOLUTION ANALYSIS
        ↓
CAPABILITY DISCOVERY
        ↓
TRANSACTION DESIGN
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

### `Signal`
A raw observable: price movement, complaint, job opening, tender, purchase request, search trend, policy, new workaround, repeated task, idle resource, etc.

### `DemandHypothesis`
A structured claim that a defined group has a recurring problem and an identifiable party may pay to solve it.

### `Payer`
The person or organization expected to provide money or other economically meaningful consideration.

### `Capability`
A person, company, product, software system, AI model, machine, asset, inventory, dataset, institution, or combination capable of satisfying the demand.

### `TransactionDesign`
The proposed commercial structure: scope, payer, provider, price logic, delivery, acceptance, risk allocation, and legal/compliance boundaries.

### `Opportunity`
A demand hypothesis that has passed sufficient evidence gates to justify transaction testing.

### `Experiment`
A bounded test intended to falsify or validate one commercial assumption.

### `Outcome`
Observed result: no response, rejection reason, paid pilot, transaction, repeat purchase, margin, delivery failure, etc.

## 4. Opportunity lifecycle

```text
SIGNAL
→ HYPOTHESIS
→ EVIDENCED
→ TRANSACTION_DESIGNED
→ TEST_READY
→ TRANSACTION_TEST
→ VALIDATED / REJECTED / DORMANT
→ REPEATABLE
→ SCALE_CANDIDATE
```

No lifecycle transition may be made solely because an LLM expresses confidence.

## 5. Capability routing

The engine should not assume the solution is another business or supplier.

Possible routes:

```text
Demand
  ├─ AI can solve directly
  ├─ operator can solve
  ├─ freelancer / student / specialist can solve
  ├─ company / manufacturer can solve
  ├─ software / product can solve
  ├─ idle asset / inventory can solve
  └─ composite route: AI + human + company + asset
```

Routing should optimize for transaction success, quality, risk, speed, and economics rather than simply lowest price.

## 6. Opportunity score inputs

The scoring layer should consume explicit evidence for:

- pain severity;
- frequency / market density;
- payer clarity;
- observed payment behavior;
- supply availability;
- current solution weakness;
- transaction simplicity;
- acquisition feasibility;
- delivery controllability;
- gross-margin potential;
- time-to-first-cash;
- regulatory / safety risk;
- defensibility / learning value;
- fit with available operator capabilities.

A detailed rubric lives in `docs/OPPORTUNITY_SCORECARD.md`.

## 7. Evidence model

Every important assertion should retain, where applicable:

- `value`;
- `source` / provenance;
- `observed_at`;
- `source_date`;
- `entity/group` affected;
- `verification_status`;
- `confidence`;
- `contradictions`;
- `notes`.

Derived conclusions must be traceable back to source evidence.

## 8. Human-in-the-loop boundaries

Human review is required before:

- declaring a commercial opportunity validated;
- contacting real people/organizations where outreach is not already explicitly requested by the user/operator;
- making commercial representations or commitments;
- pricing high-risk or ambiguous work;
- handling regulated labor, financial, medical, legal, safety-sensitive, or licensed activities;
- moving from a hypothesis to significant capital expenditure;
- representing third parties without authority.

## 9. Automation principle

Automate repeated bottlenecks, not imagined future volume.

Recommended maturity path:

```text
manual spreadsheet / structured notes
→ repeatable evidence schema
→ scripts
→ scheduled collection
→ ranking / alerts
→ capability graph
→ workflow orchestration
→ marketplace/platform only after transaction density
```

## 10. Initial future modules

### `signals`
Permitted ingestion of macro, behavioral, marketplace, procurement, hiring, price, and public commercial evidence.

### `trend_detection`
Detect sustained changes, emerging clusters, anomalies, and demand migration.

### `demand_analysis`
Convert raw signals into explicit user/problem/payer hypotheses.

### `evidence`
Validate payment behavior, existing alternatives, frequency, and contradictions.

### `capability_graph`
Represent capabilities, proof, geography, cost, availability, reliability, and prior outcomes.

### `routing`
Rank candidate solutions/capabilities for a demand.

### `transaction_design`
Generate bounded commercial test structures with clear deliverables and acceptance conditions.

### `experiments`
Manage falsifiable tests, metrics, stop rules, and outcomes.

### `learning`
Update priors and scoring based on real transaction outcomes.

## 11. Engineering rule

The system is not successful when it produces more ideas.

It is successful when it improves the rate at which we identify opportunities that survive **real payment, delivery, and repeatability tests**.
