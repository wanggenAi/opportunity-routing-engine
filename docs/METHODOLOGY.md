# Methodology — Observe Actors, Find the Transaction

## 1. Purpose

This document defines how the Opportunity Routing Engine converts social change into testable commercial opportunities.

The method is empirical:

> Observe which actors are changing, identify the friction created by that change, separate beneficiary from payer, find existing capability, and validate the transaction with real behavior and money.

Philosophy may guide where to look; evidence decides whether to act.

## 2. Unit of analysis: Actor × Change × Need

Do not begin with an industry, product, company, or assumed payer.

Begin with an **actor or group undergoing a measurable change**.

Examples:

- students have more skills/tools but weak access to paid projects;
- young adults reduce large purchases but still seek low-cost experiences;
- elderly people face increasing digital-service friction;
- adult children have less time to coordinate parents' daily needs;
- pet owners spend more time away from home;
- households prefer repair/rental/second-hand instead of replacement;
- skilled workers have fragmented availability that does not map cleanly to demand;
- merchants have idle off-peak capacity;
- AI lowers the cost of a knowledge task;
- one geography has idle resources while another has scarcity.

The system must deliberately scan both individuals and organizations.

## 3. Canonical reasoning chain

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
→ TRANSACTION
→ TEST
→ OUTCOME
```

### Step A — Actor
Who exactly is changing or experiencing friction?

Possible actor types:

- individual;
- household/family;
- student/graduate;
- worker/freelancer/technician/farmer;
- elderly person/caregiver;
- parent/child;
- pet owner;
- merchant/self-employed operator;
- enterprise/manufacturer;
- institution/community;
- overseas actor;
- owner of idle time, skill, equipment, vehicle, inventory, data, space or other resources.

Avoid labels that are too broad to validate.

Weak:
> young people

Stronger:
> Xuzhou university students with basic design/video/data skills who want paid project experience this semester.

### Step B — Change
What is measurably changing for this actor?

Possible evidence:

- prices / income / employment;
- demographics / family structure;
- technology adoption;
- regulation/policy;
- purchase/channel mix;
- lifestyle/time-use;
- search/marketplace activity;
- migration, aging, housing, education, transport;
- resource utilization.

### Step C — Behavior
How is the actor responding?

Look for actions:

- delaying purchases;
- switching to cheaper substitutes;
- renting, sharing, repairing, buying used;
- seeking side income;
- asking relatives/strangers for help;
- using informal groups;
- buying convenience;
- outsourcing;
- using AI/self-service;
- selling idle resources;
- changing where/how they transact.

### Step D — Friction
What difficulty, cost, uncertainty, delay, trust problem, coordination burden or mismatch appears?

The friction must be specific and observable.

### Step E — Need
Express the friction as a desired outcome:

> `[actor] needs [measurable outcome] under [constraints] because the current workaround is [costly/slow/risky/unavailable].`

### Step F — Beneficiary
Who actually receives the value if solved?

This may differ from the actor who initiated the request.

### Step G — Payer
Who loses enough money, time, opportunity, convenience, risk or reputation to pay?

Do not assume the beneficiary pays.

Possible structures:

- user pays;
- family member pays;
- employer pays;
- supplier pays;
- institution/government pays;
- advertiser/sponsor pays;
- counterparty pays;
- platform pays/subsidizes;
- multiple actors share payment.

A need with low direct willingness to pay may still be commercially viable if a credible third-party payer exists.

### Step H — Current workaround
What happens today?

Look for:

- family/friend help;
- chat groups;
- agencies;
- manual labor;
- repeated travel/waiting;
- informal cash services;
- premium software;
- hiring;
- fragmented vendors;
- doing nothing and accepting loss;
- free alternatives with hidden time cost.

The workaround reveals payment potential and the benchmark to beat.

### Step I — Capability
What existing ability/resource can solve the requirement?

Capability may be:

- another individual;
- student/freelancer/specialist;
- skilled worker;
- business/provider;
- AI/model/software;
- product/manufacturer;
- physical asset;
- inventory;
- vehicle/space;
- local presence;
- data/information;
- institution;
- composite workflow.

### Step J — Transaction design
Turn the need into something purchasable.

Define:

- need actor;
- beneficiary;
- payer;
- provider(s);
- orchestrator role;
- deliverable/outcome;
- trust/safety mechanism;
- acceptance criteria;
- price logic;
- timing;
- responsibility boundaries;
- legal/regulatory constraints;
- failure/refund/stop conditions.

If these cannot be bounded, the opportunity is not transaction-ready.

### Step K — Smallest real test

Do not build a platform first.

Prefer tests such as:

- Will 10 people in the target group reveal the same recent paid workaround?
- Will one family pay RMB 50/100/300 for a bounded result?
- Will one merchant accept an off-peak demand-routing test?
- Will one pet owner pay for a trusted local task?
- Will one enterprise pay for a fixed micro-project?
- Can one provider deliver to acceptance standard?
- Can the transaction leave positive contribution margin?

### Step L — Outcome learning

Record:

- actor type;
- beneficiary;
- payer;
- acquisition channel;
- stated need;
- actual payment;
- price;
- provider/resource;
- delivery time;
- trust objections;
- defects/failures;
- refund/dispute;
- repeat/referral;
- reasons for rejection.

## 4. Actor scan matrix

Every broad social scan should intentionally cover multiple actor classes rather than collapsing into enterprise problems.

Minimum categories for a local scan:

```text
Individuals
├─ students / graduates
├─ young workers / flexible workers
├─ single / renting adults
├─ parents / households
├─ elderly / caregivers / adult children
├─ pet owners
├─ value-conscious consumers
├─ skilled workers / farmers / service workers
└─ owners of idle personal resources

