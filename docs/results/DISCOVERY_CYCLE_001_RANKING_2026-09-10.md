# Discovery Cycle 001 — Comparable Ranking

Date: 2026-09-10
Status: `PROVISIONAL STRUCTURAL RANKING / NOT SUCCESS PROBABILITY`

This ranking is the first ranking produced only after the clean-slate discovery stack ran across multiple Xuzhou money flows.

Scores use `docs/OPPORTUNITY_SCORECARD.md`. A score is structural fit, not probability of success. Gates override scores.

## Ranking

| Rank | Candidate | Raw | Penalty | Adjusted | Key gates | Decision |
|---:|---|---:|---:|---:|---|---|
| 1 | Property-anchored community living-service orchestration backend | 85 | -10 bypass risk | **75** | G1 UNKNOWN; G5 UNKNOWN; G6 UNKNOWN | INVESTIGATE / FIRST VALIDATION |
| 2 | Stock-home turnover / repair / handover orchestration | 84 | -10 bypass risk | **74** | G1 UNKNOWN; G3 CONDITIONAL; G5 UNKNOWN | INVESTIGATE |
| 3 | Cross-border seller/export recurring operations routing | 82 | -10 platform/dependency risk | **72** | G1 UNKNOWN; G5 UNKNOWN; G6 UNKNOWN | INVESTIGATE |
| 4 | Public-procurement demand intelligence + qualified-supplier support routing | 81 | -10 payment/procurement-cycle risk | **71** | G1 UNKNOWN for our layer; G3 CONDITIONAL | INVESTIGATE |
| 5 | High-intent visitor → local service/merchant orchestration | 80 | -10 platform dependence | **70** | G1 UNKNOWN; G5 UNKNOWN; G6 UNKNOWN | INVESTIGATE |
| 6 | OPC / micro-enterprise demand-access + delivery-governance route | 79 | -10 low-cost/public incumbent | **69** | G1 UNKNOWN; G5 UNKNOWN | INVESTIGATE |
| 7 | Used engineering-machinery trusted evidence/transaction support | 77 | -10 bypass/incumbent risk | **67** | G3 CONDITIONAL; G5 UNKNOWN | INVESTIGATE |
| 8 | Engineering-machinery aftermarket service/parts routing | 80 | -15 on-site/custom dependence | **65** | G3 CONDITIONAL; G4 UNKNOWN | INVESTIGATE / LATER |
| 9 | County agricultural logistics/cold-chain capacity routing | 75 | -10 acquisition/thin-margin risk | **65** | G1 UNKNOWN; G5 UNKNOWN | INVESTIGATE / LATER |
| 10 | Manufacturing/service flexible-work routing | 82 | -20 regulatory/licensing ambiguity | **62** | G3 UNKNOWN/FAIL depending structure | REDESIGN BEFORE TEST |
| 11 | Silver-economy non-medical home/community service routing | 82 | -20 vulnerable-person/home trust risk | **62** | G3 CONDITIONAL | LATER / CONSTRAINED |
| 12 | NEV after-sales quote/service coordination | 77 | -15 on-site/safety complexity | **62** | G3 CONDITIONAL; G5 UNKNOWN | LATER |
| 13 | Pet home-care trust orchestration | 81 | -20 home-access/animal-safety risk | **61** | G3 CONDITIONAL | LATER |

### Special case — trade-in fulfilment

`Trade-in pickup/recycling/installation routing` scores strongly on current observable activity but **cannot be a core wedge while G6 depends materially on temporary policy subsidy**. Treat as seasonal/adjacent transaction flow, not the main platform thesis.

## #1 score decomposition — property-anchored backend

```text
pain_severity                         8 / 10
frequency_density                     9 / 10
payment_evidence                     11 / 15
current_solution_weakness             7 / 10
supply_availability                    5 / 5
acquisition_route_feasibility          8 / 8
delivery_controllability               7 / 8
delegatability_orchestration_leverage  9 / 10
time_to_first_cash                     7 / 8
unit_economics_potential               4 / 5
defensibility_learning                 4 / 5
capital_efficiency                      6 / 6
RAW                                    85
bypass-risk penalty                   -10
ADJUSTED                               75
```

