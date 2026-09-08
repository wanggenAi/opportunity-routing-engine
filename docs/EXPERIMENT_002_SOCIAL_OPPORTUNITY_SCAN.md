# EXPERIMENT 002 — Xuzhou Actor-First Social Opportunity Scan

Status: `ACTIVE`

Date opened: 2026-09-08

## Objective

Test whether the Opportunity Routing Engine can convert current Xuzhou social/market change into a ranked set of **transaction-worthy opportunities across individuals, households, groups, businesses and institutions**, rather than collapsing into enterprise-only ideas.

Xuzhou is the first field laboratory because online hypotheses can be validated rapidly through local observation and conversations.

## Core question

> Can a structured actor-first scan of current Xuzhou social/economic change identify opportunities with real need actors, identifiable payers, observable payment/workaround behavior, accessible capabilities/resources, bounded transactions and a realistic path to first cash?

## Mandatory actor coverage

The scan must deliberately cover at least these actor groups:

1. university students / graduates;
2. young workers / flexible workers / job seekers;
3. single or renting young adults;
4. parents / households / children;
5. elderly people / caregivers / adult children;
6. pet owners;
7. value-conscious consumers;
8. skilled workers / farmers / local service workers;
9. merchants / self-employed operators;
10. SMEs / manufacturers;
11. institutions / communities / schools;
12. holders of idle personal or organizational resources: skill, time, vehicles, equipment, inventory, space, data, etc.

The scan may add other groups when evidence warrants.

## Anti-bias requirement

Do not assume enterprises are the payer.

For every candidate explicitly map:

```text
Need actor:
Beneficiary:
Payer:
Capability provider:
Resource owner (if relevant):
Sponsor (if relevant):
Orchestrator value:
Transaction type:
```

The scan should test multiple structures:

- B2B
- B2C
- C2C
- C2B
- Sponsored / third-party payer
- Multi-sided

If more than half of promoted opportunities end up enterprise-paid, the result must explain with comparative evidence why enterprise opportunities genuinely scored higher rather than being easier for the researcher to imagine.

## Required evidence per candidate

Collect where available:

- measurable change signal;
- exact actor/group;
- observed behavior change;
- repeated friction/problem;
- desired outcome;
- beneficiary;
- payer candidates;
- current workaround;
- evidence of money/time/risk/headcount spent;
- existing purchase/service/transaction evidence;
- candidate capabilities/resources;
- existing competitors/substitutes;
- trust/safety constraints;
- regulatory constraints;
- shortest plausible path to a paid test.

## Example opportunity families to investigate — not conclusions

### Individuals / households
- value-for-money / repair / second-hand / rental migration;
- trusted small local services;
- young-adult convenience and social/lifestyle frictions;
- pet-care micro-needs;
- elderly digital/coordination friction with adult children as possible payer;
- household fragmented tasks that are too small for traditional service providers.

### Capability holders
- university students with underused digital/creative/research capability;
- skilled workers with fragmented availability;
- individuals with idle vehicles/equipment/space/time;
- graduates who need paid project evidence rather than generic training.

### Merchants / organizations
- merchant off-peak idle capacity routed to value-conscious consumers;
- bounded digital/data/AI micro-projects;
- local-vs-remote execution gaps;
- institutional services where beneficiary and payer differ.

### Cross-regional / cross-border
- China-language information asymmetry;
- regional resource mismatch;
- overseas demand ↔ local capability.

## Candidate output schema

```text
ID:
Title:
Need actor:
Beneficiary:
Payer:
Capability provider:
Transaction type:
Change signal:
Observed behavior:
Friction:
Need hypothesis:
Payment/workaround evidence:
Current workaround:
Capability route:
Transaction design:
Existing solutions:
Why unresolved:
Trust / legal gates:
Opportunity score:
Confidence:
Cheapest decisive test:
Success threshold:
Stop rule:
```

## Ranking rule

Use `docs/OPPORTUNITY_SCORECARD.md` and `docs/ACTOR_MODEL.md`.

Select no more than the top 5 opportunities for deeper validation.

An opportunity cannot be ranked `A: TEST NOW` if:

- need actor is vague;
- payer is unknown;
- payment evidence is absent;
- delivery/trust cannot be bounded;
- legal/safety feasibility fails;
- first validation requires heavy fixed cost.

## Success criteria

EXP-002 is successful if it produces:

1. at least 12 evidence-backed opportunity hypotheses across multiple actor groups;
2. meaningful representation of personal/household and organizational demand;
3. at least 3 candidates scoring >=65 with no failed hard gate;
4. at least 1 candidate with a plausible paid micro-test within 30 days;
5. at least 1 serious non-enterprise-payer candidate unless evidence explicitly rejects all such candidates;
6. clear rejection reasons for weak candidates;
7. a ranked recommendation based on evidence, not intuition.

## Failure criteria

The method must be revised if:

- the scan repeatedly defaults to companies/SMEs without comparative evidence;
- most personal candidates rely on complaints without payment/workaround evidence;
- need actor and payer are routinely conflated;
- scoring cannot distinguish attractive narratives from transaction-ready opportunities;
- top candidates require large capital or long sales cycles;
- source evidence is too weak to support payer or behavior claims.

## Current decision on existing EXP-003

The Xuzhou managed SME micro-project paid validation remains a valid **vertical candidate**, but it is no longer presumed to be the overall top opportunity until this broader actor-first scan is completed.

## Next experiment

After the actor-first ranking is refreshed, the highest-confidence candidate—or multiple cheap parallel candidates—should receive paid validation.

No broad platform build is authorized by EXP-002 alone.
