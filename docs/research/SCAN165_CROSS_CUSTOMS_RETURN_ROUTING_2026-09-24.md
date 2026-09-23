# Scan 165 — 9610 cross-customs return routing

Date: 2026-09-24  
Source main: `d64cdd82abc27e15506df83685a8abfbc4b9b7be`

## Why this scan moved up a level

Scan163–164 showed that the obvious "China local helper / sourcing / QC / visit / after-sales" menu is already mature.

Scan165 therefore searches state changes where the value is in **routing an asset or regulatory choice**, not sending another person to do work.

## Retained research beacon — F1

On 2026-04-01, China expanded 9610 cross-customs-district returns nationwide. A returned retail-export parcel no longer has to re-enter through the original export customs district. The enterprise may choose another eligible return port / supervised operation site.

The official interpretation explicitly frames the choice around **logistics cost and time** and reports 381,300 return tickets worth RMB 94 million during the earlier pilot period.

Current operating examples make the value jump concrete:
- Shandong Post + AliExpress + customs completed 272 returns through Jinan and estimated comprehensive logistics cost reduction above 30%.
- Shaanxi's September 2026 first case reported roughly 50% savings in capital and time cost.
- Shenzhen publicly exposes an operational 9610 return rail alongside other cross-border ecommerce modes.

This creates a candidate bridge:

```text
RETURN BATCH
+ EXPORT MODE / AGE / ORIGINAL STATE
+ OVERSEAS LOCATION
+ ELIGIBLE CHINA RETURN SITES
+ LIVE LOGISTICS COST / TIME / SITE CAPABILITY
→ ROUTE TO THE BEST VALID RETURN ENTRY
```

The candidate is **research-only**, not a commercial candidate.

## Decisive unknown

The policy says the enterprise may choose. That does not prove the seller has a commercially movable choice in practice.

The next question is:

> Do sellers or their logistics partners retain a real cross-port choice with comparable route data, or do platform/carrier/supervised-site contracts effectively preassign the return port?

If platform/carrier routing already fixes the path, F1 closes.

If the choice is real but every comparison requires recurring customs-broker judgment, F1 also closes as expert-bound.

Only if the choice is real, recurring and resolvable from stable route attributes does a distinct routing layer survive.

## Four fresh closures

- **F2 return-value recovery/disposition** — rturn and current fulfillment operators already own intake → inspection → recovery value → disposition.
- **F3 CBAM producer-to-importer data handoff** — the EU O3CI registry is the official data rail; current Chinese CBAM platforms already package calculation/data/consultant coordination.
- **F4 buyer-owned tooling transfer** — current handover and mold-transfer services already package audit, release, logistics, trial and restart; disputes remain expert/legal.
- **F5 remote China-warehouse return** — current warehouse accounts already support remote courier return, tracking, logs and photo evidence.

## Current truth

- high-attraction research beacons: **1**
- retained research formations: **1**
- commercial candidates: **0**
- transaction units: **0**
- bootstrap tasks authorized: **0**
- FIRST_EXTERNAL_VALUE_FLOW: **NOT_PROVEN**

No outreach, quote request, registration, payment or other external side effect occurred.

## Next action

Freeze one exact PR head and run repository CI + live TypeSafe/Jev. Consume only a reversible advisory route. Do not contact logistics providers or sellers until the exact-head research advisory says the retained formation still deserves that validation capital.
