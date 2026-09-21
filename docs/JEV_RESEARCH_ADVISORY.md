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
- `automatic_research_dispatch_allowed=false` inside the Jev advisory itself;
- `commercial_promotion_authority=false`;
- `mutates_commercial_state=false`;
- `may_reverse_existing_demotions=false`;
- `may_create_active_candidate=false`;
- `llm_confidence_is_commercial_evidence=false`;
- `UNKNOWN != PASS`.

A Jev recommendation can disagree with an existing engine verdict. That disagreement is diagnostic only. The existing evidence-bound verdict remains authoritative.

Phase 2 explicitly separates:

- `model_research_route` — Jev's raw typed opinion;
- `effective_research_route` — the only route downstream code may consume;
- `effective_route_source` — deterministic engine closure or Jev shadow advisory;
- `route_alignment` — whether Jev agrees with an existing authoritative closure.

If an existing verdict is an authoritative `DEMOTED_ / REJECTED_ / CLOSED_` closure, the effective route is deterministically forced to `NO_FURTHER_RESEARCH` even if Jev suggests something else.

In particular, Jev cannot:

- turn a DEMOTED formation into a retained formation;
- write `active_commercial_candidates`;
- change `first_external_value_flow`;
- bypass `validate_formation`, Attraction Leverage, Drift Audit, Need/Resource/Blocker truth, incumbent hard floors, or any other evidence gate;
- convert confidence/probabilities into commercial evidence.

## Execution

The intended environment is GitHub Actions, not a required local clone.

By default `--scan-json auto` resolves the scan named by `data/commercial_reset_state.json:last_completed_scan_id`. If that file is unavailable it falls back to the highest numbered persisted `attraction_scan_*.json`. This prevents the integration from being frozen on Scan 035 as new scans are persisted.

`.github/workflows/jev-research-advisory.yml` performs:

1. deterministic contract/unit tests;
2. a bounded live Jev shadow run for same-repository PRs or manual dispatch;
3. artifact upload only.

The workflow has `contents: read` permission and contains no persistence-to-main job.

If `TYPESAFE_API_KEY` is unavailable in this repository, the live stage produces a safe `SKIPPED_NO_SECRET` artifact instead of weakening the deterministic checks.

## Current first calibration

The initial bounded input is `ATTRACTION_SCAN_035`, which has six examined formations and zero retained/commercial promotions.

That is intentional. It provides a useful calibration set: Jev can demonstrate research-routing judgment while tests prove it cannot reverse the already-evidenced demotions.

Phase 1 calibration on Scan 035 served `jev-1.13.0` and returned six successful `NO_FURTHER_RESEARCH` routes with zero failures. The individual incumbent-preflight binary question was noisier than the final route, which is why no individual sub-answer can dispatch work.

Phase 2 adds the deterministic effective-route bridge and automatic current-scan resolution. Advisory artifacts remain non-authoritative and are not persisted into commercial truth. Automatic commercial promotion remains outside Jev authority.


## Phase 3 — agent continuation

Jev remains a typed decision gate. It does **not** execute web research, mutate commercial truth, or create a new ChatGPT/web-session turn by itself.

The runner now also writes `jev_continuation_directive.json`. This is a separate control-plane record for an already-running repository agent. It converts the effective Jev route into one of:

- `ADVANCE_TO_NEXT_SCAN` when every evaluated formation is already closed;
- `EXECUTE_RESEARCH_QUEUE` when reversible research remains;
- `STOP_FOR_HUMAN_REVIEW` when Jev returns `HUMAN_REVIEW`, the advisory fails, or the route is not safely executable.

Per-formation actions are bounded to:

- `RUN_EXACT_INCUMBENT_PREFLIGHT`;
- `RUN_CAUSAL_DESCENT`;
- `DROP_FROM_CURRENT_RESEARCH_QUEUE`;
- `REQUIRE_HUMAN_REVIEW`.

The continuation directive explicitly keeps:

- `automatic_research_execution_by_jev=false`;
- `commercial_promotion_authority=false`;
- `mutates_commercial_state=false`;
- `external_side_effects_allowed=false`;
- `may_reverse_existing_demotions=false`;
- `UNKNOWN != PASS`.

The repository-agent rule is different from granting Jev execution authority: when `autonomous_continuation_allowed=true`, an agent that is already working on the repository should consume the directive and continue the next reversible research stage in the **same task/session** instead of returning control merely to ask the user to type “continue”.

A terminated browser session still cannot be resurrected by Jev. Durable recovery remains the responsibility of `state/chatgpt-recovery`, `RECOVERY_STATE.json`, and the per-task recovery checkpoints.
