# EXPERIMENT-001 — Buyer Discovery Benchmark

Status: `DORMANT / SECONDARY LEGACY VERTICAL`

Last status review: 2026-09-10

## Role in the repository

This experiment is preserved as a narrow historical vertical benchmark. It is **not** the identity of the Opportunity Routing Engine and is not part of the current first-priority Xuzhou field sequence.

It may be resumed only if new evidence makes overseas-buyer discovery more valuable than the current actor-first payer tests.

## Objective

Determine whether an AI-assisted multi-source workflow can produce materially more **qualified, reachable overseas buyers** per unit of effort than a basic single-channel/manual workflow for one narrow Xuzhou product category.

## Test product

Initial target: perfume/cosmetic glass bottles, especially 50 ml / 100 ml products.

The test product may be narrowed further before execution if necessary, but both benchmark arms must use the same product definition.

## Core question

Can the AI-assisted workflow improve qualified-buyer yield enough to justify building vertical-specific discovery automation and later approaching authorized factories?

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

This historical vertical rubric is retained for within-experiment buyer qualification. It does not replace the repository-wide `docs/OPPORTUNITY_SCORECARD.md`.

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
- `A`: >=80 and contactability gate passes
- `B`: 65–79 or missing one non-critical verification item
- `C`: <65
- `REJECT`: fraudulent, irrelevant, inaccessible, prohibited, or materially contradictory

## Contactability hard gate

At least one legitimate, actionable business channel must exist, for example:
- official platform quotation/message channel;
- public corporate email;
- public purchasing/business email;
- public business phone;
- public WhatsApp Business contact;
- public professional/business messaging route;
- company contact form usable for B2B enquiries.

A personal/private channel obtained through improper means does not count.

## Success criteria if resumed

This benchmark is directional, not a claim of statistical significance.

A provisional strong signal is >=2x improvement in A-grade buyers per human hour, with contactability and supplier fit still passing after verification.

## Fail / rethink conditions

- <=20% improvement after equivalent effort;
- most qualified candidates depend on inaccessible/prohibited data collection;
- contactability collapses after verification;
- source duplication creates apparent volume without unique buyers;
- product-supplier fit cannot be verified well enough to support outreach.

## Outputs if resumed

- `data/experiments/experiment_001_baseline.csv`
- `data/experiments/experiment_001_ai.csv`
- `docs/results/EXPERIMENT_001_RESULT.md`

Do not create result files until real observations exist.

## Numbering correction

The original document said a successful result should "continue to Experiment 002" as a buyer-contactability/outreach experiment.

That statement is obsolete. `EXP-002` is now the canonical **Xuzhou Actor-First Social Opportunity Scan**.

If this vertical is resumed and a follow-up outreach test is justified, create a distinct vertical sub-experiment / new experiment ID. Do not reuse or reinterpret EXP-002.

## Current decision

`DORMANT` until stronger comparative evidence justifies taking field time away from EXP-006, EXP-007, EXP-003 or EXP-004.
