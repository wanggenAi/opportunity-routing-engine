# Latent Value Doctrine — Constitutional Principle

Status: `CONSTITUTIONAL / LOCKED`

This document defines the highest-order business and architectural doctrine of this repository.

Code, data models, sensors, scoring, experiments, workflows and product ideas exist to serve this doctrine. They do not define it.

If a technically correct implementation pulls the system away from this doctrine, the implementation is wrong for this repository.

## 1. The system does not begin with supply and demand

The system begins with **reality and actors**.

An actor may be a person, household, organization, institution, community, asset owner, capability holder, channel, network or other value-bearing node.

The engine must not assume that an actor already understands:
- what it owns;
- what it can do;
- what is underused;
- what it lacks;
- what others may value;
- what exchange structure could unlock value.

Therefore the core object is not an explicit listing, RFQ, procurement notice, job post, sales lead or stated demand.

Those are only observable manifestations of deeper states.

## 2. Both sides contain resources, deficits and latent value

Do not model the world as:

```text
DEMAND SIDE -> RESOURCE SIDE
```

Prefer:

```text
ACTOR A
  -> endowments
  -> constraints
  -> behavior
  -> unused / hidden / mispriced / uncombined value
  -> deficits / frictions

ACTOR B
  -> endowments
  -> constraints
  -> behavior
  -> unused / hidden / mispriced / uncombined value
  -> deficits / frictions
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

## 3. Latent value is first-class

`LATENT_VALUE` means potentially realizable value that exists in an actor, resource, relationship, behavior pattern or structural position but is not yet fully recognized, packaged, connected, trusted, priced or activated.

Examples include:
- idle time that can become bounded paid capability;
- an experienced worker whose job title hides reusable expertise;
- unused equipment whose profitable use case has not been recognized;
- a community with trusted access but no transaction architecture;
- repeated complaints that reveal a costly workaround but not yet explicit demand;
- recurring demand that can itself become a valuable routing resource;
- a dataset, relationship, location, reputation or installed base whose value appears only when combined with another actor;
- fragmented small capacities that become valuable only after aggregation and acceptance rules.

Latent value is a **hypothesis until evidenced**.

The engine must never declare value merely because it can imagine a use case.

## 4. The canonical discovery chain

The highest-order discovery chain is:

```text
ACTOR
-> ENDOWMENT / STATE
-> CHANGE
-> BEHAVIOR
-> FRICTION / UNDERUSE / MISALLOCATION
-> LATENT_VALUE_HYPOTHESIS
-> COMPLEMENTARY_ACTOR
-> EXCHANGE_HYPOTHESIS
-> BLOCKER
-> EVIDENCE
-> BOUNDED VALIDATION
-> ACCEPTED VALUE
-> SETTLEMENT
-> REPEAT / LEARNING / BETTER ALLOCATION
```

`NeedSignal`, `ResourceSignal` and `BlockerSignal` are evidence projections inside this larger model.

They must not shrink the engine into an explicit supply-demand matcher.

## 5. Discovery must search for what actors do not know about themselves

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
- resources that become valuable only in combination.

The strongest discovery is often not "someone asked for X" but:

> **something valuable is present, something costly is happening, and the actors have not yet formed the exchange that could connect them.**

## 6. Value creation is not mere matching

The orchestrator must add incremental value by doing one or more of the following:
- revealing hidden capability;
- revealing hidden deficit;
- reframing or packaging a resource;
- aggregating fragmented resources or demand;
- decomposing vague outcomes into callable CapabilityUnits;
- designing trust and acceptance;
- reducing information asymmetry;
- lowering coordination cost;
- creating a credible Hook;
- aligning incentives;
- designing a new exchange structure;
- making an unavailable relationship executable and repeatable.

A simple introduction is insufficient unless the introduction itself resolves a real recurring structural blocker.

## 7. Evidence discipline remains absolute

This doctrine does not authorize imagination to become truth.

```text
POTENTIAL VALUE != PROVEN VALUE
LATENT_VALUE_HYPOTHESIS != RESOURCE
OBSERVED FRICTION != PAID NEED
RESOURCE EXISTS != UNDERUSED
UNDERUSED != AVAILABLE
COMPLEMENTARITY != TRANSACTIONABILITY
ACTOR BENEFITS != ACTOR PAYS
UNKNOWN != PASS
```

The purpose of the engine is to **discover boldly and promote conservatively**.

Hypothesis generation may be broad.
Canonical promotion must remain fail-closed and evidence-bound.

## 8. Architecture must follow cognition

The repository must obey this dependency direction:

```text
WORLD MODEL / DOCTRINE
        ↓
DISCOVERY MODEL
        ↓
EVIDENCE MODEL
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

## 9. Architectural veto

Before adding or materially expanding any feature, ask:

1. What latent value, actor state, behavior, friction, resource or exchange structure does this help us observe, validate or activate?
2. Does it improve the engine's ability to discover value that actors may not already have articulated?
3. Does it preserve the distinction between hypothesis and evidence?
4. Does it improve our ability to connect complementary actors without turning the operator into permanent sales/delivery labor?
5. Is this generalizable system capability, or are we overfitting to one website, transaction or candidate?
6. If this feature disappeared, would the core doctrine still be intact?

If the answer to questions 1-4 is weak, the feature is not a core-priority feature even if it is technically useful.

## 10. Executable value requires operator-access truth and counterpart-visible surplus

The operator is also an `Actor` with real endowments, deficits, history, credibility, relationships, constraints and access rights.

The engine must therefore evaluate three different truths:

```text
VALUE / EXCHANGE TRUTH
!=
CURRENT OPERATOR ACCESS / EXECUTION FEASIBILITY
!=
COUNTERPARTY VISIBLE SURPLUS
```

A latent-value hypothesis may be true while the current operator still lacks a legitimate route to the relevant actor.
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

## 11. Orchestrator identity

The orchestrator is primarily responsible for:

```text
SEE STRUCTURE
-> DISCOVER HIDDEN VALUE
-> FORM EXCHANGE HYPOTHESES
-> PROVE WHAT IS REAL
-> DESIGN THE CONNECTION
-> DEFINE RULES / TRUST / ACCEPTANCE
-> ROUTE EXECUTION
-> LEARN FROM OUTCOMES
```

The operator is not defined by personally selling, sourcing or delivering every transaction.

The durable advantage is the ability to see and organize value that remains invisible or unusable in its current form.

## 12. Governing sentence

> **先观其所自：不把世界预设成“需求方与供给方”，而是观察每个 Actor 已有什么、缺什么、正在发生什么、哪些价值被闲置、遮蔽、错配或尚未成形；再以证据证明潜在价值，以结构找到互补关系，同时诚实评估操盘者自身已有的能力、信用、后台、入口与缺口；只有在价值真实、关系可达、参与者能看见真实增量收益、规则可接受时，才以信任、激励和可验收能力让原本彼此无关的价值发生连接，使价值流动、交换、沉淀并形成可持续循环。**

This doctrine is upstream of all implementation choices.
