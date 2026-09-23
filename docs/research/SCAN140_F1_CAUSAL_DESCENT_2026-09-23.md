# Scan 140 F1 — live Jev causal-descent follow-up

Date: 2026-09-23  
Source PR: #450  
Source exact head: `6b57d4c502104e1c6a24f481ddac7aaa52926bdc`  
Result: **public rent-succession rule materially advanced / retained research only / exact buyer receipt window still unbound**

## Live TypeSafe/Jev route

PR #450 exact head `6b57d4c502104e1c6a24f481ddac7aaa52926bdc` passed repository CI run `35842823646` and live TypeSafe/Jev run `35842823841`.

The live run used `ATTRACTION_SCAN_140` with four entities and returned:

- F1: `CAUSAL_DESCENT`
- F2/F3/F4: `NO_FURTHER_RESEARCH`
- continuation: `EXECUTE_RESEARCH_QUEUE`
- autonomous continuation: allowed
- external side effects: not allowed
- commercial promotion authority: false

Artifact: `10741993428`  
Digest: `sha256:4640151e4f82ebf90449694c8f9f8fee5badfb2aeffdec4c2ebe60a15453ea17`  
Served model: `jev-1.13.0`  
F1 state fingerprint: `e2c540f3951363ea7a23`.

## What changed

The original Scan 140 record correctly refused to infer buyer-side rent succession from the Weiyuan notice alone. The live Jev route justified a deeper public-law check.

That check found Supreme People's Court reference case `2024-17-5-203-007`, which addresses the same structural boundary: a judicial-auction notice discloses an existing lease but does not separately allocate post-auction rent. The reference case states that the buyer succeeds the original landlord's rights and obligations and, after ownership transfers, enjoys the rent income right. The Supreme Court interpretation also places the judicial-auction ownership-transfer boundary at service of the auction-completion adjudication.

This is decision-improving evidence. It means the generic proposition **"the buyer cannot be shown to receive post-transfer rent because the notice is silent"** is too pessimistic and is superseded.

It does **not** prove the complete Weiyuan buyer cashflow tuple.

## Remaining Weiyuan boundary

The current notice binds:

- first-auction floor: **RMB 445,886.28**;
- lease: **2022-02-24 through 2029-02-24**;
- rent: **RMB 6,000/month**;
- cadence: **quarterly**;
- rent already paid through **2026-11-30**;
- surface annual rent/floor: approximately **16.15%** before costs.

The still-unbound facts are:

- whether the scheduled 2026-10-18 auction actually sells;
- the exact auction-completion adjudication service date;
- treatment of rent already prepaid to the former owner for any period crossing the ownership-transfer date;
- the exact first unprepaid quarterly due date and amount after 2026-11-30;
- tenant identity, deposit, arrears, payment history, buyer taxes/transfer costs and full lease terms.

The calendar tail after November 2026 extends more than 24 months to 2029-02-24. But **calendar duration is not yet a source-bound buyer receipt window**. Promotion still fails closed until the transfer event and first unprepaid receipt node are bound.

## Exact public-source exhaustion

Exact searches were run against:

- execution case `(2026)川1024执1832号`;
- judgment `(2026)川1024民初929号`;
- exact Lanhuajie 46 address;
- exact RMB6,000/month / 2029-02-24 lease facts;
- the Supreme Court reference-case identifier.

No independent Weiyuan lease contract, rent ledger, prepaid-rent apportionment or auction-completion adjudication exists in the public record retrieved today. That is unsurprising because the auction itself is scheduled in the future.

Therefore:

```text
LIVE JEV CAUSAL_DESCENT = CONSUMED
GENERIC POST-TRANSFER RENT SUCCESSION = PUBLICLY SUPPORTED
ACTUAL WEIYUAN TRANSFER EVENT = NOT YET PROVEN
FIRST UNPREPAID BUYER RECEIPT = NOT YET SOURCE-BOUND
16.15% SURFACE GROSS != VERIFIED BUYER CASHFLOW YIELD
F1 = RETAINED RESEARCH ONLY
EXTERNAL CONTACT / BID / DEPOSIT / PURCHASE = NOT AUTHORIZED
```

## Decision

F1 remains `RETAINED_RESEARCH_BLOCKED_ON_FUTURE_TRANSFER_EVENT_AND_FIRST_UNPREPAID_RECEIPT_BINDING`.

F2/F3/F4 remain authoritatively closed. No active commercial candidate or transaction unit is created. The next safe step is exact-head repository CI plus live TypeSafe/Jev revalidation of this materially updated F1 state. If that exact head produces no new reversible public route class, PR #450 may merge and fresh Scan 141 may advance.
