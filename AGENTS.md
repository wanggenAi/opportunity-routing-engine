# AGENTS.md

Instructions for AI agents, coding assistants, and human contributors working in this repository.

## Prime directive

The objective is to build a truthful, evidence-driven **actor-first social demand and capability routing system** that can repeatedly:

1. observe social/market change;
2. identify the specific actors/groups affected;
3. detect unmet or migrating needs;
4. separate need actor, beneficiary and payer;
5. identify real payment/workaround behavior;
6. discover capabilities/resources that can solve the need;
7. design a bounded transaction;
8. test it cheaply;
9. learn from real outcomes.

Do not optimize for code volume, idea count, enterprise use cases, or impressive narratives. Optimize for **commercial truth**.

## Source of truth

Before changing business logic, read:

1. `docs/FORMAL_TRUTH.md`
2. `docs/ACTOR_MODEL.md`
3. `docs/METHODOLOGY.md`
4. `docs/OPPORTUNITY_SCORECARD.md`
5. `docs/ARCHITECTURE.md`
6. the relevant `docs/EXPERIMENT_*.md`

When evidence changes a major assumption, update `docs/FORMAL_TRUTH.md` in the same change.

## Non-negotiable truth rules

- Never fabricate actors, needs, payment, pricing, transactions, contacts, capabilities, market or outcome data.
- `UNKNOWN` / missing is never equivalent to pass.
- A complaint is not proof of demand.
- A need actor is not automatically the payer.
- The beneficiary is not automatically the payer.
- A trend is not proof of willingness to pay.
- Market size is not proof that we can acquire a user/payer.
- One paid transaction validates possibility, not repeatability.
- LLM confidence is not commercial evidence.
- Keep provenance and timestamps wherever practical.
- Preserve contradictions rather than smoothing them away.

## Actor-first requirement

For every serious opportunity explicitly map:

- `NEED_ACTOR`
- `BENEFICIARY`
- `PAYER`
- `CAPABILITY_PROVIDER`
- `RESOURCE_OWNER` where relevant
- `SPONSOR` where relevant
- `ORCHESTRATOR`

Do not default to enterprises as the payer or solution provider.

Candidate structures may be:

- `B2B`
- `B2C`
- `C2C`
- `C2B`
- `SPONSORED / THIRD-PARTY-PAYER`
- `MULTI-SIDED`

A broad social scan is considered biased if it repeatedly collapses back into enterprise problems without comparative evidence.

## Evidence hierarchy

Prefer direct behavioral evidence over narrative evidence.

Strong examples include:

- real individual/household purchases;
- bookings, subscriptions and paid convenience services;
- paid substitutes;
- rental/repair/second-hand transactions;
- marketplace/gig tasks;
- family members paying for another person's outcome;
- procurement/RFQ/tender activity;
- hiring specifically to solve the problem;
- explicit budgets;
- costly manual/family workarounds;
- repeat transactions.

Weaker evidence requiring corroboration:

- complaints;
- social discussion;
- survey answers;
- search volume;
- macro indicators;
- expert predictions.

## Opportunity gates

Before expensive build-out require evidence for:

- `PAIN`
- `FREQUENCY`
- `PAYER_CLARITY`
- `PAYMENT_EVIDENCE`
- `SUPPLY`
- `TRANSACTIONABILITY`
- `DEFENSIBILITY`

`PAYER_CLARITY`, `PAYMENT_EVIDENCE` and `TRANSACTIONABILITY` are hard gates.

## Development approach

1. Define the actor/group.
2. Define the social/market change affecting that actor.
3. Observe changed behavior and friction.
4. Form a falsifiable need hypothesis.
5. Identify beneficiary and alternative payer candidates.
6. Collect real behavioral/payment evidence.
7. Map current workarounds and why they are insufficient.
8. Identify possible capabilities/resources.
9. Compare transaction structures.
10. Define the smallest real test.
11. Set success/failure/stop rules.
12. Run the test and record outcomes.
13. Automate only repeated bottlenecks.

## Capability routing rules

Do not assume every problem requires a company or supplier. Candidate solutions may be:

- AI;
- the operator;
- another individual;
- student/freelancer/specialist where lawful;
- skilled worker/local helper;
- company/manufacturer;
- software/product;
- equipment/inventory/vehicle/space/assets;
- institution;
- a composite of multiple capabilities.

Do not route regulated or safety-sensitive work to unqualified providers.

## Vulnerable / high-trust groups

Opportunities involving children, elderly people, medical issues, financial matters, intimate personal data, transport/safety or home access require elevated trust and compliance review.

Commercial attractiveness never overrides safety or legal requirements.

## Platform discipline

Do **not** build a broad marketplace merely because the conceptual model supports one.

Required maturity path:

```text
manual actor research
→ real bounded transactions
→ repeated transaction pattern
→ stable need template
→ stable payer model
→ stable capability template
→ measurable routing/trust advantage
→ automation
→ platform only after sufficient density
```

## Code principles

- Small modules, explicit schemas, deterministic validation where possible.
- AI classifications must expose evidence/input and remain reviewable.
- Separate raw signals from actors and derived hypotheses.
- Separate need actor from payer.
- Separate evidence from score.
- Separate opportunity score from business decision.
- Tests must protect truth gates and lifecycle transitions.
- Never commit secrets, credentials, prohibited personal data, or paid datasets without storage rights.

## Success definition

The repository is succeeding only if the process increasingly identifies opportunities that lead to:

- real actor engagement;
- real payer engagement;
- paid pilots/transactions;
- completed delivery;
- acceptable margins;
- repeat/referral;
- proprietary learning that improves future actor/capability routing.
