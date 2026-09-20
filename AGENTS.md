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
→ RESOURCE / STATE / PSYCHOLOGY DISEQUILIBRIUM
→ COMPETING LATENT / UNFORMED OUTCOME HYPOTHESES
→ RECURSIVE CAUSAL DESCENT
→ COMPETING STRUCTURAL FRICTION HYPOTHESES
→ DISCRIMINATING EVIDENCE + FALSIFIERS + CONTRADICTION SEARCH
→ DECISION-USEFUL CAUSAL FRONTIER
→ EVIDENCED STRUCTURAL FRICTION
→ COMPLEMENTARY WORLD NODES
→ CONNECTION-PRESSURE EVIDENCE
→ PARTIAL FLOW / WORKAROUND / SUBSTITUTE / ADJACENT PRECEDENT
→ OBSERVED MISSING EDGE BETWEEN NODES
→ LATENT CONNECTION HYPOTHESIS
→ CONTRADICTION SEARCH
→ ONLY THEN: COUNTERFACTUAL EXCHANGE MECHANICS
→ CHEAP BOUNDED REALITY CONFIRMATION
→ ONLY IF SUPPORTED: NEED / RESOURCE / BLOCKER / PAYER PROJECTION
→ ROUTING / ACCEPTANCE / SETTLEMENT
→ REPEAT / LEARNING / BETTER ALLOCATION
```

The key rule is:

> **Demand does not have to exist first, and neither the first visible friction nor the Actor's stated request is assumed to reveal the governing structure. Treat surface pain as a sensor. Generate competing product-agnostic outcome hypotheses, descend recursively through competing causal explanations, require discriminating evidence and falsifiers, and stop only at the deepest decision-useful falsifiable causal frontier. Psychology is one sensor, not a universal gate. Only after structural truth and downstream connection truth are evidence-bound may the system design minimum exchange mechanics.**

`NeedSignal`, `ResourceSignal` and `BlockerSignal` are downstream fail-closed evidence projections. They must not shrink the engine into an explicit demand-matching system.

Optimize for **truthful value formation + discovered latent connections + recurring accepted outcomes + delegatability + regenerative circulation + normalized orchestration economics**, not code volume, lead count, explicit-demand count, founder activity or narrative appeal.

**Code serves the doctrine. The doctrine does not bend to the convenience of code, a website, an API, an explicit-demand feed, a current candidate or a source schema.**

## Reality-first adaptive cognition — LOCKED

Preserve this ordering:

```text
REALITY > COGNITION > SCHEMA
```

Discovery is allowed to behave like an adaptive flow rather than a railroad. It may enter through any evidence-bearing layer, branch, revisit earlier interpretations, infer backward from a downstream anomaly, merge causal paths, discover new Actors late, or replace an earlier frame when evidence changes.

Schemas, validators, state machines and canonical chains exist to prevent unsupported claims from being promoted as truth and to make reasoning auditable. They must not force reality into a preselected sequence.

Do not use fixed hypothesis counts as a substitute for causal rigor. Actively search for material alternatives where ambiguity exists and preserve them when found. If no credible alternative survives honest search, do not fabricate one merely to satisfy a schema.

When reviewing or adding a rule, ask:

> **Does this rule prevent false promotion, or does it merely suppress exploration?**

Strengthen the former. Default to weakening, moving downstream or removing the latter.

State-machine labels describe epistemic maturity; they are not a mandatory traversal order. Discovery may be nonlinear. Causal depth labels are also descriptive: preserve valid parent/child direction, but never invent intermediate layers to force contiguous numbering. Promotion must still be evidence-bound, falsifiable, contradiction-aware and fail-closed.

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
13. `docs/OPPORTUNITY_ATTRACTION_FIELD.md`
14. `docs/OPPORTUNITY_SCORECARD.md`
15. `docs/ARCHITECTURE.md`
16. current `docs/research/`, `docs/field/` and `docs/launch/` files relevant to the task.

`docs/LATENT_VALUE_DOCTRINE.md` is constitutional. `docs/STRUCTURAL_FRICTION_DISCOVERY_PRINCIPLE.md`, `docs/LATENT_CONNECTION_DISCOVERY_PRINCIPLE.md` and `docs/LATENT_VALUE_FORMATION_BRIDGE.md` are also locked constitutional discovery principles. `docs/OPPORTUNITY_ATTRACTION_FIELD.md` is the locked strategic discovery/attention principle for participant pull, operator activation and anti-drift. If another document, implementation or workflow conflicts with them, the lower-level artifact must change.

There is no inherited commercial opportunity layer. The active case epoch is `ATTRACTION_FIELD_V1` from the 2026-09-19 reset. Pre-reset cases are Git-history-only and must not be revived as current inputs.

When a major assumption changes, update `docs/FORMAL_TRUTH.md` in the same change.

## Commercial case epoch reset — LOCKED

The active commercial case space was reset on **2026-09-19** into epoch `ATTRACTION_FIELD_V1`.

This is stronger than demotion or watchlist status.

```text
PRE-RESET CASE != ACTIVE INPUT
GIT HISTORY != CANDIDATE POOL
CLOSED HISTORICAL ISSUE != FALLBACK ROUTE
DELETED CASE ARTIFACT != PRIOR
OLD SCORE != CURRENT EVIDENCE
OLD SCAN PARENTAGE != NEW SCAN PARENTAGE
```

Rules:
- all commercial cases, field scans, launch cards, result packets and candidate ledgers deleted by the reset are audit history only;
- do not restore, inherit, compare against, descend from or reopen a deleted pre-reset case merely because Git history, a commit, an old Issue or an old conversation still mentions it;
- no pre-reset candidate has watchlist, parent, prior, benchmark or fallback status;
- a formerly explored structure may appear again only if **current broad-reality sensing independently rediscovers it** under the current doctrine; in that event it is a new formation with new evidence, not a revived case;
- new commercial scan numbering starts at `ATTRACTION_SCAN_001`;
- `data/commercial_reset_state.json` is the machine-readable active case epoch;
- reusable engine code, source adapters, evidence schemas and truth rules survive the reset because they are capabilities, not commercial cases.

The reset must not be reversed to make continuation easier.

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
- `LATENT OUTCOME HYPOTHESIS != EVIDENCED LATENT OUTCOME`.
- Material latent-outcome alternatives must be preserved when reality supports them; never fabricate alternatives to satisfy a fixed count. Bound selection evidence is required before causal promotion.
- `OBSERVED COST != ROOT CAUSE`.
- `ONE PLAUSIBLE EXPLANATION != STRUCTURAL TRUTH`.
- `DEEPER STORY != DEEPER TRUTH`.
- `PSYCHOLOGY EVIDENCE != UNIVERSAL FORMATION GATE`.
- `STRUCTURAL FRICTION HYPOTHESIS != EVIDENCED STRUCTURAL FRICTION`.
- `STRUCTURAL FRICTION != MISSING EDGE`.
- `INTERVENTION_RELEVANT_BOUNDARY` requires a written rationale, actionable implication and explicit decision stability; enum-only stops are invalid.
- Legacy `STRANDING_BARRIER` is compatibility-only and normalizes to canonical `MISSING_EDGE`.
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

## Regenerative formation search rule — LOCKED

Do not begin opportunity discovery from an explicit job, gig, RFQ, marketplace task, buyer brief, quoted budget, provider price or visible transaction spread.

Those are downstream transaction observations. They may validate or falsify an independently discovered formation later, but they must not define the upstream search space.

Preferred discovery object:

```text
LARGE / REPLENISHING ACTOR POPULATION A
+ DURABLE ENDOWMENT / STATE DISEQUILIBRIUM A
+ LARGE / REPLENISHING COMPLEMENTARY NODE POPULATION B
+ DURABLE ENDOWMENT / STATE DISEQUILIBRIUM B
+ REPEATED CONNECTION PRESSURE
+ PARTIAL / INFORMAL / EXPENSIVE / FAILED FLOW
+ RECURRING MISSING EDGE
+ RECURRING EVENT SOURCE / DEMAND PUMP
→ POSSIBLE REGENERATIVE VALUE FIELD
```

The engine should look for **potential-energy gradients** that persist before a market category is fully formed. A valid search zone should usually involve large or replenishing actor/resource populations, repeated state transitions, persistent underuse/mismatch and evidence that value is already trying to cross the boundary through workarounds, referrals, substitutes, internal coordination, expensive legacy routes or other partial flows.

Before treating a formation as commercially interesting, explicitly ask:
- what keeps replenishing Actor/Node A?
- what keeps replenishing Actor/Node B?
- what recurring event keeps regenerating the pressure?
- what partial flow proves reality is already trying to connect them?
- what missing edge repeatedly prevents normal circulation?
- can that edge be standardized without making the founder the permanent provider?
- does successful routing create trust/data/coverage that makes the next routing better?
- is the field broad enough that a single observed transaction is merely one manifestation?

Hard boundaries:

```text
EXPLICIT TASK != DISCOVERY SEED
ONE LIVE TRANSACTION != DEMAND PUMP
PRICE SPREAD != LATENT CONNECTION
BUYER BUDGET != FORMATION EVIDENCE
PROVIDER QUOTE != CONNECTION PRESSURE
RECURRING FOUNDER SEARCH != REGENERATIVE DEMAND
```

The target hierarchy is:

```text
Observation
→ Pattern
→ Opportunity Archetype
→ Regenerative Loop
→ Business System
```

A one-off task may later buy validation evidence, but it cannot become the core discovery object until the underlying regenerative field has been independently evidenced.

## Scientific engineering method selection — LOCKED

Use mature data structures, algorithms, design patterns, statistical methods and mathematical models when they encode a real repository invariant or materially improve a real decision.

Do not cargo-cult sophistication.

Required method-selection chain:

```text
REAL PROBLEM
→ EXPLICIT INVARIANT / DECISION FAILURE
→ METHOD WITH MATCHING ASSUMPTIONS
→ EXECUTABLE IMPLEMENTATION
→ TESTABLE DECISION IMPROVEMENT
→ KEEP / REVISE / REMOVE
```

Before introducing a non-trivial method, state:
- the concrete problem;
- the invariant it must preserve;
- why the method matches that problem;
- its assumptions;
- its failure mode;
- the observable benefit;
- why its complexity is justified now;
- what measured condition would justify replacing it with something more complex.

Current justified attraction method:
- hard `HIGH_ATTRACTION_BEACON` floor first;
- Pareto / non-dominated sorting second via `src/attraction_frontier.py`;
- no weighted total score may override a weak critical attraction dimension.

For current Scan-scale candidate counts, transparent `O(n^2)` Pareto comparison is preferred over more complex skyline/index structures. Complexity may increase only after measured scale makes this a real bottleneck.

```text
ALGORITHM != TRUTH
MODEL != REALITY
SCORE != VALUE
COMPLEXITY != RIGOR
SIMPLE METHOD + CORRECT INVARIANTS > FANCY METHOD + WRONG ASSUMPTIONS
```

## Attraction-first discovery order — LOCKED

Attraction is the **first attention-allocation premise**, not a late score applied after
the engine has already spent most of its effort on a weak formation.

The discovery order is:

```text
BROAD CURRENT REALITY
→ ATTRACTION SIGNAL HARVEST
→ HIGH-ATTRACTION BEACONS
   (bilateral voluntary motion
    + large state-dependent value jump
    + decision window still movable
    + narrow bridge / disproportionate unlock
    + low explanation/activation burden
    + operator control without recurring labor
    + plausible self-propulsion)
