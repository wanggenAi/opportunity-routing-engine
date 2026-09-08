# Opportunity Scorecard

## Purpose

Provide a common, evidence-backed way to compare opportunities across industries **and actor structures** without confusing trend excitement with commercial viability.

The score is a prioritization aid, not proof.

Read with `docs/ACTOR_MODEL.md`.

## Hard gates

Before an opportunity can enter `TRANSACTION_TEST`, all hard gates must be explicitly answered.

### G0 — Actor / role clarity
- Who experiences the need?
- Who receives the benefit?
- Who pays?
- Who/what provides capability?
- Are any sponsor/resource-owner roles material?

Result: `PASS / UNKNOWN / FAIL`

### G1 — Payer clarity
- Who pays?
- Why does this actor have incentive and ability to pay?
- Is the payer the beneficiary, family, employer, supplier, institution, sponsor, platform, or another counterparty?
- What evidence shows willingness or budget?

Result: `PASS / UNKNOWN / FAIL`

### G2 — Transactionability
- Can the desired outcome/scope be defined?
- Can delivery be verified?
- Can trust requirements be satisfied?
- Can price logic be explained?
- Can responsibilities be bounded?

Result: `PASS / UNKNOWN / FAIL`

### G3 — Legal / trust / safety feasibility
- Can the proposed operator/provider lawfully perform or coordinate this work?
- Does it involve children, elderly/vulnerable people, home access, transport, money, medical/legal issues, employment placement or other high-trust contexts?
- Are licensing, identity verification, insurance, safeguarding or regulated boundaries understood?

Result: `PASS / CONDITIONAL / FAIL`

A `FAIL` on any hard gate blocks testing in the proposed form. `UNKNOWN` must be resolved before meaningful spend.

## Weighted score — exactly 100 points

Weight checksum:

- Pain severity: 10
- Frequency / density: 10
- Payment evidence: 15
- Current-solution weakness: 10
- Supply / capability availability: 5
- Acquisition feasibility: 10
- Delivery controllability: 10
- Time to first cash: 10
- Unit economics potential: 5
- Defensibility / learning compounding: 5
- Operator fit: 5
- Capital efficiency: 5

**Total = 100.**

### 1. Pain severity — 0–10
0: inconvenience only
5: recurring cost/delay/frustration
10: materially affects money, time, safety, livelihood, family burden, convenience, revenue, cost or risk

### 2. Frequency / density — 0–10
0: rare one-off
5: repeated within a narrow group
10: frequent and observable across many potential transactions or a dense local actor group

### 3. Payment evidence — 0–15
0: no payment/workaround behavior
5: substantial time/family effort/free workaround
10: actors pay for imperfect substitutes, convenience, repair/rental/service, or firms hire staff
15: repeated purchase/booking/subscription/order, explicit budget, procurement, or strong third-party payment evidence

Payment evidence can come from the beneficiary or a third-party payer; record which.

### 4. Current-solution weakness — 0–10
0: excellent cheap incumbent
5: meaningful friction remains
10: expensive, fragmented, slow, inconvenient, low-trust, inaccessible, badly timed, or poor-fit solution landscape

### 5. Supply / capability availability — 0–5
0: capability unavailable
2–3: exists but difficult to source/coordinate/trust
5: abundant viable capability/resource that is underused or poorly routed

### 6. Acquisition feasibility — 0–10
0: both need actors and payer are hard to identify/reach
5: one side reachable with moderate effort
10: dense local/online channels make the relevant need actors and payers directly observable/reachable

### 7. Delivery controllability — 0–10
0: highly bespoke/unbounded/high-trust or dependent on uncontrollable environment
5: manageable with explicit process and safeguards
10: standardized, measurable, low-ambiguity outcome with bounded trust/safety requirements

### 8. Time to first cash — 0–10
0: >6 months likely
3: 2–6 months
6: 30–60 days
10: realistic paid test within days/weeks

### 9. Unit economics potential — 0–5
0: little margin after acquisition, coordination, trust and delivery costs
3: plausible positive margin
5: strong value-to-cost spread, repeatability, or reusable output/network effect

### 10. Defensibility / learning compounding — 0–5
0: pure commodity introduction
3: repeated execution improves actor/capability data, process, trust or network
5: strong proprietary Actor Graph + Capability Graph + Transaction Graph feedback loop

### 11. Operator fit — 0–5
0: requires unrelated credentials/capital
3: learnable with support
5: strongly leverages analysis, GPT, systems, research, communication, local mobility/access, or existing resources

### 12. Capital efficiency — 0–5
0: heavy fixed cost/inventory
3: modest paid tools/operations
5: near-zero fixed cost before validation

## Penalties

Subtract after weighted score:

- `-20` high regulatory/licensing ambiguity
- `-20` unresolved vulnerable-person / home-access / physical-safety trust risk
- `-15` heavy on-site/custom integration dependence
- `-15` requires large capital before payer proof
- `-10` long payment cycle / collection risk
- `-10` severe platform dependency with no customer/actor ownership
- `-10` obvious bypass risk where value is only an introduction
- `-10` market dominated by a low-cost incumbent with little unresolved friction
- `-10` acquisition/support cost likely overwhelms low C2C/B2C ticket size

Scores after penalties are floored at 0.

## Cross-structure comparison rule

Do not mechanically reward B2B because enterprise budgets are larger.

A consumer/household/C2C opportunity may outrank B2B when it has:

- higher transaction frequency/density;
- easier acquisition;
- faster payment;
- abundant underused capability;
- repeat behavior;
- strong third-party payer;
- lower sales cycle;
- better local validation access.

Likewise, a personal opportunity must be downgraded when trust, support, refunds, acquisition or safety costs make the economics weak.

## Priority bands

### 80–100 — `A: TEST NOW`
Only if all hard gates pass. Design a paid micro-test immediately.

### 65–79 — `B: INVESTIGATE`
Promising but one or more evidence gaps remain. Gather targeted evidence before selling/building.

### 50–64 — `C: WATCH`
Possible but weak relative to alternatives.

### <50 — `D: REJECT / DORMANT`
Do not spend meaningful time unless conditions change.

## Evidence confidence

Every score component must include:

- evidence summary;
- source/provenance;
- observed date;
- actor/role supported;
- verification status;
- confidence (`HIGH / MEDIUM / LOW`).

Do not use false precision. Mostly low-confidence assumptions = `LOW_CONFIDENCE` regardless of numeric score.

## Final decision record

```text
Opportunity:
Need actor:
Beneficiary:
Payer:
Capability provider:
Resource owner / sponsor (if any):
Transaction type:
Desired outcome:
Current workaround:
Payment evidence:
Candidate capability route:
Trust / safety requirements:
Transaction design:
Hard gates:
Score:
Confidence:
Key unknown:
Cheapest decisive experiment:
Success threshold:
Stop rule:
Next review date:
```

## Governing principle

**The score decides what to test, not what to believe. Real transactions update belief.**
