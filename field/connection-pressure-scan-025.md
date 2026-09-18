# Connection Pressure Scan 025 — Compatibility Conversion Cost

Observed: 2026-09-18

## Question

Scan 024 established that real recurring base-load matters more than raw actor count.

This scan asks:

> even when recurring tasks exist, how much work is required to make those tasks truly share one capability and one acceptance interface?

The answer is compatibility conversion cost: setup, tooling, cleaning, calibration, protocol translation, qualification, standards translation, data mapping, retraining and other reconfiguration burden.

This refines STANDARDIZATION_BEFORE_ROUTING and COMPATIBILITY_WEIGHTED_DENSITY. It is not a new ontology.

## Evidence

### Xuzhou: minute-level multi-variety changeover

Dongxing Xuzhou factory reports minute-level rapid changeover for multi-variety, small-batch production on automated lines.

Source:
- https://szb.cnxz.com.cn/xzrb/pad/con/202603/11/content_46961.html

The relevant lesson is not “flexible manufacturing is an opportunity.” It is that heterogeneous small orders become economically aggregatable only after setup/changeover cost is pushed down.

### Jiangsu: modular process / interface standardization

A Jiangsu intelligent-factory case uses modular workstations, common process modules and rapid reconfiguration. A reported implementation reduced changeover to about three minutes and identified inconsistent device communication protocols as a real integration obstacle.

Source:
- https://www.wimc.org.cn/news_show.aspx?id=1053

Compatibility therefore has both a physical setup layer and an information/interface layer.

### Testing: spare lab != compatible lab

In 2026, Jiangsu Medical Device Testing Institute underwent CNAS/CMA review for 278 additional testing parameters, with total capability expected to reach about 2,491 parameters.

Source:
- https://da.jiangsu.gov.cn/art/2026/8/27/art_84602_11821530.html

A laboratory can have equipment and time yet still be unable to accept a task because the parameter, method, range or accredited scope does not match.

### Cross-market standards translation

A Changzhou testing organization covers Chinese, European, US and Japanese vehicle/charging standards and offers a one-test/multi-market route. Public reporting says this can avoid repeated overseas certification and save more than RMB 2 million per case.

Source:
- https://www.jiangsu.gov.cn/art/2026/9/15/art_33718_11829839.html

The product did not become more real; the acceptance interfaces became interoperable enough to reuse evidence across markets.

### Xuzhou supply-chain variety

A Xuzhou engineering-machinery supplier expanded from roughly a dozen standard cylinder types to more than 200 variants and modified production lines for rapid multi-variety small-batch switching.

Source:
- https://m.ourjiangsu.com/news/2026/5/20/1506694906969686016.html

Downstream variety propagates conversion cost upstream.

## Refinement

### COMPATIBILITY_CONVERSION_COST

Before aggregating apparently similar demand, ask:

1. What must be reconfigured between task variants?
2. How long does that conversion take?
3. What tooling/material/qualification/cleaning/calibration/translation cost occurs?
4. Is the conversion one-time per interface or repeated per job?
5. Does aggregation remain economic after conversion cost?
6. Does the output remain acceptable to the receiver?

### COMMON EXECUTION AND ACCEPTANCE COORDINATES

Tasks are meaningfully compatible only when they can be:

- described in a common specification space;
- executed by the same capability without excessive reconfiguration;
- accepted through the same or reliably translated evidence/quality interface.

## Hard boundaries

SAME_CATEGORY != SAME_ROUTABILITY

FREE_CAPACITY != COMPATIBLE_CAPACITY

ACTOR_COUNT != COMPATIBLE_TASK_DENSITY

TECHNICAL_CAPABILITY != LEGAL_SCOPE

STANDARD_EXISTS != CROSS_STANDARD_ACCEPTANCE

AGGREGATION != POSITIVE_UNIT_ECONOMICS_AFTER_CHANGEOVER

## Portfolio impact

No Formation is promoted.

The system should now discount apparent density when every job requires expensive reconfiguration. A large heterogeneous market can be less callable than a small highly standardized recurring task pool.

## Field truth

Two employer capability-proof probes remain SENT.

Qualified human replies remain 0.

FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN.
