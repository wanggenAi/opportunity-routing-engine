# Scan 137 — Fresh current asset receipt falsification

Date: 2026-09-23  
Primary domain: China  
Result: **0 retained / 0 commercial promotions / FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN**

## Admission rule

Scan 137 resumed from merged `main` `dc7cf834d24302f85702caddad000fbd3ad082ff` after Scan 136 F1/F2 reversible Jev routes were fully consumed. It searched fresh current China assets only. Exact-address repository de-duplication found no prior Scan 060-136 match for the four examined assets.

The scan preserved the existing hard floor:
- exact asset-attributable receipt quantum;
- buyer-side post-transfer continuity;
- at least 24 months of source-bound future receipt coverage;
- computable non-disqualifying economics;
- low recurring human delivery;
- `UNKNOWN != PASS`.

## F1 — Guiyang Huaguoyuan A South 4 Building 35F Room 2: closed

Current change sale: 2026-09-23 through 2026-11-21.

Public tuple:
- entry: **RMB 483,004**;
- rent: **RMB 11,760 every six months** = RMB 23,520/year;
- lease: 2021-05-01 through 2029-08-01.

Nominal annual rent / entry is approximately **4.87% gross** before all taxes, transfer costs, vacancy, repairs and ownership costs. The exact first buyer rent settlement and current rent-payment cursor are not public.

Verdict: `DEMOTED_CURRENT_GUIYANG_RMB483004_LEASED_UNIT_HAS_EXACT_RMB23520_ANNUAL_RENT_TO_2029_08_01_BUT_APPROX_4_87_PERCENT_GROSS_HARD_FAILS_CURRENT_ATTRACTION_ECONOMICS`.

## F2 — Cili Huancheng South Road Building 12 Room 111: closed

Current first auction: 2026-10-19 through 2026-10-20.

Public tuple:
- entry: **RMB 3,000,000**;
- auto-repair lease: RMB 50,000/year, 2021-2031;
- restaurant lease: RMB 50,000/year, 2024-2029;
- aggregate public rent: **RMB 100,000/year**.

Even granting the full aggregate rent, nominal gross is only **3.33%** before costs. Exact post-transfer allocation and tenant-area split remain unbound, but those unknowns cannot rescue the weak economics.

Verdict: `DEMOTED_CURRENT_CILI_RMB3000000_COMMERCIAL_ASSET_HAS_RMB100000_AGGREGATE_ANNUAL_RENT_BUT_APPROX_3_33_PERCENT_GROSS_HARD_FAILS_CURRENT_ATTRACTION_ECONOMICS`.

## F3 — Hangzhou Xinming Commercial Center Building 2 Unit 2-101: closed

Current first auction: 2026-09-23 through 2026-09-24.

Public tuple:
- entry: **RMB 991,000**;
- management term: 2023-09-13 through 2032-09-12;
- lease: 2026-06-01 through 2029-05-31;
- buyer may enjoy rent **from post-transaction title confirmation**;
- property-fee arrears through 2026-09-12: **RMB 59,535**, borne by buyer before title confirmation under the notice.

The decisive contracted rent quantum is not published on the retrieved page. A valid receipt-to-entry ratio therefore cannot be computed.

Verdict: `DEMOTED_CURRENT_HANGZHOU_RMB991000_MANAGED_SHOP_HAS_EXPLICIT_POST_CONFIRMATION_BUYER_RENT_AND_TERM_TO_2029_05_31_BUT_PUBLIC_RECEIPT_QUANTUM_IS_UNBOUND`.

## F4 — Chongqing Rongchang Guangchang Road 115 No. 3-160: closed

Current first auction: 2026-09-23 through 2026-09-24.

Public tuple:
- entry: **RMB 114,730**;
- management agreement: 2020-05-01 through 2030-04-30, subject to opening-delay extension;
- first five years: RMB 1/year;
- last five years: owner receives **90% of the mall's actual rent**;
- current unit status: **empty**;
- unit is physically opened into surrounding property and the large certificate is not subdivided.

The later-period formula is a pooled percentage of mall rent, not an exact asset-attributable contracted receipt. Current emptiness further prevents claiming an inherited cashflow.

Verdict: `DEMOTED_CURRENT_RONGCHANG_RMB114730_MALL_UNIT_HAS_LONG_MANAGEMENT_AGREEMENT_BUT_CURRENT_UNIT_IS_EMPTY_AND_90_PERCENT_OF_MALL_ACTUAL_RENT_FORMULA_IS_NOT_ASSET_ATTRIBUTABLE_CONTRACTED_RECEIPT`.

## Decision

```text
FORMATIONS EXAMINED = 4
RETAINED FOR RESEARCH = 0
ACTIVE COMMERCIAL CANDIDATES = 0
ACTIVE TRANSACTION UNITS = 0
FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN
NEXT BROAD SCAN = ATTRACTION_SCAN_138
FIRST ACTION = EXACT-HEAD CI + LIVE JEV
```

No bid, deposit, purchase, external contact or monetary action is authorized. Scan 137 adds no new retained research blocker; existing Scan 135/136 retained cases remain separately blocked on external written/source-document evidence.
