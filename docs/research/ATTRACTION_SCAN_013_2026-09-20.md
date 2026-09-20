# ATTRACTION_SCAN_013 — Newly Callable Physical/Service Rail × Unowned High-Intent Signal

Date: 2026-09-20
Epoch: `ATTRACTION_FIELD_V1`
Status: `COMPLETE / ZERO_HIGH_ATTRACTION_BEACONS / ZERO_COMMERCIAL_PROMOTIONS`

## Executive truth

Scan 013 searched for a temporary integration-lag window: a real physical/service rail
that only recently became Agent/API/MCP/Skill-callable, while a separate high-intent
state/event remained outside the rail owner's system.

Result:

```text
ACTIVE COMMERCIAL CANDIDATES = 0
HIGH_ATTRACTION_BEACONS = 0
RETAINED RESEARCH FORMATIONS = 0
FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN
```

The mechanism is real: multiple Chinese transaction/service rails are becoming
machine-callable in 2026.

But a new hard boundary appeared:

```text
NEWLY CALLABLE RAIL
+
SIMPLE / GENERIC INTENT-TO-ACTION MAPPING
=
GENERAL AGENT FEATURE
NOT AN INDEPENDENT ROUTING BUSINESS
```

If a general-purpose Agent can reproduce the bridge from:
- the user's natural-language intent/context;
- the official Skill/MCP/API schema;
- the rail's own live catalog/availability/price;

then the operator does not own a distinct routing control point.

This scan therefore retains zero and promotes **generic-Agent substitutability** into a
hard attraction kill.

## Direction 1 — ride-hailing MCP rail

### DiDi

DiDi's MCP documentation dated 2026-09-19 exposes:
- vehicle/category and estimated price;
- ride-link generation;
- Pro order creation;
- order-status query;
- cancellation;
- driver location.

Source:
https://cloud.tencent.com/developer/mcp/server/11746

The required decision inputs are essentially:
- origin;
- destination;
- product category;
- account/user context.

A general Agent can obtain those from the user or surrounding workflow and invoke the
rail directly.

Verdict:
`NEWLY_CALLABLE_RAIL_CONFIRMED / ROUTING_EDGE_GENERIC`.

### CaoCao

CaoCao's open platform exposes direct order creation and cancellation APIs, including
enterprise trip scenes, cost centers and callbacks.

Sources:
- https://open.caocaokeji.cn/zh-cn/docs/caocao_open/travel/2.7callCar.html
- https://open.caocaokeji.cn/zh-cn/docs/caocao_admin/admin/2.5steps.html

The rail itself already accepts the economically relevant policy/scene parameters.

Verdict:
`CALLABLE_RAIL + RAIL_NATIVE_POLICY_CONTEXT / NO DISTINCT ROUTER ASSET`.

## Direction 2 — 1688 Agent-native B2B procurement

The current 1688 one-stop procurement Skill is a strong action-rail proof.

It explicitly supports:
- natural-language purchase intent;
- clarification of category, budget and specification;
- product search;
- product detail;
- cart;
- direct purchase / checkout;
- order query and cancellation;
- execution from multiple Agent environments.

Source:
https://github.com/next-1688/1688-utp-shopping

It also stores user-confirmed procurement preferences locally for future personalized
recommendations.

Separate official/community Skill surfaces already expose:
- product search and multi-condition filtering;
- procurement workflows;
- supplier/order inquiry;
- shopkeeper opportunity/trend functions.

Representative sources:
- https://github.com/next-1688/1688-product-find
- https://github.com/next-1688/1688-supplychain-order-inquiry
- https://github.com/next-1688/1688-shopkeeper

The generic bridge:

```text
"I need X"
→ clarify budget/spec
→ search
→ compare
→ order
```

is therefore increasingly native to the Agent + rail itself.

Verdict:
`FULL_PROCUREMENT_ACTION_RAIL_CONFIRMED / GENERIC_PROCUREMENT_ROUTER_NOT_DISTINCT`.

A specialized procurement decision may still exist, but it must depend on a separate
reusable routing asset not present in ordinary Agent reasoning or 1688's own
capabilities.

## Direction 3 — local-life Agent execution

Meituan states that the upgraded "Xiaotuan" moved from search/Q&A into action:
- combine real-time information;
- assist with ordering;
- ride-hailing;
- reservations;
- local-life service operations.

Source:
https://www.meituan.com/news/NN260828216013035

A more specific Meituan example describes a user saying:
- six people;
- 19:00;
- near the office;
- Sichuan food;
- must have availability.

Xiaotuan combines distance, open status, review and real-time seat availability and
then assists reservation after user confirmation.

Source:
https://www.meituan.com/news/NN260727198008607

Verdict:
`CONTEXTUAL_SELECTION_PLUS_ACTION_ALREADY_GENERAL_AGENT_FEATURE_INSIDE_RAIL_OWNER`.

This directly falsifies the idea that ordinary multi-constraint service selection is a
defensible third-party routing asset.

## Direction 4 — restaurant / merchant MCP ordering

McDonald's China now exposes an MCP platform whose listed capabilities include:
- intelligent ordering and checkout;
- coupon collection;
- event/calendar information;
- nutrition calculation;
- points redemption.

Source:
https://open.mcd.cn/mcp

Verdict:
`MERCHANT_ACTION_RAIL_AGENTIZED / ORDINARY_INTENT_TO_ORDER_BRIDGE_NATIVE`.

A third party saying "the user is hungry, select and order a meal" does not own a
distinct bridge merely because the MCP is new.

