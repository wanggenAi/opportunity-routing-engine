# Latent Value Doctrine — Constitutional Principle

Status: `CONSTITUTIONAL / LOCKED`

This document defines the highest-order business and architectural doctrine of this repository.

Code, data models, sensors, scoring, experiments, workflows and product ideas exist to serve this doctrine. They do not define it.

If a technically correct implementation pulls the system away from this doctrine, the implementation is wrong for this repository.

The executable formation principle is defined in `docs/LATENT_VALUE_FORMATION_BRIDGE.md`. Despite the historical filename, that document is a constitutional discovery principle, not an optional implementation bridge.

## 1. The system does not begin with supply and demand

The system begins with **reality and actors**.

An actor may be a person, household, organization, institution, community, asset owner, capability holder, channel, network or other value-bearing node.

The engine must not assume that an actor already understands:
- what it owns;
- what it can do;
- what is underused;
- what it lacks;
- how its perception or motives are changing;
- what outcome it is moving toward or away from;
- what others may value;
- what exchange structure could unlock value.

Therefore the core object is not an explicit listing, RFQ, procurement notice, job post, sales lead or stated demand.

Those are observable manifestations of deeper states and are valid downstream evidence. They do not define the core discovery problem.

```text
DEMAND DISCOVERY != LATENT VALUE FORMATION
EXPLICIT DEMAND EXECUTION != CORE LATENT VALUE FORMATION
```

## 2. Commercial value does not have to pre-exist the discovery

A resource may objectively exist while the commercial value structure that could emerge from it does not yet exist.

The repository therefore distinguishes:

```text
OBJECTIVE ENDOWMENT EXISTS
!=
ENDOWMENT IS UTILIZED
!=
ACTOR RECOGNIZES ITS VALUE
!=
A MARKET / PRODUCT / SERVICE EXISTS
!=
PAID DEMAND EXISTS
```

The engine is allowed to reason about **value formation**: how objective resources, actor state transitions, psychology, behavior and complementary world nodes could combine into an exchange that nobody has yet organized.

That reasoning is a hypothesis, not evidence that a business exists.

The central principle is:

> **Demand does not have to exist first. The conditions from which value may emerge can exist first. The system infers a falsifiable exchange from those conditions, then reality decides whether the exchange deserves to exist.**

## 3. Actors are not fixed sides

Do not model the world as:

```text
DEMAND SIDE -> RESOURCE SIDE
```

Prefer:

```text
ACTOR A
  -> objective endowments
  -> current state / state change
  -> perception / motive / behavior
  -> unused / hidden / mispriced / uncombined value
  -> deficits / frictions / contradictions

ACTOR B
  -> objective endowments
  -> current state / state change
  -> perception / motive / behavior
  -> unused / hidden / mispriced / uncombined value
  -> deficits / frictions / contradictions
```

Either actor may simultaneously be:
- a resource owner;
- a beneficiary;
- a payer;
- a capability provider;
- a demand source;
- a distribution channel;
- a trust source;
- a data source;
- a coordination node;
- a source of recurring transaction flow.

`NEED_ACTOR` and `RESOURCE_OWNER` are roles, not permanent identities.

## 4. Resource–Psychology Disequilibrium is first-class

A primary discovery zone is the mismatch between what an actor objectively has and what the actor's current psychology, behavior, environment and available routes allow those resources to become.

```text
OBJECTIVE ENDOWMENT
+
STATE / STATE CHANGE
+
PERCEPTION / MOTIVE
+
OBSERVED BEHAVIOR
+
UNDERUSE / MISALIGNMENT
→ RESOURCE–PSYCHOLOGY DISEQUILIBRIUM
```

This may appear as:
- time without a valued new structure;
- expertise without a callable role;
- capital without trusted deployment routes;
- technical capability without access, reputation or domain context;
- customer access without execution capability;
- equipment or space without a viable scenario;
- attention without a transaction structure;
- relationships without a mechanism that converts trust into accepted outcomes.

These are search zones, not automatically opportunities.

## 5. Latent value and unformed outcomes are first-class

`LATENT_VALUE` means potentially realizable value that exists in an actor, resource, relationship, behavior pattern or structural position but is not yet fully recognized, packaged, connected, trusted, priced or activated.

`UNMET / UNFORMED OUTCOME` means a state transition that the actor may value or avoid, evidenced through state, perception, motive and behavior, but that has not yet been cleanly articulated as a purchasable product or explicit demand.