→ ONLY THEN DEEP CAUSAL DESCENT
→ COMPLEMENTARY NODES
→ CONNECTION PRESSURE
→ MISSING EDGE
→ TRUTH / INCUMBENT / CONTRADICTION TESTS
→ CHEAP REALITY CONFIRMATION
```

Use `src/attraction_discovery.py` as the canonical pre-formation discovery beacon. When multiple signals pass that hard floor, use `src/attraction_frontier.py` to compute the non-dominated attention frontier before selecting deep-dive order.

Rules:
- attraction decides **where to look first**;
- evidence decides **what may be believed**;
- do not collect every observable friction and hope scoring later will rescue focus;
- low-attraction reality can remain research context but must not consume scarce founder
  attention or external validation merely because it is true;
- no dimension may be averaged away: a dead A side, dead B side, locked decision
  window, weak value jump, high explanation burden or recurring founder labor kills
  current high-attraction status;
- prefer non-obvious connections that feel obvious after explanation because a small
  bridge releases a large, immediately legible state change;
- `HIGH_ATTRACTION_BEACON != COMMERCIAL_VALIDATION`.

## Attraction-field and anti-drift rule — LOCKED

The engine must not reward a merely plausible connection that requires everyone to be pushed.

For every retained formation, separately establish:
- **A-side attraction**: why the resource/endowment actor wants to move now, with behavior evidence;
- **B-side attraction**: why the complementary/outcome actor wants the reachable result now, with behavior evidence;
- **operator attraction**: why the operator actively wants to own the bridge rather than merely perform or sell a job;
- **activation friction**: what persuasion, permission, trust, integration, capital or behavior change still stands between the actors;
- **self-propulsion**: why successful routing makes the next flow easier rather than recreating founder labor.

Operator attraction is a strategic attention signal, never a substitute for market evidence.

Use these rules:

```text
FOUNDER EXCITEMENT != PARTICIPANT PULL
EXISTING ACTOR != FLOW SOLVED
INCUMBENT PRESENCE != AUTOMATIC KILL
BROAD REALITY > CURRENT SEARCH LENS
SEARCH LENS != ONTOLOGY
INDUSTRIAL B2B != DEFAULT WORLD
TRANSFERABLE OBJECTIVE STRANDED UNIT != TOTAL COMMERCIAL WORLD MODEL
```

## Value-chain leverage / intervention timing rule — LOCKED

A formation may contain real friction and still be strategically unattractive because the intervention sits after most value has already been allocated.

Before spending scarce human/external validation capital, explicitly classify:
- `INTERVENTION_STAGE`: discovery / pre-commitment / commitment / execution / closeout / post-transaction;
- `DECISION_MOBILITY`: are budget, vendor, scope, resource allocation or transaction terms still open, partially movable or locked?
- `ECONOMIC_PROXIMITY`: does the bridge directly affect revenue/budget, material cost/risk, transaction enablement, or merely process quality?
- `ABSENCE_CONSEQUENCE`: without the bridge, is the transaction blocked, is material value lost, is there only delay/rework, or merely minor friction?
- `PARTICIPANT_PULL`: what behavior shows that participants want this state change rather than the analyst merely observing an imperfection?

Use `src/attraction_leverage.py` as the canonical categorical gate before external validation.

```text
REAL FRICTION != ATTRACTIVE POSITION
LATE-STAGE PROCESS IMPROVEMENT != COMMERCIAL LEVERAGE
VALUE ALREADY ALLOCATED + DECISIONS LOCKED -> DEFAULT DEMOTION
```

Closeout/post-transaction opportunities are not automatically forbidden, but they survive only when the layer still controls payment/value release, prevents material economic loss/risk, satisfies a hard compliance/safety boundary, or determines whether the transaction can complete.

Do not spend founder/outreach capital merely because a process can be improved.

A white-portfolio scan must reopen broad reality rather than recursively inherit the previous candidate's industry, asset type or search lens. Deliberately counter-sample outside the prior vertical when the evidence allows it. Do not impose a fixed category quota or fabricate weak directions merely to appear broad.

Every retained formation must include the Attraction Brief defined in `docs/OPPORTUNITY_ATTRACTION_FIELD.md`. Every white-portfolio scan must include a Drift Audit covering vertical lock-in, search-lens lock-in, industrial/inventory/professional-service over-selection, incumbent auto-kill and analyst-story attraction.

A high-attraction structure should make the participant surplus legible and voluntary: A wants to release/activate something, B wants to obtain the outcome, and the operator wants to control the bridge without carrying recurring delivery. Attraction guides attention; evidence gates promotion.

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
→ RESOURCE / STATE / PSYCHOLOGY DISEQUILIBRIUM
→ COMPETING LATENT / UNFORMED OUTCOME HYPOTHESES
→ RECURSIVE CAUSAL DESCENT
→ COMPETING STRUCTURAL FRICTION HYPOTHESES
→ DISCRIMINATING EVIDENCE / FALSIFIERS / CONTRADICTION SEARCH
→ DECISION-USEFUL CAUSAL FRONTIER
→ EVIDENCED STRUCTURAL FRICTION
→ COMPLEMENTARY WORLD-NODE SEARCH
→ CONNECTION-PRESSURE EVIDENCE
→ PARTIAL FLOW / WORKAROUND / SUBSTITUTE / ADJACENT PRECEDENT
→ OBSERVED MISSING EDGE BETWEEN NODES
→ LATENT CONNECTION HYPOTHESIS
→ MINIMUM COUNTERFACTUAL EXCHANGE MECHANICS
→ CHEAP REALITY CONFIRMATION
```

