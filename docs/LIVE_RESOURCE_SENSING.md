# Live Resource Sensing — Signal-to-Capability Architecture

Status: `CANONICAL DISCOVERY SUBSYSTEM`

Effective: 2026-09-13

Constitutional parent: `docs/LATENT_VALUE_DOCTRINE.md`.

## 1. Purpose

The world is not a static supplier catalog. Actor state, time, willingness, asset use, relationships, location, skills, attention and constraints change continuously.

The system therefore needs a **live sensor layer** that repeatedly observes public reality and asks:

> What does this new behavior reveal about capabilities, surplus, deficits, constraints or newly callable value?

The objective is not to collect more listings. It is to convert fresh observations into evidence-linked, low-level capability hypotheses that can later participate in latent-value discovery and resource composition.

## 2. Sensor is not ontology

A platform, website, API, social network, marketplace, public notice, field observation or document is a **sensor**.

It must never define what a resource is.

```text
Xianyu / Xiaohongshu / Douyin / Zhihu / jobs / public notices / field agents / APIs
                                  ↓
                           SIGNAL OBSERVATIONS
                                  ↓
                            OBSERVED FACTS
                                  ↓
                      ACTOR / STATE / CHANGE
                                  ↓
                      LOW-LEVEL CAPABILITIES
                                  ↓
                     LATENT AFFORDANCE HYPOTHESES
                                  ↓
                    COMPLEMENTARITY / COMPOSITION
```

If one platform disappears, the world model must remain intact.

## 3. Resource discovery must not use a closed category list

Known categories such as expert, professor, machine, factory, institution, distributor or student are useful labels but are not the resource ontology.

The engine must not be limited to a fixed enum of resource types.

A capability key is an **open namespace**. Examples:

```text
presence.local_execution
mobility.local
evidence.capture.photo_video
communication.basic_interview
knowledge.mechanical_fault_diagnosis
trust.local_reputation
access.enterprise_installed_base
space.short_term_storage
time.flexible_paid_task
```

Tomorrow the engine may discover a capability atom that does not exist today. Adding that atom must not require redefining the business architecture.

Taxonomies may be built for search and aggregation, but taxonomy is an index, not a discovery boundary.

## 4. Observe high, abstract low

Source observations may be concrete:

```text
"offers local errands"
"accepts accompaniment tasks"
"can visit locations in Xuzhou"
```

The engine should preserve those exact observations and may derive lower-level hypotheses such as:

```text
presence.local_execution
mobility.local
time.flexible_paid_task
```

It must **not** silently infer unrelated capabilities such as technical inspection, photography equipment, professional credentials, factory access or confidentiality readiness unless separately evidenced.

The lower the capability atom, the more reusable it may become across opportunity classes. But lower-level abstraction increases inference risk, so provenance must never be discarded.

## 5. Epistemic states are mandatory

The system distinguishes:

```text
OBSERVED FACT
!=
INFERRED CAPABILITY
!=
OBSERVED CAPABILITY CLAIM
!=
CONFIRMED CAPABILITY
!=
CALLABLE CAPABILITY
```

An inference rule may create a search hypothesis. It cannot create proof.

Model confidence, semantic similarity or repeated text does not upgrade a capability to `CONFIRMED`.

## 6. Callability is multi-axis

A resource is not callable merely because it exists.

At minimum distinguish:

### Capability evidence
```text
INFERRED
OBSERVED
CONFIRMED
```

### Availability
```text
UNKNOWN
ADVERTISED
CONFIRMED
COMMITTED
```

### Permission / control
```text
UNKNOWN
ALLOWED
RESTRICTED
```

### Freshness
A capability/availability observation must have an observation time and age policy.

Therefore:

```text
CAPABILITY EXISTS
+
CURRENT AVAILABILITY
+
RIGHT / PERMISSION TO MOBILIZE
+
FRESH ENOUGH EVIDENCE
=
POTENTIALLY CALLABLE CAPABILITY
```

Even this is not transactionability; trust, safety, price, acceptance and legal constraints remain downstream.

## 7. Deterministic inference before opaque promotion

For canonical evidence, prefer auditable rules such as:

```text
observed fact A + observed fact B
-> inferred capability C
```

Every derived capability must retain:
- source signal id;
- inference rule id;
- rationale;
- observation time;
- geography where relevant.

LLMs may generate candidate inference rules or suggest new capability atoms, but an LLM confidence score must not directly promote a resource into confirmed/callable state.

## 8. Requirement decomposition uses the same capability language

An opportunity should also be decomposed downward.

Instead of:

```text
"need a local inspection person"
```

prefer a bounded capability signature such as:

```text
presence.local_execution
+ mobility.local
+ checklist.execution
+ evidence.capture.photo_video
+ communication.basic_interview
```

