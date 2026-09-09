# EXPERIMENT 004 — Xuzhou Trusted Pet-Care Validation

Status: `ACTIVE TRUST-GATE VALIDATION / NO HOME-ENTRY TRANSACTION YET`

Date opened: 2026-09-08
Last priority review: 2026-09-10

## V2 score correction

`docs/results/EXP_002_XUZHOU_ACTOR_FIRST_RANKING_V2_2026-09-10.md` corrects the earlier ranking.

Current scorecard treatment:
- raw score: `78`;
- canonical penalty: `-20 unresolved home-access / physical-safety trust risk`;
- current final: `58`;
- `G3 Legal/trust/safety = CONDITIONAL`.

This experiment is **not rejected**. Its purpose is now explicitly to test whether a trust layer can economically resolve enough of that risk to justify rescoring.

Do not treat the trust mechanism as already proven merely because trust is the product thesis.

## Objective

Test whether Xuzhou pet owners will pay for a **managed trust layer** around local pet-care transactions, rather than simply finding an informal sitter directly.

This is an actor-first individual-payer trust experiment.

## Actor map

- `NEED_ACTOR`: pet owner temporarily unable to care for pet
- `BENEFICIARY`: pet + owner
- `PAYER`: pet owner
- `CAPABILITY_PROVIDER`: vetted nearby sitter / student / flexible worker / pet-service operator
- `RESOURCE_OWNER`: provider time/local presence; owner controls home access
- `ORCHESTRATOR`: requirement definition + vetting + matching + checklist + service evidence + exception handling + outcome history
- `TRANSACTION_TYPE`: B2C / C2C / managed multi-sided local service
- `PRIMARY_GAP`: TRUST_GAP
- `SECONDARY_GAPS`: TIME_GAP / GEOGRAPHY_GAP / COORDINATION_GAP

## Core hypothesis

> Paid pet-care demand exists, but a meaningful subset of owners may refuse unmanaged stranger transactions because home access, reliability, evidence and responsibility are unclear. A managed trust layer is valuable only if it increases willingness to transact enough to cover provider + coordination + risk cost.

## Current external evidence

Paid home pet-feeding is an established category, and 2026 reporting documents:
- real per-visit prices;
- deposits / contract-like service rules;
- holiday demand spikes;
- identity / home-entry / privacy / pet-safety concerns;
- provider radius pricing and travel economics.

Source:
- https://www.jsjc.gov.cn/yaowen/202602/t20260227_1311217.shtml

This is category evidence, not proof of Xuzhou conversion.

## What is NOT being tested

- veterinary treatment;
- medication administration requiring professional expertise;
- animal transport without suitable controls;
- aggressive / dangerous animal handling;
- long-term boarding infrastructure;
- building a pet-care app;
- recruiting a large provider network;
- proving demand by asking generic "would you use this" questions.

## Phase A — payer / trust interviews

Target: 15–20 qualified Xuzhou pet owners.

A qualified owner should have at least one of:
- prior pet boarding / home-feeding / dog-walking purchase;
- upcoming travel / work absence;
- prior need to ask friends/family for pet care;
- concern about boarding or stranger home access.

Capture:
- last absence / care scenario;
- current workaround;
- amount paid or time/favor cost;
- how provider was found;
- whether an unknown sitter is categorically refused;
- exact home-access concern;
- proof required before access;
- service evidence required;
- acceptable per-visit/day range;
- willingness to pay extra for verification / managed transaction;
- repeat frequency;
- deal-breakers.

Do not collect exact home addresses, access codes, keys, or unnecessary private information in the public repository.

## Phase B — supply / economics interviews

Target: 10–15 potential providers with actual animal-care experience.

Capture:
- service radius;
- proof / references;
- service types accepted;
- minimum fee;
- travel cost/time;
- availability / holiday pricing;
- animals/tasks refused;
- willingness to follow checklist + timestamped evidence;
- emergency escalation acceptance;
- identity / reference verification willingness;
- liability expectations.

### Supply kill signals
- travel time destroys low-ticket economics;
- provider refuses evidence/standards;
- reliable backup cannot be arranged;
- providers accept animals/tasks outside safe capability boundaries.

## Phase B2 — trust-control gate

Before any home-entry transaction, define and test the minimum trust controls with owners/providers.

Candidate controls:
- identity verification;
- references / prior outcome history;
- written task scope;
- pet profile and explicit exclusions;
- agreed entry/exit evidence;
- timestamped task evidence;
- privacy / no-recording boundaries where appropriate;
- owner-secured valuables;
- key/access handling rule;
- cancellation/no-show rule;
- emergency escalation rule;
- responsibility / dispute boundary;
- qualified professional escalation where needed.

### Trust-control PASS
Proceed toward one low-risk transaction only when:
- multiple qualified owners state the defined controls materially change willingness to transact;
- provider accepts the controls;
- the transaction does not require prohibited/high-risk animal care;
- responsibility boundaries are understood;
- price can still cover provider + travel + coordination economics.

A checklist alone is not PASS.

## Phase C — first manual paid transaction

Only proceed after Phase A + Phase B + Phase B2 gates pass.

Target: one low-risk transaction first. Expand to 1–3 only after the first completes safely.

Minimum transaction controls:
- written pet profile;
- exact visit window;
- exact checklist;
- food/water/litter/walk tasks defined;
- timestamped arrival/completion evidence as agreed;
- emergency contact and escalation rule;
- explicit access-handling protocol;
- payment/cancellation rule;
- no undisclosed extra services;
- no medication/professional treatment beyond safe authorized capability.

## Strong pass

Within the validation cycle:
- >=15 qualified owner interviews;
- >=8 show recurring or meaningful care need;
- >=5 prefer the defined managed controls over unmanaged stranger hiring;
- >=3 accept a plausible paid price structure;
- trust-control gate passes;
- >=1 real paid transaction completes safely and is accepted;
- provider economics are positive;
- customer gives repeat/referral commitment or behavior.

Only then rescore the `-20` trust penalty. Do not automatically remove all 20 points; use evidence to determine whether risk is actually resolved.

## Partial pass

Demand exists but economic value concentrates in one specific trust feature, such as:
- identity verification;
- home-entry evidence;
- sitter references;
- standardized checklist;
- emergency backup;
- holiday capacity.

Narrow to that feature and retest.

## Fail / stop

Stop or redesign if:
- 20 qualified owners show no preference for managed trust;
- friends/family/known stores solve the problem with little residual friction;
- willingness to pay cannot cover provider + travel + coordination;
- home-access / pet-liability responsibility cannot be bounded;
- provider reliability is too weak;
- repeat frequency is too low for viable acquisition economics;
- trust controls add process but do not change real commitment.

## Economics fields

For each eventual transaction record:
- customer price;
- provider payout;
- transport / consumable cost;
- operator time;
- gross contribution;
- acquisition source;
- repeat likelihood;
- issue / dispute cost.

## Public-repo rule

Store only anonymized customer/provider observations in the public repository unless explicit permission exists. Never publish home addresses, access codes, keys, private phone numbers or private messages.

## Decision after experiment

If strong pass:
1. repeat manually to at least 5 successful transactions;
2. identify which trust controls actually changed conversion;
3. update scorecard penalty from evidence;
4. build only the repeated trust/routing workflow;
5. test one local cluster before wider expansion.

If fail:
Mark the current transaction design `REJECTED / DORMANT`, return evidence to EXP-002, and promote the next actor-first candidate. Do not rationalize failure into a platform build.
