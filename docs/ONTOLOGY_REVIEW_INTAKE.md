# Ontology Review Decision Intake

Status: `GOVERNANCE INFRASTRUCTURE / FAIL-CLOSED / NO REAL DECISION BUNDLED`

Effective: 2026-09-14

Parent: `docs/ONTOLOGY_GOVERNANCE.md`

## Purpose

`PROMOTION_REVIEW_READY` creates governance work, not ontology truth. This layer records an explicit reviewer decision with enough provenance to audit exactly what was reviewed before any separate ontology-version materialization is considered.

Canonical separation:

```text
ONTOLOGY REVIEW QUEUE
→ EXPLICIT REVIEW DECISION INTAKE
→ append-only review decision event
→ separate version materialization step
→ immutable ontology version
→ separate explicit activation
```

The intake ledger has no `SQLiteOntologyRegistry` handle. Recording an `ACCEPT` event therefore cannot create a version and cannot activate taxonomy.

## Required decision provenance

Every decision event requires:

```text
decision_id
review_item_id
decision
review_outcome
reviewer_id
reviewed_at (timezone-aware)
rationale
review_provenance_ref
supporting_evidence_refs
reviewed_boundary
reviewed_counterexamples
```

An approval also requires a proposed stable concept identity and label. A rename/merge/split revision direction requires an explicit `revision_instruction`.

The four review outcome classes are:

```text
ACCEPT
REJECT
REVISE
DEFER
```

They map onto the existing ontology-governance decisions; `REVISE` is the class for explicit rename/merge/split review requirements rather than a silent edit.

## Re-attestation and stale-input protection

Decision intake is bound to the queue item, not merely to its string ID.

The reviewer must re-attest:

- the exact boundary;
- the exact counterexamples;
- explicit evidence references that already exist on the queue item.

`APPROVE_NEW_CONCEPT_VERSION` must explicitly cite every supporting claim reference carried by the review item. The store also persists a deterministic fingerprint of the reviewed queue-item substance. Replaying the same `decision_id` against changed queue content fails closed.

## Append-only decision history

The SQLite decision ledger is append-only.

- exact retries of the same `decision_id` and same content are idempotent;
- changing content behind an existing `decision_id` is rejected;
- review timestamps cannot move backward within one review item;
- `DEFER` may be followed by another event;
- `ACCEPT`, `REJECT`, and explicit `REVISE` directions are terminal for that review item; a changed proposal must enter governance as a new review item.

## Truth boundary

Decision intake explicitly rejects commercial and activation truth fields such as payer confirmation, paid need, route-testability, transaction readiness, active version, and activation time.

```text
REVIEW DECISION EVENT != ONTOLOGY VERSION
REVIEW DECISION EVENT != ACTIVE TAXONOMY
REVIEW DECISION EVENT != BUSINESS PROMOTION
```

A decision may authorize a later, separately invoked version-materialization operation. That later operation still does not activate the version.

## Dry-run fixture 008

`tests/fixtures/ontology_review_queue_dry_run.json` and `tests/fixtures/ontology_review_decisions_dry_run.json` are deliberately synthetic. Their IDs, provenance refs, actors, claims, observations and concept label are marked synthetic and are not evidence about the real world.

The `ontology-review-decision-intake-008` workflow exercises:

```text
synthetic queue
→ DEFER event
→ synthetic ACCEPT event
→ append-only SQLite ledger
→ snapshot artifact
```

and asserts:

```text
active_ontology_changes = 0
taxonomy_promotion = NOT_PROMOTED
business_promotion = NOT_PROMOTED
registry_effect = NONE_DECISION_INTAKE_DOES_NOT_CREATE_OR_ACTIVATE_ONTOLOGY_VERSION
```

The workflow does not ingest the Run 003 production review queue and does not make a real approval decision for either currently queued concept.
