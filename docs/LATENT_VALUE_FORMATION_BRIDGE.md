# Latent Value Formation — Constitutional Discovery Principle

Status: `CONSTITUTIONAL DISCOVERY PRINCIPLE / LOCKED`

Effective: 2026-09-17

Parents:
- `docs/LATENT_VALUE_DOCTRINE.md`
- `docs/STRUCTURAL_FRICTION_DISCOVERY_PRINCIPLE.md`
- `docs/LATENT_CONNECTION_DISCOVERY_PRINCIPLE.md`
- `docs/DISCOVERY_ENGINE.md`
- `docs/PSYCHOLOGY_BEHAVIOR_TRACKER.md`
- `docs/RESOURCE_ACTIVATION_THESIS.md`
- `docs/field/ROUTABLE_WORLD_NODES_2026-09-16.md`

Implementation:
- `src/latent_value_formation.py`

## 1. Why this principle exists

The repository already knows how to observe explicit demand, objective resources, actor state, underuse, psychology/behavior and complementary world nodes.

The highest-order discovery problem is not merely to find demand that already exists. It is to reason about **value that has not yet been organized into a market, product, service, job, RFQ, procurement notice or even an articulated need**.

The engine must therefore distinguish:

```text
OBJECTIVE RESOURCE EXISTS
!=
RESOURCE IS UTILIZED
!=
ACTOR RECOGNIZES ITS VALUE
!=
COMMERCIAL VALUE STRUCTURE EXISTS
!=
PAID DEMAND EXISTS
```

A resource can objectively exist while the commercial value that could later emerge from it does not yet exist as an exchange.

But the engine must not jump from `A exists + B exists` to an invented connection. The upstream question is:

> **Given what real actors objectively have, what changed and what visible costs/workarounds/behaviors appear, what product-agnostic state transition is the actor actually trying to make, what deeper structural friction prevents it, and—only after that causal layer is bounded—what complementary nodes exist elsewhere and is reality already exerting directional pressure toward a connection that current routes fail to realize?**

Only after that connection pressure is evidenced may the system ask what minimum exchange mechanics would let the value flow with less friction.

This is not demand creation by imagination. It is evidence-bound **Latent Value Formation through Latent Connection Discovery**.

```text
DEMAND DISCOVERY != LATENT VALUE FORMATION
EXPLICIT DEMAND EXECUTION != CORE LATENT VALUE FORMATION
CONNECTION INVENTION != CONNECTION DISCOVERY
```

Explicit demand remains useful downstream. It must not define the discovery identity of the system.

## 2. Canonical formation chain

```text
OBJECTIVE ENDOWMENT
        ↓
STATE / STATE CHANGE
        ↓
PERCEPTION / MOTIVE
        ↓
OBSERVED BEHAVIOR
        ↓
SURFACE PHENOMENON / SURFACE FRICTION / UNDERUSE / CONTRADICTION
        ↓
RESOURCE / STATE / PSYCHOLOGY DISEQUILIBRIUM
        ↓
COMPETING LATENT / UNFORMED OUTCOME HYPOTHESES
        ↓
RECURSIVE CAUSAL DESCENT
        ↓
COMPETING STRUCTURAL FRICTION HYPOTHESES
        ↓
DISCRIMINATING EVIDENCE / FALSIFIERS / CONTRADICTION SEARCH
        ↓
DECISION-USEFUL CAUSAL FRONTIER
        ↓
EVIDENCED STRUCTURAL FRICTION
        ↓
COMPLEMENTARY WORLD-NODE SEARCH
        ↓
CONNECTION-PRESSURE EVIDENCE
        ↓
PARTIAL FLOW / WORKAROUND / SUBSTITUTE / ADJACENT PRECEDENT
        ↓
OBSERVED MISSING EDGE
        ↓
LATENT CONNECTION HYPOTHESIS
        ↓
CONTRADICTION SEARCH
        ↓
ONLY THEN: COUNTERFACTUAL EXCHANGE MECHANICS
        ↓
CHEAPEST DECISIVE REALITY CONFIRMATION
        ↓
ONLY IF REALITY SUPPORTS IT: NEW COMMERCIAL STRUCTURE
        ↓
ONLY THEN: Need / Resource / Blocker / payer / payment projection
        ↓
ROUTING / ACCEPTANCE / SETTLEMENT / LEARNING
```

