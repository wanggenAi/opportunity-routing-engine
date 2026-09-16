# Psychology & Behavior Engineering

Status: `CANONICAL VALUE-FORMATION SENSOR`

Effective: 2026-09-16

Parents:
- `docs/LATENT_VALUE_DOCTRINE.md`
- `docs/LATENT_VALUE_FORMATION_BRIDGE.md`
- `docs/DISCOVERY_ENGINE.md`
- `docs/DYNAMIC_SENSOR_FABRIC.md`

Its job is not to decide what "Chinese people think" from viral posts, and not merely to mine complaints or explicit purchase wishes. Its deeper job is to continuously detect **changes in actor decision logic** and connect them to objective endowments, state transitions, observed behavior and economic reality so the system can reason about value structures that may not yet exist.

## 1. Research focus

Default target domain:

```text
PRIMARY: Chinese consumers / households / workers / owners / enterprises
LOCAL LENS: China → Jiangsu → Xuzhou
AUXILIARY OBSERVATION: global public information
```

Foreign/global social information may help explain China, reveal possible lead/lag patterns, expose failure modes, or show external perception/use of Chinese resources. It does not establish Chinese psychology by itself.

## 2. Stable model, dynamic concepts

`PERCEPTION`, `MOTIVE` and `BEHAVIOR` are stable semantic primitives.

Named psychology themes are **not a closed canonical enum**. They are versioned concepts in the emergent taxonomy.

Seed concepts useful in 2026 include:
- `SPENDING_CAUTION`;
- `VALUE_FOR_MONEY`;
- `SMALL_TRIAL_PREFERENCE`;
- `EXPERIENCE_ORIENTATION`;
- `EMOTIONAL_VALUE` / `SELF_REWARD`;
- `CONVENIENCE_TIME_VALUE`;
- `TRUST_RISK_AVERSION`;
- `QUALITY_UPGRADE_SELECTIVITY`;
- `HEALTH_LONGEVITY`;
- `SOCIAL_CONNECTION_BELONGING`;
- `REPAIR_REUSE_RENT`;
- `OUTCOME_CERTAINTY`.

These are **seed taxonomy nodes**, not discovery boundaries. New persistent behavior may create a new candidate concept without changing core code. Old concepts may be merged, split, renamed or deprecated with lineage preserved.

## 3. The real causal question

The tracker should not begin with:

> What are people complaining about and what can we sell them?

It should reconstruct, where evidence allows:

```text
WHO IS THIS ACTOR / SEGMENT?
↓
WHAT OBJECTIVE ENDOWMENTS ALREADY EXIST?
↓
WHAT STATE IS THE ACTOR IN?
↓
WHAT CHANGED RECENTLY?
↓
HOW DOES THE ACTOR PERCEIVE THAT CHANGE?
↓
WHAT MOTIVES / FEARS / ASPIRATIONS BECOME SALIENT?
↓
WHAT BEHAVIORS FOLLOW?
↓
WHAT CONTRADICTIONS APPEAR BETWEEN RESOURCES, MOTIVES AND ACTUAL USE?
↓
WHAT RESOURCE–PSYCHOLOGY DISEQUILIBRIUM MAY EXIST?
↓
WHAT UNMET / UNFORMED OUTCOME MAY THE ACTOR BE MOVING TOWARD?
```

Psychology is therefore a **causal discovery input to Latent Value Formation**, not a decorative trend layer.

## 4. Resource–Psychology Disequilibrium

The tracker should help identify cases where objective resources and subjective/behavioral state no longer fit each other.

Illustrative patterns:

```text
MONEY ↑ / TIME ↑
BUT TRUSTED WAYS TO USE THEM FOR A NEW LIFE STATE ↓
```

```text
EXPERIENCE ↑
BUT CALLABLE ROLE / ORGANIZATIONAL IDENTITY ↓
```

```text
DIGITAL CAPABILITY ↑ / TIME ↑
BUT CLIENT ACCESS / TRUST / INDUSTRY CONTEXT ↓
```

```text
CUSTOMER OR ATTENTION ACCESS EXISTS
BUT EXECUTION / PRODUCTIZATION CAPABILITY IS WEAK
```

```text
SPACE / EQUIPMENT / DATA EXISTS
BUT THE OLD USE CASE NO LONGER FITS CURRENT BEHAVIOR
```

These are not products or demand statements. They are search zones for a possible `RESOURCE_PSYCHOLOGY_DISEQUILIBRIUM_HYPOTHESIS`.