The engine must search for what actors may not know about themselves: hidden capability, hidden deficit, underused relationships, changed resource meaning, packaging gaps, coordination gaps, unrealized exchange structures and outcomes that have not yet become product categories.

It must also search for what **reality is already trying to connect**: repeated workarounds, informal exchange, failed cross-boundary attempts, substitution, referrals, expensive legacy routes and shared state changes that expose directional pressure.

Psychology signals, when used, must be tied to the same actor segment and corroborated with behavior before they can materially raise a formation hypothesis. Psychology is not mandatory when objective state/process/technical/institutional evidence already supports the causal structure. Money evidence strengthens commercial relevance, but money is not required merely to form a bounded hypothesis worth testing.

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

Recent change is not a universal gate. Persistent observable mismatch may enter causal descent when actor state, behavior, endowment and friction are evidence-bound.

```text
NO RECENT CHANGE != NO STRUCTURAL FRICTION
```

## Causal descent v2 rule — LOCKED

For every material surface signal, the engine must preserve a falsifiable causal chain rather than jump directly from symptom to product.

```text
SURFACE SIGNAL
→ competing LATENT OUTCOME hypotheses
→ competing STRUCTURAL CONSTRAINT hypotheses
→ deeper child constraints where warranted
→ discriminating evidence / contradictions / falsifiers
→ explicit causal stop reason
→ EVIDENCED STRUCTURAL FRICTION
```

