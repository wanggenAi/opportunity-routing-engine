# Engineering Method Selection Principle

Status: `LOCKED / SCIENTIFIC ENGINEERING DISCIPLINE`

## Purpose

The repository should use mature data structures, algorithms, design patterns,
mathematical models and statistical methods when they encode a real invariant or
improve a real decision.

It must not cargo-cult sophistication.

```text
REAL PROBLEM
→ EXPLICIT INVARIANT / DECISION FAILURE
→ METHOD WITH MATCHING ASSUMPTIONS
→ EXECUTABLE IMPLEMENTATION
→ TESTABLE DECISION IMPROVEMENT
→ KEEP / REVISE / REMOVE
```

The method is downstream of reality. Reality is never forced to fit the method.

## Method-selection contract

Before introducing a non-trivial method, state:

1. **Problem** — what observed decision/error/scale problem exists?
2. **Invariant** — what must the implementation preserve?
3. **Why this method** — what established property of the method matches the problem?
4. **Assumptions** — what must be true for the method to be valid?
5. **Failure mode** — how could the method distort reality?
6. **Observable benefit** — what decision becomes more reliable, cheaper or faster?
7. **Complexity budget** — why is the implementation complexity justified now?
8. **Replacement trigger** — what measured scale/evidence would justify a more
   sophisticated method?

Do not introduce a method merely because it is common, mathematically elegant, or
available in a library.

## Current justified method: Pareto non-dominated sorting

Current problem:
multiple high-attraction signals can be strong on different critical dimensions.

A weighted total score is unsafe because:
- critical attraction dimensions are not naturally exchangeable;
- a very high value jump must not compensate for weak bilateral pull;
- strong operator control must not compensate for a locked decision window;
- arbitrary weights can manufacture a winner.

Therefore current Scan 004 attention allocation uses:

`src/attraction_frontier.py`

Method:
- hard attraction floor first;
- Pareto dominance second;
- layer 0 = non-dominated frontier;
- deeper layers = successively dominated attention tiers;
- no weighted total score selects the winner.

For expected Scan-scale candidate counts, transparent `O(n^2)` comparison is
preferred. Do not introduce spatial indexes or more complex skyline algorithms until
measured candidate volume makes the simple method a real bottleneck.

## Methods that may become justified later

These are **not automatically authorized**. Their prerequisites must exist.

- **Graph / multilayer graph algorithms** — when evidence-backed actors, resources,
  states and missing edges become numerous enough that path/bridge structure cannot be
  reasoned about locally.
- **Matching / min-cost flow / assignment** — when real transaction units, compatible
  supply and demand, capacities and costs exist.
- **Queueing models** — when arrival/service/wait data exist and delay/capacity is the
  actual economic bottleneck.
- **Bayesian updating** — when repeated comparable evidence supports calibrated
  uncertainty updates rather than narrative confidence.
- **Multi-armed bandits / adaptive allocation** — when research actions have measurable
  repeated reward signals, so exploration/exploitation can be learned rather than
  guessed.
- **Causal inference / experiments** — when intervention/comparison structure supports
  effect estimation.
- **State machines / event sourcing** — for lifecycle, recovery and truth transitions
  where legal state changes and audit history matter.
- **Strategy / Adapter / Pipeline patterns** — when interchangeable executors,
  providers or stages must vary without changing domain truth.

## Governing boundary

```text
ALGORITHM != TRUTH
MODEL != REALITY
SCORE != VALUE
COMPLEXITY != RIGOR
MATURE METHOD + WRONG ASSUMPTIONS = WRONG SYSTEM
SIMPLE METHOD + CORRECT INVARIANTS > FANCY METHOD + STORY
```

Engineering quality means using the simplest mature mechanism that faithfully encodes
the current real-world constraint and exposes its assumptions to tests.
