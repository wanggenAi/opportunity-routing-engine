# Transaction Gap Thesis

Status: `ACTIVE WORKING THESIS`

Date: 2026-09-08

## Purpose

The Opportunity Routing Engine should not only ask whether demand and supply exist. Many markets already contain both, yet transactions still fail because the mechanism between them is weak.

This document defines four cross-cutting gap classes that can create commercial opportunity across B2B, B2C, C2C, C2B, sponsored and multi-sided markets.

## 1. Demand gap

A meaningful need exists but current supply is missing, insufficient, poorly fitted, or inaccessible.

Examples:
- a new behavior creates a service category before providers adapt;
- a locality has demand but no suitable local operator;
- a user needs an outcome that existing products do not provide.

Core question:
> What outcome is repeatedly wanted but still hard to obtain?

## 2. Capability gap / idle-capability mismatch

Useful capability exists but is underutilized, hard to discover, badly packaged, or disconnected from a payer.

Examples:
- students learn AI, data, design or repair skills but cannot access bounded paid work;
- retirees hold valuable skills but lack a route to appropriate demand;
- merchants have idle space during off-peak hours;
- vehicles, equipment, inventory or rooms are idle while another actor needs temporary access.

Core question:
> What useful skill, resource, time or asset is idle, and who is paying elsewhere for the same outcome?

## 3. Price / economic gap

The desired outcome exists, but the current way of obtaining it is too expensive relative to the user's willingness or ability to pay.

Common patterns:
- premium → value-for-money substitute;
- ownership → rental / shared use;
- replacement → repair / second-hand;
- full-time headcount → fixed project;
- manual professional labor → AI-assisted workflow;
- large commitment → small trial / pay-per-use.

Core question:
> Can the same outcome be delivered with a structurally lower cost rather than merely a lower margin?

## 4. Trust gap

Demand and supply both exist, but actors hesitate to transact because quality, identity, safety, responsibility, evidence or recourse are unclear.

This can be a stronger opportunity than simple discovery.

Typical trust components:
- identity / qualification verification;
- service checklist;
- clear scope and acceptance criteria;
- timestamped or auditable evidence;
- privacy / access boundaries;
- deposits / payment rules;
- abnormal-event escalation;
- service history / reputation;
- dispute / refund boundaries;
- insurance or qualified-party routing where appropriate.

Examples:
- pet owner can find a sitter but is reluctant to let a stranger enter the home;
- household can find a service worker but cannot predict quality;
- second-hand buyer can find a device but cannot verify hidden defects;
- adult child can find elder helpers but worries about safety/accountability;
- remote customer can find local executors but cannot verify what happened on site.

Core question:
> If both sides already exist, what prevents a stranger-to-stranger transaction from feeling safe enough to happen?

## 5. Payer shift / sponsor gap

The person with the need is not always the economically strongest payer.

Every opportunity must test alternative payer structures:

```text
Need actor != Beneficiary != Payer != Capability provider
```

Potential payer shifts:
- elderly beneficiary → adult child payer;
- student beneficiary → employer / sponsor / institution payer;
- youth participant → venue sponsor because foot traffic has value;
- resident beneficiary → government / community procurement;
- end consumer → advertiser / supplier / transaction counterparty;
- worker beneficiary → employer training budget.

The existence of a third-party payer is not automatically good. The engine must verify that the payer captures enough economic value to justify payment.

## 6. Orchestrator value

The system should ask what value remains after simple introductions are removed.

Strong orchestrator value may include:
- demand clarification;
- requirement standardization;
- trust creation;
- capability screening;
- composite routing;
- fixed deliverables;
- QA;
- evidence capture;
- exception handling;
- payment coordination;
- outcome history;
- repeatability learning.

Weak orchestrator value:
> "I know someone; here is their contact information."

## 7. Canonical gap record

Every serious opportunity should include:

```text
Need actor:
Beneficiary:
Payer:
Capability provider:
Primary gap type: DEMAND / CAPABILITY / PRICE / TRUST
Secondary gap types:
Current workaround:
Why transaction does not already happen efficiently:
Payer-shift candidates:
Orchestrator value:
Evidence:
Hard gates:
Smallest decisive test:
Outcome:
```

## 8. Governing principle

**Do not assume opportunity requires missing supply. Sometimes the economic value is in making an existing transaction cheaper, safer, clearer, or easier to complete.**