The key distinction is:

> **Demand does not have to exist first. Neither the first visible pain nor the Actor's stated request is assumed to reveal the governing structure. The system must generate competing product-agnostic outcome hypotheses, descend recursively through competing causal explanations, preserve falsifiers and discriminating evidence, and stop only at the deepest decision-useful falsifiable causal frontier. Psychology may contribute but is not mandatory. Only after structural truth is evidenced may the system formally promote complementary-node search; only after connection pressure and a distinct missing edge are evidenced may it design exchange mechanics.**

The old shorthand `COUNTERFACTUAL EXCHANGE DESIGN` remains a downstream mechanism-design operation. It no longer proves that the connection itself exists.

## 2A. Surface-to-structure causal descent

A surface friction is an evidence-bearing symptom, not the final opportunity object.

```text
SURFACE PHENOMENON
→ competing LATENT STATE TRANSITION hypotheses
→ competing STRUCTURAL FRICTION hypotheses
→ recursive deeper constraint hypotheses where warranted
→ discriminating evidence / contradiction search / falsifiers
→ explicit causal stop reason
→ EVIDENCED STRUCTURAL FRICTION
```

Keep causal truth explicit:

```text
OBSERVED
!=
INFERRED
!=
EVIDENCED_STRUCTURE
```

The engine may infer structural causes from objective state, behavior, psychology where relevant, institutional rules, technical constraints, rights/access, time/space, trust, money/time sacrifice and repeated workarounds. Inference must remain product-agnostic and falsifiable. A single plausible explanation is not enough; competing latent outcomes, competing causal explanations, bound outcome-selection evidence and discriminating evidence are required before promotion.

`STRUCTURAL FRICTION` is upstream of the later inter-node `MISSING EDGE`: the former explains the blocked Actor state transition; the latter explains why complementary nodes cannot transact or coordinate normally.

Current scan orders such as `BUYER COST FIRST` and `CURRENT EXTERNALIZED WORKAROUND FIRST` remain valid sensors, not constitutional definitions.

## 2B. Decision-useful causal frontier

The engine is not required to discover one metaphysical root cause.

Real blocked transitions may have multiple causal constraints. Causal descent stops at the deepest layer that is:
- falsifiable from observable evidence; and
- decision-relevant to what resources/interfaces/rights/trust/capabilities would have to change.

Valid stop reasons:

```text
INTERVENTION_RELEVANT_BOUNDARY
NO_DEEPER_FALSIFIABLE_LAYER
EVIDENCE_LIMIT_REACHED
MULTI_CAUSAL_FRONTIER
```

`EVIDENCE_LIMIT_REACHED` preserves UNKNOWN and cannot promote. `INTERVENTION_RELEVANT_BOUNDARY` requires both an actionable intervention implication and an explicit decision-stability assertion that deeper search would not change the next decision.

An `INFERRED` causal structure may guide exploratory node search and evidence collection. It may not become candidate truth. The executable model is `src/causal_descent.py`.

## 2C. Psychology is optional causal evidence

Psychology is important when motive, fear, autonomy, identity, trust, avoidance or aspiration materially explains behavior.

But objective industrial, technical, institutional or process evidence may establish structural friction without a psychology layer.

```text
NO PSYCHOLOGY SIGNAL != NO STRUCTURAL FRICTION
```

If psychology is used, it must be provenance-bound and behavior-corroborated.

## 3. Resource / State / Psychology Disequilibrium is a primary search zone

A primary discovery target is a mismatch between what an actor objectively possesses and what the actor's current state, behavior, psychology when relevant, environment and available routes allow those resources to become.

```text
OBJECTIVE ENDOWMENT
+
CURRENT STATE
+
ACTOR WANTS / AVOIDS / ADAPTS TOWARD A DIFFERENT STATE
+
CURRENT ROUTES FAIL TO USE THE ENDOWMENT WELL
→ RESOURCE / STATE / PSYCHOLOGY DISEQUILIBRIUM
```

Illustrative structures include:

