# Formal Truth

Last updated: 2026-09-10

This document is the project's commercial source of truth. It separates observations, hypotheses, unknowns, decisions and explicit rejections. No attractive narrative may override missing evidence.

## 1. Mission

Continuously detect opportunity created by social and market change, identify the actors affected, convert repeated friction into explicit need hypotheses, identify the real beneficiary and payer, route viable capabilities/resources, manufacture trust where economically justified, design bounded transactions, and learn from real outcomes.

## 2. Core operating model

```text
ACTOR
→ CHANGE
→ BEHAVIOR
→ FRICTION
→ NEED
→ BENEFICIARY
→ PAYER
→ CURRENT WORKAROUND
→ CAPABILITY
→ TRANSACTION DESIGN
→ REAL-WORLD TEST
→ OUTCOME
→ LEARNING
```

Operationally:

```text
观势 → 察需 → 找能 → 成事 → 反馈学习
```

Philosophy may guide where to look. Behavior and money decide whether the hypothesis survives.

## 3. Actor-first truth

The system must not default to enterprises as the demand side.

For every serious opportunity, explicitly identify:
- `NEED_ACTOR` — who experiences the friction or unmet need;
- `BENEFICIARY` — who receives the result;
- `PAYER` — who has incentive and ability to pay;
- `CAPABILITY_PROVIDER` — who/what can solve it;
- `RESOURCE_OWNER` — who controls relevant skill, time, space, equipment, inventory, data, access or other resource;
- `SPONSOR` — where relevant, who funds the beneficiary's outcome because they capture another benefit;
- `ORCHESTRATOR` — who defines, routes, verifies and closes the transaction.

These roles may be the same actor or several different actors.

## 4. What we are NOT building

- a generic trend-report business;
- a social-media sentiment toy;
- a crawler whose value is merely collecting public information;
- a raw lead-list resale business;
- a general marketplace before transaction density exists;
- a traditional intermediary that only exchanges contact details;
- a system that treats complaints as proof of willingness to pay;
- a system that assumes the sufferer must be the payer;
- a system that privileges B2B because enterprise budgets are easier to observe;
- a system that treats LLM confidence as commercial truth;
- a broad AI product before a repeated paid workflow exists.

## 5. Canonical transaction-gap ontology

The system now treats the following as first-class structural gaps:

1. `DEMAND_GAP`
2. `CAPABILITY_GAP`
3. `PRICE_GAP`
4. `TRUST_GAP`
5. `INFORMATION_GAP`
6. `GEOGRAPHY_GAP`
7. `TIME_GAP`
8. `COORDINATION_GAP`
9. `PAYER_SHIFT`
10. `TECHNOLOGY_SHIFT`

Source of truth: `docs/THESIS_TRANSACTION_GAPS.md`.

A gap is not a business. It becomes commercially relevant only when a real payer will exchange economic value to reduce it.

## 6. Core commercial discipline

- `Complaint != Demand`.
- `Demand != Willingness to Pay`.
- `Trend != Business`.
- `Market Size != Customer Acquisition`.
- `LLM Confidence != Commercial Evidence`.
- `UNKNOWN != PASS`.
- Existing payment proves a category can monetize, not that our proposed transaction has value.
- Public/free provision proves need may exist, but is also a substitute that can destroy direct-pay economics.
- One transaction validates possibility, not repeatability.
- Code completion is never evidence of commercial success.

## 7. Opportunity truth gates

A candidate is not commercially qualified until evidence exists across:

1. `PAIN` — a real consequential need/friction exists;
2. `FREQUENCY` — it repeats or affects enough activity;
3. `PAYER_CLARITY` — payer is identifiable and has incentive/ability to pay;
4. `PAYMENT_EVIDENCE` — material spending or costly workaround behavior exists;
5. `SUPPLY` — realistic capability/resource can solve it;
6. `TRANSACTIONABILITY` — scope, price, trust, delivery, verification and responsibility can be bounded;
7. `LEGAL / TRUST / SAFETY` — the proposed transaction can be run within acceptable boundaries;
8. `ACQUISITION / ECONOMICS` — the transaction is not destroyed by acquisition, coordination, support or liability cost.

Canonical hard gates and weights remain in `docs/OPPORTUNITY_SCORECARD.md`.

