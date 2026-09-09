# EXPERIMENT 006 — Xuzhou Youth Micro-Experience Payer Structure

Status: `READY FOR PAYER COMMITMENT TEST`

Date opened: 2026-09-10

Canonical issue: GitHub Issue #5 was originally titled `EXP-005`; the repository already contains `EXPERIMENT_005_ASEAN_SME_AI_MICROFLOWS.md`, so this experiment is assigned **EXP-006** to preserve history and eliminate ID collision.

## Objective

Determine which actor will make a real economic commitment for one small, interest-based youth offline experience in Xuzhou:

1. participant;
2. venue / merchant;
3. blended participant + venue.

This is a `PAYER_SHIFT + TIME_GAP + COORDINATION_GAP` experiment.

It is **not** a dating-app experiment, a generic community build, or proof that young people will pay merely because they say an event sounds attractive.

## Evidence motivating the test

Current Xuzhou evidence is stronger than a generic social-demand narrative:

- local `night school + youth shop` programs have repeatedly routed young participants into cafes, craft spaces and other small venues;
- one Xuzhou cafe reported about 30% revenue growth after hosting youth-night-school activity;
- a later Xuzhou report described the same space-reuse model as increasing customer unit price by about 20% and repeat purchase rate by about 15%;
- 12 linked youth-shop/night-school sites had already covered roughly 600 attendances;
- Xuzhou has also developed many public/free youth activities, so direct participant payment remains unproven and free provision is a real substitute.

Sources:
- https://www.zgjssw.gov.cn/yaowen/202604/t20260427_8570297.shtml
- https://news.jschina.com.cn/yw/202606/t20260625_s6a3d2258e4b0baeb0111da45.shtml
- https://www.zgjssw.gov.cn/shixianchuanzhen/xuzhou/202605/t20260505_8571448.shtml

## Actor map

```text
NEED_ACTOR:
  Xuzhou young adult seeking low-pressure novelty, interest activity,
  after-work/weekend experience or social connection.

BENEFICIARY:
  participant.

PAYER candidates:
  A. participant ticket/deposit;
  B. venue/merchant cash sponsorship or minimum guarantee;
  C. blended participant payment + venue contribution.

CAPABILITY_PROVIDER:
  host / instructor / maker / photographer / activity operator.

RESOURCE_OWNER:
  cafe / studio / bookstore / craft shop / board-game venue / other suitable space.

SPONSOR:
  venue/merchant when qualified foot traffic has measurable commercial value.

ORCHESTRATOR:
  define demand, select one format, recruit the group, route venue/host,
  set scope and price, collect commitment, run acceptance/feedback,
  attribute merchant/participant outcomes where practical.

TRANSACTION TYPE:
  B2C / sponsored / multi-sided.
```

## Core hypotheses

### H1 — participant payer
At least one narrow experience format is strong enough that qualified participants will place real deposits rather than only express interest.

### H2 — merchant payer
At least some venues with off-peak capacity value qualified youth traffic enough to make a real monetary contribution, not merely offer free space.

### H3 — blended payer
A small participant payment plus venue contribution produces better attendance quality and economics than either free attendance or full participant pricing alone.

## What this experiment does NOT test

- whether young people have any social need;
- whether public youth events are popular;
- whether a free event can attract attendees;
- whether an app/community could eventually be built;
- matchmaking or personal-profile brokerage;
- alcohol-centered activity where age/safety controls become material;
- high-risk sports or activities requiring specialist safety controls.

## Phase 0 — choose one bounded event

Use exactly one simple event format for the first commitment test.

Preferred characteristics:
- 8–12 participants;
- 60–90 minutes;
- low equipment cost;
- safe public venue;
- easy acceptance criteria;
- suitable for first-time participants;
- can occur during a venue's weaker time window;
- does not require regulated expertise.

Candidate formats:
- beginner coffee tasting / coffee knowledge micro-session;
- scent / craft micro-workshop;
- beginner photography walk ending at a partner venue;
- hosted board-game / interest session;
- small city-culture / maker experience.

Do not test several formats at once. That would confound payer evidence with format preference.

## Phase A — participant commitment test

Target: 10–15 qualified Xuzhou participants who have recently paid for, searched for or attended comparable after-work/weekend activities.

Ask recent-behavior questions first, then make an exact offer.

