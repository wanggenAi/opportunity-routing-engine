# ATTRACTION_SCAN_068 — Atomic paid-unit attribution pass

**Date:** 2026-09-22  
**Status:** COMPLETE  
**Commercial promotions:** 0  
**Retained research formations:** 0  
**FIRST_EXTERNAL_VALUE_FLOW:** NOT_PROVEN

## Search question

Scan 067 proved that two external payments can still buy a broad service bundle rather than a machine-resolvable unit.

Scan 068 therefore admitted only formations where buyer spend can be attributed to the **unbundled atomic execution unit itself**, with unit/task-level pricing and an objective acceptance test wherever possible.

## Result

Six formation-diverse unit-priced markets were pressure-tested. None survived.

The core pattern changed:

```text
ATOMIC UNIT + DIRECT UNIT PRICE
→ objective acceptance?
→ if yes: category tends to become a metered API utility
→ if no: residual value remains human semantic/compliance responsibility
```

Atomic payment attribution is a strong evidence filter, but it is not a white-space detector.

## Formations

### F1 — Email verification per address

Independent buyers report current pay-as-you-go verifier spend, and ZeroBounce explicitly meters one email check as one credit.

This passes unit attribution cleanly. It also exposes why the unit is commercially mature: multiple dedicated verification providers already price the exact unit, while current waterfall products route unresolved/catch-all addresses across multiple verifiers.

**Closure:** real atomic spend; exact commodity category plus existing waterfall orchestration.

### F2 — Speech-to-text per audio duration

Users report adding API credits and paying by audio minute; current podcast buyers complain specifically that Rev's per-minute cost grows with episode duration.

The unit is clean and machine-executable. AssemblyAI currently bills pay-as-you-go transcription by exact audio duration, and local/open alternatives continue to compress the cost of raw transcription.

**Closure:** real duration-attributed spend; mature usage-based API utility.

### F3 — PDF accessibility remediation per page

Current public contracts and buyer reports price remediation by source page, commonly around $5-$6/page.

This passes economic attribution but fails the machine-acceptance floor. Allyant's own current CommonLook guidance says the highly automated editor still requires human manual verification and possible correction. Reading order, meaningful alt text, semantic structure and assistive-technology behavior cannot be reduced to a single deterministic checker result.

**Closure:** real per-page spend; human semantic/compliance acceptance remains intrinsic.

### F4 — KYC / identity verification per check

Current teams use third-party document/liveness vendors on per-check economics, and Stripe Identity currently prices completed document+selfie verification at $1.50 per verification.

The atomic unit and billing are explicit. But identity verification is already a mature API category, and current KYC orchestration products explicitly route among multiple providers by market, risk, coverage, cost and failure.

**Closure:** real per-verification spend; mature IDV plus mature orchestration/control plane.

### F5 — OCR / document text extraction per page

Current users report paid page-level OCR/vision workloads, while AWS Textract explicitly prices raw OCR by page.

This is one of the cleanest machine-verifiable atomic units in the scan. It is also already hyperscaler infrastructure, with raw text extraction priced at fractions of a cent per page and local/open models creating further substitution pressure.

**Closure:** real per-page spend; mature infrastructure commodity.

### F6 — SMS OTP per successful verification / message

Current developers report paying per SMS, and production teams actively use or switch among Twilio, Telnyx and Vonage. Twilio Verify currently charges per successful verification plus channel fees.

Again the unit is explicit and objective. But CPaaS is mature, and multi-provider messaging routing/failover is already an explicit product category.

**Closure:** real per-event spend; mature CPaaS plus existing multi-provider routing.

## Learning

Scan 068 falsifies a tempting shortcut:

```text
TWO BUYERS PAY FOR THE SAME ATOMIC UNIT
!=
UNOWNED COMMERCIAL EXECUTION LAYER
```

When acceptance is objective enough to meter directly, suppliers can expose the unit as API infrastructure and competition forms quickly.

The more useful residual signal is now visible **between suppliers**, not inside the atomic task: buyers sometimes pay multiple interchangeable providers because coverage, accuracy, latency, price or availability differs.

That observation is not yet a commercial formation. Scan 069 must require direct buyer evidence of **concurrent multi-supplier spend for the same atomic unit**, with buyer-controlled switching/fallback and measurable provider variation. Existing orchestration/aggregation control surfaces must be preflighted before any retention.

## Parallel validation

ATTRACTION_SCAN_015-F1 remains independent and unchanged. Written provider rights evidence and founder-free inbound proof remain outstanding.

## Next

Advance to `ATTRACTION_SCAN_069` only if the live Jev continuation directive permits reversible research continuation.
