# EXP-002 Xuzhou Actor-First Ranking V2 — 2026-09-10

Status: `CURRENT RESEARCH PRIORITY / NOT COMMERCIAL VALIDATION`

This memo supersedes `EXP_002_XUZHOU_ACTOR_FIRST_RANKING_V1.md` as the current research-priority ranking.

Source pool:
- `docs/research/XUZHOU_ACTOR_FIRST_SCAN_V2_2026-09-10.md`
- `docs/OPPORTUNITY_SCORECARD.md`
- `docs/THESIS_TRANSACTION_GAPS.md`

The score is a test-prioritization tool. Hard gates and evidence confidence override attractive totals.

## 1. Current top four

| Execution priority | Candidate | Raw | Penalty | Final | G0 | G1 | G2 | G3 | Confidence | Decision |
|---:|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | Youth micro-experience payer shift | 84 | 0 | 84 | PASS | **UNKNOWN** — participant vs venue vs blended | PASS for one bounded event | PASS for low-risk format | MEDIUM-HIGH | **B: INVESTIGATE / FIRST COMMITMENT TEST** |
| 2 | Skills-to-income + outcome-linked sponsor | 81 | 0 | 81 | PASS | **UNKNOWN** — training institution / project buyer commitment unproven | CONDITIONAL on one bounded project outcome | PASS if kept outside employment placement / regulated work | MEDIUM | **B: INVESTIGATE** despite >80 |
| 3 | Xuzhou bounded SME micro-project | 76 | 0 | 76 | PASS | **UNKNOWN** — buyer exists, fixed-project willingness not yet observed | PASS for defined task classes | PASS for allowed task classes | MEDIUM | **B: INVESTIGATE / EXP-003** |
| 4 | Trusted pet-care transaction layer | 78 | **-20** unresolved home-access / physical-safety trust risk | 58 | PASS | PASS — owner pays existing category | CONDITIONAL | **CONDITIONAL** | MEDIUM | **C: TRUST-RESOLUTION TEST / EXP-004** |

No candidate is currently `VALIDATED`.

No candidate may be called `A: TEST NOW` while a required hard gate remains `UNKNOWN`.

## 2. Score breakdown

Canonical dimensions are exactly those in `docs/OPPORTUNITY_SCORECARD.md`.

| Dimension | Max | Youth payer shift | Skills-to-income sponsor | SME micro-project | Pet trust layer |
|---|---:|---:|---:|---:|---:|
| Pain severity | 10 | 6 | 8 | 7 | 7 |
| Frequency / density | 10 | 8 | 9 | 7 | 7 |
| Payment evidence | 15 | 12 | 10 | 9 | 13 |
| Current-solution weakness | 10 | 7 | 7 | 7 | 8 |
| Supply / capability availability | 5 | 5 | 5 | 5 | 4 |
| Acquisition feasibility | 10 | 9 | 8 | 7 | 7 |
| Delivery controllability | 10 | 9 | 8 | 8 | 7 |
| Time to first cash | 10 | 10 | 8 | 8 | 9 |
| Unit economics potential | 5 | 4 | 4 | 4 | 3 |
| Defensibility / learning | 5 | 4 | 4 | 4 | 4 |
| Operator fit | 5 | 5 | 5 | 5 | 4 |
| Capital efficiency | 5 | 5 | 5 | 5 | 5 |
| **Raw total** | **100** | **84** | **81** | **76** | **78** |
| Penalty |  | 0 | 0 | 0 | -20 |
| **Final** |  | **84** | **81** | **76** | **58** |

## 3. Why youth micro-experience moves to execution priority #1

This is a change from V1, where pet care was first.

The new evidence is transaction-structure evidence, not merely trend evidence:

1. Xuzhou's `night school + youth shop` model has already routed groups into commercial venues.
2. One local cafe reported about **30% revenue growth** after hosting these activities.
3. A later local report described the space-reuse model as producing about **20% higher customer unit price** and **15% higher repeat rate**.
4. The capability side is abundant: venues, hosts, makers, cafes and small activity spaces already exist.
5. One event can be bounded, manually orchestrated and tested without software or material fixed cost.
6. The exact payer remains unknown, but that unknown can be attacked with real participant deposits and real merchant commitments rather than another survey.

Sources:
- https://www.zgjssw.gov.cn/yaowen/202604/t20260427_8570297.shtml
- https://news.jschina.com.cn/yw/202606/t20260625_s6a3d2258e4b0baeb0111da45.shtml

### Why no `-10 low-cost incumbent` penalty yet

Public/free youth activities are a serious substitute and are already reflected in the `current-solution weakness = 7` rather than 10.

The formal `-10` incumbent penalty applies when a low-cost incumbent dominates **with little unresolved friction**. Current evidence still leaves unresolved:
- timing;
- niche format;
- small-group quality;
- merchant off-peak capacity;
- repeat commercial events;
- exact payer structure.

If field interviews show free/public activity solves the same outcome adequately, apply the penalty and downgrade immediately.

## 4. First minimum real-money experiment

Canonical test: `docs/EXPERIMENT_006_XUZHOU_YOUTH_MICRO_EXPERIENCE_PAYER.md`.

### Hypothesis
For one exact low-risk 8–12 person micro-experience, either participants or a venue will make a real economic commitment before production because the experience or qualified foot traffic has measurable value.

### Critical UNKNOWN
`PAYER`:
- participant ticket;
- venue sponsorship / minimum guarantee;
- blended.

### Who to interview
- 10–15 young adults with recent paid/attended after-work or weekend activity behavior;
- 5–8 cafes / youth shops / studios / activity venues with weak recurring time windows.

