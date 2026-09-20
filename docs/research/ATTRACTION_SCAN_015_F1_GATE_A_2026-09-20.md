# ATTRACTION_SCAN_015-F1 — Gate A Public Rights / Callability Falsification

Date: 2026-09-20  
Formation: `ATTRACTION_SCAN_015-F1 — USED-DEVICE REALIZED-PAYOUT ROUTER`  
Status: `PARTIAL_PASS / RIGHTS_UNKNOWN / NO_COMMERCIAL_PROMOTION`

## Gate definition

F1 survives Gate A only if at least two overlapping 3C recycling rails can support:

1. partner-visible post-inspection / final settlement outcomes;
2. stable callable order/fulfillment mechanics;
3. lawful retention of the minimum non-identifying outcome fields needed for routing;
4. side-by-side / cross-rail comparison and model use;
5. the operator remaining a channel/router rather than recycler/principal.

`UNKNOWN != PASS`.

## Result

```text
TECHNICAL OUTCOME VISIBILITY       = PASS
CALLABLE PARTNER RAILS             = PASS
AT_LEAST TWO OVERLAPPING 3C RAILS  = PASS
PUBLIC COMMISSION EVIDENCE         = PASS_ON_MULTIPLE_RAILS
CROSS-RAIL DATA-USE RIGHT          = UNKNOWN
COMPETITOR COMPARISON RIGHT        = UNKNOWN
ANONYMIZED MODEL-TRAINING RIGHT    = UNKNOWN
GATE_A_OVERALL                     = PARTIAL / NOT PASSED
COMMERCIAL CANDIDATE               = FALSE
```

F1 remains a research formation.

## Rail evidence

### Suhuanji — outcome visibility is explicit

Current open-platform documentation requires partner-side transaction state.

The partner may:
- obtain estimates;
- create recycle orders;
- provide a `channelOrderId` for reconciliation;
- keep the user/order relationship locally;
- receive order callbacks.

The order callback exposes:
- `QUOTATION_MODIFICATION`;
- cancellation / rejection;
- `PAYMENT_SUCCESS`;
- `PAYMENT_FAILURE`;
- `paymentAmount`;
- `quotePrice`;
- transaction-success state.

Source:
- https://open.suhuanji.com/

Truth:

`PARTNER_VISIBLE_QUOTE_TO_PAYMENT_OUTCOME = PROVEN`.

Important boundary:

The public documentation explains operational storage and callbacks. It does **not**
publicly grant a license to aggregate those outcomes with competitor-platform outcomes
or retain them for a cross-platform predictive routing model.

### Xiaozhi / Bearhome — inspected outcome is partner-visible

Current recycling API documentation exposes:
- estimate generation;
- order creation;
- order detail;
- order lifecycle;
- inspection price;
- confirm / dispute-and-return;
- completed/cancelled/returned states;
- callbacks;
- business analytics.

The order-detail example includes a post-inspection `vaild_price`, and the partner can
confirm the recycle or reject/return after inspection.

The platform requires enterprise qualification and business review before production
credentials are issued.

Sources:
- https://www.bearhome.cn/open-platform/recycle
- https://www.bearhome.cn/open-platform

Truth:

`PARTNER_VISIBLE_INSPECTION_AND_ACCEPT_REJECT_OUTCOME = PROVEN`.

Boundary:

Public API documentation does **not** state that a partner may reuse Bearhome-derived
outcomes to rank Bearhome against competing recyclers or train a neutral cross-platform
routing model.

### Aihuishou — commission rail is real, rights are contractual

Current open-platform material supports H5/SDK/API/mini-program integration and
publicly describes a commission cooperation model.

It also says the partner obtains the channel link/integration after confirming intent
and **signing a cooperation agreement**.

Source:
- https://next-neon.aihuishou.com/

Truth:

`CALLABLE_CHANNEL_AND_COMMISSION = PROVEN`.

Boundary:

The public page does not expose the cooperation agreement terms needed to determine:
- returned final inspection/settlement data fields;
- retention rights;
- competitor comparison rights;
- derived-model rights.

