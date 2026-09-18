# Connection Pressure Scan 024 — Base-load Commitment and Compatibility-weighted Density

Observed: 2026-09-18

## Why this scan exists

Scan 023 established that a real resource and a real need can still fail to connect because the exchange is outside its economic service radius or below a useful density threshold.

This scan makes the density rule stricter:

> many potentially interested actors are not the same thing as enough recurring, compatible and economically committed work to support a shared node.

This is the system-scale equivalent of Issue #143's field rule: interest is not commitment.

It refines DENSITY_THRESHOLD_BEFORE_ORCHESTRATION and FLEXIBILITY_CALLABILITY_GATE. It does not create a new ontology and it does not promote a generic shared-service platform.

## Evidence

### Xuzhou customized buses

Xuzhou operates more than 140 customized routes and serves more than 85 enterprises/institutions. Enterprise routes are built from employee residential distribution, commuting time and route preferences. Public reporting describes stable enterprise demand, strong willingness to pay and more than two million annual enterprise commuting passenger trips.

Source:
- https://www.zgjssw.gov.cn/shixianchuanzhen/xuzhou/202602/t20260210_8556821.shtml

The relevant density is not employee count. It is repeated paid trips that share origin/destination/time structure.

### Guannan shared drone operations

Guannan integrates actual flight tasks from 11 townships and 19 departments. Units buy flight service on demand instead of each buying aircraft, training pilots and maintaining fleets. Public reporting says single-flight cost falls by more than 60%.

Source:
- https://www.jiangsu.gov.cn/art/2026/7/20/art_33718_11805793.html

The resource becomes callable because real schedulable tasks are pooled. Generic enthusiasm for low-altitude economy would not finance the node.

### Binhai shared manufacturing

Binhai Green-Island intelligent manufacturing service center centralizes expensive/high-pollution downstream processes. Its spraying center processes more than six million parts each year.

Source:
- https://jsnews.jschina.com.cn/yc/a/202605/t20260520_s6a0d44a6e4b0fd0345232e69.shtml

This is measurable recurring throughput capable of amortizing fixed equipment, governance and environmental-control cost.

### Xuzhou shared welding

XCMG has co-built a shared welding center with more than 30 local SMEs around a specific intelligent welding capability.

Source:
- https://www.zgjssw.gov.cn/shixianchuanzhen/xuzhou/202510/t20251021_8530725.shtml

Thirty companies are relevant only because sufficiently similar welding tasks can pass through a common process and acceptance interface.

## Refinement

### BASELOAD_COMMITMENT_GATE

Before treating a shared node as naturally forming, ask:

1. What work already happens repeatedly?
2. Who actually pays/orders/schedules it?
3. What fixed capability or coordination cost must this load cover?
4. What minimum frequency or throughput keeps the node alive?
5. Is there an anchor buyer, route, contract or repeated workflow that covers a meaningful fraction of the fixed floor?
6. Would the node still make sense if speculative long-tail demand disappeared?

### COMPATIBILITY_WEIGHTED_DENSITY

Raw demand cannot simply be summed.

A route requires compatible origin/destination/time.

A laboratory requires compatible testing classes and standards.

A manufacturing center requires compatible process specifications and acceptable changeover cost.

A specialist pool requires tasks that can actually be represented and routed through the same capability.

Therefore:

ECONOMIC_DENSITY = recurring real demand × compatibility × commitment × reachable service window

This is a heuristic, not a numerical scoring formula.

## Hard boundaries

INTERESTED_ACTORS != BASELOAD

POTENTIAL_VOLUME != COMMITTED_VOLUME

RAW_DENSITY != COMPATIBLE_DENSITY

ACTOR_COUNT != ROUTABLE_TASK_COUNT

ONE_OFF_TRANSACTION != STABLE_NODE

COMMITTED_VOLUME != PROFITABILITY

ANCHOR_CUSTOMER != REPEATABLE_MARKET

## Portfolio impact

No Formation is promoted.

This scan strengthens the anti-hallucination discipline around shared resources. Future candidates should not be promoted because many actors appear to have a similar problem. The system must first find recurring compatible work that is already being paid for, scheduled, routed, queued or repeatedly worked around.

## Field truth

Two direct employer capability-proof probes remain SENT.

Qualified human responses remain 0.

No additional outreach is added to increase sample count.

FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN.