Examples of latent value include:
- idle time that can become bounded paid capability;
- an experienced worker whose job title hides reusable expertise;
- unused equipment whose valuable use case has not been recognized;
- a community with trusted access but no transaction architecture;
- repeated complaints or adaptations that reveal a costly contradiction but not yet explicit demand;
- recurring demand access that can itself become a routing resource;
- a dataset, relationship, location, reputation or installed base whose value appears only when combined with another actor;
- fragmented small capacities that become valuable only after aggregation and acceptance rules.

Latent value and unformed outcomes are **hypotheses until evidenced**.

The engine must never declare value merely because it can imagine a use case.

## 6. The canonical discovery and formation chain

The highest-order chain is:

```text
WORLD SENSING
-> ACTOR
-> OBJECTIVE ENDOWMENT / STATE
-> STATE CHANGE
-> PERCEPTION / MOTIVE
-> OBSERVED BEHAVIOR
-> FRICTION / UNDERUSE / MISALLOCATION / CONTRADICTION
-> RESOURCE–PSYCHOLOGY DISEQUILIBRIUM
-> UNMET / UNFORMED OUTCOME HYPOTHESIS
-> COMPLEMENTARY WORLD-NODE SEARCH
-> COUNTERFACTUAL EXCHANGE DESIGN
-> WHY EXCHANGE DOES NOT ALREADY HAPPEN
-> EVIDENCE / CONTRADICTION SEARCH
-> CHEAP BOUNDED VALIDATION
-> ONLY IF SUPPORTED: NEED / RESOURCE / BLOCKER / PAYER PROJECTION
-> ROUTING / EXECUTION
-> ACCEPTED VALUE / SETTLEMENT
-> REPEAT / LEARNING / BETTER ALLOCATION
```

`NeedSignal`, `ResourceSignal` and `BlockerSignal` are fail-closed evidence projections inside this larger model.

They must not shrink the engine into an explicit supply-demand matcher.

## 7. Psychology & Behavior Engineering is upstream of product ideas

The psychology system is not merely a social-media complaint miner.

It helps reconstruct:

```text
WHO / ACTOR SEGMENT
→ OBJECTIVE ENDOWMENTS
→ CURRENT STATE
→ RECENT CHANGE
→ PERCEPTION
→ MOTIVE / FEAR / ASPIRATION
→ OBSERVED BEHAVIOR
→ CONTRADICTION
→ RESOURCE–PSYCHOLOGY DISEQUILIBRIUM
→ POSSIBLE UNFORMED OUTCOME
```

The system should prefer behavior over self-description and corroborate psychology with money/behavior where possible.

Platforms such as Douyin, Zhihu, Xiaohongshu, Reddit, X or future sources are sensors, not ontology.

```text
SOCIAL SALIENCE != POPULATION SHARE
PSYCHOLOGY SIGNAL != DEMAND
MOTIVE HYPOTHESIS != WILLINGNESS TO PAY
BEHAVIOR SIGNAL != TRANSACTION
```

Do not build unnecessary individual psychographic profiles or infer sensitive traits.

## 8. Discovery must search for what actors do not know about themselves

The engine must search not only for stated needs and advertised resources, but also for observable evidence of:
- idle or underused capacity;
- mismatched skills;
- low utilization;
- repeated manual work;
- avoidable delay;
- excess inventory;
- repeated repricing;
- abandoned or fragmented assets;
- hiring / layoff / project-cycle changes;
- unused distribution or relationship capacity;
- trust gaps;
- packaging gaps;
- coordination gaps;
- information asymmetry;
- recurring workarounds;
- demand aggregation potential;
- resources that become valuable only in combination;
- contradictions between endowment and behavior;
- desired state transitions that are visible before a product category exists.

The strongest discovery is often not `someone asked for X` but:

> **valuable conditions are present, actor states are changing, a contradiction is visible, and the actors have not yet formed the exchange that could create the new value.**

## 9. Value creation is not mere matching

The orchestrator must add incremental value by doing one or more of the following:
- revealing hidden capability;
- revealing hidden deficit or unformed outcome;
- identifying resource–psychology disequilibrium;
- reframing or packaging a resource;
- aggregating fragmented resources or demand;
- decomposing vague outcomes into callable CapabilityUnits;
- designing a counterfactual exchange;
- designing trust and acceptance;
- reducing information asymmetry;
- lowering coordination cost;
- creating a credible Hook;
- aligning incentives;
- making an unavailable relationship executable and repeatable.

A simple introduction is insufficient unless the introduction itself resolves a real recurring structural blocker.

## 10. Counterfactual Exchange Design is a constitutional operation

The engine must be able to ask:

