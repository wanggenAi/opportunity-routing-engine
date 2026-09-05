# EXPERIMENT-001 — Buyer Discovery Benchmark

Status: PLANNED

## Objective

Determine whether an AI-assisted multi-source workflow can produce materially more **qualified, reachable overseas buyers** per unit of effort than a basic single-channel/manual workflow for one narrow Xuzhou product category.

## Test product

Initial target: perfume/cosmetic glass bottles, especially 50 ml / 100 ml products.

The test product may be narrowed further before execution if necessary, but both benchmark arms must use the same product definition.

## Core question

Can the AI-assisted workflow improve qualified-buyer yield enough to justify building automation and later approaching factories?

## Arm A — Baseline

Single-channel/manual discovery using a conventional sourcing/search workflow.

Target: 50 raw candidates.

Record:

- elapsed human minutes;
- raw candidates found;
- real companies;
- recent/relevant buying signals;
- product-fit candidates;
- candidates with valid business contact routes;
- final A-grade buyers.

## Arm B — AI multi-source

Use multiple allowed sources and cross-source research, such as:

- current RFQs / buying requests;
- import/shipment history where legitimately available;
- company websites;
- search engines;
- public buyer/company directories;
- public professional/business profiles;
- saved searches / official APIs where available.

Target: 50 raw candidates.

Record the same metrics as Arm A.

## Qualification rubric

Suggested 100-point model:

| Dimension | Weight |
|---|---:|
| Freshness / recency | 15 |
| Product-demand specificity | 15 |
| Purchase scale / frequency evidence | 10 |
| Buyer credibility | 20 |
| Buyer contactability | 20 |
| Xuzhou supplier fit | 15 |
| Commercial attractiveness | 5 |

### Grade

- `A`: >= 80 and contactability gate passes
- `B`: 65–79 or missing one non-critical verification item
- `C`: < 65
- `REJECT`: fraudulent, irrelevant, inaccessible, prohibited, or materially contradictory

## Contactability hard gate

At least one legitimate, actionable business channel must exist, for example:

- official platform quotation/message channel;
- public corporate email;
- public purchasing/business email;
- public business phone;
- public WhatsApp Business contact;
- public professional/business messaging route;
- company contact form that is usable for B2B enquiries.

A personal/private channel obtained through improper means does not count.

## Success criteria

This first benchmark is directional, not a claim of statistical significance.

Continue to Experiment 002 if the AI-assisted arm shows a meaningful advantage in at least two of these:

1. A-grade buyers per hour;
2. valid-contact buyers per hour;
3. verified-buying-signal buyers per hour;
4. lower manual review time per qualified buyer.

A provisional strong signal is >= 2x improvement in A-grade buyers per human hour.

## Fail / rethink conditions

- <= 20% improvement after equivalent effort;
- most qualified candidates depend on inaccessible/prohibited data collection;
- contactability collapses after verification;
- source duplication creates apparent volume without unique buyers;
- product-supplier fit cannot be verified well enough to support outreach.

## Outputs

- `data/experiments/experiment_001_baseline.csv`
- `data/experiments/experiment_001_ai.csv`
- `docs/results/EXPERIMENT_001_RESULT.md`

Do not create result files until real observations exist.

## Next experiment if passed

Experiment 002: contactability audit and written-outreach pilot on a small, verified buyer cohort, with supplier authorization before any product-specific representation or binding quotation.
