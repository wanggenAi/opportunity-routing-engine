# ATTRACTION_SCAN_022-F1 — cheap falsification

Date: 2026-09-21  
Formation: `BATTERY_EXCISE_TAX_EVIDENCE_RECONCILER`  
Verdict: **DEMOTED_ERP_ABSORPTION_AND_NONCOMPOUNDING_COMPLIANCE_LAYER**  
Commercial candidate: **NO**  
Retain for active validation: **NO**  
First external value flow: **NOT_PROVEN**

## What was tested

Scan 022 retained F1 only because the September 2026 battery-consumption-tax change creates a direct cash-linked
reconciliation state:

```text
tax-paid battery inputs
× actual production consumption
× product identity
× test/exemption evidence
→ deductible tax / exemption evidence
→ statutory ledger + declaration inputs
```

This round tested whether that state supports a distinct, founder-independent software business rather than a
temporary compliance feature.

## Finding 1 — the underlying obligation is real

The policy itself is not the problem.

From 2026-09-01 specified battery categories are taxed at 2%, with the rate rising to 4% from 2027-09-01.
Specified sodium-ion, solid-state, fuel-cell and several photovoltaic battery categories receive temporary
exemptions subject to national-standard conditions.

Official policy:
- https://fgk.chinatax.gov.cn/zcfgk/c102416/c5251171/content.html

The tax administration rule requires a `电池税款抵扣台账` for tax-paid batteries used in continued production of
taxable battery products. Exemption support requires qualified test reports and product lists aligned to
accounting and invoice names/specifications/models.

Official administration rule:
- https://fgk.chinatax.gov.cn/zcfgk/c100012/c5251620/content.html

So the cash and evidence state is real.

## Finding 2 — uncomplicated reconciliation is too deterministic to own

The official interpretation publishes worked examples. For a simple purchase case, deductible tax is the
invoice amount multiplied by the tax rate and the actual production-use ratio; comparable rules exist for
processing and imports.

Official interpretation:
- https://fgk.chinatax.gov.cn/zcfgk/c100015/c5251623/content.html

That matters commercially.

Once ordinary invoice/tax-payment and production-use data have been exported, the bounded ledger calculation
does not require a proprietary decision asset. A spreadsheet, generic agent or existing finance system can
reproduce the arithmetic and exception checks.

This does **not** mean all battery-tax work is trivial. It means the simple part does not create enough
operator control.

## Finding 3 — incumbent ERP/tax systems already own the natural data position

The stronger part of F1 would be automatic joining of invoices, tax documents, production consumption,
accounting/SKU identity and declaration data.

But that is precisely where incumbent ERP/tax systems have a structural advantage.

Kingdee's current enterprise tax stack publicly describes:
- integration with internal business and finance systems;
- invoice intake and deduction workflows;
- automatic tax calculation and declaration;
- tax archives / traceability;
- policy-rule updates and risk controls.

Sources:
- https://www.kingdee.com/products/eascloud_taxation.html
- https://www.kingdee.com/resources/articles/1493612047122906049

The point is not that a public page proves Kingdee already has the exact new battery ledger. It does not.
The decisive issue is that the proposed standalone entrant does not own the source-of-record position. A new
battery rule is a natural feature expansion for systems that already sit on production, invoice and tax data.

```text
EXACT FEATURE NOT YET PUBLICLY FOUND
!=
UNOWNED CONTROL SURFACE
```

## Finding 4 — the difficult remainder reintroduces tax judgment

The State Taxation Administration's current Q&A covers questions such as:
- whether a battery cluster or downstream system is taxable;
- mixed sodium-ion/lithium configurations;
- self-use and battery-swap leasing;
- export/ domestic allocation;
- timing of tax obligations.

Source:
- https://www.chinatax.gov.cn/chinatax/c102414/c5252006/content.html

Those are not merely missing spreadsheet columns. They are tax-scope and factual-classification questions.

F1 must fail closed on ambiguous classification if it is to remain a non-consulting software product.
Professional advisers are already interpreting the policy at the supply-chain, pricing and compliance level:
- https://finance.sina.com.cn/wm/2026-07-24/doc-iniixfyc4889686.shtml

That creates a squeeze:

```text
SIMPLE / DETERMINISTIC
→ ERP / TAX SOFTWARE / EXCEL / GENERIC AGENT

COMPLEX / AMBIGUOUS
→ TAX PROFESSIONAL / INTERNAL TAX TEAM
```

The proposed standalone middle layer does not yet own a distinct value surface between them.

## Finding 5 — the supposed moat does not compound naturally

F1's original operator-asset hypothesis was:
- reusable import adapters;
- versioned reconciliation rules;
- exception taxonomy;
- non-identifying reconciliation patterns.

The falsification result is negative.

The rules are public. Invoice, production-consumption, SKU and test-report data are customer-owned and
commercially sensitive. Each enterprise's ERP/MES exports and master-data conventions can differ. If the
operator must repeatedly map customer systems, the business drifts toward implementation work.

More importantly, a completed reconciliation does not naturally return a reusable cross-customer outcome
signal or execution right that improves the next customer's decision. The workflow can become a useful
feature without becoming a compounding operator asset.

## Payer result

Exact standalone payer willingness remains **NOT PROVEN**.

Current evidence proves spending on:
- enterprise tax/ERP systems;
- internal tax functions;
- professional tax advisory.

It does not prove a separate paid market for a narrow battery-tax reconciler.

Because incumbent absorption, generic/spreadsheet substitutability and non-compounding operator control are
already hard negative evidence, further founder-led payer outreach is not justified for this formation.

## Verdict

`ATTRACTION_SCAN_022-F1` is demoted.

The durable lesson is:

```text
MANDATORY + CASH-LINKED + NEW
!=
STANDALONE ATTRACTIVE BUSINESS

PUBLIC DETERMINISTIC RULE
+ CUSTOMER-OWNED DATA
+ INCUMBENT SOURCE-OF-RECORD SYSTEM
→ OFTEN A FEATURE, NOT AN OPERATOR-CONTROLLED FORMATION
```

Do not build an MVP. Do not start battery-industry outreach. Do not let this vertical seed Scan 023.

## Next action

Remove F1 from active validation and resume formation-diverse Scan 023 from broad current reality, while
Scan 015-F1 and Scan 016-F1 continue only on their existing independent validation tracks.
