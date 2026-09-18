# Opportunity Mobilization Scan 005 — AI-built app production-readiness micro-review

Date: 2026-09-18

## Why this scan exists

Scan 004 closed the generic overseas field-service route because buyer pain was real but the bridge was already materially served.

This scan deliberately looks for a **new reality change** rather than shrinking the same story forever:

> AI agents now let people create working software faster than their ability to judge whether that software is safe and production-ready.

The candidate is not “software consulting”.

It is a possible minimum-service-unit mismatch between:

```text
AI BUILDER WITH A WORKING APP
but insufficient senior engineering judgment
              ↓↓↓

       one bounded review

              ↑↑↑
EXPERIENCED ENGINEER
with spare judgment capacity
```

---

## 1. Demand side — the builder population is now real

Chinese AI-coding communities are no longer only sharing demos.

TRAE's public community contains projects that have actually launched. One public case reports a vibe-coded WeChat mini-program reaching roughly **30,000 registered users** and about 1,000 DAU after a month.

The same community continuously shows:

- solo builders;
- product managers building applications;
- nontraditional developers;
- AI tools moving from prototypes to public release.

At the same time, Chinese engineering guidance repeatedly describes the same boundary:

```text
WORKS
!=
SAFE / MAINTAINABLE / PRODUCTION-READY
```

Academic security work on real vibe-coded applications also reports recurring vulnerability patterns such as secret exposure, unfiltered input and placeholder logic.

This establishes a real **judgment deficit**.

It does not yet establish China willingness-to-pay.

Sources:
- https://forum.trae.cn/t/topic/830
- https://forum.trae.cn/top
- https://forum.trae.cn/c/10-category/25-category/25
- https://arxiv.org/abs/2606.23130
- https://developer.volcengine.com/articles/7541228757999157289

---

## 2. Supply side — senior engineering judgment is callable

Chinese flexible-work infrastructure already exposes a supply pool.

For example, 之马工场 explicitly describes workers who want:

- tasks allocated by a platform;
- no business development;
- no price negotiation;
- work paid by actual time;
- technical work rather than sales.

That is strong supply-side behavior for a task that can be standardized.

The resource is not “someone who can write code”.

It is:

> **someone who has enough production experience to decide what the AI missed.**

Source:
- https://www.zhimawork.com/

---

## 3. Payment evidence exists globally

Human review for AI-built applications is already a paid product abroad.

Examples:

- ProductionReady.co publishes a **USD 1,500–3,000** fixed Vibe Code Audit;
- NexAI Advisors publishes a **USD 500** discovery/review unit and USD 1,500–2,500 production-readiness audit;
- an Upwork product advertises a roughly **USD 250** AI-built-app review;
- other niche providers publish fixed human audits from hundreds to several thousand US dollars.

Typical deliverables are already converging:

```text
repo / app intake
→ security + architecture + deployment review
→ severity-ranked findings
→ prioritized remediation plan
→ short debrief
```

So:

```text
HUMAN JUDGMENT HAS PAYMENT EVIDENCE
```

but:

```text
GLOBAL PAYMENT
!=
CHINA PAYMENT
```

Sources:
- https://productionready.co/vibe-code-audit/
- https://nexaiadvisors.com/services/production-ready-review
- https://www.upwork.com/services/product/development-it-a-full-security-and-code-audit-of-your-ai-built-app-in-3-days-2097337547492979661
- https://axonbuild.com/blog/vibe-coding-security-audit/

---

## 4. Why the service unit may be mismatched in China

At one end:

- a small AI-built application may have only early users or very low revenue;
- the builder may not justify a traditional security consulting project;
- some builders may not even know what kind of specialist they need.

At the other end:

- pure AI self-review is cheap;
- generic freelancer hiring is open-ended;
- formal penetration testing/security certification is too large a unit for many small apps.

The possible gap is therefore:

> **one fixed-scope, independent senior-human review before real exposure.**

Not a rebuild.

Not a month-long consultancy.

Not a compliance certificate.

Not “hire a programmer”.

---

# Narrow missing-edge hypothesis

There may be a China-market gap for:

