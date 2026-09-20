# Internet Research Control Plane

Status: `CANONICAL DISCOVERY INFRASTRUCTURE`

Effective: 2026-09-14

Parents:
- `docs/LATENT_VALUE_DOCTRINE.md`
- `docs/DISCOVERY_ENGINE.md`
- `docs/DYNAMIC_SENSOR_FABRIC.md`
- `docs/PSYCHOLOGY_BEHAVIOR_TRACKER.md`

## 1. Purpose

The engine must use the internet as a broad, evolving observation surface without confusing search capability with commercial truth.

The control plane exists to answer:

```text
WHY are we researching?
WHAT part of reality are we trying to observe?
HOW broad should the search expand?
WHICH geographies and source families are under-covered?
HOW much evidence diversity is enough for broad discovery context?
WHEN should an agent stop searching?
WHAT must remain UNKNOWN even after large-scale search?
```

It does **not** decide whether a business opportunity is real.

## 2. Current Pattern outputs are calibration, not business directions

The current small set of `OBSERVED_PATTERN` outputs proves that:
- real heterogeneous observations can enter one Fabric;
- recurring structures can be detected without using history revisions as fake events;
- `INFERRED` claims do not self-promote;
- Pattern does not silently become opportunity/archetype/business truth.

That makes the current outputs useful **calibration / regression cases**.

Until a broad research mission passes coverage audit, they must not be presented as representative market discovery or as the system's chosen business directions.

```text
REAL SOURCE OBSERVATION
!=
BROAD MARKET COVERAGE

OBSERVED_PATTERN
!=
SELECTED BUSINESS
```

## 3. Control plane and executor are separate

The Research Control Plane is stable orchestration logic.

Executors are replaceable capabilities, for example:
- interactive ChatGPT/Web research;
- browser/computer-use research;
- search-engine/API connectors;
- direct official/public source adapters;
- platform-authorized APIs/exports;
- documented manual sampling.

```text
RESEARCH MISSION
→ QUERY / SOURCE EXPANSION PLAN
→ REPLACEABLE RESEARCH EXECUTOR(S)
→ PROVENANCE-BEARING EVIDENCE
→ ObservationEnvelope
→ Coverage Audit
→ Pattern / Novelty / Hypothesis layers
```

Changing the executor must not require changing the world model.

## 4. China-first, global-information-rich

Default mission orientation:

```text
PRIMARY RESEARCH: CHINA
LOCAL ZOOM: CHINA → JIANGSU → XUZHOU
GLOBAL INFORMATION: AUXILIARY RESEARCH LANE
CROSS-BORDER: EXCEPTION ONLY
```

Global sources are deliberately included because they can reveal:
- external perception/use of Chinese resources;
- lead/lag behavior patterns;
- technology changes that reprice Chinese resources;
- failure modes that may later appear domestically;
- unexpected China-related observations invisible on domestic platforms.

But:

```text
FOREIGN TREND != CHINESE DEMAND
GLOBAL SALIENCE != CHINESE PREVALENCE
GLOBAL SOURCE COVERAGE != DOMESTIC CORROBORATION
```

## 4A. Attraction-first attention mode

The active commercial-discovery mission uses `attention_mode = ATTRACTION_FIRST`.

This changes **what broad research looks for first**, not what counts as truth.

The executor should preferentially harvest evidence of:
- A-side voluntary motion;
- B-side voluntary motion;
- sharp state-dependent value differences;
- still-open budget/vendor/access/resource decisions;
- narrow bridges that could unlock disproportionate value;
- bounded activation/explanation burden;
- self-propulsion after successful routing;
- operator control without recurring founder delivery.

The production mission is:

`data/research_missions/attraction_field_broad_reality.json`

and the production planning workflow must point to that file.

```text
ATTRACTION FIRST FOR ATTENTION
EVIDENCE FIRST FOR TRUTH
```

This is not permission to optimize search for novelty or hype. Every attraction
signal still requires provenance-bearing observations and later causal/structural
verification.

## 5. Research lanes

The first control-plane version uses six **research-control lanes**, not world-taxonomy categories:

- `CHINA_CORE` — broad Chinese reality;
- `JIANGSU_ZOOM` — provincial divergence/structure;
- `XUZHOU_ZOOM` — locally verifiable reality;
- `GLOBAL_AUXILIARY` — global information relevant to China;
- `CONTRADICTION_SEARCH` — deliberate counterevidence search;
- `SOURCE_DISCOVERY` — discover new lawful/authorized observation surfaces.

