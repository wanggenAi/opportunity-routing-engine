# Xuzhou Global Deal Engine

AI-assisted cross-border B2B opportunity discovery, buyer verification, local supplier matching, and deal facilitation for Xuzhou manufacturing clusters.

## Mission

Turn fragmented global demand signals into qualified, actionable opportunities for Xuzhou manufacturers.

The project is **not** an export-consulting product, an Alibaba/TikTok/Google agency, or a simple public-RFQ forwarding service. Its core hypothesis is that software + AI + local execution can reduce the cost of:

1. discovering overseas demand;
2. verifying buyer quality and contactability;
3. matching demand to real Xuzhou production capability;
4. moving qualified opportunities toward quotation, sample, meeting, and transaction.

## Current focus

The first validation vertical is **glass packaging**, starting with perfume/cosmetic glass bottles and the Xuzhou/Maopo supplier cluster.

## Project rule

**Evidence before automation.**

We do not build large crawlers or workflow systems until the underlying commercial hypothesis survives measurable experiments.

## Repository layout

- `docs/` — formal truth, architecture, experiments, decisions
- `prompts/` — versioned AI prompts and evaluation rubrics
- `src/` — future production code
- `workflows/` — automation and orchestration definitions
- `data/` — schemas, samples, and non-sensitive reference data only
- `tests/` — future automated tests

## Initial commercial loop

```text
Global demand sources
        ↓
Collect / normalize / deduplicate
        ↓
Buyer + demand verification
        ↓
Contactability hard gate
        ↓
Xuzhou supplier matching
        ↓
Human review
        ↓
Buyer written outreach
        ↓
Supplier authorization / factory visit
        ↓
Quotation / sample / meeting
        ↓
Deal facilitation
```

## Hard constraints

- Never fabricate buyer data, demand, contact details, supplier capability, quotations, or transaction status.
- `UNKNOWN` is not treated as `PASS`.
- A public RFQ alone is not a qualified opportunity.
- Buyer contactability is a hard gate for top-priority opportunities.
- Respect source terms, robots/access restrictions, privacy, anti-spam rules, and applicable law.
- Prefer official APIs, feeds, saved searches, licensed databases, and public business contact channels over prohibited scraping.
- Do not impersonate a supplier or submit binding quotations without authorization.
- Trade, legal, tax, customs, logistics, certification, and payment matters should be handled by qualified parties when required.

## Current phase

**Phase 0 — Commercial feasibility validation.**

Success is not measured by lines of code. It is measured by whether we can repeatedly produce better qualified, reachable overseas buyer opportunities than a basic single-channel manual workflow, and later whether those opportunities generate real replies, quotations, samples, meetings, and deals.