```text
AUTOMATED EVIDENCE PREWORK
+
ONE BOUNDED SENIOR-HUMAN JUDGMENT UNIT
+
STANDARD REPORT / ACCEPTANCE
```

sitting between AI self-review and expensive consulting/security engagements.

The exact China payer truth is **unproven**.

---

## 5. Rooter execution map

### Demand actor

AI/vibe-coded application owner immediately before:

- public launch;
- real user traffic;
- payment;
- customer handoff;
- sensitive-data use.

### Supply actor

Experienced software/security/architecture engineer with spare review capacity.

### Smallest unit

One bounded repository/application production-readiness review.

### Automated prework

Where possible:

- build/test evidence;
- dependency scan;
- secret scan;
- deployment/config inventory;
- repository map.

### Human executor

A qualified senior reviewer selected by stack/risk.

### Acceptance

A standard report covering:

- authentication/authorization;
- secrets and data;
- API/input risk;
- architecture;
- tests;
- deployment;
- rollback/observability;
- Critical / High / Medium / Low findings;
- remediation priority.

Optional short debrief.

### Money flow

```text
builder
→ orchestration layer
→ reviewer
```

### 根哥's role

- define intake and scope;
- automate evidence gathering;
- create reviewer graph;
- route by stack/risk;
- enforce report schema;
- QA;
- settlement;
- reviewer performance history.

### 根哥 must NOT

- personally review every repository;
- become the implementation developer;
- sell a light review as penetration testing/certification;
- become the required technical expert in every transaction.

### Exit path

```text
standard intake
+
evidence packet
+
reviewer specialization
+
standard acceptance
+
delegated QA
```

---

## 6. Mobilization assessment

Current evidence:

- demand urgency: **2/3**
- supply hunger: **3/3**
- resource abundance: **3/3**
- activation ease: **3/3**
- value capture: **2/3**
- repeatability: **2/3**
- self-propulsion: **1/3**
- operator exit: **3/3**

Under the canonical hard gate the candidate remains:

# **LOW / STRATEGIC WATCH**

Why?

Because `self_propulsion = 1`.

We have not proved that Chinese builders will independently enter this route without founder-by-founder education/sales.

We also have not proved Chinese payer willingness.

---

## 7. Strongest counterevidence

This candidate can still die easily:

1. Claude/Cursor/domestic tools keep improving automatic review.
2. Vibe CSA and similar tools may automate enough of the job.
3. General freelancer platforms can already supply senior developers.
4. Formal security/compliance buyers need specialist firms, not a lightweight reviewer.
5. Global niche audit firms are proliferating quickly.
6. If every customer requires a custom technical scoping call, the route degenerates into consultancy.
7. If the builder will not pay because the app has no economic value yet, there is no market.

---

## 8. Promotion conditions

Do not promote from trend evidence.

Promotion requires:

1. **one named Chinese builder** with a live/near-live AI-built product;
2. a recent real decision such as “about to open to users / enable payment / hand to a client”;
3. its current workaround and the downside it cannot resolve with AI self-review;
4. a bounded paid review unit or another real paid workaround;
5. at least **two independent reviewers** willing to use the same task/report schema;
6. a credible acquisition pump — AI-coding community/tool ecosystem/training cohort/incubator/launch workflow — rather than founder cold sales.

---

# Current state

`OMS-006-AI-BUILT-APP-PRODUCTION-READINESS-MICROREVIEW`

**RETAIN_WATCH / NOT_P0 / BUYER_PAYMENT_AND_DEMAND_PUMP_REQUIRED**

This is more operator-aligned than the closed overseas field-service route because:

- fully digital;
- low permission;
- no field travel;
- highly decomposable;
- acceptance can be standardized;
- supply is abundant;
- recurring technical execution can be delegated.

But operator fit does not create market truth.

# CURRENT BEST NEXT TRUTH

Find one real Chinese AI-app builder exactly at the transition:

```text
DEMO
→
REAL USERS / REAL DATA / REAL MONEY
```

and establish:

> **What do they do today to decide the app is safe enough to ship, what uncertainty remains, and would they pay for one fixed-scope independent human judgment unit?**

In parallel, bind two independent senior reviewers to one common report schema.

Do not build the service first.

Do not personally become the reviewer.

**FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN.**
