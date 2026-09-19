# Transaction Unit Validation 001 — Clean-Slate Flows

Date: **2026-09-19**

Status: **CSVF-003 PRIMARY / LIVE BUYER TASK BOUND / SAME-SCOPE EXECUTOR COST MISSING**

Parent:
- `CLEAN_SLATE_VALUE_FLOW_SCAN_001`

## 1. Purpose

The clean-slate scan produced three fresh flow shapes.

This validation does not ask which one sounds most interesting.

It asks whether each can already produce:

```text
BUYER TASK
+
BUYER MONEY
+
COMPATIBLE PROVIDER
+
PROVIDER COST
+
ACCEPTANCE
=
VISIBLE OPERATOR ECONOMICS
```

A visible buyer/provider price difference is not enough if a mature channel already owns the missing edge.

---

## 2. CSVF-001 — Content micro-orders

### Buyer unit

A current remote short-video editing request is priced at approximately:

```text
RMB 500 / project
```

The work is roughly one-day fast packaging/editing for Douyin content, with expected ongoing volume around 1–2 videos per week.

Source:

- https://www.yuanjisong.com/job/allcity/yunying

### Provider unit

A current independent editor with five years of experience publicly prices:

- simple/basic short video: lower tiers;
- more complex talking-head / e-commerce short video: roughly **RMB 150–300 / video**;
- up to 2 free revisions.

Source:

- https://www.ukezhitan.com/resource/42975635701661696

### Theoretical spread

```text
Buyer: RMB 500
Provider: RMB 150–300
Gross spread: RMB 200–350
```

This is only a gross calibration range.

It excludes:
- acquisition;
- platform fees;
- tax;
- briefing/QA;
- failed delivery;
- rework;
- refund/replacement.

### Why this is NOT promoted

The observed buyer is already using a mature freelancer marketplace with direct applicants.

Therefore:

```text
PRICE SPREAD EXISTS
!=
OUR MISSING EDGE EXISTS
```

If we simply insert ourselves between a marketplace buyer and marketplace editor, we are an unnecessary extra layer.

Current state:

`UNIT_ECONOMICS_CALIBRATION_ONLY / DEPRIORITIZE_AS_FIRST_FLOW`

---

## 3. CSVF-002 — SME AI micro-projects

### Buyer-side signal

A current project-coordination company advertises lightweight enterprise AI projects with a payout signal around:

```text
RMB 5,000 / project
```

covering agents, knowledge bases, Dify/n8n/Coze integrations, RPA, data sync, reports, CRM/API work.

Source:

- https://www.zhaopin.com/zhaopin/3392a386946d41f58e90aab2676d8cd2/

### Provider-side signal

Independent AI providers and part-time AI developers clearly exist.

Examples:

- https://www.ukezhitan.com/resource/10529337131994112
- https://ready-2-remote.com/analyze/recvtnaCEiRKGW

But their public prices do **not** bind the same deliverable, acceptance tests or support burden.

### Why this flow fails now

The observed buyer-side actor is already doing the thing we wanted to do:

```text
collect project
→ scope / quote
→ route to developer
→ coordinate delivery
```

So inserting ourselves again duplicates an existing intermediary.

Also:

```text
RMB 5,000 buyer payout
-
unknown compatible provider cost
=
UNKNOWN margin
```

Current state:

`FAIL_CURRENT_TRANSACTION_UNIT / KILLED_FROM_ACTIVE_SET`

Revival condition:

Only reopen with:
- a **direct SME buyer** outside an AI agency/platform;
- a bounded acceptance specification;
- an independent provider quote for the **same** specification.

---

## 4. CSVF-003 — Local-presence field microtasks

This remains the strongest fit with the original commercial logic.

### Historical calibration task

A Polish building-materials company recently offered around **RMB 700–800** for one day of Shanghai exhibition research by a Chinese student/part-timer.

The work was checklist-driven:
- locate manufacturers;
- ask predefined questions;
- collect cards/catalogues;
- take photos;
- return a short report.

The task itself expired on 2026-09-16, so it is calibration only.

Source:

- https://www.reddit.com/r/AskChina/comments/1wcbrn7/

### Why it mattered

The buyer explicitly had trouble finding a reliable local person.

At the same time, multiple potential executors appeared quickly.