Organizations
├─ merchants / self-employed
├─ SMEs
├─ manufacturers
├─ schools / institutions
├─ communities
└─ overseas actors
```

A scan is biased if >50% of promoted hypotheses assume enterprises are the payer without evidence that enterprise opportunities are objectively stronger.

## 5. Market-structure matrix

For each opportunity, test whether the strongest structure is:

- `B2B`
- `B2C`
- `C2C`
- `C2B`
- `SPONSORED / THIRD-PARTY-PAYER`
- `MULTI-SIDED`

Do not force a structure because it is familiar.

## 6. Demand migration

Look for where money, time, attention or resources move:

```text
premium → value-for-money
new → repair / second-hand
ownership → rental / shared use
large commitment → small trial
full-time job → project / flexible work
manual work → AI-assisted work
family self-coordination → paid convenience
offline friction → local/on-demand service
idle personal capability → paid micro-task
unused asset → rental/resale
```

The opportunity often exists on the receiving side of the migration.

## 7. Complaint mining

Complaints are sensors, not proof.

For each cluster ask:

1. Which exact actor is complaining?
2. What changed recently?
3. What action do they take now?
4. What does that workaround cost in money/time/risk?
5. Who benefits if solved?
6. Who could plausibly pay?
7. Is anyone already paying for substitutes?
8. What capability is underused nearby?
9. Why do current solutions fail?

A complaint with no costly workaround and no payer remains `SIGNAL`.

## 8. Intervention contamination and counterfactual controls

Successful cases can produce misleading commercial inference when an external intervention helped create the observed outcome.

Common contaminating interventions include:
- government subsidy;
- public procurement;
- official traffic / promotion;
- platform subsidy;
- free venue/resource support;
- grant-funded programming;
- unusually strong influencer exposure;
- one-time festival/event traffic;
- employer/institution mandates.

Example failure mode:

```text
public program drives users into a merchant
→ merchant revenue improves
→ researcher observes success
→ researcher incorrectly concludes merchant would pay an independent orchestrator for the same traffic
```

The observed success may prove:
- the beneficiary values the outcome;
- the capability works;
- traffic can convert;
- a sponsor can create value.

It does **not** automatically prove:
- who would pay without the intervention;
- how much they would pay;
- whether acquisition economics survive without subsidy;
- whether the result generalizes to ordinary actors.

### Required contamination record

For any strong showcase case, record where relevant:

```text
intervention_present:
intervention_type:
who_funded_it:
who_received_value:
what would happen without it: UNKNOWN / EVIDENCED
independent_payer_observed: YES / NO / UNKNOWN
control_required: YES / NO
```

### Counterfactual-control rule

When a promoted hypothesis depends heavily on a subsidized / officially promoted / unusually supported success case, compare it against at least one actor or transaction without the same support before generalizing the payer thesis.

The control does not need to be a randomized experiment. Early-stage commercial controls may be:
- similar merchant without official traffic;
- similar household without subsidy;
- normal buyer versus grant-funded buyer;
- independent acquisition versus platform-subsidized acquisition;
- ordinary period versus festival/event spike.

The purpose is to answer:

> **Is the payer mechanism intrinsic to the transaction, or are we observing the economics of the intervention?**

Do not remove an opportunity because intervention exists. Instead separate:
- `DEMAND EVIDENCE`;
- `CAPABILITY EVIDENCE`;
- `SPONSOR EVIDENCE`;
- `INDEPENDENT PAYER EVIDENCE`.

## 9. Opportunity anti-patterns

Reject/downgrade ideas based mainly on:

- “people probably want this”;
- assuming every need must become enterprise software;
- assuming the sufferer must pay;
- total market size without acquisition/payment evidence;
- one viral post;
- one subsidized showcase case generalized to an unsubsidized market;
- pure contact forwarding;
- unsafe/unlicensed labor, medical, financial or legal activity;
- bespoke delivery that cannot be bounded;
- high trust burden with tiny margins;
- heavy fixed cost before payer proof;
- solving a loud complaint whose actors consistently refuse to pay and have no third-party payer.

## 10. Operator role

The operator is a **demand analyst + resource architect + transaction orchestrator**, not necessarily the provider.

Core functions:

- observe social change;
- identify actor-specific needs;
- separate beneficiary from payer;
- define requirements;
- discover underused capability/resources;
- design transaction/trust structure;
- identify intervention contamination;
- route;
- quality/risk gate;
- learn from outcomes.

Over time the learning layer may evolve toward:

```text
Actor Graph
+ Demand Graph
+ Capability Graph
+ Trust Graph
+ Transaction Graph
+ Outcome / Learning Graph
```

This is not authorization to build the graphs before real transaction density exists.

## 11. Core maxim

**Follow the shift, but validate with behavior and money.**

Trends tell us where to look. Actors tell us what hurts. Transactions tell us whether we were right.
