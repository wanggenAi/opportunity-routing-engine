# ATTRACTION_SCAN_027 — contract-value recovery falsification

Date: 2026-09-21  
Status: COMPLETE  
Commercial promotions: **0**  
Retained research formations: **0**  
First external value flow: **NOT_PROVEN**

## Hypothesis tested

Scan 027 asked whether companies are failing to collect money or credits that are **already contractually
owed**, because a trigger is missed.

The intended shape was:

```text
CONTRACT TERM
+ MACHINE-DETECTABLE EVENT
+ MONEY / CREDIT ALREADY OWED
→ DETECT
→ CALCULATE
→ CLAIM
→ RECOVER
```

This is a real value pattern. It is not white space.

## SLA/service-credit recovery

Cloud and SaaS SLAs often require the customer to claim within a limited window. Tencent Cloud, for example,
documents service-credit compensation and a claim deadline through its ticket system.

Sources:
- https://cloud.tencent.com/document/product/301/71771
- https://cloud.tencent.com/document/product/301/50679

But exact recovery products already exist:

- Complaya monitors 190+ providers, detects SLA violations and auto-files credit claims.
  https://www.complaya.ai/
- Reclivio extracts SLA terms, monitors vendors and drafts/sends/tracks credit requests.
  https://reclivio.com/
- AllCaps explicitly markets automated SLA credit recovery, contract-to-invoice auditing and claim tracking.
  https://www.allcaps.ai/sla-credit-recovery
  https://www.allcaps.ai/

Verdict: **demoted — exact incumbent control surface**.

## Vendor rebates / tiered discounts

Retail, distribution and channel systems already treat rebates as standard structured finance.

Examples:
- Kingdee commodity rebate module:
  https://help.open.kingdee.com/dokuwiki_std/doku.php?id=%E5%95%86%E5%93%81%E8%BF%94%E5%88%A9
- Sixun supplier-contract rebate rules:
  https://service.sixun.com.cn/KB/OnlineDocReading.aspx?ID=334
- PRM/DMS rebate workflow:
  https://www.xiaoshouyi.com/prm
  https://wanmi.com/zh-CN/products/b2b

These products configure rebate formulas, ingest transaction data, calculate accruals and support settlement.

Verdict: **demoted — standard ERP/DMS/PRM capability**.

## Contract-to-invoice price / credit assurance

The broader "read the contract, compare performance/invoice, recover missed value" surface is also mature.

Sirion links obligations and SLAs to performance and billing, auto-validates invoices and calculates credits
and earnbacks:
- https://www.sirion.ai/platform/manage/contract-performance-management/

AllCaps performs contract-first vendor-invoice audit and tracks identified recovery:
- https://www.allcaps.ai/

Verdict: **demoted**.

## Claims/deductions

Supplier and customer claims are likewise already represented in QMS and revenue-recovery tooling. Modern
claims agents validate deductions against contracts/SLAs and automate adjustment/credit workflows.

Examples:
- https://reclaimit.com/claims
- https://www.putitforward.com/platform/agents/operations-and-finance/claims-disputes-resolution-agent

Verdict: **demoted**.

## Why zero retention is correct

The important outcome is methodological.

After Scan 026, "already owed money" looked narrower than generic cost optimization. But repeated searching
around credits/refunds/rebates creates another hidden ontology. The world is again being forced into one
favorite mechanism.

So Scan 028 resets that bias.

## Scan 028 boundary

Do not start from money-recovery vocabulary.

Start from **new current behavior**:
- what people/companies newly started doing in 2026;
- where they formed manual workarounds;
- where a resource is being used differently;
- where new tools changed who can act;
- where actors repeatedly cross systems or organize informal flows;
- where a new participant appears in a value chain.

Then test commercial floors only after the formation is observed.

```text
CURRENT BEHAVIOR FIRST
VALUE MECHANISM SECOND
BUSINESS THEORY LAST
```

Scan 028 must not inherit cost optimization, refund, rebate, SLA-credit, routing or any active validation
vertical as a search prior.
