# Case Mining Engine

Status: `CANONICAL / DISCOVERY INFRASTRUCTURE`

Effective: 2026-09-10

## Purpose

Continuously mine successful and failed market cases to learn **how opportunities were actually discovered, what hook opened the transaction, what resources were assembled, why the payer paid, and whether the model became repeatable**.

The engine is not a startup-story collector. It extracts reusable mechanisms.

## Canonical case chain

```text
CONTEXT CHANGE
→ ACTOR BEHAVIOR CHANGE
→ OBSERVED FRICTION
→ OPPORTUNITY INSIGHT
→ FIRST HOOK
→ FIRST PAYER COMMITMENT
→ RESOURCE STACK
→ DELIVERY / ACCEPTANCE
→ ECONOMICS
→ REPEAT / REFERRAL / EXPANSION
→ FAILURE / MOAT / BYPASS
→ REUSABLE MECHANISM
```

## What to mine

Sources may include:
- official local/industry case studies;
- procurement winners and contract histories;
- company interviews and founder stories;
- listed-company filings;
- platform merchant/service-provider success stories;
- news reports with concrete transaction/economic facts;
- industry association cases;
- business-model teardown articles;
- public reviews and user behavior;
- failed/closed businesses where failure evidence exists.

Prefer cases with observable payments, customer acquisition, repeat behavior or operating metrics.

## Case record

```text
case_id:
company_or_actor:
geography:
time_period:
market_context:
macro_signal:
money_flow_signal:
target_actor:
problem_or_friction:
what_founder_or_operator_noticed:
first_hook:
why_counterparty_engaged:
payer:
first_transaction:
resource_stack:
what_was_owned:
what_was_borrowed_or_partnered:
what_was_paid_only_after_revenue:
acceptance_mechanism:
revenue_model:
repeat_loop:
demand_pump:
supply_replenishment:
orchestration_value:
bypass_risk:
capital_required_before_proof:
regulatory_or_trust_boundary:
observed_success_evidence:
observed_failure_evidence:
replicable_mechanism:
non_replicable_advantage:
sources:
confidence:
```

## The hook is first-class

For every successful case ask:

> **What did they possess, promise, demonstrate, aggregate, guarantee, pre-sell or coordinate that caused the first counterparty to take the next step?**

Common hook classes:
- pre-aggregated demand;
- pre-qualified supply;
- exclusive/underused resource access;
- guaranteed outcome or acceptance condition;
- measurable cost saving;
- revenue-share / pay-after-result;
- trial / deposit / minimum guarantee;
- verified information unavailable cheaply elsewhere;
- reduced trust/risk;
- faster access / response;
- bundled fragmented capabilities;
- regulatory/policy timing advantage;
- arbitrage of idle capacity;
- local distribution/channel access.

A hook must create enough immediate value that the counterparty can say yes without first believing a grand platform story.

## Light-capital mechanism extraction

Because the initial operator has limited capital, explicitly identify whether early execution used:
- customer prepayment/deposit;
- supplier credit;
- success-fee compensation;
- revenue share;
- commission-only acquisition;
- existing idle capacity;
- borrowed/partner resources;
- free/low-cost public infrastructure;
- no-inventory coordination;
- pay-provider-after-acceptance;
- staged commitments.

The system should prefer legal, transparent **capital-light orchestration**, not deceptive promises or hidden liabilities.

## Survivorship-bias control

For each attractive mechanism, seek at least one:
- failed comparator;
- incumbent alternative;
- case where direct matching bypassed the intermediary;
- case where margins collapsed from acquisition/coordination cost;
- case where regulation/trust blocked scale.

`success story != base rate`.

## Transferability scoring

Score mechanisms, not celebrity founders.

Ask:
1. Did success depend on unique personal fame/network?
2. Did it require large upfront capital?
3. Was the first hook reproducible?
4. Was payer behavior externally observable?
5. Did demand recur?
6. Could execution be delegated?
7. Could providers be replaced?
8. Did orchestration remain valuable after first introduction?
9. Can the mechanism work in Xuzhou or another accessible market?
10. Can it be tested cheaply and quickly?

## Output

The Case Mining Engine should produce:
- `mechanism library` — reusable hooks/loops;
- `anti-pattern library` — why similar attempts fail;
- `local analog list` — Xuzhou/Jiangsu actors resembling successful structures;
- `opportunity seeds` — hypotheses generated from mechanism + current money-flow evidence.

## Governing invariant

> **Do not copy what a successful business sells. Reconstruct what changed, what they noticed, what first hook converted a counterparty, how resources were assembled, and why the transaction kept recurring.**
