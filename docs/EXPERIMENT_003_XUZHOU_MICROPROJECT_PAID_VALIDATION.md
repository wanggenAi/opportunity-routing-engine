# EXPERIMENT 003 — Xuzhou Managed SME Micro-Project Paid Validation

Status: `ACTIVE / PREFERRED ORCHESTRATION SANDBOX`

Date opened: 2026-09-08

Strategic kernel: `docs/RESOURCE_ORCHESTRATION_KERNEL.md`.

## Objective

Test a bounded buyer-side transaction structure that can feed the system-level `EXP-008`:

> SME / merchant payer → bounded desired outcome → transaction architecture → decomposed capability units → routed provider(s) → accepted delivery → settlement.

The operator is **not** the default salesperson or final delivery provider.

This experiment validates buyer/output/payment mechanics. `EXP-007` may supply capability providers. `EXP-008` measures whether acquisition + delivery can both be delegated.

## Actor / role map

```text
Need actor: SME / merchant
Beneficiary: SME / merchant
Payer: SME / merchant
Demand-source capability provider: connector / commissioned BD / referral partner / inbound channel / other route
Capability provider: student / freelancer / specialist / company / AI-assisted provider / composite
Orchestrator: requirement architecture + decomposition + routing + incentive + QA/acceptance governance
Transaction type: C2B / B2B / composite
```

## Core hypothesis

A meaningful subset of Xuzhou businesses has small but real work that is delayed, poorly handled internally, or uneconomic to staff full-time. They will pay for a fixed/bounded result when the orchestration layer can:
- clarify the real outcome;
- define acceptance;
- route suitable capability;
- manage quality/replacement;
- reduce coordination risk.

## Initial task classes

Prefer low-risk tasks with bounded acceptance:

1. commercial / competitor / public-Internet research;
2. Excel / data cleanup / analysis;
3. document extraction / classification workflows;
4. small non-sensitive automation scripts;
5. simple digital-content assets with explicit acceptance.

Avoid employment placement, labor dispatch, regulated professional work without qualified providers, safety-critical work, open-ended support, complex on-site integration, deceptive engagement or misuse of private data.

## Phase A — demand-source capability

Do **not** assume the operator personally cold-calls 15–20 businesses.

Test one or more routable demand-access methods:
- commissioned local BD;
- industry connector/referrer;
- accounting/software/service provider with adjacent clients;
- association/community operator;
- online inbound / public task source;
- trusted introduction channel.

Define the acquisition capability explicitly, e.g.:

```text
Input: target definition + allowed offer
Output: attended qualified requirement conversation
Qualification: payer/decision route exists + recent bounded task/problem
Payout: per qualified attended meeting or converted paid pilot
Anti-spam: no payout for unqualified contact lists
```

Target evidence: >=15 qualified payer conversations across the validation cycle, regardless of whether they came from one or multiple demand-source providers.

The operator may participate in requirement architecture. That is different from being the default lead generator.

## Phase B — transaction objective

For every real task discovered, convert vague need into:

```text
payer:
desired outcome:
inputs:
required final output:
acceptance criteria:
deadline:
price / budget:
trust / data boundary:
revision boundary:
failure / refund condition:
```

Do not sell a student/freelancer. Sell an accepted outcome.

## Phase C — capability decomposition and routing

For each paid candidate, define required `CapabilityUnit`s.

Example:

```text
requirement architecture
→ data extraction/cleaning
→ analysis/implementation
→ QA
→ acceptance
```

Each external capability unit should define input, output, acceptance, payout, deadline and replacement rule.

Use `docs/templates/CAPABILITY_UNIT_TEMPLATE.md`.

`EXP-007` may be used to source/prove capability providers.

## Phase D — paid pilot

At least one real payer commits money to an exact bounded output.

Delivery should preferably be performed by a non-operator provider so that EXP-003 can contribute evidence toward EXP-008.

Record:
- payer inflow;
- demand-source payout;
- provider payout(s);
- QA/resource costs;
- operator hours by function;
- operator shadow cost;
- acceptance;
- settlement;
- repeat/referral.

## Price guidance

Initial pilot range remains `RMB 300–2,000` for small tasks unless real evidence supports another amount.

This is a test range, not a market-price claim.

## PASS criteria

### Commercial PASS
Within the validation cycle:
- >=15 qualified payer conversations;
- >=5 real recent bounded tasks discovered;
- >=3 accept fixed/bounded-result structure in principle;
- >=1 real paid pilot;
- pilot delivered and accepted;
- settlement completed.

### Strategic orchestration PASS
In addition:
- demand acquisition materially comes from a non-operator capability route;
- final delivery is primarily performed by a non-operator capability provider;
- operator shadow labor is recorded;
- orchestrator contributes recurring value beyond introduction.

If these hold, link the transaction to `EXP-008 O2/L4` evidence.

### Strong follow-up
- repeat/referral;
- second transaction using same task template;
- alternate provider or provider replacement succeeds;
- normalized orchestration margin is plausibly positive.

## Stop / downgrade rules

Stop or redesign if:
- 20 qualified payer conversations produce zero paid-pilot willingness;
- tasks are mostly unbounded/on-site/regulated;
- buyer sees no value beyond direct cheap provider access;
- capability supply cannot meet acceptance at viable economics;
- revisions/coordination destroy normalized margin;
- acquisition cannot be delegated economically;
- operator repeatedly must rescue delivery;
- bypass leaves no recurring orchestration value.

## Economic truth

Do not report profit using free founder labor.

```text
payer inflow
- demand-source payout
- provider payouts
- resource / QA / trust / failure costs
= cash contribution margin

cash contribution margin
- operator shadow labor
= normalized orchestration margin
```

## Relationship to broader engine

This remains one sandbox, not the system identity.

It is currently preferred because many digital/knowledge tasks are:
- easy to bound;
- remotely deliverable;
- measurable;
- supplied by multiple provider classes;
- relatively low legal/safety risk;
- suitable for testing provider replacement.

That is **orchestration fit**, not enterprise-first bias.

## Build rule

No freelancer/project marketplace before repeated accepted transactions, delegated acquisition/delivery and provider replacement evidence exist.

## Governing question

> **Will a real payer buy a bounded result, and can the engine source the payer and route delivery without the operator becoming the salesperson or worker?**
