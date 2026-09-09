# Transaction Gap Thesis

Status: `ACTIVE WORKING THESIS`

Last updated: 2026-09-10

## Purpose

The Opportunity Routing Engine should not only ask whether demand and supply exist. Many markets already contain both, yet transactions still fail because the mechanism between actors is weak, the payer is misidentified, or a structural shift has changed the economics.

This document defines the canonical gap ontology used in broad scans, opportunity records and field validation.

A gap is not a business by itself. It is a hypothesis about **where value may be created by making a transaction possible, safer, cheaper, faster, clearer or better aligned with the actor who captures the benefit.**

## 1. Canonical gap ontology

### G01 — `DEMAND_GAP`
A meaningful outcome is repeatedly wanted but current supply is missing, insufficient, poorly fitted or inaccessible.

Core question:
> What outcome is repeatedly wanted but still hard to obtain?

Evidence to prefer:
- purchases of imperfect substitutes;
- repeated waiting / travel / manual effort;
- failed attempts to obtain the outcome;
- repeated requests or bookings that exceed supply.

### G02 — `CAPABILITY_GAP`
Useful skill, labor, knowledge, equipment, inventory, space, time or another resource exists but is underused, poorly packaged, hard to discover or disconnected from a payer.

Examples:
- trained students cannot convert skill into accepted paid output;
- a specialist has fragmented idle time;
- a merchant has off-peak space;
- equipment is idle while another actor needs temporary or transferred capacity.

Core question:
> What useful capability is idle, and who is already paying elsewhere for the same outcome?

### G03 — `PRICE_GAP`
The desired outcome exists, but the incumbent cost structure is misaligned with the payer's willingness or ability to pay.

Common migrations:
- premium → value-for-money;
- ownership → rental / shared access;
- replacement → repair / verified second-hand;
- full-time headcount → bounded project;
- large commitment → trial / pay-per-use;
- manual expert-heavy workflow → deterministic + AI-assisted workflow with expert escalation.

Core question:
> Can the same outcome be delivered with a structurally lower total cost, not merely a lower margin?

### G04 — `TRUST_GAP`
Demand and supply both exist, but actors hesitate to transact because identity, quality, safety, responsibility, evidence or recourse are unclear.

Typical trust components:
- identity / qualification verification;
- service checklist;
- explicit scope and acceptance criteria;
- timestamped / auditable evidence;
- privacy and access boundaries;
- deposit / payment / cancellation rules;
- abnormal-event escalation;
- service history / reputation;
- dispute / refund boundaries;
- insurance or qualified-party routing where appropriate.

Core question:
> If both sides already exist, what prevents a stranger-to-stranger transaction from feeling safe enough to happen?

### G05 — `INFORMATION_GAP`
Actors could transact, but one or both sides lack decision-grade information: availability, quality, price, requirements, compatibility, provenance, condition, eligibility or status.

Information alone is weak value if a search engine or incumbent already solves it cheaply. The opportunity becomes stronger when information is converted into a verified decision or transaction artifact.

Core question:
> Which missing fact repeatedly blocks a real decision, and will someone pay to know or verify it?

### G06 — `GEOGRAPHY_GAP`
Capability, inventory, demand or trusted execution exists in one place while the paying need exists elsewhere.

Examples:
- a remote buyer needs local verification;
- an asset is valuable to buyers outside the immediate area;
- a service must be performed near the need actor;
- a cross-region information or execution gap prevents exchange.

Core question:
> Is physical locality itself scarce enough to command payment after travel/logistics costs?

### G07 — `TIME_GAP`
The right capability or asset exists, but availability is misaligned with when the need occurs.

Examples:
- holiday pet-care peaks;
- merchant space is idle off-peak while peak periods are full;
- a buyer needs same-day verification;
- a worker has fragmented hours that conventional employment cannot use.

Core question:
> Is timing mismatch causing enough cost, delay or lost revenue to support a transaction?

### G08 — `COORDINATION_GAP`
The solution requires multiple small actions, actors or providers whose individual components exist but are costly to coordinate.

Potential orchestrator value:
- requirement definition;
- task decomposition;
- sequencing;
- provider routing;
- QA / acceptance;
- exception handling;
- payment coordination;
- outcome evidence.

Core question:
> Is the buyer paying for the underlying work, or for not having to coordinate the work themselves?

