# Connection Pressure Scan 020 — Failed Exchange Ledger

Observed: 2026-09-18

## Why this scan exists

A failed procurement already contains a real buyer, a defined task, a budget or price boundary, a deadline and a failed exchange.

That makes it a high-information sensor — but also a dangerous source of false positives.

Hard rule:

~~~text
PROCUREMENT_FAILED != MARKET_GAP
~~~

The system must identify why the exchange failed before treating it as connection pressure.

This scan does not create a government-procurement business thesis.

## Case 1 — same buyer, same round, mixed success and failure

Xuzhou's 2026 fiscal-information-service tender had four packages.

Budget:
- package 1: RMB 870,000
- package 2: RMB 490,000
- package 3: RMB 389,500
- package 4: RMB 298,000

Package 2 succeeded at RMB 440,000.

Packages 1, 3 and 4 were voided because valid bidders were fewer than three.

Sources:
- https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004002/20260810/07096141-325e-4ee6-a349-19235b531349.html
- https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260901/6372d6e3-9ee9-4c10-b855-c210c30ee692.html

The buyer re-tendered the failed scopes the next day at essentially the same budget levels. The second deadline is 2026-09-24 and is still in the future at this scan time.

Source:
- https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004002/20260902/98623c73-449c-44e5-b72a-a94ec203ba92.html

Reading: the failure is package/interface specific. Do not infer a generic Xuzhou IT-supply gap and do not pre-claim second-round success.

## Case 2 — capability existed; evidence acceptance killed the exchange

The Hanwang water-supply design project initially had four scored bidders.

After review, two bidders were judged ineligible because the required social-security proof for the entrusted agent had not been provided. Fewer than three compliant bidders remained, so the tender failed.

Sources:
- https://ggzy.zwb.xz.gov.cn/jyxx/003003/003003003/20250611/f9f7305b-acaf-4268-b074-27a0072e18b0.html
- https://ggzy.zwb.xz.gov.cn/jyxx/003003/003003003/20250619/0332c617-d4ca-44d0-9610-34ce9d9547b7.html

The project was later re-tendered and successfully awarded to 徐州市水利建筑设计研究院有限公司 at a 1.8% fee rate.

Source:
- https://ggzy.zwb.xz.gov.cn/jyxx/003003/003003004/20250729/f80f3c7c-671b-40e7-8faa-c438eec5ec8e.html

The first failure therefore cannot be read as missing design capability. The market contained capable actors; the first exchange failed at an evidence / eligibility acceptance boundary.

Public evidence obtained here does not prove that the second tender relaxed the proof rule.

Therefore:

~~~text
RETRY_SUCCESS
!=
PROOF_THAT_THRESHOLD_WAS_LOWERED
~~~

## Case 3 — repeated low participation under materially similar terms

The Social Governance Procuratorial Case-Handling Center procurement used:
- RMB 1.03 million budget;
- no consortium;
- construction or decoration qualification;
- a qualified project manager;
- safety-production license.

The first procurement, JSZC-320305-YXHC-C2026-0003, was terminated because suppliers were fewer than three.

The second procurement, JSZC-320305-YXHC-C2026-0004, kept the same budget and materially the same published qualification bundle and was publicly indexed as terminated again on 2026-09-14.

Sources:
- https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004002/20260818/f61dae68-c496-4d1c-b4e6-7602ee5ab6d8.html
- https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004002/20260902/d9f3315d-e87c-4143-8714-047fab10d590.html
- https://www.ixbang.com/govbid/r320305/

This is a stronger residual sensor than a one-off failure.

But cause is still unknown.

Possible explanations:
- eligible bidder population;
- scope economics;
- responsibility bundle;
- timing;
- qualification constraints;
- procurement visibility;
- payment terms;
- other bidder opportunity costs.

None is proven.

~~~text
REPEATED_FAILURE != KNOWN_CAUSE
~~~

## Case 4 — the same service category can succeed one year and fail another

Xuzhou's 2026 environmental-impact-assessment technical-review procurement had one package succeed and two packages fail because valid supplier count was below three.

