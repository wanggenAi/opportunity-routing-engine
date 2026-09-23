# Scan 141 F1/F2 Jev route consumption — 2026-09-23

## Exact-head advisory consumed

Source head: `f013e028594b54dead62cb272c724fd595636a55`.

- Repository CI run `35847088351`: SUCCESS.
- TypeSafe/Jev run `35847088348`: SUCCESS.
- Artifact `10743748656`, digest `sha256:6c2277721a459b1b22a7b71ee656e227d636fe4d476baf8997f254740b75a5a1`.
- Served model: `jev-1.13.0`.
- F1 fingerprint `049584a3f275632edd7a`: `CAUSAL_DESCENT`.
- F2 fingerprint `8910eb5483f73fd726d5`: `EXACT_INCUMBENT_PREFLIGHT`.
- F3/F4 remain authoritative `NO_FURTHER_RESEARCH` closures.

Jev is shadow research advisory only. It did not mutate commercial state, authorize promotion, or authorize external side effects.

## F1 — Mianyang causal descent

Current public notice mirror:
https://m.fang.com/fapai/mianyang/out_12722428.html

The notice binds RMB284,590 entry, RMB24,000/year rent, rent paid through 2027-06-30, and only month-level lease end `2029-06`.

Exact public searches did not produce a day-precision lease-end date or a first unprepaid due node. `2029-06` must not be rewritten as `2029-06-30`. Transfer / handover language also does not bind case-specific prepaid-rent allocation.

Resolution: public causal descent is exhausted at the underlying lease / rent-ledger boundary. F1 remains research-only.

## F2 — Wuhu exact incumbent preflight

Current public notice mirror:
https://m.fang.com/fapai/wuhu/out_12692605.html

Earlier same-case mirror:
https://m.fang.com/fapai/wuhu/out_12537855.html

The current notice binds RMB299,200 entry, lease 2024-05-01 through 2031-04-30, RMB18,800/year rent and annual settlement. Its platform summary says no priority purchaser, but the embedded court notice body says a masked individual has priority-purchase rights. The notice body is more specific; however, the public source does not establish whether that right-holder is the tenant. The earlier same-case B118 listing used the same case number and economics but left the lease field blank.

The later current notice therefore adds material lease information; the earlier omission is not proof of no lease. Neither public version supplies a current paid-through cursor, first unprepaid buyer receipt, a source-bound tenant/right-holder relationship, or a case-specific payment ledger.

Resolution: exact incumbent preflight is exhausted at the case-specific lease/payment-ledger boundary. F2 remains research-only.

## Commercial result

- Active commercial candidates: 0.
- Active transaction units: 0.
- FIRST_EXTERNAL_VALUE_FLOW: NOT_PROVEN.
- No external contact, inspection, bid, deposit, purchase, or monetary action was performed.

## Next action

Freeze the route-consumption head and require repository CI plus live TypeSafe/Jev on that exact SHA. If the advisory only repeats the already-consumed F1/F2 route classes without new public evidence, merge PR #451 and advance to a fresh Scan 142.
