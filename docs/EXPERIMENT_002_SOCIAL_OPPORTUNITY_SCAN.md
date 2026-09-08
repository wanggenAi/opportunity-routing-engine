# EXPERIMENT 002 — Social Opportunity Scan

Status: `PLANNED / ACTIVE NEXT`

Date opened: 2026-09-08

## Objective

Test whether the Opportunity Routing Engine can convert current social/market change into a ranked set of **transaction-worthy** opportunities rather than merely interesting ideas.

This is the first experiment under the broadened project mission.

## Core question

> Can a structured scan of current China social and economic signals identify opportunities with clear payers, observable payment behavior, accessible supply, bounded delivery, and a realistic path to first cash within 30–60 days?

## Scope

Scan at least 10 distinct change domains, including but not limited to:

1. value-conscious / conservative consumption;
2. employment structure and project-based work;
3. AI substitution of repetitive knowledge work;
4. aging / household service coordination;
5. idle assets / inventory / second-hand migration;
6. small-business cost reduction;
7. education / student capability utilization;
8. local-vs-remote execution gaps;
9. China-language information asymmetry;
10. domestic or cross-border demand-capability mismatch.

The scan must not force an opportunity in every domain.

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

1. at least 10 evidence-backed opportunity hypotheses across multiple domains;
2. at least 3 candidates scoring >=65 with no failed hard gate;
3. at least 1 candidate with a plausible paid micro-test within 30 days;
4. clear rejection reasons for weak candidates;
5. a ranked recommendation based on evidence, not intuition.

## Failure criteria

The method must be revised if:

- most candidates rely on complaints without payment evidence;
- scoring cannot distinguish attractive narratives from transaction-ready opportunities;
- the top-ranked candidates still require large capital or long sales cycles;
- results collapse into one preconceived industry instead of genuinely scanning society;
- source evidence is too weak to support payer or behavior claims.

## Next experiment

The highest-ranked candidate should receive its own `EXPERIMENT_003_*` paid-validation test.

No platform build is authorized by EXP-002 alone.
