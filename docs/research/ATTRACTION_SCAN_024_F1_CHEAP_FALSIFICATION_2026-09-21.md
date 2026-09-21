# ATTRACTION_SCAN_024-F1 — cheap falsification

Date: 2026-09-21  
Formation: `MULTI_PROVIDER_PREPAID_QUOTA_POOL_ROUTER` / 多模型预付额度池消耗路由器  
Verdict: **DEMOTED — active open-source control surface and non-compounding gateway feature**  
Commercial candidate: **NO**  
First external value flow: **NOT_PROVEN**

## Decision

Do not build this as a standalone business.

The underlying problem is real: prepaid AI quota can reset or expire, and provider-native package state is
machine-readable. But the exact control edge is already being implemented inside mature/open-source gateways
and provider-native entitlement systems.

## Kill 1 — exact active incumbent exists

OmniRoute currently describes itself as a multi-provider AI gateway with quota-aware auto-fallback. Its routing
surface includes remaining-quota and reset-aware strategies and explicitly targets subscription quota that
would otherwise expire.

Source:
- https://github.com/diegosouzapw/OmniRoute

This is not a weak lookalike. It occupies the same control loop:

```text
MULTIPLE PROVIDER CONNECTIONS
+ QUOTA / RESET STATE
→ RANK ELIGIBLE TARGETS
→ ROUTE REQUEST
→ FALL BACK WHEN QUOTA IS EXHAUSTED
```

## Kill 2 — the missing generic adapter is already being absorbed

OmniRoute issue #13616 requested generic billing/quota support for arbitrary OpenAI-compatible connections:
a configurable quota endpoint plus field mapping into a common `UsageQuota` representation.

The issue was opened on 2026-09-13 and closed as **completed** on 2026-09-18.

Source:
- https://github.com/diegosouzapw/OmniRoute/issues/13616

That matters because Scan 024-F1's supposed edge was precisely to normalize Tencent/Alibaba/other provider
package state and feed it into quota-aware routing.

LiteLLM issue #31823 independently asks for provider quota pools/package-based routing as a first-class router
concept:
- https://github.com/BerriAI/litellm/issues/31823

The conclusion is not "nobody wants it." The conclusion is **the ecosystem treats it as gateway functionality**.

## Kill 3 — provider and aggregator internalization

Alibaba Token Plan team plans already prioritize the shared usage package nearest expiry when several packages
are present:
- https://help.aliyun.com/zh/model-studio/token-plan-team-overview

Current enterprise multi-model subscriptions also reduce the fragmentation itself. Qiniu publicly markets a
single enterprise subscription/API key spanning models from multiple vendors under one shared quota pool:
- https://news.qiniu.com/archives/1788856850196

Those structures compress the residual cross-provider waste the standalone router would monetize.

## Kill 4 — no distinct compounding operator asset

The state used by this router belongs to:
- provider quota/billing APIs;
- customer credentials;
- customer workload/policy metadata.

Routing outcomes do not naturally create a proprietary acceptance graph or exclusive transaction rail.
A better routing rule can be copied into open-source gateways. The operator does not gain stronger control
merely because more requests pass through it.

This fails the project's compounding-asset floor.

## Payer evidence remains insufficient

Prepaid quota waste is observable, and current enterprise-plan comparison material explicitly warns that
unstable utilization can waste non-rollover quota.

But the direct LiteLLM request has only sparse public engagement, and no current evidence proves that a buyer
will pay a separate vendor for this narrow function rather than expect it from LiteLLM, OmniRoute, its cloud
gateway, or the provider itself.

Therefore:

```text
REAL PAIN = YES
MACHINE STATE = YES
EXACT INCUMBENT = YES
STANDALONE PAYER = NOT PROVEN
DISTINCT OPERATOR ASSET = NO
COMMERCIAL FORMATION = NO
```

## Final state

`ATTRACTION_SCAN_024-F1` is removed from active validation.

Do not revive it because a new provider adds another quota API. Reconsider only if new evidence creates a
scarce control asset that cannot be copied as ordinary gateway functionality.

Proceed to Scan 025 from fresh high-energy reality without LLM, Token Plan, quota-pool or gateway terms as a
search prior.
