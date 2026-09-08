# Xuzhou Transaction Gap Scan V2 — 2026-09-08

Status: `PRELIMINARY / EVIDENCE-BACKED / FIELD VALIDATION REQUIRED`

This scan supplements the actor-first ranking by classifying opportunities through four gap types:

- demand gap;
- capability gap;
- price/economic gap;
- trust gap.

It also tests payer-shift / sponsor structures.

## 1. Strong current signals

### A. Pet economy + trust gap

Xuzhou is explicitly supporting pet-economy consumption, and current public reporting shows a large local pet base and rapid growth in pet-service infrastructure. National reporting on paid at-home pet feeding shows strong demand but repeated problems around privacy, home access, service standards and liability.

Opportunity thesis:

```text
Pet owner / payer
→ needs temporary care
→ provider supply already exists
→ transaction blocked by TRUST
→ orchestrator adds verification + checklist + evidence + history + exception rules
```

Decision: `FIELD TEST NOW` through EXP-004; no app build.

## 2. Youth experience + venue-sponsored payer shift

Xuzhou is actively building youth-economy and night-economy scenes. The local `night school + youth shop` model demonstrates that a merchant can receive measurable commercial value from youth activities; one published Xuzhou example reported roughly 30% store revenue growth over two months after hosting classes, while 12 linked youth-shop sites reached roughly 600 attendances.

This creates two possible payer models:

### Direct participant payer
```text
Young person needs social / interest experience
→ pays small ticket
→ venue / instructor / organizer delivers
```

### Venue-sponsored / multi-sided payer
```text
Young person receives low-cost or free experience
→ venue receives foot traffic + conversion
→ venue pays / subsidizes organizer
```

The second structure may outperform pure ticketing if youth willingness to pay is weak but merchant traffic value is strong.

Key unknowns:
- participant willingness to pay at RMB 29 / 49 / 79;
- merchant willingness to pay fixed sponsorship, minimum guarantee, or revenue share;
- repeat conversion after an event;
- whether public/free programs suppress private willingness to pay.

Decision: `B: INVESTIGATE` with no-code event test.

## 3. Skills-to-income capability gap

Xuzhou's 2026 skills-night-school expansion provides unusually visible evidence of capability creation:
- initial courses attracted 170+ participants;
- later monthly plans reached 33 courses and 600+ planned learners;
- training includes AI, AIGC, drones, repair, ecommerce, elder care, storage/organization and other practical skills;
- youth flexible employment is already material in scale.

Opportunity thesis:

```text
Learner / capability provider
→ gains skill
→ wants income / portfolio / first real task
→ payer is elsewhere
→ missing layer = project packaging + trust + QA + payer access
```

This is not a training business by default. The opportunity is potentially in converting trained but under-monetized capability into a defined result for a payer.

Key risk: collapse into low-value recruitment/freelance marketplace.

Decision: keep as high-potential `CAPABILITY GAP`, but payer must be discovered per task class.

## 4. Elder services + payer-shift evidence

Xuzhou is expanding home/community elder-service infrastructure and explicitly plans further growth in home services, caregiver training and silver-economy services. Existing Xuzhou procurement has paid providers for home elder services; elsewhere in Jiangsu, 2026 reforms are increasingly using consumer vouchers and government purchasing to let older residents choose among providers.

Actor structure:

```text
Need actor / beneficiary: elderly person
Payer candidates:
- adult child
- government / voucher
- institution / community
- elderly person directly
Capability provider: qualified service organization / trained worker
```

The commercial insight is payer separation, not an instruction to enter regulated care directly.

Narrow low-risk opportunity candidates:
- service navigation / comparison;
- appointment / information coordination;
- non-medical digital assistance;
- routing to qualified providers;
- family-facing evidence / status coordination where legally appropriate.

Decision: `WATCH / NARROW TEST ONLY`; broad care delivery remains high-risk.

## 5. Night economy + experience demand gap

Xuzhou's 2026 night economy is strong:
- the city reports thousands of food-service merchants participating in evening demand;
- night tourism and major commercial districts are seeing high traffic;
- outside-city consumption is a meaningful share of core commercial spending;
- cultural, sports, market and youth scenes are being deliberately combined.

Potential opportunity is not another restaurant-discovery app.

More specific wedges:
- micro-events using idle merchant space;
- curated visitor micro-experiences;
- local photographers / guides / makers routed to visitors;
- merchant-sponsored youth community events;
- real-time `what can I do tonight` bundles with transaction rather than content only.

Incumbent discovery platforms are strong, so pure information aggregation is weak.

Decision: only pursue where `transaction + local execution + trust` adds value.

## 6. Value-conscious consumption + price gap

Xuzhou consumer activity remains strong overall, but policy-led trade-in demand demonstrates that consumers respond materially to effective price reduction and certainty. By late May, local trade-in subsidies had used about RMB 460 million and were reported to have driven roughly RMB 4.8 billion in consumption.

This does not prove a generic discount business.

The useful price-gap lens is:
- repair vs replace;
- rental vs ownership;
- verified second-hand vs new;
- shared use vs idle ownership;
- AI/projectized service vs full-time labor;
- off-peak capacity vs peak retail price.

Decision: scan only for categories where cost reduction is structural and current incumbents remain weak.

## 7. Revised cross-opportunity ranking

This is not a full rescoring of every candidate; it is a gap-adjusted field priority ranking.

| Priority | Opportunity | Primary gap | Payer model | Main unknown | Field decision |
|---|---|---|---|---|---|
| 1 | Trusted pet-care transaction layer | TRUST | individual pet owner | premium / booking fee enough to support coordination? | EXP-004 active |
| 2 | Youth micro-experience + merchant sponsor | DEMAND + PAYER SHIFT | participant and/or venue | who pays more reliably? | prepare EXP-005 |
| 3 | Skills-to-income project conversion | CAPABILITY | task-specific buyer | payer density + QA economics | continue discovery |
| 4 | SME bounded micro-projects | PRICE + CAPABILITY | SME / merchant | real fixed-project willingness | EXP-003 active |
| 5 | Narrow elder service navigation | TRUST + PAYER SHIFT | child / government / elder | low-risk unserved layer? | watch / interviews only |
| 6 | Visitor micro-experience routing | DEMAND + TRUST | tourist | acquisition vs OTA/platform incumbents | watch |
| 7 | Verified second-hand / repair routing | PRICE + TRUST | individual | incumbent advantage too strong? | watch |

## 8. New system insight

A useful opportunity engine needs at least three graphs:

```text
ACTOR GRAPH
who has the need / benefit / money / resource

CAPABILITY GRAPH
who or what can solve it

TRANSACTION FRICTION GRAPH
what prevents the two sides from completing a transaction
```

The third graph is critical. Two-sided existence does not imply a market is functioning efficiently.

## 9. Field rule for Xuzhou

Before any in-person visit, define one unknown to resolve.

Every field visit should record:
- actor type;
- exact hypothesis;
- current workaround;
- actual spend / economic cost;
- trust blocker;
- acceptable transaction structure;
- payer identity;
- price signal;
- PASS / FAIL criterion;
- next decision.

Do not collect interviews for their own sake.
