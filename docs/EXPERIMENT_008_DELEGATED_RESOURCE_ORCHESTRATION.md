# EXPERIMENT 008 — Delegated Resource Orchestration Loop

Status: `ACTIVE / SYSTEM-LEVEL PRIORITY`

Date opened: 2026-09-10

## 1. Purpose

Test the core strategic thesis of the repository:

> Can one real paid outcome be completed when both demand acquisition and delivery are performed by routed capability providers, while the operator primarily designs and governs the transaction?

This is not a vertical experiment. Any lawful, low-risk, bounded transaction may serve as the sandbox.

Preferred first sandbox: a digital / knowledge / research / data / automation micro-project where acceptance is easy to define.

## 2. System hypothesis

A valuable outcome can be transformed into a network of bounded capability units such that:

1. a demand-source / BD capability finds or qualifies the payer;
2. the orchestrator turns the need into a transaction objective;
3. delivery is routed to one or more capability providers;
4. acceptance is explicit;
5. all economic flows are recorded;
6. routine acquisition and delivery do not depend on the operator personally performing them.

## 3. Operator constraint

For the canonical O2 attempt, the operator may:
- choose the target transaction class;
- define target/payer qualification;
- define the brief;
- decompose capability units;
- recruit/approve capability providers;
- design incentives/payouts;
- define acceptance;
- resolve exceptions;
- approve settlement;
- record learning.

The operator must **not** be counted as the primary performer of:
- payer cold outreach / routine BD;
- final delivery production.

If the operator temporarily rescues a failing capability, record the intervention, time and shadow cost. The run may still be useful but does not count as clean O2 PASS.

## 4. Preferred first transaction classes

Select only tasks that are low-risk and bounded, e.g.:
- research pack;
- competitor / public-market research;
- spreadsheet cleanup / transformation;
- document extraction / classification;
- simple non-sensitive automation;
- bounded web/data collection from permitted public sources;
- simple digital asset or analysis output.

Avoid in the first O2 proof:
- medical/legal/financial advice;
- regulated employment placement;
- childcare/eldercare/home access;
- transport/safety-critical work;
- large custom software build;
- open-ended consulting;
- tasks requiring the operator's personal credential or reputation to deliver.

## 5. Capability decomposition template

Minimum route:

```text
C1 DEMAND_SOURCE / BD
Input: target definition + offer boundary
Output: qualified payer / attended requirement conversation / signed task
Payout: explicit event-based commission

C2 REQUIREMENT / TRANSACTION ARCHITECTURE
Performed initially by orchestrator
Output: bounded brief + acceptance + budget + deadline

C3 DELIVERY
Input: accepted brief
Output: final deliverable
Payout: fixed/milestone accepted-output fee

C4 QA / ACCEPTANCE
May be orchestrator or delegated where objective
Output: acceptance evidence / defect list

C5 SETTLEMENT
Output: payer collection + provider/BD payouts + margin record
```

Additional capability units may be added only when necessary.

## 6. Hard gates

### Payer gate
At least one real payer commits money to the exact bounded output.

### Acquisition delegation gate
The qualified payer/transaction is sourced or advanced materially by a non-operator demand-source capability under explicit terms.

### Delivery delegation gate
The accepted deliverable is produced primarily by a non-operator capability provider.

### Acceptance gate
The payer/authorized acceptor confirms the agreed acceptance criteria are met.

### Settlement gate
Payer inflow and provider/acquisition payouts are recorded.

## 7. PASS levels

### `O1 / L4 partial pass`
- real payer;
- delivery delegated;
- accepted and settled;
- operator still performs acquisition.

Useful but does not prove target model.

### `O2 / L4 system PASS`
- real payer commitment;
- demand acquisition materially delegated;
- delivery delegated;
- accepted output;
- settlement completed;
- operator shadow labor recorded;
- no material legal/trust failure.

### `L5 strong commercial signal`
- same payer repeats or refers another payer under comparable economics.

### `L6 orchestration proof`
At least one of:
- second delegated transaction repeats with similar template;
- provider is replaced while acceptance still succeeds;
- alternate demand-source route produces a valid payer;
- alternate delivery route succeeds without redesigning the transaction.

## 8. Economic record

For every attempt:

```text
payer_inflow:
demand_source_payout:
delivery_provider_payout:
other_provider_payouts:
resource_costs:
qa_trust_costs:
refund_failure_reserve:
other_operating_costs:
cash_contribution_margin:
operator_hours_transaction_architecture:
operator_hours_execution_rescue:
operator_shadow_rate:
operator_shadow_cost:
normalized_orchestration_margin:
```

Early O2 proof may accept low/negative normalized margin if the learning cost is bounded and explicit.

Do not call it repeatable until normalized economics are plausible.

## 9. Capability-provider record

For each provider:

```text
provider_id_anonymized:
capability_unit:
claim:
proof:
quoted_price:
actual_payout:
accepted_output: YES/NO
revision_count:
late: YES/NO
replacement_needed: YES/NO
reliability_learning:
```

No unnecessary personal data in the public repository.

## 10. Demand-source record

```text
source_provider_id_anonymized:
target_definition:
channel:
payout_rule:
contacts_attempted_if_known:
qualified_leads:
attended_meetings:
real_payer_commitments:
payout:
quality_notes:
```

The point is to measure whether demand access itself can become a capability unit.

## 11. Failure conditions

This experiment fails in a transaction class if:
- no real payer can be acquired economically;
- acquisition cannot be bounded/delegated;
- delivery cannot be bounded/delegated;
- provider revisions/coordination exceed buyer value;
- buyer can bypass immediately and orchestrator creates no recurring value;
- acceptance remains subjective/unbounded;
- operator repeatedly rescues core execution;
- normalized economics cannot plausibly become positive;
- legal/trust/safety boundaries make routing inappropriate.

A failed transaction class does not falsify the entire engine. Record which capability/interface failed and test a better-bounded class.

## 12. Relationship to existing experiments

### EXP-003
Use as a source of bounded SME/merchant buyer problems and real paid output tests.

### EXP-007
Use as a source of capability providers and outcome-linked capability supply.

EXP-003 and EXP-007 can feed one EXP-008 transaction while retaining separate evidence records.

### EXP-006
May also serve as an O2 sandbox if merchant BD, participant recruitment, venue capability and event execution are delegated. It is not preferred for the first O2 proof because ticket size and coordination complexity may make normalized economics harder.

### EXP-004
Not preferred for initial O2 proof due home-access/safety trust burden.

## 13. Build rule

No marketplace/platform build.

The first implementation is a manual orchestration ledger plus explicit capability contracts/briefs.

Software is authorized only after repeated transactions expose a stable bottleneck.

## 14. Governing question

> **Can the system complete a real accepted transaction by routing people/resources into capability slots, while the operator remains primarily the architect rather than the worker?**
