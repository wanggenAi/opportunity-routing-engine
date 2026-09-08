# Opportunity Scorecard

## Purpose

Provide a common, evidence-backed way to compare opportunities across industries without confusing trend excitement with commercial viability.

The score is a prioritization aid, not proof.

## Hard gates

Before an opportunity can enter `TRANSACTION_TEST`, all hard gates must be explicitly answered.

### G1 — Payer clarity
- Who pays?
- Why do they pay?
- What evidence shows willingness or budget?

Result: `PASS / UNKNOWN / FAIL`

### G2 — Transactionability
- Can scope be defined?
- Can delivery be verified?
- Can price logic be explained?
- Can responsibilities be bounded?

Result: `PASS / UNKNOWN / FAIL`

### G3 — Legal / safety feasibility
- Can the proposed operator/provider lawfully perform or coordinate this work?
- Are required licenses, regulated activities, employment/financial/medical/legal/safety boundaries understood?

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
10: materially affects revenue, cost, risk, livelihood, or operations

### 2. Frequency / density — 0–10
0: rare one-off
5: repeated within a narrow group
10: frequent and observable across many potential transactions

### 3. Payment evidence — 0–15
0: no payment behavior
5: people spend time/use free workarounds
10: pay for imperfect substitutes or hire staff
15: explicit budget / repeated purchase / procurement evidence

### 4. Current-solution weakness — 0–10
0: excellent cheap incumbent
5: meaningful friction remains
10: expensive, fragmented, slow, low-trust, or poor-fit solution landscape

### 5. Supply / capability availability — 0–5
0: capability unavailable
2–3: exists but difficult to source/coordinate
5: abundant viable supply that is currently underutilized or poorly routed

### 6. Acquisition feasibility — 0–10
0: target payer inaccessible
5: reachable with moderate sales effort
10: active intent channels / marketplaces / procurement / communities make target payers directly observable

### 7. Delivery controllability — 0–10
0: highly bespoke/unbounded/dependent on customer environment
5: manageable with expertise
10: remote, standardized, measurable deliverable with low ambiguity

### 8. Time to first cash — 0–10
0: >6 months likely
3: 2–6 months
6: 30–60 days
10: realistic paid test within days/weeks

### 9. Unit economics potential — 0–5
0: little margin after coordination/delivery
3: plausible positive margin
5: strong value-to-cost spread or reusable output

### 10. Defensibility / learning compounding — 0–5
0: pure commodity introduction
3: repeated execution improves data/process/network
5: strong proprietary feedback loop or capability graph advantage

### 11. Operator fit — 0–5
0: requires unrelated credentials/capital
3: learnable with support
5: strongly leverages analysis, GPT, systems, research, communication, or existing access

### 12. Capital efficiency — 0–5
0: heavy fixed cost/inventory
3: modest paid tools/operations
5: near-zero fixed cost before validation

## Penalties

Subtract after weighted score:

- `-20` high regulatory/licensing ambiguity
- `-15` heavy on-site/custom integration dependence
- `-15` requires large capital before payer proof
- `-10` long payment cycle / collection risk
- `-10` severe platform dependency with no customer ownership
- `-10` obvious bypass risk where value is only an introduction
- `-10` market dominated by a low-cost incumbent with little unresolved friction

Scores after penalties are floored at 0.

## Priority bands

### 80–100 — `A: TEST NOW`
Only if all hard gates pass. Design a paid micro-test immediately.

### 65–79 — `B: INVESTIGATE`
Promising but one or more evidence gaps remain. Gather targeted evidence before selling/building.

### 50–64 — `C: WATCH`
Possible but weak relative to alternatives. Keep as a monitored hypothesis.

### <50 — `D: REJECT / DORMANT`
Do not spend meaningful time unless conditions change.

## Evidence confidence

Every score component must include:

- evidence summary;
- source/provenance;
- observed date;
- verification status;
- confidence (`HIGH / MEDIUM / LOW`).

Do not use false precision. A score based mostly on low-confidence assumptions should be visibly marked `LOW_CONFIDENCE` regardless of numeric total.

## Final decision record

Each scored opportunity should end with:

```text
Opportunity:
Target group:
Payer:
Desired outcome:
Current workaround:
Candidate capability route:
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