This allows the system to search across resources that never advertised the final service SKU.

The engine evaluates **capability-bundle coverage**, not job-title similarity.

## 9. Coverage is not an automated decision about people

The discovery engine may identify that an evidence-linked set of resource capabilities covers a requirement bundle.

It must not turn this into an automated employment, eligibility or high-impact decision about an individual.

Canonical coverage states:

```text
INCOMPLETE
HYPOTHESIS_COVERED
DISCOVERED_COVERED
CALLABLE_COVERED
```

These states describe evidence coverage of a capability bundle. Human-reviewed transaction design still decides whether and how a real actor/resource may participate.

## 10. Example — from advertised task to latent capability

Suppose a public listing says an actor accepts local paid errands and other in-person tasks.

The source may directly support:

```text
OBSERVED: task.local_errand
OBSERVED: offers_paid_offline_tasks = true
OBSERVED: local_mobility_observed = true
```

Rules may create:

```text
INFERRED: presence.local_execution
INFERRED: mobility.local
```

The system must not add:

```text
capture.mobile_photo_video
technical.factory_inspection
confidentiality.ready
```

without additional evidence.

A later opportunity can be decomposed into capability atoms. If the observed/inferred graph covers part of that bundle, the system has discovered a **possible composition route**, not a provider commitment.

## 11. Sensor architecture

Each source adapter should implement only:

```text
RAW SOURCE ITEM
-> normalized SignalObservation
```

A normalized signal may contain:
- source id;
- signal id;
- observation time;
- actor reference;
- geography;
- exact observed facts;
- explicit capability claims;
- advertised availability where source-supported;
- permission only when source-supported;
- raw/provenance reference.

Source adapters must not contain opportunity strategy.

## 12. Time is first-class

The engine should model the world as a stream, not a static database.

Future sensing should support:
- first seen / last seen;
- repeated observation;
- state transitions;
- disappearance;
- repricing;
- availability changes;
- geography changes;
- capability confirmation/rejection;
- expiration/staleness.

The important object is often not `Actor X has Y`, but:

> `Actor X appears to have gained/lost/repriced/released/advertised Y at time T.`

## 13. Learning loop

The long-run loop is:

```text
SENSE
-> NORMALIZE
-> ABSTRACT
-> HYPOTHESIZE
-> DECOMPOSE REQUIREMENT
-> TEST CAPABILITY COVERAGE
-> VERIFY CALLABILITY
-> COMPOSE RESOURCES
-> VALIDATE TRANSACTION
-> OBSERVE OUTCOME
-> UPDATE RULES / CAPABILITY GRAPH / TRUST
-> SENSE AGAIN
```

Rejected hypotheses are learning data. A false inference should reduce or remove that rule rather than being forgotten.

## 14. Initial implementation

Current implementation:
- `src/live_resource_signals.py` — neutral SignalObservation, observed facts, open-ended capability claims, deterministic inference rules, availability/permission/freshness and explicit confirmation.
- `src/capability_coverage.py` — requirement-bundle decomposition and fail-closed capability coverage states.
- `tests/test_live_resource_signals.py` — truth-boundary tests including open capability namespace, non-inference of unsupported capability, callability confirmation, freshness and geography.

No platform-specific social sensor is canonical yet.

## 15. Build order from here

Do not start by writing broad scrapers.

Correct order:

1. stabilize neutral signal/capability contracts;
2. add a persistent signal ledger and state-change model;
3. define a small auditable capability-rule registry;
4. connect one lawful, technically stable sensor at a time;
5. retain raw evidence and non-promoted observations;
6. measure which sensors/rules repeatedly create useful latent-value hypotheses;
7. only then expand collection breadth or use model-assisted abstraction;
8. confirm real resources before any transaction claim.

## 16. Governing invariants

```text
PLATFORM != ONTOLOGY
LISTING != RESOURCE CLASS
OBSERVED FACT != INFERRED CAPABILITY
INFERRED CAPABILITY != CONFIRMED CAPABILITY
ADVERTISED != CURRENTLY AVAILABLE
CAPABILITY EVIDENCE != PERMISSION
CAPABILITY COVERAGE != TRANSACTIONABILITY
STALE SIGNAL != CURRENT STATE
TAXONOMY != DISCOVERY BOUNDARY
UNKNOWN != PASS
```

## 17. Governing sentence

> **持续把互联网与现实世界当作变化中的传感器网络：先保留原始行为与时间，再将其抽象成尽可能底层、可复用但仍带证据边界的能力原子；用同一种能力语言分解新机会，寻找原本没有被命名的互补组合；任何推导都只能形成假设，只有经过可用性、权限、时效和真实验证后，资源才进入可调用层。**
