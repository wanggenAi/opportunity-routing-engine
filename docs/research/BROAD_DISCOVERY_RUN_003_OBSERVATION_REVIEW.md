# Broad Discovery Run 003 — Observation Review

Status: `REVIEWED / NON-CANONICAL / NOT BUSINESS PROMOTION`

Date: 2026-09-14

## Purpose

Run 003 deliberately widened the China-primary sensor surface beyond prior eldercare and idle-asset structures. This review converts only bounded, manually reviewed source captures into the Observation Fabric and then asks whether exact reviewed claims form coherent candidate concepts.

The review is not a ranking, taxonomy promotion, opportunity recommendation, payer claim or route test.

## Pipeline

```text
30 governed research-evidence records
→ 18 bounded reviewed ObservationEnvelopes
→ 5 explicit reviewed semantic alignments
→ 2 PROMOTION_REVIEW_READY
→ 3 CANDIDATE
→ 0 exact source-native ObservedPatterns
```

All semantic alignments preserve exact claim lineage. Different source-native concepts are not silently rewritten into one canonical node.

## Promotion-review-ready concepts

### `SKILL_TO_WORK_MATCHING_INFRASTRUCTURE`

Four reviewed observations across national, Jiangsu and Xuzhou levels describe linked behavior around demand forecasting, shortage-skill training, employment-linked training incentives and more precise placement/matching.

This supports only an ontology-governance question: whether this recurring behavior deserves a versioned concept in the emergent taxonomy.

It does **not** prove:
- a private project-work marketplace;
- employer willingness to pay an orchestrator;
- spare/callable professional capacity;
- good gig-work economics;
- causal effectiveness of training;
- payer, settlement or route testability.

### `PLATFORM_TRUST_AND_GOVERNANCE_INFRASTRUCTURE`

Four independent reviewed observations span platform/merchant research, national live-commerce rules, Jiangsu after-sales governance and a Xuzhou local trust platform. They coherently describe identity/qualification checks, consumer protection, after-sales/dispute handling and merchant/platform service infrastructure.

This does **not** prove:
- merchant pain is monetizable;
- merchants want another intermediary;
- governance improves margins;
- local public-platform mechanics transfer to commercial platforms;
- a new payer or route exists.

## Candidate concepts that remain below the gate

### `CIRCULAR_RECOMMERCE_INFRASTRUCTURE`
Three positive reviewed observations are coherent but below the four-observation threshold. A separate Xuzhou record shows material subsidy leverage and is retained as counterevidence rather than counted as positive support.

```text
SUBSIDIZED FLOW != ORGANIC RECOMMERCE DEMAND
```

### `PET_SERVICE_ECOSYSTEM_FORMALIZATION`
National paid-service use, Jiangsu formalization policy and Xuzhou ecosystem evidence are directionally coherent but still total only three reviewed observations. The national whitepaper also reports medical share falling relative to 2024.

```text
PET MARKET GROWTH != ALL PET SERVICE SUBCATEGORY GROWTH
```

### `LOGISTICS_CAPACITY_ORCHESTRATION`
Three observations cover national third-party logistics leasing, digital capacity-demand matching and a Xuzhou shared cloud-warehouse case. They remain below the gate and preserve a decisive boundary:

```text
MARKET VACANCY != CALLABLE SPARE CAPACITY
```

Q2 absorption recovery is retained alongside vacancy; the system must not freeze a temporary slack state into a permanent idle-capacity narrative.

## Truth boundaries

```text
SEARCH CAPTURE != OBSERVATION UNTIL REVIEWED
REVIEWED ALIGNMENT != TAXONOMY PROMOTION
PROMOTION_REVIEW_READY != TAXONOMY PROMOTED
PROMOTION_REVIEW_READY != OBSERVED PATTERN
SUBSIDIZED FLOW != ORGANIC DEMAND
TRAINING/MATCHING ACTION != PAID TASK MARKET
PLATFORM GOVERNANCE != MERCHANT WILLINGNESS TO PAY
MARKET VACANCY != CALLABLE CAPACITY
CANDIDATE != BUSINESS
UNKNOWN != PASS
```

## Engineering change

The former Run-002-specific observation-review script has been generalized to:

```text
scripts/build_broad_discovery_observation_review.py
```

Run-specific evidence, reviewed observations and alignment hypotheses are now data. The core review builder no longer contains eldercare/procurement-specific truth language. The old Run 002 entry point remains a compatibility wrapper.

This preserves the architectural rule:

> code encodes how to understand and govern evidence; today's observed industry structures remain data, not permanent ontology or implementation branches.
