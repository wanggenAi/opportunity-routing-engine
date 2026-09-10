# Hook & Orchestration Design

Status: `CANONICAL / OPPORTUNITY-TO-TRANSACTION BRIDGE`

Effective: 2026-09-10

## Purpose

Define how a discovered opportunity becomes a targeted, low-capital first transaction.

The orchestrator should not approach actors empty-handed with a vague request to cooperate. A first contact should carry a **hook**: a minimal, credible, economically relevant asset or conditional offer that makes the next step rational for the counterparty.

## Canonical transition

```text
DISCOVERED OPPORTUNITY
→ PAYER / ACTOR MAP
→ WHAT EACH PARTY ALREADY HAS
→ WHAT EACH PARTY LACKS
→ MINIMUM CONTROLLABLE ASSET
→ HOOK
→ CONDITIONAL COMMITMENT
→ CAPABILITY / RESOURCE ASSEMBLY
→ ACCEPTED TRANSACTION
```

## Hook definition

A `Hook` is:

> A bounded, credible piece of value or conditional transaction structure that reduces a counterparty's reason to ignore the orchestrator.

It is not:
- a broad platform pitch;
- an unverifiable promise;
- fake demand;
- pretending to own resources not controlled;
- deceptive arbitrage;
- requiring large inventory before proof.

## Hook classes

### H1 — Demand hook
Example:
- 5 qualified buyers interested under exact terms;
- 20 verified participants willing to pay a deposit;
- one institution willing to purchase if supply condition is met.

### H2 — Supply/capability hook
Example:
- two pre-qualified providers who can deliver an exact output at known cost/SLA;
- verified spare capacity from a venue, machine, technician or service team.

### H3 — Information hook
Example:
- a verified demand map;
- competitor/price/procurement intelligence that saves real search cost;
- a recurring signal others do not maintain efficiently.

### H4 — Outcome hook
Example:
- fixed accepted output for a small pilot;
- pay-after-acceptance;
- replacement guarantee for a bounded task;
- measurable cost/time reduction test.

### H5 — Distribution hook
Example:
- access to a concentrated channel/community/merchant network;
- existing audience or institutional route with permission.

### H6 — Idle-resource hook
Example:
- underused space/time/equipment/skills that can be activated with little marginal cost.

### H7 — Capital-structure hook
Example:
- deposit-funded execution;
- supplier paid after buyer acceptance;
- success fee/revenue share;
- staged payment;
- minimum guarantee conditioned on outcome.

Use only when transparent, legal and contractually accepted.

## Capital-light orchestration rule

Before spending operator capital ask:

```text
Can payer pre-commit?
Can a deposit cover part of delivery?
Can providers accept milestone/acceptance payout?
Can idle capacity reduce marginal cost?
Can a partner provide the asset for revenue share?
Can execution be staged so each commitment unlocks the next?
```

The goal is not `zero cost at any price`; the goal is **minimize irreversible capital before commercial proof**.

## Targeted contact rule

Do not broadcast when a concentrated actor route exists.

Prefer:

```text
identified payer cluster
+ known current friction
+ hook matched to that friction
+ explicit next step
```

over:

```text
post everywhere
+ hope someone responds
```

## Negotiation map

Before contact define:

```text
actor:
what_they_have:
what_they_want:
what_they_fear:
current_workaround:
what_we_control_now:
hook:
what_we_need_from_them:
conditional_exchange:
walk_away_condition:
```

## Resource position

The orchestrator does not need to own every resource before contact.

But distinguish:
- `OWNED` — directly controlled;
- `OPTIONED` — provider has explicitly agreed under conditions;
- `DISCOVERED` — available candidate, not committed;
- `HYPOTHETICAL` — not yet verified.

Never present `DISCOVERED/HYPOTHETICAL` as `OWNED/OPTIONED`.

## Hook strength levels

```text
H0 story only
H1 verified information / actor evidence
H2 conditional resource commitment
H3 signed/deposit-backed counterpart commitment
H4 completed pilot proof
H5 repeatable demand/supply loop
```

Prefer first outreach at H1 or H2 when feasible.

## Orchestrator role

The operator should preferentially own:
- structural insight;
- actor/resource map;
- hook design;
- conditional sequencing;
- acceptance rules;
- incentive split;
- risk boundary;
- route substitution.

The operator need not personally perform routine sales/delivery if those capabilities can be delegated.

## Governing invariant

> **Approach the market with a controlled piece of value and a conditional exchange, not with a request for strangers to believe a platform that does not yet exist.**