> **If currently separate real-world nodes were connected under explicit roles, incentives, permission, trust and acceptance, could a new exchange emerge that creates incremental value for every required participant?**

The answer may describe a structure that does not currently exist as a mature market or product.

This remains counterfactual until accepted by reality.

```text
COUNTERFACTUAL EXCHANGE != ACCEPTED EXCHANGE
COMPLEMENTARITY != TRANSACTIONABILITY
LATENT VALUE FORMATION != COMMERCIAL OPPORTUNITY
```

The design must preserve who controls each node, what each participant gains, why the exchange is absent today, what permissions matter, what the orchestrator contributes and what experiment can falsify the thesis.

## 11. Evidence discipline remains absolute

This doctrine does not authorize imagination to become truth.

```text
OBJECTIVE RESOURCE EXISTS != COMMERCIAL VALUE EXISTS
POTENTIAL VALUE != PROVEN VALUE
LATENT_VALUE_HYPOTHESIS != RESOURCE
UNFORMED OUTCOME HYPOTHESIS != DEMAND
OBSERVED FRICTION != PAID NEED
PSYCHOLOGY HYPOTHESIS != DEMAND
DEMAND != WILLINGNESS TO PAY
WILLINGNESS TO PAY != TRANSACTION
RESOURCE EXISTS != UNDERUSED
UNDERUSED != AVAILABLE
COMPLEMENTARITY != TRANSACTIONABILITY
ACTOR BENEFITS != ACTOR PAYS
COUNTERFACTUAL EXCHANGE != ACCEPTED EXCHANGE
UNKNOWN != PASS
```

The purpose of the engine is to **infer boldly and promote conservatively**.

Hypothesis generation may be broad.
Canonical promotion must remain fail-closed and evidence-bound.

## 12. Architecture must follow cognition

The repository must obey this dependency direction:

```text
WORLD MODEL / DOCTRINE
        ↓
LATENT VALUE FORMATION MODEL
        ↓
DISCOVERY / EVIDENCE MODEL
        ↓
DECISION / VALIDATION MODEL
        ↓
ORCHESTRATION MODEL
        ↓
SOFTWARE MODULES
        ↓
IMPLEMENTATION DETAILS
```

Never reverse it.

Do not let:
- one API;
- one website;
- one source format;
- one procurement feed;
- one current candidate;
- one data schema;
- one convenient implementation

redefine the business architecture.

A source adapter is an **observer**, not the strategy.
A data field is an **observation**, not the ontology.
A current opportunity is a **sample**, not the business identity.
An explicit demand is a **downstream observation**, not the definition of opportunity formation.

## 13. Architectural veto

Before adding or materially expanding any feature, ask:

1. What actor state, objective endowment, psychology/behavior shift, disequilibrium, unformed outcome, complementary node or exchange structure does this help us observe, infer, validate or activate?
2. Does it improve the engine's ability to form and test value structures that actors may not already have articulated?
3. Does it preserve the distinction between inference and evidence?
4. Does it improve our ability to connect complementary nodes without turning the operator into permanent sales/delivery labor?
5. Is this generalizable system capability, or are we overfitting to one website, explicit demand, transaction or candidate?
6. If this feature disappeared, would the core doctrine still be intact?

If answers 1–4 are weak, the feature is not a core-priority feature even if technically useful.

## 14. Executable value requires operator-access truth and counterpart-visible surplus

The operator is also an `Actor` with real endowments, deficits, history, credibility, relationships, constraints and access rights.

The engine must therefore evaluate three different truths:

```text
VALUE / EXCHANGE TRUTH
!=
CURRENT OPERATOR ACCESS / EXECUTION FEASIBILITY
!=
COUNTERPARTY VISIBLE SURPLUS
```

A latent-value formation may be true while the current operator still lacks a legitimate route to the relevant actor.
A legitimate route may exist while the actor still has no concrete reason to participate.

Relevant `OperatorEndowment` may include, where evidenced and appropriate:
- years of real professional work;
- accepted project/delivery history;
- domain and technical literacy;
- systems-analysis and coordination ability;
- prior employers/clients/projects that legitimately signal competence;
- education and training;
- cross-region or international experience;
- communication and trust-building ability;
- local knowledge;
- existing relationships and warm paths;
- reputation / references;
- assets, capital, data, distribution or other resources the operator can credibly mobilize.

These are **inputs to feasibility**, not entitlement to counterpart attention.

### Backing is a first-class resource

When the target actor is high-trust, high-status or institutionally controlled, prefer truthful borrowed legitimacy over unsupported personal outreach.

