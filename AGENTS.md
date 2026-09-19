# AGENTS.md

Instructions for AI agents, coding assistants and human contributors working in this repository.

## Prime directive

Build a truthful, evidence-driven **Actor-First Regenerative Latent-Value Formation & Orchestration Engine** whose highest-order purpose is not merely to find existing demand, but to detect the real-world conditions from which **new value structures may form before actors have articulated them as demand**, discover the latent connections reality is already trying to form, and organize those connections only after evidence justifies doing so.

The repository does **not** begin from a fixed `DEMAND SIDE -> SUPPLY SIDE` model. It begins from actors, objective endowments, state changes, perception, motive, behavior, contradictions, underuse, misallocation, unrealized complementarities and observable connection pressure.

```text
WORLD SENSING
→ ACTOR + OBJECTIVE ENDOWMENT
→ STATE / STATE CHANGE
→ PERCEPTION / MOTIVE
→ OBSERVED BEHAVIOR
→ SURFACE PHENOMENON / SURFACE FRICTION / UNDERUSE / CONTRADICTION
→ RESOURCE–PSYCHOLOGY DISEQUILIBRIUM
→ LATENT / UNFORMED OUTCOME HYPOTHESIS
→ STRUCTURAL FRICTION HYPOTHESIS
→ CROSS-EVIDENCE + ALTERNATIVE-EXPLANATION SEARCH
→ EVIDENCED STRUCTURAL FRICTION
→ COMPLEMENTARY WORLD NODES
→ CONNECTION-PRESSURE EVIDENCE
→ PARTIAL FLOW / WORKAROUND / SUBSTITUTE / ADJACENT PRECEDENT
→ OBSERVED MISSING EDGE / STRANDING BARRIER BETWEEN NODES
→ LATENT CONNECTION HYPOTHESIS
→ CONTRADICTION SEARCH
→ ONLY THEN: COUNTERFACTUAL EXCHANGE MECHANICS
→ CHEAP BOUNDED REALITY CONFIRMATION
→ ONLY IF SUPPORTED: NEED / RESOURCE / BLOCKER / PAYER PROJECTION
→ ROUTING / ACCEPTANCE / SETTLEMENT
→ REPEAT / LEARNING / BETTER ALLOCATION
```

The key rule is:

> **Demand does not have to exist first, and the first visible friction is not necessarily the real opportunity. Treat surface pain as a sensor: infer the actor's latent desired state, test the deeper structural friction that prevents that state transition, then discover evidence that reality is already exerting pressure toward a connection among complementary nodes. Only after those layers are evidence-bound should the system design minimum exchange mechanics and let reality confirm or falsify the remaining uncertainty.**

`NeedSignal`, `ResourceSignal` and `BlockerSignal` are downstream fail-closed evidence projections. They must not shrink the engine into an explicit demand-matching system.

Optimize for **truthful value formation + discovered latent connections + recurring accepted outcomes + delegatability + regenerative circulation + normalized orchestration economics**, not code volume, lead count, explicit-demand count, founder activity or narrative appeal.

**Code serves the doctrine. The doctrine does not bend to the convenience of code, a website, an API, an explicit-demand feed, a current candidate or a source schema.**

## Durable execution and recovery protocol — LOCKED

GitHub's current repository state is the operational source of truth for project progress. Chat context is disposable transport; it is never authoritative project state.

At the start of every non-trivial task, before planning new work:
1. resolve the current `main` HEAD and inspect recent git history;
2. inspect open pull requests and their exact head SHAs;
3. inspect the active/open Issues relevant to the current mission;
4. inspect GitHub Actions / CI for the relevant commit or PR head;
5. inspect workflow artifacts when they exist;
6. read `TASK_STATE.md`;
7. read the persisted JSON, ledgers, result packets or other durable artifacts referenced by `TASK_STATE.md`.

Do not ask the user to restate project background merely because a chat restarted. Do not infer progress from chat memory. Do not redo work already present on `main` and already verified by repository evidence.

