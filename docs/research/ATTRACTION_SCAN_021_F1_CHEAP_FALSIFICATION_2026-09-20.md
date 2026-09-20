# ATTRACTION_SCAN_021-F1 — cheap falsification

Date: 2026-09-20  
Formation: `SME_OVERDUE_PAYMENT_EVIDENCE_COMPILER` / 中小企业逾期回款证据编译器  
Verdict: **DEMOTED — generic-agent substitutable and value-layer squeezed**  
Commercial candidate: **NO**  
First external value flow: **NOT_PROVEN**

## Decision

Do not build an MVP and do not run founder-led sales for this formation.

The underlying pain is real and economically important, but the hypothesized standalone software layer does
not survive the repository's commercial hard floors.

## Decisive kill 1 — generic-agent substitutability

The narrow product was supposed to accept a company's contract, delivery/acceptance, reconciliation,
settlement and payment records, then map them into the public complaint schema and generate a packet.

That bridge is fundamentally:

```text
PRIVATE_USER_DOCUMENTS
+ PUBLIC_OFFICIAL_RULE_SCHEMA
→ FACT_EXTRACTION
→ COMPLETENESS_CHECK
→ DRAFTED_PACKET
```

The official form already exposes the core structured fields and attachments. Generic AI tools already
generate collection/legal-document drafts from user facts. The basic bridge therefore does not require a
distinct operator-owned data asset, scarce right, unique execution rail, or proprietary outcome graph.

Sources:
- Official national complaint platform: https://sme-dj.miit.gov.cn/
- Public complaint form with structured identity/contract/amount/evidence fields:
  https://interests.ssme.sh.gov.cn/demands/form.html
- Current free generic legal-document generator example:
  https://www.utoolhub.com/legalcraft

This triggers the existing hard kill:

`GENERIC_AGENT_SUBSTITUTABILITY_SHOULD_KILL_HIGH_ATTRACTION`.

## Decisive kill 2 — the value layer is squeezed from both sides

### Simple cases

The official rail is public and directly accessible. The regulation also explicitly encourages legal service
institutions to provide public-interest legal services to SMEs in payment disputes.

Source:
- https://www.miit.gov.cn/xwfb/gxdt/sjdt/art/2025/art_2610a93b60554b9c81d6e37c2bc8232f.html

That does not mean every SME gets free full representation. It does mean a narrow paid "help me prepare the
official complaint packet" product faces structural price pressure from the official workflow, public guides,
generic AI and public-interest support.

### Complex cases

When the value comes from deciding whether facts are disputed, choosing a legal path, negotiating, preserving
assets, litigating, arbitrating or enforcing, the work moves into the professional legal-service layer.

The Shanghai Lawyers Association's current 2026 trial guidance defines enterprise receivables work as a
full-lifecycle legal service spanning non-litigation collection, negotiation, lawyer letters, mediation,
litigation, arbitration, preservation and enforcement:
- https://info.lawyers.org.cn/info/20bfcad74f7c43ae9c0fdc7ce557c05d

Current market evidence also shows enterprises paying lawyers on recovered-value economics. A 2026 Nanjing
receivables collection procurement reported bids of 6%, 9% and 10% of successfully recovered funds:
- https://www.yfbzb.com/winbid/detail/20260811_621437621.html

That is strong evidence that money exists in receivables recovery. It is **not** evidence that the narrow
self-serve packet compiler gets paid. Instead it reinforces the squeeze:

```text
LOW COMPLEXITY → official/free/generic AI
HIGH COMPLEXITY → licensed professional service
MIDDLE PACKET COMPILER → weak distinct value capture
```

## Decisive kill 3 — no compounding operator asset

The official platform owns the complaint submission and result rail. The proposed operator would mostly see
documents the user uploads for one case.

No current evidence proves:
- automatic return of final recovery outcomes to the compiler;
- a proprietary acceptance/rejection graph unavailable to generic agents;
- exclusive submission rights;
- a reusable data advantage that compounds with volume.

Without one of those, repeated usage does not clearly strengthen the operator's control position.

## What remains true

The scan was still useful.

It proved that formation-diverse search can surface a non-router mechanism. It also generated a durable
lesson: **direct-cash pain is not enough when the proposed intermediary is squeezed between free automation
and licensed expert service.**

The official payment-recovery rail remains economically meaningful, but the rail's value belongs mainly to
the SME receiving payment and to professional services that contribute non-commoditized judgment/execution.
It does not automatically create economics for a thin packet-preparation layer.

## Final state

```text
ATTRACTION_SCAN_021-F1
RESEARCH BEACON → DEMOTED
ACTIVE COMMERCIAL CANDIDATE = NO
ACTIVE VALIDATION = NO
FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN
```

Do not revive this formation unless new evidence proves a genuinely non-generic control asset or a native
paid rail for the machine contribution.

Proceed with Scan 022 from broad reality without inheriting overdue-payment/legal-tech terms.