### Where to find them
- youth-shop / night-school-linked commercial areas;
- central commercial areas with after-work youth traffic;
- university-adjacent activity zones;
- suitable cafes/studios with observable off-peak periods.

Do not walk around without this payer question.

### Participant questions
1. What was the last leisure / interest activity you actually paid for?
2. What did it cost?
3. What did you do last weekend / after work instead?
4. What makes you avoid small-group activities?
5. For this exact event, which price do you accept: RMB 29 / 49 / 79?
6. Will you place a real refundable deposit now at the selected price?
7. What exact condition would make you refuse?

### Venue questions
1. Which recurring hours are genuinely underused?
2. How do you currently acquire new customers and what does it cost?
3. Have you hosted an activity? What happened to customer spend or repeat visits?
4. What are 8–12 qualified first-time visitors worth economically?
5. Will you pay RMB 200+ as a sponsor / minimum guarantee for this exact event?
6. If not cash, will you accept a revenue-share with a guaranteed minimum contribution?
7. What measurable outcome would make you repeat next month?

### PASS
At least one payer arm reaches Level 3 commitment:
- **participant arm:** >=6 qualified participants place real deposits; or
- **venue arm:** >=1 venue commits >=RMB 200 cash / guaranteed economic contribution.

Then run one event only.

### FAIL
- 15 qualified participants produce zero deposits at the lowest viable price; AND
- 8 qualified venues produce zero monetary commitment; or
- acquisition / coordination economics exceed realistic gross contribution; or
- public/free substitutes fully satisfy the same outcome.

### Evidence to record
- anonymized participant deposit count and price;
- refusal reasons;
- venue written commitment / refusal;
- venue weak-time window;
- event direct cost;
- attendance;
- participant revenue;
- venue contribution;
- attributable participant consumption where practical;
- repeat commitment;
- disputes / safety incidents;
- operator time.

### Next action
Do **not** build software. Resolve G1 with real commitments first.

## 5. Candidate #2 — skills-to-income + outcome-linked sponsor

### Actor structure

```text
NEED_ACTOR / BENEFICIARY: trained student / graduate / learner
PAYER candidates:
  - project buyer
  - training institution with outcome-linked incentive
  - employer / sponsor
CAPABILITY_PROVIDER: learner / student / young worker
ORCHESTRATOR: task definition + proof + QA + acceptance + outcome evidence
```

### New evidence
Xuzhou's 2026 subsidized skill-training policy states that training classes with stable employment above 50% can receive up to 20% additional subsidy tilt.

That does **not** prove a training institution will buy project orchestration. It does prove that employment outcome has economic value to an actor other than the learner.

Source:
- https://szb.cnxz.com.cn/dscb/pc/con/202606/30/content_52078.html

### Critical unknown
Will a training provider or project buyer commit money to a **bounded outcome** such as a real project, verified portfolio artifact or accepted deliverable, rather than generic training / recruitment?

### Cheapest next test
Interview 5 training providers / skill-program operators and 5 real project buyers. Ask for the last cohort/project, actual placement/project evidence, current cost, and an exact paid/sponsored pilot structure.

Do not create an employment-placement product.

## 6. Candidate #3 — SME bounded micro-project

EXP-003 remains valid because:
- payer identity is observable;
- existing businesses spend on relevant capability;
- delivery can be bounded;
- first cash could be fast;
- no platform is required.

It does **not** outrank the broader scan merely because enterprise budgets are easier to observe.

The decisive unknown remains:
> Will one Xuzhou business pay for a fixed accepted result in this format?

Continue `EXP-003` unchanged as a secondary parallel paid test.

## 7. Candidate #4 — pet trust layer is corrected, not abandoned

V1 gave the pet candidate a raw/final score of 79 with no penalty while simultaneously recording home access / animal safety / liability as unresolved.

That conflicts with the canonical scorecard, which requires:

> `-20 unresolved vulnerable-person / home-access / physical-safety trust risk`

V2 corrects the arithmetic rather than protecting the old conclusion.

### Interpretation
This does **not** mean pet care has no demand.

Payment evidence is strong. The exact question is whether a managed trust layer can resolve enough of the home-entry / reliability / liability problem to remove or materially reduce the penalty **without destroying unit economics**.

Therefore:
- keep owner/provider interviews active;
- do not call it the #1 opportunity;
- do not run home-access transactions until trust controls and responsibility boundaries are acceptable;
- if trust can be demonstrably bounded, rescore.

## 8. Explicitly not promoted

Despite real signals, the following remain `WATCH / DORMANT / REJECT` in current form:
- generic job matching;
- generic youth housing information;
- paid-study-room directory;
- broad household-services marketplace;
- second-hand listing marketplace;
- broad tourism guide / content routing;
- direct childcare marketplace;
- broad eldercare marketplace;
- public idle-asset brokerage;
- broad ASEAN AI SaaS.

The reasons are combinations of strong incumbents, free substitutes, safety/regulation, unclear payer, acquisition economics or insufficient distinct orchestrator value.

## 9. Portfolio decision

Current execution order:

```text
1. EXP-006 — resolve youth payer with real commitment
2. skills-to-income sponsor/payer discovery — no platform, no recruitment business
3. EXP-003 — pursue one bounded SME paid result in parallel
4. EXP-004 — resolve pet trust/home-access gate before paid home-entry transaction
```

Only the first routes that produce Level 4–5 evidence — completed payment/delivery and repeat/referral — earn automation investment.

## 10. Governing decision

**The project remains GO as a method. No vertical is validated. The highest-value next information is payer commitment, not more code.**
