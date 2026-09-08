# Opportunity Routing Engine

A validation-first system for continuously discovering unmet demand created by social change, identifying the people or organizations able to satisfy it, and turning high-confidence mismatches into testable transactions.

> Observe society → detect demand shifts → validate willingness to pay → route capabilities → test transactions → learn from outcomes.

## Mission

Build a repeatable **opportunity discovery and capability routing engine** that can adapt as society, technology, demographics, policy, employment, consumption, and business behavior change.

The project does **not** assume one industry, one customer type, one geography, or one business model.

A demand side may be:

- consumers;
- enterprises;
- manufacturers;
- overseas companies;
- students;
- skilled workers;
- local communities;
- institutions.

A capability side may be:

- another person;
- a company;
- a manufacturer;
- a freelancer;
- software;
- AI;
- a service provider;
- equipment, inventory, capital, or other resources.

The system's job is not merely to introduce two parties. Its job is to reduce the friction required to make a useful transaction happen.

## Core thesis

Social change continuously creates temporary imbalances:

- demand exists but supply is hard to find;
- supply exists but demand cannot see it;
- both sides exist but information is fragmented;
- a problem is common but the requirement is poorly defined;
- a solution exists but is too expensive, slow, complex, or inaccessible;
- technology makes an old solution suddenly much cheaper;
- a group is complaining because an unmet need is emerging;
- resources are idle in one place while scarce elsewhere.

These imbalances are candidate opportunities, not automatically businesses.

The engine must distinguish **social noise** from **transaction-capable demand**.

## Canonical loop

```text
SOCIAL / MARKET SIGNALS
        ↓
Trend & behavior detection
        ↓
Problem / friction clustering
        ↓
Demand hypothesis
        ↓
Payment & behavior evidence
        ↓
Existing-solution / competition analysis
        ↓
Capability & resource discovery
        ↓
Transaction-friction analysis
        ↓
Opportunity scoring
        ↓
Small real-world validation
        ↓
Transaction / rejection
        ↓
Outcome learning
        ↺
```

## The four operating verbs

### 1. Observe — 观势
Detect structural change: consumption, employment, technology, demographics, regulation, prices, supply chains, social behavior, and new forms of coordination.

### 2. Detect — 察需
Convert complaints, workarounds, search behavior, purchases, hiring, procurement, and repeated friction into explicit demand hypotheses.

### 3. Route — 找能
Find the capability that can solve the requirement: person, company, AI, software, supplier, service provider, asset, or a combination.

### 4. Transact — 成事
Turn the match into a bounded, priced, deliverable, verifiable transaction. A contact introduction alone is not sufficient value.

## Hard commercial rule

**Complaint ≠ demand. Demand ≠ business.**

A candidate opportunity should not be promoted without evidence for:

1. `PAIN` — the problem is real and sufficiently costly;
2. `FREQUENCY` — the problem repeats or affects enough transactions;
3. `PAYMENT` — an identifiable party has willingness or demonstrated behavior to pay;
4. `SUPPLY` — a viable capability/resource can solve it;
5. `TRANSACTIONABILITY` — scope, price, delivery, and acceptance can be defined;
6. `DEFENSIBILITY` — repeated execution can create proprietary learning, network, data, or process advantage.

## Evidence before automation

Do not build a broad marketplace, crawler, or agent network before repeated transaction evidence exists.

Correct order:

```text
manual observation
→ real demand evidence
→ small transaction experiment
→ repeated wins/losses
→ reusable workflow
→ automation
→ capability graph
→ marketplace/platform only when density exists
```

## Initial opportunity domains

The engine may scan across domains without committing to any of them:

- value-for-money / consumption migration;
- small business external project work;
- China research and information asymmetry;
- AI-enabled replacement of expensive manual work;
- idle asset / inventory utilization;
- local execution tasks;
- domestic or cross-border B2B demand matching;
- skills/capability utilization where legally appropriate;
- aging, employment, education, household, and community frictions;
- new needs created by policy or technological change.

The previous **Xuzhou overseas buyer ↔ manufacturer** thesis remains a valid vertical experiment, but it is no longer the identity of the repository.

## Repository layout

- `docs/FORMAL_TRUTH.md` — current proven facts, hypotheses, unknowns, and decisions
- `docs/METHODOLOGY.md` — opportunity-discovery methodology
- `docs/OPPORTUNITY_SCORECARD.md` — canonical opportunity scoring/gates
- `docs/ARCHITECTURE.md` — system architecture and lifecycle
- `docs/EXPERIMENT_*.md` — falsifiable commercial experiments
- `prompts/` — versioned analysis/extraction/routing prompts
- `data/` — non-sensitive schemas, observations, experiments
- `src/` — code only after repeated bottlenecks justify automation
- `tests/` — truth gates, evidence, scoring, lifecycle tests

## Current phase

**Phase 0 — Build and validate the opportunity-discovery method itself.**

The immediate objective is not to prove one grand business idea. It is to test whether this framework can repeatedly identify opportunities that survive real payment and transaction validation.