These lanes control search coverage. They do not define industries, consumer psychologies or opportunity categories.

## 6. Dynamic query expansion

Bootstrap seed queries are allowed, but they are not permanent discovery boundaries.

New search terms should also come from:
- residual/unbound concepts;
- novelty clusters;
- newly observed changes;
- macro/local divergences;
- unresolved Pattern gaps;
- new technology vocabulary;
- new actor vocabulary;
- newly discovered source surfaces;
- contradictions and failed hypotheses.

Therefore:

```text
TODAY'S QUERY LIST != TOMORROW'S WORLD MODEL
```

A dynamic term may be researched immediately without adding a core enum.

## 7. Coverage budget

Each mission has explicit budgets such as:
- total queries;
- results per query;
- results per host;
- lane allocation;
- minimum independent hosts;
- minimum source-family diversity;
- maximum single-host concentration;
- maximum global-auxiliary share;
- freshness horizon.

The purpose is not to artificially limit research. It is to make breadth, cost and stopping conditions observable and controllable.

A larger mission can raise these budgets without changing ontology.

## 8. Coverage states

### `CALIBRATION_ONLY`
A mission exists but broad evidence coverage has not been executed.

Use for:
- framework tests;
- regression cases;
- adapter validation;
- local pilot observations.

Do not present its Pattern outputs as broad market discovery.

### `PARTIAL_DISCOVERY`
Real research evidence exists, but coverage is concentrated or missing required lanes/source diversity.

Useful for hypothesis generation, not broad-market claims.

### `BROAD_DISCOVERY_READY`
The configured coverage gate has been satisfied across independent hosts, source families and research lanes.

This state means only:

> The engine has a sufficiently broad research context for this mission.

It does **not** mean any business is proven.

```text
BROAD_DISCOVERY_READY != OPPORTUNITY_CONFIRMED
```

## 9. Source expansion

The system should continuously discover new sources rather than freeze today's platforms.

A new source may be discovered through:
- search results;
- citations/links from trusted sources;
- newly important communities/platforms;
- API/documentation discovery;
- actor behavior changes;
- new public datasets;
- new technical modalities.

Discovery produces a `SensorCandidate` only.

Activation still requires source-specific qualification, permission/access review and provenance rules.

## 10. Research executor contract

Any executor must obey:

```text
PUBLIC_OR_AUTHORIZED_ONLY
NO LOGIN/ACCESS-CONTROL BYPASS
NO CAPTCHA/ANTI-BOT BYPASS
NO PRIVATE-MESSAGE COLLECTION
NO SOURCE DISCOVERY → SILENT ACTIVATION
NO SEARCH RESULT → BUSINESS TRUTH
NO FOREIGN SIGNAL → DOMESTIC FACT
NO SOCIAL SALIENCE → POPULATION SHARE
```

Every accepted result must retain enough provenance to become an auditable ObservationEnvelope.

## 11. Contradiction search is mandatory

A broad internet search engine can easily become a confirmation engine.

For that reason the control plane reserves explicit research budget for:
- opposing evidence;
- falling/failed trends;
- incumbent solutions;
- free substitutes;
- regulatory blockers;
- evidence that the apparent pattern is source/platform selection bias.

The system should become harder to fool as internet coverage expands, not easier.

## 12. Internet breadth and source legality are separate axes

The engine should expand observation breadth aggressively while remaining conservative about automated access.

A source can remain useful in `PUBLIC_MANUAL` or interactive research mode even when an automated API is paid, gated or unavailable.

Conversely, an easy API is not automatically valuable.

```text
EASY ACCESS != HIGH SIGNAL VALUE
HARD AUTOMATION != USELESS SOURCE
```

## 13. Production contract

Initial implementation:
- `src/research_control_plane.py` — mission, query expansion, evidence coverage audit;
- `data/research_missions/attraction_field_broad_reality.json` — active attraction-first broad-reality mission config;
- `scripts/build_research_mission.py` — deterministic mission artifact builder;
- `.github/workflows/research-mission-plan.yml` — production planning artifact.

The production planning workflow intentionally does not claim it searched the internet. Before a compliant research executor supplies evidence, its coverage artifact must remain `CALIBRATION_ONLY`.

## 14. Governing invariant

> **联网能力不是某几个网站的爬虫，而是一种可治理、可替换、可扩展的研究能力：尽可能展开全球公开/授权信息边界，主要理解中国现实，再通过来源多样性、地域分层、反证搜索和证据晋级规则，把互联网的广度变成可信的现实观察，而不是把信息量本身当成商业真相。**
