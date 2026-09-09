# Consumer Psychology & Behavior Tracker

Status: `CANONICAL DISCOVERY MODULE`

Effective: 2026-09-10

This module is part of `docs/DISCOVERY_ENGINE.md`.

Its job is not to decide what "Chinese people think" from viral posts. Its job is to continuously detect **directional changes in consumer decision logic** and connect those changes to observable behavior and money flow.

## 1. Core question

> Which decision logics are becoming more or less salient for a defined actor segment, and are those psychological signals corroborated by actual spending, search, booking, hiring, transaction or workaround behavior?

The tracker is a **hypothesis sensor**, not a commercial truth engine.

## 2. Why this must be tracked over time

Consumer psychology is neither perfectly stable nor random.

Some regimes persist for months or years:
- income/security caution;
- preference for value-for-money;
- delayed large purchases;
- risk aversion;
- preference for small commitments.

Other signals move faster:
- event-driven emotional consumption;
- travel/experience demand;
- platform-specific fads;
- seasonal health/fitness concerns;
- new technology anxiety or excitement;
- local-event-driven consumption.

Therefore store **time series**, not one-off conclusions.

## 3. Do not report fake population shares

Social platforms are not representative probability samples.

Do not claim:

> `37% of Xuzhou youth are cautious consumers`

from social-content counts.

Use separate concepts:

### `SIGNAL_SALIENCE`
How strongly a theme appears within the observed source universe.

### `MOMENTUM`
How quickly that signal is rising/falling versus its own historical baseline.

### `BEHAVIOR_CORROBORATION`
Whether actors are doing something consistent with the signal.

### `MONEY_CORROBORATION`
Whether spending / orders / prices / paid services / budgets move consistently with it.

### `REPRESENTATIVE_SHARE`
Allowed only when a source is a defensible survey/statistical sample with an explicit denominator/methodology.

## 4. Geographic hierarchy

Track at multiple levels:

```text
CHINA
  ↓
JIANGSU
  ↓
XUZHOU
  ↓
DISTRICT / COMMERCIAL CLUSTER where evidence exists
```

Never infer Xuzhou psychology from national social content alone.

Local signals may be sparse; uncertainty must remain visible.

## 5. Actor-segment hierarchy

Examples:
- 18–24 students / early graduates;
- 25–34 young workers;
- young families;
- parents with school-age children;
- middle-income households;
- price-sensitive households;
- 50–59 pre-senior group;
- 60+ elderly;
- adult children paying for parents;
- pet owners;
- county / rural consumers;
- merchants / self-employed operators;
- SME decision-makers.

Do not infer protected or sensitive traits from individual users.

## 6. Canonical psychology dimensions

Initial taxonomy:

1. `SPENDING_CAUTION`
   - fear of future income uncertainty;
   - reduced discretionary commitment;
   - stronger savings / delay behavior.

2. `VALUE_FOR_MONEY`
   - active price comparison;
   - discount/substitute seeking;
   - value optimization rather than pure cheapness.

3. `SMALL_TRIAL_PREFERENCE`
   - small-ticket / short-cycle / reversible commitment preferred over large commitment.

4. `EXPERIENCE_ORIENTATION`
   - service, travel, sports, culture, learning, events or experiential consumption preferred over more goods.

5. `EMOTIONAL_VALUE / SELF_REWARD`
   - spending for mood, identity, novelty, aesthetics, ceremony or self-reward.

6. `CONVENIENCE / TIME_VALUE`
   - willingness to pay to save coordination, waiting, travel or cognitive load.

7. `TRUST / RISK_AVERSION`
   - stronger need for verification, accountability, known brands/providers, guarantees and visible proof.

8. `QUALITY_UPGRADE_SELECTIVITY`
   - overall caution coexisting with premium spend in selected categories where quality or utility is strongly perceived.

9. `HEALTH / LONGEVITY`
   - health management, recovery, preventive care, fitness, age-friendly services or long-term wellbeing.

10. `SOCIAL_CONNECTION / BELONGING`
   - spending or participation motivated by community, shared identity, offline connection or group belonging.

11. `REPAIR_REUSE_RENT`
   - repair, second-hand, rental, sharing, maintenance and longer asset life instead of replacement.

12. `OUTCOME_CERTAINTY`
   - willingness to pay for guaranteed/verified results rather than information or uncertain effort.

Taxonomy may evolve only when evidence shows persistent unmapped behavior.

## 7. Source classes

### Tier A — hard money / behavior
Highest commercial relevance:
- official retail/service statistics;
- transaction / booking / payment aggregates;
- procurement / tender / order data;
- platform transaction aggregates;
- prices and paid service volumes;
- hiring / outsourcing spend;
- repair / resale / rental transactions;
- footfall linked to spend where credible.