If GitHub facts and `TASK_STATE.md` disagree, GitHub wins. Correct `TASK_STATE.md` at the next safe checkpoint instead of forcing reality to match stale state.

For long tasks, work in small, independently verifiable stages. A useful stage should end in one or more durable checkpoints such as:
- a focused commit;
- a pushed branch;
- a pull request with exact head SHA;
- a CI run with recorded conclusion;
- a persisted JSON / ledger / result packet;
- a workflow artifact when the workflow actually emits one;
- an Issue update that points to the durable repository evidence.

After every material stage, refresh `TASK_STATE.md` with facts, evidence pointers, the current blocker and exactly one best next action. Keep it compact. It is an operational handoff record, not a narrative log and not a duplicate of Issues, PR descriptions, scan reports or research documents.

On interruption, timeout, connection loss or a new chat, resume before replanning:
`LIVE GITHUB STATE -> TASK_STATE -> referenced durable evidence -> next unresolved action`.

Do not create a second checkpoint system when an existing repository ledger, persisted JSON, PR, Issue or workflow artifact already carries the needed evidence. `TASK_STATE.md` should point to those objects rather than copy their contents.

A state-only checkpoint commit necessarily advances `main`. Therefore `Last Verified Main` in `TASK_STATE.md` means the latest functional/CI-verified main SHA observed before the state checkpoint write. On every resume, resolve live `main` first; if newer material commits exist, reconcile and update the file.

Before ending a long task, leave `TASK_STATE.md` in a handoff-ready state:
- no imaginary CI or artifact claims;
- no stale active PR/branch claims when they can be resolved;
- completed work separated from blockers;
- exactly one next action;
- explicit do-not-repeat items;
- current doctrine guardrails preserved.

## Constitutional source of truth

Before changing business logic, read these in order:
1. `docs/LATENT_VALUE_DOCTRINE.md`
2. `docs/STRUCTURAL_FRICTION_DISCOVERY_PRINCIPLE.md`
3. `docs/LATENT_CONNECTION_DISCOVERY_PRINCIPLE.md`
4. `docs/LATENT_VALUE_FORMATION_BRIDGE.md`
5. `docs/FORMAL_TRUTH.md`
6. `docs/RESOURCE_ACTIVATION_THESIS.md`
7. `docs/DISCOVERY_ENGINE.md`
8. `docs/PSYCHOLOGY_BEHAVIOR_TRACKER.md`
9. `docs/RESOURCE_IMBALANCE_ENGINE.md`
10. `docs/RESOURCE_ORCHESTRATION_KERNEL.md`
11. `docs/ACTOR_MODEL.md`
12. `docs/THESIS_TRANSACTION_GAPS.md`
13. `docs/OPPORTUNITY_SCORECARD.md`
14. `docs/ARCHITECTURE.md`
15. current `docs/research/`, `docs/field/` and `docs/launch/` files relevant to the task.

`docs/LATENT_VALUE_DOCTRINE.md` is constitutional. `docs/STRUCTURAL_FRICTION_DISCOVERY_PRINCIPLE.md`, `docs/LATENT_CONNECTION_DISCOVERY_PRINCIPLE.md` and `docs/LATENT_VALUE_FORMATION_BRIDGE.md` are also locked constitutional discovery principles. If another document, implementation or workflow conflicts with them, the lower-level artifact must change.

There is no active `EXP-*` opportunity layer after the 2026-09-10 reset. Do not recreate it unless the architecture is explicitly changed.

When a major assumption changes, update `docs/FORMAL_TRUTH.md` in the same change.

## Architectural dependency direction — LOCKED

The repository must preserve this dependency direction:

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

A source adapter is an observer, not the strategy.
A data field is an observation, not the ontology.
A current opportunity is a sample, not the business identity.
A procurement feed is one sensor, not the business model.
An explicit demand is evidence, not the definition of value formation.
A plausible pairing is a hypothesis, not a discovered connection.

