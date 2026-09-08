# EXP-002 Xuzhou Actor-First Ranking V1 — 2026-09-08

Status: `PRELIMINARY / RECOMPUTED / NOT PROOF`

This ranking supersedes the old enterprise-heavy ranking. Scores use `docs/OPPORTUNITY_SCORECARD.md`. Numerical score never overrides hard gates or evidence confidence.

## 1. Score table

| Priority | ID | Opportunity | Raw | Penalty | Final | Hard gate | Confidence | Decision |
|---|---|---|---:|---:|---:|---|---|---|
| 1 | XZA-002 | Trusted neighborhood pet-care micro-network | 79 | 0 | 79 | G3 `CONDITIONAL` — home access / animal safety / liability | MEDIUM | **B: INVESTIGATE — best personal-payer field candidate** |
| 2 | XZA-003 | Youth interest-based micro-social experiences | 75 | 0 | 75 | G1 `UNKNOWN` — self-pay vs sponsor/venue payer | MEDIUM | **B: INVESTIGATE** |
| 3 | XZA-001 | Student / young capability → bounded paid projects | 81 | 0 | 81 | G1 `UNKNOWN` — payer varies by project | LOW-MEDIUM | **B: INVESTIGATE despite high raw score** |
| 4 | XZA-004 | Trusted home micro-services / household task routing | 76 | -10 incumbent | 66 | G3 task-dependent | MEDIUM | **B: INVESTIGATE narrowly** |
| 5 | XZA-012 | Visitor micro-experience / photography routing | 71 | -10 OTA/local incumbent | 61 | PASS for non-regulated experience | MEDIUM | C: WATCH |
| 6 | XZA-005 | Second-hand device inspection / transaction assurance | 73 | -10 strong inspection/platform incumbents | 63 | liability needs bounding | MEDIUM | C: WATCH |
| 7 | XZA-007 | Value-for-money local experience router | 71 | -10 strong discovery/coupon incumbents | 61 | G1 monetization weak | MEDIUM | C: WATCH |
| 8 | XZA-006 | Graduation / move-out liquidation and reuse | 69 | -10 strong C2C substitutes | 59 | PASS | MEDIUM | C: WATCH / SEASONAL |
| 9 | XZA-010 | Single / renter local micro-help | 68 | -10 mature errand/service platforms | 58 | direct payment evidence weak | LOW | C: WATCH |
| 10 | XZA-011 | Youth interest-skill micro-classes | 74 | -10 public/free low-cost substitutes | 64 | G1 direct paid demand incomplete | LOW-MEDIUM | C: WATCH |
| 11 | XZA-008 | Adult-child sponsored elder digital/life assistance | 68 | -20 regulatory/safety ambiguity in broad form | 48 | G3 `CONDITIONAL` | MEDIUM | D/C: DO NOT ENTER BROADLY |
| 12 | XZA-009 | Holiday child-care / activity coordination | 64 | -20 safety/licensing ambiguity | 44 | G3 `CONDITIONAL` / free public substitute | HIGH on pain, LOW on business fit | D: DO NOT ENTER DIRECTLY |

## 2. Why the top decision is not the highest raw score

XZA-001 has a higher raw score than XZA-002, but its payer definition is broad and the business can easily collapse into an unstructured freelance/job marketplace. Therefore it does not deserve first field priority yet.

XZA-002 (pet care) has a more explicit transaction:

```text
Pet owner / payer
→ needs pet cared for during absence
→ pays per visit / day
→ vetted local capability performs checklist
→ evidence returned
→ transaction completes
```

The main unknown is not whether payment exists. It is whether an orchestrated trust layer can create enough additional value over direct informal hiring or pet-shop boarding.

## 3. Strongest personal-payer candidate: pet-care trust layer

### Evidence supporting it
- Quanshan's registered dog/cat count exceeds 180,000 and pet diagnostic institutions rose sharply over five years.
- Jiangsu consumer research indicates continued planned pet spending growth among a meaningful share of pet owners.
- Home pet-feeding / dog walking is already a paid service category.
- Informal provider markets exist, so supply is not hypothetical.

### The real transaction friction
The customer is not mainly buying "someone who can pour food into a bowl".

The customer is buying:
- trust to enter the home;
- punctuality;
- service evidence;
- pet-specific instructions followed correctly;
- emergency escalation;
- accountability if something goes wrong.

If the engine can solve these better than an unmanaged stranger transaction, there may be orchestrator value.

### Cheapest decisive validation
Before building any platform:
1. interview 15–20 Xuzhou pet owners;
2. interview 10–15 potential local sitters/providers;
3. capture existing price, how they currently find providers, trust blockers, what proof they require and whether they would pay a premium / booking fee for a verified transaction;
4. if trust/payment gate passes, run 1–3 manually managed paid visits with explicit pet profile, checklist, evidence and emergency boundaries;
5. measure customer willingness to repeat and provider economics.

### Stop rule
Stop or redesign if:
- 20 qualified pet owners show no willingness to use a managed/verified service;
- price spread is too small to support coordination;
- direct trusted-friend / pet-store alternatives dominate with no unresolved friction;
- home-access / liability risk cannot be bounded acceptably.

## 4. Second personal candidate: youth interest social

The evidence for **need** is strong: Xuzhou repeatedly organizes low-pressure interest-based social events, marriage/social services are included in Youth Card, and night-school + small-shop formats attract young participants.

But the payer is not yet proven. Many existing events are public-interest or subsidized.

Therefore the experiment should test:
- will participants pay RMB 29 / 49 / 79 for a well-hosted small interest event?
- or is the stronger model venue/sponsor-paid because events generate store traffic?

Do not build a dating app. Test one event transaction.

## 5. Cross-candidate insight: trust is emerging as a major demand class

Across personal markets, the repeated unresolved issue is often not lack of supply:

- pet owner can find a sitter, but cannot easily trust them;
- household can find cleaners, but quality varies;
- second-hand buyer can find cheap devices, but cannot verify condition;
- elder family can find helpers, but safety/accountability matters;
- social participant can find people online, but cannot guarantee a safe, comfortable offline context.

This suggests a deeper opportunity thesis:

> **In fragmented C2C / local-service markets, the orchestrator may earn value by manufacturing trust — verification, task definition, evidence, QA, accountability and outcome history — rather than by merely manufacturing discovery.**

This thesis should become a first-class variable in future scans.

## 6. Current portfolio decision

Run in parallel, cheaply:

1. `EXP-004` — personal-payer validation of trusted pet care;
2. continue `VERTICAL EXP-003` — SME bounded micro-project paid test;
3. prepare a no-code youth social payer test only after pet-care interviews begin;
4. do not build a marketplace yet.

The first category to produce accepted paid transactions with repeat/referral signal earns the next automation investment.
