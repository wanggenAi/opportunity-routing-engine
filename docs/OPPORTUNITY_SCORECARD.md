# Opportunity Scorecard

## Purpose

Compare opportunities across actor structures using commercial truth **and strategic fit for a resource orchestration engine**.

A profitable founder-operated service can be commercially real yet strategically weak if it cannot be decomposed, delegated, replaced or governed economically.

Read with:
- `docs/RESOURCE_ORCHESTRATION_KERNEL.md`
- `docs/ACTOR_MODEL.md`

## Hard gates

### G0 — Actor / role clarity
Answer:
- who experiences the need?
- who benefits?
- who pays?
- who sponsors, owns resources or provides capabilities?
- what role does the orchestrator play?

Result: `PASS / UNKNOWN / FAIL`

### G1 — Payer clarity
Answer:
- who pays?
- why do they have incentive and ability to pay?
- what real budget/payment/workaround evidence exists?

Result: `PASS / UNKNOWN / FAIL`

### G2 — Transactionability
Answer:
- can the desired outcome and scope be bounded?
- can output be verified?
- can price/payout logic be explained?
- can responsibility/failure/refund conditions be bounded?

Result: `PASS / UNKNOWN / FAIL`

### G3 — Legal / trust / safety feasibility
Answer:
- can the transaction be lawfully and safely coordinated?
- are licensing, identity, insurance, safeguarding, home access, vulnerable-person or other trust requirements understood?

Result: `PASS / CONDITIONAL / FAIL`

### G4 — Capability decomposability / delegatability
Answer:
- can recurring execution be represented as one or more `CapabilityUnit`s?
- can each unit define input, output, acceptance and payout?
- are there plausible providers other than the operator?
- can a failed provider be replaced without redesigning the whole transaction?

Result: `PASS / UNKNOWN / FAIL`

### G5 — Orchestration value
Answer:
- does the orchestration layer create material recurring value beyond introduction?
- does it reduce ambiguity, search, coordination, trust, QA, failure, settlement or replacement cost?
- after buyer and provider know each other, is there still a reason for the orchestration layer to exist?

Result: `PASS / UNKNOWN / FAIL`

### Gate policy

A `FAIL` on G0–G3 blocks the proposed transaction test in that form.

G4/G5 may be `UNKNOWN` when the experiment explicitly exists to resolve them, but **both must PASS before promotion to `REPEATABLE` or `SCALE_CANDIDATE`**.

Founder willingness to personally perform a difficult task does not convert G4 from `FAIL/UNKNOWN` to `PASS`.

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

## 1. Pain severity — 0–10
0: inconvenience only.
10: materially affects money, time, safety, livelihood, family burden, revenue, cost or risk.

## 2. Frequency / transaction density — 0–10
0: rare one-off.
10: frequent/repeated transactions or dense observable actor group.

## 3. Payment evidence — 0–15
0: no payment/workaround behavior.
5: meaningful time/family/manual workaround.
10: actors pay substitutes or hire capability.
15: repeated purchase/order, explicit budget, procurement, deposits or strong third-party payer evidence.

Record whose payment behavior is being observed.

## 4. Current-solution weakness — 0–10
0: excellent cheap incumbent.
10: costly, fragmented, slow, badly timed, low-trust, inaccessible or poorly coordinated current solution.

## 5. Supply / capability availability — 0–5
0: required capability unavailable.
5: several viable resources/providers exist and capability can plausibly be routed.

Abundant people with claimed skills do not equal proven capability supply.

## 6. Acquisition route feasibility — 0–8
0: need actors/payers cannot be economically reached.
4: one credible route with moderate effort.
8: several identifiable channels or delegated demand-source capabilities can reach qualified payers.

Do not award points merely because the operator personally knows how to cold-call.

## 7. Delivery controllability — 0–8
0: unbounded/highly bespoke/unverifiable.
4: manageable with process.
8: standardized or tightly bounded output with objective acceptance and manageable trust/safety.