Before adding or materially expanding a feature, answer:
1. What objective endowment, actor state/change, psychology/behavior shift, contradiction, disequilibrium, unformed outcome, complementary node, connection-pressure evidence or exchange structure does this help observe, infer, validate or activate?
2. Does it improve discovery of value relationships reality is already trying to form rather than merely generate plausible combinations?
3. Does it preserve inference/evidence boundaries?
4. Does it improve our ability to discover and activate complementary nodes without making the operator permanent search/sales/delivery labor?
5. Is it reusable system capability rather than overfitting to one source, website, explicit demand, transaction or candidate?

If answers 1–4 are weak, the feature is not a core-priority feature even if technically useful.

## Non-negotiable truth rules

- Never fabricate actors, endowments, psychology, needs, payments, prices, contacts, capabilities, transactions or outcomes.
- `UNKNOWN != PASS`.
- `OBJECTIVE RESOURCE EXISTS != COMMERCIAL VALUE EXISTS`.
- `DEMAND DISCOVERY != LATENT VALUE FORMATION`.
- Inference != fact.
- `SURFACE PHENOMENON != STRUCTURAL FRICTION`.
- `SURFACE FRICTION != OPPORTUNITY`.
- `STATED NEED != LATENT OUTCOME`.
- `OBSERVED COST != ROOT CAUSE`.
- `STRUCTURAL FRICTION HYPOTHESIS != EVIDENCED STRUCTURAL FRICTION`.
- `STRUCTURAL FRICTION != MISSING EDGE`.
- `BUYER COST FIRST != CONSTITUTION`.
- `EXTERNALIZED WORKAROUND FIRST != CONSTITUTION`.
- `OBSERVED != INFERRED != EVIDENCED_STRUCTURE`.
- Potential value != proven value.
- Latent-value formation hypothesis != commercial opportunity.
- Unformed outcome hypothesis != demand.
- Psychology hypothesis != demand.
- Motive hypothesis != willingness to pay.
- `CONNECTION INVENTION != CONNECTION DISCOVERY`.
- `COMPLEMENTARITY != LATENT CONNECTION`.
- `CONNECTION HYPOTHESIS != CONNECTION PRESSURE EVIDENCE`.
- `MISSING EDGE HYPOTHESIS != OBSERVED MISSING EDGE`.
- `COUNTERFACTUAL EXCHANGE != LATENT CONNECTION EVIDENCE`.
- `LATENT CONNECTION != ACCEPTED EXCHANGE`.
- Human outreach != primary discovery sensor.
- Complaint != demand.
- Demand != willingness to pay.
- Willingness to pay != transaction.
- Beneficiary != payer by default.
- Trend != business.
- Social-media salience != population share.
- Paid Need != Resource Imbalance.
- Resource Exists != Resource Is Underused.
- Underused != available.
- Complementarity != transactionability.
- Counterfactual exchange != accepted exchange.
- `DISCOVERED != OPTIONED`.
- Introduction != orchestration value.
- Founder free labor != profit.
- Capability claim != capability proof.
- One provider != replaceable supply.
- One transaction != repeatability.
- One customer != recurring Demand Pump.
- Recurring founder sales effort != regenerative demand.
- LLM confidence != commercial evidence.
- Preserve provenance, dates and contradictions.
- Separate subsidized/officially promoted outcomes from independent payer evidence.

## Formation-first discovery rule

Do not start from the operator's existing skills, a favored product, a fashionable technology, a known procurement feed, a supplier catalog or an already-articulated demand list.

Start from broad reality:
- GDP / sector contribution;
- CPI/PPI/service inflation;
- income / employment;
- consumption category mix;
- retail / service retail / online retail;
- investment / equipment investment;
- imports / exports;
- demographics / aging / household structure;
- technology / policy;
- industry-chain movement;
- actor psychology / decision logic;
- observed spending, workarounds and operational behavior;
- observable underused skills, assets, channels and productive capacity;
- utilization changes, idle time, fragmentation, repeated repricing and stranded assets;
- relationships, trust, reputation, access, distribution and installed-base resources;
- combinations of resources whose value appears only when connected;
- repeated partial, informal, substitute and adjacent flows that may reveal a connection already trying to form.

