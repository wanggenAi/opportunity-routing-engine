# ATTRACTION_SCAN_070 — Buyer-built / self-hosted abstraction residual pass

**Date:** 2026-09-22  
**Status:** COMPLETE  
**Commercial promotions:** 0  
**Retained research formations:** 0  
**FIRST_EXTERNAL_VALUE_FLOW:** NOT_PROVEN

## Search question

Scan 069 proved that concurrent multi-supplier spend creates real routing value but usually inside already-formed orchestration categories.

Scan 070 tested a stronger residual:

> Do two independent current buyers still build or self-host their own provider abstraction in production despite available orchestrators, and can they state why they need that control?

This is materially stronger than merely using multiple suppliers because it exposes engineering spend, lock-in avoidance and operational control directly.

## Result

Six formations were pressure-tested. None survived commercial promotion.

The strongest case was KYC/IDV. Two independent fintech practitioners describe maintaining buyer-owned abstraction layers: one built a backend middleware router so a KYC vendor could be dropped without forcing a mobile release, while another spent six months making providers hot-swappable because false-positive rates, fraud patterns, compliance requirements, pricing and data portability change.

That behavior is real. It is also now directly productized by vendor-neutral KYC orchestration platforms and self-host/open infrastructure.

The same pattern repeats in email, payments, DNS/CDN and LLM gateways. SMS has a strong current custom production example but does not satisfy the strict second-independent-current-production-build floor in this pass.

## Formations

### F1 — Buyer-built KYC / IDV router

This is the strongest behavioral residual.

Two independent practitioners report maintaining vendor abstraction for concrete production reasons: eliminating client release coupling, preserving provider hot-swap, handling changing fraud/false-positive behavior, escaping surprise price increases and protecting data portability.

Current control surfaces now map almost exactly to those motives. Omnified exposes vendor-neutral, per-jurisdiction KYC routing and waterfall fallback. Forest sits above multiple IDV providers. Ballerine exposes workflow/plugin orchestration and self-host/data-ownership semantics; its current repository warns that the OSS version is being rebuilt and is not actively supported, but that caveat does not rescue white space because managed/current alternatives are also present.

**Closure:** buyer-built engineering cost passes; exact control category already exists.

### F2 — Buyer-built multi-provider SMS failover

A current production operator reports an in-house 50/50 Vonage/Telnyx system with failover and sticky per-user provider selection.

A separate infrastructure team publicly describes an internal project to add additional providers alongside Twilio, but the evidence does not prove that second build reached recurring current production.

Open-source communications gateways now implement multi-provider SMS/email failover as reusable infrastructure.

**Closure:** one strong production build; strict second-current-buyer floor fails and exact reusable control surfaces exist.

### F3 — Transactional email provider abstraction

A 2026 Rails operator built a hybrid delivery manager that chooses SES, SendGrid or future providers and manages SES capacity. An independent developer built chain_mail after recurring provider failures, exposing automatic provider failover and runtime provider changes.

Current CourierX and Mailers.io offerings now expose the same one-API / BYOK / multi-provider routing and failover control surface.

**Closure:** buyer-built behavior passes; reusable abstraction is directly productized.

### F4 — Multi-PSP payment abstraction

In-house payment operating systems are a known enterprise pattern, but this pass did not establish two independent fresh buyer-built production cases that explicitly reject current orchestrators.

That evidence gap is secondary because Hyperswitch now supplies the exact reusable layer as Apache-licensed self-hostable infrastructure: many PSP connectors, routing, retries, reconciliation and cost observability.

**Closure:** strict buyer-built floor incomplete; exact self-hosted control plane is mature.

### F5 — Self-hosted multi-provider DNS / CDN control

Teams do maintain provider-independent DNS through Git/IaC and self-hosted tooling. Current public implementations also package multi-DNS synchronization and secondary-CDN failover.

But self-hosting DNSControl or a reusable failover project is not evidence that the abstraction is unowned; it is consumption of the existing open control surface.

**Closure:** control need passes; reusable asset is already open infrastructure.

### F6 — Multi-provider LLM gateway

Current deployed applications implement provider routing/fallback across several model vendors, proving the architecture is ordinary production practice. This pass does not establish two independent buyers explicitly rejecting existing gateways before building.

The exact category is already unusually dense: LiteLLM and several other self-hosted gateways unify provider protocols, routing, fallback, cost control and governance.

**Closure:** explicit bypass floor fails; control surface saturation is decisive.

## Learning and drift audit

Scan 070 surfaces a second-order problem in the research process.

Scans 065 through 070 successively raised the evidence floor:

```text
deterministic paid execution
→ two buyer signals
→ confirmed money motion
→ atomic unit attribution
→ concurrent multi-supplier spend
→ buyer-built provider abstraction
```

Each step improved evidence quality, but the chain has begun to create a hidden mechanism ontology centered on infrastructure orchestration.

The repository has already learned this failure mode once in Scans 053–057. Continuing to derive Scan 071 from another narrower provider-routing residual would optimize the search procedure around its own previous failures rather than around commercial reality.

Therefore Scan 071 is a **broad formation-diverse reset**.

It should start from direct current buyer budget reality—external payment, contract or recurring procurement for a bounded outcome—but must not require atomicity, multi-provider architecture, orchestration, routing, failover, abstraction or software delivery as the opportunity shape.

Scans 065–070 formations are excluded from seeding the reset.

## Parallel validation

ATTRACTION_SCAN_015-F1 remains independent and unchanged. Written provider rights evidence and founder-free inbound proof remain outstanding.

## Next

Advance to `ATTRACTION_SCAN_071` only if the live Jev continuation directive permits reversible research continuation.
