# Origin Probe Packet 001 — Non-OEM Maintenance Trace Truth

Date: 2026-09-16
Candidate: `XZ-NONOEM-MAINTENANCE-TRACE-AI-001`
State: `PUBLIC_TARGET_POOL_READY / ORIGIN_TRUTH_STILL_BLOCKED`

## Purpose

This packet exists to answer one narrow reality question before any buyer outreach, software build, data collection or dataset project:

> Do independent Xuzhou engineering-machinery aftermarket actors actually retain maintenance/failure traces with enough common structure and lawful control to support a derived cross-actor dataset that is not already absorbed by OEM/platform systems?

This is not a sales script for a data platform.

## What public research has already falsified

The missing edge is **not** generic maintenance digitization.

Commercial tools already provide:

- repair work orders and equipment histories;
- inspection / maintenance / spare-part records;
- lifecycle equipment ledgers;
- equipment alarms and predictive-maintenance workflows;
- engineering-machinery fleet/rental management.

OEM/industrial-platform routes already provide first-party telemetry, fault/repair data, lifecycle analytics and high-quality dataset construction.

Therefore the surviving hypothesis is narrower:

`INDEPENDENT AFTERMARKET TRACE -> RIGHTS / GOVERNANCE -> COMMON SCHEMA -> DOMAIN ADJUDICATION -> MODEL-READY DERIVED EVIDENCE`

The hypothesis fails if any one of those transitions is not real.

## Stage 1 safety and truth boundary

Do **not** ask for, photograph, upload, copy, export or retain any customer record or equipment-level record.

Do not request:

- customer names;
- phone numbers;
- equipment serial numbers;
- VIN/device identifiers;
- contract prices;
- OEM confidential diagnostics;
- screenshots of customer systems;
- raw repair orders.

At Stage 1, only inspect or ask about:

- whether a record exists;
- storage medium;
- blank field names / schema;
- retention duration;
- owner/controller;
- whether the same data is already sent to an OEM/dealer/platform/insurer;
- whether de-identified derived reuse could ever be separately authorized.

## Target pool

### 1. 徐州福泰工程机械贸易有限公司 — `HIGH`

Public basis: repair + parts + rental; dedicated repair workshop; broad terminal-user base; current 2026 activity.

Probe value: strongest test of repeated third-party repair traces plus parts/action history.

### 2. 徐州路信工程机械租赁有限公司 — `HIGH`

Public basis: equipment rental plus explicit field emergency repair, repair and maintenance.

Probe value: strong test of field-service traces and whether they are retained or remain technician memory / paper / chat.

### 3. 徐州永合工程机械有限公司 — `HIGH`

Public basis: equipment rental and repair; mixed-brand road machinery fleet.

Probe value: tests whether non-single-OEM fleets create cross-brand traces outside one OEM telemetry ecosystem.

### 4. 徐州众瑞达工程机械有限公司 — `MEDIUM_HIGH`

Public basis: 50+ units; rental, road construction and road maintenance/repair.

Probe value: fleet-owner contrast; tests whether repeated maintenance events create equipment-linked histories.

### 5. 徐州市华通公路工程机械有限公司 — `MEDIUM_HIGH`

Public basis: 2026 references describe active rental/construction/technical service, about 80 major equipment units and regular maintenance.

Probe value: larger-fleet contrast; tests whether scale produces structured maintenance data and whether OEM systems already absorb it.

## Minimum schema questions

For each actor answer only the following:

1. Is any repair/maintenance history retained?
2. Medium: paper / Excel / ERP-SaaS / WeChat / technician memory / mixed?
3. What are the **blank field names** on a typical record?
4. Is each event linked internally to one equipment identity?
5. Are the following separable fields present?
   - symptom;
   - diagnostic code/observation;
   - diagnosis or root cause;
   - action performed;
   - replaced part;
   - post-repair result;
   - repeat repair / rework;
   - operating context / hours / environment.
6. How long are records retained?
7. Who controls the record: actor, customer, OEM/dealer, software vendor, insurer, mixed?
8. Is the same information already uploaded or contractually assigned to an OEM/dealer/platform?
9. Could a separately authorized **de-identified derived dataset** ever be considered if the actor receives measurable value?

## Common-schema gate

Do not invent normalization.

A minimum common record may be proposed only if at least 3 of 5 actors independently expose compatible field classes.

Example only — not an assumed schema:

`equipment_class + operating_context + symptom + diagnosis + repair_action + replaced_component + result + recurrence`

If actual field structures do not support this, the proposal dies or is narrowed.

## Rights gate

`RECORD_EXISTS != REUSE_RIGHT_EXISTS`

At least two origin actors must have a plausible lawful path to authorize a de-identified derivative use before buyer validation.

Any OEM, customer, platform, insurance, employee-IP, trade-secret or confidentiality restriction remains fail-closed.

## Existing-route absorption gate

For each actor ask whether the same traces are already transmitted to or governed by:

- OEM telematics/service system;
- authorized dealer system;
- fleet/rental SaaS;
- insurer/financier;
- enterprise ERP/EAM;
- industrial Internet platform.

If the same high-value trace is already comprehensively captured and governed by an incumbent route, it is not our missing edge.

## Pass

Stage 1 passes only if all are true:

- at least 3/5 actors retain non-trivial repair/failure histories;
- at least 3/5 support a minimum common schema;
- at least 2/5 have a plausible separate authorization path for de-identified derived reuse;
- the useful fields are not already fully absorbed by incumbent OEM/platform routes.

## Kill

Kill or materially narrow the route if:

- records are mostly oral or discarded;
- fields are too heterogeneous;
- useful diagnosis/outcome labels do not exist;
- rights cannot be cleared;
- OEM/platform systems already own/capture the relevant traces;
- value would require founder-led ongoing annotation/consulting.

## Only after Stage 1 pass

Do **not** bring raw records to a buyer.

Produce one abstracted schema + field availability matrix + rights summary, then test one buyer-side question:

> Does this non-OEM trace class add measurable training/evaluation/diagnostic value beyond your existing telemetry, OEM service and public/high-quality datasets — enough for a bounded paid pilot?

No paid intent -> no dataset build.

## External action status

`NO_OUTREACH_SENT = TRUE`

Public research and target qualification only in this run.