## 5. Contradiction is first-class signal

The engine should actively preserve contradictions such as:
- more free time but less daily structure;
- deep expertise but fewer occasions to contribute;
- more money but stronger fear of being cheated;
- desire to keep up with technology but avoidance of complex tools;
- high digital execution capacity but weak trust and income access;
- abundant options but decision paralysis;
- stated preference that conflicts with observed spending or behavior.

A contradiction may indicate:
1. a valuable state transition not yet served;
2. a resource whose use case has changed;
3. a hidden blocker;
4. a false psychology thesis.

The system must not force contradictions into one average sentiment score.

## 6. Residual / novelty rule

If observed behavior cannot be explained well by existing concepts, retain it as `RESIDUAL` / `UNBOUND` instead of forcing it into the nearest label.

Promotion path:

```text
UNMAPPED OBSERVATIONS
→ repeated pattern
→ multi-source evidence
→ multi-actor evidence
→ time persistence
→ candidate concept
→ review / contradiction search
→ versioned taxonomy promotion
```

Viral volume from one platform is insufficient for promotion.

## 7. Core question

> Which perceptions and motives are becoming more or less salient for a defined actor segment, what objective state change preceded them, what behavior follows, what contradictions remain, and do those signals imply a falsifiable change in how existing resources may be valued or used?

The tracker is a **formation-hypothesis sensor**, not a commercial truth engine.

## 8. Do not report fake population shares

Social platforms are not representative probability samples.

Keep separate:

### `SIGNAL_SALIENCE`
How strongly a concept appears within the observed source universe.

### `MOMENTUM`
How quickly that signal changes versus its own historical baseline.

### `BEHAVIOR_CORROBORATION`
Whether actors do something consistent with the signal.

### `MONEY_CORROBORATION`
Whether spending, orders, prices, savings, subscriptions, bookings or paid services move consistently with it.

### `REPRESENTATIVE_SHARE`
Allowed only when a defensible survey/statistical sample has an explicit denominator and methodology.

```text
SOCIAL SALIENCE != POPULATION SHARE
GLOBAL SALIENCE != CHINESE PREVALENCE
```

## 9. Geography and transfer

Domestic evidence should be tracked at the most specific supported level:

```text
CHINA
  ↓
JIANGSU
  ↓
XUZHOU
  ↓
DISTRICT / COMMERCIAL CLUSTER where evidence exists
```

Never infer Xuzhou psychology from national content alone.

Foreign/global observations require separate source geography and China-relevance evidence.

A foreign pattern may create:

```text
TRANSFER_HYPOTHESIS
```

but material promotion requires domestic corroboration.

## 10. Global social layer

Lawful public/authorized sources may include current or future global communities, social platforms, forums, product-review sites, developer communities and video/comment ecosystems.

Current examples such as Reddit, X, Instagram or Telegram are source instances only.

Useful China-related questions include:
- how foreign actors perceive or use Chinese products/resources;
- whether a technology/behavior pattern abroad may have a plausible China mechanism;
- what failure modes appeared abroad before domestic adoption matured;
- whether global technology changes alter the value of a Chinese/Jiangsu/Xuzhou resource.

The tracker must not turn this into an export-first strategy or infer Chinese motives from foreign users.

## 11. Domestic source classes

### Tier A — hard money / behavior
Official retail/service statistics, transaction/booking/payment aggregates, prices, paid volumes, hiring/outsourcing spend, resale/rental/repair transactions and other direct behavior evidence.

### Tier B — representative / structured research
Official household surveys, disclosed-method industry surveys, consumer panels and structured local surveys.

### Tier C — search / platform trends
Search trends, public aggregate engagement, public trend lists and topic growth.

### Tier D — social / media language
Public posts/comments where permitted, creator discourse, forums, video comments and news narratives.

Tier D is especially useful for early observation of state, language, motive, workaround and contradiction. It cannot independently prove prevalence, underuse, willingness to pay or commercial value.

## 12. Platform collection policy

Prefer:
1. official/open APIs;
2. platform-authorized tools/exports;
3. public search/index results;
4. public pages where automated access is allowed and rate-limited;
5. documented manual sampling when automation is not permitted.

Do not:
- bypass login/access controls;
- defeat CAPTCHAs or anti-bot measures;
- impersonate users;
- collect private messages;
- build unnecessary user-level psychographic profiles;
- retain unnecessary handles, IDs, phone numbers or sensitive personal data;
- infer sensitive traits from individuals;
- use hidden psychological manipulation to make a formation hypothesis become true.

