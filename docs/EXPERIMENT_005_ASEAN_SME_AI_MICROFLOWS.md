# EXPERIMENT 005 — China–ASEAN SME AI Microflows

Status: `INVESTIGATE`
Started: 2026-09-08
Primary geography: Xuzhou, Jiangsu → ASEAN markets
Initial ASEAN focus: Malaysia first, then Vietnam / Thailand / Indonesia as evidence justifies

## 1. Why this experiment exists

Test whether a commercially attractive niche exists in small, frequent, rules-heavy or coordination-heavy cross-border workflows that:

- matter to SMEs but are too small / fragmented for heavyweight enterprise software;
- can be improved with AI + structured workflow + bounded human review;
- have a clearly identifiable payer;
- can be sold first as a concierge service before product software is built;
- can accumulate reusable rules, document patterns, workflow data and expert-routing knowledge.

This is **not** a decision to become a generic AI outsourcing shop.

The target is a narrow class of repeatable micro-workflows where the customer pays for a measurable outcome.

## 2. Evidence already strong enough to justify investigation

The following are observations, not proof of product-market fit.

### E1 — ASEAN MSMEs face affordability / capability / trust barriers to AI adoption

ADB's 2026 analysis of MSME AI adoption in Southeast Asia identifies four persistent barriers: access and affordability, capabilities and skills, awareness/use-case relevance, and trust/safety/governance. It explicitly recommends low-cost, low-code and pay-as-you-go adoption paths for MSMEs.

Source: Asian Development Bank, *From Generative to Agentic: The Next Phase of AI Adoption for MSMEs*, 2026.

### E2 — ASEAN policy explicitly prioritizes MSME digital transformation and market participation

ASEAN's Strategic Action Plan on MSME Development 2026–2030 includes accelerating digital and technology transformation, increasing participation in regional/global markets, building digital-economy capability, and supporting micro businesses in adding value to exports through digitalisation.

Source: ASEAN Secretariat, SAP MSMED 2030 priority areas.

### E3 — Cross-border trade remains documentation / rules / digitalisation intensive

ASEAN Customs' 2026–2030 programme prioritizes simplifying and modernising customs procedures, digitalisation, customs automation, trade facilitation and border security. ASEAN's 2025 digital trade-facilitation report still identifies policy, legal and technical obstacles and capacity-building needs even though overall implementation has improved.

Sources: ASEAN Customs 2026–2030 Strategic Plans of Customs Development; ASEAN Digital and Sustainable Trade Facilitation 2025.

### E4 — MSME difficulty navigating trade rules is explicitly recognised

ASEAN's 2026 business materials on the upgraded ATIGA state that MSMEs face distinct difficulties using trade agreements and describe the need for actionable guidance on preferential treatment, rules of origin and customs facilitation for businesses with limited trade-compliance resources.

Source: ASEAN for Business Bulletin, First Edition 2026.

### E5 — Cross-border e-commerce barriers are current and validated by stakeholders

ASEAN reported in June 2026 that ITC had developed an analysis of MSME cross-border e-commerce challenges, with findings and proposed priority actions validated by more than 100 stakeholders across government, business-support organisations, marketplaces, technology companies and service providers.

Source: ASEAN Secretariat, International MSME Day 2026.

### E6 — China–ASEAN AI cooperation is explicitly moving toward use cases, demand matching and compliance

China–ASEAN AI cooperation bodies formed in 2026 are publicly emphasizing application scenarios, demand matching, standards/rules coordination, compliance co-building and ASEAN market expansion. Guangxi policy materials specifically name multilingual AI, intelligent customs declaration, overseas-warehouse management, cross-border payment, data compliance and smart-port scenarios.

Sources: PRC MIIT / China–ASEAN AI Center materials; China–ASEAN Business & Investment Summit; Guangxi CPPCC 2026 proposals.

## 3. Core hypothesis

There exists a set of cross-border workflows with the following structure:

```text
SME / trader / service operator experiences repeated friction
        ↓
Existing solution = manual staff + spreadsheets + messaging + broker / consultant + portal hopping
        ↓
Heavy enterprise software is excessive / too broad / too expensive / too difficult to deploy
        ↓
A bounded AI-assisted workflow can reduce time, error, search or coordination cost
        ↓
Human expert remains in the loop where legal / customs / accounting / certification judgment is regulated
        ↓
Customer pays for a specific output or recurring workflow
```

The hypothesis is **not proven** until payment evidence exists.

## 4. First candidate problem clusters

These are hypotheses to investigate, not claims of validated demand.

1. Commercial invoice / packing-list / bill-of-lading consistency pre-check
2. Missing-field detection before customs submission
3. Product-description normalization for customs / logistics documents
4. HS-code research assistant with mandatory expert confirmation
5. Rules-of-origin eligibility checklist
6. Preferential-tariff evidence pack preparation
7. Certificate-of-origin document readiness check
8. Country-specific import requirement checklist
9. Product label / packaging requirement checklist
10. Certification / permit requirement triage
11. Regulatory-change watch mapped to a company's SKU list
12. Trade-policy / tariff change impact summary for a specific product
13. Multilingual inbound inquiry extraction and structured RFQ creation
14. Multilingual quotation drafting with terminology control
15. WhatsApp / email follow-up queue extraction
16. Buyer question → internal owner routing
17. Export quotation completeness / Incoterms consistency check
18. Freight quote comparison normalization
19. Shipment exception / delay message summarization and customer update drafting
20. Overseas-warehouse inventory exception detection
21. Marketplace listing localization and required-field validation
22. Cross-border return / complaint case intake and evidence pack
23. Cross-border e-payment reconciliation / exception triage
24. Trade-finance document checklist and discrepancy pre-screen
25. Supplier / buyer due-diligence evidence collection assistant
26. Cross-border data-transfer / privacy checklist for small deployments
27. AI-use governance checklist for SME deployments
28. Export-readiness checklist for first-time exporters
29. Tender / procurement notice extraction into actionable requirements
30. Repeated compliance Q&A knowledge base built from verified expert answers

