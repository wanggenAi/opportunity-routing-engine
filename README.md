# Opportunity Routing Engine

A validation-first system for continuously discovering unmet demand created by social change, understanding the actors affected by that change, routing available capabilities/resources, and turning high-confidence mismatches into testable transactions.

> Observe society → identify changing actors → detect unmet needs → identify payer → route capabilities → test transactions → learn from outcomes.

## Mission

Build a repeatable **social demand discovery and capability routing engine** that adapts as society, technology, demographics, policy, employment, consumption, family structure, lifestyles, and business behavior change.

The project does **not** assume one industry, one customer type, one geography, one payer, or one business model.

The first question is not “which company has a problem?”

The first question is:

> **Which actor or group is changing, what new friction is appearing, and who has enough incentive to pay for a better outcome?**

## Actor-first principle

An `Actor` may be:

- an individual consumer;
- a student or graduate;
- an unemployed or flexibly employed worker;
- a parent or household;
- an elderly person or caregiver;
- a pet owner;
- a tenant, homeowner, buyer, or seller;
- a skilled worker, farmer, freelancer, driver, or service worker;
- a small merchant or self-employed operator;
- an enterprise, manufacturer, institution, school, community, or government body;
- an overseas person or organization;
- a holder of idle time, skill, equipment, inventory, space, data, or other resources.

The actor experiencing the problem does **not** have to be the payer.

A transaction may contain distinct roles:

- `NEED_ACTOR` — experiences the need/friction;
- `BENEFICIARY` — receives the outcome;
- `PAYER` — provides money or economically meaningful consideration;
- `CAPABILITY_PROVIDER` — supplies skill/resource/service/product;
- `ORCHESTRATOR` — defines, routes, coordinates, verifies, and learns from the transaction.

Example:

```text
Elderly person has digital-service friction
        ↓
Adult child wants the problem solved
        ↓
Student/local helper provides bounded assistance
        ↓
Adult child pays
        ↓
Engine defines scope, trust, routing, evidence and acceptance
```

## Core thesis

Social change continuously creates temporary imbalances:

- a person/group develops a new need before supply adapts;
- one group has idle capability while another has scarcity;
- people still want the underlying outcome but reject the old price/format;
- a household problem exists but the payer is a family member or institution;
- supply exists but trust, discovery, coordination, geography, timing, or verification blocks exchange;
- technology makes an old service cheaper enough to create a new transaction;
- people complain because a new unmet need is emerging;
- resources are idle in one place while valuable elsewhere.

These imbalances are candidate opportunities, not automatically businesses.

## Canonical loop

```text
SOCIAL / MARKET SIGNALS
        ↓
ACTOR & GROUP CHANGE DETECTION
        ↓
Behavior / complaint / workaround clustering
        ↓
Need hypothesis
        ↓
Beneficiary + payer identification
        ↓
Payment / costly-behavior evidence
        ↓
Existing solution analysis
        ↓
Capability / resource discovery
        ↓
Transaction design
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
Detect structural change in people and organizations: consumption, employment, family structure, demographics, technology, regulation, prices, lifestyles, social behavior, supply chains, and coordination patterns.

### 2. Detect — 察需
Convert changed behavior, complaints, workarounds, purchases, searches, hiring, requests, repeated inconvenience, and resource idleness into explicit need hypotheses.

### 3. Route — 找能
Find what can solve the requirement: another person, a group, company, AI, software, product, specialist, manufacturer, physical asset, institution, or combination.

### 4. Transact — 成事
Turn the route into a bounded, priced, deliverable, verifiable transaction. A contact introduction alone is not sufficient value.

## Market structures supported

The engine must be able to discover and compare:

- `B2B` — organization ↔ organization/capability;
- `B2C` — organization/capability → individual;
- `C2C` — individual/resource ↔ individual need;
- `C2B` — individual capability/resource → organization;
- `SPONSORED` — beneficiary uses, another actor pays;
- `MULTI_SIDED` — multiple actors jointly create the transaction.

No structure receives priority merely because its payer is easier to observe.

## Hard commercial rule

**Complaint ≠ demand. Need ≠ payer. Demand ≠ business.**

A candidate opportunity should not be promoted without evidence for:

1. `PAIN` — the problem is real and sufficiently costly;
2. `FREQUENCY` — it repeats or affects enough transactions;
3. `PAYER` — someone has incentive and ability to pay;
4. `PAYMENT` — material payment/workaround behavior exists;
5. `SUPPLY` — viable capability/resource can solve it;
6. `TRANSACTIONABILITY` — scope, price, delivery, trust and acceptance can be defined;
7. `DEFENSIBILITY` — repeated execution can create proprietary learning, network, data or process advantage.

## Evidence before automation

Do not build a broad marketplace before repeated transaction evidence exists.

```text
observe actors
→ identify real need
→ locate payer
→ run bounded transaction
→ record outcome
→ repeat
→ build capability graph
→ automate repeated routing
→ platform only after density exists
```

## Initial actor domains

The first scans should deliberately include both individuals and organizations:

- university students / graduates;
- young workers / flexible workers;
- single and renting young adults;
- parents / households;
- elderly people / caregivers / adult children;
- pet owners;
- skilled workers / farmers / local service workers;
- value-conscious consumers;
- small merchants / self-employed operators;
- SMEs / manufacturers;
- institutions / communities;
- overseas actors with China-related needs;
- holders of idle skill, time, equipment, inventory or space.

The previous **Xuzhou overseas buyer ↔ manufacturer** thesis remains one vertical experiment only.

## Repository layout

- `docs/FORMAL_TRUTH.md` — current proven facts, hypotheses, unknowns, and decisions
- `docs/ACTOR_MODEL.md` — canonical actor/role model
- `docs/METHODOLOGY.md` — opportunity-discovery methodology
- `docs/OPPORTUNITY_SCORECARD.md` — canonical opportunity scoring/gates
- `docs/ARCHITECTURE.md` — system architecture and lifecycle
- `docs/EXPERIMENT_*.md` — falsifiable commercial experiments
- `prompts/` — versioned analysis/extraction/routing prompts
- `data/` — schemas, observations, experiments
- `src/` — code only after repeated bottlenecks justify automation
- `tests/` — truth gates, evidence, scoring, lifecycle tests

## Current phase

**Phase 0 — Validate the actor-first opportunity-discovery method itself.**

The immediate objective is not to prove one grand business idea. It is to test whether this framework can repeatedly identify opportunities across real people, groups, households, enterprises and institutions that survive payment and transaction validation.