Store aggregate/anonymized signal records whenever possible.

## 13. Signal record schema

```text
signal_id:
observed_at:
source_date:
source_id:
source_type:
origin_geography:
relevance_geography:
actor_segment:
semantic_primitive: PERCEPTION / MOTIVE / BEHAVIOR
concept:
taxonomy_version:
state_context: optional
state_change_context: optional
objective_endowment_refs: optional
direction: optional
intensity: optional
behavior_corroboration:
money_corroboration:
contradictions: optional
resource_psychology_disequilibrium_ref: optional
representative_sample: YES / NO
representative_share: optional
sample_size: optional
provenance_quality:
key_evidence_refs:
notes:
```

Unknown concept is allowed. `concept` is an open namespace.

The psychology record may reference objective evidence, but it may not manufacture it.

## 14. Time windows

Maintain where practical:
- 7-day fast signal;
- 30-day tactical signal;
- 90-day regime signal;
- 365-day structural context.

Fast social spikes should decay quickly unless behavior/money data confirms them.

## 15. Confidence rule

`HIGH` confidence should generally require multiple source classes and at least one behavior/money source.

Social-content volume alone cannot produce `HIGH` confidence.

Contradictory hard evidence must reduce confidence even when social salience is high.

## 16. Formation bridge

The tracker must not emit a startup idea directly.

It emits evidence-bound ingredients for value formation:

```text
ACTOR SEGMENT
+
OBJECTIVE STATE / STATE CHANGE
+
PERCEPTION / MOTIVE CHANGE
+
OBSERVED BEHAVIOR
+
CONTRADICTION
→ investigate RESOURCE–PSYCHOLOGY DISEQUILIBRIUM
→ infer UNMET / UNFORMED OUTCOME HYPOTHESIS
→ search COMPLEMENTARY WORLD NODES
→ design COUNTERFACTUAL EXCHANGE
→ run CHEAP VALIDATION
```

Only later should strict transaction evidence be projected into:
- NeedSignal;
- ResourceSignal;
- BlockerSignal;
- payer;
- payment evidence;
- resource control/availability.

```text
PSYCHOLOGY HYPOTHESIS != DEMAND
UNFORMED OUTCOME != DEMAND
DEMAND != WILLINGNESS TO PAY
WILLINGNESS TO PAY != TRANSACTION
```

## 17. Social language as state evidence, not purchase intent

Public language can be useful when it reveals statements such as:
- a changed daily structure;
- a newly available resource;
- a lost role or channel;
- fear, aspiration or avoidance;
- a repeated workaround;
- a conflict between capability and available opportunity;
- a new adaptation behavior.

A single sentence is not an individual psychological diagnosis and not a commercial lead by default.

The engine should aggregate recurring structures across time, actors and source classes, then test whether the implied disequilibrium is real.

## 18. Anti-confirmation-bias rule

For every promoted psychology or formation thesis actively search for:
- contradictory spend/saving behavior;
- opposing actor segments;
- local divergence from national evidence;
- foreign patterns that fail to transfer to China;
- policy/subsidy contamination;
- platform algorithm distortion;
- bots/coordinated manipulation;
- seasonal/event effects;
- evidence that the resource is not actually underused;
- evidence that the supposed outcome is already solved cheaply;
- evidence that behavior is expressive rather than action-oriented.

Preserve disagreement rather than averaging it away.

## 19. Engineering boundary

The engineering target is **normalization + provenance + time series + state linkage + residual detection + contradiction preservation + corroboration**, not scraper breadth for its own sake.

Source adapters should be added when access is lawful/permitted, provenance can be retained, the source adds unique signal value, and collection reliability is acceptable.

Platform additions must not require changes to semantic primitives.

Do not build a giant social scraper before the value-formation contract can use the observations it already has.

## 20. Governing invariant

> **心理行为工程不是“看看大家抱怨什么、想买什么”。它要观察 Actor 在什么状态、拥有什么、发生了什么变化、如何感受变化、产生了什么动机、真实行为怎样偏移，以及资源与心理/行为之间出现了什么矛盾。平台只是传感器。真正要寻找的是 Resource–Psychology Disequilibrium 和尚未成形的 outcome，再把它交给互补节点搜索与 Counterfactual Exchange Design。心理解释可能的方向，行为与钱帮助判断它是否真实；任何心理信号都不能直接升级成需求。**
