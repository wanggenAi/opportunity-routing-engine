# Opportunity Scorecard

Status: `CANONICAL`

## Purpose

Compare opportunities using commercial truth **and strategic fit for a sustainable resource-orchestration engine**.

A founder-operated service can be commercially real yet strategically weak if it cannot be decomposed, delegated, replaced, repeatedly sourced, or governed economically.

Read with:
- `docs/DISCOVERY_ENGINE.md`
- `docs/RESOURCE_ORCHESTRATION_KERNEL.md`
- `docs/ACTOR_MODEL.md`
- `docs/OPPORTUNITY_MOBILIZATION_GATE.md`

## Hard / strategic gates

### G0 — Actor / role clarity
Who experiences the need, benefits, pays, owns resources, supplies capabilities, and orchestrates?

Result: `PASS / UNKNOWN / FAIL`

### G1 — Payer clarity
Who pays, why do they have incentive/ability, and what real budget/payment/workaround evidence exists?

Result: `PASS / UNKNOWN / FAIL`

### G2 — Transactionability
Can the desired outcome, scope, acceptance, price/payout logic, responsibility and failure conditions be bounded?

Result: `PASS / UNKNOWN / FAIL`

### G3 — Legal / trust / safety feasibility
Can the transaction be lawfully and safely coordinated? Are licensing, confidentiality, data access, identity, insurance, vulnerable-person and other trust boundaries understood?

Result: `PASS / CONDITIONAL / FAIL`

### G4 — Capability decomposability / delegatability
Can recurring execution be represented as `CapabilityUnit`s with input, output, acceptance and payout? Are plausible providers available besides the operator? Can failure be rerouted?

Result: `PASS / UNKNOWN / FAIL`

### G5 — Orchestration value
Does the orchestration layer create recurring value beyond contact introduction by reducing ambiguity, search, coordination, trust, QA, failure, settlement or replacement cost?

Result: `PASS / UNKNOWN / FAIL`

### G6 — Regenerative circulation / recurring demand
Can the opportunity sustain a continuing transaction loop rather than depend on isolated founder-led deals?

Answer:
- Is there a recurring `Demand Pump` — a channel, aggregator, installed base, lifecycle event, recurring workflow or actor behavior that continually generates tasks?
- Can one acquired demand relationship generate multiple transaction events?
- Can capability supply replenish or be replaced continuously?
- Do task templates repeat enough for learning to reduce future coordination cost?
- Does transaction history improve trust/routing and make the next transaction easier?
- Can the system continue without a fresh founder-led sales campaign for every single task?

Result: `PASS / UNKNOWN / FAIL`

A one-off transaction may still be tested for learning, but **G6 must PASS before an opportunity becomes a core `REPEATABLE` / `SCALE_CANDIDATE` system**.

### G7 — Mobilization potential / bilateral pull / self-propulsion
Once reality validity and a narrow missing edge are established, does the route contain enough actor energy to move with little founder push?

Answer:
- Is the demand side already taking observable action to solve the problem rather than merely expressing interest?
- Is the supply/resource side already seeking utilization, income, orders, application or an outlet?
- Are callable resources abundant enough to route and replace?
- Can the first useful flow activate with low permission and low capital?
- Is there credible economic room for the orchestration layer after payouts, QA, failure and acquisition cost?
- Does the behavior repeat?
- Once the route is visible, can actors continue entering without founder persuasion on every transaction?
- Can the operator eventually exit recurring sales and delivery while routing, acceptance and settlement continue?

Result: `HIGH / MEDIUM / LOW / UNASSESSED`

A high G7 requires evidence-backed bilateral pull, clear value capture, repeatability, self-propulsion and operator exit. It does not prove market validation.

### Gate policy

- A `FAIL` on G0–G3 blocks the proposed transaction test in that form.
- G4–G6 may be `UNKNOWN` when the test explicitly exists to resolve them.
- G4, G5 and G6 must all `PASS` before promotion to repeatable/core platform status.
- Current-stage founder attention should prefer Reachability A/B candidates with G7 `HIGH`; a truthful but low-mobilization candidate may stay in the ledger without consuming founder attention.
- Founder willingness to personally perform acquisition or delivery never converts G4, G6 or G7 into PASS/HIGH.
- G7 is evaluated by `docs/OPPORTUNITY_MOBILIZATION_GATE.md` and is separate from the 100-point weighted score below.

## Weighted score — exactly 100 points

- Pain severity: 10
- Frequency / transaction density: 10
- Payment evidence: 15
- Current-solution weakness: 10
- Supply / capability availability: 5
- Acquisition route feasibility: 8
- Delivery controllability: 8
- Delegatability / orchestration leverage: 10
- Time to first cash: 8
- Unit economics potential: 5
- Defensibility / learning compounding: 5
- Capital efficiency: 6

**Total = 100.**

### 1. Pain severity — 0–10
10 means the friction materially affects money, time, safety, livelihood, revenue, cost, risk or operational performance.

### 2. Frequency / transaction density — 0–10
10 means repeated transactions occur or a dense observable actor/channel continually creates tasks. This supports G6 but does not replace it.

