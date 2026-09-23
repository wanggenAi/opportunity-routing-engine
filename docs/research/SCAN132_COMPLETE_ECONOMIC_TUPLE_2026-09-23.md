# Scan 132 — Complete asset-level economic tuple

Date: 2026-09-23  
Primary domain: China  
Result: **0 retained / 0 commercial promotions / FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN**

## Admission rule

Scan 132 required the same asset or contract-control position to bind all six fields:

1. acquisition/entry price;
2. contracted receipt amount;
3. contract term;
4. identified counterparty;
5. explicit post-transfer receipt/control right;
6. low recurring human delivery.

No field may be inferred from a listing title, generic market yield, old rent, asset class or transferability alone.

## F1 — Hangzhou long-term small leased property

The Hangzhou Property Exchange lists a non-residential unit at RMB 395,000. It is already leased from 2026-01-09 through 2031-01-08. A buyer must continue the existing lease, and prepaid rent/deposit are settled after transfer.

This is a stronger structural match than Scan 131's short remaining Wuhu leases. It still fails because the public page says rent details are in the underlying lease contract rather than publishing the receipt amount. Without the amount, source-bound economics cannot be computed.

Verdict: `DEMOTED_LONG_TERM_SMALL_LEASED_PROPERTY_CLEARS_PRICE_TERM_AND_LEASE_SUCCESSION_BUT_PUBLIC_ECONOMIC_TUPLE_OMITS_CONTRACTED_RECEIPT_AMOUNT`

## F2 — Xiamen full tuple but short remaining receipts

The Xiamen notice is unusually explicit:

- starting acquisition price: RMB 2,112,800;
- lease: 2026-04-26 through 2027-04-25;
- monthly rent: RMB 3,700;
- prepaid rent stays with the prior owner through 2026-10-25;
- one-month deposit offsets November;
- buyer begins collecting rent in December 2026.

The complete tuple therefore exists in public evidence. It is still not a commercial candidate because only a short contracted buyer-receipt window remains before expiry, and the disclosed annualized gross rent is only RMB 44,400 before commission, platform fees, taxes, transfer costs, maintenance or vacancy.

Verdict: `DEMOTED_EXPLICIT_COMPLETE_RENT_TUPLE_AND_POST_TRANSFER_COLLECTION_EXIST_BUT_REMAINING_CONTRACTED_RECEIPT_WINDOW_IS_TOO_SHORT_AND_NORMALIZED_ECONOMICS_TOO_WEAK_FOR_CURRENT_COMMERCIAL_PROMOTION`

## F3 — cheap leased ownership without transferred rent

Jilin's official public-resource platform exposes multiple leased properties at genuinely small prices, including examples at RMB 114,656.50 and RMB 182,600. The same official notice says the existing lease remains in force after sale.

The decisive clause is economic: **all rent during the surviving lease continues to be collected by and belong to the seller.** The buyer inherits ownership and tenant possession constraints, but not the cashflow.

Verdict: `DEMOTED_SMALL_OFFICIAL_LEASED_PROPERTIES_ARE_ACQUIRABLE_BUT_EXISTING_LEASE_RENTS_ARE_EXPLICITLY_RESERVED_TO_SELLER_SO_POST_TRANSFER_CASHFLOW_RIGHT_FAILS`

## F4 — Beihua University vending-machine site right

Beihua University offered a three-year site right for 32 vending machines and 8 coffee machines. Annual site rent is RMB 508,800 and mobile payment is required.

This is not inherited cashflow. The RMB 508,800 is an operator cost. No current user purchase ledger, minimum spend or customer contract transfers. The operator must deploy new equipment, maintain food traceability, clean/disinfect at least weekly, respond to failures within one hour, pay utilities and perform maintenance. Machine checkout does not remove recurring field operations.

Verdict: `DEMOTED_CAMPUS_VENDING_RIGHT_HAS_MACHINE_PAYMENT_AND_THREE_YEAR_LOCATION_CONTROL_BUT_NO_CONTRACTED_RECEIPTS_AND_EXPLICIT_RECURRING_FIELD_OPERATIONS_FAIL_FOUNDER_LIGHT_CASHFLOW`

## Important excluded regression

A Nanchang listing was marketed with “original annual rent RMB 14,400” and a RMB 36,660 starting price, but its body states that the property is currently **not leased**. Historical or headline rent is therefore not admissible as current cashflow.

## Scan conclusion

```text
FORMATIONS EXAMINED = 4
RETAINED = 0
ACTIVE COMMERCIAL CANDIDATES = 0
ACTIVE TRANSACTION UNITS = 0
FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN
NEXT = ATTRACTION_SCAN_133
```

Scan 133 should front-load two quantitative checks before deep diligence: durable buyer receipt coverage and receipt-to-entry economics. It must still require explicit counterparty and post-transfer rights, remain founder-light, avoid property-only ontology lock-in, avoid regulated financial products, and never reuse Scan 060-132 formations.
