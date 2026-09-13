# Resource Composition — Capability-Cover Hypotheses

Status: `DISCOVERY SUBSYSTEM / EVIDENCE-BOUND`

Constitutional parent: `docs/LATENT_VALUE_DOCTRINE.md`.

## Purpose

Live sensing can discover low-level capabilities that sit on different actors. A useful outcome may require a combination that no single actor advertises as a finished service.

The Resource Composition layer asks:

> Which evidence-linked actor/capability combinations can structurally cover a bounded capability requirement, and what is the maturity of that coverage?

It does **not** ask which person is best, who should be hired, who is eligible, or whether a transaction should occur.

## Position in the discovery chain

```text
SIGNAL OBSERVATIONS
-> CAPABILITY CLAIMS
-> REQUIREMENT BUNDLE
-> CAPABILITY COVERAGE
-> RESOURCE COMPOSITION HYPOTHESES
-> CALLABILITY / ACCESS / CONSENT / TRUST
-> COUNTERPARTY SURPLUS
-> PAYER / TRANSACTION TRUTH
-> BOUNDED VALIDATION
```

## Minimal cover, not best route

The first implementation searches for **minimal actor sets** whose combined capability claims cover all required capability atoms.

Minimal means only:

> removing any selected actor would make that particular combination incomplete.

It does not mean:
- lowest cost;
- highest quality;
- safest provider;
- preferred worker;
- recommended contractor;
- commercially optimal route.

Alternative minimal compositions are retained. Deterministic output ordering exists only for reproducibility.

## Composition maturity

```text
HYPOTHESIS_COMPOSED
```
At least one required capability is covered only by an `INFERRED` claim.

```text
DISCOVERED_COMPOSED
```
Every required capability has at least `OBSERVED` / `CONFIRMED` evidence, but one or more legs are not currently callable.

```text
CALLABLE_COMPOSED
```
Every required capability has at least one fresh claim that is `CONFIRMED`, currently `CONFIRMED`/`COMMITTED` available, and `ALLOWED` for mobilization.

Even the strongest state means only that the capability bundle is structurally callable under current evidence.

## Hard boundaries

```text
CAPABILITY COMPOSITION != PERSON RANKING
COMPOSITION HYPOTHESIS != EMPLOYMENT DECISION
MINIMAL COVER != BEST ROUTE
HYPOTHESIS_COMPOSED != DISCOVERED_COMPOSED
DISCOVERED_COMPOSED != CALLABLE_COMPOSED
CALLABLE_COMPOSED != COUNTERPARTY CONSENT
CALLABLE_COMPOSED != ACCESS / BACKING
CALLABLE_COMPOSED != LEGAL / TRUST / SAFETY PASS
CALLABLE_COMPOSED != PAYER
CALLABLE_COMPOSED != TRANSACTIONABILITY
UNKNOWN != PASS
```

## Provenance

Every composition preserves:
- selected actor references;
- required capability keys;
- evidence maturity by capability;
- which selected actors support each capability;
- callable actor references where current evidence supports callability;
- underlying source signal ids.

The system must therefore be able to answer not only `what combination did we hypothesize?`, but also `which observations caused us to believe each leg exists?`.

## Current implementation

- `src/resource_composition.py`
  - deterministic minimal-cover enumeration;
  - multi-actor composition;
  - evidence/callability maturity;
  - geography filtering;
  - freshness enforcement through existing `CapabilityClaim.is_callable()`;
  - provenance aggregation;
  - bounded `max_actors` / `max_hypotheses` controls.
- `tests/test_resource_composition.py`
  - single/multi-actor covers;
  - inferred vs observed vs callable states;
  - stale evidence;
  - geography mismatch;
  - non-minimal-superset elimination;
  - alternative composition preservation;
  - provenance retention.

## Next layer

The next useful work is not to add a provider score.

It is to connect compositions back to real latent-value / exchange hypotheses and measure whether sensors plus inference rules repeatedly produce combinations worth validating. That later layer must still separately test access, consent, legal/trust/safety, counterpart-visible surplus, payer and economics.