```text
HAS MONEY
+ HAS TIME
+ SEEKS AUTONOMY / EXPERIENCE / CERTAINTY
+ CANNOT NAVIGATE TRUSTED MODERN ROUTES
→ possible unformed outcome, not a product yet
```

```text
HAS DEEP INDUSTRY EXPERIENCE
+ RETIRES FROM FULL-TIME ROLE
+ STILL VALUES CONTRIBUTION / RELEVANCE
+ DOES NOT WANT ANOTHER FULL-TIME JOB
→ potentially callable bounded expertise, if reality also shows connection pressure toward a concrete use
```

```text
HAS DIGITAL / AI EXECUTION CAPABILITY
+ HAS TIME
+ WEAK TRUST / CLIENT ACCESS / INDUSTRY CONTEXT
→ underused execution capacity, not automatically market supply or a connection
```

```text
HAS EQUIPMENT / SPACE / DATA / DISTRIBUTION
+ CURRENT UTILIZATION IS LOW
+ ADJACENT ACTORS ARE CHANGING BEHAVIOR
+ OLD PACKAGING NO LONGER FITS
→ possible new combination, not automatically a business or latent connection
```

The engine should search for the disequilibrium before inventing a product, then search for real connection-pressure evidence before inventing a route.

## 4. UNMET / UNFORMED OUTCOME

The system must not jump directly from psychology to a product idea.

It should first ask what state transition an actor appears to value but cannot currently achieve through available routes.

That is an `UNMET / UNFORMED OUTCOME HYPOTHESIS`.

Examples:

```text
CURRENT STATE
→ observable tension / contradiction
→ desired or avoided state implied by motive + behavior
→ outcome class that is not yet cleanly articulated
```

An outcome hypothesis can exist before an actor says `I want to buy X`.

But:

```text
UNFORMED OUTCOME HYPOTHESIS != DEMAND
DESIRED STATE != WILLINGNESS TO PAY
PSYCHOLOGICAL TENSION != COMMERCIAL OPPORTUNITY
UNFORMED OUTCOME != LATENT CONNECTION
```

The outcome should stay product-agnostic long enough for the system to search heterogeneous world nodes, connection pressure and alternative transformations.

## 5. Psychology & Behavior Engineering is a causal discovery input

The psychology system is not merely a complaint miner or trend-label generator.

Its deeper job is to help reconstruct an evidence-bound causal chain:

```text
WHO IS THIS ACTOR / SEGMENT?
↓
WHAT OBJECTIVE ENDOWMENTS EXIST?
↓
WHAT STATE IS THE ACTOR IN?
↓
WHAT CHANGED?
↓
HOW IS THE CHANGE PERCEIVED?
↓
WHAT MOTIVES / FEARS / ASPIRATIONS APPEAR?
↓
WHAT BEHAVIORS FOLLOW?
↓
WHAT CONTRADICTIONS APPEAR BETWEEN ENDOWMENT, MOTIVE AND BEHAVIOR?
↓
WHAT RESOURCE–PSYCHOLOGY DISEQUILIBRIUM MAY EXIST?
```

Lawful aggregate evidence may come from public/authorized social platforms, search behavior, reviews, forums, video/comment ecosystems, surveys, transaction/booking/hiring/saving/substitution/repair behavior and future source types.

Current examples such as Douyin, Zhihu, Xiaohongshu, Reddit, X or other communities are sensor instances only. They are not ontology and they do not define strategy.

The valuable signal is often not `I want to buy X`, but an actor unintentionally revealing a state transition, motive, workaround, contradiction or unused endowment.

Repeated workarounds, substitutions, referrals and informal coordination are especially valuable because they may expose **connection pressure** before a formal market category exists.

## 6. Contradiction is first-class discovery evidence

Many valuable formation hypotheses begin with a contradiction rather than a stated demand.

Examples of structural contradiction patterns:

```text
RESOURCE ↑ BUT UTILIZATION ↓
TIME ↑ BUT STRUCTURE / PURPOSE ↓
SKILL ↑ BUT CALLABILITY / TRUST ↓
CAPITAL ↑ BUT CONFIDENCE / ROUTE CERTAINTY ↓
CUSTOMER ACCESS ↑ BUT EXECUTION CAPABILITY ↓
TECHNICAL CAPABILITY ↑ BUT INDUSTRY CONTEXT / CREDIT ↓
SPACE / EQUIPMENT EXISTS BUT SCENARIO / PACKAGING IS ABSENT
ATTENTION EXISTS BUT TRANSACTION STRUCTURE IS ABSENT
```

