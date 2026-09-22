# ATTRACTION_SCAN_073 — Buyer-side non-role repeat-spend pass

**Date:** 2026-09-22  
**Status:** COMPLETE  
**Commercial promotions:** 0  
**Retained research formations:** 0  
**FIRST_EXTERNAL_VALUE_FLOW:** NOT_PROVEN

## Boundary

This scan changes the payer evidence source after two broad role/contract-budget passes.

Primary payer evidence must come from the buyer side and must be non-role: repeat purchase, procurement, award, invoice, renewal or recurring service spend. A job posting cannot be the sole payer signal. A seller-defined productized-service page cannot be the primary signal.

The scan remains formation-diverse and mechanism-neutral. It does not inherit routing, atomicity, provider abstraction, failover, software shape or any other mechanism requirement from Scans 060–072.

## Result

Six current buyer-side non-role spend signals were pressure-tested and all six failed closed:

| Formation | Buyer-side non-role spend signal | Why it closes |
|---|---|---|
| Municipal short-term-rental compliance | 2026 multi-year RFP with annual subscription/support pricing; buyer already uses Host Compliance | Granicus Host Compliance already owns listing identification, permit/tax, monitoring, outreach and complaint workflows; true enforcement stays municipal |
| Workers' comp medical bill review | 2026 procurement with three-year initial term plus renewal options | Routine fee-schedule/coding review is a mature automated category; high-dollar/inappropriate-care residual requires licensed clinical judgment |
| Parking citation processing | 2026 nine-month Turbo Data Systems extension capped at $56,250 | The named incumbent already owns citation processing, payment and municipal workflow; adjudication/legal authority is government-controlled |
| Municipal hotel/sales-tax administration | September 2026 MuniServices renewal | Tax administration/payment/compliance audit is already a mature vendor category; residual audit value is jurisdiction-specific statutory/examiner work |
| FOIA/public-records workflow | 2026 federal eFOIAXpress renewal plus separate county JustFOIA annual-subscription procurement | Intake, tracking, review, redaction, approval, payment and release are productized; final exemption/disclosure decisions remain accountable human/legal work |
| Managed detection and response | 2026 Arctic Wolf annual renewal for $129,801.10; cumulative contract value $364,753.78 since 2024 | 24x7 monitor/detect/triage/respond is the exact mature MDR category; residual value includes human security context, escalation and accountability |

## Cross-scan conclusion

Buyer-side procurement and renewal records are materially stronger **money-motion evidence** than job postings because the buyer has actually selected or renewed an external outcome.

But the first pass also exposes a different selection bias:

```text
CURRENT BUYER PROCUREMENT / RENEWAL
→ REAL RECURRING MONEY MOTION
→ NAMED CATEGORY / NAMED INCUMBENT OFTEN VISIBLE IN THE SAME RECORD
→ STANDARD CONTROL LOOP ALREADY PRODUCTIZED
→ RESIDUAL VALUE OFTEN AUTHORITY / JUDGMENT / ACCOUNTABILITY
```

That does not justify abandoning buyer-side non-role spend after one pass. It justifies one independent second pass before changing evidence source or deriving any mechanism boundary.

## Next evidence boundary

Scan 074 should run a second formation-diverse sample of current buyer-side non-role repeat purchase / procurement / award / invoice / renewal evidence.

It must:
- exclude Scan 060–073 formations and primary signal patterns from seeding;
- not use a job posting as sole payer evidence;
- not use seller-defined productized service as the primary signal;
- inherit no preferred mechanism;
- keep exact-incumbent, founder-independence, data/action-rights and normalized-margin preflight fail-closed.

## Drift Audit

- The scan did not continue the Scan 071/072 role-budget lens; the payer source changed as required.
- Procurement categories were treated as downstream economic evidence, not as the ontology of what the business must be.
- Incumbent presence was not an automatic kill; each case was checked for whether the incumbent already resolves the same repeatable control loop and what residual remains.
- No formation was retained merely because its contract value is large.
- No new mechanism rule is derived from one non-role-spend pass.

## Parallel validation

ATTRACTION_SCAN_015-F1 remains independent and unchanged. Written provider rights evidence plus founder-free inbound proof are still decisive.

## Next

Advance to `ATTRACTION_SCAN_074` only if repository CI and live Jev authorize continuation.
