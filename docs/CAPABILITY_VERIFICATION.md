# Capability Verification Ledger

## Purpose

Public observations, reviewed signal imports and inference rules must not manufacture `CONFIRMED`, `COMMITTED`, or `ALLOWED` state.

Capability verification is therefore a **separate evidence boundary** after discovery:

```text
RAW / PUBLIC OBSERVATION
-> OBSERVED / INFERRED CAPABILITY GRAPH
-> EXPLICIT VERIFICATION OR FALSIFICATION EVENT
-> TIME-SCOPED VERIFIED CAPABILITY PROJECTION
-> CAPABILITY COVERAGE / RESOURCE COMPOSITION
```

The verification ledger is append-only. It never edits the original signal, graph materialization, rule version or prior observation.

## Verification event

Each event requires:

- immutable `verification_id`;
- `actor_ref`;
- `capability_key`;
- verdict: `CONFIRMED` or `REJECTED`;
- timezone-aware `verified_at`;
- explicit `evidence_ref`;
- explicit `evidence_note`;
- optional geography;
- availability state;
- permission state;
- optional related globally unambiguous signal references.

For a `CONFIRMED` capability, availability and permission remain independent dimensions:

```text
CONFIRMED capability
+ UNKNOWN availability
+ UNKNOWN permission
= NOT CALLABLE
```

Only when the normal capability contract also has current confirmed/committed availability, allowed permission and freshness may it become callable.

A `REJECTED` capability may not smuggle availability or permission state; those fields must remain `UNKNOWN` for rejection events.

## Falsification semantics

A rejection does not delete history.

If a rejection is at least as new as a base OBSERVED/INFERRED claim for the same actor/capability, that older claim is suppressed from the time-scoped verified projection.

If a **newer real observation** later appears, the capability may re-enter the projection as unverified evidence and await a new verification event.

Therefore:

```text
REJECTED_OLD_EVIDENCE != PERMANENT_BLACKLIST
NEWER_OBSERVATION != AUTOMATIC_RECONFIRMATION
```

## Composition integration

Composition Runs optionally consume a verification database.

Each run persists a `verification_snapshot_fingerprint` alongside:

- exact capability graph materialization;
- exact requirement bundle version;
- `as_of` time;
- freshness window;
- composition parameters.

No verification database preserves the pre-verification behavior and records fingerprint `NONE`.

When verification is supplied:

```text
all required capabilities structurally observed
-> DISCOVERED_COMPOSED

all required capabilities also have fresh callable verified claims
-> CALLABLE_COMPOSED
```

`CALLABLE_COMPOSED` is still only a resource-callability statement.

It does **not** establish:

- counterpart consent;
- access to premises/data/assets;
- legal or safety approval;
- payer commitment;
- acceptable price/economics;
- transaction readiness.

## Reviewed verification intake

Verification uses its own reviewed JSON/JSONL intake and is intentionally separate from ordinary signal intake.

Example:

```json
{
  "verification_id": "verify-20260913-001",
  "actor_ref": "actor-a",
  "capability_key": "presence.local_execution",
  "verdict": "CONFIRMED",
  "verified_at": "2026-09-13T22:00:00+08:00",
  "evidence_ref": "field-check:verify-20260913-001",
  "evidence_note": "Direct reviewed capability and availability check",
  "geography": "Xuzhou",
  "availability": "CONFIRMED",
  "permission": "ALLOWED",
  "related_signal_refs": ["sensor-a::item-1"]
}
```

Import:

```bash
python scripts/import_capability_verifications.py \
  --input data/reviewed_verifications.jsonl \
  --db data/capability_verifications.db \
  --summary-output artifacts/verification_import_summary.json
```

Build compositions with the verified projection:

```bash
python scripts/build_resource_compositions_from_graph.py \
  --graph-db data/capability_graph.db \
  --requirement-db data/requirements.db \
  --verification-db data/capability_verifications.db \
  --run-db data/composition_runs.db \
  --summary-output artifacts/composition_summary.json
```

The verification intake explicitly rejects fields attempting to establish transaction-layer truth, such as payer commitment, transaction readiness, counterpart consent, access approval or safety approval.

## Governing invariants

```text
PUBLIC_OBSERVATION_NE_VERIFICATION
VERIFICATION_HISTORY_IS_APPEND_ONLY
VERIFICATION_REQUIRES_EXPLICIT_EVIDENCE_REF
CONFIRMATION_NE_AVAILABILITY
CONFIRMATION_NE_PERMISSION
REJECTION_DOES_NOT_REWRITE_RAW_EVIDENCE
NEWER_OBSERVATION_MAY_REOPEN_REJECTED_CAPABILITY_AS_UNVERIFIED
CONFIRMED_CLAIM_NE_CALLABLE_UNLESS_AVAILABILITY_PERMISSION_FRESHNESS_PASS
CALLABLE_COMPOSED_NE_COUNTERPARTY_CONSENT
CALLABLE_COMPOSED_NE_TRANSACTIONABILITY
UNKNOWN_NE_PASS
```
