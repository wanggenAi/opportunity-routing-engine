# Opportunity Routing Engine

A validation-first **Actor-First Opportunity Routing Engine** for continuously discovering transaction-worthy imbalances created by social change, identifying the actors affected, routing available capabilities/resources, designing trust/transaction structures, and learning from real outcomes.

> Observe society → identify changing actors → detect friction → identify beneficiary/payer → route capability → design transaction → test with real money → learn.

## Mission

Build a reusable system that answers two questions increasingly well:

> **Where is society currently forming a new tradable imbalance?**

and

> **How can we validate that imbalance as a real transaction as quickly and cheaply as possible?**

The project does **not** assume one industry, one customer type, one geography, one payer, or one business model.

The first question is not “which company has a problem?”

It is:

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
- a holder of idle time, skill, equipment, inventory, space, data, access or other resources.

The actor experiencing the problem does **not** have to be the payer.

Every serious transaction should distinguish:
- `NEED_ACTOR` — experiences the friction;
- `BENEFICIARY` — receives the outcome;
- `PAYER` — provides money/economic consideration;
- `CAPABILITY_PROVIDER` — supplies skill/resource/service/product;
- `RESOURCE_OWNER` — controls relevant time, space, equipment, inventory, data, access or other resource;
- `SPONSOR` — pays because another actor's outcome creates value for them;
- `ORCHESTRATOR` — defines, routes, coordinates, verifies, closes and learns from the transaction.

Example:

```text
elderly person has a need
        ↓
adult child values the outcome
        ↓
qualified provider supplies capability
        ↓
adult child pays
        ↓
engine defines scope, trust, evidence and acceptance
```

## Canonical chain

```text
ACTOR
→ CHANGE
→ BEHAVIOR
→ FRICTION
→ NEED
→ BENEFICIARY
→ PAYER
→ CURRENT WORKAROUND
→ CAPABILITY
→ TRANSACTION DESIGN
→ REAL-WORLD TEST
→ OUTCOME
→ LEARNING
```

Operationally:

```text
观势 → 察需 → 找能 → 成事 → 反馈学习
```

Trends tell us where to look. Behavior and money tell us whether the hypothesis is right.

## What we scan for — transaction gaps

Canonical gap ontology:

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

See `docs/THESIS_TRANSACTION_GAPS.md`.

A gap is not automatically a business. It matters only if a real payer will exchange economic value to reduce it.

## Market structures supported

The engine must compare:
- `B2B`;
- `B2C`;
- `C2C`;
- `C2B`;
- `SPONSORED / THIRD-PARTY-PAYER`;
- `MULTI_SIDED`.

No structure receives priority merely because its payer is easier to observe.

## Hard commercial discipline

```text
Complaint != Demand
Demand != Willingness to Pay
Trend != Business
Market Size != Customer Acquisition
LLM Confidence != Commercial Evidence
UNKNOWN != PASS
```

Prefer evidence such as:
- completed purchases / paid services;
- deposits / bookings / repeat purchases;
- current substitute spending;
- recruitment / procurement / RFQ / tender activity;
- merchant subsidies or spend for traffic/conversion;
- family/institution payment for another beneficiary;
- costly manual workarounds;
- repeated relisting/repricing / failed transactions;
- repeat/referral.

Macro data, searches, complaints and social discussion generate hypotheses. They do not independently validate a business.

## Opportunity scoring

Use `docs/OPPORTUNITY_SCORECARD.md` exactly.

Hard gates include:
- actor/role clarity;
- payer clarity;
- transactionability;
- legal/trust/safety feasibility.

A high weighted score cannot override an `UNKNOWN` or failed hard gate.

## Field laboratory — Xuzhou

Xuzhou is the first field laboratory because online evidence can be converted into in-person falsification quickly.

Current scan source:
- `docs/research/XUZHOU_ACTOR_FIRST_SCAN_V2_2026-09-10.md`

It contains **38 distinct friction records** across youth, students/graduates, workers, households, pet owners, merchants, institutions, asset owners and enterprises.

Current ranking:
- `docs/results/EXP_002_XUZHOU_ACTOR_FIRST_RANKING_V2_2026-09-10.md`

Current field sequence:

```text
1. EXP-006 — youth micro-experience payer commitment
2. EXP-007 — skills-to-income payer discovery
3. EXP-003 — bounded SME micro-project paid validation
4. EXP-004 — pet trust/home-access gate resolution
```

`EXP-001` and broad `EXP-005` are currently dormant/secondary verticals.

No current vertical is commercially validated.

## Field rule

Do not go out to “ask around.”

Before every field visit define:

```text
Hypothesis:
Critical UNKNOWN:
Who to interview:
Where to find them:
5–8 questions:
PASS:
FAIL:
Evidence to record:
Next action:
```

Use `docs/FIELD_VALIDATION_PLAYBOOK_XUZHOU.md`.

A friendly statement is weak evidence. A real refusal at a real price is useful evidence. A deposit is stronger. Completed payment + accepted delivery + repeat/referral is strongest.

## Evidence before automation

```text
observe
→ hypothesis
→ evidence
→ payer commitment
→ first paid transaction
→ repeat manually
→ identify recurring bottleneck
→ automate that bottleneck
```

Do **not**:

```text
build platform
→ then search for users
```

## Long-run learning architecture

If transaction density eventually justifies software, the learning layer should evolve toward six linked graphs:

```text
Actor Graph
Demand Graph
Capability Graph
Trust Graph
Transaction Graph
Outcome / Learning Graph
```

See `docs/ARCHITECTURE.md`.

This is a future architecture, not a current build mandate.

## Repository layout

- `docs/FORMAL_TRUTH.md` — current commercial truth, unknowns, decisions and rejections
- `docs/ACTOR_MODEL.md` — canonical actor/role model
- `docs/METHODOLOGY.md` — opportunity-discovery methodology
- `docs/THESIS_TRANSACTION_GAPS.md` — canonical gap ontology
- `docs/OPPORTUNITY_SCORECARD.md` — scoring, gates and penalties
- `docs/ARCHITECTURE.md` — lifecycle and long-run graph architecture
- `docs/FIELD_VALIDATION_PLAYBOOK_XUZHOU.md` — field evidence discipline
- `docs/EXPERIMENT_*.md` — falsifiable commercial experiments
- `docs/research/` — evidence-backed research pools
- `docs/results/` — ranked / superseded result snapshots
- `prompts/` — versioned analysis/extraction/routing prompts
- `data/` — structured observations when justified
- `src/` — code only when repeated bottlenecks justify automation
- `tests/` — truth gates, evidence, scoring and lifecycle tests

## Current phase

**Phase 0 — Prove the discovery-and-validation method through real commitments and transactions.**

Success is not “we found many ideas” or “the software runs.”

Success is that the system repeatedly finds actor-specific transaction structures that survive real payer commitment, delivery, economics and repetition.
