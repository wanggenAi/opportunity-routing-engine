# ATTRACTION_SCAN_113 — Completed-control + post-transfer cashflow pass

**Date:** 2026-09-22  
**Status:** COMPLETE  
**Primary research domain:** CHINA  
**Commercial promotions:** 0  
**Retained research formations:** 0  
**FIRST_EXTERNAL_VALUE_FLOW:** NOT_PROVEN

## Purpose

Scan 113 stops treating a transfer listing, consent or transfer path as sufficient evidence. The pass requires an **actually completed controlling transfer** and then asks whether the same target continues to generate external value after control changes.

The strongest public evidence source in this pass is purchase accounting: purchase date, realized control consideration, and purchase-date-to-period-end revenue / profit / cashflow for the acquired target.

```text
COMPLETED CONTROLLING TRANSFER
+ SAME ENTITY / SAME CONTROL POSITION
+ POST-TRANSFER EXTERNAL REVENUE
+ POST-TRANSFER PROFIT
+ POST-TRANSFER CASHFLOW
+ RIGHTS CONTINUITY
+ LOW OWNER / REPLACEMENT LABOR
+ BOUNDED CAPITAL
+ NONCOMMODITY MACHINE-OPERABLE CONTROL
=> POSSIBLE VERIFIED POST-TRANSFER CONTROL CASHFLOW
```

## Result

| Formation | Strongest evidence | Decisive failure |
|---|---|---|
| Boke Guoxin healthcare information / AI software | control rose from 32% to 70%; post-purchase revenue RMB47.82m and net profit RMB8.15m | post-purchase cashflow negative RMB2.26m; enterprise healthcare integration/support labor and capital not closed |
| Xinyan Micro fabless sensor chips | completed 100% acquisition; post-purchase revenue RMB29.83m and net profit RMB10.83m | post-purchase cashflow negative RMB0.83m; recurring expert R&D/design-in/supply-chain work; RMB160m entry |
| Youde renewable O&M platform | completed 70% control acquisition; post-acquisition smart-O&M segment revenue reported | target-specific post-purchase profit/cashflow not isolated; 100+ service centers and professional field engineers remain core delivery |

No formation survives every floor.

## F1 — Boke Guoxin: completed software control and positive accounting profit still do not close cash generation

Shanghai JHCT moved from a pre-existing 32% interest to 70% control of Boke Guoxin in 2026. The incremental 38% control acquisition consideration was approximately RMB73.7102 million.

Sources:
- https://static.cninfo.com.cn/finalpage/2026-04-29/1225227412.PDF
- https://static.cninfo.com.cn/finalpage/2026-08-28/1225520056.PDF
- https://www.stcn.com/article/detail/3631826.html

The half-year acquisition accounting table reports purchase-date-to-period-end revenue of RMB47.8185 million and net profit of RMB8.1473 million. This is real post-control economic continuity, not a pre-transfer estimate. But the same table reports cashflow of **negative RMB2.2650 million**.

The target owns specialized healthcare-information products and AI/domain capability, so it is not trivially generic-agent substitutable. That does not cure the remaining failures: hospital integration, data governance, implementation/support effort, institution-specific permissions and replacement labor remain unclosed, while the control consideration is far outside bounded small-operator capital.

**Verdict:** demoted.

## F2 — Xinyan Micro: specialized IP survives generic-agent substitution but still requires expert organization

MIXC Integrated Circuits completed a 100% acquisition of Shanghai Xinyan Microelectronics on 2026-03-20.

Sources:
- https://static.cninfo.com.cn/finalpage/2026-08-31/1225535290.PDF
- https://www.stcn.com/article/detail/3617792.html

The acquisition-accounting table binds RMB160 million of control cost to purchase-date-to-period-end revenue of RMB29.8339 million and net profit of RMB10.8331 million. Cashflow over the same post-purchase interval was **negative RMB0.8265 million**.

The fabless model is less asset-heavy than owning fabrication plants, and the chip IP/product position is genuinely noncommodity. But the business still requires recurring semiconductor R&D, verification, customer design-in, foundry/supply-chain coordination and technical support. This is a specialized technology company, not a founder-light machine-operated routing asset.

**Verdict:** demoted.

## F3 — Youde renewable O&M: software platform plus completed control still rests on field-service labor

Shenzhen Sunrise New Energy completed its 70% acquisition of Youde New Energy Technology (Ningbo) on 2026-05-29. The deal includes RMB100 million fixed consideration plus up to RMB56.8 million conditional consideration.

Sources:
- https://static.cninfo.com.cn/finalpage/2026-08-28/1225517056.PDF
- https://www.stcn.com/article/detail/4141499.html
- https://www.stcn.com/article/detail/3869512.html
- https://static.cninfo.com.cn/finalpage/2026-04-29/1225244453.PDF

The target has a real UniCare software/data platform and a nationwide O&M footprint, but that footprint explicitly includes more than 100 local service centers and professional O&M engineers. The buyer's 2026 H1 smart-O&M segment reported RMB17.4668 million of revenue after the acquisition, but the public packet does not isolate purchase-date-to-period-end target revenue, target profit and target operating cashflow as one target-level accounting record.

The platform therefore fails two hard tests at once: target-specific post-transfer cash generation is unclosed, and recurring field engineering remains an essential value-delivery layer.

**Verdict:** demoted.

## Excluded observations

- A current Suzhou capacitor-manufacturer acquisition has positive 2026 H1 profit but remains physical manufacturing with specialized production labor and lacks a clean target-level post-purchase revenue/cashflow packet.
- A current large battery-separator acquisition has very strong post-transfer revenue/profit but is an obvious large-capital physical-manufacturing duplicate.
- A current seed-company control acquisition reports negative purchase-date-to-period-end net profit and operating cashflow and therefore fails before machine-control analysis.
- Smaller current technology acquisitions with zero or negative post-purchase operating results were excluded early.

## Learning

```text
COMPLETED CONTROL
+ POSITIVE POST-PURCHASE REVENUE
+ POSITIVE POST-PURCHASE NET PROFIT
!= POSITIVE POST-PURCHASE CASH GENERATION

PLATFORM SOFTWARE
!= MACHINE DELIVERY
WHEN FIELD ENGINEERS / IMPLEMENTATION TEAMS REMAIN CORE

SPECIALIZED IP
!= FOUNDER-LIGHT CONTROL
WHEN RECURRING EXPERT ORGANIZATION IS REQUIRED
```

Scan 113 materially improves evidence quality: it proves that completed control plus positive post-purchase revenue/profit exists in current China public records. The next discriminator is stricter and more useful: **positive post-transfer operating cashflow plus explicit low human-service burden**.

This is an evidence-priority change, not a product or vertical thesis.

## Parallel validation

`ATTRACTION_SCAN_015-F1` remains unchanged and still requires an actual official written provider response/agreement plus organic founder-free inbound proof. No response is neither a pass nor a denial.

## Next

Validate Scan 113 on one exact final PR head with repository CI and live TypeSafe/Jev. If autonomous continuation remains allowed, run Scan 114 with completed-control + positive post-transfer operating-cashflow + low-human-service priority.
