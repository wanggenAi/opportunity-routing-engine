# Psychology Evidence Lineage

Status: `DISCOVERY INFRASTRUCTURE / FAIL-CLOSED`

Effective: 2026-09-15

Parent: `docs/PSYCHOLOGY_BEHAVIOR_TRACKER.md`

## Purpose

Consumer psychology is a hypothesis layer. A scalar such as `behavior_corroboration=0.8` or `money_corroboration=0.8` is not evidence by itself.

Every psychology signal must retain explicit provenance, and every non-zero corroboration claim must point to the evidence that supports it.

## Signal lineage

Each `PsychologySignal` requires:

```text
key_evidence_refs
```

The signal cannot exist in the tracker without at least one evidence reference.

Optional specialized evidence must remain inside the signal's total lineage:

```text
behavior_evidence_refs ⊆ key_evidence_refs
money_evidence_refs ⊆ key_evidence_refs
representative_evidence_refs ⊆ key_evidence_refs
```

A detached evidence ref fails closed.

## Behavior and money corroboration

```text
behavior_corroboration > 0
→ behavior_evidence_refs required

money_corroboration > 0
→ money_evidence_refs required
```

This still does not mean:

```text
behavior evidence == payer
money movement == willingness to pay for our product
corroborated psychology == opportunity
```

The values remain bounded discovery weights, now with auditable lineage.

## Representative share

A population-like share has stricter requirements:

```text
representative_sample = true
+ representative_evidence_refs
+ representative_share
+ positive sample_size
```

A source being categorized as representative research does not automatically make every statistic a representative population share.

## Snapshot lineage

Aggregated snapshots retain the union of:

- supporting evidence refs;
- behavior evidence refs;
- money evidence refs;
- representative evidence refs.

This allows downstream reasoning to audit exactly which evidence raised a psychology hypothesis above social/search salience alone.

## Governing boundaries

```text
NAKED SCALAR != EVIDENCE
SOCIAL SALIENCE != POPULATION SHARE
SEARCH INTEREST != PAID DEMAND
BEHAVIOR CORROBORATION != PAYER
MONEY CORROBORATION != BUSINESS OPPORTUNITY
PSYCHOLOGY SIGNAL != TAXONOMY PROMOTION
UNKNOWN != PASS
```

The psychology layer may rank which hypotheses deserve further investigation. It must never manufacture payer, paid need, route testability, active ontology state or commercial promotion.