Do not assume a single root cause. The accepted frontier may be multi-causal.

Every selected latent outcome requires an evidence-bound selection rationale. Every causal stop requires a written stop rationale; a stop-reason enum by itself is not enough. Do not force psychology, observed behavior or a recent change when objective technical/institutional/process/state evidence already supports the causal structure.

Valid stop reasons are:
- `INTERVENTION_RELEVANT_BOUNDARY`;
- `NO_DEEPER_FALSIFIABLE_LAYER`;
- `EVIDENCE_LIMIT_REACHED`;
- `MULTI_CAUSAL_FRONTIER`.

`EVIDENCE_LIMIT_REACHED` preserves UNKNOWN and cannot promote.

An inferred structural hypothesis may guide **exploratory** complementary-node search, analogue search and discriminating evidence collection. It may not promote a candidate or justify exchange design.

Psychology/perception/motive evidence is optional when objective behavior, state, institutional, technical or process evidence is sufficient. If psychology is used, it must be provenance-bound and behavior-corroborated.

The canonical implementation is `src/causal_descent.py`. Do not bypass it by stuffing a deeper-sounding sentence into a generic `friction` field.

### Causal lineage persistence — LOCKED

A causal record id, root-cause label or prose summary is not evidence. Any formation/candidate that claims `EVIDENCED_STRUCTURE` must carry the inspectable structured causal lineage, and every support/contradiction/discriminating reference in that lineage must bind to evidence in the same durable evidence packet.