### Tier B — representative / structured research
- official household surveys;
- industry surveys with disclosed methodology;
- credible consumer panels;
- structured local surveys.

### Tier C — search / platform trends
- search trend indexes;
- platform trend lists;
- topic growth;
- public aggregate engagement.

### Tier D — social / media language
- public posts;
- comments where legally/technically permitted;
- news narratives;
- creator discourse;
- forum discussions.

Tier D is valuable for early change detection but cannot independently prove population prevalence or willingness to pay.

## 8. Platform collection policy

Prefer:
1. official/open APIs;
2. platform-authorized tools/exports;
3. public search/index results;
4. public pages where automated access is allowed and rate-limited;
5. manually sampled public material when automation is not permitted.

Do not:
- bypass login/access controls;
- defeat CAPTCHAs or anti-bot measures;
- impersonate users;
- collect private messages;
- build user-level psychological profiles;
- retain unnecessary handles, phone numbers, IDs or sensitive personal data;
- exceed reasonable automated-access load;
- infer sensitive traits from individuals.

Store aggregate/anonymized signal records whenever possible.

## 9. Signal record schema

```text
signal_id:
observed_at:
source_date:
source_type:
source_name:
source_url_or_ref:
geography:
actor_segment:
psychology_dimension:
direction: -1.0 .. +1.0
intensity: 0.0 .. 1.0
behavior_corroboration: 0.0 .. 1.0
money_corroboration: 0.0 .. 1.0
representative_sample: YES / NO
representative_share: optional
sample_size: optional
provenance_quality: LOW / MEDIUM / HIGH
notes:
```

Direction expresses movement in the named dimension, not positive/negative emotion.

Example:
`SPENDING_CAUTION direction=+0.8` means caution is increasing.

## 10. Time windows

Maintain at minimum:
- 7-day fast signal;
- 30-day tactical signal;
- 90-day regime signal;
- 365-day structural context.

Fast social spikes should decay quickly unless behavior/money data confirms them.

## 11. Inference outputs

For each `geography × actor_segment × psychology_dimension × window` output:

```text
salience_index: -100 .. +100
momentum: falling / stable / rising / accelerating
confidence: LOW / MEDIUM / HIGH
evidence_diversity:
behavior_corroboration:
money_corroboration:
representative_share: optional only when valid
key_supporting_signals:
key_contradictions:
last_updated:
```

## 12. Confidence rule

`HIGH` confidence should generally require multiple source classes and at least one behavior/money source.

Social-content volume alone cannot produce `HIGH` confidence.

Contradictory hard evidence must reduce confidence even when social salience is high.

## 13. Opportunity bridge

The tracker must not emit a startup idea directly.

It emits **discovery hypotheses** such as:

```text
Xuzhou 25–34 young workers
+ VALUE_FOR_MONEY rising
+ EXPERIENCE_ORIENTATION stable/rising
+ large-ticket goods weak
+ service/event spend resilient
→ investigate low-commitment high-experience services
```

Then the Discovery Engine asks:
- where is money actually moving?
- what specific friction remains?
- who pays?
- what current workaround exists?

Only after this does the Orchestration Engine ask:
- what capability units are required?
- can acquisition/delivery be delegated?
- what is the acceptance/settlement structure?

## 14. Anti-confirmation-bias rule

For every promoted psychology thesis actively search for:
- contradictory spend categories;
- opposing actor segments;
- local divergence from national data;
- policy/subsidy contamination;
- algorithmic/platform trend distortion;
- seasonal/event effects.

The tracker should preserve disagreement rather than average it away.

## 15. 2026 baseline example — not a permanent conclusion

Current public data illustrates why the tracker is necessary:
- national goods retail growth is relatively weak while service retail is materially faster;
- Jiangsu goods/retail growth is modest while production/business services are stronger;
- Xuzhou reported faster retail growth than the Jiangsu aggregate and strong online retail growth;
- selected upgrade categories can grow strongly even during broad caution.

This is consistent with a **selective / structural migration** interpretation rather than a simplistic `people stopped spending` thesis.

The tracker must update this view as new data arrives.

## 16. Engineering boundary

The first engineering target is **normalization + aggregation + time-series inference**, not aggressive web crawling.

Source adapters should be added one by one only when:
- access is lawful/permitted;
- provenance can be retained;
- the source adds unique signal value;
- collection cost/reliability is acceptable.

## 17. Governing invariant

> **Psychology tells us why behavior may be changing. Behavior and money tell us whether the psychology matters economically.**