Contradictions do not prove opportunity or connection. They identify places where the current arrangement may be leaving value unrealized.

The system should preserve contradictory evidence rather than averaging it away, because contradictions may either reveal the formation mechanism or falsify it.

## 7. Objective evidence remains independent

Psychology may not fill objective evidence gaps.

Formation-ready reasoning separately requires evidence for:

```text
OBJECTIVE_ENDOWMENT
ORIGIN_STATE
ORIGIN_CHANGE
UNDERUSE_MISALIGNMENT
OBSERVED_BEHAVIOR
COMPLEMENTARY_NODE
CONNECTION_PRESSURE
STRANDING_BARRIER
```

`CONNECTION_PRESSURE` is the explicit bridge between plausible complementarity and a reality-grounded latent connection. It may be evidenced by repeated workarounds, partial/informal flows, failed attempts, substitutions, referrals, shared causal pressure, adjacent/historical analogues or other attributable observations showing that value is already trying to cross the boundary.

A viral narrative about retirees, graduates, parents, merchants, enterprises or another group cannot manufacture an endowment, underuse state, complementary resource or connection pressure.

Likewise:

```text
OBJECTIVE RESOURCE != COMMERCIAL VALUE
RESOURCE EXISTS != RESOURCE IS UNDERUSED
UNDERUSED != AVAILABLE
AVAILABLE != OPTIONED
COMPLEMENTARITY != LATENT_CONNECTION
CONNECTION_HYPOTHESIS != CONNECTION_PRESSURE_EVIDENCE
```

These truths remain independent axes.

## 8. Psychology boundaries remain absolute

Psychology can help explain the direction of a state transition:

```text
STATE CHANGE
→ changed perception
→ changed motive
→ observed adaptation behavior
```

It can help infer why an objectively available resource is not being used in the old way and what classes of outcomes may become newly valued.

It cannot prove demand or a connection.

```text
PSYCHOLOGY SIGNAL != DEMAND
MOTIVE HYPOTHESIS != WILLINGNESS TO PAY
BEHAVIOR SIGNAL != TRANSACTION
SOCIAL SALIENCE != POPULATION SHARE
PSYCHOLOGY STORY != CONNECTION PRESSURE
INFERENCE != FACT
```

`PsychologySnapshot` evidence must retain provenance from the canonical tracker. Before a formation becomes `VALIDATION_READY`, psychology must be tied to the same actor segment and have behavior corroboration. Money corroboration strengthens the hypothesis but is not required merely to decide that a cheap bounded validation is worthwhile.

## 9. Complementary world nodes are heterogeneous

The system does not search only for another person or supplier.

A complementary node may be a:

```text
PERSON
GROUP / COMMUNITY
ORGANIZATION / INSTITUTION
PHYSICAL ASSET / SPACE / EQUIPMENT
CAPABILITY / PROCESS
CHANNEL / NETWORK
DATA / INFORMATION SOURCE
CAPITAL / BUDGET
AUTHORITY / ACCESS RIGHT
SOFTWARE / AI / API
TRUST / REPUTATION RELATIONSHIP
DEMAND / EVENT FLOW
CONTRACT / RULE / STANDARD
```

The node taxonomy stays open. The important fields are the node's observed state, possible contribution, owner/controller, permission boundary and evidence lineage.

The engine should search across node types because value may emerge only from a combination that no participant currently describes as a product category.

But node existence and complementarity are only search-space reduction:

```text
A CAN HELP B
!=
REALITY IS ALREADY PUSHING A AND B TOWARD EXCHANGE
```

Only the second claim may support latent-connection promotion.

## 10. Latent Connection Discovery precedes Counterfactual Exchange Mechanics

The central upstream question is:

> **What evidence shows that currently separate real-world nodes are already being pushed toward the same value flow, while an observed missing edge prevents that flow from becoming normal?**

