# Consumer Psychology & Behavior Tracker

Status: `CANONICAL DISCOVERY MODULE`

Effective: 2026-09-14

Parents:
- `docs/DISCOVERY_ENGINE.md`
- `docs/DYNAMIC_SENSOR_FABRIC.md`

Its job is not to decide what "Chinese people think" from viral posts. Its job is to continuously detect **directional changes in Chinese consumer/actor decision logic** and connect those changes to observable behavior and money flow.

## 1. Research focus

Default target domain:

```text
PRIMARY: Chinese consumers / households / workers / owners / enterprises
LOCAL LENS: China → Jiangsu → Xuzhou
AUXILIARY OBSERVATION: global public information
```

Foreign/global social information may help explain China, reveal possible lead/lag patterns, expose failure modes, or show external perception/use of Chinese resources. It does not establish Chinese consumer psychology by itself.

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

## 3. Residual / novelty rule

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

## 4. Core question

> Which perceptions and motives are becoming more or less salient for a defined Chinese actor segment, what behavior follows, and are those psychological signals corroborated by actual spending, search, booking, hiring, transaction, saving, substitution or workaround behavior?

The tracker is a **hypothesis sensor**, not a commercial truth engine.

## 5. Do not report fake population shares

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

## 6. Geography and transfer

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

## 7. Global social layer

Lawful public/authorized sources may include current or future global communities, social platforms, forums, product-review sites, developer communities and video/comment ecosystems.

Current examples such as Reddit, X, Instagram or Telegram are source instances only.

Useful China-related questions include:
- how foreign actors perceive or use Chinese products/resources;
- whether a technology/behavior pattern abroad may have a plausible China mechanism;
- what failure modes appeared abroad before domestic adoption matured;
- whether global technology changes alter the value of a Chinese/Jiangsu/Xuzhou resource.

The tracker must not turn this into an export-first strategy or infer Chinese consumer motives from foreign users.

## 8. Domestic source classes

### Tier A — hard money / behavior
Official retail/service statistics, transaction/booking/payment aggregates, prices, paid volumes, hiring/outsourcing spend, resale/rental/repair transactions and other direct behavior evidence.

### Tier B — representative / structured research
Official household surveys, disclosed-method industry surveys, consumer panels and structured local surveys.

### Tier C — search / platform trends
Search trends, public aggregate engagement, public trend lists and topic growth.

### Tier D — social / media language
Public posts/comments where permitted, creator discourse, forums, video comments and news narratives.

Tier D is valuable for early detection but cannot independently prove prevalence or willingness to pay.

## 9. Platform collection policy

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
- infer sensitive traits from individuals.

Store aggregate/anonymized signal records whenever possible.

## 10. Signal record schema

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
direction: optional
intensity: optional
behavior_corroboration:
money_corroboration:
representative_sample: YES / NO
representative_share: optional
sample_size: optional
provenance_quality:
key_evidence_refs:
contradictions:
notes:
```

Unknown concept is allowed. `concept` is an open namespace.

## 11. Time windows

Maintain where practical:
- 7-day fast signal;
- 30-day tactical signal;
- 90-day regime signal;
- 365-day structural context.

Fast social spikes should decay quickly unless behavior/money data confirms them.

## 12. Confidence rule

`HIGH` confidence should generally require multiple source classes and at least one behavior/money source.

Social-content volume alone cannot produce `HIGH` confidence.

Contradictory hard evidence must reduce confidence even when social salience is high.

## 13. Opportunity bridge

The tracker must not emit a startup idea directly.

It emits evidence-bound hypotheses such as:

```text
Chinese actor segment
+ perception/motive change
+ observed behavior change
+ money corroboration
→ investigate the resulting state/friction/resource change
```

Then the Discovery Engine asks:
- what structural state changed?
- where is money actually moving?
- what friction or underuse persists?
- what hidden resource or deficit may exist?
- is there a recurring pattern rather than a one-off event?

Only downstream evidence gates decide need, payer, resource, blocker and route testability.

## 14. Anti-confirmation-bias rule

For every promoted psychology thesis actively search for:
- contradictory spend/saving behavior;
- opposing actor segments;
- local divergence from national evidence;
- foreign patterns that fail to transfer to China;
- policy/subsidy contamination;
- platform algorithm distortion;
- bots/coordinated manipulation;
- seasonal/event effects.

Preserve disagreement rather than averaging it away.

## 15. Engineering boundary

The engineering target is **normalization + provenance + time series + residual detection + corroboration**, not scraper breadth for its own sake.

Source adapters should be added when access is lawful/permitted, provenance can be retained, the source adds unique signal value, and collection reliability is acceptable.

Platform additions must not require changes to semantic primitives.

## 16. Governing invariant

> **主要研究中国人的认知、动机、行为和真实钱流；全球社交与互联网信息只是增加观察半径。心理主题不是写死的枚举，无法解释的新行为应进入 residual pool，让 taxonomy 随证据生长。Psychology explains possible reasons; behavior and money decide whether those reasons matter economically.**