## 8. Strong evidence hierarchy

Highest-value evidence includes:
- completed purchases / paid services;
- repeat purchase / booking / subscription;
- deposits or signed sponsor commitments;
- actual service prices;
- procurement / RFQ / tenders;
- hiring specifically to solve the problem;
- family members paying for another person's outcome;
- merchant subsidy or spending for traffic/conversion;
- costly manual workaround;
- repeated failed transactions / repricing / relisting;
- referral and repeat intent backed by behavior.

Macro data, surveys, searches, complaints and social content may generate hypotheses but cannot independently validate a transaction.

## 9. Intervention contamination truth

A strong observed outcome can be commercially misleading if it was created or amplified by an external intervention.

Relevant interventions include:
- government subsidy;
- public procurement;
- official traffic / media exposure;
- platform subsidy;
- free venue/resource support;
- grant-funded programming;
- one-time festival/event traffic;
- institution/employer mandates;
- unusually strong influencer exposure.

The engine must distinguish:

```text
DEMAND EVIDENCE
CAPABILITY EVIDENCE
SPONSOR EVIDENCE
INDEPENDENT PAYER EVIDENCE
```

They are not interchangeable.

Example:

> A youth program sends people into a cafe and cafe revenue improves.

This supports that:
- youth traffic can have merchant value;
- the venue can host the activity;
- a sponsor/intervention can create a working transaction.

It does **not** prove:
- the cafe would independently pay an external orchestrator;
- the same economics exist without official traffic;
- another ordinary cafe would pay;
- participant direct-pay willingness exists.

When a promoted hypothesis relies materially on a subsidized / officially promoted / unusually supported success case, at least one comparison without the same support is required before generalizing the payer thesis.

Source of truth: `docs/METHODOLOGY.md`, section `Intervention contamination and counterfactual controls`.

## 10. Long-run learning architecture

The intended learning system is now:

```text
Actor Graph
+ Demand Graph
+ Capability Graph
+ Trust Graph
+ Transaction Graph
+ Outcome / Learning Graph
```

This is a long-run architecture, not authorization to build those systems now.

The manual transaction ledger must come first. Automation earns its place only after repeated real transactions expose a recurring bottleneck.

## 11. Current truth status

**Status: GO — continue building and testing the Actor-First Opportunity Routing method. No vertical is validated.**

Xuzhou remains the first field laboratory because public hypotheses can be turned into local commitment tests quickly.

The current broad scan is:
- `docs/research/XUZHOU_ACTOR_FIRST_SCAN_V2_2026-09-10.md`

It contains **38 friction records** across youth, students, workers, households, pet owners, merchants, institutions, asset owners and enterprises.

Only four currently deserve targeted validation.

## 12. Current execution priority

Source of truth:
- `docs/results/EXP_002_XUZHOU_ACTOR_FIRST_RANKING_V2_2026-09-10.md`

### Priority 1 — Youth micro-experience payer shift

Status: `B: INVESTIGATE / FIRST COMMITMENT TEST`

Canonical experiment: `EXP-006`.

Why it moved to first:
- repeated local youth participation exists;
- merchant-side value is measurable in local cases;
- one reported youth-night-school cafe experienced roughly 30% revenue growth;
- later reporting on the same space-reuse logic described about 20% higher customer unit price and 15% higher repeat rate;
- supply/resources already exist;
- one event is low-capital and bounded;
- the exact payer can be tested with real deposits / merchant guarantees instead of more opinion research.

Critical unknown:
> Will the participant, venue, or both make real economic commitment for one exact event?

Selection-bias correction:
> The strongest cafe case received youth-program / official traffic support. It is a mechanism anchor, not sufficient independent merchant-payer proof. EXP-006 therefore requires merchant controls without relying on the same support story.

No software build is authorized.

### Priority 2 — Skills-to-income + outcome-linked sponsor

Status: `B: INVESTIGATE`.

Important new payer hypothesis:
- trained learner is beneficiary/capability provider;
- project buyer may pay for accepted output;
- training institution may have an economic incentive because Xuzhou's 2026 subsidized training framework allows additional support for classes exceeding the stable-employment threshold.