Useful evidence includes repeated manual workarounds, informal exchange, failed cross-boundary attempts, substitution, referral behavior, existing expensive routes and adjacent/historical structures.

Only after that question has evidence may the engine ask:

> **Given this evidenced latent connection, what minimum roles, incentives, permissions, trust, acceptance and settlement mechanics would reduce the friction?**

That downstream operation is the repository's historical `Counterfactual Exchange Design`.

```text
LATENT_CONNECTION_DISCOVERY
PRECEDES
COUNTERFACTUAL_EXCHANGE_DESIGN

COUNTERFACTUAL_EXCHANGE_DESIGN
!=
LATENT_CONNECTION_EVIDENCE

COUNTERFACTUAL EXCHANGE
!=
ACCEPTED EXCHANGE
```

The mechanism design should explain:
- what observed connection pressure it serves;
- what state would change;
- which nodes contribute what;
- what the origin actor gains;
- what complementary nodes gain;
- what observed missing edge blocks the relationship today;
- which permissions/controllers matter;
- what value the orchestrator adds beyond introduction;
- what single cheapest experiment can kill or support the remaining uncertainty.

A mechanism may be novel even when the underlying relationship pressure is discovered rather than invented.

## 11. Maturity states

```text
OBSERVED_TRANSITION
→ RESOURCE_PSYCHOLOGY_MISALIGNMENT_HYPOTHESIS
→ LATENT_VALUE_FORMATION_HYPOTHESIS
→ COMPLEMENTARITY_HYPOTHESIS
→ VALIDATION_READY
```

### `OBSERVED_TRANSITION`
A state change or psychology signal is visible, but objective resource/state evidence or psychology linkage is incomplete.

### `RESOURCE_PSYCHOLOGY_MISALIGNMENT_HYPOTHESIS`
Objective endowments/state/change and a perception/motive signal coexist, but underuse or behavior linkage is not yet strong enough.

### `LATENT_VALUE_FORMATION_HYPOTHESIS`
Underuse/misalignment and observed behavior are evidenced; an unmet/unformed outcome can be stated without claiming a market exists.

### `COMPLEMENTARITY_HYPOTHESIS`
One or more evidenced world nodes could plausibly change the state, and minimum exchange mechanics may be describable, but **connection-pressure evidence, barrier truth or contradiction resolution is still incomplete**.

### `VALIDATION_READY`
All formation evidence dimensions are present, including explicit `CONNECTION_PRESSURE`; psychology is behavior-corroborated; complementary nodes are evidenced; the stranding barrier is observed; and no material unresolved contradiction remains.

It means only:

> reality already provides enough directional evidence to justify spending scarce human/external validation capital on the remaining decisive uncertainty.

It does **not** mean payer, paid need, resource control, route testability, profitability or scale.

## 12. Example — retirement transition × young digital capacity

This is an **illustrative hypothesis**, not a canonical opportunity and not a fixed target market.

One origin segment may contain:
- newly available time;
- pension/savings for some segments;
- decades of professional/life experience;
- a retirement-driven change in schedule, identity and social structure.

Psychology/behavior sensing may observe:
- desire for autonomy, experience, relevance or connection;
- learning, travel, interest-group, digital-tool or selective continued-work behavior;
- contradictions between objective resources and available ways to use them.

Another segment may contain:
- time;
- digital/AI execution capability;
- adaptability to new tools;
- weak client access, industry context, capital or trust.

Complementary nodes may also include trusted communities/institutions, spaces, software/payment infrastructure, SMEs needing bounded judgment, existing service channels or future nodes not yet named.

None of that proves that these nodes should be connected.

Before field validation, the system must find evidence such as repeated informal cross-generation help, referrals, existing paid/unpaid substitutes, repeated attempts, adjacent precedents or other real behavior showing the relationship is already trying to form.

The correct next question is not:

> Should we build a senior-training app?

Nor is it:

> Could we connect seniors and young digital workers?

It is:

> **What is reality already making these actors do around the missing connection, and which observed edge prevents that behavior from becoming an accepted value flow?**

Possible formations can then be killed or strengthened independently.

## 13. Projection to transaction truth happens later