That is much closer to the desired structure:

```text
BUYER HAS MONEY + LOCAL-PRESENCE DEFICIT
+
LOCAL PEOPLE HAVE TIME + MOBILITY + BASIC CAPABILITY
+
SEARCH / SCREEN / BRIEF / QA GAP
```

---

# 5. A LIVE buyer task is now bound

A current Upwork listing from **Wine Services**, a Bordeaux market-research agency, requests a Shanghai-based person to visit **21 wine shops**.

Required output:

- visit the 21 stores;
- photograph wine shelves;
- labels must be clearly readable;
- obtain complete inventory where possible.

Payment:

```text
US$25 / complete satisfactory store
US$6 / missed / refused / incomplete store
Maximum stated budget: US$525
```

The rate includes travel.

Source:

- https://www.upwork.com/freelance-jobs/apply/Shanghai-Wine-Shop-Survey_~022100554984121028743/

The client profile shows approximately:
- US$19K historical spend;
- 55 hires;
- 3 active hires.

The listing currently shows:
- 10–15 proposals;
- 0 interviewing.

### Evidence warning

The current page was posted very recently and displays current proposal activity, but it also displays a deadline of **Nov 17, 2025**, which conflicts with the 2026 posting date.

Therefore:

```text
POSTING / BUYER / BUDGET / TASK = BOUND
DEADLINE = UNKNOWN
```

Do not silently “fix” the inconsistent deadline.

---

## 6. Current Shanghai supply

A current Shanghai Fiverr provider publicly offers:

**US$100** for a short offline field task of up to **4 onsite working hours**.

Available services include:
- site inspection;
- photo/video verification;
- simple offline errands;
- Shanghai-wide onsite support.

Source:

- https://www.fiverr.com/menglan9711/be-your-onsite-assistant-runner-and-exhibition-support-in-shanghai

This proves:

```text
SAME-CITY PAID EXECUTION SUPPLY EXISTS
```

but it does **not** prove:

```text
21 WINE SHOPS = US$100
```

The scope is not compatible enough to multiply or extrapolate.

China mystery-shopper/evaluator systems also maintain flexible retail-store executors, but project-specific compensation is not public.

Source:

- https://www.bareinternational.com.cn/evaluators

So the supply network is real, but the exact 21-store execution cost is still unknown.

---

## 7. Why we still cannot claim profit

Current known equation:

```text
Buyer revenue = US$525 max
Compatible full-scope executor cost = UNKNOWN
Operator margin = UNKNOWN
```

It would be fake precision to say:

> “US$525 buyer - US$200 worker = US$325 profit”

because public evidence does not establish that the 21 stores can be completed inside two US$100 four-hour blocks.

Travel route, shop spacing, refusal rate and evidence processing all matter.

That is exactly what the new truth discipline is for.

---

## 8. Adjacent future tasks — useful counterexamples

Fresh upcoming Canton Fair / factory-visit jobs exist.

Examples include:
- a Canton Fair assistant wanted for Oct 17–26 at US$20–45/hour;
- factory-visit / business interpretation work;
- sourcing assistants for October trips.

These prove cross-border local-presence demand is live.

But many require:
- professional interpretation;
- sourcing experience;
- negotiation;
- technical/factory knowledge.

Those are **not** the simple youth-capacity connection we are trying to validate.

A professional interpreter can already sell directly at meaningful day rates.

Therefore the primary search target remains:

> checklist-driven local presence where reliability, coverage and evidence collection matter more than specialist professional judgment.

---

## 9. Portfolio after transaction-unit validation

```text
CSVF-001 = CALIBRATION ONLY
CSVF-002 = KILLED FROM ACTIVE SET
CSVF-003 = PRIMARY TRANSACTION UNIT
```

Formal opportunity promotions:

`0`

External actions:

`0`

`FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN`

---

## 10. Next truth boundary

For the live Shanghai wine-shop task, bind:

```text
one exact / near-exact executor quote
for:
21 Shanghai wine shops
+ shelf photos
+ readable labels
+ inventory where possible
+ travel included / explicitly priced
```

If public evidence cannot produce this quote, stop web extrapolation.

Prepare **one bounded executor quote request** and ask for explicit authorization before contacting a provider.

Only after provider cost is bound may we calculate operator margin.