```text
CAUSAL RECORD ID != CAUSAL EVIDENCE
UNBOUND CAUSAL EVIDENCE REF != EVIDENCE
DENORMALIZED CAUSAL SUMMARY MUST MATCH CANONICAL CAUSAL LINEAGE
```

Persisted JSON and generated artifacts must fail closed if the structured lineage is missing, malformed, evidence-unbound or inconsistent with the projected Actor/current-state/surface/outcome/structural-friction summaries.

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

There is currently **no active commercial candidate, transaction unit, inherited parent formation, watchlist fallback or launch route**.

The commercial case layer was intentionally cleared on 2026-09-19. Historical field scans, old Xuzhou/industrial/consumer/eldercare candidates, prior launch cards and old result packets are not current evidence inputs. They remain recoverable through Git history for audit only.

The current formation capability exists in `src/latent_value_formation.py`. `VALIDATION_READY` requires explicit `CONNECTION_PRESSURE` evidence, but scarce external validation additionally requires the value-chain leverage gate in `src/attraction_leverage.py`. `ATTRACTION_SCAN_003-F1` was demoted on 2026-09-20 for weak downstream leverage. The next empirical task is a genuinely fresh `ATTRACTION_SCAN_004`.

Current priorities:
1. begin from broad current reality, not an inherited vertical or historical candidate;
2. observe objective endowments, actor state/state-change, psychology/behavior where relevant and real workarounds/partial flows;
3. generate competing product-agnostic outcome and structural-friction hypotheses;
4. descend causally and preserve contradictions/falsifiers;
5. search heterogeneous complementary nodes only after structural truth is credible;
6. discover `CONNECTION_PRESSURE` and an observed missing edge;
7. require an Attraction Brief with separately evidenced A-side pull and B-side pull plus explicit operator strategic attraction;
8. require the value-chain leverage / intervention-timing gate before spending external validation capital;
9. run a Drift Audit before retaining any formation;
10. treat incumbent presence as evidence about flow resolution, not automatic rejection;
11. use human/external validation only on the decisive remaining unknown after leverage survives;
12. keep the founder as orchestration/routing control plane rather than default search, sales or execution node.

