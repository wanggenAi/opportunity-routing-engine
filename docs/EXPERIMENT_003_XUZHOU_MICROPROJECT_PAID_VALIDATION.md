# EXPERIMENT 003 — Xuzhou Managed SME Micro-Project Paid Validation

Status: `READY TO RUN / SECONDARY VERTICAL`

Date opened: 2026-09-08

## Objective

Test one specific transaction structure:

> Xuzhou SME / merchant need actor + payer → bounded project → capability routed through operator / GPT / student / freelancer → accepted delivery → payment.

This experiment remains valid, but it is **not the presumed top opportunity of the Opportunity Routing Engine**.

The broader `EXP-002` actor-first scan now compares personal, household, C2C, sponsored and enterprise opportunities under the same scorecard.

## Actor map

```text
Need actor: SME / merchant
Beneficiary: SME / merchant
Payer: SME / merchant
Capability provider: operator / AI / student / freelancer / specialist
Orchestrator: Opportunity Routing Engine operator
Transaction type: C2B / B2B / composite
```

## Core hypothesis

> A meaningful subset of Xuzhou businesses has small but real work that is delayed, poorly handled internally, or uneconomic to staff full-time; they will pay for a fixed-scope result if the task is clarified, matched to suitable capability, quality-controlled, and delivered with low risk.

## Initial task classes

Only test task classes with bounded acceptance criteria and low regulatory burden:

1. commercial / competitor / Chinese-Internet research;
2. Excel / data cleanup / analysis;
3. document extraction / classification / summarization workflows;
4. small automation scripts;
5. simple digital-content asset packages where acceptance criteria are explicit.

Do not test:

- employment placement;
- labor dispatch;
- safety-critical engineering;
- medical, legal, financial, accounting or other regulated professional work without qualified providers;
- open-ended IT support;
- complex customer-site integration;
- deceptive review manipulation / fake engagement;
- work requiring misuse of personal/private data.

## Test design

### Arm A — payer discovery

Target: 15–20 Xuzhou businesses with observable evidence of recurring small digital/content/data work.

For each target, capture:

- business type;
- observed signal;
- recent small task;
- current workaround;
- internal time/cost;
- desired output;
- acceptable deadline;
- acceptable price range if disclosed;
- trust/risk objections;
- whether a fixed-scope paid pilot is acceptable.

### Arm B — capability discovery

Target: 20–30 students / graduates / young skilled people.

Prioritize capabilities the operator can assess:

- research;
- Excel / data;
- Python / scripting;
- design / content;
- AI tool use;
- document processing.

Capture:

- capability claim;
- evidence / portfolio;
- test task result where needed;
- minimum acceptable fee;
- availability;
- deadline reliability;
- revision tolerance;
- confidentiality acceptance;
- prohibited/refused tasks.

## Transaction format

The operator must not sell “a student” or “a freelancer”. Sell a bounded result:

```text
Problem
→ written brief
→ fixed deliverables
→ fixed acceptance criteria
→ fixed or bounded price
→ capability selection
→ QA
→ delivery
→ acceptance
→ payment
```

## First-price guidance

Candidate pilot range: RMB 300–2,000 depending on task size.

This is a test range, not a market price claim.

## Success criteria

### Strong pass
Within 30 days:

- >=15 qualified payer-side conversations;
- >=5 reveal a real small task from the prior 90 days;
- >=3 accept the fixed-scope project model in principle;
- >=1 pays for a real pilot;
- paid pilot is delivered and accepted;
- direct contribution margin is positive;
- repeat/referral signal exists.

### Partial pass
Real task demand and payer interest repeatedly appear, but transaction is blocked by one isolatable factor such as price, trust proof, category, or payment mechanism.

### Fail / stop

- 20 qualified payer conversations produce zero paid pilot willingness;
- most tasks are too bespoke/on-site/regulated;
- customers prefer direct cheap freelancers and see no value in managed QA/routing;
- capable supply cannot meet quality/reliability requirements at viable economics;
- transaction disputes/legal structure make the model unattractive.

## Portfolio rule

EXP-003 may run because it is cheap and can produce real payment evidence, but it must **not** consume the entire research agenda.

In parallel, EXP-002 must continue scanning and comparing:

- B2C;
- C2C;
- household/family-sponsored;
- student/young-adult needs;
- pet-owner needs;
- elderly/caregiver/adult-child structures;
- value-conscious consumption migration;
- idle personal capability/resource exchanges;
- other actor-first hypotheses.

## Required records

For each transaction/test retain:

- need actor;
- beneficiary;
- payer;
- capability provider;
- transaction type;
- source/provenance;
- pain/task;
- current workaround;
- payment evidence;
- price signal;
- deliverables;
- acceptance criteria;
- quoted price;
- provider cost;
- status;
- outcome;
- failure reason;
- repeat/referral signal.

## Decision after experiment

If strong pass:
- validate this **vertical only**;
- repeat at least 5 transactions manually;
- compare its real economics against other actor-first candidates;
- automate only repeated bottlenecks.

If fail:
- do not build a marketplace;
- return to the actor-first EXP-002 ranking.