Why it leads despite only 75 adjusted:
- Xuzhou has a very dense, identifiable property channel: 2,237 residential communities and 690+ property-service companies;
- local property operators explicitly want to extend value-added/community convenience services;
- resident household service demand recurs without the operator generating every lead from zero;
- the property front desk can be the demand front end while execution stays external;
- service supply is abundant and can be optioned rather than employed;
- low-risk service units can be bounded and accepted;
- the operator can remain behind the scenes as task/quality/settlement architect;
- zero/near-zero fixed capital is realistic.

Sources:
- https://szb.cnxz.com.cn/xzrb/pad/con/202608/10/content_53962.html
- https://m.thepaper.cn/newsDetail_forward_34024461
- https://szb.cnxz.com.cn/dscb/pad/con/202607/16/content_52808.html

## #1 gates

### G0 Actor / role clarity — PASS
- Need actor: resident / household / owner.
- Beneficiary: resident + property relationship.
- Payer: resident for an exact service; alternate property/supplier-share structures remain testable.
- Demand entry: property/community front door.
- Capability provider: independent household-service providers.
- Orchestrator: backend service architecture / routing / acceptance / replacement / settlement.

### G1 Payer clarity — UNKNOWN for our exact structure
People already pay for household services, but we do not yet know whether:
- residents will buy through a property-mediated route at an acceptable price;
- property will actively distribute it;
- provider margin supports property + orchestration take.

`existing category payment != payment to our exact structure`.

### G2 Transactionability — PASS for low-risk wedge
Start only with bounded low-risk services such as:
- deep/general cleaning;
- appliance cleaning;
- move-in/move-out cleaning;
- other non-regulated, fixed-output home-maintenance services.

Avoid gas, structural, safety-critical electrical, medical, childcare or vulnerable-person care in the first wedge.

### G3 Legal / trust / safety — PASS/CONDITIONAL by service class
Low-risk cleaning/household service can be tested with identity/business qualification, service evidence and complaint/replacement rules. Home entry remains a trust requirement, but much lower than medical/elder/pet/home-key models.

### G4 Delegatability — PASS
- property/distribution is a routable channel;
- delivery is provided by vendors;
- QA/complaint handling can be standardized;
- operator is not required to clean/repair/sell door-to-door.

### G5 Orchestration value — UNKNOWN
Largest strategic risk:

> after first introduction, why does the property not directly contract the provider?

The backend must prove recurring value through multi-provider qualification, service catalog, price/SLA, evidence, complaint handling, replacement, cross-community routing and settlement.

If these add little value, kill the model.

### G6 Regenerative circulation — UNKNOWN but structurally strong
Property controls a persistent community demand base, but our exact demand pump is not proven until:
- one property produces more than one resident transaction;
- preferably different service/task events recur without restarting acquisition from zero.

## Why #2 is not merged automatically

Stock-home turnover/repair is a promising **wedge inside or adjacent to #1**, but the ranking keeps it separate to preserve evidence clarity. It may become the first service template if its ticket and orchestration margin are better than generic household services.

## Why engineering machinery did not rank #1

Xuzhou's engineering-machinery money flow is larger and strategically important, but first-entry friction is higher:
- domain expertise;
- safety/liability;
- incumbent dealer/OEM service networks;
- equipment/part compatibility;
- onsite requirements;
- trust cost.

It remains a long-run high-value candidate, not the easiest first proof for a zero-capital orchestrator.

## Why tourism did not rank #1

Demand is large and growing, but:
- events/seasonality affect flow;
- major platforms already own much local discovery;
- public promotion/coupons contaminate merchant WTP;
- repeat at one payer/channel remains less certain than a resident installed-base channel.

## Why flexible work did not rank #1

Supply/demand density is attractive, but employment-service / dispatch / worker-management structures can trigger regulatory obligations. Existing public employment infrastructure also lowers private intermediation value.

## Decision

Cycle 001 selects **Property-Anchored Community Living-Service Orchestration Backend** as the first targeted validation candidate.

This does NOT authorize platform development.

Next objective:

> prove one property/community can act as a recurring Demand Pump while delivery is executed by optioned external providers and the orchestrator creates enough QA/replacement/settlement value to survive bypass.

Only a real transaction and repeat can advance the evidence level.