## 5. Narrowest starting wedge

Default first wedge for field validation:

> **Xuzhou engineering-machinery / component SMEs exporting to Malaysia: document + market-entry compliance pre-check.**

Why this wedge:

- Xuzhou provides local access to a dense manufacturing ecosystem;
- Malaysia is strategically relevant to the operator's planned location and can later support in-person validation;
- documents and compliance create bounded artifacts that can be inspected and verified;
- the workflow can begin manually with AI assistance before product software exists;
- regulated judgments can remain with qualified customs / legal / certification professionals.

This wedge is provisional and must lose priority if another microflow shows stronger payment evidence.

## 6. Actor model

Potential `NEED_ACTOR`:
- export clerk / foreign-trade salesperson;
- owner of a small exporter;
- freight forwarder / customs-service operator;
- marketplace cross-border seller;
- ASEAN importer / distributor.

Potential `PAYER`:
- exporting SME;
- importer / distributor;
- freight forwarder / customs-service firm;
- cross-border e-commerce merchant;
- occasionally a platform / business-support organisation.

Potential `CAPABILITY_PROVIDER`:
- AI / LLM workflow;
- trained operator;
- customs broker;
- certification consultant;
- trade lawyer / accountant where required;
- bilingual student / freelancer for bounded non-regulated tasks.

`ORCHESTRATOR`:
- Opportunity Routing Engine operator.

## 7. Hard commercial gates

Before any candidate becomes `TRANSACTION_TEST`, require:

- `G0 Actor clarity = PASS`
- `G1 Payer clarity = PASS`
- `G2 Transactionability = PASS`
- `G3 Legal/trust/safety = PASS or CONDITIONAL with explicit boundary`
- at least one concrete current workaround or substitute;
- at least one observable cost: money, staff-hours, delay, error/rework or risk;
- a bounded deliverable;
- a price hypothesis;
- a real prospect willing to inspect / trial / pay.

`UNKNOWN != PASS`.

## 8. Five execution phases

### Phase A — Evidence mining

Target: **50 problem records**.

Each record must capture actor, payer hypothesis, workflow, current workaround, source, observed cost, frequency evidence, regulatory boundary and confidence.

Stop rule: do not call a problem "real demand" merely because an official policy document mentions the domain.

### Phase B — Rank and select

Use the canonical scorecard.

Target output:
- top 10 for targeted interviews;
- top 3 for concierge test design;
- explicit rejection reasons for low-ranked candidates.

### Phase C — Field / remote validation

For each top candidate:
- 5–10 conversations with actual operators / payers;
- obtain real anonymised workflow examples where lawful;
- document current workaround and time / money cost;
- ask for a concrete paid or deposit-backed trial rather than generic interest.

Xuzhou allows local visits. Remote validation can target forwarders, trade-service firms and ASEAN-side operators.

### Phase D — Paid concierge test

Deliver manually with AI assistance first.

Example deliverable:
- uploaded document set;
- consistency / missing-item report;
- requirements checklist;
- source-backed risk flags;
- questions that must be escalated to a qualified professional;
- turnaround-time and acceptance criteria.

The tool must never present itself as customs / legal / certification authority.

### Phase E — Automation only after repetition

Only automate the repeated bottleneck that survives paid tests.

Candidate automation order:
1. structured intake;
2. document extraction;
3. deterministic cross-document checks;
4. source retrieval / provenance;
5. workflow routing;
6. audit trail;
7. expert escalation;
8. reusable customer / SKU knowledge.

## 9. 30-day measurable objective

Success is not "software finished".

Success means:
- >= 50 evidence records;
- >= 20 records with at least medium evidence confidence;
- >= 15 real conversations with need actors / payers / providers;
- >= 5 real workflow samples or detailed walkthroughs;
- >= 3 explicit price conversations;
- >= 1 paid or deposit-backed concierge test;
- one ranked decision: `BUILD_NARROW`, `KEEP_MANUAL`, `PIVOT_MICROFLOW`, or `REJECT_VERTICAL`.

## 10. Safety / compliance boundary

The system may assist with retrieval, extraction, comparison, checklisting and evidence organisation.

It must not silently replace licensed / accountable professional judgment. Customs classification, legal advice, tax treatment, certification conclusions, sanctions/export-control decisions and other regulated determinations require explicit source provenance and, where appropriate, qualified human confirmation.

## 11. Current decision

`GO: INVESTIGATE AND VALIDATE`.

Do **not** yet build a broad SaaS product.

Build only the evidence pipeline and ranking tooling needed to discover which microflow deserves a paid test.