## 8. Delegatability / orchestration leverage — 0–10
0: value depends on operator personally executing core work.
3: some tasks can be delegated but key recurring bottleneck remains operator-bound.
5: delivery can be delegated but acquisition/governance remains founder-heavy.
8: acquisition and delivery can both be routed as capability units with measurable outputs.
10: multiple replaceable providers/routes exist, interfaces are stable, and the orchestrator mainly designs/governs rather than executes.

This dimension is central to strategic fit.

## 9. Time to first cash — 0–8
0: >6 months likely.
2: 2–6 months.
5: 30–60 days.
8: paid test realistic within days/weeks.

## 10. Unit economics potential — 0–5
Evaluate **normalized orchestration margin**, not only cash margin.

0: little/no margin after acquisition, provider payouts, QA/trust, failures and operator shadow labor.
3: plausible positive normalized margin.
5: strong value-cost spread and repeat potential.

## 11. Defensibility / learning compounding — 0–5
0: pure commodity introduction.
3: execution improves task templates, trust, provider reliability or buyer knowledge.
5: strong compounding from Actor + Demand + Capability + Orchestration + Trust + Transaction + Outcome data.

## 12. Capital efficiency — 0–6
0: heavy fixed cost/inventory before proof.
3: moderate working capital/tools.
6: near-zero fixed cost and providers/resources can be paid from or close to transaction cash flow.

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

Scores are floored at 0.

## Founder shadow-cost rule

Whenever the operator personally performs sales, recruitment, research, delivery, QA, hosting, transport, support or another routable function, estimate:

```text
operator_hours × realistic replacement hourly cost
```

Record it as `operator_shadow_cost`.

A test may still be worth running for learning, but do not report positive repeatable economics using unpaid founder labor.

## Orchestration-fit rule

Strategically preferred opportunities have:
- real payer evidence;
- bounded outputs;
- several routable capability providers;
- objective acceptance;
- short transaction cycles;
- low/controlled safety risk;
- delegated acquisition potential;
- delegated delivery potential;
- enough gross surplus to pay all capabilities;
- recurring value for governance/QA/replacement/data.

A high-value consulting engagement that depends on the operator personally selling and delivering every project may be a viable job, but is not automatically a high-fit engine opportunity.

## Priority bands

### 80–100 — `A: TEST NOW`
Requires G0–G3 PASS and no unacknowledged G4/G5 failure. Run the smallest transaction/delegation test.

### 65–79 — `B: INVESTIGATE`
Promising but targeted unknowns remain.

### 50–64 — `C: WATCH / REDESIGN`
Potential value, weak structure or poor orchestration fit.

### <50 — `D: REJECT / DORMANT`
Do not spend meaningful time unless mechanism changes.

## Evidence maturity

Use:

```text
L0 statement
L1 observed recent behavior / workaround
L2 exact terms accepted verbally
L3 deposit / authorized commitment / signed task
L4 completed accepted transaction + settlement
L5 repeat / referral
L6 delegated repeat / provider replacement / alternate route succeeds
```

L4 proves one transaction. L6 begins to prove the orchestration engine.

## Final decision record

```text
Opportunity:
Need actor:
Beneficiary:
Payer:
Sponsor / resource owner:
Desired outcome:
Current workaround:
Payment evidence:
Transaction objective:
Required capability units:
Demand-source capability:
Candidate providers/resources:
Acceptance criteria:
Trust / safety requirements:
Incentive / payout design:
Replacement design:
Orchestrator recurring value:
Hard gates G0-G5:
Weighted score:
Penalties:
Final score:
Evidence maturity:
Cash contribution margin:
Operator shadow cost:
Normalized orchestration margin:
Key unknown:
Cheapest decisive experiment:
Success threshold:
Stop rule:
```

## Governing principle

**Score the system that completes the transaction, not the founder's willingness to personally do the work.**
