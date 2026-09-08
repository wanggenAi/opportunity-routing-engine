# EXPERIMENT 002 — Xuzhou-First Social Opportunity Scan

Status: `ACTIVE`

Date opened: 2026-09-08

## Objective

Test whether the Opportunity Routing Engine can convert current social/market change into a ranked set of **transaction-worthy** opportunities rather than merely interesting ideas.

The first geographic observation field is **Xuzhou, Jiangsu** because the operator is currently local and can validate online hypotheses through rapid in-person visits to universities, commercial districts, communities, industrial parks, small businesses, factories, and public-service ecosystems.

Xuzhou is the first field laboratory, not the permanent scope of the project.

## Core question

> Can a structured Xuzhou-first scan identify opportunities with clear payers, observable payment behavior, accessible supply/capability, bounded delivery, and a realistic path to first cash within 30–60 days?

## Phase A — Xuzhou baseline scan

Scan at least 10 distinct local change/mismatch domains, including but not limited to:

1. university students / graduates with underutilized skills or time;
2. SMEs that need small digital/content/data tasks but do not justify full-time headcount;
3. youth shops and small merchants with customer-acquisition or operating friction;
4. AI substitution of repetitive knowledge work;
5. skills training participants who still lack real paid projects;
6. flexible employment / project-based work;
7. idle assets, inventory, equipment, and second-hand migration;
8. aging / household service coordination;
9. tourism and night-economy demand around local merchants;
10. local-vs-remote execution or information gaps;
11. value-conscious consumption and repair/rental/used alternatives;
12. domestic or cross-border demand-capability mismatch.

The scan must not force an opportunity in every domain.

## Phase B — local field verification

Only the highest-ranked hypotheses may proceed to field verification.

Possible verification targets include:

- university students / student organizations / career centers;
- youth shops and local merchants;
- SME owners and functional managers;
- skill-night-school participants or training providers;
- industrial park firms;
- existing service providers;
- public or regulated institutions where appropriate.

Field interviews must test a specific commercial unknown. Do not perform generic networking visits without a decision question.

## Required evidence per domain

For each domain collect, where available:

- measurable change signal;
- affected group;
- observed behavior change;
- repeated friction/problem;
- current workaround;
- evidence of money/time/headcount/procurement spent on the workaround;
- identifiable payer;
- candidate capabilities/resources;
- existing competitors/substitutes;
- regulatory/safety constraints;
- shortest plausible path to a paid test.

## Output schema

Each candidate opportunity must use:

```text
ID:
Title:
Geography:
Change signal:
Affected group:
Observed behavior:
Friction:
Demand hypothesis:
Payer:
Payment evidence:
Current workaround:
Capability route:
Transaction design:
Existing solutions:
Why unresolved:
Hard gates:
Opportunity score:
Confidence:
Cheapest decisive test:
Success threshold:
Stop rule:
Field-verification target:
```

## Ranking rule

Use `docs/OPPORTUNITY_SCORECARD.md`.

Select no more than the top 5 opportunities for deeper validation.

An opportunity cannot be ranked `A: TEST NOW` if:

- payer is unknown;
- payment evidence is absent;
- delivery cannot be bounded;
- legal/safety feasibility fails;
- first validation requires heavy fixed cost.

## Success criteria

EXP-002 is successful if it produces:

1. at least 10 evidence-backed Xuzhou-first opportunity hypotheses across multiple domains;
2. at least 3 candidates scoring >=65 with no failed hard gate;
3. at least 1 candidate with a plausible paid micro-test within 30 days;
4. clear rejection reasons for weak candidates;
5. a ranked recommendation based on evidence, not intuition;
6. a field-verification plan for the top candidates.

## Failure criteria

The method must be revised if:

- most candidates rely on complaints without payment evidence;
- scoring cannot distinguish attractive narratives from transaction-ready opportunities;
- the top-ranked candidates still require large capital or long sales cycles;
- results collapse into one preconceived industry instead of genuinely scanning the local economy;
- source evidence is too weak to support payer or behavior claims.

## Next experiment

The highest-ranked candidate should receive its own `EXPERIMENT_003_*` paid-validation test.

No broad marketplace/platform build is authorized by EXP-002 alone.
