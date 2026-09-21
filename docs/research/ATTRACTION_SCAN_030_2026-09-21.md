# ATTRACTION_SCAN_030 — single-owner manual bridge scan

Date: 2026-09-21  
Status: COMPLETE  
Commercial promotions: **0**  
Retained research formations: **0**  
First external value flow: **NOT_PROVEN**

## Search rule

Scan 030 removed the two-sided marketplace problem entirely.

Required shape:

```text
ONE ACTOR OWNS INPUT DATA
+ SAME ACTOR OWNS FINAL ACTION RIGHT
+ NO NEW SUPPLY
+ NO MARKETPLACE LIQUIDITY
+ REPEATED MANUAL CROSS-SYSTEM BRIDGE
```

The hypothesis was that this might reveal a lightweight, founder-independent control edge.

The scan instead found that the most visible bridges are already the core territory of RPA, IDP, low-code,
ERP/TMS/BMS and vertical SaaS.

## Logistics AR/AP reconciliation

Current logistics firms still face genuinely painful multi-system reconciliation. A recent Kingdee description
of 3PL finance notes that TMS, WMS and customer ERP formats often require manual document collection and
cross-checking.

But the same product category already executes the bridge:
- multi-system/API collection;
- OCR extraction;
- rule normalization;
- automatic matching;
- difference marking;
- settlement-document generation;
- ERP writeback.

Source:
- https://www.kingdee.com/resources/articles/1455247181102503105

Current BMS products likewise convert WMS/TMS operational events into AR/AP bills under contract rules.

Source:
- https://www.ittx.com.cn/article/logistics-ar-ap-automated-reconciliation-guide.html

Verdict: **demoted — exact vertical automation**.

## Manufacturing BOM/report/order bridges

Manufacturing users still move data between ERP, MES, PLM, WMS, OA, email and Excel.

But current RPA/agent tooling explicitly targets:
- BOM import and version comparison;
- inventory threshold → purchase request;
- order → invoice/voucher generation;
- report aggregation;
- cross-system writeback.

Sources:
- https://cloud.tencent.com/developer/article/2638530
- https://www.ai-indeed.com/encyclopedia/18806.html

The bridge is real. The transformation is generic.

Verdict: **demoted**.

## Cross-border declaration data re-entry

A seller can own the source order and the declaration right yet still hate repeated customs-data entry.

But current declaration SaaS already offers:
- API integration with ERP/platforms;
- Excel imports;
- light manual entry;
- document generation;
- one-click declaration.

Source:
- https://www.kjtong.com/

Verdict: **demoted — existing integration/declaration SaaS**.

## Chain-store omnichannel settlement

Multi-channel receipts from Meituan, Taobao instant retail, Douyin, WeChat and other channels create difficult
headquarters-to-store reconciliation.

Current platforms already aggregate and reconcile this state:
- 食亨 performs channel revenue aggregation, line-item settlement checking and automated split settlement.
- 企迈 provides unified multichannel settlement and difference reconciliation.
- 有赞 provides collection, rules and automatic brand/store split settlement.

Sources:
- https://www.shihengtech.com/products/settlement
- https://www.qmai.com/payment/
- https://www.youzan.com/chanpin/weixinshoukuanfzgl

Verdict: **demoted — exact control surface**.

## Small-logistics WeChat/Excel order capture

The smallest operators make the manual bridge especially visible: orders arrive through chat or spreadsheets.

But even lightweight TMS products now advertise:
- WeChat/Excel order import;
- dispatch;
- automatic billing;
- reconciliation;
- dashboards.

Source:
- https://www.yunjux.com/

Verdict: **demoted**.

## Main learning

The stronger boundary solved one problem but exposed another:

```text
ONE OWNER + OWNED ACTION RIGHTS
REMOVES MARKETPLACE LIQUIDITY RISK

BUT

COPY/PASTE + EXCEL + RECONCILIATION
IS THE NATIVE TERRITORY OF GENERIC AUTOMATION
```

A future single-owner formation must not be merely data movement.

## Scan 031 boundary

Search formation-diverse, current **exceptions** where:

- one actor already owns the inputs;
- one actor already owns the action right;
- the consequence of the exception is material;
- generic RPA cannot decide the exception from field mapping alone;
- a bounded, reusable domain state might still make the decision machine-resolvable;
- recurring human expert judgment is not required.

```text
EXCEPTION EVENT
+ NON-GENERIC DOMAIN STATE
+ OWNED ACTION RIGHT
+ REUSABLE MACHINE DECISION
!=
GENERIC RPA
```

This is a search boundary, not a required product shape. Zero retention remains valid.