### 3. Payment evidence — 0–15
0 = no payment/workaround behavior. 10 = actors already pay substitutes/hire capability. 15 = repeated orders, budgets, procurement, deposits or strong third-party payment evidence.

### 4. Current-solution weakness — 0–10
10 means current solutions remain costly, fragmented, slow, badly timed, low-trust, inaccessible or poorly coordinated.

### 5. Supply / capability availability — 0–5
5 means several viable providers/resources exist and can plausibly be routed. Claimed skill alone is not proven supply.

### 6. Acquisition route feasibility — 0–8
8 means several identifiable channels or delegated demand-source capabilities can reach qualified payers. Do not award points merely because the operator can cold-call.

### 7. Delivery controllability — 0–8
8 means tightly bounded output, objective acceptance and manageable trust/safety.

### 8. Delegatability / orchestration leverage — 0–10
0 = value depends on operator execution. 5 = delivery can delegate but acquisition/governance remains founder-heavy. 8 = acquisition and delivery can both route. 10 = multiple replaceable providers/routes and stable interfaces exist.

### 9. Time to first cash — 0–8
8 means a paid test is realistic within days/weeks; 5 means roughly 30–60 days; 0 means more than six months is likely.

### 10. Unit economics potential — 0–5
Evaluate normalized orchestration margin after acquisition payouts, provider payouts, QA/trust, failures and operator shadow labor.

### 11. Defensibility / learning compounding — 0–5
5 means repeated transactions improve Actor + Demand + Capability + Orchestration + Trust + Transaction + Outcome data and reduce future routing cost/risk.

### 12. Capital efficiency — 0–6
6 means near-zero fixed cost before proof and most resource payouts can occur from or close to transaction cash flow.

## Penalties

Subtract after weighted score:
- `-25` persistent operator-personal-execution dependency on core recurring work
- `-20` high regulatory/licensing ambiguity
- `-20` unresolved vulnerable-person / home-access / physical-safety trust risk
- `-15` heavy on-site/custom integration dependence
- `-15` requires large capital before payer proof
- `-10` long payment cycle / collection risk
- `-10` severe platform dependency with no customer/actor ownership
- `-10` obvious bypass risk where value is mainly introduction
- `-10` low-cost incumbent with little unresolved friction
- `-10` acquisition/support cost likely overwhelms low ticket
- `-10` single irreplaceable capability provider for a core recurring unit
- `-15` structurally one-off demand with no credible recurring demand source

Scores are floored at zero.

## Founder shadow-cost rule

Whenever the operator personally performs sales, recruitment, research, delivery, QA, hosting, transport, support or another routable function, record:

```text
operator_hours × realistic replacement hourly cost
```

Founder free labor is not profit.

## Sustainability / blood-circulation rule

A preferred platform wedge should resemble:

```text
RECURRING DEMAND PUMP
→ TASK QUEUE
→ CAPABILITY DECOMPOSITION
→ REPLACEABLE SUPPLY
→ ACCEPTANCE
→ SETTLEMENT
→ REPUTATION / OUTCOME DATA
→ BETTER ROUTING + LOWER FAILURE COST
→ MORE DEMAND / BETTER SUPPLY
↺
```

Do not confuse recurring customer acquisition with recurring demand. The ideal demand source already has a continuing stream of problems/orders/workflows before the orchestrator arrives.

## Priority bands

### 80–100 — `A: TEST NOW`
Requires G0–G3 ready and no unacknowledged G4–G6 failure. Run the smallest real transaction/delegation/circulation test.

### 65–79 — `B: INVESTIGATE`
Promising but targeted unknowns remain.

### 50–64 — `C: WATCH / REDESIGN`
Potential value but weak evidence, economics, delegation or circulation.

### <50 — `D: REJECT / DORMANT`
Do not spend meaningful time unless the mechanism changes.

## Evidence maturity

```text
L0 statement
L1 observed recent behavior / workaround
L2 exact terms accepted verbally
L3 deposit / authorized commitment / signed task
L4 completed accepted transaction + settlement
L5 repeat / referral
L6 delegated repeat / provider replacement / alternate route succeeds
L7 regenerative loop: recurring demand source sends multiple transactions and routing cost/risk improves
```

L4 proves one transaction. L6 begins to prove orchestration. **L7 begins to prove the sustainable system.**

## Final decision record

```text
Opportunity:
Need actor / beneficiary / payer:
Demand Pump:
Desired outcome:
Current workaround / payment evidence:
Transaction objective:
Required CapabilityUnits:
Demand-source capability:
Candidate providers/resources:
Acceptance criteria:
Trust / safety / data boundaries:
Incentive / payout design:
Replacement design:
Orchestrator recurring value:
Regenerative loop:
Hard gates G0-G6:
Weighted score / penalties / final score:
Evidence maturity L0-L7:
Cash contribution margin:
Operator shadow cost:
Normalized orchestration margin:
Key UNKNOWN:
Cheapest decisive test:
Success threshold / stop rule:
```

## Governing principle

**Score the circulating system that completes repeated transactions, not the founder's willingness to personally hustle for the next job.**