Do not resume any old launch, candidate, scan family or Issue as a fallback. If a similar structure is independently rediscovered, treat it as a new case in the new epoch.

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

## Durable web-session checkpoint branch — LOCKED

For ChatGPT Plus web sessions and any other long-running agent session that can stall or disappear, use `docs/WEB_SESSION_RECOVERY.md`.

- The permanent recovery branch is `state/chatgpt-recovery`; `RECOVERY_STATE.json` is a static bootstrap manifest and volatile task checkpoints live at `recovery/tasks/<task_key>.json`.
- Recovery precedence is: live GitHub refs/PRs/Actions/artifacts/persisted data > recovery checkpoint > `TASK_STATE.md` > chat history.
- Recovery is **control-plane only**. Business/runtime code and production workflows must not read, wait on or depend on the recovery state. Runtime latency tax must remain zero.
- Checkpoint size is adaptive: checkpoint on long waits, non-idempotent/ambiguous side effects, merge/production verification, stage identity changes, roughly >8 minutes of redo risk, or several durable conclusions. Do not checkpoint reads, polling, every tool call or transient reasoning.
- Coalesce safe, discoverable GitHub steps into one checkpoint before the next long wait rather than producing one commit per micro-step.
- Checkpoint commits live only on the state branch and must use `[skip ci] recovery:` commit messages. The state branch is never opened as a PR or merged into `main`.
- Recovery-only PRs must complete their PR-head checks before merge; then the merge/squash commit should include `[skip ci]` so the control-plane-only integration does not launch duplicate main-push CI, scans, tagging or production workflows. Never apply this shortcut to business/runtime changes.
- Each task-checkpoint blob SHA plus monotonically increasing `generation` is the writer fence. Different tasks use different files; same-task workers must CAS the same file and a losing worker must stop mutating. On a CAS/SHA conflict, the losing worker must stop mutating, re-read live GitHub and reacquire state; never force-overwrite.
- Before any non-idempotent external action, persist a `pending_operation` write-ahead intent. If the outcome becomes ambiguous, reconcile provider-side evidence before retrying; never blindly repeat payments, outreach, submissions or other irreversible actions.
- If GitHub proves that a commit, PR, CI result, merge, production run or artifact already exists, consume that evidence and continue from the first unfinished stage.
- On every resume, classify the volatile checkpoint as `FRESH`, `STALE`, or `CONFLICTED` against live GitHub before mutating anything; reconcile stale state forward and stop on unresolved conflicts.
- On resume, list `recovery/tasks/` and match task identity to live branch/PR/mission. Never let one active task overwrite or absorb another task's checkpoint.
- If recovery storage is unavailable, existing business execution continues unaffected. Read-only work may continue; unsafe non-idempotent mutations pause until durable intent/reconciliation is possible.
- Recovery state is bounded and secret-free: schema v2, <=16 KiB, compact references instead of logs/transcripts, no credentials, sensitive tokens, private customer/user PII or unpublished sensitive business content.
- If the state file is corrupt, recover the newest valid state-branch revision and reconcile with live GitHub; if the branch is missing, recreate from live repository truth rather than chat memory.
- `TASK_STATE.md` remains the stable mission handoff; the recovery-state branch is the volatile execution cursor. Neither may override live GitHub truth.