The previous year's same general service category had all three packages successfully awarded.

Sources:
- https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004002/20260513/a9ea112b-1b58-4feb-a155-3fdad5e2b780.html
- https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260604/be305043-4308-4547-9945-6b0f9b840bcf.html

A failed package therefore does not automatically establish a durable capability gap. Supplier availability, package design, price, workload and timing may vary.

## Case 5 — one supplier can fail while the market works

In the 2026 Gulou community fitness-center survey/design procurement, one design institute's bid was rejected because its price exceeded the maximum.

Three other valid bids remained and a winning candidate was selected.

Source:
- https://ggzy.zwb.xz.gov.cn/jyxx/003001/003001007/20260605/94551942-4ae5-4e44-a676-d9b479f8b9e3.html

Therefore:

~~~text
ACTOR_OFFER_REJECTED
!=
MARKET_FAILURE
~~~

# Analytical classification — evidence triage only

These labels are not a new ontology.

### PARTICIPATION_SHORTAGE

Too few counterparties submitted or survived evaluation.

It identifies the immediate event, not the underlying cause.

### EVIDENCE_OR_ELIGIBILITY_REJECTION

Actors or capability may exist, but the receiver does not accept their proof / formal state.

### PRICE_BOUNDARY_REJECTION

The offer exceeds the buyer's permitted or economically acceptable boundary.

### ACCEPTANCE_INTERFACE_MISMATCH

The capability, deliverable or evidence exists but does not map to the receiver's required representation.

### RESPONSIBILITY_OR_SCOPE_BURDEN

A task bundle may combine obligations that sharply reduce callable supply.

This must be evidenced, not assumed.

### PROCEDURAL_OR_BUYER_TERMINATION

The exchange stops for procedural or buyer-side reasons and tells us little about supply.

### PERSISTENT_INTERFACE_FAILURE

A materially similar exchange is retried and still fails.

This deserves deeper research but still does not reveal cause by itself.

# The highest-value object is the retry delta

When an exchange fails and is retried, compare:
- budget;
- scope;
- package size;
- qualification;
- accepted evidence;
- consortium or subcontracting rules;
- response window;
- delivery period;
- payment;
- risk allocation;
- acceptance terms;
- bidder population.

The useful sequence is:

~~~text
FAILED_EXCHANGE
↓
OBSERVED_BOUNDARY
↓
INTERFACE_OR_TERMS_CHANGE
↓
SUCCESSFUL_EXCHANGE
~~~

Only when the changed boundary can be identified do we learn a reusable natural-formation mechanism.

# Promotion gate

A failed-exchange record becomes worth field validation only with:

~~~text
REAL_REPEATED_DEMAND
+
STABLE_IDENTIFIABLE_FAILURE_BOUNDARY
+
MEASURABLE_ACTOR_COST_OR_DELAY
+
LAWFUL_CHANGEABLE_BOUNDARY
+
PARTIAL_FLOW_OR_SUCCESSFUL_RETRY_AFTER_CHANGE
~~~

Without this:

~~~text
FAILED_PROCUREMENT = SENSOR_ONLY
~~~

## Closures

Do not build:
- generic government-procurement lead generation;
- failed-tender supplier matching;
- a bidder marketplace inferred from insufficient-three-bidder events;
- a business thesis from one invalid or overpriced bid.

## Next highest-information data

1. Xuzhou retry pairs where failed and successful tender documents expose a clear interface delta.
2. Repeated low-participation projects where buyer-side delay or cost is observable.
3. Private B2B failed exchanges with non-procedural causes.
4. Scene / technology-demand records that timeout, get re-scoped or require manual translation before match.
5. Post-verification residue after certification, trial work or inspection.

## Field truth

Two direct capability-proof employer probes remain sent.

Qualified human responses last checked: 0.

~~~text
FAILED_EXCHANGE_PUBLIC_EVIDENCE
!=
FIRST_EXTERNAL_VALUE_FLOW
~~~

Issue #143 stays open.
