# Scan 134 — Unprepaid receipts + automatic continuity

Date: 2026-09-23  
Primary domain: China  
Result: **0 retained / 0 commercial promotions / FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN**

## Admission tightening

Scan 134 required all of the following before commercial retention:

- a current transferable asset or contract right;
- an explicit entry price;
- future receipts not already prepaid to the seller;
- a receipt amount attributable to the exact acquired asset;
- automatic post-transfer contract continuity;
- at least 24 months of source-bound buyer receipt coverage;
- gross receipt-to-entry economics that are not obviously disqualifying;
- low recurring human delivery.

This scan specifically tested whether fixing the contract-continuity failure from Scan 133 was enough. It was not.

## F1 — Zhongshan 125-property bundle: continuity passes, economics fail

The official Zhongshan public-resource auction opens 2026-09-24 at RMB 60,427,825 for 125 properties.

For the specifically disclosed leased unit at Jinxiu Haiwan Cheng Phase 10 Unit 10, the official notice binds:

- tenant: 陈莲娣;
- lease through 2029-12-17;
- monthly rent of RMB 698.70, RMB 733.64 and RMB 770.32 by lease year;
- monthly payment before the 8th;
- buyer obligation to continue the existing lease;
- buyer rent entitlement from the month after handover, full payment and lease confirmation.

This clears the post-transfer continuity gate. But the acquisition is inseparable from the full RMB 60.43m bundle. Even the highest disclosed annual rent for the unit is only RMB 9,243.84, about **0.0153%** of the bundle floor before tax, commission, management or title-transfer costs. Eighty-six bundle properties are also still in title-certificate processing.

Verdict: `DEMOTED_ACTIVE_ZHONGSHAN_RMB60427825_BUNDLE_HAS_EXPLICIT_2029_LEASE_CONTINUITY_AND_POST_TRANSFER_RENT_RIGHT_BUT_DISCLOSED_RENT_IS_ECONOMICALLY_IMMATERIAL_AND_BUNDLE_SCALE_FAILS_SMALL_OPERATOR_SCOPE`

## F2 — Xi'an Huangcheng Lidu: succession passes, duration and attribution fail

The current second auction runs 2026-09-25 through 2026-09-28 with a RMB 3.32m floor.

The public court-notice text says the buyer succeeds to the prior owner's rights and obligations under the existing lease. The disclosed lease runs from 2026-03-01 through 2028-02-29 at RMB 10,916/month.

Two fields fail:

1. the RMB 10,916 rent covers three spaces together, so the exact receipt amount attributable to the auctioned 2-20302 unit is not bound;
2. the remaining receipt window at the September 2026 auction is materially below 24 months.

Verdict: `DEMOTED_ACTIVE_XIAN_RMB3320000_ASSET_HAS_EXPLICIT_LEASE_SUCCESSION_AND_RMB10916_MONTHLY_RENT_BUT_RECEIPT_IS_POOLED_ACROSS_THREE_SPACES_AND_REMAINING_WINDOW_IS_BELOW_24_MONTHS`

## F3 — Chongqing Jiulongpo: current tenant, incomplete public tuple

The current bankruptcy auction runs 2026-09-24 through 2026-09-25 at RMB 12,576,536 for three commercial certificates. All three are occupied by 金色印象足浴店.

The public auction page says monthly rent, lease term and escalation are in attachments rather than exposing them in the retrieved page. More importantly, it states that leased-area litigation has resulted in rent deductions to the owners committee and some individuals. The buyer also assumes post-delivery maintenance, management and occupancy risks.

The net buyer receipt amount, durable term and clean income right therefore remain unbound.

Verdict: `DEMOTED_ACTIVE_CHONGQING_RMB12576536_TENANTED_BUNDLE_HAS_CURRENT_OCCUPANCY_BUT_RENT_TERM_ARE_ATTACHMENT_ONLY_AND_LITIGATED_RENT_DEDUCTIONS_PREVENT_SOURCE_BOUND_NET_BUYER_RECEIPT_ECONOMICS`

## F4 — Xuzhou 5.02MWp distributed PV: operating machine, no public receipt ledger

This is a fresh exact asset, not Scan 133's Hainan residential-PV group.

Beijing Property Exchange materials state that the Xuzhou Nanhai Leather Factory project has 5.02MWp capacity, connected to the grid in May 2025, has EMC/grid/acceptance documentation and is operating normally. A current 2026-09-22 relisting exposes a RMB 19.443941m transfer floor.

That proves a real operating machine asset and a current transfer rail. It does **not** bind the project's current electricity receipt amount, payer/tariff, remaining receipt period, buyer settlement succession or O&M burden. Those fields remain UNKNOWN.

Verdict: `DEMOTED_CURRENT_XUZHOU_RMB19443941_5_02MWP_PV_ASSET_PROVES_LIVE_MACHINE_OPERATION_AND_TRANSFER_RAIL_BUT_PROJECT_SPECIFIC_RECEIPTS_TERM_SETTLEMENT_AND_LOW_LABOR_TRANSITION_REMAIN_UNBOUND`

## Scan conclusion

```text
FORMATIONS EXAMINED = 4
RETAINED = 0
ACTIVE COMMERCIAL CANDIDATES = 0
ACTIVE TRANSACTION UNITS = 0
FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN
NEXT = ATTRACTION_SCAN_135
```

## Scan 135 boundary

Before deep diligence, reject:

- inseparable multi-asset bundles whose receipts cannot justify the whole entry price;
- pooled rent that cannot be allocated to the exact acquired asset;
- receipt amounts or terms that exist only in unretrieved attachments;
- contracts with less than 24 months of source-bound future buyer receipts.

Prioritize a **single asset or economically separable unit** with exact unprepaid receipts, automatic contract continuity, at least 24 months of remaining coverage and non-disqualifying receipt-to-entry economics. Continue to prioritize named enterprise payers or machine-metered assets where the full receipt ledger is public-bound. No Scan 060-134 formation reuse, no regulated securities/financial products and no gate relaxation.