Backing may come from:
- a recognized institution;
- employer or organizational authorization;
- a government / park / association program;
- a technology-transfer center;
- a trusted sponsor or warm introducer;
- a recognized professional role;
- an already-committed complementary actor;
- a partner whose reputation is accepted by the target actor.

The system must ask:

> **Who or what gives the operator a legitimate and credible reason to be in this conversation?**

A public contact route is not automatically strong backing. A warm introducer, authorized program, employer mandate or already-committed counterpart may be materially stronger.

### The counterpart must see concrete surplus

Do not enter a relationship merely to explain to an actor that the actor has a problem, hidden resource or opportunity.

The counterpart-facing question is:

> **What does this actor concretely gain by participating, and why should the actor believe that gain is real?**

Possible surplus includes, where evidenced:
- more revenue or a higher realized price;
- lower cost;
- less downtime / scrap / failure loss;
- higher asset/capability utilization;
- a customer, order, project or funded route;
- lower search / coordination / transaction cost;
- lower risk;
- access to a scarce capability, channel, market or relationship;
- legitimate organizational recognition or policy/project benefit the actor actually values.

The engine should prefer:

```text
CURRENT BASELINE
-> PROPOSED EXCHANGE
-> VISIBLE INCREMENTAL GAIN
-> WHO BEARS COST / RISK
-> WHEN GAIN BECOMES OBSERVABLE
-> WHAT WOULD FALSIFY THE CLAIM
```

### Analysis artifacts are subordinate

A presentation, report, problem brief, model or analysis can support preparation or an already legitimate conversation.

It is not a default credential and it is not the counterparty benefit.

```text
ANALYSIS != SURPLUS
PPT / REPORT != HOOK BY DEFAULT
PROBLEM EXPLANATION != COUNTERPARTY BENEFIT
ACTOR HAS HIDDEN VALUE != ACTOR SHOULD WORK WITH US
```

If any lower-level document treats a `FIRST VALUE PACKET`, PPT, diagnosis or analysis artifact as a hard access credential by itself, this constitutional section overrides it.

### Local field context

Local norms around backing, oral trust, face, status and relationship can materially affect execution, but they are runtime field priors to test rather than universal facts.

For a local candidate, record whether the first-contact decision is driven primarily by:
- trusted introduction / backing;
- real professional background;
- orally legible economics;
- institutional role;
- direct measurable gain;
- written material.

Do not assign written artifacts artificial priority merely because they are easy for the software to represent.

The system must never silently assume:

```text
PUBLIC ACTOR = ACCESSIBLE ACTOR
VALUABLE ACTOR = CALLABLE RESOURCE
OPERATOR SKILL = COUNTERPART TRUST
PUBLIC WINDOW = STRONG BACKING
ANALYSIS = COUNTERPARTY SURPLUS
DISCOVERED VALUE = EXECUTABLE VALUE
```

An opportunity may therefore be commercially attractive but temporarily `ACCESS_BLOCKED`.
That is a route constraint, not evidence that the underlying latent value is false.

## 15. Orchestrator identity

The orchestrator is primarily responsible for:

```text
SEE STRUCTURE
-> OBSERVE OBJECTIVE ENDOWMENTS / STATE CHANGES
-> IDENTIFY RESOURCE–PSYCHOLOGY DISEQUILIBRIUM
-> FORM UNMET / UNFORMED OUTCOME HYPOTHESES
-> SEARCH COMPLEMENTARY WORLD NODES
-> DESIGN COUNTERFACTUAL EXCHANGES
-> PROVE WHAT IS REAL
-> DEFINE RULES / TRUST / ACCEPTANCE
-> ROUTE EXECUTION
-> LEARN FROM OUTCOMES
```

The operator is not defined by personally selling, sourcing or delivering every transaction.

The durable advantage is the ability to see conditions from which value can form, test those structures against reality, and organize accepted circulation when they survive.

## 16. Governing sentence

> **先观其所自：不把世界预设成“需求方与供给方”，也不等待市场先把需求说出来。先观察每个 Actor 客观拥有什么、状态怎样变化、如何感受这种变化、动机与行为怎样偏移，以及“客观拥有”与“实际利用”之间出现了什么错位；再从这种 Resource–Psychology Disequilibrium 中推导尚未被清晰表达的结果，寻找世界另一处真实存在的互补节点，设计一种可能尚不存在的交换。推导不是事实，心理不是需求，需求不是付费，付费意愿也不是成交；只有现实验证、权限、参与者增量收益、验收与结算成立时，潜在价值才真正进入商业世界。**
