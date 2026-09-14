# Eldercare Structure Validation Plan 006

Status: `NON-CANONICAL EVIDENCE-ACQUISITION PLAN`

Parent state: `ELDERCARE_CAPACITY_ORCHESTRATION` is `STRUCTURE_VALIDATION_READY` with exactly one missing structural-commercialization dimension: `COMPOUNDING`.

This plan does not promote eldercare into a business, route, payer or market-entry decision. It exists to falsify or support the single remaining compounding hypothesis as cheaply and safely as possible.

## Domain-neutral planning architecture

The core `structure_validation_planning` module no longer knows about assets, leases, eldercare or any other vertical. Domain-specific measurement requirements are supplied through a reviewed validation profile.

The eldercare profile uses:

```text
case_unit = DEIDENTIFIED_INSTITUTION_OR_PROCESS_EPISODE
```

It measures institution/process-level episodes rather than individual beneficiary records.

## Three bounded tasks

1. `LOCAL_CASE_PANEL`
   - collect 5–10 current comparable process episodes across at least three independent focal actors;
   - record the same process and execution metrics for every case;
   - preserve failures and incomparable cases.

2. `LOCAL_PAID_MANDATE`
   - corroborate at least two Jiangsu/Xuzhou paid mandates with first-party settlement/payment evidence;
   - contracts, awards and budgets remain below settlement truth;
   - this is local corroboration, not a missing global structural dimension.

3. `COMPOUNDING`
   - use at least two later cases across at least two independent focal actors;
   - require explicit references to reused prior cases, templates, rules, routing knowledge or prior outcomes;
   - compare predeclared metrics such as intake, assessment, coordination, handoffs, exceptions, QA rework, total cycle and acceptance;
   - preserve confounders and negative results.

## Privacy / vulnerable-person boundary

The profile forbids unnecessary personal or health data. Do not collect:

- beneficiary names;
- national IDs;
- phone numbers;
- home addresses;
- diagnoses;
- medical records;
- raw health data.

Use only authorized/public, minimum-necessary, de-identified institution/process-level evidence.

## Pass / falsification logic

`COMPOUNDING` may only become evidenced when time-ordered later cases reuse identifiable prior artifacts and measurably improve at least two predeclared execution metrics without degrading acceptance/quality, with plausible alternative explanations considered.

The following are insufficient by themselves:

```text
database growth
digital platform adoption
automation
one-time speed improvement
repeated revenue
more cases
operator familiarity
```

If later cases do not improve, or still require bespoke operator work from zero, the compounding thesis should be falsified rather than narrated into success.
