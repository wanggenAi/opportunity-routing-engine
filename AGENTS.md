# AGENTS.md

Instructions for AI agents, coding assistants, and human contributors working in this repository.

## Prime directive

The objective is to build a truthful, evidence-driven system that can repeatedly:

1. observe social/market change;
2. detect unmet or migrating demand;
3. identify the real payer and payment behavior;
4. discover capabilities/resources that can solve the demand;
5. design a bounded transaction;
6. test it cheaply;
7. learn from real outcomes.

Do not optimize for code volume, idea count, or impressive narratives. Optimize for **commercial truth**.

## Source of truth

Before changing business logic, read:

1. `docs/FORMAL_TRUTH.md`
2. `docs/METHODOLOGY.md`
3. `docs/OPPORTUNITY_SCORECARD.md`
4. `docs/ARCHITECTURE.md`
5. the relevant `docs/EXPERIMENT_*.md`

When evidence changes a major assumption, update `docs/FORMAL_TRUTH.md` in the same change.

## Non-negotiable truth rules

- Never fabricate demand, payment, buyer, supplier, user, pricing, transaction, market, contact, or capability data.
- `UNKNOWN` / missing is never equivalent to pass.
- A complaint is not proof of demand.
- A trend is not proof of willingness to pay.
- Market size is not proof that we can acquire a customer.
- One paid transaction validates possibility, not repeatability.
- LLM confidence is not commercial evidence.
- Keep provenance and timestamps wherever practical.
- Preserve contradictions rather than smoothing them away.

## Evidence hierarchy

Prefer direct behavioral evidence over narrative evidence.

Stronger examples:

- real purchases;
- paid substitutes;
- procurement/RFQ/tender activity;
- repeated marketplace tasks;
- hiring specifically to solve the problem;
- explicit budgets;
- costly manual workarounds;
- repeat transactions.

Weaker examples that require corroboration:

- complaints;
- social discussion;
- survey answers;
- search volume;
- macro indicators;
- expert predictions.

## Opportunity gates

Before expensive build-out, require evidence for:

- `PAIN`
- `FREQUENCY`
- `PAYMENT`
- `SUPPLY`
- `TRANSACTIONABILITY`
- `DEFENSIBILITY`

`PAYMENT` and `TRANSACTIONABILITY` are hard gates.

## Development approach

1. Define the social/market signal.
2. Form a falsifiable demand hypothesis.
3. Identify the payer.
4. Collect real behavioral/payment evidence.
5. Map current solutions and why they are insufficient.
6. Identify possible capabilities/resources.
7. Define the smallest real transaction test.
8. Set success/failure/stop rules.
9. Run the test and record outcomes.
10. Automate only repeated bottlenecks.

## Capability routing rules

Do not assume every problem requires a company or supplier. Candidate solutions may be:

- AI;
- the operator;
- a freelancer/student/specialist where lawful;
- a company/manufacturer;
- software/product;
- equipment/inventory/assets;
- a composite of multiple capabilities.

Do not route regulated or safety-sensitive work to unqualified providers.

## Platform discipline

Do **not** build a broad marketplace merely because the conceptual model supports one.

Required maturity path:

```text
manual transactions
→ repeated transaction pattern
→ stable demand template
→ stable capability template
→ measurable routing advantage
→ automation
→ platform only after sufficient density
```

## Code principles

- Small modules, explicit schemas, deterministic validation where possible.
- AI classifications must expose evidence/input and remain reviewable.
- Separate raw signals from derived hypotheses.
- Separate evidence from score.
- Separate opportunity score from business decision.
- Tests must protect truth gates and lifecycle transitions.
- Never commit secrets, credentials, prohibited personal data, or paid datasets without storage rights.

## Compliance

Respect source terms, privacy, anti-spam rules, labor/employment licensing, financial/medical/legal regulation, platform rules, and applicable law.

Where a transaction requires a licensed professional or regulated entity, the engine may route to qualified parties but must not pretend the operator is licensed.

## Success definition

The repository is succeeding only if the process increasingly identifies opportunities that lead to:

- real payer engagement;
- paid pilots;
- completed delivery;
- acceptable margins;
- repeat transactions;
- proprietary learning that improves future routing.