Required capture:
- last paid leisure / interest activity;
- actual price paid;
- current workaround for novelty/social activity;
- preferred time and group size;
- biggest attendance blocker;
- exact acceptance/rejection at RMB 29 / 49 / 79;
- whether they will place a real refundable deposit now for the chosen event;
- reason for refusal.

### Participant PASS
For the chosen price, **>=6 qualified participants place real deposits** before the event is produced.

A verbal "I would pay" is not PASS.

## Phase B — venue commitment test

Target: 5–8 cafes / youth shops / studios / small activity spaces with observable off-peak capacity.

Required capture:
- weakest recurring time windows;
- current acquisition/promotion method and cost where disclosed;
- whether similar events have been hosted;
- customer spend / repeat effect if measured;
- value of 8–12 qualified first-time visitors;
- cash sponsorship / minimum guarantee willingness;
- alternative revenue-share structure;
- measurement method for participant consumption / repeat where feasible.

### Venue PASS
At least one venue makes a **real monetary commitment of RMB 200+ per event**, or signs a revenue-share/minimum-guarantee structure with a guaranteed economic contribution of at least RMB 200.

Free space alone is useful capability evidence but does **not** pass the payer gate.

## Phase C — run one real transaction

Proceed only after at least one payer arm passes.

Minimum controls:
- fixed date/time/place;
- 8–12 maximum participants;
- written event scope;
- clear host responsibility;
- participant cancellation/refund rule;
- venue contribution/payment rule;
- basic safety / conduct boundary;
- no collection of unnecessary sensitive personal information;
- attendance evidence;
- direct costs recorded;
- participant payment recorded;
- venue contribution and attributable consumption recorded where possible.

## First real-money design

Default first offer:

```text
Event: one 60–90 minute hosted micro-experience
Capacity: 10 people
Participant test price: RMB 49
Participant commitment threshold: 6 paid/refundable deposits
Venue sponsor test: RMB 200 minimum cash/guaranteed contribution
Direct-cost cap before payer proof: RMB 100
No custom app, website or paid advertising required
```

If a venue passes first, participant price may be reduced, but the change must be recorded as a separate blended-payer test rather than silently altering the experiment.

## Strong pass

Within the first test cycle:
- >=10 qualified participant conversations;
- >=5 venue conversations;
- participant or venue payer gate passes with real commitment;
- >=1 real event occurs;
- direct cash revenue/contribution covers direct event costs;
- no material safety/dispute failure;
- at least one payer requests, prepays, or explicitly commits to another event.

## Partial pass

Examples:
- participants deposit at RMB 29 but not RMB 49;
- venues provide free space but refuse cash sponsorship;
- venue will pay only after demonstrable first-event conversion;
- one narrow format converts while generic social events do not;
- attendance works but repeat intent is weak.

Do not call these validated. Narrow the payer/format hypothesis and retest.

## Fail / stop

Stop or downgrade if:
- 15 qualified participants produce zero real deposits at the lowest tested viable price;
- 8 qualified venues produce zero monetary commitment and see no measurable traffic value;
- acquisition effort/cost overwhelms event gross contribution;
- free/public events satisfy the same outcome sufficiently;
- coordination/safety burden is too high for the ticket/sponsor economics;
- no payer wants repetition after one completed event.

## Field locations

Do not wander broadly. Start where the relevant actors already concentrate:
- youth-shop / night-school-linked commercial areas;
- cafes / studios / craft venues with non-peak periods;
- university-adjacent youth activity areas;
- central commercial areas where young workers already spend after work/weekends.

For each trip, use `docs/FIELD_VALIDATION_PLAYBOOK_XUZHOU.md` and record one critical unknown.

## Evidence levels

Use the repository field-playbook scale:
- Level 0: statement;
- Level 1: prior behavior;
- Level 2: exact price acceptance;
- Level 3: deposit / written sponsor commitment;
- Level 4: completed transaction;
- Level 5: repeat / referral.

This experiment does not pass from Level 0–2 evidence alone.

## Decision after experiment

If participant payer passes:
- repeat the same format before broadening categories;
- test acquisition and repeat economics.

If venue payer passes:
- test whether attributable traffic/revenue is strong enough for repeated sponsorship.

If blended payer wins:
- keep both payer roles explicit in the Transaction Graph.

If all fail:
- mark the youth-experience hypothesis `DORMANT` / `REJECTED` in current form;
- do not rationalize the failure into an app/community build.

## Governing question

**Who will commit real economic value for this exact event before we build anything?**
