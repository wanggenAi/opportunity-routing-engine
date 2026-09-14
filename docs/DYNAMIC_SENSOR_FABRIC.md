# Dynamic Sensor Fabric & China Research Focus

Status: `CANONICAL DISCOVERY INFRASTRUCTURE`

Effective: 2026-09-14

Constitutional parent: `docs/LATENT_VALUE_DOCTRINE.md`.

## 1. Governing principle

The engine must not freeze today's platforms, industries, resource classes, psychology themes or social categories into the ontology.

> **Keep the high-level semantic kernel stable; let lower-level concepts, source surfaces and taxonomies evolve with evidence.**

Today's examples such as Xiaohongshu, Douyin, Weibo, Zhihu, Reddit, X, Instagram, Telegram, job boards, reviews, marketplaces, filings and procurement systems are sensor instances only. They are not architectural boundaries.

## 2. Stable semantic kernel

The stable kernel is intentionally small:

```text
ACTOR
STATE
CHANGE
RESOURCE
CAPABILITY
PERCEPTION
MOTIVE
BEHAVIOR
FLOW
CONSTRAINT
FRICTION
OUTCOME
EVIDENCE
TIME
SPACE
```

`OPPORTUNITY` is downstream inference, not a primitive fact.

A source-specific field, platform category or current trend must map into these primitives rather than expanding the kernel every time the world changes.

## 3. Open concept namespace

Below the kernel, concept labels are open-ended.

Examples such as `SPENDING_CAUTION`, `WAREHOUSE_UNDERUTILIZATION`, `AI_AGENT_PERMISSION_FRICTION` or future concepts that do not exist today are allowed without a core-code enum change.

Known labels are indexes, not discovery boundaries.

```text
OBSERVATION
→ existing concept fits?
  → yes: attach evidence
  → no: RESIDUAL
        → repeated across observations?
        → multiple sources?
        → multiple actors?
        → persists through time?
        → semantically coherent?
        → CANDIDATE CONCEPT
        → promotion review
        → versioned ontology node
```

A new concept may later be merged, split, renamed or deprecated. Historical lineage and supporting observations must remain auditable.

## 4. Unknown is a first-class discovery state

Unclassified observations are not ingestion failures.

`UNKNOWN`, `UNBOUND`, `RESIDUAL` and `NOVEL` states are valuable because new social behavior and new resource forms often appear before the system has language for them.

Never force an unexplained signal into the nearest known taxonomy node merely to improve coverage.

## 5. Dynamic source discovery

The Sensor Fabric itself is dynamic.

A source lifecycle may be:

```text
DISCOVERED
→ QUALIFIED
→ ACTIVE
→ DEGRADED
→ RETIRED
```

A source candidate should be evaluated on observable dimensions such as:
- actor density;
- behavior density;
- commercial/economic signal density;
- geography;
- update frequency;
- provenance quality;
- historical depth;
- access legality/terms;
- schema stability;
- spam/manipulation risk;
- unique signal value relative to existing sources.

A newly important platform should be addable through the source registry/adapters without changing the world model.

## 6. China is the primary research domain

The project's default market-research priority is:

```text
PRIMARY RESEARCH DOMAIN: CHINA
PRIMARY EXECUTION LENS: CHINA → JIANGSU → XUZHOU
SECONDARY OBSERVATION LAYER: GLOBAL INFORMATION
CROSS-BORDER: EXCEPTION ONLY
```

The engine primarily studies:
- Chinese household and consumer psychology;
- Chinese spending and saving behavior;
- employment, income, credit and household balance-sheet changes;
- Chinese enterprise behavior, hiring, pricing, inventory and investment;
- domestic platform/ecosystem changes;
- domestic market structure and money flow;
- resources, underuse and frictions inside China;
- local divergence in Jiangsu and Xuzhou where evidence exists.

Xuzhou is the first field laboratory because reality can be checked locally. It is not the intellectual boundary of the system.

## 7. Global information is an auxiliary sensor, not the primary market

The system may use lawful public/authorized information from anywhere in the world, including foreign social media, forums, company sites, developer communities, product reviews and industry sources.

Global information is useful when it helps explain or challenge a China hypothesis, for example:
- how foreign actors discuss Chinese products, firms or technology;
- a behavior or technology pattern that may later appear in China;
- a failure mode that can be checked before it becomes common domestically;
- a foreign observation that reveals an unexpected use of a Chinese resource;
- a global technology change that changes the value of a domestic resource.

Truth boundaries:

```text
GLOBAL SALIENCE != CHINESE POPULATION PREVALENCE
FOREIGN TREND != CHINESE DEMAND
FOREIGN COMPLAINT != DOMESTIC PAID NEED
GLOBAL SUCCESS STORY != CHINA TRANSFERABILITY
TRANSFER HYPOTHESIS != DOMESTIC FACT
```

A foreign/global signal with China relevance may create a `TRANSFER_HYPOTHESIS`. Domestic corroboration is required before it can materially raise a China opportunity thesis.

## 8. Cross-border is not the default business identity

The system is allowed to discover cross-border opportunities because a broad engine should not discard real value.

However, cross-border routing is an exception path, not the research objective.

A cross-border candidate should enter serious validation only when direct evidence is unusually strong, including a concrete China relation and an executable domestic side. The system must not bias discovery toward exporting Chinese goods/services merely because foreign data is available.

```text
ABILITY TO DISCOVER CROSS-BORDER VALUE
!=
CROSS-BORDER-FIRST STRATEGY
```

## 9. Psychology and social sensing

The system studies aggregate changes in Chinese consumer/actor decision logic. `PERCEPTION` and `MOTIVE` are stable semantic primitives; individual psychology-theme names are dynamic concepts.

Platforms are observation surfaces only.

Domestic social sources are useful for early signal detection but must be corroborated with behavior and money where possible. Foreign social sources may inform China-related hypotheses but cannot establish what Chinese consumers believe or how common a motive is inside China.

Do not build unnecessary user-level psychographic profiles or infer protected/sensitive traits.

## 10. Source geography is not target geography

Each observation must keep at least:

```text
source / origin geography
observed actor geography where known
target/relevance geography if hypothesized
evidence for the relationship
```

A US Reddit post about a Chinese product is not a Chinese consumer observation. It may still be relevant evidence about how an external actor perceives a Chinese resource.

## 11. Regenerative patterns outrank one-off events

A one-off event may be a useful sensor or route test, but core discovery should search for recurring structures:

```text
repeated actor state change
+ repeated behavior
+ persistent friction / underuse
+ reusable transformation mechanism
+ recurring or regenerating value flow
```

A failed tender, isolated order or single viral complaint is an observation. It becomes strategically important only when it contributes to a repeatable pattern or a strongly evidenced exceptional transaction.

## 12. Engineering contracts

The initial code contracts are:
- `src/semantic_kernel.py` — stable primitives + open concept namespace;
- `src/emergent_taxonomy.py` — evidence-gated residual/candidate review readiness;
- `src/geographic_focus.py` — China-primary / global-auxiliary / cross-border-exception policy.

These contracts are deliberately source-agnostic.

They do not automatically promote business truth. Need, payer, resource, underuse, blocker, callability and transaction gates remain downstream and fail-closed.

## 13. Governing invariant

> **不要把今天看到的世界写死进代码。把理解世界的方法写进代码：全球都可以成为传感器，但主要研究中国社会、中国消费者、中国企业和中国资源；江苏、徐州是第一现实验证坐标。平台、分类和热点可以不断变化，高层语义、证据边界和事实晋级规则保持稳定。**
