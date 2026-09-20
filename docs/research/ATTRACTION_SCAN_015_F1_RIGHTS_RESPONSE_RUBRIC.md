# ATTRACTION_SCAN_015-F1 — Written Rights Response Rubric

Date: 2026-09-20  
Gate: `GATE_A_RIGHTS_CALLABILITY`

## Purpose

Prevent a vague business reply such as "可以合作", "可以接 API", or "可以给佣金"
from being mistaken for permission to build the decisive cross-rail routing asset.

A provider response is evaluated claim-by-claim.

## Evidence classes

```text
PASS
= explicit written permission from current official partner contract,
  current official documentation, or company-domain business email

CONDITIONAL_PASS
= written permission exists but only under a clearly stated contract/onboarding
  condition that is feasible and does not destroy the router role

UNKNOWN
= silence, generic cooperation language, "具体签约后看", phone-only statement,
  or documentation that exposes data but says nothing about reuse

FAIL
= explicit prohibition, exclusivity, competitor-comparison ban,
  no retention, no derived-use, or requirement that makes the operator
  the recycler/principal rather than a router
```

## Mandatory dimensions per rail

### R1 — Multi-rail comparison

Question:
May the channel show or use this rail's current estimate while also presenting or
evaluating other licensed recycling partners?

- PASS: explicitly allowed.
- CONDITIONAL_PASS: allowed under branding/display rules.
- UNKNOWN: generic API access only.
- FAIL: exclusivity or competitor-comparison prohibition.

### R2 — Final-outcome visibility

Question:
Can the partner receive the post-inspection/final transaction result?

Minimum useful outcome:
- inspected/revised quote;
- accept/reject or terminal transaction state;
- final payout or settlement amount;
- completion/cancel/return timestamp/state.

At least two overlapping 3C rails must PASS.

### R3 — Non-identifying outcome retention

Question:
May the partner retain minimized non-identifying records after the original order is
completed?

Preferred retained fields:
- rail;
- device model/config bucket;
- non-identifying condition features;
- initial estimate;
- inspection quote;
- accept/reject;
- final payout;
- time-to-cash;
- return/cancel class.

FAIL if all outcome data must be deleted immediately after fulfillment.

### R4 — Derived statistical / routing use

Question:
May retained non-identifying outcome records be aggregated into statistics/models that
influence which rail receives future orders?

This is the decisive moat dimension.

A rail that permits storage only for reconciliation but forbids future routing/model
use does **not** satisfy F1.

### R5 — Competitor benchmarking / ranking

Question:
May the resulting statistics be used for side-by-side performance comparison or
ranking across licensed partners?

A UI leaderboard is not required. Internal routing comparison is sufficient if
explicitly permitted.

### R6 — Economic settlement

Question:
What event earns commission/settlement?

Preferred:
- completed/paid/accepted order.

Reject economic evidence that pays only for raw lead submission while final transaction
quality is irrelevant.

### R7 — Operator role

Question:
Can the operator remain a technology/channel/router?

FAIL if the operator must:
- buy the device;
- take inventory;
- perform grading;
- become recycling principal;
- bear per-device resale/price risk.

### R8 — Data/privacy obligations

Capture:
- controller/processor role;
- retention period;
- deletion duties;
- security/audit requirements;
- whether anonymized/aggregate outputs may survive deletion of identifiable order data.

## Gate-A pass rule

```text
FOR AT LEAST TWO OVERLAPPING 3C RAILS:

R1 ∈ {PASS, CONDITIONAL_PASS}
R2 = PASS
R3 ∈ {PASS, CONDITIONAL_PASS}
R4 ∈ {PASS, CONDITIONAL_PASS}
R6 = PASS
R7 ∈ {PASS, CONDITIONAL_PASS}

AND

NO MATERIAL FAIL ON R5/R8
→ GATE_A_PASS
```

If only one rail satisfies the rule:

`GATE_A_FAIL_FOR_CROSS_RAIL_ASSET`.

If two rails allow transaction integration but R3/R4 remain UNKNOWN:

`GATE_A_REMAINS_UNKNOWN`.

If two rails explicitly prohibit future derived routing use:

`KILL_F1_CURRENT_FORM`.

## Anti-persuasion rules

Do not count these as PASS:
- "欢迎合作";
- "API 都能给";
- "数据可以看";
- "佣金可以谈";
- "签合同后都好说";
- "行业里都这么做";
- verbal-only sales assurance;
- access to a dashboard without explicit reuse terms.

The decisive question is not whether data can be viewed.

It is:

> **May the router lawfully retain minimized non-identifying outcomes and use them to
> choose among competing licensed rails in future transactions?**

## Current provider table

| Dimension | Aihuishou | Xiaozhi/Bearhome | Suhuanji |
| --- | --- | --- | --- |
| R1 multi-rail comparison | UNKNOWN | UNKNOWN | UNKNOWN |
| R2 final-outcome visibility | UNKNOWN_PUBLIC | PASS | PASS_STRONG_DATA_CLOSURE |
| R3 non-identifying retention | UNKNOWN | UNKNOWN | UNKNOWN |
| R4 future derived routing use | UNKNOWN | UNKNOWN | UNKNOWN |
| R5 benchmark/ranking | UNKNOWN | UNKNOWN | UNKNOWN |
| R6 commission/settlement | PARTIAL_PASS | PARTIAL_PASS | UNKNOWN |
| R7 router/channel role | CONDITIONAL_INFERENCE | CONDITIONAL_INFERENCE | CONDITIONAL_INFERENCE |
| R8 data/privacy obligations | UNKNOWN_CONTRACT | UNKNOWN_CONTRACT | UNKNOWN_CONTRACT |

No row above may be upgraded from inference/unknown without current attributable written
evidence.


## Suhuanji contact integrity rule

The current Open Platform says credentials require contact with Suhuanji business
staff, but no current verifiable public email/phone endpoint has been established.

Until an official endpoint is verified:

`DO_NOT_CONTACT_LOOKALIKE_BRANDS_OR_INFER_CORPORATE_IDENTITY`.

Technical API evidence remains usable; outreach evidence does not.
