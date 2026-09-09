# AGENTS.md

Instructions for AI agents, coding assistants and human contributors working in this repository.

## Prime directive

The repository builds a truthful, evidence-driven **Actor-First Resource Orchestration Engine**.

Its purpose is to repeatedly:

1. observe real-world change and friction;
2. identify the desired outcome and payer;
3. convert ambiguous demand into a bounded transaction objective;
4. decompose that objective into `CapabilityUnit`s;
5. route capability units to suitable people, organizations, AI, assets, venues, channels or other resources;
6. define incentives, interfaces, trust and acceptance criteria;
7. execute, accept and settle the transaction;
8. record outcomes, reliability, economics and replacement behavior;
9. improve future routing;
10. automate only repeated proven bottlenecks.

Strategic kernel: `docs/RESOURCE_ORCHESTRATION_KERNEL.md`.

Optimize for **commercial truth + completed accepted outcomes + delegatability + orchestration economics**, not code volume, founder activity, idea count or narrative appeal.

## Source of truth

Before changing business logic, read:

1. `docs/RESOURCE_ORCHESTRATION_KERNEL.md`
2. `docs/FORMAL_TRUTH.md`
3. `docs/ACTOR_MODEL.md`
4. `docs/METHODOLOGY.md`
5. `docs/OPPORTUNITY_SCORECARD.md`
6. `docs/ARCHITECTURE.md`
7. relevant `docs/EXPERIMENT_*.md`

When a major assumption changes, update `docs/FORMAL_TRUTH.md` in the same change.

## Non-negotiable truth rules

- Never fabricate actors, needs, payments, prices, contacts, capabilities, transactions or outcomes.
- `UNKNOWN != PASS`.
- Complaint != demand.
- Demand != willingness to pay.
- Beneficiary != payer by default.
- Trend != business.
- Introduction != orchestration value.
- Founder free labor != profit.
- One transaction != repeatability.
- LLM confidence != commercial evidence.
- Preserve provenance, dates and contradictions.
- Subsidized/officially promoted success must be separated from independent payer evidence.

## Canonical actor roles

Map where relevant:
- `NEED_ACTOR`
- `BENEFICIARY`
- `PAYER`
- `SPONSOR`
- `RESOURCE_OWNER`
- `CAPABILITY_PROVIDER`
- `ORCHESTRATOR`

An actor may hold several roles. The operator is not automatically the capability provider.

## Capability-first execution

The atomic execution unit is a `CapabilityUnit`, not a person.

Every recurring task should, where feasible, define:

```text
purpose
input
required output
acceptance criteria
provider class
proof required
price model
payout condition
deadline / SLA
dependencies
trust / safety requirements
replacement rule
failure / refund rule
```

Candidate capabilities include:
- demand scouting;
- lead qualification;
- sales / BD;
- participant/user recruitment;
- requirements discovery;
- research;
- development;
- design;
- translation;
- venue/asset provision;
- logistics;
- delivery;
- hosting;
- verification;
- QA;
- support;
- settlement administration.

**Sales, acquisition and delivery are routable capabilities. Do not silently assign them to the operator.**

## Delegation-first rule

For every execution task ask:

```text
Can this be eliminated?
Can it be automated safely?
Can it be delegated as a bounded capability unit?
Only if not, should the operator perform it temporarily?
```

If the operator performs a task temporarily, record:
- why delegation was not yet feasible;
- time spent;
- replacement plan;
- `operator_shadow_cost`.

Repeated founder dependence is a bottleneck, not evidence of product-market fit.

## Operator kernel

The initial operator should preferentially retain:
- opportunity judgment;
- transaction architecture;
- capability decomposition;
- interface/acceptance definition;
- incentive design;
- routing approval;
- trust/risk boundaries;
- exception arbitration;
- outcome learning.

Everything else should be tested for delegation or automation.

## Opportunity gates

Before serious promotion, answer:
- `G0 ACTOR_ROLE_CLARITY`
- `G1 PAYER_CLARITY`
- `G2 TRANSACTIONABILITY`
- `G3 LEGAL_TRUST_SAFETY`
- `G4 CAPABILITY_DECOMPOSABILITY / DELEGATABILITY`
- `G5 ORCHESTRATION_VALUE`

G4/G5 may be the explicit unknown in an early experiment, but must pass before a candidate becomes `REPEATABLE` / `SCALE_CANDIDATE`.

## Economic truth

Always distinguish:

```text
cash contribution margin
vs
normalized orchestration margin after operator shadow labor
```

A transaction supported by unpaid founder sales, delivery or QA is not proven economically repeatable.

Early experiments may intentionally buy learning at low/negative normalized margin, but this must be explicit.

## Orchestration value test

Do not defend a model whose only value is exchanging contacts.

Orchestration should create recurring value through one or more of:
- requirement clarification;
- task decomposition;
- provider qualification;
- trust;
- dependency management;
- QA/acceptance;
- replacement;
- settlement;
- outcome accountability;
- accumulated routing/reliability data.

If buyer/provider bypass destroys most value after one introduction, downgrade the opportunity.

## Safety and regulated work

Do not route regulated or safety-sensitive work to unqualified providers.

Children, elderly/vulnerable people, home access, transport, medical, legal, financial, employment-placement and other high-trust activities require elevated legal/trust/safety review.

Commercial attractiveness never overrides safety or law.

## Platform discipline

Do not build a broad marketplace because the conceptual model supports one.

Required maturity path:

```text
real payer
→ bounded transaction
→ capability decomposition
→ manual resource routing
→ accepted delivery
→ settlement
→ delegated acquisition + delegated delivery
→ repeated template
→ provider replacement works
→ normalized positive economics
→ recurring bottleneck identified
→ automation
→ platform/network product only if density justifies it
```

## Development principles

- Small explicit schemas; deterministic validation where possible.
- Separate raw evidence from derived claims.
- Separate actors from roles.
- Separate people/resources from capabilities.
- Separate capability claims from capability proof.
- Separate score from decision.
- Separate cash margin from normalized margin.
- AI classifications must expose evidence and remain reviewable.
- Tests should protect truth gates and lifecycle transitions.
- Never commit secrets or unnecessary private/sensitive data.

## Success definition

The repository succeeds when it increasingly produces transactions with:
- real payer commitment;
- clear capability decomposition;
- routed acquisition/delivery rather than founder dependence;
- accepted output;
- settlement;
- measurable normalized economics;
- repeat/referral;
- replaceable capability providers;
- proprietary outcome/reliability learning that improves future orchestration.

**The engine must win through architecture and routing, not through the operator personally doing everything.**
