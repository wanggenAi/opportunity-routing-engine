# ATTRACTION_SCAN_004-F1 — Discoverability Reassessment

Date: 2026-09-20  
Formation: `ATTRACTION_SCAN_004-F1 — LEGACY EQUIPMENT HARVEST PARTS GRAPH / 工业旧设备器官库`

## Verdict

`DEMOTED_FROM_HIGH_ATTRACTION / INFORMATION_CAPTURE_BOTTLENECK`

Commercial candidate: **NO**  
Retained research formation: **NO**  
Next action: **RETURN TO CLEAN-SLATE ATTRACTION SEARCH**

## Why the prior attraction judgment was wrong

The formation had a real state-dependent value jump:

```text
retiring machine part
→ low / hidden value

same compatible part during another factory's outage
→ potentially high recovery value
```

But the prior beacon treated that value jump as more important than the operator's
ability to repeatedly **observe and address the moving units**.

That was incorrect.

The actual route requires the operator to know:
- which factory currently needs which exact part;
- which retiring / idle machine contains that part;
- whether the seller will dismantle it;
- whether the exact revision / interface / firmware / condition is compatible;
- whether the part is still present and usable;
- whether the match can be verified quickly enough to matter.

Those facts are not naturally concentrated in one public, structured, continuously
searchable surface.

The formation therefore depends on building the information market before routing the
value market.

That is not a narrow bridge.

## New governing distinction

```text
LARGE VALUE GAP
!=
HIGH-ATTRACTION OPPORTUNITY
```

A current high-attraction route must also satisfy:

```text
A-SIDE DISCOVERABILITY
+
B-SIDE DISCOVERABILITY
+
MATCH RESOLVABILITY
```

Meaning:

### A-side discoverability

Can the operator repeatedly discover the relevant supply/resource units from:
- public listings;
- platform feeds;
- searchable databases;
- APIs;
- structured digital exhaust;
- permissioned partner data;
- other scalable observable traces?

If every unit requires phone calls, relationships, site visits, private groups or
manual inventory archaeology, current attraction is low.

### B-side discoverability

Can the operator repeatedly discover demand/state-change events while the decision
window is still open?

If demand becomes visible only after private outreach or inside closed maintenance
networks, current attraction is low.

### Match resolvability

Once A and B are visible, can compatibility be determined from accessible evidence?

If each match requires bespoke engineering interpretation, physical inspection or
founder-specific expertise before the route can even be identified, current attraction
is low.

## Reassessment of F1

Previous profile incorrectly classified F1 as a high-attraction beacon.

Corrected capture-feasibility view:

```text
A-side voluntary motion        = strong
B-side voluntary motion        = strong
state-dependent value jump     = strong
decision window                = strong

BUT

A-side discoverability         = weak
B-side discoverability         = weak / fragmented
match resolvability            = weak / expert-dependent
```

Hard-floor result:

`LOW_ATTRACTION`

The direct China donor-reuse artifact remains true and useful as research evidence.
It does not rescue the formation.

## Why "just search Taobao / 1688 / second-hand platforms" is not enough

A high-attraction route cannot depend on a chain such as:

```text
search platform A
→ search platform B
→ ask dealer
→ ask factory
→ inspect donor machine
→ infer part identity
→ ask engineer about compatibility
→ negotiate dismantling
→ repeat from zero next time
```

That is recurring search labor.

Even if software can automate some crawling, the underlying information is often:
- absent;
- stale;
- unstructured;
- hidden inside whole-machine listings;
- private to factories;
- not indexed by exact component identity;
- insufficient to establish compatibility.

```text
SCRAPING HARDER != DISCOVERABILITY
MORE SEARCH QUERIES != ADDRESSABLE MARKET
FOUNDER HUNTING != ROUTING CONTROL
```

## New attraction search preference

Future clean-slate scans should prefer realities where the value-producing units are
already leaving dense digital traces.

Examples of desirable source topology:
- public transaction/order/event streams;
- standardized listings with exact identities;
- repeated platform postings;
- open registries;
- machine-readable government data;
- API-accessible inventories;
- public price/capacity/status feeds;
- large communities where both sides self-publish structured intent;
- existing software exhaust from an already-running workflow.

The attractive opportunity should be closer to:

```text
THE WORLD ALREADY EMITS THE SIGNAL
→ WE NOTICE A NON-OBVIOUS CONNECTION
→ A SMALL ROUTING LAYER UNLOCKS VALUE
```

not:

```text
FIRST BUILD A SENSOR NETWORK
→ THEN BUILD A MARKET GRAPH
→ THEN MAYBE DISCOVER A TRANSACTION
```

## Final state

```text
ATTRACTION_SCAN_004-F1 = DEMOTED
HIGH_ATTRACTION_BEACONS = 0
RETAINED_RESEARCH_FORMATIONS = 0
ACTIVE_COMMERCIAL_CANDIDATES = 0
FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN
NEXT = FRESH CLEAN-SLATE SEARCH WITH DISCOVERABILITY HARD GATE
```
