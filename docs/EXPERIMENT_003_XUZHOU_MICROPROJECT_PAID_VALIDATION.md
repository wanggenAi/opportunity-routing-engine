# EXPERIMENT 003 — Xuzhou Managed Micro-Project Paid Validation

Status: `READY TO RUN`

Date opened: 2026-09-08

## Objective

Test whether Xuzhou SMEs / small merchants will pay for **bounded, result-oriented micro-projects** that are fulfilled through a managed capability-routing layer rather than a traditional full-time hire or open-ended outsourcing relationship.

This experiment tests money, not interest.

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

Good target signals include:

- currently hiring content, ecommerce, data or digital roles;
- youth shops reporting traffic / operating problems;
- small teams where full-time specialization is expensive;
- businesses with obvious repetitive public-facing information work;
- companies participating in digital / AI transformation ecosystems but where a full system project is unnecessary.

For each target, capture:

- business type;
- observed signal;
- recent small task;
- current workaround;
- internal time/cost;
- desired output;
- acceptable deadline;
- acceptable price range if disclosed;
- trust / risk objections;
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
- prohibited / refused tasks.

## Transaction format

The operator must not sell "a student" or "a freelancer".

Sell a result:

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

The provider may be:

- the operator + GPT;
- a student / freelancer;
- a specialist;
- a combination.

The customer buys the deliverable, not the identity of the labor source.

## First-price guidance

Do not optimize for maximum price in the first transaction.

Candidate pilot range: RMB 300–2,000 depending on task size.

This is a test range, not a market price claim.

A pilot must still compensate external contributors fairly and remain contribution-positive after direct delivery costs.

## Success criteria

### Strong pass
Within 30 days:

- >=15 qualified payer-side conversations;
- >=5 reveal a real small task from the prior 90 days;
- >=3 accept the fixed-scope project model in principle;
- >=1 pays for a real pilot;
- paid pilot is delivered and accepted;
- direct contribution margin is positive;
- customer would plausibly buy another bounded task or refer another payer.

### Partial pass
- real task demand is repeatedly observed;
- payer interest exists;
- no transaction occurs because of a narrow issue that can be isolated and retested (price, category, trust proof, contract/payment mechanism).

### Fail / stop
Stop or pivot the model if any of the following occurs:

- 20 qualified payer conversations produce zero paid pilot willingness;
- most tasks are too bespoke / on-site / regulated to standardize;
- customers consistently prefer direct cheap freelancers and see no value in managed QA/routing;
- capable supply cannot meet quality/reliability requirements at viable economics;
- transaction disputes or legal structure make the model unattractive.

## Required records

Create a non-sensitive ledger containing:

- `demand_id`
- target profile
- source / provenance
- pain / task
- payer evidence
- current workaround
- price signal
- deliverables
- acceptance criteria
- capability matched
- quoted price
- provider cost
- status
- outcome
- failure reason
- follow-up / repeat signal

Do not publish private customer communications or sensitive data to the public repository without permission. Public reporting should use anonymized summaries unless the underlying information is already public and appropriate to retain.

## Decision after experiment

If strong pass:
- promote XZ-001 to `A: TEST NOW / REPEAT`;
- repeat at least 5 transactions manually;
- identify the narrowest high-frequency task class;
- automate only the repeated bottleneck.

If fail:
- do not build a marketplace;
- return to EXP-002 ranking and promote the next candidate.
