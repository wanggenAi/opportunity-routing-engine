# ATTRACTION_SCAN_016-F1 — final cheap falsification

Date: 2026-09-21  
Formation: `9610_CROSS_CUSTOMS_RETURN_ROUTER` / 跨境电商9610跨关区退货路由  
Verdict: **DEMOTED — exact two-rail third-party callability and operator economics remain unproven**  
Commercial candidate: **NO**  
First external value flow: **NOT_PROVEN**

## Decision

Remove Scan 016-F1 from active validation.

This is **not** a conclusion that 9610 cross-customs returns lack value. The physical/regulatory capability is
real and now well proven.

The failed hypothesis is narrower:

> an independent neutral operator can machine-route a seller's already-triggered 9610 return across at least
> two independent China re-entry rails, receive structured execution outcomes, and earn non-consulting economics.

After cheap public falsification, the non-compensatory gates for that hypothesis remain unproven.

## What is proven

### Nationwide legal / physical choice set

GACC Announcement 2026 No.24 made 9610 retail-export cross-customs-district returns nationally available from
2026-04-01.

The notice also requires participating enterprises to have dedicated operating capability and to expose
production-system data to, or connect it with, Customs systems.

Source:
- https://www.mofcom.gov.cn/zcfb/zgdwjjmywg/art/2026/art_3db24e4b76784738a17196c585795546.html

Real execution exists:
- Hangzhou processed returned goods that had originally been exported through Shanghai and Shenzhen.
- Zhejiang reporting states AliExpress can choose a convenient return port.
- Yiwu's TIR + cross-border return mode had already processed substantial real return volume and reported lower
  logistics cost than air.

Sources:
- https://www.hzzx.gov.cn/cshz/content/2026-04/03/content_9201257.htm
- https://zjic.zj.gov.cn/ywdh/shjs/202604/t20260402_24018213.shtml

So:

```text
POLICY = REAL
MULTIPLE PHYSICAL ROUTES = REAL
SELLER COST/TIME VALUE = REAL
```

## What generic APIs prove—and do not prove

4PX exposes a unified logistics open platform to merchants and software providers, including return-service
categories.

Source:
- https://open.4px.com/apiInfo/introduce

Cainiao exposes structured warehouse return APIs such as sales-return notification and return-receipt
information.

Source:
- https://developer.alibaba.com/docs/api.htm?apiId=25326

These facts prove that reverse logistics can be machine-integrated.

They do **not** establish this stronger object:

```text
NEUTRAL THIRD-PARTY ROUTER
→ GET 9610 CROSS-CUSTOMS QUOTE FROM RAIL A
→ GET 9610 CROSS-CUSTOMS QUOTE FROM RAIL B
→ SELECT
→ CREATE EXACT CUSTOMS-RETURN ORDER
→ RECEIVE STATUS / CUSTOMS / INBOUND / RECOVERY OUTCOME
```

No two independent public rails satisfying that exact contract were established.

## Why physical route diversity is not enough

The real examples are embedded in enterprise/platform/customs operational relationships.

In the Zhejiang example, the cross-border platform itself described choosing the convenient return port.
The GACC rule requires the participating enterprise's production system to connect with Customs.

That is materially different from an open neutral execution rail.

Therefore:

```text
PORT CAN PROCESS RETURN
!=
NEUTRAL ROUTER CAN CALL PORT/RAIL
```

## Generic return-routing value is already mature

AfterShip Returns currently provides:
- return zones and routing rules;
- multiple carriers and warehouses;
- automated labels;
- full Returns API;
- real-time carrier-rate comparison;
- automatic cheapest-carrier selection.

Sources:
- https://support.aftership.com/en/returns/articles/15389080-how-to-set-up-return-routing-rules-with-aftership-returns
- https://www.aftership.com/docs/returns
- https://support.aftership.com/en/returns/articles/15389066-how-to-manage-carriers-and-warehouses
- https://support.aftership.com/en/returns/articles/15389132-auto-select-the-cheapest-carrier-per-shipment

This means the general "choose the best reverse-logistics carrier/location" layer is already mature.

The only potentially distinct residual layer is the exact **9610 customs re-entry action**.

That is also the layer whose neutral third-party callability is not proven.

## Economics fail

No current evidence establishes a native third-party payout, take rate or machine-contribution payment for a
neutral 9610 route selector.

Seller cost savings are real, but:

```text
SELLER SAVES MONEY
!=
NEUTRAL ROUTER HAS ECONOMICS
```

Without a native economic rail, the product risks collapsing into enterprise sales, consulting or an embedded
feature of a logistics/platform operator.

## Operator-asset fail

The original asset hypothesis was cross-provider realized:
- reverse cost;
- clearance time;
- inbound time;
- recoverability outcomes.

But no public evidence establishes a neutral router's rights to retain and combine those outcomes across
providers.

Without that right, more transactions do not automatically create a stronger independent operator asset.

## Final gate table

```text
NATIONWIDE 9610 CHOICE SET             PASS
MULTIPLE PHYSICAL ROUTES               PASS
GENERIC RETURN/WAREHOUSE APIs           PASS
TWO INDEPENDENT CALLABLE 9610 RAILS     NOT PROVEN — NONCOMPENSATORY FAIL
STRUCTURED CROSS-RAIL OUTCOMES          NOT PROVEN
CROSS-PROVIDER OUTCOME REUSE RIGHTS     NOT PROVEN
NON-CONSULTING ROUTER ECONOMICS         NOT PROVEN — NONCOMPENSATORY FAIL
GENERIC RETURN ROUTING WHITE SPACE      FAIL — MATURE CONTROL SURFACE
```

## Reconsideration rule

Do not revive Scan 016-F1 because another port announces 9610 cross-customs return support.

Reconsider only if new evidence proves all of:
1. two independent providers expose or contractually confirm machine-callable 9610 cross-customs
   quote/order/status/outcome rails;
2. a neutral operator has non-consulting economics;
3. cross-provider non-identifying outcome retention/reuse rights are established.

Until then, the formation is resolved/demoted.
