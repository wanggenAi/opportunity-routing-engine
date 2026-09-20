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


## Additional activation constraints confirmed

Public partner onboarding now adds two concrete setup requirements:

### Xiaozhi / Bearhome

The current Open Platform documentation says production access requires merchant
registration and enterprise qualification, including business-license and legal-person
identity materials. Individual developers are not currently supported for API access.

Source:
- https://www.bearhome.cn/open-platform/recycle

Truth:
`ENTERPRISE_ENTITY_REQUIRED_FOR_PRODUCTION_API = PROVEN`.

### Aihuishou

The current Open Platform FAQ states that channel commission / old-device settlement
is monthly and the channel must issue a VAT invoice.

Source:
- https://next-neon.aihuishou.com/

Truth:
`CHANNEL_INVOICING_CAPABILITY_REQUIRED_FOR_SETTLEMENT = PROVEN`.

These are bounded one-time/administrative activation costs, not recurring transaction
labor. They do not kill F1 by themselves, but they must be included in activation
friction and cannot be treated as zero-cost API access.

## Outreach readiness

The canonical written-rights inquiry is complete in:

`docs/research/ATTRACTION_SCAN_015_F1_RIGHTS_INQUIRY.md`

Current verified public contacts:
- Aihuishou channel cooperation: `dennis.xie@atrenew.com`
- Bearhome/Xiaozhi business cooperation: `service@bearhome.cn`, 400-155-5151

The inquiry has been prepared for review but no external message is treated as sent or
as evidence until an actual provider response exists.

Gate A remains:

`PARTIAL_PASS_RIGHTS_UNKNOWN`.


## Public rights-risk signal — Aihuishou

A deeper official-source pass found a material caution in Aihuishou's current public
consumer terms/privacy materials:

- the current user-service agreement says that, unless law permits or Aihuishou gives
  written permission, users may not copy/modify platform operational or client/server
  interaction data or create derivative works through unauthorized third-party access;
- the privacy policy says partner access to shared personal information is limited to
  lawful, necessary and explicitly stated service purposes, and partners may not use
  that shared personal information for unrelated purposes.

Sources:
- https://pages.aihuishou.com/content/help/user-protocol
- https://pages.aihuishou.com/content/help/privacyV2

These consumer/public terms are **not** a substitute for the separate channel
cooperation agreement and therefore do not prove that an authorized channel cannot use
properly anonymized outcome statistics.

They do prove that:

`WRITTEN_PERMISSION_IS_A_HARD_REQUIREMENT_NOT_AN_OPTIONAL_NICE_TO_HAVE`.

Do not infer partner derivative-data rights from technical API access.

## Deeper neutral-incumbent search

A current web pass found:
- repeated advice and editorial/marketing content telling users to compare multiple
  recycling platforms;
- JiMao's current "competitor quote + add-on" mechanism, where a user can upload a
  competing platform quote and JiMao may add value;
- many single-platform articles comparing estimated versus final payout.

Representative source:
- https://www.jiumao100.com/news/qyxinwen/1607.html

Current search did **not** establish a mature neutral product whose core asset is
cross-platform empirical estimate→inspection→accept/reject→final-payment history and
whose routing action allocates future orders among independent rails.

Truth remains:

`EXACT_NEUTRAL_REALIZED_PAYOUT_ROUTER_INCUMBENT = NOT_ESTABLISHED`.

This is not evidence of absence. Continue contradiction search before promotion.


## Suhuanji — stronger transaction-data closure

A fresh pass over the current Open Platform documentation strengthens the technical
half of Gate A.

The documentation explicitly treats the integrator as a **合作平台** and requires the
partner to maintain its own user/order relationship. It exposes:

- pre-order valuation: `valuationPrice`;
- order quote: `quotePrice`;
- channel-side commercial price: `channelPrice`;
- payment status: `paymentStatus`;
- payment amount: `paymentAmount`;
- payment time: `paymentTime`;
- transaction-success time: `transactionSuccessTime`;
- partner order identifier: `channelOrderId`.

The platform also allows the partner to apply its own marketing adjustment through
`channelPrice`.

Source:
- https://open.suhuanji.com/

This proves a stronger machine-observable chain:

```text
PARTNER USER/ORDER RELATIONSHIP
→ VALUATION
→ QUOTE / QUOTE MODIFICATION
→ ACCEPT/REJECT / TERMINAL STATE
→ PAYMENT AMOUNT + PAYMENT TIME
→ TRANSACTION SUCCESS TIME
```

Truth:

`SUHUANJI_ESTIMATE_TO_REALIZED_PAYOUT_DATA_CLOSURE = PASS`.

It still does **not** prove:
- cross-competitor comparison permission;
- post-fulfillment non-identifying retention rights;
- future routing/model use rights;
- competitor benchmarking permission;
- channel commission terms.

The documentation says APP Key / APP Secret must be obtained by contacting Suhuanji
business staff, but the current public documentation does not expose a verifiable
business email or telephone endpoint.

Truth:

`SUHUANJI_PUBLIC_BUSINESS_CONTACT = UNRESOLVED`.

Do not substitute similarly named recycling companies or unverified third-party
contacts.


## Public-rights search ceiling

A targeted current-web pass searched the official/public surfaces for all three rails
for terms around:
- cooperation agreement;
- data ownership;
- retention;
- anonymized statistics;
- competitor comparison;
- benchmarking;
- derivative/model use.

Result:

```text
AIHUISHOU
  public technical/channel material = present
  public consumer data-use restriction signal = present
  explicit partner cross-rail derivative-data grant = NOT FOUND

XIAOZHI / BEARHOME
  public technical/outcome material = present
  enterprise onboarding = present
  explicit partner cross-rail derivative-data grant = NOT FOUND

SUHUANJI
  public technical/outcome material = strong
  partner-owned valuation/order execution path = present
  explicit partner cross-rail derivative-data grant = NOT FOUND
```

Truth:

`PUBLIC_RIGHTS_SEARCH_CEILING_REACHED = TRUE`.

This does **not** mean rights are denied.
It means current public evidence cannot upgrade R1/R3/R4/R5.

Further same-layer web searching should not be treated as the default next action.
The decisive evidence must now come from:
1. a current partner agreement supplied by the rail; or
2. an official written business response.

## Suhuanji execution-layer separation

The current Suhuanji API exposes `/order/createOnly`.

Its documentation explicitly says that a cooperation platform with its **own category
valuation logic** does not need to use Suhuanji's goods/valuation interfaces; it may
create the order itself and push the order into Suhuanji for execution.

Source:
- https://open.suhuanji.com/

This strengthens:

```text
ROUTER-OWNED DECISION / VALUATION LAYER
→ RAIL-OWNED PHYSICAL FULFILLMENT
→ RAIL RETURNS QUOTE / PAYMENT / TERMINAL OUTCOME
```

Truth:

`SUHUANJI_SUPPORTS_PARTNER_DECISION_LAYER_WITH_RAIL_EXECUTION = PASS`.

This is technically favorable for F1 because the router need not collapse into a
simple embedded quote widget.

It still does not grant the rights to retain rail-returned outcomes for cross-rail
future routing.
