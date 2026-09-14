# Emergent Ontology Governance

Status: `GOVERNANCE INFRASTRUCTURE / FAIL-CLOSED`

Effective: 2026-09-14

Parents:
- `docs/LATENT_VALUE_DOCTRINE.md`
- `docs/DYNAMIC_SENSOR_FABRIC.md`
- `docs/DISCOVERY_ENGINE.md`

## 1. Purpose

The world model must be able to learn new lower-level concepts without freezing today's categories into core code and without allowing an LLM or one research batch to silently redefine ontology truth.

The stable semantic kernel remains:

```text
ACTOR / STATE / CHANGE / RESOURCE / CAPABILITY / PERCEPTION / MOTIVE /
BEHAVIOR / FLOW / CONSTRAINT / FRICTION / OUTCOME / EVIDENCE / TIME / SPACE
```

Lower-level concepts are versioned governance objects.

## 2. Promotion-review readiness is not promotion

The emergent-taxonomy evidence gate may produce:

```text
RESIDUAL
→ CANDIDATE
→ PROMOTION_REVIEW_READY
```

`PROMOTION_REVIEW_READY` only means the evidence is diverse enough to justify an ontology-governance decision.

It does not mean:
- a concept already exists in the active ontology;
- the proposed label/definition is correct;
- the concept is an opportunity;
- a payer exists;
- a resource is available;
- a route is testable;
- a business should be pursued.

## 3. Two-stage governance

Canonical governance path:

```text
PROMOTION_REVIEW_READY alignment
→ ONTOLOGY_PROMOTION_REVIEW queue
→ explicit review decision
→ immutable ontology concept version
→ separate explicit activation
```

The separation is deliberate.

```text
REVIEW QUEUE != ONTOLOGY VERSION
APPROVED VERSION != ACTIVE TAXONOMY
MODEL SUGGESTION != REVIEW DECISION
ONTOLOGY CONCEPT != BUSINESS OPPORTUNITY
```

No production workflow may turn queue membership directly into active taxonomy.

## 4. Versioned concept identity

A concept has a stable `concept_id` and one or more immutable versions.

Each version preserves at least:

```text
concept_id
version
primitive
preferred_label
aliases
definition
boundary
counterexamples
source_alignment_refs
supporting_claim_refs
created_from_review_item_id
change_kind
version_state
rationale
```

A changed definition, boundary or label receives a new version. Historical versions are never overwritten.

`CREATE` must begin at version 1. `REVISE`, `RENAME`, and `DEPRECATE` operate on an existing stable identity and therefore cannot begin at version 1. `MERGE` and `SPLIT` may create a genuinely new stable concept identity at version 1 because their meaning is carried by explicit cross-concept lineage.

## 5. Change kinds and lineage

Supported version changes include:

```text
CREATE
REVISE
RENAME
MERGE
SPLIT
DEPRECATE
```

Lineage relations include:

```text
REVISED_FROM
RENAMED_FROM
MERGED_FROM
SPLIT_FROM
DEPRECATED_BY
```

The registry records lineage between concrete concept versions. Lifecycle lineage is not decorative metadata: it is part of registry validity.

Required semantics:

```text
REVISE     → REVISED_FROM immediately previous version of same concept
RENAME     → RENAMED_FROM immediately previous version of same concept
MERGE      → MERGED_FROM at least two distinct parent concepts
SPLIT      → SPLIT_FROM a shared source version, with at least two child concept identities
DEPRECATE  → immediately previous version DEPRECATED_BY the new deprecated version
```

A lifecycle version may be registered before its lineage edges are attached so the referenced version exists for foreign-key-safe edge creation. That transient state is intentionally not usable: an orphan lifecycle version cannot be activated, and `snapshot()` fails closed until the lineage graph validates.

Lineage direction is also validated. For example, `MERGED_FROM` must originate from a `MERGE` version, `SPLIT_FROM` from a `SPLIT` version, and `DEPRECATED_BY` must point to a `DEPRECATE` version. This prevents a syntactically valid edge from silently changing lifecycle meaning.

