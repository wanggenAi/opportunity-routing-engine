---
name: used-device-realized-payout-preflight
description: "Use when a user is actively considering selling or recycling a used phone, tablet, or computer and wants to understand expected final realized payout rather than only a displayed estimate. This preflight must not execute transactions, claim live cross-platform routing, collect identifying order data, or invent platform outcomes."
---

# Used-device realized-payout preflight

## Objective

Detect whether the user has genuine current sell/recycle intent and help frame the
decision around **final realized payout after inspection**, not only the first displayed
estimate.

This is an experiment artifact. It is not a live recycling router.

## Trigger examples

Use when the user asks questions such as:
- where should I recycle/sell my old phone;
- which recycler is likely to pay me more after inspection;
- why does the final recycle price differ from the estimate;
- should I choose a higher estimate or a more reliable final payout;
- I want to sell this phone/tablet/laptop now.

Do not trigger for:
- buying a new phone with no old-device sale intent;
- generic second-hand market news;
- repair advice;
- device appraisal where the user is not considering a transaction.

## Allowed non-identifying inputs

Ask only for what is necessary:
- device category;
- model/configuration;
- storage bucket;
- coarse condition flags;
- coarse region only if relevant;
- desired time-to-cash;
- priority: expected payout / speed / downside certainty.

Never ask for or retain:
- name;
- mobile;
- exact address;
- payment account;
- identity document;
- IMEI;
- serial number;
- account credentials.

## Truth boundary

Always preserve:

`DISPLAYED_ESTIMATE != FINAL_REALIZED_PAYOUT`.

But do not claim that a specific platform will pay more unless current authorized
evidence supports that claim.

When live licensed rail data and outcome history are unavailable, say clearly that
cross-platform realized-payout routing is not currently available.

Do not fabricate:
- live quotes;
- inspection outcomes;
- payout probabilities;
- platform rankings;
- transaction success rates;
- time-to-cash statistics.

## No transaction execution

This preflight must not:
- create a recycling order;
- submit pickup details;
- transmit payment details;
- call private/partner APIs;
- scrape gated pricing endpoints;
- route a user to a rail based on operator commission.

## Experiment signal

A useful invocation is one where the user has a current device and asks for a decision
that changes where/how they sell it.

Generic questions and developer tests are not qualified sell intent.

If hosted in a public discovery surface, experiment analytics must distinguish
platform-native discovery from founder-distributed links.

## Output shape

1. Identify whether there is current sell/recycle intent.
2. Summarize only the non-identifying device facts supplied.
3. Explain the estimate-to-final-payout uncertainty relevant to the decision.
4. If authorized live routing is unavailable, state that boundary.
5. Do not ask for personal fulfillment/payment details.