Therefore these remain `UNKNOWN`.

## Legal / privacy boundary

The routing asset must not depend on retaining identifiable seller data.

China's Personal Information Protection Law currently states that:
- processing must have a clear and reasonable purpose and be directly related to that
  purpose;
- collection must be limited to the minimum necessary scope;
- processing purposes/methods/categories must be disclosed;
- when processing purpose or method changes, consent requirements may change;
- anonymous information that cannot identify a natural person falls outside the
  statutory definition of personal information.

Primary sources:
- National People's Congress / PIPL;
- MIIT publication of PIPL.

Therefore a safer target routing record is:

```text
RAIL_ID
DEVICE_MODEL_BUCKET
NON_IDENTIFYING_CONDITION_FEATURES
INITIAL_ESTIMATE
POST_INSPECTION_QUOTE
ACCEPT_REJECT
FINAL_PAYOUT
TIME_TO_CASH
RETURN_CANCEL_REASON_CLASS
TIMESTAMP_BUCKET / REGION_BUCKET IF NECESSARY
```

Do not make the moat:
- name;
- mobile;
- exact address;
- payment account;
- device IMEI / serial number tied to a person;
- other user-identifying order data.

Even anonymization does not override partner contract restrictions.

## Decisive finding

The first half of Gate A survives:

```text
TRANSACTION EXECUTION
→ POST-INSPECTION / PAYMENT OUTCOME
→ PARTNER-VISIBLE MACHINE DATA
```

is real on current rails.

But the central commercial right remains unresolved:

```text
PARTNER CAN SEE OUTCOME
!=
PARTNER MAY USE OUTCOME
TO BUILD A CROSS-COMPETITOR ROUTING ASSET
```

This is now the single narrowest Gate-A unknown.

## Required external confirmation

Before building any transaction integration, obtain written contractual/business
confirmation from at least **two overlapping 3C rails** answering the same questions:

1. Can our channel show your current estimate alongside other licensed recycling
   partners' estimates?
2. After an order completes, which post-inspection/final-payment fields are returned to
   us?
3. May we retain **anonymous/non-identifying** estimate→inspection→final-outcome records
   for statistical quality/routing analysis?
4. May those anonymous outcome statistics be used to choose which partner receives a
   future user order?
5. Are there restrictions on benchmarking, ranking, displaying competitor results or
   derived models?
6. What commission event is settled: order creation, inspection acceptance, completed
   payment, or another event?
7. Do we remain a referral/channel technology provider rather than buyer/recycler or
   transaction principal?
8. What data deletion/retention, security, audit and privacy obligations apply?

Acceptable proof:
- signed/unsigned current partner agreement supplied by the rail;
- official written business email;
- official partner documentation with explicit terms.

A phone-only verbal answer is insufficient for canonical PASS unless followed by
written confirmation.

## Gate-A state machine

```text
PUBLIC_TECHNICAL_DOCS
→ TECHNICAL_PASS
→ RIGHTS_UNKNOWN
→ TWO_RAIL_WRITTEN_CONFIRMATIONS
   ├─ rights compatible → GATE_A_PASS
   └─ rights incompatible / exclusive / no reuse → KILL_OR_REDESIGN_F1
```

## What not to do

- Do not scrape logged-in/private APIs to bypass onboarding.
- Do not create real user orders merely to discover contract restrictions.
- Do not retain personal order data as a moat.
- Do not assume "API access" grants derivative-data/model rights.
- Do not assume anonymization defeats contractual use restrictions.
- Do not rank by commission.
- Do not start Gate B transaction execution before Gate A rights are bounded.

## Next action

Use scarce external-validation capital only on the narrow rights question.

Prepare/send the same concise cooperation-rights inquiry to:
- Aihuishou channel cooperation;
- Bearhome/Xiaozhi business cooperation;
- optionally Suhuanji business cooperation as the third rail.

Until two written confirmations exist:

`GATE_A = NOT PASSED`.
