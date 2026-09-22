# ATTRACTION_SCAN_123 — Independent strict current-economic admission repeat

Date: 2026-09-23  
Epoch: `ATTRACTION_FIELD_V1`  
Primary domain: China

## Purpose

Consume the verified Scan 122 continuation and independently repeat the strict primary-admission rule on fresh current-report evidence:

```text
CURRENT SAME-ENTITY REPORT
+ INTRINSICALLY LOW CURRENT / LATEST DIRECTLY DISCLOSED FTE
+ POSITIVE EXTERNAL REVENUE
+ POSITIVE NET PROFIT
+ UNAMBIGUOUS POSITIVE CONSOLIDATED OCF
=> PRIMARY FORMATION ADMISSION
```

Partial matches are excluded observations. Scan 123 deliberately includes fresh non-manufacturing routes and does not relax any gate.

## Result

**Zero primary formations were admitted.**

This is an allowed outcome, not a missing-data substitute. Six fresh low-headcount current-report packets were screened and each failed at least one current economic leg before control-history deepening:

- **Mokylin / 墨麟股份** — 10 FTE; revenue RMB647,807.93; net loss RMB2,573,353.13; consolidated OCF negative RMB2,635,782.97. Fresh non-manufacturing game-development/operation route; excluded on profit and OCF.
- **Qianxiang Media / 千想传媒** — 19 FTE; revenue RMB4,069,967.53; net profit RMB355,826.15; consolidated OCF negative RMB2,893,516.50. Fresh media/advertising route; excluded on OCF.
- **Zhongshi Huaze / 中食花泽** — 16 FTE; revenue RMB883,914.85; net loss RMB29,262.59; OCF positive RMB176,848.62. Fresh health-product sales route; excluded on profit.
- **Zhengyang / 正扬股份** — 12 FTE; revenue RMB22,018.35; attributable net loss RMB1,382,283.73; consolidated OCF negative RMB1,365,176.18. Excluded on profit and OCF.
- **ST Yizhongshi / ST义众实** — 13 FTE; revenue RMB13,767,591.13; consolidated net loss RMB1,383,231.34; consolidated OCF negative RMB1,435,283.75. Excluded on profit and OCF.
- **175 / 壹柒伍** — 20 FTE; revenue RMB2,245,828.69; net loss RMB523,092.90; consolidated OCF negative RMB1,520,439.54. Second fresh non-manufacturing game route; excluded on profit and OCF.

No control-history research was spent on these packets because none earned primary admission.

## Interpretation

Scan 123 does **not** replicate the Scan 122 control-reproducibility bottleneck because there is no admitted survivor on which to run that test. Therefore completed fresh-operator control must **not** be promoted into the primary entry gate yet.

The repeat instead confirms a different operational fact: fresh low-FTE non-manufacturing packets are discoverable, but current profit and cash conversion remain strong early filters. Scan 124 should preserve the same constitution while prioritizing positive-profit and positive-OCF retrieval signals for search efficiency.

No product, vertical or mechanism is derived from this zero-admission result.

## Jev control-plane correction

The existing Jev runner treated an empty `examined_formations` list as execution failure and forced human review. That would create an incentive to fabricate a primary formation merely to satisfy validation.

Scan 123 therefore adds an explicit fail-closed distinction:

- `status=COMPLETE`
- `zero_primary_admissions=true`
- `examined_formations=[]`

is an authoritative zero-admission research result and may advance with zero Jev entity calls;

an unmarked or malformed empty input remains a failure and still requires human review.

Jev remains shadow-only, has no commercial-promotion authority and cannot mutate authoritative commercial truth.

## Commercial truth

- Active commercial candidates: 0
- Retained research formations: 0
- Primary formations admitted in Scan 123: 0
- FIRST_EXTERNAL_VALUE_FLOW: `NOT_PROVEN`
- Parallel validation `ATTRACTION_SCAN_015-F1`: unchanged; still waiting on real written provider rights evidence and organic founder-free inbound proof.

## Sources

See `data/research_runs/attraction_scan_123.json` for the persisted source URL set and machine-readable early exclusions.