Then reconstruct:

```text
ACTOR / SEGMENT
→ OBJECTIVE ENDOWMENTS
→ CURRENT STATE
→ STATE CHANGE
→ PERCEPTION / MOTIVE
→ BEHAVIOR
→ SURFACE PHENOMENON / SURFACE FRICTION / CONTRADICTION
→ RESOURCE–PSYCHOLOGY DISEQUILIBRIUM
→ LATENT / UNFORMED OUTCOME HYPOTHESIS
→ STRUCTURAL FRICTION HYPOTHESIS
→ CROSS-EVIDENCE / ALTERNATIVE-EXPLANATION SEARCH
→ EVIDENCED STRUCTURAL FRICTION
→ COMPLEMENTARY WORLD-NODE SEARCH
→ CONNECTION-PRESSURE EVIDENCE
→ PARTIAL FLOW / WORKAROUND / SUBSTITUTE / ADJACENT PRECEDENT
→ OBSERVED MISSING EDGE / STRANDING BARRIER BETWEEN NODES
→ LATENT CONNECTION HYPOTHESIS
→ MINIMUM COUNTERFACTUAL EXCHANGE MECHANICS
→ CHEAP REALITY CONFIRMATION
```

The engine must search for what actors may not know about themselves: hidden capability, hidden deficit, underused relationships, changed resource meaning, packaging gaps, coordination gaps, unrealized exchange structures and outcomes that have not yet become product categories.

It must also search for what **reality is already trying to connect**: repeated workarounds, informal exchange, failed cross-boundary attempts, substitution, referrals, expensive legacy routes and shared state changes that expose directional pressure.

Psychology signals must be tied to the same actor segment and corroborated with behavior before they can materially raise a formation hypothesis. Money evidence strengthens commercial relevance, but money is not required merely to form a bounded hypothesis worth testing.

## Structural Friction Discovery rule — LOCKED

Surface pain is an observation layer, not the terminal discovery object.

For any meaningful cost, shortage, complaint, delay, workaround, idle resource or stated need, ask:

1. What is directly observed?
2. What state is the Actor actually trying to reach or avoid?
3. What product-agnostic latent outcome follows from state, psychology and behavior?
4. What deeper structural condition prevents that transition?
5. What alternative explanations could also fit the same surface event?
6. What additional evidence would distinguish them?

Use three truth states:

```text
OBSERVED
→ INFERRED
→ EVIDENCED_STRUCTURE
```

Do not promote an inferred causal story as fact. A structural-friction hypothesis becomes `EVIDENCED_STRUCTURE` only when converging behavior, objective state, money/time sacrifice, repeated workaround/failure, independent source classes or comparable evidence survives contradiction search.

Discovery may enter through `BUYER COST FIRST`, `BEHAVIOR FIRST`, `STATE CHANGE FIRST`, `RESOURCE UNDERUSE FIRST`, `RESOURCE–PSYCHOLOGY DISEQUILIBRIUM FIRST`, `PARTIAL FLOW FIRST`, `CURRENT EXTERNALIZED WORKAROUND FIRST` or another evidence-bearing route. These are scan heuristics, not constitutional doctrine.

A bounded human probe is allowed before a missing edge is fully public when broad sensing has already isolated one decisive causal unknown. Mark it `DECISIVE_UNKNOWN / PROBE_ELIGIBLE`; ask about the narrow uncertainty, not for generic pain points or business ideas.

```text
SURFACE FRICTION
→ LATENT OUTCOME
→ STRUCTURAL FRICTION
→ COMPLEMENTARY WORLD NODES
→ CONNECTION PRESSURE
→ MISSING EDGE
→ LATENT CONNECTION
```

`STRUCTURAL FRICTION` explains why the Actor cannot reach the desired state under current structures. `MISSING EDGE` explains why identified complementary nodes cannot form normal value flow. Do not collapse them.

