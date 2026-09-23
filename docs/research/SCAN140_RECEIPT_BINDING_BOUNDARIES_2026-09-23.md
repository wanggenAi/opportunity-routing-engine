# Scan 140 — receipt-binding boundaries — 2026-09-23

## Result

Scan 140 tested fresh current Chinese formations without reusing Scan 060–139 addresses or case IDs. It deliberately compared four different receipt-control shapes: a whole-title lease with an unpaid future tail, a 25% fractional title against a whole-asset lease, owners-committee pooled rent distribution, and a fully prepaid lease.

Only **ATTRACTION_SCAN_140-F1** is retained for research. Nothing is promoted commercially and FIRST_EXTERNAL_VALUE_FLOW remains NOT_PROVEN.

## F1 — Weiyuan Lanhuajie 46

The current first auction is scheduled for 2026-10-18. Public material binds a RMB445,886.28 floor, RMB6,000/month rent paid quarterly, lease end 2029-02-24 and rent paid through 2026-11-30. Surface annual rent/floor is about 16.15%.

The decisive missing fact is not price or rent. It is **buyer-side receipt succession**: the public notice does not say that post-transfer rent belongs to the buyer or bind the first unprepaid payment to the buyer. This is therefore research-only.

## F2 — Fuding 25% title share

The current 60-day sale runs through 2026-10-23 at RMB441,156. The lease on the whole room runs to 2030-04-30 and public material reports RMB40,000/year contractual rent but RMB30,000/year actual execution, paid through 2026-10-30.

The acquired object is only a **25% ownership share**. No public source binds a specific rent share or collection right to that fractional buyer. Pro-rata attribution would be inference, not evidence, so the formation closes.

## F3 — Nanchong pooled rent distribution

The official Nanhai Court sale remains open through 2026-10-23 at RMB128,004. The court states that the owners committee centrally leases and collects rent, then distributes it annually by owned area; lease end is 2029-12-19.

This is a stronger control mechanism than unit-by-unit collection, but the exact distributable pool and these three titles' distribution quantum are not public. Economics therefore cannot be computed and the formation closes.

## F4 — Shanghai fully prepaid lease

The current Pudong auction starts 2026-10-12 at RMB1,010,000. Existing rent is RMB75,000/year, but the tenant has already paid through 2027-01-19 — the exact lease end.

The apparent ~7.43% historical rent/floor ratio is not buyer cashflow. There is no unprepaid contracted receipt left under the current lease, so the formation closes.

## Guardrails

UNKNOWN is not PASS. Whole-asset receipts are not assigned to fractional title without a source. Prepaid historical rent is not counted as buyer cashflow. No bid, deposit, purchase, inspection or external contact is authorized.

## Next

Freeze the final PR head, require repository CI plus live TypeSafe/Jev against ATTRACTION_SCAN_140, consume any reversible public F1 route, and only then decide whether Scan 141 may advance.


## Live Jev causal-descent update

Exact head `6b57d4c502104e1c6a24f481ddac7aaa52926bdc` passed repository CI `35842823646` and live TypeSafe/Jev `35842823841`. Jev routed only F1 to `CAUSAL_DESCENT`; F2-F4 stayed `NO_FURTHER_RESEARCH`.

The follow-up found Supreme People's Court reference case `2024-17-5-203-007`. That authority materially advances F1: when a judicial-auction notice discloses an existing lease but does not separately allocate post-auction rent, the buyer generally succeeds the original landlord position and enjoys rent after ownership transfers. The transfer boundary is service of the auction-completion adjudication.

This supersedes the narrower sentence above that buyer-side receipt succession is wholly unbound. The **remaining** fail-closed boundary is case-specific: the Weiyuan auction has not yet occurred, so there is no actual adjudication-service date; rent is already paid through 2026-11-30; the public record does not bind prepaid-rent apportionment or the exact first unprepaid quarterly due date.

Detailed evidence and decision: `data/research_runs/scan140_f1_causal_descent_evidence.json` and `docs/research/SCAN140_F1_CAUSAL_DESCENT_2026-09-23.md`.

F1 remains research-only. No commercial promotion or external side effect is authorized.