## 6. Deprecation

Deprecation is a versioned state, not deletion.

A deprecated version:
- remains queryable for historical interpretation;
- preserves evidence and lineage;
- cannot be activated;
- does not erase observations that used an earlier concept version.

Deprecating a concept whose earlier version is currently active is not allowed as an implicit side effect. The operator must first perform a separate explicit `deactivate()` action and only then register the `DEPRECATE` version. This prevents a registry from simultaneously claiming that a concept is deprecated while an older version remains active.

Once the latest version for a stable `concept_id` is `DEPRECATED`, that concept history is terminal:
- no earlier `ELIGIBLE` version may be reactivated;
- no later `REVISE` / `RENAME` / other eligible version may silently revive the same stable identity;
- a genuinely new concept must use a new `concept_id` and preserve its relationship through explicit lineage.

Historical data must remain interpretable under the taxonomy version that existed when it was produced.

## 7. Activation

Activation is a separate explicit state mutation over immutable versions.

A registered version is not active merely because it was approved for creation.

Activation requires:
- an existing `ELIGIBLE` ontology version;
- a concept whose latest version is not `DEPRECATED`;
- complete lifecycle lineage for any non-`CREATE` change;
- explicit actor/authority identity;
- timezone-aware activation time;
- explicit rationale.

A `DEPRECATED` version cannot be activated, and an older eligible version cannot be used to resurrect a concept after a later deprecation.

## 8. Review queue behavior

`src/ontology_governance.py` builds review work only from assessments already in `PROMOTION_REVIEW_READY`.

`CANDIDATE` and `RESIDUAL` assessments do not enter the queue automatically.

For Broad Discovery Run 003, the current queue is expected to contain only:

```text
SKILL_TO_WORK_MATCHING_INFRASTRUCTURE
PLATFORM_TRUST_AND_GOVERNANCE_INFRASTRUCTURE
```

while these remain below the gate:

```text
CIRCULAR_RECOMMERCE_INFRASTRUCTURE
PET_SERVICE_ECOSYSTEM_FORMALIZATION
LOGISTICS_CAPACITY_ORCHESTRATION
```

This is a property of the current evidence snapshot, not a permanent ranking.

## 9. No automatic business promotion

Ontology governance sits upstream of commercial validation.

```text
ACTIVE ONTOLOGY CONCEPT
!=
OBSERVED PATTERN
!=
REGENERATIVE COMMERCIAL STRUCTURE
!=
ROUTE_TESTABLE OPPORTUNITY
```

The commercial system still requires its own recurrence, payer, resource, blocker, access, safety, settlement, delegatability and compounding evidence.

## 10. Synthetic lifecycle verification

`ontology-lifecycle-lineage-010` is a main-only synthetic dry run. It constructs only `concept:synthetic-lifecycle-010-*` identities and exercises:

```text
CREATE
→ REVISE / REVISED_FROM
→ MERGE / MERGED_FROM
→ SPLIT / SPLIT_FROM
→ RENAME / RENAMED_FROM
→ DEPRECATE / DEPRECATED_BY
```

The artifact must report validated lineage, zero active synthetic concepts, zero production ontology changes, and `NOT_PROMOTED` for both taxonomy and business. It never consumes the Run 003 production review queue and never approves a real concept.

## 11. Governing invariant

> **让 taxonomy 随证据生长，但不让模型的命名冲动变成事实：先积累多来源、多 Actor、跨时间的 reviewed evidence，再进入显式 ontology review；定义变化必须产生新版本，revise/rename/merge/split/deprecate 必须保留可验证 lineage；缺 lineage 的 lifecycle version 不能 activation、不能通过 snapshot 审计；任何版本只有经过独立 activation 才能成为当前 ontology；deprecation 必须先显式 deactivate，且一旦 stable concept identity 被 deprecated 就不能通过旧版本或追加 eligible 版本偷偷复活；ontology 本身永远不能替代商业证据。**