## Resource–Psychology Disequilibrium rule

A primary search zone is a mismatch between:

```text
WHAT THE ACTOR OBJECTIVELY HAS
vs
WHAT THE ACTOR'S CURRENT STATE / PSYCHOLOGY / BEHAVIOR / ENVIRONMENT ALLOWS IT TO DO WITH THOSE ENDOWMENTS
```

The system should explicitly look for contradictions such as:
- more time but less structure;
- expertise but no callable role;
- capital but no trusted deployment route;
- execution capability but no trust/client access;
- customer access but weak execution;
- equipment/space/data but no current viable scenario;
- attention but no transaction structure.

A contradiction is a search signal, not a business verdict or connection proof.

## Psychology & behavior rule

Do not reduce psychology sensing to pain-point mining.

The canonical causal sequence is:

```text
STATE CHANGE
→ PERCEPTION
→ MOTIVE / FEAR / ASPIRATION
→ OBSERVED BEHAVIOR
→ CONTRADICTION
→ POSSIBLE RESOURCE–PSYCHOLOGY DISEQUILIBRIUM
→ POSSIBLE UNFORMED OUTCOME
```

Public/authorized social platforms, forums, reviews, search and comment ecosystems can expose language and behavior clues. Platforms are sensors, not strategy. Do not build individual psychographic dossiers or infer sensitive traits.

A statement such as `I don't know what to do now`, `I want to learn X`, or `I cannot find work` is not automatically a lead, need, connection or willingness-to-pay signal. It is an observation to connect with objective state/endowment evidence and repeated behavior.

## Latent Connection Discovery rule

For a credible formation hypothesis, first ask:

> **What evidence shows that currently separate real-world nodes are already being pushed toward the same value flow, while an observed missing edge prevents that flow from becoming normal?**

The nodes may be people, groups, organizations, institutions, assets, spaces, equipment, capability/process units, channels, data, capital/budget, rights/access, software/AI/API, contracts/rules/standards, demand/event flows, trust/reputation relationships or new node types not yet named.

Do not require the eventual mechanism to already exist as a standard product category.

But before `VALIDATION_READY`, do require:
- evidenced node existence/state;
- explicit `CONNECTION_PRESSURE` evidence;
- an observed stranding barrier / missing edge;
- explicit controller/permission unknowns;
- participant-surplus hypotheses;
- contradiction search;
- a falsifiable cheapest reality confirmation;
- kill conditions.

Useful connection-pressure evidence can include repeated workarounds, informal/manual exchange, repeated failed attempts, substitution, referrals, shared causal pressure, expensive legacy routes and adjacent/historical analogues.

Only after connection pressure is evidenced may `Counterfactual Exchange Design` describe the minimum roles, incentives, permissions, trust, acceptance and settlement mechanics needed to reduce friction.

```text
LATENT CONNECTION DISCOVERY
PRECEDES
COUNTERFACTUAL EXCHANGE DESIGN
```

A well-written exchange design is not evidence that the connection exists.

## Resource Imbalance rule — downstream promotion only

`Need / Resource / Blocker` is the current fail-closed evidence gate for transaction promotion, not the entire ontology and not the first discovery step.

Before promoting an exchange route to `ROUTE_TESTABLE`, separately establish:

```text
VERIFIED NEED / DEFICIT
+
VERIFIED RESOURCE / SURPLUS
+
OBSERVED TRANSACTION BLOCKER
```

Canonical transaction-projection states are:

```text
NEED_ONLY
RESOURCE_ONLY
PAIR_HYPOTHESIS
ROUTE_TESTABLE
```

`ROUTE_TESTABLE` requires at minimum direct paid need evidence, an identified payer, a compatible resource at least `DISCOVERED`, underuse at least `OBSERVED`, blocker evidence at least `OBSERVED`, and exact capability/geography identity.

It only authorizes a cheap bounded real-world transaction test. It does not mean transaction-ready, profitable, scalable or G0-G6 approved.

