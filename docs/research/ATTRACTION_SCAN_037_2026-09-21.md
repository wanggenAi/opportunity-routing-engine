# ATTRACTION_SCAN_037 — classify post-incumbent residual leakage

Date: 2026-09-21  
Status: COMPLETE  
Commercial promotions: **0**  
Retained research formations: **0**  
First external value flow: **NOT_PROVEN**

## Search rule

Scan 037 tested the failure mode left open by Scan 036:

```text
AN INCUMBENT EXISTS
+
MANUAL WORK STILL EXISTS
!=
UNOWNED CONTROL EDGE
```

A formation could proceed only if residual leakage remained after exact-incumbent preflight and the leakage was caused by a structural control-right, data-right or action-edge gap rather than simple non-adoption, implementation debt, poor discipline or participant non-response.

## Results

Six unrelated domains still showed real manual work in 2026. None survived causal classification of that residual.

- **Enterprise AI-agent runtime enforcement:** identity/runtime products now cover agent identity, entitlement governance, runtime authorization and enforcement. Residual leakage is deployment/coverage.
- **Vendor onboarding:** portals and workflow products already cover intake, document collection, approvals and ERP hand-offs. Residual leakage is implementation fragmentation.
- **Supplier Scope 3 data collection:** supplier portals, questionnaires, API/ERP ingestion and quality scoring exist. Residual leakage is participation/source-data quality.
- **Creator multi-brand payout reconciliation:** creator operations products already track milestones, invoices, balances and payout status. Residual leakage is payment-rail fragmentation/adoption.
- **Healthcare prior authorization:** multiple platforms automate lookup, evidence assembly, submission, follow-up and denial workflow. The hard remainder is payer heterogeneity and clinical judgment.
- **Construction change orders:** paid products already capture field evidence, route approvals, sync costs and preserve audit trails. Residual leakage is field adoption/discipline.

## Main learning

```text
RESIDUAL LEAKAGE
→ classify cause
    ├─ non-adoption / implementation / discipline → NOT WHITE SPACE
    ├─ participant non-response / poor source data → NOT CONTROL EDGE
    └─ structural control-right / data-right / cross-system action gap → eligible for deep research
```

This prevents the engine from mistaking low software penetration for a new business.

## Scan 038

Remain broad and mechanism-neutral. Keep payer/workaround and digital/delegatable prefilters, but only spend deep-research effort where post-incumbent leakage is tied to a structural control-right, data-right or cross-system action gap.
