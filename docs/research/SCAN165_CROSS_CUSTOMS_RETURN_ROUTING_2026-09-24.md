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


## Exact incumbent / route-ownership preflight

The exact-head Scan165 advisory returned one reversible route for F1: `EXACT_INCUMBENT_PREFLIGHT`.

The preflight confirmed that policy optionality is real, but did **not** confirm a distinct callable routing market:

- In Hangzhou's first nationwide-mode case, the AliExpress representative says the **platform** can choose the return plan and convenient port; airport logistics and customs jointly built the operating plan.
- Jinan's live flow was created through a Shandong Post + AliExpress + local government + customs operating mechanism with repeated declaration/clearance drills.
- Guangdong Post's current cross-border customs system integrates customs, China Post's 9610 system and partner brokers into a full-process closed loop including return declaration.
- Current 9610 system vendors already support multi-port / nationwide customs workflows and return documents, but their public surfaces are execution systems, not neutral live cross-port quote/capacity markets.
- Current port-local return centers can provide full-chain reverse-logistics execution to sellers nationwide.

No public source found a stable independent surface exposing, across eligible return ports, the current all-in cost, route SLA, supervised-site capacity, customs-operating constraints and a repeatable booking/settlement action.

Therefore the original F1 scores for operator control, match resolvability, action-gate callability and recurring missing edge were too optimistic.

```text
POLICY OPTIONALITY
!= PUBLIC COMPARABLE ROUTE DATA
!= OPERATOR CONTROL
!= CALLABLE CROSS-PORT MARKET
```

The scan now fails closed on those dimensions.

## Final Scan165 truth

- high-attraction beacons: **0**
- retained research formations: **0**
- authoritative closures: **F1-F5**
- commercial candidates: **0**
- transaction units: **0**
- bootstrap tasks authorized: **0**
- FIRST_EXTERNAL_VALUE_FLOW: **NOT_PROVEN**

F1 is closed as:

`DEMOTED_POLICY_OPTIONALITY_IS_REAL_BUT_DISTINCT_OPERATOR_CONTROL_MATCH_RESOLVABILITY_AND_CROSS_PORT_ACTION_RAIL_ARE_NOT_EVIDENCED`

No outreach, provider quote request, registration, payment or other external side effect occurred.

The next scan should not reinterpret policy optionality itself as an opportunity. It must search for another actor state transition where the missing edge is already observable and the control/action surface is actually ownable.