Live source normalization must be auditable. Narrow deterministic classification is preferred over opaque semantic promotion. Ambiguous or unclassified evidence must remain unbound rather than being guessed into a pair.

## Canonical actor roles

Map where relevant:
- `NEED_ACTOR`
- `BENEFICIARY`
- `PAYER`
- `SPONSOR`
- `RESOURCE_OWNER`
- `CAPABILITY_PROVIDER`
- `ORCHESTRATOR`

These are roles, not permanent identities. The same actor may carry several roles and may simultaneously contain resources, deficits, motives and state transitions.

Operator != capability provider by default.

## Capability-first execution

The atomic execution unit is a `CapabilityUnit`, not a person/job title.

Define where feasible:

```text
purpose
input
required output
acceptance criteria
provider class
proof required
price model
payout condition
deadline / SLA
dependencies
trust / safety / confidentiality requirements
replacement rule
failure / refund rule
```

Sales, demand sourcing, qualification, research, development, design, delivery, QA, support, logistics and settlement are all potential routable capabilities.

## Delegation-first rule

For every recurring execution task:

```text
eliminate?
→ automate safely?
→ delegate as bounded CapabilityUnit?
→ only then temporary operator execution
```

When the operator temporarily executes a routable task, record time, reason, replacement plan and `operator_shadow_cost`.

## Demand Pump / circulation rule

A preferred core opportunity should ultimately attach to a recurring event source: a channel, installed base, workflow, lifecycle, actor transition or relationship that naturally generates repeated formation/transaction events.

A Demand Pump is itself potentially a resource: recurring access, recurring problems, recurring attention or recurring transaction flow may become latent value when structured correctly.

Preferred loop:

```text
RECURRING STATE / EVENT FLOW
→ FORMATION OR TASK QUEUE
→ CAPABILITY DECOMPOSITION
→ REPLACEABLE / REPLENISHING NODES
→ ACCEPTED OUTCOME
→ SETTLEMENT
→ PERFORMANCE / TRUST DATA
→ BETTER FORMATION + ROUTING + LOWER FAILURE COST
→ MORE ACCEPTED EXCHANGES
↺
```

A one-off job can buy learning but cannot become the core platform wedge until circulation is proven.

## Opportunity gates

Answer all seven:
- `G0 ACTOR_ROLE_CLARITY`
- `G1 PAYER_CLARITY`
- `G2 TRANSACTIONABILITY`
- `G3 LEGAL_TRUST_SAFETY`
- `G4 CAPABILITY_DECOMPOSABILITY / DELEGATABILITY`
- `G5 ORCHESTRATION_VALUE`
- `G6 REGENERATIVE_CIRCULATION / RECURRING_DEMAND`

G0–G3 protect transaction truth/safety. G4–G6 may be explicit early unknowns but all must PASS before `REPEATABLE` / `SCALE_CANDIDATE`.

## Economic truth

Always distinguish:

```text
payer inflow
- acquisition payout
- provider payouts
- resource / QA / trust / failure / operating cost
= cash contribution margin

cash contribution margin
- operator shadow labor
= normalized orchestration margin
```

A repeatable business cannot depend on unpaid founder execution to appear profitable.

## Orchestration value test

The layer must add recurring value beyond introduction through one or more of:
- revealing hidden capability, disequilibrium or unformed outcome;
- discovering connection pressure and the true missing edge;
- designing minimum exchange mechanics for an evidenced latent connection;
- reframing / packaging / aggregating resources;
- requirement clarification;
- decomposition;
- qualification;
- dependency management;
- trust;
- QA;
- acceptance;
- replacement;
- settlement;
- accountability;
- accumulated routing/reliability data.

If buyer/provider bypass destroys most value after one introduction, downgrade it.

## Safety / compliance

Do not route regulated/safety-sensitive work to unqualified providers. Respect upstream contracts, confidentiality, data-access boundaries, labor classification, vulnerable-person safeguards and sector-specific obligations.