`src/latent_value_formation.py` may project a `VALIDATION_READY` formation into the existing canonical `LatentValueCandidate` model.

The projection stays:

```text
source_mode = LATENT_VALUE_DISCOVERY
```

It does not create:
- `NeedSignal`;
- payer truth;
- payment evidence;
- `ResourceSignal` control/availability;
- `BlockerSignal` transaction scope;
- `ROUTE_TESTABLE` status.

Those must still be proven through the Resource Imbalance and transaction layers.

This ordering is mandatory:

```text
VALUE FORMATION REASONING
→ LATENT CONNECTION PRESSURE
→ MINIMUM EXCHANGE MECHANICS
→ CHEAP REALITY CONFIRMATION
→ EVIDENCE PROJECTION
→ FAIL-CLOSED TRANSACTION VALIDATION
→ ORCHESTRATION
```

not:

```text
PLAUSIBLE COMBINATION
→ HUMAN OUTREACH AS SEARCH
→ CALL IT DISCOVERY
```

and not:

```text
EXPLICIT DEMAND FEED
→ CALL IT THE CORE BUSINESS
```

## 14. Privacy, dignity and anti-manipulation boundary

The formation engine uses aggregate/segment evidence and non-sensitive actor-state observations where possible.

Do not:
- build unnecessary individual psychographic dossiers;
- infer sensitive personal traits;
- target vulnerable people through hidden manipulation;
- exploit unemployment, aging, loneliness or financial pressure;
- manufacture fear or artificial scarcity to make a hypothesis true;
- treat people as inert inventory.

People remain `ACTOR`s. Their time, knowledge, capability, trust and access may participate in value formation only under explicit voluntary terms.

## 15. Human validation is scarce capital

Founder time, field visits, phone calls, trusted introductions and counterpart attention are scarce resources.

The system must use broad sensing and cross-source evidence to eliminate weak connection stories before external contact.

Preferred sequence:

```text
SENSING
→ CONNECTION PRESSURE
→ CONTRADICTION / MISSING-EDGE CHECK
→ RANKED LATENT CONNECTION
→ SINGLE DECISIVE UNKNOWN
→ TARGETED HUMAN / FIELD CONFIRMATION
```

A field probe should recover a recent concrete event, workaround, failed attempt, cost, authority boundary or commitment signal. It should not ask a person to validate an abstract solution story.

## 16. Governing invariants

```text
OBJECTIVE RESOURCE EXISTS != COMMERCIAL VALUE EXISTS
DEMAND DISCOVERY != LATENT VALUE FORMATION
INFERENCE != FACT
PSYCHOLOGY HYPOTHESIS != DEMAND
CONNECTION INVENTION != CONNECTION DISCOVERY
COMPLEMENTARITY != LATENT CONNECTION
CONNECTION HYPOTHESIS != CONNECTION PRESSURE EVIDENCE
MISSING EDGE HYPOTHESIS != OBSERVED MISSING EDGE
COUNTERFACTUAL EXCHANGE != LATENT CONNECTION EVIDENCE
LATENT CONNECTION != ACCEPTED EXCHANGE
HUMAN OUTREACH != PRIMARY DISCOVERY SENSOR
DEMAND != WILLINGNESS TO PAY
WILLINGNESS TO PAY != TRANSACTION
LATENT VALUE FORMATION != COMMERCIAL OPPORTUNITY
UNKNOWN != PASS
```

> **不是先由我们想象 A 和 B 应该怎样连接，再让人去现实里替这个想法找证据。系统先观察 Actor 客观拥有什么、状态怎样变化、真实行为怎样偏移、哪些资源被阻塞，以及现实是否已经通过绕行、替代、局部交换、重复尝试和共同压力留下了“连接正在形成”的痕迹。只有这些痕迹收敛成 Connection Pressure，才允许设计最小交换机制，并把人的时间、信誉和现场行动用于最后一个关键未知量。不是创造一条漂亮的路，再问现实愿不愿意走；而是先发现现实已经踩出来的小径，再决定是否值得把它变成路。**

Legacy `STRANDING_BARRIER` is accepted only at compatibility boundaries and is normalized to canonical `MISSING_EDGE`; new canonical records must use `MISSING_EDGE`.