Critical unknown:
> Will any training provider / project buyer actually pay for a bounded capability-to-output conversion layer?

Do not turn this into generic recruitment or labor dispatch.

### Priority 3 — Xuzhou bounded SME micro-project

Status: `B: INVESTIGATE / SECONDARY VERTICAL`.

Canonical experiment: `EXP-003`.

Payer identity is clear, but willingness to buy the proposed fixed-project format remains unproven.

### Priority 4 — Trusted pet-care transaction layer

Status: `C: TRUST-RESOLUTION TEST`.

Canonical experiment: `EXP-004`.

Correction from V1:
- raw score remains strong because payment behavior exists;
- the canonical scorecard requires a `-20` penalty while home-access / physical-safety trust risk remains unresolved;
- therefore it is no longer current priority #1.

The purpose of EXP-004 is now explicitly to determine whether trust controls can remove that penalty economically.

## 13. Current explicit rejections / dormant forms

Do not spend meaningful build time on these current forms:
- generic Xuzhou job-matching platform;
- generic youth-housing information product;
- generic paid-study-room directory;
- broad household-service marketplace;
- pure second-hand listing marketplace;
- pure tourism/content guide;
- direct childcare marketplace;
- broad eldercare marketplace;
- public idle-asset brokerage;
- generic freelancer marketplace;
- broad ASEAN AI SaaS before a paid repeated microflow exists.

These can be revisited only if new evidence changes the transaction mechanism.

## 14. Public / sponsored payer truth

A public or third-party payer can be commercially real, but must be modeled correctly.

Examples currently observed:
- merchant traffic/revenue can justify venue-side contribution to youth experiences;
- training-outcome incentives can create a sponsor hypothesis around learner outcomes;
- government procurement proves elder-service payment categories exist.

But:
- public provision must not be misreported as private consumer willingness to pay;
- theoretical sponsor interest is not a PASS;
- long procurement cycles and regulated service boundaries must be scored honestly;
- subsidized success must not be generalized to independent payer behavior without a control.

## 15. Experiment ID truth

Repository history created an ID collision:
- `docs/EXPERIMENT_005_ASEAN_SME_AI_MICROFLOWS.md` already exists as EXP-005;
- GitHub Issue #5 was later opened with the title `EXP-005` for the youth micro-experience payer test.

Canonical resolution as of 2026-09-10:
- ASEAN SME AI microflows retains **EXP-005**;
- youth micro-experience payer structure is **EXP-006**;
- historical references to youth as EXP-005 should be treated as stale and corrected when touched.

No experiment history is deleted to hide the inconsistency.

## 16. Current field rule

Every field trip must resolve a defined unknown.

Required before departure:

```text
Hypothesis:
Critical UNKNOWN:
Who to interview:
Where to find them:
5–8 questions:
What counts as PASS:
What counts as FAIL:
What evidence to record:
Next action:
```

A friendly answer is not evidence. A refusal at a real price is evidence. A deposit is stronger. Completed payment + delivery + repeat/referral is stronger still.

## 17. Immediate build rule

Current priority is:

```text
observe
→ hypothesize
→ collect behavioral/payment evidence
→ run field commitment test
→ complete first real-money transaction
→ repeat manually
→ identify repeated bottleneck
→ automate only that bottleneck
```

Not:

```text
build platform
→ search for users later
```

## 18. Hard unknowns

1. Can the engine repeatedly discover opportunities that survive real payment tests?
2. Can it discover payer shifts earlier than ordinary idea-first research?
3. Does manufacturing trust create enough incremental willingness to pay to cover its cost?
4. Can idle skills/assets be converted into standardized accepted outcomes rather than low-value listings?
5. Which acquisition channels produce transaction density at acceptable cost?
6. Which payer structures repeat rather than producing one-off novelty?
7. Which trust controls materially change conversion rather than merely adding process?
8. When does orchestration create defensible value rather than bypass risk?
9. Can outcome data improve future ranking decisions?
10. Which repeated bottleneck, if any, eventually justifies software automation?
11. How often do subsidized / intervention-backed showcase cases overstate independent payer economics, and can simple controls prevent that error?

## 19. Governing truth

**Trends tell us where to look. Actors show us the friction. Money, delivery and repetition tell us whether we found a business.**