## Direction 5 — travel Skill + native commission

Fliggy's current AI open platform is explicitly built for native Agents:
- official product and dynamic-inventory search;
- hotel/flight/attraction/vacation coverage;
- natural-language travel search;
- developer partner program.

Sources:
- https://flyai.open.fliggy.com/
- https://flyai.open.fliggy.com/docs

The promoter program states:
- developers integrate the FlyAI Skill into their Agent;
- supported hotel/vacation orders are automatically attributed;
- the developer can earn order commission.

Source:
https://flyai.open.fliggy.com/docs/partner

This is a real native monetization rail.

But the current public capability is heavily search-oriented, and some products still
return jump links for real-time price/booking.

Source:
https://flyai.open.fliggy.com/docs/faq

More importantly, the ordinary travel-intent bridge is itself what FlyAI exposes.

Verdict:
`NATIVE_COMMISSION_REAL / GENERIC_TRAVEL_AGENT_IS_DISTRIBUTION_NOT_DISTINCT_ROUTING`.

A developer can earn money by audience/distribution, but that does not satisfy the
current requirement for an independent routing asset.

## Direction 6 — generic action MCPs beyond commerce

The same pattern appears outside commerce.

Tencent Meeting's MCP lets a general Agent:
- schedule;
- modify;
- cancel;
- inspect meetings;
- read recordings/transcripts.

Source:
https://meeting.tencent.com/support/topic/2233/index.html

This is not itself a commercial candidate. It is evidence that "an Agent can now do
what previously required opening the app" is becoming a platform capability category.

Verdict:
`APP_ACTION_AGENTIZATION_IS_INFRASTRUCTURE, NOT AUTOMATIC OPPORTUNITY`.

## Structural correction — General-Agent substitutability

The previous attraction model could reject:
- hidden demand/supply;
- unresolvable matches;
- uncallable action gates;
- founder sales/search/delivery;
- expert matching.

But it could still falsely retain a formation where:
- both sides are visible;
- the rail is callable;
- the value jump is real;
- matching is easy;
- the operator appears to "orchestrate";
while a general Agent can perform the exact same orchestration from public rail
capabilities and ordinary user context.

That is not meaningful operator control.

New hard rule:

```text
USER INTENT / ORDINARY CONTEXT
+
OFFICIAL RAIL SCHEMA
+
GENERAL AGENT REASONING
→ SAME ROUTING DECISION
=
GENERIC_AGENT_SUBSTITUTABLE
→ LOW CURRENT ATTRACTION
```

The key question becomes:

> What durable routing asset does the operator own that a general Agent or rail owner
> cannot reproduce from the same prompt and API?

Examples of potentially distinctive assets:
- a cross-domain compatibility graph not owned by either rail;
- outcome-derived acceptance/rejection history;
- a continuously maintained multi-rail constraint graph;
- permissioned or proprietary evidence unavailable to the generic Agent;
- a specialized routing model trained on real outcomes;
- a reusable eligibility/compatibility rule base whose maintenance is itself
  systematized rather than founder expert labor.

These are examples of asset types, not opportunity assumptions.

## Important boundary

"Specialized" cannot become an excuse for consulting.

The next route must satisfy both:

```text
NOT GENERIC-AGENT SUBSTITUTABLE
AND
NOT RECURRING-EXPERT DEPENDENT
```

The desired middle is:

```text
SPECIALIZED
+
REUSABLE
+
MACHINE-RESOLVABLE
+
COMPOUNDING
```

## Engineering consequence

Scan 013 justifies an executable hard kill in the attraction layer:

`generic_agent_substitutable: bool`

If true, with attributable evidence, the signal cannot become
`HIGH_ATTRACTION_BEACON`.

This prevents new MCP/Skill/API availability from being mistaken for operator control.

## Pareto result

`PARETO_ELIGIBLE = 0`
`PARETO_FRONTIER = empty`

No weighted score was used to manufacture a winner.

## Drift audit

- treated new MCP/Skill availability as opportunity proof? No.
- confused native commission with routing control? No.
- treated generic multi-constraint recommendation as proprietary? No.
- treated ordinary user context as an operator asset? No.
- promoted a general Agent feature merely because the action rail is new? No.
- converted specialization into manual expert work? No.
- allowed zero retention? Yes.

## Final state

```text
ATTRACTION_SCAN_013 = COMPLETE
ACTIVE COMMERCIAL CANDIDATES = 0
HIGH_ATTRACTION_BEACONS = 0
RETAINED RESEARCH FORMATIONS = 0
FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN
```

## Next search direction

Run `ATTRACTION_SCAN_014` with working label:

`NON-GENERIC DECISION EDGE × CALLABLE ACTION RAIL`

Search broad current reality for cases where:
1. a real high-intent state/event is observable;
2. a stable external action rail already exists;
3. the action rail is callable enough to execute;
4. user intent + ordinary context + official rail schema are insufficient to choose
   the correct route;
5. a reusable specialized routing asset can resolve the decision;
6. that asset is not already owned by the rail owner or a mature incumbent;
7. the asset is machine-executable without recurring expert judgment;
8. each outcome improves the asset through compatibility, acceptance, constraint,
   performance or route-history evidence;
9. the resulting decision changes a real economic action;
10. the operator can capture value without recurring acquisition, sales or delivery.

Retain zero if:
- specialization is only prompt wording;
- the generic Agent can derive the same answer from public information;
- the rail owner already contains the decisive rule/data;
- each case requires founder/expert interpretation;
- the "asset" does not compound from repeated outcomes.