Never hide subcontracting where approval is required. Never access customer systems/data without explicit authorization.

Psychology sensing must not be used for covert manipulation, sensitive-trait inference or exploitation of vulnerable groups.

## Platform discipline

Required maturity path:

```text
FORMATION HYPOTHESIS
→ CONNECTION-PRESSURE EVIDENCE
→ CHEAP BOUNDED REALITY CONFIRMATION
→ L3 real commitment
→ L4 accepted paid transaction + settlement
→ L5 repeat/referral
→ L6 delegated repeat/provider replacement/alternate route
→ L7 recurring event flow produces multiple transactions and routing improves
→ only then automate repeated transaction bottlenecks / consider network product
```

Do not build a broad marketplace first.

## Current project truth

There is currently no permanent canonical business vertical.

Existing explicit-demand field probes, including public technology-demand and digital-transformation routes, remain useful empirical tests. They are **downstream samples**, not the identity of the system and not evidence that the engine should become a demand-matching platform.

The current formation capability exists in `src/latent_value_formation.py`. `VALIDATION_READY` now additionally requires explicit `CONNECTION_PRESSURE` evidence. The immediate architectural task is not another ontology rewrite. It is to ensure world sensing, objective resource/state evidence, psychology/behavior evidence, partial-flow/workaround evidence and observed missing edges feed that model empirically.

Current priorities:
1. maintain broad reality/money-flow/behavior sensors;
2. expand objective endowment, state-transition and resource-underuse sensing;
3. link psychology/motive evidence to the same actor segment and observed behavior;
4. preserve contradictions rather than averaging them away;
5. generate evidence-bound `RESOURCE_PSYCHOLOGY_DISEQUILIBRIUM` and `UNMET / UNFORMED OUTCOME` hypotheses;
6. search heterogeneous complementary world nodes;
7. discover `CONNECTION_PRESSURE` through repeated workaround, partial flow, substitution, referral, failed-attempt, shared-pressure and analogue evidence;
8. identify observed missing edges separately from imagined ones;
9. only then design minimum exchange mechanics with kill conditions;
10. use human/external validation capital on the single most decisive unresolved truth;
11. only after support exists, project Need/Resource/Blocker/payer truth and perform transaction gating;
12. keep the founder as orchestration/routing control plane rather than default search, sales or execution node.

Do not resume an old launch merely because a launch document or open historical Issue exists.

## Architecture freeze discipline

Do not respond to this doctrine by endlessly building ontology, taxonomies, dashboards, generic agent frameworks or new scrapers.

The formation model already exists. Under `P0 / FIRST EXTERNAL VALUE FLOW`, prefer:

```text
FIELD TRUTH
>
INTERNAL COMPLETENESS
```

But field action is not a substitute for upstream discovery. Broad sensing should eliminate imagined connections before scarce external contact is spent.

Add engineering only when it directly fixes a truth gap, access/validation blocker, repeated empirical bottleneck or doctrine violation.

## Success definition

The repository succeeds when it increasingly produces:
- evidence-linked actor/endowment/state transitions;
- resource–psychology disequilibrium hypotheses;
- unmet/unformed outcome hypotheses that were not already explicit demand;
- heterogeneous complementary-node structures;
- evidence-bound latent connections with explicit `CONNECTION_PRESSURE`;
- observed missing edges rather than invented blockers;
- minimum falsifiable exchange mechanics;
- reality confirmations that kill weak formations quickly;
- real payer commitment when a formation survives;
- recurring event/Demand Pumps;
- clear CapabilityUnits;
- delegated acquisition/delivery;
- accepted outputs and settlement;
- provider/node replaceability;
- positive normalized orchestration economics;
- repeated transactions from the same underlying structure;
- outcome/reliability learning that improves future formation and routing.

**The engine wins by discovering the value channels reality is already trying to form, proving what is real and designing circulation only after the connection is evidenced — not by waiting for the market to publish a task, and not by imagining a pairing then using human effort as the search algorithm.**
