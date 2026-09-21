# Jev Research Advisory

This integration adds TypeSafe AI Jev as a **shadow research-sequencing second opinion** for the opportunity-routing engine.

It does not add a commercial decision-maker.

## Purpose

Jev receives a compact, persisted attraction-scan record and may answer bounded questions about what research should happen next:

- whether exact incumbent/control-loop preflight is still needed;
- whether deeper causal research could be useful after required preflight;
- research route:
  - `NO_FURTHER_RESEARCH`
  - `EXACT_INCUMBENT_PREFLIGHT`
  - `CAUSAL_DESCENT`
  - `HUMAN_REVIEW`
- relative research-attention priority: `LOW / MEDIUM / HIGH`;
- evidence-state label:
  - `ADEQUATE_FOR_CURRENT_RESEARCH_STAGE`
  - `INSUFFICIENT`
  - `CONFLICTED`
  - `STALE_OR_LINEAGE_UNCLEAR`.

This matches the current Scan 036 research order without turning that order into a permanent business ontology.

## Authority boundary

The contract is fail-closed:

- `authority=SHADOW_RESEARCH_ADVISORY_ONLY`;
- `commercial_promotion_authority=false`;
- `mutates_commercial_state=false`;
- `may_reverse_existing_demotions=false`;
- `may_create_active_candidate=false`;
- `llm_confidence_is_commercial_evidence=false`;
- `UNKNOWN != PASS`.

A Jev recommendation can disagree with an existing engine verdict. That disagreement is diagnostic only. The existing evidence-bound verdict remains authoritative.

In particular, Jev cannot:

- turn a DEMOTED formation into a retained formation;
- write `active_commercial_candidates`;
- change `first_external_value_flow`;
- bypass `validate_formation`, Attraction Leverage, Drift Audit, Need/Resource/Blocker truth, incumbent hard floors, or any other evidence gate;
- convert confidence/probabilities into commercial evidence.

## Execution

The intended environment is GitHub Actions, not a required local clone.

`.github/workflows/jev-research-advisory.yml` performs:

1. deterministic contract/unit tests;
2. a bounded live Jev shadow run for same-repository PRs or manual dispatch;
3. artifact upload only.

The workflow has `contents: read` permission and contains no persistence-to-main job.

If `TYPESAFE_API_KEY` is unavailable in this repository, the live stage produces a safe `SKIPPED_NO_SECRET` artifact instead of weakening the deterministic checks.

## Current first calibration

The initial bounded input is `ATTRACTION_SCAN_035`, which has six examined formations and zero retained/commercial promotions.

That is intentional. It provides a useful calibration set: Jev can demonstrate research-routing judgment while tests prove it cannot reverse the already-evidenced demotions.

A later phase may persist advisory history after enough calibration. Automatic commercial promotion remains outside Jev authority.