### G09 — `PAYER_SHIFT`
The need actor or beneficiary is not the economically strongest payer. Another actor captures enough value or avoids enough loss to pay or subsidize the transaction.

Examples:
- elderly beneficiary → adult child / institution payer;
- learner beneficiary → employer / training institution / sponsor payer;
- youth participant → venue payer because qualified foot traffic has value;
- resident beneficiary → government / community procurement;
- end user → supplier / advertiser / transaction counterparty.

Core question:
> Who gains or avoids loss when the need is solved, even if they do not consume the service directly?

`PAYER_SHIFT` does not pass merely because a sponsor exists in theory. The sponsor's economic incentive and actual commitment must be observed.

### G10 — `TECHNOLOGY_SHIFT`
A technology change makes an old outcome newly affordable, fast, measurable or routable enough to support a transaction that previously did not work economically.

Examples:
- AI reduces research / extraction / classification cost;
- low-code tools reduce setup cost;
- inexpensive verification technology improves auditability;
- new digital infrastructure reduces search or payment friction.

Core question:
> Does technology change the unit economics or transaction boundary, or merely make the demo look impressive?

`TECHNOLOGY_SHIFT` is an enabler, not payment evidence.

## 2. Multiple gaps may coexist

A serious opportunity may contain several gaps. Record one `PRIMARY_GAP` and zero or more `SECONDARY_GAPS`.

Example:

```text
Pet owner needs temporary care
→ supply exists
→ holiday availability is uneven          TIME_GAP
→ stranger enters home                    TRUST_GAP
→ owner must coordinate instructions      COORDINATION_GAP
→ payment already occurs                  PAYMENT EVIDENCE
```

The commercial question is which gap the payer will actually pay the orchestrator to reduce.

## 3. Public / free provision rule

Government, community, school or nonprofit provision has two meanings at once:

1. it is evidence that the underlying need exists;
2. it is an incumbent / substitute that may destroy direct consumer willingness to pay.

Therefore:
- never count public provision as direct private willingness-to-pay evidence;
- downgrade direct-pay hypotheses when free supply solves the same outcome adequately;
- test `PAYER_SHIFT` when the institution itself has an explicit budget or outcome incentive;
- look for residual gaps in timing, quality, niche fit, convenience, trust or continuity rather than duplicating a free service.

## 4. Outcome-linked sponsor rule

A third-party payer becomes especially important when its own economics are explicitly linked to the beneficiary's outcome.

Examples:
- a venue receives incremental traffic / revenue from an activity;
- a training institution receives outcome-linked support when learners achieve stable employment;
- an institution purchases a defined public service for a beneficiary group.

This is stronger than a generic statement that a sponsor "might pay", but it is still not a PASS until the exact payer accepts the proposed transaction.

## 5. Orchestrator value

The engine should ask what value remains after simple introductions are removed.

Strong orchestrator value may include:
- demand clarification;
- requirement standardization;
- trust creation;
- capability screening;
- composite routing;
- fixed deliverables;
- QA;
- evidence capture;
- exception handling;
- payment coordination;
- outcome history;
- repeated learning.

Weak orchestrator value:
> "I know someone; here is their contact information."

## 6. Canonical gap record

Every serious opportunity should include:

```text
Need actor:
Beneficiary:
Payer:
Capability provider:
Resource owner / sponsor:
Primary gap:
Secondary gaps:
Change:
Observed behavior:
Current workaround:
Economic cost / payment evidence:
Why the transaction does not already happen efficiently:
Orchestrator value:
Hard gates:
Cheapest decisive test:
Outcome:
Learning:
```

## 7. Gap-to-field rule

Every unresolved gap should be translated into a field-verifiable unknown.

Weak:
> Trust seems important.

Strong:
> Of 15 pet owners who previously paid or used a costly workaround, how many refuse an unknown sitter specifically because of home-entry risk, and how many will place a real booking/deposit when identity, checklist, evidence and exception rules are defined?

Weak:
> Young people like experiences.

Strong:
> For one defined 8–15 person event, can either six participants place real deposits at the test price or one venue commit real money / a minimum guarantee because the expected qualified foot traffic has measurable value?

## 8. Governing principle

**Do not assume opportunity requires missing supply. The value may be in reducing a demand, capability, price, trust, information, geography, time, coordination or payer mismatch — sometimes unlocked by a technology shift. Real behavior and real money decide whether the gap is commercially meaningful.**
