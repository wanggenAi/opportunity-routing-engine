# Architecture — Validation First

## Stage 0: research workflow

```text
Sources
  ├─ Current RFQs
  ├─ Import/shipment evidence
  ├─ Company websites
  ├─ Search engines
  ├─ Public business directories
  └─ Public professional/business profiles
        ↓
Collection
        ↓
Normalization
        ↓
Deduplication
        ↓
Buyer / demand verification
        ↓
Contactability hard gate
        ↓
Opportunity scoring
        ↓
Supplier capability matching
        ↓
Human review
```

## Stage 1: qualified opportunity workflow

```text
A-grade buyer
   ↓
Written outreach
   ↓
Buyer interest / requirement clarification
   ↓
Supplier shortlist
   ↓
Supplier authorization
   ↓
Factory capability confirmation
   ↓
Quotation / sample / meeting
   ↓
Deal facilitation
```

## Stage 2: future automation modules

Only build when evidence justifies them.

### `collectors`
Source-specific ingestion using APIs, feeds, exports, saved-search notifications, or permitted public-page retrieval.

### `normalizers`
Convert raw source records into a canonical opportunity schema.

### `verification`
Company identity, demand recency, import evidence, contact-route validation, contradiction checks.

### `scoring`
Deterministic score inputs + AI-assisted classification with evidence references.

### `supplier_graph`
Xuzhou supplier capabilities, product/process/MOQ/export-market metadata, evidence timestamps.

### `matching`
Buyer requirement ↔ supplier capability ranking.

### `outreach`
Human-approved written outreach drafts, reply classification, follow-up suggestions.

### `crm`
Opportunity lifecycle, activity history, evidence, supplier/buyer relationship state.

## Canonical opportunity lifecycle

```text
RAW
→ NORMALIZED
→ VERIFIED_BUYER
→ CONTACTABLE
→ QUALIFIED
→ SUPPLIER_MATCHED
→ OUTREACH_READY
→ CONTACTED
→ RESPONDED
→ REQUIREMENT_CONFIRMED
→ SUPPLIER_AUTHORIZED
→ QUOTED
→ SAMPLE_OR_MEETING
→ NEGOTIATION
→ WON / LOST / DORMANT
```

No stage may be skipped by assumption.

## Core data principle

Every important assertion should retain:

- value;
- evidence/source;
- observed_at / source_date where available;
- verification status;
- confidence or contradiction state.

This is more important than model sophistication.

## Human-in-the-loop boundaries

Human approval remains mandatory before:

- representing a supplier;
- sending product-specific claims not already public/authorized;
- submitting a quotation;
- making commitments on price, MOQ, lead time, certification, logistics, payment, or contract terms;
- escalating to sensitive/personal contact methods;
- changing commercial relationship status to WON.

## Engineering principle

Start with reproducible spreadsheets/CSV/JSON and scripts. Introduce databases, queues, agents, scheduled jobs, and dashboards only when the experiment volume requires them.
