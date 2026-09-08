# EXPERIMENT 004 — Xuzhou Trusted Pet-Care Validation

Status: `READY FOR FIELD VALIDATION`

Date opened: 2026-09-08

## Objective

Test whether Xuzhou pet owners will pay for a **managed trust layer** around local pet-care transactions, rather than simply finding an informal sitter directly.

This is the first actor-first experiment whose primary payer is an individual consumer.

## Actor map

- `NEED_ACTOR`: pet owner temporarily unable to care for pet
- `BENEFICIARY`: pet + owner
- `PAYER`: pet owner
- `CAPABILITY_PROVIDER`: vetted nearby sitter / student / flexible worker / pet-service operator
- `ORCHESTRATOR`: requirement definition + vetting + matching + checklist + service evidence + exception handling + outcome history
- `TRANSACTION_TYPE`: B2C / C2C / managed multi-sided local service

## Core hypothesis

> Xuzhou already has pet-care demand and informal supply. A meaningful subset of pet owners will prefer or pay for a more trusted, standardized transaction because stranger access, reliability, evidence and pet-specific execution are more important than the lowest possible price.

## What is NOT being tested

- veterinary treatment;
- medication administration that requires professional expertise;
- animal transport without suitable controls;
- aggressive / dangerous animal handling;
- long-term boarding infrastructure;
- building a pet-care app;
- recruiting a large provider network.

## Phase A — payer interviews

Target: 15–20 qualified Xuzhou pet owners.

A qualified owner should have at least one of:
- prior pet boarding / home-feeding / dog-walking purchase;
- upcoming travel / work absence;
- prior need to ask friends/family for pet care;
- concern about pet-store boarding or stranger home access.

Capture:
- pet type / count (non-sensitive summary only);
- neighborhood;
- last absence / care scenario;
- current workaround;
- amount paid or time/favor cost;
- how provider was found;
- biggest trust concern;
- required proof before giving home access;
- required service evidence;
- acceptable per-visit/day range;
- willingness to pay extra for verification / managed transaction;
- repeat frequency;
- deal-breakers.

## Phase B — supply interviews

Target: 10–15 potential providers.

Capture:
- location / service radius;
- pet experience;
- proof / references;
- service types accepted;
- minimum fee;
- travel cost/time;
- availability;
- animals/tasks refused;
- willingness to use checklist + timestamped evidence;
- emergency escalation acceptance;
- identity / trust verification willingness.

## Phase C — first manual paid transactions

Only proceed if Phase A shows meaningful willingness.

Target: 1–3 low-risk transactions.

Minimum transaction controls:
- written pet profile;
- exact visit window;
- exact checklist;
- water / food / litter / walk tasks defined;
- timestamped arrival / completion evidence;
- photo/video evidence agreed in advance;
- no medication unless explicitly safe and within provider capability;
- emergency contact and escalation rule;
- key / access handling protocol;
- payment and cancellation rule;
- no undisclosed extra services.

## Strong pass

Within 30 days:
- >=15 qualified pet-owner interviews;
- >=8 show recurring or meaningful care need;
- >=5 prefer a verified/managed option over an unmanaged stranger transaction;
- >=3 accept a plausible paid price structure;
- >=1 real paid transaction completes safely and is accepted;
- provider economics are positive;
- customer expresses repeat or referral intent.

## Partial pass

Demand exists but the value concentrates in one specific trust feature, such as:
- identity verification;
- home-entry evidence;
- pet-sitter references;
- standardized checklist;
- emergency backup;
- holiday capacity.

Narrow the model to that feature and retest.

## Fail / stop

Stop or redesign if:
- 20 qualified owners show no preference for managed trust;
- everyone prefers friends/family or known pet stores;
- willingness to pay cannot cover provider + coordination cost;
- home-access / pet-liability risks cannot be bounded;
- provider reliability is too weak;
- repeat frequency is too low for viable acquisition economics.

## Economics fields

For each test transaction record:
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
2. identify the highest-value trust controls;
3. build only the repeated trust/routing workflow;
4. test one neighborhood/campus-adjacent cluster before wider Xuzhou expansion.

If fail:
Return to EXP-002 and promote the next actor-first candidate. Do not rationalize failure into a platform build.
