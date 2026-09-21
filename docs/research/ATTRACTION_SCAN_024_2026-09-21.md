# ATTRACTION_SCAN_024 — high-energy micro-edge scan

Date: 2026-09-21  
Epoch: `ATTRACTION_FIELD_V1`  
Status: COMPLETE  
Commercial promotions: **0**  
Retained research formations: **1**  
First external value flow: **NOT_PROVEN**

## Search rule

Scan 024 follows the boundary left by Scan 023:

```text
HIGH-ENERGY EXISTING FLOW
→ REPEATED LEAKAGE / DELAY / UNCERTAINTY
→ ONE NARROW UNOWNED MICRO-EDGE
→ MACHINE-RESOLVABLE STATE
→ EXISTING EXECUTION RAILS
→ DO NOT REBUILD THE WHOLE MARKETPLACE
```

The scan explicitly rejects "hot market = opportunity" and "build another gateway/marketplace" logic.

## Retained research beacon

### ATTRACTION_SCAN_024-F1 — MULTI_PROVIDER_PREPAID_QUOTA_POOL_ROUTER
Chinese: **多模型预付额度池消耗路由器**

This is **not** a generic LLM cost router and not another model marketplace.

The narrow hypothesis is:

1. an enterprise has already bought prepaid AI packages / Token Plans from multiple providers or accounts;
2. each package has its own remaining quota, supported models/capabilities and reset/expiry window;
3. some compatible workloads can run on more than one purchased package;
4. the router reads provider-native quota state;
5. it sends the next compatible request toward already-paid capacity that is most at risk of expiring;
6. PAYG or lower-priority capacity is used only when prepaid capacity is unavailable, incompatible or intentionally reserved.

The value target is **unused already-paid capacity**, not generic model-price arbitrage.

## Why this is a real machine state

### Tencent TokenHub exposes package balance and expiry through API

Tencent's current Token Plan data model exposes:
- total quota and total used;
- cycle quota/current cycle;
- start and expiry time;
- exclusive/shared pool quantities;
- API-key subpackage balance;
- model allowlists and quota-exhausted status.

Sources:
- https://cloud.tencent.com/document/api/1823/132279
- https://cloud.tencent.com/document/product/1823/132270
- https://cloud.tencent.com/document/api/1823/132276
- https://cloud.tencent.com/document/product/1823/130660

That means the router does not need browser scraping just to know whether a Tencent package has remaining
capacity.

### Alibaba also exposes expiring/non-rollover plan state

Alibaba Model Studio documents that unused personal-plan credits do not roll into the next 7-day window and
team-plan monthly quota does not roll over. It also now exposes Token Plan usage through the official CLI and
shared-package detail through OpenAPI.

Sources:
- https://help.aliyun.com/zh/model-studio/token-plan-overview
- https://help.aliyun.com/zh/model-studio/token-plan-personal-faq
- https://help.aliyun.com/zh/model-studio/cli/usage-quota
- https://help.aliyun.com/zh/model-studio/list-subscription-shared-packages
- https://help.aliyun.com/zh/model-studio/token-plan-team-overview

So at least two major China-provider ecosystems expose machine-readable or machine-invocable plan state.
This is stronger than a hypothetical dashboard-only quota.

## Why this is narrower than existing gateway cost control

Generic AI gateway control is already mature.

Cloudflare AI Gateway supports:
- dollar spend limits by provider/model/metadata;
- rate and budget nodes;
- dynamic routing and fallback.

Sources:
- https://developers.cloudflare.com/ai-gateway/features/spend-limits/
- https://developers.cloudflare.com/ai-gateway/features/dynamic-routing/

Kong AI Gateway also manages model/provider cost for governance, budget enforcement and chargeback:
- https://developer.konghq.com/ai-gateway/model-cost-management/

Those products validate enterprise demand for AI-governance control, but their current public documentation
does not establish a first-class abstraction that continuously reads **external prepaid provider-package
remaining entitlement + expiry** and routes to consume that entitlement before it vanishes.

That distinction is the only reason F1 survives this scan.

## Direct gap evidence: LiteLLM issue #31823

On 2026-07-01, an open LiteLLM feature request asked for **provider quota pools / package-based routing** as a
first-class routing concept.

The issue explicitly describes enterprise deployments that purchase quota from multiple vendors/accounts,
where each package has its own usage window and remaining capacity. The desired router selects a provider
package based on remaining quota, priority, routing weight and capabilities, with package-level reconciliation.

Source:
- https://github.com/BerriAI/litellm/issues/31823

This is unusually direct evidence that the micro-edge is not invented from scratch.

It is **not** evidence that a standalone business exists. In fact, it creates the opposite risk: a mature
gateway may absorb the feature quickly.

## Why F1 is not a commercial candidate

Hard unknowns remain:

- whether anyone will pay separately for prepaid-quota utilization instead of accepting it as a gateway feature;
- whether savings are material after workload-quality, model-capability and data-policy constraints;
- whether quota state can be refreshed reliably for enough providers and account/package types;
- whether provider terms permit automated routing across packages/providers;
- whether BYOK credential handling/security makes activation too expensive;
- whether LiteLLM, Cloudflare, Kong or the model providers absorb the feature before a business can form;
- whether any operator asset compounds beyond open-source routing code;
- whether buyers with multi-provider prepaid waste can be discovered without founder-led enterprise sales.

Therefore:

```text
FEATURE GAP != BUSINESS
OPEN ISSUE != PAYER
MACHINE STATE != OPERATOR CONTROL
```

## Other micro-edges tested

### Cross-order travel disruption/refund orchestration — demoted

Travel refund/change pain is large, but leading OTAs are already internalizing linked guarantees, anomaly
checks and fast refund/change flows. Cross-platform execution rights remain fragmented.

Verdict: **platform internalization + fragmented action rights**.

### Rental-housing deposit evidence assistant — demoted

Deposit disputes are real, but deposit supervision/custody, platform guarantees, move-out condition reports
and existing evidence-helper apps are already absorbing the obvious workflow.

Verdict: **regulatory/platform absorption**.

### Generic LLM cost router — demoted

Provider/model routing, dollar budgets, rate limits, spend management and fallback are already standard AI
gateway functions.

Verdict: **mature gateway control surface**.

## Next falsification

Do not build a standalone product yet.

Run the cheapest falsification package:

1. search for an exact existing product/plugin that already consumes provider-native subscription/package balances;
2. quantify realistic wasted prepaid quota for a multi-provider buyer;
3. test one Tencent + one Alibaba machine-state adapter without scraping;
4. prove compatible-workload routing can preserve quality/security/data-residency constraints;
5. determine whether a buyer would pay for savings or expects the gateway/provider to include this for free;
6. watch LiteLLM #31823 and adjacent gateway releases for rapid feature absorption;
7. kill F1 if the durable result is just a small open-source gateway feature with no compounding operator asset.

In parallel, Scan 025 must restart from high-energy reality and **must not inherit LLM/quota/gateway terms as
a search prior**.
